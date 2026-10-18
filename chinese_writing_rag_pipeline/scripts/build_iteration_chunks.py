#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the human-in-the-loop chunks -> chunks/iteration_chunks.jsonl, kept
apart from the basic-data build (chunk_builder.py). Everything here comes from
the supervising teacher reviewing the system, in raw/iteration data/:

  1. Critiques of AI feedback -- the docs listed in CRITIQUE_DOCS, each with
     "Student N" / "AI feedback:" and the teacher's "My comment" after each AI item:
       ai_feedback_item -- one AI item + the teacher's critique of it
       ai_error_card    -- all critiques sharing a failure-mode tag, aggregated
                           (the app pins these into every feedback prompt)
  2. Rules added by the teacher:
       vocab_error      -- one entry of the word-choice error list (vocab_errors.json)
       teacher_rule     -- one of the teacher's additional rules (extra_rules.json)
       vocab_suggestion_example -- one of the teacher's examples of a good vocabulary
                           suggestion (vocab_suggestion_examples.txt)
       scene_list       -- one per story: the required scenes in story order
                           (story_scenes.md), used for end-of-story content feedback
  3. Prompt updates live in lib/rag/assembleFeedbackPrompt.ts, not here.

vocab_errors.json and story_scenes.md are hand-converted from the teacher's
docx in the same folder. Every source file is required: a missing one stops the
build with an error (it used to be skipped silently, which would have dropped
its chunks from the live database on the next --embed --prune). This script reads basic_corpus.json only to link AI
critiques to their graded sample and to count missed scenes; it never changes
the basic corpus.
"""
import json
import re
import sys
from collections import defaultdict, Counter
from pathlib import Path

sys.path.insert(0, "scripts")
from tagging import tag_grammar_text, tag_ai_eval_text
from rule_descriptions import AI_EVAL_DESC
from extract_json import extract
from parse_corpus import (FormatError, load_registry, story_by_filename, sample_id,
                          split_blocks, take_until, STUDENT_HEADER)
from chunk_builder import make_chunk, dedup_key, build_scene_checklists

ITERATION_DIR = Path("raw/iteration data")
CORPUS_PATH = "extracted/basic_corpus.json"
VOCAB_PATH = ITERATION_DIR / "vocab_errors.json"
SUGGESTION_EXAMPLES_PATH = ITERATION_DIR / "vocab_suggestion_examples.txt"
EXTRA_RULES_PATH = ITERATION_DIR / "extra_rules.json"
SCENES_PATH = ITERATION_DIR / "story_scenes.md"
OUT_PATH = "chunks/iteration_chunks.jsonl"
CHECKLISTS_PATH = "chunks/scene_checklists.json"
CRITIQUE_LABELS_PATH = ITERATION_DIR / "critique_labels.json"
# AI-critique docs to read, listed by name: other docs in the folder can also
# contain "AI feedback" headings (e.g. her comments on the critique tags) and
# are not student-sample critiques. Add a new critique doc here.
CRITIQUE_DOCS = ["Pear Story with AI and Teacher feedback.docx"]
MAX_AI_ERROR_CARD_EXAMPLES = 6

AI_MARKER = re.compile(r"^AI feedback\s*[:：]?$", re.I)
GRAMMAR_HEADER = re.compile(r"^Grammar Corrections?\s*[:：]?$", re.I)
VOCAB_HEADER = re.compile(r"^Vocabulary Suggestions?\s*[:：]?$", re.I)


# ---------------------------------------------------------------------------
# 1. Critiques of AI feedback
# ---------------------------------------------------------------------------
def parse_ai_items(body, where):
    """Items after "AI feedback:". Section headers set the category; the
    错别字 line is a header and its own item; "My comment" attaches to the
    item before it."""
    items, category = [], None
    for p in body:
        if GRAMMAR_HEADER.match(p):
            category = "grammar"
        elif VOCAB_HEADER.match(p):
            category = "vocabulary"
        elif p.startswith("My comment"):
            if not items or items[-1]["my_comment"] is not None:
                raise FormatError(f'{where}: "My comment" with no AI item before it: "{p[:60]}"')
            items[-1]["my_comment"] = p
        elif p.startswith("错别字"):
            items.append({"category": "wrong_characters", "raw_text": p, "my_comment": None})
        else:
            if category is None:
                raise FormatError(f'{where}: AI item before any section header: "{p[:60]}"')
            items.append({"category": category, "raw_text": p, "my_comment": None})
    return items


def require(path):
    """Stop the build if a source file is missing (never skip it silently)."""
    if not Path(path).exists():
        raise FormatError(f"{path}: source file missing -- restore it (git history, or the snapshot "
                          f"it was built into) before rebuilding")
    return path


def load_critique_labels():
    """Failure-mode labels per critiqued AI item, keyed by the chunk text."""
    require(CRITIQUE_LABELS_PATH)
    labels = json.load(open(CRITIQUE_LABELS_PATH, encoding="utf-8"))["labels"]
    unknown = sorted({t for tags in labels.values() for t in tags} - set(AI_EVAL_DESC))
    if unknown:
        raise FormatError(f"{CRITIQUE_LABELS_PATH}: labels with no description in rule_descriptions.py: {unknown}")
    return labels


def build_ai_critique_chunks(registry, samples_by_id):
    """ai_feedback_item chunks from every AI-critique doc, each linked to the
    graded basic-data sample it reviews (same story, same student number).
    The doc's own copy of the teacher feedback is not re-read."""
    chunks = []
    labels = load_critique_labels()
    for name in CRITIQUE_DOCS:
        path = require(ITERATION_DIR / name)
        paras = extract(path)
        where = str(path)
        if not any(AI_MARKER.match(p) for p in paras):
            raise FormatError(f'{where}: listed in CRITIQUE_DOCS but has no "AI feedback:" heading')
        story = story_by_filename(registry, path.stem, where)
        n = 0
        for m, body in split_blocks(paras, STUDENT_HEADER, where):
            num = m.group(1)
            sid = sample_id(story, num)
            sample = samples_by_id.get(sid)
            if sample is None:
                raise FormatError(f"{where}: Student {num} has no graded sample {sid} in the basic data")
            split = take_until(body, AI_MARKER)
            if split is None:
                continue  # this student was not AI-reviewed
            for idx, item in enumerate(parse_ai_items(split[1], f"{where} Student {num}")):
                comment = item["my_comment"] or ""
                text = item["raw_text"] + ("\n" + comment if comment else "")
                if text in labels:
                    eval_tags, tag_source = labels[text], "label"
                else:
                    eval_tags, tag_source = (tag_ai_eval_text(comment) if comment else []), "regex_fallback"
                chunks.append(make_chunk(
                    f"ai_feedback_item:{sid}::a{idx}", "ai_feedback_item", text,
                    source_doc=path.stem, doc_type="ai_critique", story_id=story["story_id"],
                    sample_id=sid, parent_id=f"sample:{sid}",
                    ai_category=item["category"], ai_raw_text=item["raw_text"],
                    teacher_comment=comment,
                    eval_tags=eval_tags, tag_source=tag_source,
                    grammar_tags=tag_grammar_text(item["raw_text"]),
                ))
                n += 1
        print(f"{path.name}: {n} critiqued AI items -> {story['story_id']}")
    return chunks


