#!/usr/bin/env python3
"""Step 9 -- review sheet of the places the finders flagged in the test stories
that the teacher did not mark, for the teacher to judge.

    data/05_align/edits_test.jsonl (answer key), data/<finder>/candidates.jsonl
        ->  review/09_extra_flags.csv                 the sheet (opens in Excel)
            review/09_extra_flags_instructions.md     how to fill it in (teacher-facing)

    python scripts/09_extra_flags.py

Flags from all finders that overlap each other are merged into one row (one
place in the story); a row lists every correction proposed there and how many
checkers agreed. Rows are in reading order, story by story.

Her answers do two things:
  - "error" rows are real errors she did not mark: they measure how many of the
    finders' extra flags are right, and can be added to the answer key;
  - "not an error" rows show what the finders flag that she accepts -- the
    judging step of the teacher layer should learn to drop these.
Decisions already typed in are kept when the sheet is rebuilt.
"""
import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FINDERS = {"06_find_baseline": "AI checker", "08_find_gec": "correction model"}
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
SHEET = ROOT / "review" / "09_extra_flags.csv"
INSTRUCTIONS = ROOT / "review" / "09_extra_flags_instructions.md"

spec = importlib.util.spec_from_file_location("score", ROOT / "scripts" / "07_score.py")
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)

COLUMNS = ["row_id", "story", "sentence_with_flag", "flagged_text", "suggested_corrections", "reasons_given",
           "flagged_by", "TEACHER_DECISION", "TEACHER_CORRECTION", "TEACHER_NOTE"]
HUMAN = ["TEACHER_DECISION", "TEACHER_CORRECTION", "TEACHER_NOTE"]


def main():
    key, _, _ = score.load_key()
    texts = {s["sample_id"]: s["text"] for s in json.load(open(CORPUS, encoding="utf-8"))["samples"]}
    cands = []
    for name in FINDERS:
        for line in open(ROOT / "data" / name / "candidates.jsonl", encoding="utf-8"):
            c = json.loads(line)
            if c["start"] is not None:
                c["finder"] = name
                cands.append(c)

    extra = [c for c in cands if not any(e["sample_id"] == c["sample_id"] and score.overlaps(c, e) for e in key)]
    groups = []
    for c in sorted(extra, key=lambda c: (c["sample_id"], c["start"])):
        g = next((g for g in groups if g[0]["sample_id"] == c["sample_id"] and any(score.overlaps(c, x) for x in g)), None)
        g.append(c) if g else groups.append([c])

    kept = {}
    if SHEET.exists():
        with open(SHEET, encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                if any(row.get(h) for h in HUMAN):
                    kept[row["row_id"]] = row

    rows = []
    for g in groups:
        sid = g[0]["sample_id"]
        start, end = min(c["start"] for c in g), max(c["end"] for c in g)
        row_id = f"{sid}@{start}-{end}"
        text = texts[sid]
        corrections, reasons = [], []
        for c in g:
            fix = score.show(text, c)
            if fix not in corrections:
                corrections.append(fix)
            if c["finder"] == "06_find_baseline" and c["why"] not in reasons:
                reasons.append(c["why"])
        ai_runs = len({c["run"] for c in g if c["finder"] == "06_find_baseline"})
        by = []
        if ai_runs:
            by.append(f"AI checker ({ai_runs} of 3 tries)")
        if any(c["finder"] == "08_find_gec" for c in g):
            by.append("correction model")
        lo = max(text.rfind("，", 0, start), text.rfind("。", 0, start)) + 1
        ends = [i for i in (text.find("。", end), text.find("，", end)) if i >= 0]
        hi = min(ends) if ends else len(text)
        sentence = text[lo:start] + "【" + text[start:end] + "】" + text[end:hi] if end > start else \
            text[lo:start] + "【^】" + text[start:hi]
        k = kept.get(row_id, {})
        rows.append([row_id, sid, sentence, text[start:end] or "(something missing here)",
                     "\n".join(corrections), "\n".join(reasons), " + ".join(by),
                     k.get("TEACHER_DECISION", ""), k.get("TEACHER_CORRECTION", ""), k.get("TEACHER_NOTE", "")])

    SHEET.parent.mkdir(parents=True, exist_ok=True)
    with open(SHEET, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(COLUMNS)
        w.writerows(rows)
    INSTRUCTIONS.write_text(INSTRUCTIONS_TEXT.format(n=len(rows), stories=len({r[1] for r in rows})), encoding="utf-8")
    print(f"{len(rows)} rows ({len(kept)} earlier decisions kept) -> {SHEET.relative_to(ROOT)}")


INSTRUCTIONS_TEXT = """# Places flagged that the teacher did not mark

The automatic checkers were run on the {stories} test stories, and they flagged {n} places that the
teacher's own corrections do not mark. Some of these are likely real errors that were simply not
marked; others are things the teacher accepts. Her judgment on each place shows how often the
checkers are right, and teaches the system which kinds of flags to keep and which to drop.

## The sheet: `09_extra_flags.csv` (opens in Excel)

One row per flagged place, story by story in reading order.

| Column | Meaning |
|---|---|
| story | the student story |
| sentence_with_flag | the clause, with the flagged text in 【 】 (【^】 marks a place where something may be missing) |
| flagged_text | the student's words that were flagged |
| suggested_corrections | the correction(s) proposed: [+X] add X, [-X] delete X, [A→B] replace A with B |
| reasons_given | the checker's short reason, where it gave one |
| flagged_by | which checker flagged it: the AI checker (and in how many of its 3 tries), the correction model, or both |

## What to fill in

- **TEACHER_DECISION**: `error` (a real error that should be corrected), `not an error`, or `unsure`.
- **TEACHER_CORRECTION** (optional): her own correction, if it differs from the suggested ones.
- **TEACHER_NOTE** (optional): anything worth recording, e.g. "acceptable for this level" or "style only".

Places flagged by both checkers, or by the AI checker in all 3 tries, are the most likely to be real
errors; places flagged only once are the least certain. Rows already filled in are kept if the sheet
is rebuilt.
"""


if __name__ == "__main__":
    main()
