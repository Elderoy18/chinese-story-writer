#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the basic-data RAG chunk set from extracted/basic_corpus.json
-> chunks/basic_chunks.jsonl. Basic data only: graded samples and model
stories. Human-in-the-loop chunks (AI critiques, vocab list, scene lists) are
built separately by build_iteration_chunks.py.

Chunk types (see docs/design.md for full rationale):
  story_prompt   -- one per story (top anchor: model title + sample stats + the
                     scenes students most often left out)
  model_story    -- the near-perfect exemplar text for a story prompt
  sample         -- one full student story instance (parent for everything below)
  correction_item-- one atomic teacher gold correction (original -> corrected, why)
  content_flag   -- one structured content-coverage/coherence/factual flag
  rule_card      -- aggregated exemplars of one grammar/linguistic point across the corpus
  rule_example   -- one student sentence she corrected under one rule (the student's own
                     words); parent_id = its rule_card, so a similarity hit on a student
                     sentence with the same error leads to the card

Grammar rules per correction come from raw/correction_rules.json (labels keyed by
the correction's text). Where the correction has exact edits on the story text
(raw/aligned_edits_train.jsonl), the correction_item carries them, rule-card
examples show the student's whole clause before and after her fix, and each
rule card gets her standard fix (metadata `standard_fix`, from corrections with
that rule only). A correction with no label there falls back to the
regex tagger (tagging.py) and is listed in extracted/unlabelled_corrections.json
so it can be labelled.

Every chunk is a flat dict: {chunk_id, chunk_type, text, metadata{...}}
so a single vector collection can hold everything and be filtered by chunk_type /
story_id / grammar_tags / doc_type at query time (metadata filtering),
while parent_id links let a retriever "expand" an atomic hit back up to its
sample or story_prompt context (small-to-big / parent-document retrieval).
"""
import json
import os
import re
import sys
from collections import defaultdict, Counter

sys.path.insert(0, "scripts")
from tagging import tag_grammar_text, parse_content_flag, split_correction
from rule_descriptions import GRAMMAR_RULE_DESC, NO_RULE_CARD
from aligned_edits import load_aligned_edits, before_after, standard_fix

CORPUS_PATH = "extracted/basic_corpus.json"
RULE_LABELS_PATH = "raw/correction_rules.json"
UNLABELLED_PATH = "extracted/unlabelled_corrections.json"
# Regex triggers per rule card (S7-4): a match in the student's scene brings the card
# into the prompt. Optional: the file is new, and snapshots built before it have none.
RULE_CARD_TRIGGERS_PATH = "raw/iteration data/rule_card_triggers.json"
OUT_PATH = "chunks/basic_chunks.jsonl"
MAX_RULE_CARD_EXAMPLES = 8


def load_rule_labels():
    labels = json.load(open(RULE_LABELS_PATH, encoding="utf-8"))["rules"]
    unknown = sorted({r for rules in labels.values() for r in rules} - set(GRAMMAR_RULE_DESC))
    if unknown:
        sys.exit(f"{RULE_LABELS_PATH}: rules with no description in rule_descriptions.py: {unknown}")
    return labels


def pick_examples(tag, examples, n):
    """Choose a rule card's examples: first corrections whose explanation names
    this rule in the teacher's own shorthand (the regex tagger finds exactly
    those), then ones with any explanation, then the rest; spread round-robin
    across stories (in corpus order), with no repeated original span -- so the
    card shows the rule's range, not just the first story's first few hits."""
    ranked = sorted(examples, key=lambda e: (tag not in tag_grammar_text(e["text"]),
                                             not e["metadata"]["explanation"]))
    by_story = defaultdict(list)
    for ex in ranked:
        by_story[ex["metadata"]["story_id"]].append(ex)
    queues = [by_story[sid] for sid in dict.fromkeys(e["metadata"]["story_id"] for e in examples)]
    picked, seen = [], set()
    while len(picked) < n and any(queues):
        for q in queues:
            while q:
                ex = q.pop(0)
                key = ex["metadata"]["original_span"] or ex["text"]
                if key not in seen:
                    seen.add(key)
                    picked.append(ex)
                    break
            if len(picked) == n:
                break
    return picked


def dedup_key(t):
    """Normalize a scene-description string for de-duplication purposes only
    (collapse whitespace differences); the original, readable spacing is kept
    separately for display)."""
    return re.sub(r"\s+", " ", t).strip("。.;； ").lower()


def build_scene_checklists(corpus):
    """Derive a canonical 'required plot beats' checklist per story from the
    union of every 'Miss scene' annotation the teacher wrote for that story.
    (1) expert documents: the raw/ folder;
    (2) build pipeline: chunk_builder.py and embed-to-mongo.mjs;
    (3) reference library: the rag_chunks collection;
    (4) request assembler: assembleFeedbackPrompt.ts;
    (5) LLM: gpt-5.6-terra;
    (6) feedback log: the stored feedback and feedbackChunkIds. If you release code, Appendix C could list this mapping.
    """
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


def load_rule_card_triggers():
    """{rule name: [regex, ...]} from rule_card_triggers.json; {} if the file is absent."""
    if not os.path.exists(RULE_CARD_TRIGGERS_PATH):
        return {}
    rules = json.load(open(RULE_CARD_TRIGGERS_PATH, encoding="utf-8"))["rules"]
    out = {}
    for tag, trigs in rules.items():
        if tag not in GRAMMAR_RULE_DESC:
            sys.exit(f"{RULE_CARD_TRIGGERS_PATH}: {tag} is not a rule in rule_descriptions.py")
        out[tag] = [t["regex"] for t in trigs]
        for t in out[tag]:
            re.compile(t)  # fail loudly on a malformed trigger
    return out


def make_chunk(chunk_id, chunk_type, text, **meta):
    return {"chunk_id": chunk_id, "chunk_type": chunk_type, "text": text, "metadata": meta}


def build_chunks(corpus, rule_labels, aligned=None):
    """aligned: her exact edits by (sample_id, correction line) -- load_aligned_edits()."""
    chunks = []
    unlabelled = []
    aligned = load_aligned_edits() if aligned is None else aligned
    texts = {s["sample_id"]: s["raw_text"] for s in corpus["samples"]}

    model_by_story = {m["story_id"]: m for m in corpus["model_stories"]}
    missed_scenes = build_scene_checklists(corpus)

    # ---- model_story chunks -------------------------------------------------
    for m in corpus["model_stories"]:
        chunks.append(make_chunk(
            f"model_story:{m['story_id']}", "model_story", m["text"],
            story_id=m["story_id"], title=m["title"], doc_type="model",
            source_doc="model_stories",
        ))

    # ---- per-sample chunk tree ----------------------------------------------
    story_stats = defaultdict(lambda: {"n_samples": 0, "grammar_tags": Counter()})

    for s in corpus["samples"]:
        sid = s["sample_id"]
        story_stats[s["story_id"]]["n_samples"] += 1

        chunks.append(make_chunk(
            f"sample:{sid}", "sample", s["raw_text"],
            source_doc=s["source_doc"], doc_type=s["doc_type"], story_id=s["story_id"],
            sample_id=sid, n_teacher_items=len(s["teacher_correction_items"]),
            n_content_flags=len(s["content_flags"]),
        ))

        for idx, raw in enumerate(s["teacher_correction_items"]):
            split = split_correction(raw)
            if raw in rule_labels:
                gtags, tag_source = rule_labels[raw], "label"
            else:
                gtags, tag_source = tag_grammar_text(raw), "regex_fallback"
                unlabelled.append({"sample_id": sid, "text": raw, "regex_tags": gtags})
            story_stats[s["story_id"]]["grammar_tags"].update(gtags)
            exact = {}
            edits = aligned.get((sid, raw), [])
            if edits:
                before, after = before_after(s["raw_text"], edits)
                exact = {"edits": [{k: e[k] for k in ("op", "start", "end", "original", "corrected")} for e in edits],
                         "clause_before": before, "clause_after": after}
            chunks.append(make_chunk(
                f"correction_item:{sid}::c{idx}", "correction_item", raw,
                source_doc=s["source_doc"], doc_type=s["doc_type"], story_id=s["story_id"],
                sample_id=sid, parent_id=f"sample:{sid}",
                original_span=split["original_span"], corrected_span=split["corrected_span"],
                explanation=split["explanation"], grammar_tags=gtags, tag_source=tag_source,
                **exact,
            ))

        for idx, raw in enumerate(s["content_flags"]):
            rec = parse_content_flag(raw)
            chunks.append(make_chunk(
                f"content_flag:{sid}::f{idx}", "content_flag", raw,
                source_doc=s["source_doc"], doc_type=s["doc_type"], story_id=s["story_id"],
                sample_id=sid, parent_id=f"sample:{sid}", **{k: v for k, v in rec.items() if k != "raw_text"},
            ))

    # ---- story_prompt anchor chunks -----------------------------------------
    empty_stats = {"n_samples": 0, "grammar_tags": Counter()}
    for story_id in sorted(set(story_stats) | set(model_by_story)):
        stats = story_stats.get(story_id, empty_stats)
        model = model_by_story.get(story_id)
        missed = missed_scenes.get(story_id, [])
        lines = [f"Story prompt: {story_id}"]
        if model:
            lines.append(f"Model exemplar title: {model['title']}")
        lines.append(f"Reviewed student samples: {stats['n_samples']}")
        if missed:
            lines.append("Scenes students most often left out (from the teacher's 'Miss scene' notes):")
            for c in missed:
                lines.append(f"  - {c['scene_description']} "
                             f"(missing in {c['times_flagged_missing']}/{stats['n_samples']} samples)")
        if stats["grammar_tags"]:
            top = ", ".join(f"{t}×{n}" for t, n in stats["grammar_tags"].most_common(10))
            lines.append(f"Most common grammar issues in this batch: {top}")
        chunks.append(make_chunk(
            f"story_prompt:{story_id}", "story_prompt", "\n".join(lines),
            story_id=story_id, doc_type="story_prompt",
            has_model_story=bool(model), n_samples=stats["n_samples"],
            n_missed_scene_items=len(missed),
        ))

    # ---- rule_card chunks (aggregate grammar tags across whole corpus) -----
    card_triggers = load_rule_card_triggers()
    grammar_examples = defaultdict(list)
    for ch in chunks:
        if ch["chunk_type"] == "correction_item":
            for tag in ch["metadata"]["grammar_tags"]:
                grammar_examples[tag].append(ch)

    for tag, examples in grammar_examples.items():
        if tag in NO_RULE_CARD:
            continue
        desc = GRAMMAR_RULE_DESC.get(tag, "")
        picked = pick_examples(tag, examples, MAX_RULE_CARD_EXAMPLES)
        lines = [f"Grammar/linguistic point: {tag}", desc, "Examples (original -> corrected, why):"]
        story_ids = set()
        for ex in picked:
            md = ex["metadata"]
            story_ids.add(md["story_id"])
            if md.get("clause_before"):  # her exact edits: the student's whole clause, before and after
                orig, corr = md["clause_before"], md["clause_after"]
            else:
                orig = md.get("original_span") or "(see raw)"
                corr = md.get("corrected_span") or ""
            expl = md.get("explanation") or ""
            lines.append(f"  - {orig} -> {corr}" + (f"  [{expl}]" if expl else ""))
        text = "\n".join(lines)
        # her standard fix: from corrections labelled with this rule only (edit -> rule is unambiguous)
        single = [(e, texts[ex["metadata"]["sample_id"]]) for ex in examples if ex["metadata"]["grammar_tags"] == [tag]
                  for e in aligned.get((ex["metadata"]["sample_id"], ex["text"]), [])]
        chunks.append(make_chunk(
            f"rule_card:{tag}", "rule_card", text,
            grammar_tag=tag, description=desc, n_examples_total=len(examples),
            example_sample_ids=[e["metadata"]["sample_id"] for e in picked],
            story_ids=sorted(story_ids),
            **({"standard_fix": fix} if (fix := standard_fix(single)) else {}),
            **({"triggers": card_triggers[tag]} if tag in card_triggers else {}),
        ))

    # ---- rule_example chunks (index rule cards by the student sentences she corrected) --
    cards = {ch["metadata"]["grammar_tag"] for ch in chunks if ch["chunk_type"] == "rule_card"}
    for ch in [c for c in chunks if c["chunk_type"] == "correction_item"]:
        md = ch["metadata"]
        if not md.get("clause_before"):
            continue
        for tag in md["grammar_tags"]:
            if tag in cards:
                chunks.append(make_chunk(
                    f"rule_example:{ch['chunk_id'].split(':', 1)[1]}::{tag}", "rule_example", md["clause_before"],
                    parent_id=f"rule_card:{tag}", grammar_tag=tag, story_id=md["story_id"],
                    sample_id=md["sample_id"], correction_id=ch["chunk_id"], clause_after=md["clause_after"],
                ))

    return chunks, unlabelled


def main():
    corpus = json.load(open(CORPUS_PATH, encoding="utf-8"))
    chunks, unlabelled = build_chunks(corpus, load_rule_labels())

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        for ch in chunks:
            f.write(json.dumps(ch, ensure_ascii=False) + "\n")

    by_type = Counter(ch["chunk_type"] for ch in chunks)
    print(f"Wrote {OUT_PATH}: {len(chunks)} basic chunks")
    for t, n in by_type.most_common():
        print(f"  {t:20s} {n}")

    n_items = by_type["correction_item"]
    if unlabelled:
        with open(UNLABELLED_PATH, "w", encoding="utf-8") as f:
            json.dump(unlabelled, f, ensure_ascii=False, indent=1)
        print(f"\n{len(unlabelled)}/{n_items} corrections have no rule label in {RULE_LABELS_PATH} "
              f"(regex tags used instead) -> listed in {UNLABELLED_PATH}")
    else:
        if os.path.exists(UNLABELLED_PATH):
            os.remove(UNLABELLED_PATH)
        print(f"\nAll {n_items} corrections have rule labels.")


if __name__ == "__main__":
    main()
