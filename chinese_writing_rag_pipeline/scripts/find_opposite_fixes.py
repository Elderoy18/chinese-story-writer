#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find places where the teacher's corrections go in opposite directions in the
same context: she adds X after a word in one story and removes X after the
same word in another (e.g. +了 / -了 after 成为), or changes A -> B in one
place and B -> A in another. Retrieved together, such corrections give the
model contradictory examples; usually the context explains the difference
(e.g. 了 is wrong before quoted speech, right otherwise), and that condition
belongs in the rule.

    python scripts/find_opposite_fixes.py [--test-set ../eval/test_set_h20.json]
        -> review/contradictions/opposite_fixes.csv (+ instructions.md)

A report for review, not a build step: every pair is her own real correction.
Uses her exact edits on the training stories (raw/aligned_edits_train.jsonl)
with HanLP's word before the edit (v2 parse).
"""
import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, "scripts")
from aligned_edits import ALIGNED_EDITS_PATH, ERROR_OPS, before_after, first_alternative  # noqa: E402

CORPUS_PATH = "extracted/basic_corpus.json"
RULE_LABELS_PATH = "raw/correction_rules.json"
OUT_DIR = Path("review/contradictions")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test-set", default="../eval/test_set_h20.json")
    args = ap.parse_args()
    texts = {s["sample_id"]: s["raw_text"] for s in json.load(open(CORPUS_PATH, encoding="utf-8"))["samples"]}
    held = {s["sample_id"] for s in json.load(open(args.test_set, encoding="utf-8"))["samples"]}
    labels = json.load(open(RULE_LABELS_PATH, encoding="utf-8"))["rules"]

    adds, removes, swaps = defaultdict(list), defaultdict(list), defaultdict(list)
    for line in open(ALIGNED_EDITS_PATH, encoding="utf-8"):
        e = json.loads(line)
        if e["op"] not in ERROR_OPS or e["start"] is None or e["sample_id"] in held:
            continue
        left = e.get("hanlp_left") or ""
        o, c = e["original"] or "", first_alternative(e["corrected"])
        if e["op"] == "insert" and len(c) <= 2:
            adds[(left, c)].append(e)
        elif e["op"] == "delete" and len(o) <= 2:
            removes[(left, o)].append(e)
        elif e["op"] == "replace" and len(o) <= 3 and len(c) <= 3:
            swaps[(o, c)].append(e)

    def show(e):
        b, a = before_after(texts[e["sample_id"]], [e])
        rules = ", ".join(labels.get(e["teacher_line"], []))
        return f"{e['sample_id']}: {b} -> {a}" + (f"  [{e['teacher_note']}]" if e["teacher_note"] else "") + f"  ({rules})"

    rows = []
    for (left, x), add in adds.items():
        rem = removes.get((left, x))
        if left and rem:
            rows.append({"pattern": f"after {left}: +{x} / -{x}", "n_one_way": len(add), "n_other_way": len(rem),
                         "one_way_examples": "\n".join(show(e) for e in add[:3]),
                         "other_way_examples": "\n".join(show(e) for e in rem[:3])})
    for (o, c), fwd in swaps.items():
        back = swaps.get((c, o))
        if back and o < c:
            rows.append({"pattern": f"{o}→{c} / {c}→{o}", "n_one_way": len(fwd), "n_other_way": len(back),
                         "one_way_examples": "\n".join(show(e) for e in fwd[:3]),
                         "other_way_examples": "\n".join(show(e) for e in back[:3])})
    rows.sort(key=lambda r: -(r["n_one_way"] + r["n_other_way"]))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cols = ["pattern", "n_one_way", "n_other_way", "one_way_examples", "other_way_examples",
            "WHAT DECIDES IT (her condition, e.g. 'no 了 before quoted speech')", "NOTE"]
    with open(OUT_DIR / "opposite_fixes.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    (OUT_DIR / "instructions.md").write_text(f"""# Corrections that go in opposite directions

`opposite_fixes.csv` lists {len(rows)} patterns where her corrections on the
training stories go both ways in the same context: adding a character after a
word in one story and removing it after the same word in another, or changing
A to B in one place and B to A in another. Each row shows up to three examples
of each direction (the student's clause -> her fix, her note, the rule labels).

These are her real corrections, so both directions are usually right -- for
different reasons. When both are retrieved for the same scene, the model sees
what looks like a contradiction. For each row, fill in what decides it (e.g.
"了 after 告诉 only when no quoted speech follows"); that condition can then be
added to the rule card or teacher rule, so the model applies it the same way
every time. Leave blank if it is unclear; send the unclear ones to her.
""", encoding="utf-8")
    print(f"{len(rows)} opposite-direction patterns -> {OUT_DIR}/opposite_fixes.csv")
    for r in rows[:15]:
        print(f"  {r['pattern']:28} {r['n_one_way']} / {r['n_other_way']}")


if __name__ == "__main__":
    main()
