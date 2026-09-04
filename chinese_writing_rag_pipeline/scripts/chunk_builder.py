#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the hierarchical RAG chunk set from extracted/corpus.json.

Chunk types (see docs/design.md for full rationale):
  story_prompt   -- one per writing-prompt/story (top anchor: model text + canonical
                     scene checklist + aggregate stats)
  model_story    -- the near-perfect exemplar text for a story prompt
  sample         -- one full student story instance (parent for everything below)
  correction_item-- one atomic teacher gold correction (original -> corrected, why)
  ai_feedback_item-- one atomic AI feedback item + teacher's critique of it
  content_flag   -- one structured content-coverage/coherence/factual flag
  rule_card      -- aggregated exemplars of one grammar/linguistic point across the corpus
  ai_error_card  -- aggregated exemplars of one AI-feedback-failure-mode across the corpus

Every chunk is a flat dict: {chunk_id, chunk_type, text, metadata{...}}
so a single vector collection can hold everything and be filtered by chunk_type /
story_id / grammar_tags / eval_tags / doc_type at query time (metadata filtering),
while parent_id links let a retriever "expand" an atomic hit back up to its
sample or story_prompt context (small-to-big / parent-document retrieval).
"""
import json
import re
import sys
from collections import defaultdict, Counter

sys.path.insert(0, "scripts")
from tagging import tag_grammar_text, tag_ai_eval_text, parse_content_flag, split_correction
from rule_descriptions import GRAMMAR_RULE_DESC, AI_EVAL_DESC

MAX_RULE_CARD_EXAMPLES = 8
MAX_AI_ERROR_CARD_EXAMPLES = 6


def dedup_key(t):
    """Normalize a scene-description string for de-duplication purposes only
    (collapse whitespace differences); the original, readable spacing is kept
    separately for display)."""
    return re.sub(r"\s+", " ", t).strip("。.;； ").lower()


def build_scene_checklists(corpus):
    """Derive a canonical 'required plot beats' checklist per story from the
    union of every 'Miss scene' annotation the teacher wrote for that story."""
    per_story_counts = defaultdict(Counter)
    per_story_display = defaultdict(dict)
    for s in corpus["samples"]:
        for f in s["content_flags"]:
            rec = parse_content_flag(f)
            if rec["flag_type"] != "miss_scene":
                continue
            for item in rec.get("missing_scene_items", []):
                item = item.strip()
                key = dedup_key(item)
                if key:
                    per_story_counts[s["story_id"]][key] += 1
                    per_story_display[s["story_id"]].setdefault(key, item)
    checklists = {}
    for story_id, counter in per_story_counts.items():
        checklists[story_id] = [
            {"scene_description": per_story_display[story_id][key], "times_flagged_missing": cnt}
            for key, cnt in counter.most_common()
        ]
    return checklists


def make_chunk(chunk_id, chunk_type, text, **meta):
    return {"chunk_id": chunk_id, "chunk_type": chunk_type, "text": text, "metadata": meta}


def build_chunks(corpus):
    chunks = []

    model_by_story = {m["story_id"]: m for m in corpus["model_stories"]}
    scene_checklists = build_scene_checklists(corpus)

    # ---- model_story chunks -------------------------------------------------
    for m in corpus["model_stories"]:
        chunks.append(make_chunk(
            f"model_story:{m['story_id']}", "model_story", m["text"],
            story_id=m["story_id"], title=m["title"], doc_type="model",
            source_doc="model_stories",
        ))

    # ---- per-sample chunk tree ----------------------------------------------
    story_stats = defaultdict(lambda: {"n_samples": 0, "grammar_tags": Counter(), "ai_eval_tags": Counter()})

    for s in corpus["samples"]:
        sid = s["sample_id"]
        story_stats[s["story_id"]]["n_samples"] += 1

        chunks.append(make_chunk(
            f"sample:{sid}", "sample", s["raw_text"],
            source_doc=s["source_doc"], doc_type=s["doc_type"], story_id=s["story_id"],
            sample_id=sid, n_teacher_items=len(s["teacher_correction_items"]),
            n_ai_items=len(s["ai_feedback_items"]), n_content_flags=len(s["content_flags"]),
        ))

        for idx, raw in enumerate(s["teacher_correction_items"]):
            split = split_correction(raw)
            gtags = tag_grammar_text(raw)
            story_stats[s["story_id"]]["grammar_tags"].update(gtags)
            chunks.append(make_chunk(
                f"correction_item:{sid}::c{idx}", "correction_item", raw,
                source_doc=s["source_doc"], doc_type=s["doc_type"], story_id=s["story_id"],
                sample_id=sid, parent_id=f"sample:{sid}",
                original_span=split["original_span"], corrected_span=split["corrected_span"],
                explanation=split["explanation"], grammar_tags=gtags,
            ))

        for idx, item in enumerate(s["ai_feedback_items"]):
            comment = item.get("my_comment") or ""
            etags = tag_ai_eval_text(comment) if comment else []
            story_stats[s["story_id"]]["ai_eval_tags"].update(etags)
            gtags_ai = tag_grammar_text(item["raw_text"])
            text = item["raw_text"] + ("\n" + comment if comment else "")
            chunks.append(make_chunk(
                f"ai_feedback_item:{sid}::a{idx}", "ai_feedback_item", text,
                source_doc=s["source_doc"], doc_type=s["doc_type"], story_id=s["story_id"],
                sample_id=sid, parent_id=f"sample:{sid}",
                ai_category=item["category"], ai_raw_text=item["raw_text"],
                teacher_comment=comment, eval_tags=etags, grammar_tags=gtags_ai,
            ))

        for idx, raw in enumerate(s["content_flags"]):
            rec = parse_content_flag(raw)
            chunks.append(make_chunk(
                f"content_flag:{sid}::f{idx}", "content_flag", raw,
                source_doc=s["source_doc"], doc_type=s["doc_type"], story_id=s["story_id"],
                sample_id=sid, parent_id=f"sample:{sid}", **{k: v for k, v in rec.items() if k != "raw_text"},
            ))

    # ---- story_prompt anchor chunks -----------------------------------------
    all_story_ids = set(story_stats.keys()) | set(model_by_story.keys())
    empty_stats = {"n_samples": 0, "grammar_tags": Counter(), "ai_eval_tags": Counter()}
    for story_id in all_story_ids:
        stats = story_stats.get(story_id, empty_stats)
        model = model_by_story.get(story_id)
        checklist = scene_checklists.get(story_id, [])
        lines = [f"Story prompt: {story_id}"]
        if model:
            lines.append(f"Model exemplar title: {model['title']}")
        lines.append(f"Reviewed student samples: {stats['n_samples']}")
        if checklist:
            lines.append("Canonical required plot beats (derived from teacher 'missing scene' annotations):")
            for c in checklist:
                lines.append(f"  - {c['scene_description']} (flagged missing in {c['times_flagged_missing']} samples)")
        if stats["grammar_tags"]:
            top = ", ".join(f"{t}×{n}" for t, n in stats["grammar_tags"].most_common(10))
            lines.append(f"Most common grammar issues in this batch: {top}")
        if stats["ai_eval_tags"]:
            top = ", ".join(f"{t}×{n}" for t, n in stats["ai_eval_tags"].most_common(10))
            lines.append(f"AI-feedback quality issues observed: {top}")
        text = "\n".join(lines)
        chunks.append(make_chunk(
            f"story_prompt:{story_id}", "story_prompt", text,
            story_id=story_id, doc_type="story_prompt",
            has_model_story=bool(model), n_samples=stats["n_samples"],
            n_scene_checklist_items=len(checklist),
        ))

    # ---- rule_card chunks (aggregate grammar tags across whole corpus) -----
    grammar_examples = defaultdict(list)
    for ch in chunks:
        if ch["chunk_type"] == "correction_item":
            for tag in ch["metadata"]["grammar_tags"]:
                grammar_examples[tag].append(ch)

    for tag, examples in grammar_examples.items():
        desc = GRAMMAR_RULE_DESC.get(tag, "")
        picked = examples[:MAX_RULE_CARD_EXAMPLES]
        lines = [f"Grammar/linguistic point: {tag}", desc, "Examples (original -> corrected, why):"]
        story_ids = set()
        for ex in picked:
            md = ex["metadata"]
            story_ids.add(md["story_id"])
            orig = md.get("original_span") or "(see raw)"
            corr = md.get("corrected_span") or ""
            expl = md.get("explanation") or ""
            lines.append(f"  - {orig} -> {corr}" + (f"  [{expl}]" if expl else ""))
        text = "\n".join(lines)
        chunks.append(make_chunk(
            f"rule_card:{tag}", "rule_card", text,
            grammar_tag=tag, description=desc, n_examples_total=len(examples),
            example_sample_ids=[e["metadata"]["sample_id"] for e in picked],
            story_ids=sorted(story_ids),
        ))

    # ---- ai_error_card chunks (aggregate AI-feedback failure modes) --------
    ai_examples = defaultdict(list)
    for ch in chunks:
        if ch["chunk_type"] == "ai_feedback_item":
            for tag in ch["metadata"]["eval_tags"]:
                ai_examples[tag].append(ch)

    for tag, examples in ai_examples.items():
        desc = AI_EVAL_DESC.get(tag, "")
        picked = examples[:MAX_AI_ERROR_CARD_EXAMPLES]
        lines = [f"AI-feedback calibration pattern: {tag}", desc, "Examples (AI said / teacher's verdict):"]
        for ex in picked:
            md = ex["metadata"]
            lines.append(f"  - AI: {md['ai_raw_text']}")
            lines.append(f"    Teacher: {md['teacher_comment']}")
        text = "\n".join(lines)
        chunks.append(make_chunk(
            f"ai_error_card:{tag}", "ai_error_card", text,
            eval_tag=tag, description=desc, n_examples_total=len(examples),
            example_sample_ids=[e["metadata"]["sample_id"] for e in picked],
        ))

    return chunks, scene_checklists


def main():
    corpus = json.load(open("extracted/corpus.json", encoding="utf-8"))
    chunks, scene_checklists = build_chunks(corpus)

    with open("chunks/chunks.jsonl", "w", encoding="utf-8") as f:
        for ch in chunks:
            f.write(json.dumps(ch, ensure_ascii=False) + "\n")

    with open("chunks/scene_checklists.json", "w", encoding="utf-8") as f:
        json.dump(scene_checklists, f, ensure_ascii=False, indent=1)

    by_type = Counter(ch["chunk_type"] for ch in chunks)
    print("Total chunks:", len(chunks))
    for t, n in by_type.most_common():
        print(f"  {t:20s} {n}")

if __name__ == "__main__":
    main()
