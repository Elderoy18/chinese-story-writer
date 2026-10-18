#!/usr/bin/env python3
"""Precision-first scorer: how good is the feedback a system shows, by the
teacher's priorities -- false positives and incorrect corrections first, missed
errors last ("可以接受AI miss errors，但是不能出现false positives或incorrect
corrections").

    python scripts/score.py <items.jsonl> [<items.jsonl> ...] [--name NAME]
        ->  reports/score_<name>.md

Input: one feedback item per line --
    {"sample_id", "run", "start", "end",       # the item's span in the student's story text
     "before", "after",                        # the student's words and the corrected version (after = null for a comment)
     "dimension", "strength"}                  # e.g. grammar / vocabulary / coherence ...; error | suggestion
"run" tells repeated runs apart (any value); give several files to compare systems.

Each item gets exactly one verdict:
    same_as_hers     -- at a place she corrected, and its "after" equals her
                        corrected text for that span (her edits applied to "before")
    at_her_place     -- at a place she corrected, with a different correction:
                        the error is real; whether this correction is right
                        needs her label (or is assumed right in the best case)
    correct / incorrect_correction / false_positive
                     -- her label (review/labels/teacher_labels.jsonl) for an item
                        at a place she did NOT mark, or a different correction
    unconfirmed      -- at a place she did not mark, not yet labelled

Metrics (in her order of priority):
    1. false positives per scene       -- labelled not-an-error; range up to all unconfirmed
    2. incorrect corrections           -- labelled
    3. consistency                     -- share of items found in every run (by span)
    4. recall                          -- share of her corrections the items cover
Unconfirmed items are reported as a range (best case: all fine; worst case: all
false positives) until she labels them, so a number is never better than the
evidence for it.

Answer key: data/05_align/edits_test.jsonl (her corrections on the test stories).
Standard library only.
"""
import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEY = ROOT / "data" / "05_align" / "edits_test.jsonl"
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
SPLIT = ROOT / "data" / "03_split" / "split.json"
LABELS = ROOT / "review" / "labels" / "teacher_labels.jsonl"
REPORTS = ROOT / "reports"

ERROR_OPS = {"replace", "delete", "insert"}
squash = lambda s: re.sub(r"[\s，。！？、；：,.!?;:“”‘’\"'（）()…—]", "", s or "")  # compare without spaces/punctuation


def overlaps(a, b):
    """Spans overlap; a zero-width insertion counts if it touches the other span."""
    if a["start"] is None or b["start"] is None:
        return False
    if a["start"] == a["end"] or b["start"] == b["end"]:
        return a["start"] <= b["end"] and b["start"] <= a["end"]
    return a["start"] < b["end"] and b["start"] < a["end"]


def load_key():
    key = [json.loads(l) for l in open(KEY, encoding="utf-8")]
    return [e for e in key if e.get("start") is not None and e["op"] in ERROR_OPS | {"comment"}]


def load_labels():
    """{(sample_id, before, after): label} -- her judgment of one item, reused in every later round."""
    out = {}
    if LABELS.exists():
        for line in open(LABELS, encoding="utf-8"):
            r = json.loads(line)
            out[(r["sample_id"], r["before"], r["after"])] = r["label"]
    return out


def her_after(item, edits, text):
    """Her corrected text for the item's span: her edits inside it, applied to the
    student's words. None if one of her edits crosses the span's edges."""
    s, e = item["start"], item["end"]
    inside = [x for x in edits if x["op"] in ERROR_OPS and overlaps(item, x)]
    if any(x["start"] < s or x["end"] > e for x in inside):
        return None
    out, pos = [], s
    for x in sorted(inside, key=lambda x: x["start"]):
        out += [text[pos:x["start"]], x["corrected"] or ""]
        pos = x["end"]
    out.append(text[pos:e])
    return "".join(out)


def verdict(item, key_by_sample, labels, texts):
    mine = [x for x in key_by_sample[item["sample_id"]] if overlaps(item, x)]
    lab = labels.get((item["sample_id"], item["before"], item["after"]))
    if mine:
        gold = her_after(item, mine, texts[item["sample_id"]])
        if item["after"] is not None and gold is not None and squash(item["after"]) == squash(gold):
            return "same_as_hers"
        if item["after"] is None and any(x["op"] == "comment" for x in mine):
            return "same_as_hers"  # a comment at the place she commented
        return lab or "at_her_place"
    return lab or "unconfirmed"


