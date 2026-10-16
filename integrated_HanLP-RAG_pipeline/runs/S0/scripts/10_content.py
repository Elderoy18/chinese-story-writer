#!/usr/bin/env python3
"""Step 10 -- the end-of-story content check: is every required scene of the
story told? Run on the test stories and scored against the teacher's own
"Miss ... scene" flags.

    data/02_corpus/corpus.json (samples, scene_lists), data/03_split/split.json
        ->  data/10_content/checks_<split>.jsonl      one story per line, with every run
            reports/10_content_<split>.md
            review/10_content_review.csv              disagreements, for the teacher
            review/10_content_instructions.md

    python scripts/10_content.py --split train   # calibration: 1 run per train story, no review sheet
    python scripts/10_content.py                 # test: 3 runs per story, scored, review sheet

The answer key: each of her "Miss ... scene" phrases is mapped to a scene in
her required-scene list (story_scenes.md) by word overlap -- she wrote her flags
with the same wording as the list. A flag much shorter than its scene ("神农
fainted" for "神农 tried 夹竹桃 and fainted") marks that scene as PARTLY missing.
A required scene she did not flag counts as told.

The check: the whole story, as the app has it after END STORY, plus her scene
list, go to an LLM. For each required scene it names the scene's CORE (key
event + the key things the scene names, e.g. 茶, 夹竹桃, the market) and gives a
verdict -- told / partly (a named key thing or the outcome is missing) /
missing -- with the student's words it relied on (checked by code to occur in
the story). Details (clothing colours, "every day", reasons) are listed
separately and never count as gaps. It also lists statements that contradict
the story, and a short learner-facing note for each gap. Run N_RUNS times per
story; the majority verdict is scored, and the runs show how stable it is.

Prompt calibration was done on the TRAIN stories only (--split train), so the
test stories stay an honest measurement:
  v1: told / partly / missing, "partly" = any element absent. Too strict: it
      called most scenes partly told for missing details she never flags.
  v2: core vs details (above). Better, but still stricter than her (e.g. 肚子疼
      instead of fainting called partly told).
  v3: v2 + her own past decisions per scene from the train stories (versions
      she accepted / flagged), leave-one-out on train.

Scored two ways, since her flags do not say how she treats a half-told scene:
  missing only         -- a "partly" verdict counts as told
  missing + partly     -- a "partly" verdict counts as a gap
"""
import argparse
import csv
import json
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from llm import api_key, cached_json_call, prompt_version

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
SPLIT = ROOT / "data" / "03_split" / "split.json"
OUT_DIR = ROOT / "data" / "10_content"
CACHE = OUT_DIR / "cache"
REPORT = ROOT / "reports" / "10_content.md"
SHEET = ROOT / "review" / "10_content_review.csv"
INSTRUCTIONS = ROOT / "review" / "10_content_instructions.md"

MODEL = "gpt-5.6-terra"
REASONING_EFFORT = "medium"
N_RUNS = 3
WORKERS = 8
N_ACCEPTED, N_FLAGGED = 3, 2   # teacher examples shown per required scene
EXAMPLE_SOURCE = OUT_DIR / "checks_train_v2.jsonl"   # frozen v2 calibration run on train
PART_RATIO = 0.6   # a flag with under 60% of its scene's words marks the scene as partly missing

