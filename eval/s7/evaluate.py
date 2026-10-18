#!/usr/bin/env python3
"""S7 measurement harness: accuracy, consistency and retrieval of one stage,
from its repeated runs on the 20-story test set.

    python eval/s7/evaluate.py S6-h20 S6-h20-r2 S6-h20-r3 [--name S6-h20]
        -> eval/reports/S7_<name>.md, eval/s7/out/<name>.json

Every run is scored with the judge of eval/v1_vs_v2/score.py (same prompts and
cache; strict in her way, given her corrections on each scene and her written
rules; where she corrected a place it is a real error whatever the judge says).
Answer key: her aligned edits in eval/test_set_h20.json (the one edit she
rejected in her review is left out).

Measures (eval/S7_plan.md, Phase 2):
  Accuracy, per run, mean (lowest-highest) over the runs -- in her order:
    false positives / scene, incorrect corrections / scene, items fully right,
    corrected text not fully correct, partial sentences, content scenes caught,
    expressiveness, recall (last).
  Consistency across the runs (same input, same retrieval):
    places flagged in every run; lexical = identical Chinese corrected text
    (explanation text stripped); information = the judge says every run names
    the same error with an equivalent fix (her alternatives count as equal).
  Retrieval:
    Jaccard of retrieved chunk ids between runs, per scene;
    card reach = for each of her corrections, is the rule card for its rule in
    the prompt (searched or pinned)? -- and per rule, at how many of its places.
  Attribution, per her correction: retrieval miss / ignored / misapplied / right.
"""
import argparse
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "eval" / "v1_vs_v2"))
import score as S  # noqa: E402  (parsing + judge, shared with the v1-vs-v2 report)

RUNS = REPO / "eval" / "runs"
OUT = HERE / "out"

# Judge prompts OpenAI's content filter refuses (a story about poisonous plants can
# trip it). The scene (or the story's content check) is then left out of the
# metrics for every run, so stages stay comparable; the report lists it.
REFUSED = set()  # ("scene", scene_text) / ("expr", scene_text) / ("content", story_text)
REFUSED_LOG = OUT / "refused.json"  # every refusal seen in any evaluation: left out of all of them


def load_refused():
    if REFUSED_LOG.exists():
        REFUSED.update(tuple(x) for x in json.load(open(REFUSED_LOG, encoding="utf-8")))


