#!/usr/bin/env python3
"""
Parse the 5 extracted paragraph-JSON files into a unified, structured corpus.json.

Doc types produced:
  - "model"        : the 4 near-perfect model stories (no feedback)
  - "teacher_only" : mengmu / shennong batches -- story + teacher correction items
                      + content-coverage flags (Miss scene / Wrong information / Coherence)
  - "ai_reviewed"  : the two docs where a student story received both "Teacher feedback"
                      (gold) and "AI feedback" (machine), with the teacher's own
                      "My comment" critique of each AI feedback item.
"""
import json
import re

def norm_marker(s):
    return s.strip().rstrip(':：').strip()

def is_sample_number_alone(p):
    return re.fullmatch(r'\d+', p) is not None

def is_sample_number_glued(p):
    m = re.match(r'^(\d+)([一-鿿].*)$', p)
    return m

# ---------------------------------------------------------------------------
# Model stories
# ---------------------------------------------------------------------------
STORY_TITLE_TO_ID = {
    "神农尝百草": "shennong_chang_baicao",
    "孟母三迁": "mengmu_san_qian",
    "嫦娥奔月": "chang_e_ben_yue",
    "张骞出使西域": "zhang_qian_chu_shi_xi_yu",
}

def parse_model_stories():
    paras = json.load(open("extracted/model_stories.json", encoding="utf-8"))
    out = []
    i = 0
    while i < len(paras):
        header = paras[i]
        m = re.match(r'^Story \d+:\s*(.+)$', header)
        if not m:
            i += 1
            continue
        title = m.group(1).strip()
        text = paras[i + 1]
        story_id = STORY_TITLE_TO_ID.get(title, re.sub(r'\W+', '_', title))
        out.append({
            "story_id": story_id,
            "title": title,
            "text": text,
        })
        i += 2
    return out

# ---------------------------------------------------------------------------
# Teacher-only docs (mengmu, shennong)
# ---------------------------------------------------------------------------
def parse_teacher_only(path, source_doc, story_id):
    paras = json.load(open(path, encoding="utf-8"))
    samples = []
    i = 0
    n = len(paras)
    while i < n:
        p = paras[i]
        if is_sample_number_alone(p):
            sample_num = p
            i += 1
            story_text = paras[i]
            i += 1
        else:
            m = is_sample_number_glued(p)
            if not m:
                i += 1
                continue
            sample_num = m.group(1)
            story_text = m.group(2)
            i += 1

        if i < n and norm_marker(paras[i]) == "Teacher feedback":
            i += 1

        teacher_items = []
        content_flags = []
        closing_note = None
        while i < n:
            p2 = paras[i]
            if is_sample_number_alone(p2) or is_sample_number_glued(p2):
                break
            if p2.strip() == "Try to include more details and descriptions":
                closing_note = p2
                i += 1
                continue
            if p2.startswith("Miss") or p2.startswith("Wrong information") or p2.startswith("Coherence problem"):
                content_flags.append(p2)
                i += 1
                continue
            teacher_items.append(p2)
            i += 1

        samples.append({
            "sample_id": f"{source_doc}#{sample_num}",
            "source_doc": source_doc,
            "doc_type": "teacher_only",
            "story_id": story_id,
            "sample_num": sample_num,
            "raw_text": story_text,
            "teacher_correction_items": teacher_items,
            "content_flags": content_flags,
            "ai_feedback_items": [],
            "closing_note": closing_note,
        })
    return samples

# ---------------------------------------------------------------------------
# AI-reviewed docs
# ---------------------------------------------------------------------------
def _consume_ai_list(paras, i, n, category, stop_fn):
    """Consume numbered AI-feedback items (+ optional My comment) until stop_fn(paras[i]) is True."""
    items = []
    while i < n and not stop_fn(paras[i]):
        item_text = paras[i]
        i += 1
        comment = None
        if i < n and paras[i].startswith("My comment"):
            comment = paras[i]
            i += 1
        items.append({"category": category, "raw_text": item_text, "my_comment": comment})
    return items, i

def parse_ai_reviewed_numbered(path, source_doc, story_id):
    """student_examples_corrections.docx: samples headed by a bare integer paragraph."""
    paras = json.load(open(path, encoding="utf-8"))
    samples = []
    i = 0
    n = len(paras)
    while i < n:
        p = paras[i]
        if not is_sample_number_alone(p):
            i += 1
            continue
        sample_num = p
        i += 1
        story_text = paras[i]
        i += 1
        samples.append(_parse_one_ai_reviewed_unit(paras, i, n, source_doc, story_id, sample_num))
        i = samples[-1].pop("_next_i")
        samples[-1]["raw_text"] = story_text
    return samples

