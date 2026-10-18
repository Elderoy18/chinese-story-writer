#!/usr/bin/env python3
"""Consistency of v1 S5, v1 S6 and v2 S0, each run 3 times on the same 18 scenes:

  run to run      -- is the same place flagged every time, with the same
                     correction and category; do the content verdicts agree;
                     how much do the quality numbers move between runs?
  place to place  -- within one run, is the same kind of error (her corrections
                     grouped by category) caught everywhere it occurs, or only
                     at some of its places?

    node eval/run_stage.mjs S5-r2 ; ... S5-r3 ; ... S6-r2 ; ... S6-r3        (once)
    chinese_writing_rag_pipeline_v2/.venv/Scripts/python eval/v1_vs_v2/v2_repeat.py 2 3   (once)
    python eval/v1_vs_v2/consistency.py   -> eval/reports/v1_vs_v2_consistency.md

Uses score.py's parsing and judge (same prompts, same cache).
"""
import json
import statistics
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score as S  # noqa: E402

V2_RUNS = Path(__file__).resolve().parent / "v2_runs"
SYSTEMS = {"v1-S5": ["S5", "S5-r2", "S5-r3"], "v1-S6": ["S6", "S6-r2", "S6-r3"], "v2-S0": ["S0", "r2", "r3"]}
CATEGORIES = S.V2 / "data" / "11_categories" / "edits_test.jsonl"
REPORT = S.REPO / "eval" / "reports" / "v1_vs_v2_consistency.md"


def run_label(system, run):
    return system if run in ("S5", "S6", "S0") else f"{system}-{run}"


def load():
    ts = {s["sample_id"]: s for s in json.load(open(S.TEST_SET, encoding="utf-8"))["samples"]}
    corpus = json.load(open(S.CORPUS, encoding="utf-8"))
    csamples = {s["sample_id"]: s for s in corpus["samples"]}
    scene_lists = {s["story_id"]: s for s in corpus["scene_lists"]}
    key = defaultdict(list)
    for l in open(S.KEY, encoding="utf-8"):
        e = json.loads(l)
        key[e["sample_id"]].append(e)
    v2 = {"S0": S.V2 / "runs" / "S0" / "feedback.json", "r2": V2_RUNS / "r2" / "feedback.json",
          "r3": V2_RUNS / "r3" / "feedback.json"}
    v2 = {k: {d["sample_id"]: d for d in json.load(open(p, encoding="utf-8"))} for k, p in v2.items()}
    jobs = []
    for sid, s in ts.items():
        cs = csamples[sid]
        sl = scene_lists[cs["story_id"]]
        smp = {"sample_id": sid, "text": cs["text"], "scenes": s["scenes"], "content_flags": cs["content_flags"],
               "scene_list": sl["scenes"], "title": sl["title"]}
        for system, runs in SYSTEMS.items():
            for run in runs:
                out = S.load_v2(v2[run][sid]) if system.startswith("v2") else S.load_v1(run, sid, s["scenes"])
                jobs.append((run_label(system, run), smp, out))
    with ThreadPoolExecutor(8) as pool:
        recs = [r for rs in pool.map(lambda j: S.build(j[0], j[1], j[2], key), jobs) for r in rs]
    return ts, key, recs


def clusters(items_by_run):
    """Group overlapping items across runs (one scene) -> list of {run: [items]}."""
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


def pct(a, b):
    return f"{a}/{b} ({100 * a / b:.0f}%)" if b else "–"


def share(a, b):
    return f"{100 * a / b:.0f}%" if b else "–"


