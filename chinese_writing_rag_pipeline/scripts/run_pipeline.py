#!/usr/bin/env python3
"""
Rebuild the RAG corpus from the source documents in one command.

    python chinese_writing_rag_pipeline/scripts/run_pipeline.py           # build chunks.jsonl
    python chinese_writing_rag_pipeline/scripts/run_pipeline.py --embed   # ...and load into Atlas

Steps:
  1. extract_json.py   raw/basic data/*, raw/iteration data/*  -> extracted/basic|iteration/*.json
  2. parse_corpus.py   extracted/... + raw/stories.json         -> extracted/corpus.json
  3. chunk_builder.py  corpus.json + raw/story_scenes.md + raw/vocab_errors.json
                                                                 -> chunks/chunks.jsonl
  4. (--embed) embed-to-mongo.mjs --prune                        -> rag_chunks in Atlas,
     re-embedding every chunk and deleting chunks no longer in chunks.jsonl.

Adding basic data:
  - More graded student stories: drop a .docx in raw/basic data/ whose file name
    contains the story's "match" word from raw/stories.json, laid out as
    "Student N" / story text / "Teacher feedback:" / one correction per line /
    "Miss ..." flags. A new story also needs an entry in raw/stories.json.
  - A new model story: add "Story N: <title>" + the text to the model stories doc
    and give the title a corpus ID in raw/stories.json.
Then re-run this script. Any layout problem stops the run with the file and the
sample it is in.
"""
import subprocess
import sys
from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = PIPELINE_ROOT / "scripts"


def run(cmd):
    print(f"\n=== {' '.join(str(c) for c in cmd[1:])} ===", flush=True)
    result = subprocess.run(cmd, cwd=PIPELINE_ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    for script in ("extract_json.py", "parse_corpus.py", "chunk_builder.py"):
        run([sys.executable, SCRIPTS / script])
    if "--embed" in sys.argv:
        run(["node", SCRIPTS / "embed-to-mongo.mjs", "--prune"])
    else:
        print("\nchunks/chunks.jsonl is rebuilt. To load it into Atlas, re-run with --embed.")


if __name__ == "__main__":
    main()
