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

    python eval/make_snapshot.py <name>
"""
import hashlib
import json
import os
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
    build_scene_list_chunks, build_vocab_suggestion_chunks, VOCAB_PATH, SCENES_PATH,
    SUGGESTION_EXAMPLES_PATH,
)
from parse_corpus import load_registry  # noqa: E402

INPUTS = ["extracted/basic_corpus.json", "raw/stories.json", "raw/correction_rules.json",
          str(VOCAB_PATH), str(SCENES_PATH), str(SUGGESTION_EXAMPLES_PATH)]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python eval/make_snapshot.py <name>")
    name = sys.argv[1]
    out_dir = ROOT / "eval/snapshots" / name
    if out_dir.exists():
        sys.exit(f"{out_dir} already exists -- snapshots are frozen; pick a new name")

    test_set = json.load(open(ROOT / "eval/test_set.json", encoding="utf-8"))
    held_out = {s["sample_id"] for s in test_set["samples"]}

    corpus = json.load(open("extracted/basic_corpus.json", encoding="utf-8"))
    missing = held_out - {s["sample_id"] for s in corpus["samples"]}
    if missing:
        sys.exit(f"held-out samples not in the corpus: {sorted(missing)}")
    corpus = {**corpus, "samples": [s for s in corpus["samples"] if s["sample_id"] not in held_out]}

    basic, unlabelled = build_chunks(corpus, load_rule_labels())
    registry = load_registry()
    ai_items = build_ai_critique_chunks(registry, {s["sample_id"]: s for s in corpus["samples"]})
    scene_chunks, _ = build_scene_list_chunks(registry, corpus)
    chunks = (basic + ai_items + build_ai_error_cards(ai_items) + build_vocab_chunks(registry)
              + build_vocab_suggestion_chunks() + scene_chunks)

    ids = [c["chunk_id"] for c in chunks]
    if len(ids) != len(set(ids)):
        sys.exit("duplicate chunk ids")
    leaked = [c["chunk_id"] for c in chunks if c["metadata"].get("sample_id") in held_out]
    if leaked:
        sys.exit(f"held-out sample chunks leaked into the snapshot: {leaked[:5]}")

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
        "held_out": sorted(held_out),
        "inputs": {p: sha(p) for p in INPUTS},
        "counts": dict(Counter(c["chunk_type"] for c in chunks)),
        "unlabelled_corrections": len(unlabelled),
    }
    with open(out_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print(f"Wrote {out_dir}: {len(chunks)} chunks {manifest['counts']}")
    print(f"Next: node eval/embed_snapshot.mjs {name}")


if __name__ == "__main__":
    main()