def run_to_run(system, labels, ts, key, recs):
    items = [r for r in recs if r["kind"] == "item" and r["system"] in labels]
    by_scene = defaultdict(lambda: defaultdict(list))
    for r in items:
        by_scene[(r["sample_id"], r["scene"])][r["system"]].append(r)
    n_by, bad_by = Counter(), Counter()
    same_fix = same_cat = 0
    singles = []
    for sc, per_run in sorted(by_scene.items()):
        for g in clusters(per_run):
            k = len(g)
            n_by[k] += 1
            its = [it for v in g.values() for it in v]
            bad_by[k] += any(S.item_flags(it)["false_positive"] or S.item_flags(it)["incorrect"] for it in its)
            if k == 3:
                same_fix += len({S.squash(v[0]["after"] or "") for v in g.values()}) == 1
                same_cat += len({v[0]["section"] for v in g.values()}) == 1
            if k == 1:
                run, v = next(iter(g.items()))
                singles.append((sc, run, v[0]))
    errs = [e for sid in ts for e in key[sid] if e["op"] in ("replace", "delete", "insert") and e["start"] is not None]
    caught = Counter(sum(any(S.overlaps(r["span"], e) for r in items if r["system"] == lab and r["sample_id"] == e["sample_id"])
                         for lab in labels) for e in errs)
    content = defaultdict(dict)
    for r in recs:
        if r["kind"] == "content" and r["system"] in labels:
            content[r["sample_id"]][r["system"]] = {s["n"]: s["system"] for s in r["judge"]["scenes"]}
    c_agree = c_tot = 0
    for per in content.values():
        for n in per[labels[0]]:
            c_tot += 1
            c_agree += len({per[lab].get(n) for lab in labels}) == 1
    ms = [S.metrics([r for r in recs if r["system"] == lab], key, list(ts), 18) for lab in labels]
    return {"places": sum(n_by.values()), "n_by": n_by, "bad_by": bad_by, "same_fix": same_fix, "same_cat": same_cat,
            "caught": caught, "n_errs": len(errs), "content": (c_agree, c_tot), "metrics": ms, "singles": singles,
            "items_per_run": [m["items"] for m in ms]}


def spread(vals, fmt="{:.2f}"):
    return f"{fmt.format(statistics.mean(vals))} ({fmt.format(min(vals))}–{fmt.format(max(vals))})"