SYSTEM = """You check whether a learner's Chinese retelling of a traditional story contains every scene the story requires. You judge content only -- not grammar, vocabulary or style, and not how well a scene is written.

You receive the teacher's list of required scenes (in story order, with ids) and the learner's whole story. Under most scenes you also see the teacher's past decisions on OTHER learners' versions of that scene: versions she accepted as told and versions she flagged as missing. They show where her line is -- judge this learner the way she judged them.

For EACH required scene:
1. core: first name the scene's CORE in a few English words -- its key event plus the key things the scene names (a named plant such as 茶 / 夹竹桃 / 灵芝, a place such as the market or the school, an outcome such as fainting or feeling better). Everything else in the scene's description is a DETAIL: clothing colours, how often something happens ("every day"), how a character travels ("climbed mountains"), adjectives ("famous"), and the reasons or thoughts behind an action.
2. verdict:
- told: a reader who knows the story would recognise the core event in the learner's story, even if it is told briefly, in other words, spread over several sentences, combined with another scene, or with details left out or changed. Setting-the-scene openings count as told when the learner gives the situation in any form.
- partly: the core event is there but one of its named key things or its outcome is absent or replaced (e.g. 神农 tries plants but 茶 is never named; he eats a flower but it is not 夹竹桃, or he does not faint; they move, but not to a market).
- missing: the core event is not told at all.
A missing DETAIL never makes a scene partly or missing.
Also give:
- evidence: the learner's words that tell (part of) this scene, as a list of quotes, each copied EXACTLY from the story (one quote per sentence or clause; never join or shorten quotes); [] if missing.
- missing_part: the part of the CORE that is not told, in English ("" if told).
- details_left_out: details of the scene the learner did not tell, in English (may be empty; these are not gaps).
- out_of_order: true if the scene is told in clearly the wrong place in the story's sequence.

Then list wrong_information: statements in the story that contradict the story as the teacher's scenes describe it (e.g. a character who is not in the story, an event that happens differently). Give the learner's words exactly and say what is wrong. Do not list details the learner merely added or simplified.

Finally, feedback: for each scene that is missing or partly told, one short sentence in English addressed to the learner saying what the story still needs and where it belongs -- describe the place by the events around it, never by a scene number. Write Chinese only for character names and short story words. Keep it encouraging and simple; the learner is a beginner."""

SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["scenes", "wrong_information", "feedback"],
    "properties": {
        "scenes": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["id", "core", "verdict", "evidence", "missing_part", "details_left_out", "out_of_order"],
            "properties": {"id": {"type": "string"}, "core": {"type": "string"},
                           "verdict": {"type": "string", "enum": ["told", "partly", "missing"]},
                           "evidence": {"type": "array", "items": {"type": "string"}}, "missing_part": {"type": "string"},
                           "details_left_out": {"type": "array", "items": {"type": "string"}},
                           "out_of_order": {"type": "boolean"}}}},
        "wrong_information": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["learner_text", "problem"],
            "properties": {"learner_text": {"type": "string"}, "problem": {"type": "string"}}}},
        "feedback": {"type": "array", "items": {"type": "string"}},
    },
}
PROMPT_VERSION = prompt_version(SYSTEM, SCHEMA)


# ---------------------------------------------------------------------------
# The answer key: her flags -> scenes of her list
# ---------------------------------------------------------------------------
def words(s):
    """Lower-case English words and single Chinese characters."""
    return re.findall(r"[a-z]+|[一-鿿]", s.lower())


STOP = set("a an the and to of in on at for by his her their it he she they is was are be because how".split())


def map_flag(phrase, scenes):
    """(scene index, part?, coverage) for one 'Miss' phrase."""
    p = [w for w in words(phrase) if w not in STOP]
    best = None
    for i, s in enumerate(scenes):
        sw = [w for w in words(s) if w not in STOP]
        cov = sum(1 for w in set(p) if w in sw) / max(len(set(p)), 1)
        if best is None or cov > best[2]:
            best = (i, len(set(p)) < PART_RATIO * len(set(sw)), cov)
    return best


def gold_for(sample, scenes):
    gold, mapping = ["told"] * len(scenes), []
    for f in sample["content_flags"]:
        if f["type"] != "miss_scene":
            continue
        for phrase in f["scenes"]:
            i, part, cov = map_flag(phrase, scenes)
            gold[i] = "missing" if not part or gold[i] == "missing" else "partly"
            mapping.append({"phrase": phrase, "scene": i, "part": part, "coverage": round(cov, 2)})
    return gold, mapping


# ---------------------------------------------------------------------------
def build_examples():
    """The teacher's own past decisions per required scene, from the TRAIN stories:
    learner versions she accepted as told and versions she flagged. Taken from the
    v2 calibration run (its evidence quotes = what each learner wrote for the
    scene) and her flags. Accepted examples prefer borderline ones -- scenes the
    v2 check wrongly called partly told -- since those show where her line is."""
    rows = [json.loads(l) for l in open(EXAMPLE_SOURCE, encoding="utf-8")]
    ex = {}
    for r in sorted(rows, key=lambda r: r["sample_id"]):
        for i, g in enumerate(r["gold"]):
            v = r["runs"][0]["verdicts"][i]
            quote = "".join(v["evidence"]).strip()
            if not quote or len(quote) > 60:
                continue
            kind = "accepted" if g == "told" else "flagged"
            ex.setdefault((r["story_id"], i), []).append(
                {"sample_id": r["sample_id"], "kind": kind, "text": quote, "borderline": v["verdict"] != "told"})
    out = {}
    for key, items in ex.items():
        acc = sorted([e for e in items if e["kind"] == "accepted"], key=lambda e: (not e["borderline"], len(e["text"])))
        fl = sorted([e for e in items if e["kind"] == "flagged"], key=lambda e: len(e["text"]))
        out[key] = acc[:N_ACCEPTED + 1] + fl[:N_FLAGGED + 1]  # one spare of each, for leave-one-out
    return out