def parse_ai_reviewed_scenes(path, source_doc, story_id):
    """Pear_Story_Corrections.docx: samples headed by 'Scene N:' + text on the next paragraph."""
    paras = json.load(open(path, encoding="utf-8"))
    samples = []
    i = 0
    n = len(paras)
    while i < n:
        p = paras[i]
        m = re.match(r'^Scene (\d+):\s*$', p) or re.match(r'^Scene (\d+):(.*)$', p)
        if not m or not p.startswith("Scene"):
            i += 1
            continue
        scene_num = m.group(1)
        i += 1
        story_text = paras[i]
        i += 1
        rec = _parse_one_ai_reviewed_unit(paras, i, n, source_doc, story_id, scene_num, is_scene=True)
        i = rec.pop("_next_i")
        rec["raw_text"] = story_text
        samples.append(rec)
    return samples

def _parse_one_ai_reviewed_unit(paras, i, n, source_doc, story_id, unit_num, is_scene=False):
    assert norm_marker(paras[i]) == "Teacher feedback", f"expected Teacher feedback at {i}: {paras[i]}"
    i += 1
    teacher_items = []
    closing_note = None
    while i < n and norm_marker(paras[i]) != "AI feedback":
        if paras[i].strip() == "Try to include more details and descriptions":
            closing_note = paras[i]
        else:
            teacher_items.append(paras[i])
        i += 1
    # consume 'AI feedback:' marker
    i += 1

    ai_items = []
    # optional leading Wrong-characters line
    if i < n and paras[i].startswith("错别字"):
        wc_line = paras[i]
        i += 1
        comment = None
        if i < n and paras[i].startswith("My comment"):
            comment = paras[i]
            i += 1
        ai_items.append({"category": "wrong_characters", "raw_text": wc_line, "my_comment": comment})

    # Grammar Corrections header
    if i < n and "Grammar Correction" in paras[i]:
        i += 1
        items, i = _consume_ai_list(
            paras, i, n, "grammar",
            stop_fn=lambda x: "Vocabulary Suggestion" in x
        )
        ai_items.extend(items)

    # Vocabulary Suggestions header
    if i < n and "Vocabulary Suggestion" in paras[i]:
        i += 1
        def stop(x):
            return (is_sample_number_alone(x) or is_sample_number_glued(x) is not None
                    or x.startswith("Scene "))
        items, i = _consume_ai_list(paras, i, n, "vocabulary", stop_fn=stop)
        ai_items.extend(items)

    key = "scene_num" if is_scene else "sample_num"
    sample_id = f"{source_doc}#scene{unit_num}" if is_scene else f"{source_doc}#{unit_num}"
    return {
        "sample_id": sample_id,
        "source_doc": source_doc,
        "doc_type": "ai_reviewed",
        "story_id": story_id,
        key: unit_num,
        "teacher_correction_items": teacher_items,
        "content_flags": [],
        "ai_feedback_items": ai_items,
        "closing_note": closing_note,
        "_next_i": i,
    }

# ---------------------------------------------------------------------------
def main():
    corpus = {"model_stories": [], "samples": []}
    corpus["model_stories"] = parse_model_stories()

    corpus["samples"].extend(parse_teacher_only(
        "extracted/mengmu_samples.json", "mengmu_samples", "mengmu_san_qian"))
    corpus["samples"].extend(parse_teacher_only(
        "extracted/shennong_samples.json", "shennong_samples", "shennong_chang_baicao"))
    corpus["samples"].extend(parse_ai_reviewed_numbered(
        "extracted/student_examples_corrections.json", "student_examples_corrections", "pear_story_narrative"))
    corpus["samples"].extend(parse_ai_reviewed_scenes(
        "extracted/pear_story_corrections.json", "pear_story_corrections", "pear_story_creative"))

    with open("extracted/corpus.json", "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=1)

    # ---- sanity report ----
    print("Model stories:", len(corpus["model_stories"]))
    from collections import Counter
    by_doc = Counter(s["source_doc"] for s in corpus["samples"])
    print("Samples by source doc:", dict(by_doc))
    n_teacher_items = sum(len(s["teacher_correction_items"]) for s in corpus["samples"])
    n_ai_items = sum(len(s["ai_feedback_items"]) for s in corpus["samples"])
    n_flags = sum(len(s["content_flags"]) for s in corpus["samples"])
    print("Total teacher correction items:", n_teacher_items)
    print("Total AI feedback items:", n_ai_items)
    print("Total content-coverage flags:", n_flags)
    n_ai_with_comment = sum(
        1 for s in corpus["samples"] for it in s["ai_feedback_items"] if it.get("my_comment")
    )
    print("AI items with a teacher 'My comment':", n_ai_with_comment, "/", n_ai_items)

if __name__ == "__main__":
    main()
