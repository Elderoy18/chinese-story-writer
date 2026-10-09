#!/usr/bin/env python3
"""
Parse the paragraph-JSON files written by extract_json.py into one structured
extracted/corpus.json. No file names are hard-coded: every document is
recognized by its own headers.

Basic data (extracted/basic/*.json):
  - model stories doc : "Story N: <title>" followed by the story text.
  - samples doc       : "Student N" followed by the student's story, then
                        "Teacher feedback:" and one correction per paragraph,
                        then content flags ("Miss ...", "Wrong information ...",
                        "Coherence problem ..."). Which story the doc belongs to
                        comes from its file name (the "match" words in
                        raw/stories.json).

Iteration data (extracted/iteration/*.json), only docs containing "AI feedback":
  - AI review doc     : the same "Student N" layout, plus "AI feedback:" with
                        错别字 / Grammar Corrections / Vocabulary Suggestions items,
                        each optionally followed by the teacher's "My comment".
                        The AI items are attached to the matching basic-data
                        sample (same story, same student number); its teacher
                        feedback is NOT re-read -- the basic doc is the source
                        for that.

Every story must be registered in raw/stories.json; an unknown title or file
name stops the run with a message saying what to add.

Doc types in the output:
  "model"        : model stories (no feedback)
  "teacher_only" : a student sample with teacher feedback
  "ai_reviewed"  : a teacher_only sample that also has AI feedback + My comments
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

REGISTRY_PATH = "raw/stories.json"
BASIC_DIR = Path("extracted/basic")
ITERATION_DIR = Path("extracted/iteration")
OUT_PATH = "extracted/corpus.json"

MODEL_HEADER = re.compile(r"^Story\s*#?\s*(\d+)\s*[:：]\s*(.+)$", re.I)
STUDENT_HEADER = re.compile(r"^Student\s*#?\s*(\d+)\s*[:：]?\s*(.*)$", re.I)
TEACHER_MARKER = re.compile(r"^Teacher feedback\s*[:：]?$", re.I)
AI_MARKER = re.compile(r"^AI feedback\s*[:：]?$", re.I)
GRAMMAR_HEADER = re.compile(r"^Grammar Corrections?\s*[:：]?$", re.I)
VOCAB_HEADER = re.compile(r"^Vocabulary Suggestions?\s*[:：]?$", re.I)
FLAG_PREFIXES = ("Miss", "Wrong information", "Coherence problem")
CLOSING_NOTE = "Try to include more details and descriptions"


class FormatError(Exception):
    pass


def load_registry():
    stories = json.load(open(REGISTRY_PATH, encoding="utf-8"))["stories"]
    ids = [s["story_id"] for s in stories]
    dupes = [i for i, n in Counter(ids).items() if n > 1]
    if dupes:
        raise FormatError(f"{REGISTRY_PATH}: duplicate story_id {dupes}")
    return stories


def story_by_title(registry, title, where):
    for s in registry:
        if s["title"] == title:
            return s
    raise FormatError(
        f'{where}: story "{title}" has no corpus ID. Add an entry to {REGISTRY_PATH}, e.g.\n'
        f'  {{"story_id": "<pinyin_id>", "title": "{title}", "match": ["<word in its samples file name>"]}}'
    )


def story_by_filename(registry, stem, where):
    hits = [s for s in registry if any(m in stem for m in s["match"])]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise FormatError(
            f'{where}: no story in {REGISTRY_PATH} matches the file name "{stem}". '
            f'Add the story (or a word from this file name to its "match" list).'
        )
    raise FormatError(
        f'{where}: file name "{stem}" matches several stories '
        f'({", ".join(s["story_id"] for s in hits)}); make the "match" words more specific.'
    )


def split_blocks(paras, header, where):
    """[(header_match, [body paragraphs...]), ...]; text before the first header
    is an error, so a typo in a header can't silently merge two samples."""
    blocks = []
    for p in paras:
        m = header.match(p)
        if m:
            blocks.append((m, []))
        elif blocks:
            blocks[-1][1].append(p)
        else:
            raise FormatError(f'{where}: text before the first header: "{p[:60]}"')
    nums = Counter(m.group(1) for m, _ in blocks)
    dupes = [n for n, c in nums.items() if c > 1]
    if dupes:
        raise FormatError(f"{where}: header number(s) used twice: {dupes}")
    return blocks


def take_until(body, marker):
    """Split body at the first paragraph matching marker -> (before, after) or None."""
    for i, p in enumerate(body):
        if marker.match(p):
            return body[:i], body[i + 1:]
    return None


# ---------------------------------------------------------------------------
# Basic data
# ---------------------------------------------------------------------------
def parse_model_doc(paras, registry, where):
    out = []
    for m, body in split_blocks(paras, MODEL_HEADER, where):
        title = m.group(2).strip()
        story = story_by_title(registry, title, where)
        if not body:
            raise FormatError(f'{where}: "Story {m.group(1)}: {title}" has no story text')
        out.append({"story_id": story["story_id"], "title": title, "text": "\n".join(body)})
    return out


def sample_id(story, num):
    return f"{story.get('sample_id_prefix', story['story_id'])}#{num}"


