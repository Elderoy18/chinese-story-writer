#!/usr/bin/env python3
"""Build a frozen retrieval snapshot for the stage evaluation.

Uses the same build code as the pipeline (chunk_builder.py and
build_iteration_chunks.py) on the current source files, but with the held-out
test samples removed from the basic corpus -- so their corrections are not in
correction_items, rule_card examples, or story_prompt statistics. Writes

    eval/snapshots/<name>/chunks.jsonl     every chunk (basic + human-in-the-loop)
    eval/snapshots/<name>/manifest.json    inputs (with hashes), counts, held-out ids

Then run `node eval/embed_snapshot.mjs <name>`. Make a new snapshot (new name)
whenever the teacher's data changes -- e.g. vocab entries or scenes added after a
review -- and point the refined stage at it in eval/stages.json.

    python eval/make_snapshot.py <name> [--test-set eval/test_set_h20.json]

--test-set (default eval/test_set.json) names the stories to hold out. Besides
dropping their samples, the build stops if any chunk's text contains one of
their sentences (10+ characters) -- e.g. a held-out correction that reached a
rule card's examples through another route. One exception: an entry of one of
the teacher's hand-made lists (TEACHER_LIST_TYPES) that quotes a phrase found
only in held-out stories is dropped and listed in the manifest
("dropped_for_held_out") -- her example came from a test story.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPELINE = ROOT / "chinese_writing_rag_pipeline"
os.chdir(PIPELINE)  # the pipeline modules use paths relative to it
sys.path.insert(0, str(PIPELINE / "scripts"))

from chunk_builder import build_chunks, load_rule_labels  # noqa: E402
from build_iteration_chunks import (  # noqa: E402
    build_ai_critique_chunks, build_ai_error_cards, build_vocab_chunks,
    build_scene_list_chunks, build_vocab_suggestion_chunks, build_teacher_rule_chunks,
    VOCAB_PATH, SCENES_PATH, EXTRA_RULES_PATH,
    SUGGESTION_EXAMPLES_PATH, CRITIQUE_LABELS_PATH, CRITIQUE_REVISIONS_PATH, CRITIQUE_DOCS, ITERATION_DIR,
)
from parse_corpus import load_registry  # noqa: E402

INPUTS = ["extracted/basic_corpus.json", "raw/stories.json", "raw/correction_rules.json",
          str(VOCAB_PATH), str(SCENES_PATH), str(SUGGESTION_EXAMPLES_PATH), str(EXTRA_RULES_PATH),
          str(CRITIQUE_LABELS_PATH), str(CRITIQUE_REVISIONS_PATH), *(str(ITERATION_DIR / d) for d in CRITIQUE_DOCS),
          "raw/aligned_edits_train.jsonl", "scripts/rule_descriptions.py"]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]


TEACHER_LIST_TYPES = {"vocab_suggestion_example", "vocab_error", "teacher_rule"}


def quotes_only_in_held_out(chunk, held_texts, other_texts, min_len=5):
    """The chunk's “quoted” student phrases that occur in a held-out story and in no other story."""
    out = []
    for q in re.findall(r"“([^”]{%d,})”" % min_len, chunk["text"]):
        q = q.rstrip("。，")
        if any(q in t for t in held_texts) and not any(q in t for t in other_texts):
            out.append(q)
    return out


def held_out_sentences(test_set, min_len=10):
    out = set()
    for s in test_set["samples"]:
        for sent in re.split(r"(?<=[。！？!?])", s["raw_text"]):
            sent = sent.strip().rstrip("。！？!?")
            if len(sent) >= min_len:
                out.add(sent)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--test-set", default="eval/test_set.json",
                    help="test set whose stories are held out (path from the repo root)")
    args = ap.parse_args()
    name = args.name
    out_dir = ROOT / "eval/snapshots" / name
    if out_dir.exists():
        sys.exit(f"{out_dir} already exists -- snapshots are frozen; pick a new name")

    missing_inputs = [p for p in INPUTS if not Path(p).exists()]
    if missing_inputs:
        sys.exit(f"source files missing: {missing_inputs} -- restore them before building a snapshot")

    test_set = json.load(open(ROOT / args.test_set, encoding="utf-8"))
    held_out = {s["sample_id"] for s in test_set["samples"]}

    corpus = json.load(open("extracted/basic_corpus.json", encoding="utf-8"))
    missing = held_out - {s["sample_id"] for s in corpus["samples"]}
    if missing:
        sys.exit(f"held-out samples not in the corpus: {sorted(missing)}")
    held_texts = [s["raw_text"] for s in corpus["samples"] if s["sample_id"] in held_out]
    corpus = {**corpus, "samples": [s for s in corpus["samples"] if s["sample_id"] not in held_out]}
    other_texts = [s["raw_text"] for s in corpus["samples"]]

    basic, unlabelled = build_chunks(corpus, load_rule_labels())
    registry = load_registry()
    ai_items = build_ai_critique_chunks(registry, {s["sample_id"]: s for s in corpus["samples"]})
    scene_chunks, _ = build_scene_list_chunks(registry, corpus)
    chunks = (basic + ai_items + build_ai_error_cards(ai_items) + build_vocab_chunks(registry)
              + build_vocab_suggestion_chunks() + build_teacher_rule_chunks() + scene_chunks)

    dropped = {}
    for c in chunks:
        if c["chunk_type"] in TEACHER_LIST_TYPES:
            qs = quotes_only_in_held_out(c, held_texts, other_texts)
            if qs:
                dropped[c["chunk_id"]] = qs
    chunks = [c for c in chunks if c["chunk_id"] not in dropped]
    for cid, qs in dropped.items():
        print(f"dropped {cid}: quotes held-out text {qs}")

    ids = [c["chunk_id"] for c in chunks]
    if len(ids) != len(set(ids)):
        sys.exit("duplicate chunk ids")
    leaked = [c["chunk_id"] for c in chunks if c["metadata"].get("sample_id") in held_out]
    if leaked:
        sys.exit(f"held-out sample chunks leaked into the snapshot: {leaked[:5]}")
    sents = held_out_sentences(test_set)
    leaked_text = [(c["chunk_id"], x) for c in chunks for x in sents if x in c["text"]]
    if leaked_text:
        sys.exit(f"held-out sentences found in chunk text: {leaked_text[:5]}")

    out_dir.mkdir(parents=True)
    with open(out_dir / "chunks.jsonl", "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True,
                            cwd=ROOT).stdout.strip()
    manifest = {
        "name": name,
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "git_commit": commit,
        "test_set": args.test_set,
        "held_out": sorted(held_out),
        "inputs": {p: sha(p) for p in INPUTS},
        "counts": dict(Counter(c["chunk_type"] for c in chunks)),
        "dropped_for_held_out": dropped,
        "unlabelled_corrections": len(unlabelled),
    }
    with open(out_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print(f"Wrote {out_dir}: {len(chunks)} chunks {manifest['counts']}")
    print(f"Next: node eval/embed_snapshot.mjs {name}")


if __name__ == "__main__":
    main()