def story_input(scenes, story_text, examples, story_id, sample_id):
    lines = ["required scenes (story order):"]
    for i, s in enumerate(scenes):
        lines.append(f"S{i + 1}: {s}")
        ex = [e for e in examples.get((story_id, i), []) if e["sample_id"] != sample_id]  # never its own label
        acc = [e["text"] for e in ex if e["kind"] == "accepted"][:N_ACCEPTED]
        fl = [e["text"] for e in ex if e["kind"] == "flagged"][:N_FLAGGED]
        if acc or fl:
            lines.append("    the teacher's past decisions on other learners' versions of this scene -- "
                         + (f"accepted as told: {' | '.join(acc)}" if acc else "")
                         + (" ; " if acc and fl else "")
                         + (f"flagged as missing: {' | '.join(fl)}" if fl else ""))
    return "\n".join(lines) + f"\n\nlearner's story:\n{story_text}"


def majority(vs):
    c = Counter(vs).most_common()
    return c[0][0] if len(c) == 1 or c[0][1] > c[1][1] else "partly"  # a tie between verdicts is a half-told scene


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["test", "train"], default="test",
                    help="train: calibration only (1 run per story, no review sheet)")
    args = ap.parse_args()
    runs_n = N_RUNS if args.split == "test" else 1
    corpus = json.load(open(CORPUS, encoding="utf-8"))
    split = json.load(open(SPLIT, encoding="utf-8"))
    samples = {s["sample_id"]: s for s in corpus["samples"]}
    lists = {sl["story_id"]: sl["scenes"] for sl in corpus["scene_lists"]}
    examples = build_examples()

    jobs = []
    if args.split == "test":
        stories = [(samples[t["sample_id"]], "".join(samples[t["sample_id"]]["text"][sc["start"]:sc["end"]] for sc in t["scenes"]))
                   for t in split["test"]]
    else:  # train stories of the stories that have a scene list
        stories = [(samples[i], samples[i]["text"]) for i in split["train"] if samples[i]["story_id"] in lists]
    for s, story_text in stories:
        for run in range(1, runs_n + 1):
            jobs.append((s, story_text, run))

    api_key()
    print(f"{len(jobs)} calls ({len(jobs) // runs_n} {args.split} stories x {runs_n} runs), model {MODEL} ({REASONING_EFFORT}), prompt {PROMPT_VERSION}")
    with ThreadPoolExecutor(WORKERS) as pool:
        results = list(pool.map(lambda j: cached_json_call(
            CACHE, MODEL, REASONING_EFFORT, SYSTEM, SCHEMA, "content_check",
            story_input(lists[j[0]["story_id"]], j[1], examples, j[0]["story_id"], j[0]["sample_id"]), salt=f"run{j[2]}"), jobs))

    per_story, usage = {}, Counter()
    for (s, story_text, run), (rec, _) in zip(jobs, results):
        usage.update({k: v for k, v in rec.get("usage", {}).items() if isinstance(v, int)})
        scenes = lists[s["story_id"]]
        out = rec["output"]
        verdicts = {v["id"]: v for v in out["scenes"]}
        row = per_story.setdefault(s["sample_id"], {"sample": s, "story_text": story_text, "runs": []})
        row["runs"].append({
            "run": run,
            "verdicts": [verdicts.get(f"S{i + 1}", {"verdict": "missing", "evidence": [], "missing_part": "(no verdict returned)",
                                                    "out_of_order": False}) for i in range(len(scenes))],
            "wrong_information": out["wrong_information"], "feedback": out["feedback"],
        })

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    for sid, row in per_story.items():
        s = row["sample"]
        scenes = lists[s["story_id"]]
        gold, mapping = gold_for(s, scenes)
        votes = [[r["verdicts"][i]["verdict"] for r in row["runs"]] for i in range(len(scenes))]
        bad_evidence = sum(1 for r in row["runs"] for v in r["verdicts"] for q in v["evidence"]
                           if q.strip() and q.strip() not in row["story_text"])
        records.append({"sample_id": sid, "story_id": s["story_id"], "gold": gold, "flag_mapping": mapping,
                        "votes": votes, "majority": [majority(v) for v in votes], "runs": row["runs"],
                        "evidence_not_in_story": bad_evidence})
    with open(OUT_DIR / f"checks_{args.split}.jsonl", "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    report = REPORT.with_name(f"10_content_{args.split}.md")
    write_report(records, lists, usage, runs_n, report, args.split)
    if args.split == "test":
        write_sheet(records, lists)
    print(f"tokens {dict(usage)}")
    print(f"Report: {report.relative_to(ROOT)}" + (f"; review sheet: {SHEET.relative_to(ROOT)}" if args.split == "test" else ""))


# ---------------------------------------------------------------------------
def scores(records, pred_of, gap):
    """Counts over every (story, required scene): gold gap vs predicted gap."""
    tp = fp = fn = tn = 0
    for r in records:
        for i, g in enumerate(r["gold"]):
            p = pred_of(r, i) in gap
            t = g != "told"
            tp += p and t
            fp += p and not t
            fn += t and not p
            tn += not p and not t
    return tp, fp, fn, tn


def write_report(records, lists, usage, runs_n, path, split_name):
    pct = lambda a, b: f"{a}/{b} ({100 * a / b:.0f}%)" if b else "0/0"
    n_cells = sum(len(r["gold"]) for r in records)
    gold_gaps = sum(1 for r in records for g in r["gold"] if g != "told")
    L = [f"# Step 10 report: content check (required scenes) -- {split_name}", "",
         f"- model {MODEL} ({REASONING_EFFORT}), prompt {PROMPT_VERSION}, {runs_n} run(s) per story; tokens {dict(usage)}",
         f"- {len(records)} {split_name} stories, {n_cells} required scenes in total; the teacher flagged {gold_gaps} as missing "
         f"({sum(1 for r in records for g in r['gold'] if g == 'partly')} of them only partly)",
         f"- evidence quotes not found in the story: {sum(r['evidence_not_in_story'] for r in records)}", "",
         "## How her flags map onto her scene list", "",
         "| Her flag | Mapped to scene | Part only? | Word overlap |", "|---|---|---|---|"]
    seen = set()
    for r in records:
        for m in r["flag_mapping"]:
            k = (r["story_id"], m["phrase"])
            if k not in seen:
                seen.add(k)
                L.append(f"| {m['phrase']} | {m['scene'] + 1}. {lists[r['story_id']][m['scene']][:60]} | "
                         f"{'yes' if m['part'] else ''} | {m['coverage']} |")

    L += ["", "## Agreement with her flags", "",
          "Per required scene: does the check call it a gap where she flagged it, and not where she did not?", "",
          "| Verdicts used | Counting as a gap | Her gaps found | Check's gaps she also flagged | Scenes where both agree |",
          "|---|---|---|---|---|"]
    for label, pred in [("majority of 3 runs", lambda r, i: r["majority"][i])] + \
            [(f"run {k + 1}", (lambda k: lambda r, i: r["runs"][k]["verdicts"][i]["verdict"])(k)) for k in range(runs_n if runs_n > 1 else 0)]:
        for gap_label, gap in (("missing only", ("missing",)), ("missing + partly", ("missing", "partly"))):
            tp, fp, fn, tn = scores(records, pred, gap)
            L.append(f"| {label} | {gap_label} | {pct(tp, tp + fn)} | {pct(tp, tp + fp)} | {pct(tp + tn, n_cells)} |")

    unstable = sum(1 for r in records for v in r["votes"] if len(set(v)) > 1)
    L += ["", f"Stability: the {runs_n} run(s) gave the same verdict for {pct(n_cells - unstable, n_cells)} required scenes.", "",
          "## Per scene of the story", "", "| Story | Scene | Her flags | Check: missing | Check: partly |", "|---|---|---|---|---|"]
    for story in sorted({r["story_id"] for r in records}):
        rs = [r for r in records if r["story_id"] == story]
        for i, sc in enumerate(lists[story]):
            L.append(f"| {story} | {i + 1}. {sc[:50]} | {sum(1 for r in rs if r['gold'][i] != 'told')} | "
                     f"{sum(1 for r in rs if r['majority'][i] == 'missing')} | {sum(1 for r in rs if r['majority'][i] == 'partly')} |")

    L += ["", "## Wrong information found (majority of runs not required; all runs listed)", ""]
    for r in records:
        items = {(w["learner_text"], w["problem"]) for run in r["runs"] for w in run["wrong_information"]}
        flags = [f["raw"] for f in r["sample"]["content_flags"] if f["type"] == "wrong_information"] if "sample" in r else []
        for t, p in sorted(items):
            L.append(f"- {r['sample_id']}: “{t}” — {p}")
    L += ["", "## Example learner feedback (run 1, first 6 stories)", ""]
    for r in records[:6]:
        L += [f"**{r['sample_id']}**"] + [f"- {f}" for f in r["runs"][0]["feedback"]] + [""]
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Review sheet: where the check and her flags disagree
# ---------------------------------------------------------------------------
COLUMNS = ["row_id", "story", "required_scene", "teacher_flag", "checker_verdict", "checker_runs",
           "student_words_used", "what_checker_says_is_missing", "TEACHER_DECISION", "TEACHER_NOTE"]
HUMAN = ["TEACHER_DECISION", "TEACHER_NOTE"]
SAY = {"told": "told", "partly": "partly told", "missing": "missing"}


def write_sheet(records, lists):
    kept = {}
    if SHEET.exists():
        with open(SHEET, encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                if any(row.get(h) for h in HUMAN):
                    kept[row["row_id"]] = row
    rows = []
    for r in records:
        for i, sc in enumerate(lists[r["story_id"]]):
            g, p = r["gold"][i], r["majority"][i]
            if (g == "told") == (p == "told") and not (g == "missing" and p == "partly"):
                continue
            run1 = next((run["verdicts"][i] for run in r["runs"] if run["verdicts"][i]["verdict"] == p), r["runs"][0]["verdicts"][i])
            row_id = f"{r['sample_id']}#S{i + 1}"
            k = kept.get(row_id, {})
            rows.append([row_id, r["sample_id"], sc,
                         {"told": "not flagged", "partly": "flagged as partly missing", "missing": "flagged as missing"}[g],
                         SAY[p], ", ".join(SAY[v] for v in r["votes"][i]), " / ".join(run1["evidence"]), run1["missing_part"],
                         k.get("TEACHER_DECISION", ""), k.get("TEACHER_NOTE", "")])
    SHEET.parent.mkdir(parents=True, exist_ok=True)
    with open(SHEET, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(COLUMNS)
        w.writerows(rows)
    INSTRUCTIONS.write_text(INSTRUCTIONS_TEXT.format(n=len(rows)), encoding="utf-8")


INSTRUCTIONS_TEXT = """# Content check: places where the checker and the teacher's flags disagree

For each test story, an automatic content check went through the teacher's list of required scenes
and decided whether each scene is told, partly told, or missing. Most of its decisions match the
teacher's "Miss ... scene" notes. The sheet `10_content_review.csv` lists the {n} cases where they do
not, so that the teacher can say which reading is right.

| Column | Meaning |
|---|---|
| story | the student story |
| required_scene | the scene from the teacher's scene list |
| teacher_flag | what the teacher's notes on this story say about the scene |
| checker_verdict | what the content check decided (the most common answer over its 3 tries) |
| checker_runs | its answer in each of the 3 tries |
| student_words_used | the student's words the check relied on, if any |
| what_checker_says_is_missing | the part of the scene the check found missing |

## What to fill in

- **TEACHER_DECISION**: `told`, `partly told`, or `missing` -- the right verdict for this scene in this story.
- **TEACHER_NOTE** (optional): e.g. "half-told scenes are not flagged at this level", or "the student's version counts".

The answers show whether the check is too strict or too lenient, and how half-told scenes should be
treated. Rows already filled in are kept if the sheet is rebuilt.
"""


if __name__ == "__main__":
    main()
