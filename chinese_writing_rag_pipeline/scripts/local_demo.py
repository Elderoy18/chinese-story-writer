#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LOCAL, DEPENDENCY-LIGHT verification demo.

This sandbox has no outbound access to huggingface.co, so the production
sentence-embedding pipeline (embed_and_index.py / retrieve.py) can't actually
be executed here. This script proves out the same chunking + hierarchical
retrieval + metadata-filtering logic using a TF-IDF vector space instead
(scikit-learn + jieba, both pure-PyPI, no model download needed), so the
pipeline can be verified end-to-end today. Swap in embed_and_index.py /
retrieve.py in a normal environment for real semantic (not just lexical)
retrieval quality.

Usage:
    python scripts/local_demo.py                 # builds index + runs demo queries
"""
import json
import pickle
import re
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CHUNKS_PATH = "chunks/chunks.jsonl"
INDEX_PATH = "chunks/tfidf_index.pkl"


def tokenize(text):
    """Mixed Chinese/English tokenizer: jieba-segment CJK runs, keep English
    words and rule-notation tokens (了, 着, 把, etc. survive as single-char
    jieba tokens; ASCII words survive as-is)."""
    text = text.lower()
    tokens = []
    for seg in re.findall(r"[一-鿿]+|[a-zA-Z0-9]+", text):
        if re.match(r"[一-鿿]", seg):
            tokens.extend(jieba.lcut(seg))
        else:
            tokens.append(seg)
    return tokens


def build_index():
    chunks = [json.loads(l) for l in open(CHUNKS_PATH, encoding="utf-8")]
    corpus = [c["text"] for c in chunks]
    vectorizer = TfidfVectorizer(tokenizer=tokenize, lowercase=False, token_pattern=None)
    matrix = vectorizer.fit_transform(corpus)
    with open(INDEX_PATH, "wb") as f:
        pickle.dump({"vectorizer": vectorizer, "matrix": matrix, "chunks": chunks}, f)
    print(f"Indexed {len(chunks)} chunks -> {INDEX_PATH}")
    return vectorizer, matrix, chunks


def load_index():
    with open(INDEX_PATH, "rb") as f:
        d = pickle.load(f)
    return d["vectorizer"], d["matrix"], d["chunks"]


def search(vectorizer, matrix, chunks, query, chunk_types=None, story_id=None, k=5):
    qv = vectorizer.transform([query])
    sims = cosine_similarity(qv, matrix)[0]
    order = sims.argsort()[::-1]
    results = []
    for idx in order:
        ch = chunks[idx]
        if chunk_types and ch["chunk_type"] not in chunk_types:
            continue
        if story_id and ch["metadata"].get("story_id") != story_id:
            continue
        if sims[idx] <= 0:
            continue
        results.append((sims[idx], ch))
        if len(results) >= k:
            break
    return results


def expand_to_parent(chunks_by_id, ch):
    parent_id = ch["metadata"].get("parent_id")
    return chunks_by_id.get(parent_id)


def print_hits(results, chunks_by_id=None, expand=False):
    for score, ch in results:
        print(f"  [{score:.3f}] ({ch['chunk_type']}) {ch['chunk_id']}")
        print(f"      {ch['text'][:180].replace(chr(10), ' | ')}")
        if expand and chunks_by_id:
            parent = expand_to_parent(chunks_by_id, ch)
            if parent:
                print(f"      -> parent [{parent['chunk_type']}] {parent['chunk_id']}: "
                      f"{parent['text'][:120].replace(chr(10), ' | ')}")
    print()


def main():
    vectorizer, matrix, chunks = build_index()
    chunks_by_id = {c["chunk_id"]: c for c in chunks}

    print("\n" + "=" * 90)
    print("DEMO 1: a NEW student sentence with a directional-complement error")
    print("        (should surface the directional_complement rule_card + similar")
    print("        correction_item exemplars)")
    print("=" * 90)
    q = "他走去学校，没有停下来。"
    print(f"query: {q!r}\n")
    print("-- rule_card / correction_item hits --")
    print_hits(search(vectorizer, matrix, chunks, q,
                       chunk_types=["rule_card", "correction_item"], k=5))

    print("=" * 90)
    print("DEMO 2: meta-query for AI-feedback calibration -- 'AI says no correction")
    print("        needed but the phrasing is misleading' (should surface")
    print("        ai_error_card:misleading_no_error_framing / false_positive_*)")
    print("=" * 90)
    q2 = "AI feedback says no correction needed but explanation is misleading, over-correction of something already correct"
    print(f"query: {q2!r}\n")
    print_hits(search(vectorizer, matrix, chunks, q2, chunk_types=["ai_error_card"], k=5))

    print("=" * 90)
    print("DEMO 3: story-scoped content-coverage lookup for 孟母三迁")
    print("        (retrieves the story_prompt anchor card with the auto-derived")
    print("        canonical scene checklist)")
    print("=" * 90)
    q3 = "孟母三迁 故事 缺少情节 环节"
    print(f"query: {q3!r}\n")
    print_hits(search(vectorizer, matrix, chunks, q3,
                       chunk_types=["story_prompt"], story_id="mengmu_san_qian", k=2))

    print("=" * 90)
    print("DEMO 4: small-to-big expansion -- an atomic correction_item hit expanded")
    print("        back up to its parent sample (full student story) for context")
    print("=" * 90)
    q4 = "把梨放进筐里"
    print(f"query: {q4!r}\n")
    hits = search(vectorizer, matrix, chunks, q4, chunk_types=["correction_item"], k=3)
    print_hits(hits, chunks_by_id=chunks_by_id, expand=True)


if __name__ == "__main__":
    main()
