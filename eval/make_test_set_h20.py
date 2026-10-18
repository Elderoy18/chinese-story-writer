#!/usr/bin/env python3
"""Freeze the 20-story test set for S7 into eval/test_set_h20.json.

The 20 stories are the ones the teacher reviewed in the alignment check
("align test.xlsx"): v2's test split. The 6 stories of eval/test_set.json are
among them, with the same scene splits; v1 and v2 hold the same story texts.

Per story:
  scenes          -- v2's scene split (whole sentences), as text
  gold.corrections -- her correction lines as in eval/test_set.json (original /
                      corrected / explanation split + her v1 rule labels from
                      raw/correction_rules.json)
  gold.content_flags -- her "Miss ... scene" etc. flags
  gold.aligned_edits -- her corrections as exact edits on the story text (v2
                      step 5; character positions in raw_text), each with her
                      decision from the alignment review
  gold.review_notes  -- her notes from the alignment review, classified:
                      missed (an error the edits do not cover), alternative
                      (another correct fix), rule (a rule explanation),
                      fix_rejected (her "no" + her correction); raw text kept

Every one of these stories is held out of snapshots built with
--test-set eval/test_set_h20.json. Known issues in her review (notes that look
attached to the wrong row) are listed in "_known_issues" for checking with her.

    python eval/make_test_set_h20.py      (standard library only)
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPELINE = ROOT / "chinese_writing_rag_pipeline"
V2 = ROOT / "chinese_writing_rag_pipeline_v2"
SPLIT = V2 / "data" / "03_split" / "split.json"
EDITS = V2 / "data" / "05_align" / "edits_test.jsonl"
REVIEW = PIPELINE / "raw" / "iteration data" / "align test.xlsx"
OUT = ROOT / "eval" / "test_set_h20.json"
sys.path.insert(0, str(PIPELINE / "scripts"))
from tagging import split_correction  # noqa: E402

KNOWN_ISSUES = [
    "shennong_samples#18 f5 / f6: the notes look swapped (the note on 夹竹桃是毒的 is about 会帮他, and the "
    "note on 灵芝会帮他 is about 是毒的).",
    "shennong_samples#49/f9/p0/k0 (吃 -> 吃了): no decision, and the note (别的/别人) belongs to another item.",
    "Some 'miss' notes point to an error that another row's edit already covers (e.g. delete 了 in 住了在 is "
    "mengmu_samples#4 p1/k1; delete 他 is shennong_samples#49 k2).",
]


def read_xlsx(path):
    """First sheet as a list of {header: value} rows (standard library only)."""
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    t = "{%s}t" % ns["m"]
    z = zipfile.ZipFile(path)
    shared = [("".join(x.text or "" for x in si.iter(t)))
              for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns)]

    def col(ref):
        n = 0
        for ch in re.match(r"[A-Z]+", ref).group():
            n = n * 26 + ord(ch) - 64
        return n - 1

    rows = []
    for row in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).iter("{%s}row" % ns["m"]):
        cells = {}
        for c in row.findall("m:c", ns):
            v = c.find("m:v", ns)
            if c.get("t") == "inlineStr":
                cells[col(c.get("r"))] = "".join(x.text or "" for x in c.iter(t))
            elif v is not None:
                cells[col(c.get("r"))] = shared[int(v.text)] if c.get("t") == "s" else v.text
        rows.append([cells.get(i, "") for i in range(max(cells) + 1)] if cells else [])
    header = rows[0]
    return [dict(zip(header, r + [""] * (len(header) - len(r)))) for r in rows[1:] if r]


def ref_set(tail):
    """'k0' -> {'k0'}; 'k0-1' -> {'k0', 'k1'}; 'k0-1-2' -> k0 to k2; 'note' -> {'note'}.
    Both review rows and edits use these tails (an edit's own tail is merged when
    one of her corrections was split into several edits)."""
    if tail == "note":
        return {"note"}
    nums = [int(n) for n in tail[1:].split("-")]
    return {f"k{i}" for i in range(min(nums), max(nums) + 1)}


def covered_refs(item_id):
    """Review row id -> (sample/fid/p prefix, set of ref tails it covers)."""
    sample, fid, part, tail = item_id.split("/")
    return f"{sample}/{fid}/{part}", ref_set(tail)


def note_kind(note):
    n = note.strip().lower()
    if n.startswith("miss"):
        return "missed"
    if n.startswith("another correction"):
        return "alternative"
    if n.startswith(("note", "add")):
        return "rule"
    return "comment"


def main():
    split = json.load(open(SPLIT, encoding="utf-8"))["test"]
    corpus = {s["sample_id"]: s for s in json.load(open(PIPELINE / "extracted/basic_corpus.json", encoding="utf-8"))["samples"]}
    labels = json.load(open(PIPELINE / "raw/correction_rules.json", encoding="utf-8"))["rules"]
    edits = [json.loads(l) for l in open(EDITS, encoding="utf-8")]
    review = read_xlsx(REVIEW)

    by_row = {}
    for r in review:
        prefix, refs = covered_refs(r["item_id"])
        by_row[r["item_id"]] = (prefix, refs, r)
    counts = Counter()
    samples = []
    for t in split:
        sid = t["sample_id"]
        s = corpus[sid]
        text = s["raw_text"]
        scenes = [text[x["start"]:x["end"]] for x in t["scenes"]]
        if "".join(scenes) != text:
            sys.exit(f"{sid}: scenes do not cover the story text exactly")

        aligned = []
        for e in (e for e in edits if e["sample_id"] == sid):
            prefix = f"{sid}/{e['fid']}/{e['ref'].split('/')[0]}"
            tails = ref_set(e["ref"].split("/")[1])
            row = next((r for p, refs, r in by_row.values() if p == prefix and tails <= refs), None)
            if e["start"] is not None and text[e["start"]:e["end"]] != (e["original"] or ""):
                sys.exit(f"{e['edit_id']}: position does not match the story text")
            decision = (row or {}).get("DECISION", "").strip().lower() or None
            aligned.append({"edit_id": e["edit_id"], "op": e["op"], "start": e["start"], "end": e["end"],
                            "original": e["original"], "corrected": e["corrected"],
                            "her_line": e["teacher_line"], "her_piece": e["teacher_piece"],
                            "her_note": e["teacher_note"], "review_row": (row or {}).get("item_id"),
                            "her_decision": decision})
            counts[f"edits, decision {decision}"] += 1

        notes = []
        for p, refs, r in by_row.values():
            if not p.startswith(sid + "/"):
                continue
            if r.get("DECISION", "").strip().lower() == "no":
                notes.append({"review_row": r["item_id"], "kind": "fix_rejected", "text": r["CORRECTION"].strip()})
            note = r.get("REVIEWER_NOTE", "").strip()
            if note:
                notes.append({"review_row": r["item_id"], "kind": note_kind(note), "text": note})
        counts.update(f"notes: {n['kind']}" for n in notes)

        gold = []
        for raw in s["teacher_correction_items"]:
            sp = split_correction(raw)
            gold.append({"text": raw, "original_span": sp["original_span"], "corrected_span": sp["corrected_span"],
                         "explanation": sp["explanation"], "rules": labels.get(raw, [])})
            counts["corrections with rule labels" if labels.get(raw) else "corrections WITHOUT rule labels"] += 1

        samples.append({"sample_id": sid, "story_id": s["story_id"], "raw_text": text, "scenes": scenes,
                         "gold": {"corrections": gold, "content_flags": s["content_flags"],
                                  "aligned_edits": aligned, "review_notes": notes}})

    out = {
        "_about": "S7 test set: the 20 stories the teacher reviewed in the alignment check (v2's test split; "
                  "includes the 6 stories of test_set.json, same scenes). Held out of every snapshot built with "
                  "--test-set eval/test_set_h20.json. Built by eval/make_test_set_h20.py from v2's split and "
                  "aligned edits and her review in 'align test.xlsx'.",
        "_known_issues": KNOWN_ISSUES,
        "samples": samples,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(samples)} stories, {sum(len(s['scenes']) for s in samples)} scenes")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
