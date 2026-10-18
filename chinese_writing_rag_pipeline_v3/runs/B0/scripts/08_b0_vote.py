#!/usr/bin/env python3
"""Step 8 (B0) -- keep only corrections that at least 2 of the 3 runs agree on.

    data/07_b0_write/items.jsonl  ->  data/08_b0_vote/items.jsonl   (run = "voted")

Items from different runs are the same correction when their clauses overlap in
the same story. A group is kept if it contains items from at least MIN_RUNS
different runs. Its representative is the item whose corrected clause most runs
gave (ties: the earliest run). This can only remove items, never add them: a
correction one run makes and the others do not is exactly the "caught at
random" kind, and such one-off flags are where wrong corrections concentrate.
"""
import json
import re
from collections import Counter, defaultdict

from b0_lib import ROOT

IN = ROOT / "data" / "07_b0_write" / "items.jsonl"
OUT = ROOT / "data" / "08_b0_vote"
MIN_RUNS = 2
squash = lambda s: re.sub(r"[\s，。！？、；：,.!?;:“”‘’\"'（）()…—]", "", s or "")


def overlaps(a, b):
    return a["sample_id"] == b["sample_id"] and a["start"] < b["end"] and b["start"] < a["end"]


def main():
    items = [json.loads(l) for l in open(IN, encoding="utf-8")]
    groups = []
    for it in sorted(items, key=lambda x: (x["sample_id"], x["start"], x["run"])):
        g = next((g for g in groups if any(overlaps(it, o) for o in g)), None)
        g.append(it) if g else groups.append([it])
    kept, sizes = [], Counter()
    for g in groups:
        runs = {i["run"] for i in g}
        sizes[len(runs)] += 1
        if len(runs) < MIN_RUNS:
            continue
        votes = Counter((i["start"], i["end"], squash(i["after"])) for i in g)
        best = max(g, key=lambda i: (votes[(i["start"], i["end"], squash(i["after"]))], -i["run"]))
        kept.append({**best, "run": "voted", "agreeing_runs": len(runs),
                     "same_correction_runs": votes[(best["start"], best["end"], squash(best["after"]))]})
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "items.jsonl", "w", encoding="utf-8") as fh:
        for it in kept:
            fh.write(json.dumps(it, ensure_ascii=False) + "\n")
    print(f"{len(items)} items in {len(groups)} places; found by 1/2/3 runs: {sizes[1]}/{sizes[2]}/{sizes[3]}; "
          f"kept {len(kept)} -> {(OUT / 'items.jsonl').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
