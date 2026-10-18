#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The teacher's corrections as exact edits on the story text
(raw/aligned_edits_train.jsonl, see its .about.json): loading, and showing an
edit inside its clause, before and after her fix.

Used by chunk_builder.py (correction_item `edits`, rule_card examples and
standard fixes, rule_example chunks) and mine_triggers.py.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ALIGNED_EDITS_PATH = Path("raw/aligned_edits_train.jsonl")
ERROR_OPS = {"replace", "delete", "insert"}
CLAUSE_END = "，。！？；：,.!?;:"


def load_aligned_edits():
    """Error edits (replace / delete / insert with a position), grouped by
    (sample_id, her correction line) -- the key correction_item chunks use."""
    if not ALIGNED_EDITS_PATH.exists():
        raise FileNotFoundError(f"{ALIGNED_EDITS_PATH}: source file missing")
    by_line = defaultdict(list)
    for line in open(ALIGNED_EDITS_PATH, encoding="utf-8"):
        e = json.loads(line)
        if e["op"] in ERROR_OPS and e["start"] is not None:
            by_line[(e["sample_id"], e["teacher_line"])].append(e)
    return by_line


def first_alternative(s):
    """Her corrections sometimes give alternatives ('怕/担心'); use the first."""
    return (s or "").split("/")[0]


def clause_span(text, start, end):
    """The clause (between punctuation) containing [start, end)."""
    lo = max([text.rfind(p, 0, start) for p in CLAUSE_END] + [-1]) + 1
    his = [i for i in (text.find(p, max(end, start)) for p in CLAUSE_END) if i >= 0]
    return lo, (min(his) if his else len(text))


def before_after(text, edits):
    """(student's clause(s), the same text with all these edits applied):
    the whole clause(s) the edits touch, so neither side is a fragment."""
    edits = sorted(edits, key=lambda e: (e["start"], e["end"]))
    lo = min(clause_span(text, e["start"], e["end"])[0] for e in edits)
    hi = max(clause_span(text, e["start"], e["end"])[1] for e in edits)
    out, pos = [], lo
    for e in edits:
        if e["start"] < pos:  # overlapping alternatives: keep the first
            continue
        out.append(text[pos:e["start"]])
        out.append(first_alternative(e["corrected"]))
        pos = e["end"]
    out.append(text[pos:hi])
    return text[lo:hi], "".join(out)


def signature(e, max_len=3):
    """A short description of what an edit does, for counting her usual fix:
    '+了', '-了', '去→到'; longer rewrites are 'rewrite'."""
    o, c = e["original"] or "", first_alternative(e["corrected"])
    if len(o) > max_len or len(c) > max_len:
        return "rewrite"
    if e["op"] == "insert":
        return f"+{c}"
    if e["op"] == "delete":
        return f"-{o}"
    return f"{o}→{c}"


def standard_fix(edits_with_text, n_examples=3, min_count=2):
    """Her usual fix for one rule, from single-rule corrections: the most common
    edit signatures seen at least min_count times, and up to n whole-clause
    examples of them. None if no fix recurs (one-off fixes are not a standard).
    edits_with_text: list of (edit, story_text)."""
    sigs = Counter(signature(e) for e, _ in edits_with_text)
    top = [(s, n) for s, n in sigs.most_common() if s != "rewrite" and n >= min_count][:3]
    if not top:
        return None
    examples, seen = [], set()
    for sig, _ in top:
        for e, text in edits_with_text:
            if signature(e) == sig and len(examples) < n_examples:
                b, a = before_after(text, [e])
                if b not in seen and b != a:
                    seen.add(b)
                    examples.append({"before": b, "after": a, "note": e["teacher_note"]})
                    break
    return {"signatures": [{"fix": s, "count": n} for s, n in top],
            "n_rewrites": sigs.get("rewrite", 0), "n_edits": sum(sigs.values()), "examples": examples}


def strip_punct(s):
    return re.sub(rf"[{re.escape(CLAUSE_END)}\s]", "", s)