def build_ai_error_cards(ai_items):
    """One card per failure mode. Examples are picked so that as many different
    critiques as possible appear somewhere: cards are filled smallest first, and
    each prefers critiques no other card has shown yet (then document order)."""
    examples = defaultdict(list)
    for ch in ai_items:
        for tag in ch["metadata"]["eval_tags"]:
            examples[tag].append(ch)
    shown, picks = set(), {}
    for tag in sorted(examples, key=lambda t: (len(examples[t]), t)):
        ranked = sorted(examples[tag], key=lambda e: e["chunk_id"] in shown)  # stable: unshown first
        picks[tag] = ranked[:MAX_AI_ERROR_CARD_EXAMPLES]
        shown.update(e["chunk_id"] for e in picks[tag])
    cards = []
    for tag, exs in examples.items():
        desc = AI_EVAL_DESC.get(tag, "")
        picked = sorted(picks[tag], key=lambda e: exs.index(e))  # keep document order on the card
        lines = [f"AI-feedback calibration pattern: {tag}", desc, "Examples (AI said / teacher's verdict):"]
        for ex in picked:
            md = ex["metadata"]
            lines.append(f"  - AI: {md['ai_raw_text']}")
            lines.append(f"    Teacher: {md['teacher_comment']}")
        cards.append(make_chunk(
            f"ai_error_card:{tag}", "ai_error_card", "\n".join(lines),
            eval_tag=tag, description=desc, n_examples_total=len(exs),
            example_sample_ids=[e["metadata"]["sample_id"] for e in picked],
            example_chunk_ids=[e["chunk_id"] for e in picked],
        ))
    return cards


