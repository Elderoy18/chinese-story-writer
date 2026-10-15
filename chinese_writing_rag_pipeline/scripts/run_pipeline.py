#!/usr/bin/env python3
"""
Rebuild the RAG knowledge base from the source documents in one command.

    python chinese_writing_rag_pipeline/scripts/run_pipeline.py           # build the chunk files
    python chinese_writing_rag_pipeline/scripts/run_pipeline.py --embed   # ...and load into Atlas

Two separate builds, one per kind of data:

  Basic data -- raw/basic data/ (graded samples + model stories, before any AI round)
    1. extract_json.py    raw/basic data/*              -> extracted/basic/*.json
    2. parse_corpus.py    + raw/stories.json (corpus IDs) -> extracted/basic_corpus.json
    3. chunk_builder.py                                  -> chunks/basic_chunks.jsonl

  Human-in-the-loop data -- raw/iteration data/ (the teacher's review of the system)
    4. build_iteration_chunks.py  AI critiques, vocab_errors.json, story_scenes.md
                                                         -> chunks/iteration_chunks.jsonl

  5. (--embed) embed-to-mongo.mjs --prune -> rag_chunks in Atlas: re-embeds
     every chunk in both files and deletes chunks that are in neither.

Adding basic data:
  - More graded student stories: drop a .docx in raw/basic data/ whose file name
    contains the story's "match" word from raw/stories.json, laid out as
    "Student N" / story text / "Teacher feedback:" / one correction per line /
    "Miss ..." flags. A new story also needs an entry in raw/stories.json.
  - A new model story: add "Story N: <title>" + the text to the model stories doc
    and give the title a corpus ID in raw/stories.json.
Then re-run this script. Any layout problem stops the run with the file and the
sample it is in.

Grammar rules for each correction come from raw/correction_rules.json. New
corrections have no label yet: they fall back to the regex tagger and are listed
in extracted/unlabelled_corrections.json. Label them (rule names from
scripts/rule_descriptions.py), add them to raw/correction_rules.json, and re-run.
"""
import os
import subprocess
import sys
from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = PIPELINE_ROOT / "scripts"


def run(cmd):
    print(f"\n=== {' '.join(str(c) for c in cmd[1:])} ===", flush=True)
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}  # no __pycache__ in scripts/
    result = subprocess.run(cmd, cwd=PIPELINE_ROOT, env=env)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    for script in ("extract_json.py", "parse_corpus.py", "chunk_builder.py",
                   "build_iteration_chunks.py"):
        run([sys.executable, SCRIPTS / script])
    if "--embed" in sys.argv:
        run(["node", SCRIPTS / "embed-to-mongo.mjs", "--prune"])
    else:
        print("\nChunk files rebuilt. To load them into Atlas, re-run with --embed.")


if __name__ == "__main__":
    main()