def score(items, key, labels, texts, n_scenes):
    key_by_sample = defaultdict(list)
    for e in key:
        key_by_sample[e["sample_id"]].append(e)
    runs = sorted({i["run"] for i in items}, key=str)
    per_run = {}
    for r in runs:
        its = [i for i in items if i["run"] == r]
        v = Counter(verdict(i, key_by_sample, labels, texts) for i in its)
        errors = [e for e in key if e["op"] in ERROR_OPS]
        found = sum(1 for e in errors if any(i["sample_id"] == e["sample_id"] and overlaps(e, i) for i in its))
        per_run[r] = {"items": len(its), "verdicts": v, "recall": (found, len(errors)),
                      "by_strength": Counter((i.get("strength", "error"), verdict(i, key_by_sample, labels, texts)) for i in its),
                      "by_dimension": Counter((i.get("dimension", "?"), verdict(i, key_by_sample, labels, texts)) for i in its)}
    # consistency: an item counts as stable if every run has an item overlapping it
    stable = total = 0
    if len(runs) > 1:
        for r in runs:
            for i in (x for x in items if x["run"] == r):
                total += 1
                stable += all(any(o["sample_id"] == i["sample_id"] and overlaps(i, o) for o in items if o["run"] == q)
                              for q in runs if q != r)
    return per_run, (stable, total)


def pct(a, b):
    return f"{a}/{b} ({100 * a / b:.0f}%)" if b else "0/0"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--name")
    args = ap.parse_args()
    key, labels = load_key(), load_labels()
    corpus = json.load(open(CORPUS, encoding="utf-8"))
    texts = {s["sample_id"]: s["text"] for s in corpus["samples"]}
    split = json.load(open(SPLIT, encoding="utf-8"))
    n_scenes = sum(len(t["scenes"]) for t in split["test"])
    name = args.name or "+".join(Path(f).parent.name for f in args.files)

    L = [f"# Score: {name}", "",
         f"Answer key: {len([e for e in key if e['op'] in ERROR_OPS])} of her corrections on {len(split['test'])} test stories "
         f"({n_scenes} scenes). Teacher labels on file: {len(labels)}.", "",
         "Verdicts: **same as hers** = her correction; **at her place** = a real error, different correction (needs her label); "
         "**unconfirmed** = a place she did not mark, not yet labelled. Ranges: best case (unconfirmed all fine) – "
         "worst case (unconfirmed all false positives).", ""]
    for f in args.files:
        items = [json.loads(l) for l in open(f, encoding="utf-8")]
        per_run, (stable, total) = score(items, key, labels, texts, n_scenes)
        L += [f"## {f}", "",
              "| Run | Items / scene | False positives / scene (labelled – worst case) | Incorrect corrections | "
              "Same as hers | At her place, other correction | Unconfirmed | Recall of her corrections |",
              "|---|---|---|---|---|---|---|---|"]
        for r, m in per_run.items():
            v, n = m["verdicts"], m["items"]
            fp, unc = v["false_positive"], v["unconfirmed"]
            L.append(f"| {r} | {n / n_scenes:.1f} | {fp / n_scenes:.2f} – {(fp + unc) / n_scenes:.2f} | {v['incorrect_correction']} | "
                     f"{pct(v['same_as_hers'], n)} | {pct(v['at_her_place'], n)} | {pct(unc, n)} | {pct(*m['recall'])} |")
        if total:
            L += ["", f"Consistency: {pct(stable, total)} of items are found (same place) in every run."]
        r0 = next(iter(per_run.values()))
        L += ["", "Verdicts by strength and by dimension (first run):", "",
              "| | same as hers | at her place | unconfirmed | labelled ok | labelled wrong |", "|---|---|---|---|---|---|"]
        for group in ("by_strength", "by_dimension"):
            keys = sorted({k for k, _ in r0[group]})
            for k in keys:
                c = {vv: r0[group][(k, vv)] for vv in ("same_as_hers", "at_her_place", "unconfirmed", "correct",
                                                       "incorrect_correction", "false_positive")}
                L.append(f"| {k} | {c['same_as_hers']} | {c['at_her_place']} | {c['unconfirmed']} | {c['correct']} | "
                         f"{c['incorrect_correction'] + c['false_positive']} |")
        L.append("")
    REPORTS.mkdir(parents=True, exist_ok=True)
    out = REPORTS / f"score_{re.sub(r'[^A-Za-z0-9_+.-]', '_', name)}.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Report: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