# ---------------------------------------------------------------------------
# 2. Rules added by the teacher
# ---------------------------------------------------------------------------
def build_vocab_chunks(registry):
    """One chunk per entry. `triggers` are regexes the app matches against the
    student's text (lexical retrieval); the chunk text is embedded for
    semantic retrieval."""
    vocab = json.load(open(require(VOCAB_PATH), encoding="utf-8"))
    titles = {s["story_id"]: s["title"] for s in registry}
    chunks = []
    for e in vocab["entries"]:
        from_titles = " / ".join(titles.get(s, s) for s in e["story_ids"])
        text = f"Vocabulary error (用错的词, from the teacher's list; collected from {from_titles}): *{e['wrong']} -> {e['correct']}"
        if e["note"]:
            text += f" -- {e['note']}"
        chunks.append(make_chunk(
            f"vocab_error:{e['id']}", "vocab_error", text,
            story_ids=e["story_ids"], wrong=e["wrong"], correct=e["correct"],
            note=e["note"], triggers=e["triggers"],
            source="vocabulary_list_errors_correct.md",
        ))
    return chunks


def build_teacher_rule_chunks():
    """One chunk per rule in extra_rules.json (the teacher's additional rules).
    `triggers` mark where a student's text may break the rule -- candidates for
    the model to check, not errors by themselves."""
    require(EXTRA_RULES_PATH)
    chunks = []
    for r in json.load(open(EXTRA_RULES_PATH, encoding="utf-8"))["rules"]:
        for t in r["triggers"]:
            re.compile(t)  # fail loudly on a malformed trigger
        chunks.append(make_chunk(
            f"teacher_rule:{r['id']}", "teacher_rule", r["rule"],
            triggers=r["triggers"], source=r["source"],
        ))
    return chunks


SUGGESTION_EXAMPLE = re.compile(r"^(\S+) -- “([^”]+)”：(.+)$")


def build_vocab_suggestion_chunks():
    """One chunk per line of the teacher's list of good vocabulary suggestions:
    <student's word> -- “<phrase>”：<alternative>，<why>；<alternative>，<why>"""
    require(SUGGESTION_EXAMPLES_PATH)
    chunks = []
    lines = [l.strip() for l in SUGGESTION_EXAMPLES_PATH.read_text(encoding="utf-8").splitlines()]
    for n, line in enumerate((l for l in lines if l and not l.startswith("#")), 1):
        m = SUGGESTION_EXAMPLE.match(line)
        if not m:
            raise FormatError(f'{SUGGESTION_EXAMPLES_PATH}: line not in "<word> -- “<phrase>”：..." form: "{line[:60]}"')
        chunks.append(make_chunk(
            f"vocab_suggestion_example:{n}", "vocab_suggestion_example", line,
            word=m.group(1), phrase=m.group(2), source="vocab_suggestion_examples.txt",
        ))
    return chunks


NUMBER_WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen "
    "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}