def save_refused():
    OUT.mkdir(exist_ok=True)
    json.dump(sorted(REFUSED), open(REFUSED_LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _refusable(kind, judge, key_arg):
    def wrapped(*args):
        try:
            return judge(*args)
        except RuntimeError as e:
            if "flagged" not in str(e) and "invalid_prompt" not in str(e):
                raise
            REFUSED.add((kind, args[key_arg]))
            return {"scenes": [], "notes": []} if kind == "content" else {}
    return wrapped


S.judge_scene = _refusable("scene", S.judge_scene, 1)      # (earlier, scene_text, edits, items)
S.judge_expr = _refusable("expr", S.judge_expr, 2)         # (title, earlier, scene_text, ideas)
S.judge_content = _refusable("content", S.judge_content, 1)  # (scene_list, story_text, flags, notes)


def drop_refused(recs, test_set):
    """Remove records whose judge prompt was refused -- for all runs alike."""
    scene_of = {(s["sample_id"], i + 1): sc for s in test_set["samples"] for i, sc in enumerate(s["scenes"])}
    text_of = {s["sample_id"]: s["raw_text"] for s in test_set["samples"]}
    def refused(r):
        if r["kind"] == "item":
            return ("scene", scene_of[(r["sample_id"], r["scene"])]) in REFUSED
        if r["kind"] == "expr":
            return ("expr", scene_of[(r["sample_id"], r["scene"])]) in REFUSED
        return ("content", text_of[r["sample_id"]]) in REFUSED
    return [r for r in recs if not refused(r)]

INFO_SYSTEM = """You compare feedback items that the same automatic system gave, in separate runs, about the same place in one scene a learner of Chinese wrote. You get the scene, the teacher's corrections on it (reference), and one item per run (some runs may have flagged nothing there).

Return:
- same_error: true if every run's item points at the same error (or the same set of errors) in the learner's words.
- equivalent_fix: true if every run's corrected text is correct and fixes that error in a way the teacher would accept as the same fix -- different wording counts as equivalent when each is a correct fix of the same problem (she often accepts alternatives, e.g. 怕/担心). false if any run fixes a different error, leaves the error, or introduces a new one.
- reason: one short sentence."""

INFO_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["same_error", "equivalent_fix", "reason"],
    "properties": {"same_error": {"type": "boolean"}, "equivalent_fix": {"type": "boolean"}, "reason": {"type": "string"}},
}


def clean_after(after):
    """v1's corrected text sometimes runs into its English explanation
    ('让妈妈很着急，害得 requires ...'): keep the Chinese correction only."""
    if after is None:
        return None
    m = re.search(r"[A-Za-z]", after)
    if m:
        after = after[:m.start()]
        after = after[:after.rfind("，")] if "，" in after else after
    return S.squash(after)


def load_key(test_set):
    key = defaultdict(list)
    for s in test_set["samples"]:
        for e in s["gold"]["aligned_edits"]:
            if e["her_decision"] == "no":
                continue  # her review rejected this edit
            key[s["sample_id"]].append({**e, "sample_id": s["sample_id"], "teacher_line": e["her_line"],
                                        "teacher_piece": e["her_piece"], "teacher_note": e["her_note"]})
    return key


def scene_offsets(text, scenes):
    out, pos = [], 0
    for sc in scenes:
        pos = text.index(sc, pos)
        out.append((pos, pos + len(sc)))
        pos += len(sc)
    return out


def run_one(run, test_set, key, scene_lists):
    """Judge one run of a stage on every story -> (item/expr/content records, retrieved ids per scene)."""
    recs, retrieved = [], {}
    def one(s):
        r = json.load(open(RUNS / run / f"{s['sample_id'].replace('#', '_')}.json", encoding="utf-8"))
        for sc in r["scenes"]:
            retrieved[(s["sample_id"], sc["scene"])] = sc["retrieved"]
        sl = scene_lists[s["story_id"]]
        smp = {"sample_id": s["sample_id"], "text": s["raw_text"], "scenes": s["scenes"],
               "content_flags": [{"raw": f} for f in s["gold"]["content_flags"]], "scene_list": sl["scenes"], "title": sl["title"]}
        return S.build(run, smp, S.load_v1(run, s["sample_id"], s["scenes"]), key)
    with ThreadPoolExecutor(8) as pool:
        for rs in pool.map(one, test_set["samples"]):
            recs += rs
    return recs, retrieved


def info_judge(scene_text, edits, items):
    user = (f"Scene:\n{scene_text}\n\nThe teacher's corrections on this scene:\n{S.her_corrections_text(edits)}\n\n"
            "The system's item in each run:\n" +
            "\n".join(f"Run {i + 1}: {it['shown'] if it else '(nothing flagged here)'}" for i, it in enumerate(items)))
    try:
        rec, _ = S.cached_json_call(S.CACHE, S.MODEL, S.EFFORT, INFO_SYSTEM, INFO_SCHEMA, "info_consistency", user)
    except RuntimeError as e:
        if "flagged" not in str(e) and "invalid_prompt" not in str(e):
            raise
        return {"same_error": None, "equivalent_fix": None, "reason": "judge prompt refused by the content filter"}
    out = dict(rec["output"])
    out["reason"] = re.split(r"[}】]|</", out["reason"])[0].strip()  # the judge occasionally appends junk
    return out


def clusters(items_by_run):
    flat = [(run, it) for run, its in items_by_run.items() for it in its if it["span"]]
    parent = list(range(len(flat)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            a, b = flat[i][1]["span"], flat[j][1]["span"]
            if a[0] < b[1] and b[0] < a[1]:
                parent[find(i)] = find(j)
    groups = defaultdict(lambda: defaultdict(list))
    for i, (run, it) in enumerate(flat):
        groups[find(i)][run].append(it)
    return list(groups.values())


def consistency(runs, recs, test_set, key):
    items = [r for r in recs if r["kind"] == "item"]
    texts = {s["sample_id"]: s for s in test_set["samples"]}
    by_scene = defaultdict(lambda: defaultdict(list))
    for r in items:
        by_scene[(r["sample_id"], r["scene"])][r["system"]].append(r)
    places, jobs = [], []
    for (sid, sc), per_run in sorted(by_scene.items()):
        s = texts[sid]
        lo, hi = scene_offsets(s["raw_text"], s["scenes"])[sc - 1]
        edits = [e for e in key[sid] if e["start"] is not None and lo <= e["start"] <= hi]
        for g in clusters(per_run):
            row = [g[run][0] if run in g else None for run in runs]
            n = sum(x is not None for x in row)
            lexical = n == len(runs) and len({clean_after(x["after"]) for x in row}) == 1
            places.append({"sample_id": sid, "scene": sc, "n_runs": n, "lexical": lexical,
                           "wrong_any": any(x and (S.item_flags(x)["false_positive"] or S.item_flags(x)["incorrect"]) for x in row),
                           "shown": [x["shown"] if x else None for x in row]})
            if n >= 2:
                jobs.append((len(places) - 1, s["scenes"][sc - 1], edits, row))
    with ThreadPoolExecutor(8) as pool:
        for (i, *_), out in zip(jobs, pool.map(lambda j: info_judge(*j[1:]), jobs)):
            places[i]["info"] = out
    return places


def attribution(run, recs, retrieved, test_set, key, cards):
    """Per her correction line: was its rule card in the prompt, was it caught, was the fix right."""
    items = [r for r in recs if r["kind"] == "item" and r["system"] == run]
    rows = []
    for s in test_set["samples"]:
        offs = scene_offsets(s["raw_text"], s["scenes"])
        by_line = defaultdict(list)
        for e in key[s["sample_id"]]:
            if e["start"] is not None and e["op"] in ("replace", "delete", "insert"):
                by_line[e["teacher_line"]].append(e)
        for g in s["gold"]["corrections"]:
            edits = by_line.get(g["text"])
            if not edits:
                continue
            sc = next(i + 1 for i, (lo, hi) in enumerate(offs) if lo <= edits[0]["start"] <= hi)
            want = [f"rule_card:{r}" for r in g["rules"] if f"rule_card:{r}" in cards]
            got = set(retrieved[(s["sample_id"], sc)])
            hit = [r for r in items if r["sample_id"] == s["sample_id"] and r["scene"] == sc
                   and any(S.overlaps(r["span"], e) for e in edits)]
            right = any(not S.item_flags(r)["incorrect"] and not S.item_flags(r)["after_not_correct"] for r in hit)
            card_in = bool(want) and any(w in got for w in want)
            if not want:
                blame = "no card for this rule"
            elif not hit:
                blame = "generation: card there, error missed" if card_in else "retrieval: card not there, error missed"
            elif not right:
                blame = "generation: card there, fix wrong" if card_in else "retrieval: card not there, fix wrong"
            else:
                blame = "right" + ("" if card_in else " (without its card)")
            rows.append({"sample_id": s["sample_id"], "scene": sc, "line": g["text"], "rules": g["rules"],
                         "cards_wanted": want, "card_in_prompt": card_in, "caught": bool(hit), "fix_right": right,
                         "blame": blame})
    return rows


def spread(vals, fmt="{:.2f}"):
    vals = [v for v in vals if v is not None]
    if not vals:
        return "–"
    return f"{fmt.format(statistics.mean(vals))} ({fmt.format(min(vals))}–{fmt.format(max(vals))})"


def pct(a, b):
    return f"{a}/{b} ({100 * a / b:.0f}%)" if b else "–"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+", help="stage ids of the repeated runs, e.g. S6-h20 S6-h20-r2 S6-h20-r3")
    ap.add_argument("--name", help="report name (default: first run id)")
    ap.add_argument("--test-set", default="eval/test_set_h20.json")
    args = ap.parse_args()
    name = args.name or args.runs[0]
    test_set = json.load(open(REPO / args.test_set, encoding="utf-8"))
    key = load_key(test_set)
    corpus = json.load(open(S.CORPUS, encoding="utf-8"))
    scene_lists = {s["story_id"]: s for s in corpus["scene_lists"]}
    snapshot = json.load(open(RUNS / args.runs[0] / "stage.json", encoding="utf-8"))["snapshot"]
    cards = {json.loads(l)["chunk_id"] for l in open(REPO / "eval" / "snapshots" / snapshot / "chunks.jsonl", encoding="utf-8")
             if '"chunk_type": "rule_card"' in l}
    sids = [s["sample_id"] for s in test_set["samples"]]
    n_scenes = sum(len(s["scenes"]) for s in test_set["samples"])

    load_refused()
    raw, retrieved, M, attr = {}, {}, {}, {}
    for run in args.runs:
        raw[run], retrieved[run] = run_one(run, test_set, key, scene_lists)
        print(f"{run}: judged {sum(x['kind'] == 'item' for x in raw[run])} items")
    save_refused()
    refused_scenes = sorted({(s["sample_id"], i + 1) for s in test_set["samples"] for i, sc in enumerate(s["scenes"])
                             if ("scene", sc) in REFUSED})
    n_scored = n_scenes - len(refused_scenes)
    recs = []
    for run in args.runs:
        r = drop_refused(raw[run], test_set)
        recs += r
        M[run] = S.metrics(r, key, sids, n_scored)
        attr[run] = [a for a in attribution(run, r, retrieved[run], test_set, key, cards)
                     if (a["sample_id"], a["scene"]) not in refused_scenes]
    places = consistency(args.runs, recs, test_set, key)

    # retrieval: Jaccard between runs, card reach per rule (first run)
    jac = [len(set(retrieved[a][k]) & set(retrieved[b][k])) / len(set(retrieved[a][k]) | set(retrieved[b][k]))
           for a, b in combinations(args.runs, 2) for k in retrieved[a]]
    reach = defaultdict(lambda: [0, 0])
    for row in attr[args.runs[0]]:
        for c in row["cards_wanted"]:
            reach[c][1] += 1
            reach[c][0] += c in retrieved[args.runs[0]][(row["sample_id"], row["scene"])]

    full = [p for p in places if p["n_runs"] == len(args.runs)]
    info_ok = [p for p in full if p.get("info", {}).get("same_error") and p.get("info", {}).get("equivalent_fix")]
    L = [f"# S7 measurement: {name}", "",
         f"Runs: {', '.join(args.runs)} -- snapshot `{snapshot}`, test set `{args.test_set}` "
         f"({len(sids)} stories, {n_scenes} scenes). Judge {S.MODEL} ({S.EFFORT}), prompts as `eval/v1_vs_v2/score.py`.", "",
         f"Scenes left out because the judge prompt was refused by OpenAI's content filter (all runs alike): "
         f"{', '.join(f'{a} scene {b}' for a, b in refused_scenes) or 'none'}; scored scenes: {n_scored}. "
         f"Other refusals: {sorted(k for k, _ in REFUSED if k != 'scene') or 'none'}.", "",
         "## Accuracy (her order of priority), mean (lowest–highest) over the runs", "",
         "| | |", "|---|---|",
         f"| False positives / scene | {spread([m['fp'] / n_scored for m in M.values()])} |",
         f"| Incorrect corrections / scene | {spread([m['incorrect'] / n_scored for m in M.values()])} |",
         f"| Items fully right | {spread([100 * m['clean'] / m['items'] for m in M.values()], '{:.0f}%')} |",
         f"| Corrected text not fully correct | {spread([100 * m['after_bad'] / m['with_after'] for m in M.values() if m['with_after']], '{:.0f}%')} |",
         f"| Partial sentences | {spread([100 * m['partial'] / m['items'] for m in M.values()], '{:.0f}%')} |",
         f"| Items in Other / Content | {spread([100 * m['invalid_cat'] / m['items'] for m in M.values()], '{:.0f}%')} |",
         f"| Wrong category (Grammar & Vocabulary as one) | {spread([100 * m['miscat_coarse'] / m['items'] for m in M.values()], '{:.0f}%')} |",
         f"| Her flagged scenes caught (content) | {spread([100 * m['content']['caught'] / m['content']['her_flagged'] for m in M.values() if m['content']['her_flagged']], '{:.0f}%')} |",
         f"| Content notes worded 'miss…' / 'need…' | {spread([100 * m['content']['notes_miss_need'] / m['content']['notes'] for m in M.values() if m['content']['notes']], '{:.0f}%')} |",
         f"| Good expressiveness ideas: 孟母 | {spread([100 * m['expr']['mengmu'][0] / m['expr']['mengmu'][1] for m in M.values() if m['expr']['mengmu'][1]], '{:.0f}%')} |",
         f"| Good expressiveness ideas: 神农 | {spread([100 * m['expr']['shennong'][0] / m['expr']['shennong'][1] for m in M.values() if m['expr']['shennong'][1]], '{:.0f}%')} |",
         f"| Recall of her corrections | {spread([100 * m['recall'][0] / m['recall'][1] for m in M.values()], '{:.0f}%')} |",
         f"| Items per run | {' / '.join(str(m['items']) for m in M.values())} |", "",
         "## Consistency across the runs (same input, same retrieval)", "",
         "| | |", "|---|---|",
         f"| Places flagged in every run | {pct(len(full), len(places))} |",
         f"| Places flagged in only one run | {pct(sum(p['n_runs'] == 1 for p in places), len(places))} |",
         f"| &nbsp;&nbsp;of which wrong (false positive or incorrect) | {pct(sum(p['wrong_any'] for p in places if p['n_runs'] == 1), sum(p['n_runs'] == 1 for p in places))} |",
         f"| Places in every run: **lexical** (identical corrected text) | {pct(sum(p['lexical'] for p in full), len(full))} |",
         f"| Places in every run: **information** (same error, equivalent fix) | {pct(len(info_ok), len(full))} |",
         f"| Places in every run: same error identified | {pct(sum(bool(p.get('info', {}).get('same_error')) for p in full), len(full))} |", "",
         "## Retrieval", "",
         f"- Jaccard of retrieved chunks between runs, per scene: min {min(jac):.2f}, mean {statistics.mean(jac):.2f} "
         f"({len(jac)} pairs) -- 1.0 = every run saw the same chunks, so any run-to-run difference is the model's.",
         f"- **Card reach**: her corrections whose rule card was in the prompt: "
         f"{pct(sum(r['card_in_prompt'] for r in attr[args.runs[0]] if r['cards_wanted']), sum(bool(r['cards_wanted']) for r in attr[args.runs[0]]))}.",
         "", "Rule cards by how many of their places they reached (run 1; rules with 2+ places):", "",
         "| Rule card | Reached / places |", "|---|---|"]
    for c, (got, tot) in sorted(reach.items(), key=lambda x: (x[1][0] / x[1][1], -x[1][1])):
        if tot >= 2:
            L.append(f"| {c.split(':', 1)[1]} | {got}/{tot} |")
    L += ["", "## Attribution: why her corrections were missed or got a wrong fix", "",
          "| | " + " | ".join(args.runs) + " |", "|---|" + "---|" * len(args.runs)]
    labels = sorted({r["blame"] for rows in attr.values() for r in rows})
    for b in labels:
        L.append(f"| {b} | " + " | ".join(str(sum(r['blame'] == b for r in attr[run])) for run in args.runs) + " |")
    L += ["", "(Blame needs her correction's rule card: 'retrieval' = the card was not in the prompt; "
          "'generation' = it was, and the model missed or misapplied it.)", "",
          "## Places flagged in only some runs, or with different fixes", ""]
    for p in places:
        if p["n_runs"] < len(args.runs) or not (p.get("info", {}).get("same_error") and p.get("info", {}).get("equivalent_fix")):
            L.append(f"- {p['sample_id']} scene {p['scene']} ({p['n_runs']}/{len(args.runs)} runs)"
                     + (f" -- {p['info']['reason']}" if p.get("info") else ""))
            for i, sh in enumerate(p["shown"]):
                L.append(f"  - run {i + 1}: {sh[:140] if sh else '—'}")
    report = REPO / "eval" / "reports" / f"S7_{name}.md"
    report.write_text("\n".join(L) + "\n", encoding="utf-8")
    OUT.mkdir(exist_ok=True)
    json.dump({"runs": args.runs, "snapshot": snapshot, "metrics": M, "places": places, "attribution": attr,
               "jaccard": jac, "card_reach": reach}, open(OUT / f"{name}.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1, default=str)
    print(f"wrote {report.relative_to(REPO)}")


if __name__ == "__main__":
    main()
