#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRODUCTION embedding + indexing script for the *deployed app*.

Unlike embed_and_index.py (sentence-transformers + local Chroma), this script
targets the stack the Next.js app actually runs on:

  - embeddings: OpenAI ``text-embedding-3-small`` (1536-dim)
  - vector store: the same MongoDB Atlas database the app already uses
                  (collection ``rag_chunks`` in ``chinese-writer-data``)

It reads chunks/chunks.jsonl, embeds every chunk's ``text``, and upserts one
document per chunk keyed on ``chunk_id``. Retrieval happens at request time in
lib/rag/retrieve.ts via an Atlas ``$vectorSearch`` aggregation.

IMPORTANT: the query side (lib/rag/embed.ts) must embed with the SAME model.
If you change EMBED_MODEL here, change it there too and re-run this script.

Setup / run:
    pip install -r requirements.txt          # now includes openai + pymongo
    # from the repo root, so it picks up .env.local:
    #   MONGODB_URI=...      (already set for the app)
    #   OPENAI_API_KEY=...   (already set for the app)
    python chinese_writing_rag_pipeline/scripts/embed_to_mongo.py

    # then create the Atlas Vector Search index once -- see docs/atlas_setup.md
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

EMBED_MODEL = "text-embedding-3-small"
EMBED_DIM = 1536
DB_NAME = "chinese-writer-data"
COLLECTION = "rag_chunks"

REPO_ROOT = Path(__file__).resolve().parents[2]
PIPELINE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHUNKS = PIPELINE_ROOT / "chunks" / "chunks.jsonl"


def load_dotenv_local():
    """Minimal .env.local reader (no python-dotenv dependency)."""
    env_path = REPO_ROOT / ".env.local"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip())


def flatten_metadata(chunk):
    """Promote the fields we filter/display on to the top level of the Mongo
    doc. Lists (grammar_tags, story_ids, ...) stay as real arrays -- Atlas
    ``$vectorSearch`` filters handle array membership natively, unlike Chroma
    which forced a comma-joined string in embed_and_index.py."""
    md = dict(chunk["metadata"])
    doc = {
        "_id": chunk["chunk_id"],
        "chunk_id": chunk["chunk_id"],
        "chunk_type": chunk["chunk_type"],
        "text": chunk["text"],
    }
    doc.update(md)
    return doc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunks", default=str(DEFAULT_CHUNKS))
    ap.add_argument("--batch-size", type=int, default=128)
    ap.add_argument("--dry-run", action="store_true",
                    help="embed + print counts but do not write to Mongo")
    args = ap.parse_args()

    load_dotenv_local()

    try:
        from openai import OpenAI
        from pymongo import MongoClient, UpdateOne
    except ImportError as e:
        sys.exit(f"Missing dependency ({e}). pip install -r requirements.txt")

    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY not set (checked env + .env.local)")
    mongo_uri = os.environ.get("MONGODB_URI")
    if not mongo_uri and not args.dry_run:
        sys.exit("MONGODB_URI not set (checked env + .env.local)")

    chunks = [json.loads(l) for l in open(args.chunks, encoding="utf-8")]
    print(f"Loaded {len(chunks)} chunks from {args.chunks}")

    client = OpenAI()
    all_embeddings = []
    for i in range(0, len(chunks), args.batch_size):
        batch = chunks[i:i + args.batch_size]
        for attempt in range(5):
            try:
                resp = client.embeddings.create(
                    model=EMBED_MODEL,
                    input=[c["text"] for c in batch],
                )
                break
            except Exception as e:  # noqa: BLE001 - transient API errors
                wait = 2 ** attempt
                print(f"  embed batch {i} failed ({e}); retrying in {wait}s")
                time.sleep(wait)
        else:
            sys.exit(f"embedding failed after retries at batch {i}")
        all_embeddings.extend(d.embedding for d in resp.data)
        print(f"  embedded {min(i + args.batch_size, len(chunks))}/{len(chunks)}")

    assert len(all_embeddings) == len(chunks)
    assert len(all_embeddings[0]) == EMBED_DIM, (
        f"expected {EMBED_DIM}-dim vectors, got {len(all_embeddings[0])}"
    )

    if args.dry_run:
        print("--dry-run: skipping Mongo write")
        return

    mc = MongoClient(mongo_uri)
    coll = mc[DB_NAME][COLLECTION]
    ops = []
    for chunk, emb in zip(chunks, all_embeddings):
        doc = flatten_metadata(chunk)
        doc["embedding"] = emb
        doc["embed_model"] = EMBED_MODEL
        ops.append(UpdateOne({"_id": doc["_id"]}, {"$set": doc}, upsert=True))

    result = coll.bulk_write(ops, ordered=False)
    print(f"Upserted into {DB_NAME}.{COLLECTION}: "
          f"{result.upserted_count} inserted, {result.modified_count} updated, "
          f"{coll.count_documents({})} total docs")
    print("\nNext: create the Atlas Vector Search index -> docs/atlas_setup.md")


if __name__ == "__main__":
    main()