def main():
    ts, key, recs = load()
    R = {system: run_to_run(system, [run_label(system, r) for r in runs], ts, key, recs) for system, runs in SYSTEMS.items()}
    names = list(SYSTEMS)
    row = lambda label, f: f"| {label} | " + " | ".join(f(R[s]) for s in names) + " |"
    L = ["# Consistency: v1 S5, v1 S6 and v2, each run 3 times", "",
         "Same 6 stories / 18 scenes as `v1_vs_v2.md`. Repeat runs use identical inputs: v1 stages "
         "`S5-r2/-r3`, `S6-r2/-r3` (aliases in `eval/stages.json`); v2 runs 2-3 from `eval/v1_vs_v2/v2_repeat.py` "
         "(LLM finder run k, explanation and enrichment re-run, content-check run k; the GEC model and teacher "
         "patterns are deterministic). All judged with the same judge and prompts as `v1_vs_v2.md`.", "",
         "## 1. Run to run", "",
         "A **place** is a stretch of the student's text flagged in at least one run (overlapping items across runs "
         "count as one place).", "",
         "| | " + " | ".join(names) + " |", "|---|" + "---|" * len(names),
         row("Items per run", lambda r: " / ".join(map(str, r["items_per_run"]))),
         row("Places flagged in all 3 runs", lambda r: pct(r["n_by"][3], r["places"])),
         row("Places flagged in only 1 run", lambda r: pct(r["n_by"][1], r["places"])),
         row("&nbsp;&nbsp;of which wrong (false positive or incorrect)", lambda r: pct(r["bad_by"][1], r["n_by"][1])),
         row("Places in all 3 runs that are wrong", lambda r: pct(r["bad_by"][3], r["n_by"][3])),
         row("Places in all 3 runs: **same corrected text** every time", lambda r: pct(r["same_fix"], r["n_by"][3])),
         row("Places in all 3 runs: same section every time", lambda r: pct(r["same_cat"], r["n_by"][3])),
         row("Her corrections caught in all 3 runs", lambda r: pct(r["caught"][3], r["n_errs"])),
         row("Her corrections caught in some runs only", lambda r: pct(r["caught"][1] + r["caught"][2], r["n_errs"])),
         row("Content: required scenes with the same verdict in all 3 runs", lambda r: pct(*r["content"])),
         "", "Quality numbers across the 3 runs, mean (lowest–highest):", "",
         "| | " + " | ".join(names) + " |", "|---|" + "---|" * len(names),
         row("False positives / scene", lambda r: spread([m["fp"] / 18 for m in r["metrics"]])),
         row("Incorrect corrections / scene", lambda r: spread([m["incorrect"] / 18 for m in r["metrics"]])),
         row("Items fully right", lambda r: spread([100 * m["clean"] / m["items"] for m in r["metrics"]], "{:.0f}%")),
         row("Corrected text not fully correct", lambda r: spread([100 * m["after_bad"] / m["with_after"] for m in r["metrics"]], "{:.0f}%")),
         row("Partial sentences", lambda r: spread([100 * m["partial"] / m["items"] for m in r["metrics"]], "{:.0f}%")),
         row("Wrong category", lambda r: spread([100 * m["miscat"] / m["items"] for m in r["metrics"]], "{:.0f}%")),
         row("Her flagged scenes caught (content)", lambda r: spread([100 * m["content"]["caught"] / m["content"]["her_flagged"] for m in r["metrics"]], "{:.0f}%")),
         row("Recall of her corrections", lambda r: spread([100 * m["recall"][0] / m["recall"][1] for m in r["metrics"]], "{:.0f}%")),
         ""]

    # ---------------- place to place
    cat_of = {json.loads(l)["edit_id"]: json.loads(l).get("category") for l in open(CATEGORIES, encoding="utf-8")}
    errs = [e for sid in ts for e in key[sid] if e["op"] in ("replace", "delete", "insert") and e["start"] is not None]
    groups = defaultdict(list)
    for e in errs:
        c = cat_of.get(e["edit_id"])
        if c and c != "other":
            groups[c].append(e)
    groups = {c: es for c, es in groups.items() if len(es) >= 2}
    items = [r for r in recs if r["kind"] == "item"]
    labels = [run_label(s, r) for s, runs in SYSTEMS.items() for r in runs]
    detail, tally = defaultdict(dict), {lab: Counter() for lab in labels}
    for c, es in groups.items():
        for lab in labels:
            hit = [any(S.overlaps(r["span"], e) for r in items if r["system"] == lab and r["sample_id"] == e["sample_id"]) for e in es]
            tally[lab]["all" if all(hit) else ("none" if not any(hit) else "mixed")] += 1
            detail[c][lab] = sum(hit)
    L += ["## 2. Same kind of error, different places", "",
          f"Her corrections grouped by error category (v2's draft category labels on her edits; {len(groups)} categories "
          "with 2+ corrections in these stories). A category is **mixed** in a run when the run catches some of its "
          "places but not others.", "",
          "| | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    for state, label in (("all", "Categories caught at every place"), ("mixed", "Mixed"), ("none", "None caught")):
        L.append(f"| {label} (per run) | " + " | ".join(
            " / ".join(str(tally[run_label(s, r)][state]) for r in SYSTEMS[s]) for s in names) + " |")
    L += ["", "Places caught per category, runs 1 / 2 / 3:", "",
          "| Category | Her corrections | " + " | ".join(names) + " |", "|---|---|" + "---|" * len(names)]
    for c, es in sorted(groups.items(), key=lambda x: -len(x[1])):
        L.append(f"| {c} | {len(es)} | " + " | ".join(
            " / ".join(str(detail[c][run_label(s, r)]) for r in SYSTEMS[s]) for s in names) + " |")

    # ---------------- unstable places
    L += ["", "## 3. Places flagged in only one run", ""]
    for s in names:
        L += [f"### {s}", ""]
        for sc, run, it in R[s]["singles"]:
            x = S.item_flags(it)
            verdict = "false positive" if x["false_positive"] else ("incorrect" if x["incorrect"] else "ok")
            L.append(f"- {sc[0]} scene {sc[1]} ({run}) [{it['section']}] `{it['shown'][:100]}` -- {verdict}")
        L.append("")
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {REPORT.relative_to(S.REPO)}")


if __name__ == "__main__":
    main()
