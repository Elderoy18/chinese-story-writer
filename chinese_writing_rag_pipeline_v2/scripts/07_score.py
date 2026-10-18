#!/usr/bin/env python3
"""Step 7 -- score a finder against the answer key.

    data/05_align/edits_test.jsonl + review/05_align_test.csv   (answer key)
    data/<finder>/candidates.jsonl                              (finder output)
        ->  reports/07_score_<finder>.md

    python scripts/07_score.py                      # scores 06_find_baseline
    python scripts/07_score.py <finder folder name> # any later finder
    python scripts/07_score.py <finder> <finder>    # several together: union + what each finds alone

Answer key: the teacher's error edits on the test stories (insert / delete /
replace), minus anything marked wrong/drop in the review sheet and anything the
aligner could not place. Her comment edits (e.g. "introduce 孟子 when he first
appears") are scored separately: they mark a problem, not an exact change.

Matching is by position: a teacher edit is FOUND if a candidate in the same
story overlaps it. An insertion point counts as the characters either side of
it, so "insert 了 after 买" matches a candidate at 买 or right after it.
For found edits we also check whether the finder proposed the SAME correction.

Recall    = teacher edits found / teacher edits.
Unmatched = candidates that match no teacher edit. These are NOT necessarily
            wrong -- the teacher does not mark every error -- so they are listed
            for review rather than counted as mistakes.
Stability = for each teacher edit, in how many of the runs it was found.
"""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEY = ROOT / "data" / "05_align" / "edits_test.jsonl"
REVIEW = ROOT / "review" / "05_align_test.csv"
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
ERROR_OPS = ("insert", "delete", "replace")
REJECT = ("wrong", "drop", "no")
PUNCT = re.compile(r"[\s，。！？、；：,.!?;:“”‘’\"'（）()…]")