def parse_samples_doc(paras, story, source_doc, where):
    samples = []
    for m, body in split_blocks(paras, STUDENT_HEADER, where):
        num = m.group(1)
        glued = [m.group(2)] if m.group(2) else []
        split = take_until(body, TEACHER_MARKER)
        if split is None:
            raise FormatError(f'{where}: Student {num} has no "Teacher feedback:" line')
        story_paras, feedback = split
        story_text = "\n".join(glued + story_paras)
        if not story_text:
            raise FormatError(f"{where}: Student {num} has no story text")

        items, flags, closing_note = [], [], None
        for p in feedback:
            if p == CLOSING_NOTE:
                closing_note = p
            elif p.startswith(FLAG_PREFIXES):
                flags.append(p)
            else:
                items.append(p)

        samples.append({
            "sample_id": sample_id(story, num),
            "source_doc": source_doc,
            "doc_type": "teacher_only",
            "story_id": story["story_id"],
            "sample_num": num,
            "raw_text": story_text,
            "teacher_correction_items": items,
            "content_flags": flags,
            "ai_feedback_items": [],
            "closing_note": closing_note,
        })
    return samples


# ---------------------------------------------------------------------------
# Iteration data: AI review overlay
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


def apply_ai_review_doc(paras, story, source_doc, samples_by_id, where):
    n_items = 0
    for m, body in split_blocks(paras, STUDENT_HEADER, where):
        num = m.group(1)
        sample = samples_by_id.get(sample_id(story, num))
        if sample is None:
            raise FormatError(
                f"{where}: Student {num} has AI feedback but no matching sample in the "
                f"basic data for {story['story_id']}"
            )
        split = take_until(body, AI_MARKER)
        if split is None:
            continue  # this student was not AI-reviewed
        before_ai, ai_body = split
        before_teacher = take_until(before_ai, TEACHER_MARKER)
        story_text = "\n".join(([m.group(2)] if m.group(2) else []) +
                               (before_teacher[0] if before_teacher else before_ai))
        if story_text != sample["raw_text"]:
            print(f"  WARNING {where}: Student {num}'s story text differs from the basic data copy")
        items = parse_ai_items(ai_body, f"{where} Student {num}")
        sample["ai_feedback_items"].extend(items)
        sample["doc_type"] = "ai_reviewed"
        sample["ai_review_doc"] = source_doc
        n_items += len(items)
    return n_items


# ---------------------------------------------------------------------------
def load_paras(path):
    return json.load(open(path, encoding="utf-8"))


def main():
    registry = load_registry()
    corpus = {"model_stories": [], "samples": []}

    basic = sorted(BASIC_DIR.glob("*.json"))
    if not basic:
        sys.exit(f"No files in {BASIC_DIR} -- run extract_json.py first")
    for path in basic:
        paras, where = load_paras(path), str(path)
        if any(STUDENT_HEADER.match(p) for p in paras):
            story = story_by_filename(registry, path.stem, where)
            samples = parse_samples_doc(paras, story, path.stem, where)
            corpus["samples"].extend(samples)
            print(f"{path.stem}: {len(samples)} samples -> {story['story_id']}")
        elif any(MODEL_HEADER.match(p) for p in paras):
            models = parse_model_doc(paras, registry, where)
            corpus["model_stories"].extend(models)
            print(f"{path.stem}: {len(models)} model stories")
        else:
            raise FormatError(f'{where}: no "Student N" or "Story N: <title>" headers found')

    dupes = [i for i, n in Counter(s["sample_id"] for s in corpus["samples"]).items() if n > 1]
    if dupes:
        raise FormatError(f"two samples docs share a story and student numbers: {dupes[:5]}")
    dupes = [i for i, n in Counter(m["story_id"] for m in corpus["model_stories"]).items() if n > 1]
    if dupes:
        raise FormatError(f"more than one model story for {dupes}")

    # Registry order, not file-name order: rule_card / ai_error_card show the
    # first N examples in corpus order, so this decides which examples they get.
    rank = {s["story_id"]: i for i, s in enumerate(registry)}
    corpus["samples"].sort(key=lambda s: rank[s["story_id"]])  # stable within a doc

    samples_by_id = {s["sample_id"]: s for s in corpus["samples"]}
    for path in sorted(ITERATION_DIR.glob("*.json")):
        paras = load_paras(path)
        if not any(AI_MARKER.match(p) for p in paras):
            continue  # vocab list, scene list, rules: not handled here
        story = story_by_filename(registry, path.stem, str(path))
        n = apply_ai_review_doc(paras, story, path.stem, samples_by_id, str(path))
        print(f"{path.stem}: {n} AI feedback items -> {story['story_id']}")

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=1)

    # ---- sanity report ----
    samples = corpus["samples"]
    n_ai = sum(len(s["ai_feedback_items"]) for s in samples)
    n_comment = sum(1 for s in samples for it in s["ai_feedback_items"] if it["my_comment"])
    print(f"\nWrote {OUT_PATH}")
    print("Model stories:", len(corpus["model_stories"]))
    print("Samples by story:", dict(Counter(s["story_id"] for s in samples)))
    print("Teacher correction items:", sum(len(s["teacher_correction_items"]) for s in samples))
    print("Content-coverage flags:", sum(len(s["content_flags"]) for s in samples))
    print(f"AI feedback items: {n_ai} ({n_comment} with a teacher 'My comment')")


if __name__ == "__main__":
    try:
        main()
    except FormatError as e:
        sys.exit(f"FORMAT ERROR: {e}")
