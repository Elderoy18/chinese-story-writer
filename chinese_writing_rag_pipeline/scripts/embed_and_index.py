#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRODUCTION embedding + indexing script.

Embeds every chunk in chunks/chunks.jsonl with a multilingual sentence
embedding model and loads them into a persistent Chroma collection, with full
chunk metadata attached for filtered retrieval.

Model choice: this corpus mixes Chinese story/correction text with English
grammar explanations, so a *multilingual* embedding model is required (a
Chinese-only model will under-perform on the English rule explanations, and
vice versa). Good options, in rough order of quality/cost tradeoff:
  - "BAAI/bge-m3"                              (best quality, large, 1024-dim)
  - "intfloat/multilingual-e5-small"            (good quality/size balance, 384-dim)
  - "paraphrase-multilingual-MiniLM-L12-v2"     (smaller/faster, 384-dim)
  - OpenAI "text-embedding-3-small" / -large     (API-based, no local GPU needed)
  - Voyage AI "voyage-3-lite" / "voyage-3"       (API-based, strong on CJK)

NOTE: this sandboxed session has no outbound access to huggingface.co (model
downloads are blocked), so this script could not actually be executed here.
It is written to run as-is in a normal dev environment with internet access.
For a locally-runnable proof that the *chunking and retrieval logic* work,
see scripts/tfidf_demo_index.py + scripts/tfidf_demo_query.py, which use only
scikit-learn/jieba (pure PyPI, no model download) as a stand-in retriever.

Usage:
    python scripts/embed_and_index.py --model intfloat/multilingual-e5-small
"""
import argparse
import json
import sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunks", default="chunks/chunks.jsonl")
    ap.add_argument("--persist-dir", default="chunks/chroma_db")
    ap.add_argument("--collection", default="chinese_writing_feedback_rag")
    ap.add_argument("--model", default="intfloat/multilingual-e5-small")
    ap.add_argument("--batch-size", type=int, default=64)
    args = ap.parse_args()

    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
    except ImportError as e:
        sys.exit(f"Missing dependency ({e}). pip install chromadb sentence-transformers")

    print(f"Loading embedding model: {args.model}")
    model = SentenceTransformer(args.model)

    # e5-family models expect a "query: " / "passage: " instruction prefix for
    # best retrieval quality; harmless no-op prefix stripping for other models.
    is_e5 = "e5" in args.model.lower()

    client = chromadb.PersistentClient(path=args.persist_dir)
    collection = client.get_or_create_collection(
        name=args.collection, metadata={"hnsw:space": "cosine"}
    )

    chunks = [json.loads(l) for l in open(args.chunks, encoding="utf-8")]
    print(f"Embedding {len(chunks)} chunks...")

    ids, docs, metas = [], [], []
    for ch in chunks:
        ids.append(ch["chunk_id"])
        text = ch["text"]
        docs.append(f"passage: {text}" if is_e5 else text)
        meta = {"chunk_type": ch["chunk_type"], "text_raw": ch["text"][:2000]}
        for k, v in ch["metadata"].items():
            # Chroma metadata values must be str/int/float/bool; flatten lists.
            if isinstance(v, list):
                meta[k] = ", ".join(str(x) for x in v)
            elif v is None:
                continue
            else:
                meta[k] = v
        metas.append(meta)

    for i in range(0, len(ids), args.batch_size):
        batch_docs = docs[i:i + args.batch_size]
        embeddings = model.encode(batch_docs, show_progress_bar=False, normalize_embeddings=True)
        collection.upsert(
            ids=ids[i:i + args.batch_size],
            embeddings=embeddings.tolist(),
            documents=[ch["text"] for ch in chunks[i:i + args.batch_size]],
            metadatas=metas[i:i + args.batch_size],
        )
        print(f"  indexed {min(i + args.batch_size, len(ids))}/{len(ids)}")

    print(f"Done. Persisted Chroma collection '{args.collection}' at {args.persist_dir}")

if __name__ == "__main__":
    main()
