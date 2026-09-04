#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRODUCTION hierarchical retriever over the Chroma collection built by
embed_and_index.py. Supports metadata-filtered semantic search plus
"small-to-big" parent expansion (an atomic correction_item/ai_feedback_item
hit can be expanded back up to its parent `sample` chunk for full context).

Example:
    python scripts/retrieve.py "他走去公园" --chunk-types correction_item rule_card --k 5
"""
import argparse
import json

def get_collection(persist_dir="chunks/chroma_db", collection="chinese_writing_feedback_rag"):
    import chromadb
    client = chromadb.PersistentClient(path=persist_dir)
    return client.get_collection(collection)

def embed_query(model, text, is_e5):
    q = f"query: {text}" if is_e5 else text
    return model.encode([q], normalize_embeddings=True)[0].tolist()

def search(collection, model, is_e5, query_text, chunk_types=None, story_id=None,
           grammar_tag=None, eval_tag=None, k=5):
    where = {}
    clauses = []
    if chunk_types:
        clauses.append({"chunk_type": {"$in": chunk_types}})
    if story_id:
        clauses.append({"story_id": story_id})
    if grammar_tag:
        # grammar_tags is stored as a comma-joined string; substring match isn't
        # supported by Chroma's `where`, so tag-exact filtering is best done on
        # single-tag fields (see chunk_builder: rule_card.grammar_tag) or via a
        # separate keyword pre-filter. Kept here for rule_card/single-tag chunks.
        clauses.append({"grammar_tag": grammar_tag})
    if eval_tag:
        clauses.append({"eval_tag": eval_tag})
    if len(clauses) == 1:
        where = clauses[0]
    elif len(clauses) > 1:
        where = {"$and": clauses}

    query_embedding = embed_query(model, query_text, is_e5)
    res = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        where=where or None,
    )
    hits = []
    for i in range(len(res["ids"][0])):
        hits.append({
            "chunk_id": res["ids"][0][i],
            "distance": res["distances"][0][i],
            "text": res["documents"][0][i],
            "metadata": res["metadatas"][0][i],
        })
    return hits

def expand_to_parent(collection, hit):
    parent_id = hit["metadata"].get("parent_id")
    if not parent_id:
        return None
    got = collection.get(ids=[parent_id])
    if not got["ids"]:
        return None
    return {"chunk_id": got["ids"][0], "text": got["documents"][0], "metadata": got["metadatas"][0]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--chunk-types", nargs="*", default=None)
    ap.add_argument("--story-id", default=None)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--model", default="intfloat/multilingual-e5-small")
    ap.add_argument("--expand-parent", action="store_true")
    args = ap.parse_args()

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(args.model)
    is_e5 = "e5" in args.model.lower()
    collection = get_collection()

    hits = search(collection, model, is_e5, args.query,
                  chunk_types=args.chunk_types, story_id=args.story_id, k=args.k)
    for h in hits:
        print(f"[{h['distance']:.3f}] {h['chunk_id']}")
        print(f"    {h['text'][:200]}")
        if args.expand_parent:
            parent = expand_to_parent(collection, h)
            if parent:
                print(f"    -> parent {parent['chunk_id']}: {parent['text'][:150]}")
        print()

if __name__ == "__main__":
    main()
