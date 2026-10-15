#!/usr/bin/env python3
"""
Parse the basic-data paragraph-JSON files written by extract_json.py into one
structured extracted/basic_corpus.json. Reads ONLY extracted/basic/ (from
raw/basic data/): graded student samples and model stories, before any AI
round. Human-in-the-loop data (AI critiques, rule lists) is handled separately
by build_iteration_chunks.py.

No file names are hard-coded: every document is recognized by its own headers.
  - model stories doc : "Story N: <title>" followed by the story text.
  - samples doc       : "Student N" followed by the student's story, then
                        "Teacher feedback:" and one correction per paragraph,
                        then content flags ("Miss ...", "Wrong information ...",
                        "Coherence problem ..."). Which story the doc belongs to
                        comes from its file name (the "match" words in
                        raw/stories.json).

Every story must be registered in raw/stories.json; an unknown title or file
name stops the run with a message saying what to add.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

REGISTRY_PATH = "raw/stories.json"
BASIC_DIR = Path("extracted/basic")
OUT_PATH = "extracted/basic_corpus.json"

MODEL_HEADER = re.compile(r"^Story\s*#?\s*(\d+)\s*[:：]\s*(.+)$", re.I)
STUDENT_HEADER = re.compile(r"^Student\s*#?\s*(\d+)\s*[:：]?\s*(.*)$", re.I)
TEACHER_MARKER = re.compile(r"^Teacher feedback\s*[:：]?$", re.I)
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


def sample_id(story, num):
    return f"{story.get('sample_id_prefix', story['story_id'])}#{num}"


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


def parse_model_doc(paras, registry, where):
    out = []
    for m, body in split_blocks(paras, MODEL_HEADER, where):
        title = m.group(2).strip()
        story = story_by_title(registry, title, where)
        if not body:
            raise FormatError(f'{where}: "Story {m.group(1)}: {title}" has no story text')
        out.append({"story_id": story["story_id"], "title": title, "text": "\n".join(body)})
    return out


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
            "closing_note": closing_note,
        })
    return samples


def main():
    registry = load_registry()
    corpus = {"model_stories": [], "samples": []}

    basic = sorted(BASIC_DIR.glob("*.json"))
    if not basic:
        sys.exit(f"No files in {BASIC_DIR} -- run extract_json.py first")
    for path in basic:
        paras, where = json.load(open(path, encoding="utf-8")), str(path)
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

    # Registry order, not file-name order: rule_cards show the first N examples
    # in corpus order, so this decides which examples they get.
    rank = {s["story_id"]: i for i, s in enumerate(registry)}
    corpus["samples"].sort(key=lambda s: rank[s["story_id"]])  # stable within a doc

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=1)

    samples = corpus["samples"]
    print(f"\nWrote {OUT_PATH}")
    print("Model stories:", len(corpus["model_stories"]))
    print("Samples by story:", dict(Counter(s["story_id"] for s in samples)))
    print("Teacher correction items:", sum(len(s["teacher_correction_items"]) for s in samples))
    print("Content-coverage flags:", sum(len(s["content_flags"]) for s in samples))


if __name__ == "__main__":
    try:
        main()
    except FormatError as e:
        sys.exit(f"FORMAT ERROR: {e}")
