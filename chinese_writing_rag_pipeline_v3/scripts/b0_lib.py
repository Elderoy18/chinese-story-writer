"""Shared helpers for the B0 steps (07-09): loading the test scenes, clause spans,
and her train corrections as retrievable examples. Standard library only."""
import json
import math
import re
from pathlib import Path

from llm import embed

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
SPLIT = ROOT / "data" / "03_split" / "split.json"
TRAIN_EDITS = ROOT / "data" / "05_align" / "edits_train.jsonl"
EMBED_CACHE = ROOT / "data" / "b0_embeddings"

CLAUSE_END = "，。！？；：,!?;:\n"
DIMENSIONS = ["grammar", "vocabulary", "coherence"]
COHERENCE_TYPES = ["reference", "temporality", "connectors"]


def load():
    corpus = json.load(open(CORPUS, encoding="utf-8"))
    split = json.load(open(SPLIT, encoding="utf-8"))
    samples = {s["sample_id"]: s for s in corpus["samples"]}
    return corpus, split, samples


def test_scenes(split, samples):
    """[(sample, scene number, start, end, earlier scenes' text)] in story order."""
    out = []
    for t in split["test"]:
        s = samples[t["sample_id"]]
        for k, sc in enumerate(t["scenes"]):
            earlier = [s["text"][x["start"]:x["end"]] for x in t["scenes"][:k]]
            out.append((s, k + 1, sc["start"], sc["end"], earlier))
    return out


def clause_span(text, start, end):
    """Widen [start, end) to whole clauses: from after the previous clause mark to
    and including the next one (the clause's own punctuation stays with it)."""
    s = start
    while s > 0 and text[s - 1] not in CLAUSE_END:
        s -= 1
    e = max(end, s)
    while e < len(text) and text[e] not in CLAUSE_END:
        e += 1
    while s < e and text[s].isspace():
        s += 1
    return s, e


def clauses(text, start, end):
    """[(s, e)] clause spans inside text[start:end] (without the closing mark)."""
    out, s = [], start
    for i in range(start, end):
        if text[i] in CLAUSE_END:
            if text[s:i].strip():
                out.append((s, i))
            s = i + 1
    if text[s:end].strip():
        out.append((s, end))
    return out


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)) or 1)


class Examples:
    """Her train corrections, retrievable by the student clause they were made in.
    Each example: the student's clause, her correction of the error in it, her note."""

    def __init__(self, samples):
        rows = []
        for line in open(TRAIN_EDITS, encoding="utf-8"):
            e = json.loads(line)
            if e["op"] not in ("replace", "delete", "insert") or e["start"] is None:
                continue
            text = samples[e["sample_id"]]["text"]
            cs, ce = clause_span(text, e["start"], e["end"])
            clause = text[cs:ce].strip("，。！？；：,!?;: \n")
            if not clause:
                continue
            rows.append({"clause": clause, "original": e["original"] or "", "corrected": e["corrected"] or "",
                         "note": e["teacher_note"] or "", "edit_id": e["edit_id"]})
        self.rows = rows
        self.vectors = embed([r["clause"] for r in rows], EMBED_CACHE)

    def for_scene(self, scene_text, k=6):
        """Her corrections nearest to the scene's clauses: the best match per clause,
        then the k most similar overall (no two from the same clause text)."""
        parts = [c for c in re.split(f"[{re.escape(CLAUSE_END)}]", scene_text) if len(c.strip()) >= 2]
        if not parts:
            return []
        qv = embed(parts, EMBED_CACHE)
        best = {}
        for v in qv:
            i, sim = max(((j, cosine(v, w)) for j, w in enumerate(self.vectors)), key=lambda x: x[1])
            if sim > best.get(i, 0):
                best[i] = sim
        picked, seen = [], set()
        for i, sim in sorted(best.items(), key=lambda x: -x[1]):
            r = self.rows[i]
            if r["clause"] in seen:
                continue
            seen.add(r["clause"])
            picked.append(r)
            if len(picked) == k:
                break
        return picked