def parse_story_scenes(registry):
    """Read the teacher's required-scene list (story_scenes.md):

        **Story 1: <title>**
        Seven scenes: <scene>; <scene>；<scene> ...

    Returns {story_id: [scene, ...]} in story order. The stated scene count is
    checked against the split so a stray or missing separator fails loudly."""
    text = require(SCENES_PATH).read_text(encoding="utf-8")
    title_to_id = {s["title"]: s["story_id"] for s in registry}
    scenes_by_story = {}
    for m in re.finditer(r"\*\*Story \d+:\s*(.+?)\*\*\s*\n+\s*(\w+) scenes:\s*(.+)", text):
        title, count_word, body = m.group(1).strip(), m.group(2).lower(), m.group(3)
        if title not in title_to_id:
            raise FormatError(f'{SCENES_PATH}: story "{title}" is not in raw/stories.json')
        scenes = [sc.strip() for sc in re.split(r"[;；]", body) if sc.strip()]
        if len(scenes) != NUMBER_WORDS[count_word]:
            raise FormatError(f"{SCENES_PATH}: {title} says {count_word} scenes, parsed {len(scenes)}")
        scenes_by_story[title_to_id[title]] = scenes
    return scenes_by_story


def build_scene_list_chunks(registry, corpus):
    """scene_list:<story_id> -- the teacher's required scenes in story order.
    Each scene's metadata also records how often the teacher flagged that exact
    beat as missing in the graded samples (None if no annotation matches it
    word for word) -- for analysis, not shown to the feedback model."""
    titles = {s["story_id"]: s["title"] for s in registry}
    derived = build_scene_checklists(corpus)
    chunks, checklists = [], {}
    for story_id, scenes in parse_story_scenes(registry).items():
        counts = {dedup_key(c["scene_description"]): c["times_flagged_missing"]
                  for c in derived.get(story_id, [])}
        checklist = [
            {"scene_number": i, "scene_description": sc,
             "times_flagged_missing": counts.get(dedup_key(sc))}
            for i, sc in enumerate(scenes, 1)
        ]
        checklists[story_id] = checklist
        lines = [f"Required scenes for {titles[story_id]}, in story order "
                 f"({len(scenes)}, from the teacher's scene list):"]
        lines += [f"  {c['scene_number']}. {c['scene_description']}" for c in checklist]
        chunks.append(make_chunk(
            f"scene_list:{story_id}", "scene_list", "\n".join(lines),
            story_id=story_id, n_scenes=len(scenes), source="story_scenes.md",
        ))
    return chunks, checklists


# ---------------------------------------------------------------------------
def main():
    registry = load_registry()
    corpus = json.load(open(CORPUS_PATH, encoding="utf-8"))
    samples_by_id = {s["sample_id"]: s for s in corpus["samples"]}

    ai_items = build_ai_critique_chunks(registry, samples_by_id)
    chunks = (ai_items + build_ai_error_cards(ai_items) + build_vocab_chunks(registry)
              + build_vocab_suggestion_chunks() + build_teacher_rule_chunks())
    scene_chunks, checklists = build_scene_list_chunks(registry, corpus)
    chunks += scene_chunks

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        for ch in chunks:
            f.write(json.dumps(ch, ensure_ascii=False) + "\n")
    with open(CHECKLISTS_PATH, "w", encoding="utf-8") as f:
        json.dump(checklists, f, ensure_ascii=False, indent=1)

    n_comment = sum(1 for c in ai_items if c["metadata"]["teacher_comment"])
    print(f"Wrote {OUT_PATH}: {len(chunks)} human-in-the-loop chunks "
          f"({n_comment}/{len(ai_items)} AI items with a teacher comment)")
    for t, n in Counter(ch["chunk_type"] for ch in chunks).most_common():
        print(f"  {t:20s} {n}")


if __name__ == "__main__":
    try:
        main()
    except FormatError as e:
        sys.exit(f"FORMAT ERROR: {e}")
