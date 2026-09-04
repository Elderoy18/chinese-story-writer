#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
End-to-end demo: given a NEW (unseen) student story, retrieve the right
hierarchy of chunks and assemble the final prompt that would be sent to the
feedback-generating LLM.

This is the piece that actually operationalizes the RAG system: instead of
asking a bare LLM to "give feedback on this Chinese story", we ground it with
(1) the story's model exemplar + auto-derived required-scene checklist,
(2) grammar/vocabulary rule cards relevant to the errors actually present,
(3) AI-feedback calibration cards -- concrete examples of the 5 failure modes
    the teacher identified, so the generator is explicitly warned against
    repeating them,
(4) a handful of nearest real correction_item exemplars for style-matching.

Uses the local TF-IDF retriever (scripts/local_demo.py) so it is runnable in
this sandbox without model downloads; swap `search()`/`get_collection()` for
scripts/retrieve.py's Chroma-backed versions in a real deployment -- the
prompt-assembly logic below is retriever-agnostic.
"""
import json
import sys
sys.path.insert(0, "scripts")
from local_demo import build_index, search, tokenize  # noqa: F401 (tokenize needed for pickle-safe reload)

SYSTEM_INSTRUCTIONS = """You are a Chinese-language writing tutor giving feedback to an early learner \
on a short narrative writing assignment. Follow these rules, which come directly from the \
supervising teacher's review of this system's past mistakes:

1. Only give feedback on ACTUAL errors. If a sentence is already correct, say nothing about it in \
   the error sections -- do not write "no correction needed, it is grammatically correct" as a feedback \
   item. Save all positive remarks for a single closing "Encouragement" section.
2. Be exhaustive: scan every sentence. Past runs of this system frequently missed real errors -- do not \
   stop after finding a few.
3. When you flag a span, your corrected version AND your explanation must both be linguistically \
   correct, and the explanation must state the actual grammatical rule involved (not just "this is \
   unclear").
4. Point your feedback at the exact span that is wrong. Do not label span A as incorrect and then \
   explain span B.
5. Categorize correctly: 错别字/Wrong Characters is for mis-written characters only; word-choice problems \
   go under Vocabulary Suggestions; syntax/morphology problems go under Grammar Corrections. Do not mix \
   these up.
6. This transcript has already been cleaned of speech disfluencies (repetitions, false starts, filler \
   pauses) -- do not flag anything as an error on the grounds that it looks like a repetition or a pause.
7. After grammar/vocabulary feedback, separately check story CONTENT: compare against the required plot \
   beats below and note any that are missing or misremembered, and note if the writing lacks sufficient \
   descriptive detail.

Output format: three sections -- "Grammar Corrections", "Vocabulary Suggestions", and "Content & \
Coverage" (missing/incorrect plot points, coherence) -- each as a list of "original span：corrected \
span，explanation" items (empty if nothing to flag), followed by a short "Encouragement" paragraph.
"""

def format_rule_card(hit):
    md = hit["metadata"]
    return f"### Rule: {md['grammar_tag']}\n{hit['text']}"

def format_error_card(hit):
    md = hit["metadata"]
    return f"### AI failure mode to avoid: {md['eval_tag']}\n{hit['text']}"

def assemble(student_text, story_id, chunks_by_id, vectorizer, matrix, chunks, top_rules=4, top_calibration=3, top_examples=3):
    story_card = chunks_by_id.get(f"story_prompt:{story_id}")
    model_card = chunks_by_id.get(f"model_story:{story_id}")

    rule_hits = search(vectorizer, matrix, chunks, student_text, chunk_types=["rule_card"], k=top_rules)
    # Always include the highest-value calibration cards (the false-positive /
    # misdirected / miscategorized modes), regardless of lexical similarity to
    # this particular story, since they are process guardrails, not content matches.
    priority_eval_tags = [
        "false_positive_unneeded_correction", "misleading_no_error_framing",
        "misdirected_feedback", "miscategorized_error_type", "disfluency_false_positive",
    ]
    calibration_hits = [(1.0, chunks_by_id[f"ai_error_card:{t}"]) for t in priority_eval_tags
                         if f"ai_error_card:{t}" in chunks_by_id][:top_calibration]
    example_hits = search(vectorizer, matrix, chunks, student_text, chunk_types=["correction_item"], k=top_examples)

    parts = [SYSTEM_INSTRUCTIONS]

    if model_card:
        parts.append(f"### Model exemplar for this prompt ({model_card['metadata']['title']})\n{model_card['text']}")
    if story_card:
        parts.append(f"### Required plot beats / prior batch stats\n{story_card['text']}")

    if rule_hits:
        parts.append("## Relevant grammar rule cards (ground your explanations in these)")
        for score, hit in rule_hits:
            parts.append(format_rule_card(hit))

    if calibration_hits:
        parts.append("## AI-feedback calibration guardrails (avoid repeating these documented failure modes)")
        for score, hit in calibration_hits:
            parts.append(format_error_card(hit))

    if example_hits:
        parts.append("## Nearby real correction exemplars (style reference for how to phrase corrections)")
        for score, hit in example_hits:
            parts.append(f"- {hit['text']}")

    parts.append(f"## Student's story to review\n{student_text}")
    return "\n\n".join(parts)

def main():
    vectorizer, matrix, chunks = build_index()
    chunks_by_id = {c["chunk_id"]: c for c in chunks}

    # A brand-new (unseen) toy submission for the 孟母三迁 prompt, deliberately
    # containing: a directional-complement error, a redundant repeated subject,
    # and missing the "market" scene -- to show retrieval pulling exactly the
    # right cards.
    new_student_text = (
        "孟子小的时候，他跟他的妈妈住在墓地的旁边。他常常跟朋友玩，跟朋友玩祭拜的游戏。"
        "孟母觉得不好，所以他们搬家去了学校的旁边。孟子每天都在学校学习，后来他成为了很有名的哲学家。"
    )
    prompt = assemble(new_student_text, "mengmu_san_qian", chunks_by_id, vectorizer, matrix, chunks)

    with open("chunks/example_assembled_prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)

    print(f"Assembled prompt: {len(prompt)} chars (~{len(prompt)//4} tokens est.)")
    print("Saved to chunks/example_assembled_prompt.txt")
    print("\n----- PREVIEW (first 2000 chars) -----\n")
    print(prompt[:2000])

if __name__ == "__main__":
    main()