def load_key():
    rejected = set()
    if REVIEW.exists():
        with open(REVIEW, encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                if row.get("DECISION", "").strip().lower() in REJECT:
                    rejected.add(row["item_id"])
    edits = [json.loads(l) for l in open(KEY, encoding="utf-8")]
    item = lambda e: e["edit_id"].rsplit("/e", 1)[0]
    key = [e for e in edits if e["start"] is not None and e["op"] != "unplaceable" and item(e) not in rejected]
    return key, len(edits) - len(key), len(rejected)


def span(e):
    s, t = e["start"], e["end"]
    return (s - 1, s + 1) if s == t else (s, t)


def overlaps(a, b):
    (a0, a1), (b0, b1) = span(a), span(b)
    return a0 < b1 and b0 < a1


bare = lambda s: PUNCT.sub("", s or "")


def show(text, e):
    s, t = e["start"], e["end"]
    lo = max(text.rfind("，", 0, s), text.rfind("。", 0, s)) + 1
    ends = [i for i in (text.find("，", t), text.find("。", t)) if i >= 0]
    hi = min(ends) if ends else len(text)
    mid = {"comment": f"⟦{text[s:t]}⟧", "insert": f"[+{e['corrected']}]", "delete": f"[-{e['original']}]"}.get(
        e["op"], f"[{e['original']}→{e['corrected']}]")
    return text[lo:s] + mid + text[t:hi]


def load_finders(names):
    """Candidates of one or more finders; with several, runs are labelled <finder>:<run>."""
    cands, infos = [], {}
    for name in names:
        infos[name] = json.load(open(ROOT / "data" / name / "run_info.json", encoding="utf-8"))
        for line in open(ROOT / "data" / name / "candidates.jsonl", encoding="utf-8"):
            c = json.loads(line)
            c["finder"] = name
            if len(names) > 1:
                c["run"] = f"{name}:{c['run']}"
            cands.append(c)
    return cands, infos


def main():
    names = sys.argv[1:] or ["06_find_baseline"]
    finder = "+".join(names)
    cands, infos = load_finders(names)
    info = {"model": " + ".join(i["model"] for i in infos.values()),
            "reasoning_effort": " / ".join(str(i["reasoning_effort"]) for i in infos.values()),
            "prompt_version": " / ".join(str(i["prompt_version"]) for i in infos.values())}
    texts = {s["sample_id"]: s["text"] for s in json.load(open(CORPUS, encoding="utf-8"))["samples"]}
    key, excluded, rejected = load_key()
    errors = [e for e in key if e["op"] in ERROR_OPS]
    comments = [e for e in key if e["op"] == "comment"]
    runs = sorted({c["run"] for c in cands})
    placed = [c for c in cands if c["start"] is not None]
    by_sample = defaultdict(list)
    for c in placed:
        by_sample[c["sample_id"]].append(c)

    def found_by(e, run=None):
        return [c for c in by_sample[e["sample_id"]] if (run is None or c["run"] == run) and overlaps(e, c)]

    # recall per run and for the union of runs
    per_run = {r: sum(1 for e in errors if found_by(e, r)) for r in runs}
    union_found = [e for e in errors if found_by(e)]
    stability = Counter(sum(1 for r in runs if found_by(e, r)) for e in errors)
    same_fix = sum(1 for e in union_found if any(bare(c["corrected"]) == bare(e["corrected"]) and
                                                 bare(c["original"]) == bare(e["original"]) for c in found_by(e)))
    com_found = sum(1 for e in comments if found_by(e))

    # candidates: matched to a teacher edit (error or comment) or not
    matches = lambda c: any(overlaps(c, e) for e in key if e["sample_id"] == c["sample_id"])
    cand_run = {r: [c for c in placed if c["run"] == r] for r in runs}
    matched_run = {r: sum(1 for c in cand_run[r] if matches(c)) for r in runs}

    n, pct = len(errors), lambda a, b: f"{a}/{b} ({100 * a / b:.0f}%)" if b else "0/0"
    L = [f"# Step 7 report: scoring {finder}", "",
         f"Finder: {info['model']} ({info['reasoning_effort']}), prompt {info['prompt_version']}, {len(runs)} run(s) in total.",
         f"Answer key: {n} teacher error edits + {len(comments)} comment edits on {len({e['sample_id'] for e in key})} test stories "
         f"({excluded} edits excluded: unplaceable/unplaced or rejected in review ({rejected} items rejected)).", "",
         "## Recall: how many of the teacher's corrections the finder points at", "",
         "| | Found |", "|---|---|",
         *[f"| run {r} | {pct(per_run[r], n)} |" for r in runs],
         f"| average of one run | {sum(per_run.values()) / len(runs):.1f}/{n} ({100 * sum(per_run.values()) / len(runs) / n:.0f}%) |",
         f"| any of the {len(runs)} runs (union) | {pct(len(union_found), n)} |",
         f"| teacher comment edits (problem pointed at) | {pct(com_found, len(comments))} |", "",
         f"Of the teacher edits found, the finder proposed **the same correction** for {pct(same_fix, len(union_found))}.", "",
         "## Stability: in how many runs each teacher correction was found", "",
         "| Found in | Teacher edits |", "|---|---|",
         *[f"| {k} of {len(runs)} runs | {stability[k]} |" for k in sorted(stability, reverse=True)], "",
         f"Edits found in some runs but not all ({sum(v for k, v in stability.items() if 0 < k < len(runs))}) are the "
         "'caught at random' problem in numbers.", "",
         "## Recall by kind of edit", "", "| Kind | Found (union) |", "|---|---|"]
    for op in ERROR_OPS:
        es = [e for e in errors if e["op"] == op]
        L.append(f"| {op} | {pct(sum(1 for e in es if found_by(e)), len(es))} |")
    for story in sorted({e["story_id"] for e in errors}):
        es = [e for e in errors if e["story_id"] == story]
        L.append(f"| {story} | {pct(sum(1 for e in es if found_by(e)), len(es))} |")

    L += ["", "## Candidates: how many point at something the teacher corrected", "",
          "| | Candidates | Match a teacher edit | Match nothing she marked |", "|---|---|---|---|"]
    for r in runs:
        k = len(cand_run[r])
        L.append(f"| run {r} | {k} | {pct(matched_run[r], k)} | {k - matched_run[r]} |")
    unmatched = [c for c in placed if not matches(c)]
    conf = Counter((c["confidence"], matches(c)) for c in placed)
    L += ["", f"High-confidence candidates matching a teacher edit: {pct(conf[('high', True)], conf[('high', True)] + conf[('high', False)])}; "
              f"low-confidence: {pct(conf[('low', True)], conf[('low', True)] + conf[('low', False)])}.",
          f"Candidates that could not be located: {len(cands) - len(placed)}.", "",
          "Candidate types: " + ", ".join(f"{t} {v} ({100 * sum(1 for c in placed if c['type'] == t and matches(c)) // v}% match)"
                                         for t, v in Counter(c["type"] for c in placed).most_common()), ""]

    if len(names) > 1:
        sets = {nm: {id(e) for e in errors if any(c["finder"] == nm for c in found_by(e))} for nm in names}
        L += ["## Which finder found what", "", "| Finder | Found (all its runs) | Found ONLY by this finder |", "|---|---|---|"]
        for nm in names:
            others = set().union(*(sets[o] for o in names if o != nm))
            L.append(f"| {nm} | {pct(len(sets[nm]), n)} | {len(sets[nm] - others)} |")
        both = set.intersection(*sets.values())
        L += [f"| found by all finders | {pct(len(both), n)} | |", ""]
        for nm in names:
            others = set().union(*(sets[o] for o in names if o != nm))
            only = [e for e in errors if id(e) in sets[nm] - others]
            L += [f"### Found only by {nm} ({len(only)})", ""]
            L += [f"- {e['sample_id']}: {show(texts[e['sample_id']], e)}" for e in only[:40]] + [""]

    missed = [e for e in errors if not found_by(e)]
    L += [f"## Teacher corrections no run found ({len(missed)})", ""]
    L += [f"- {e['sample_id']}: {show(texts[e['sample_id']], e)}" + (f" — {e['teacher_note']}" if e["teacher_note"] else "")
          for e in missed]

    seen, uniq = set(), []
    for c in sorted(unmatched, key=lambda c: (c["sample_id"], c["start"], c["run"])):
        k = (c["sample_id"], c["start"], c["end"], bare(c["corrected"]))
        if k not in seen:
            seen.add(k)
            uniq.append(c)
    L += ["", f"## Candidates matching nothing the teacher marked ({len(uniq)} distinct; first 60)", "",
          "Not necessarily wrong: these are for the teacher to judge.", ""]
    L += [f"- {c['sample_id']} ({c['confidence']}, {c['type']}): {show(texts[c['sample_id']], c)} — {c['why']}" for c in uniq[:60]]

    out = ROOT / "reports" / f"07_score_{finder}.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"recall per run {per_run} of {n}; union {len(union_found)}; stability {dict(stability)}")
    print(f"Report: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
