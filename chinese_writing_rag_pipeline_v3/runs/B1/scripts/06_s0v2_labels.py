#!/usr/bin/env python3
"""Step 6 -- turn the teacher's comments on the previous system's feedback (S0,
`S0_v2_feedback check.docx`) into evaluation labels.

    data/01_extracted/feedback_data/S0_v2_feedback check.json, corpus, OpenAI
        ->  data/06_s0v2_labels/comments.jsonl          one comment per line, with what it says
            review/06_s0v2_comment_tags.csv              for checking the tags by hand
            reports/06_s0v2_labels.md                    the previous system's measured problems

These are EVALUATION labels, not system input: they measure the previous system
on the stories she reviewed (6 of the 20 test stories), so later systems have a
measured baseline to beat. Nothing here is shown to any feedback model.

Her document is the S0 feedback for 6 stories ("Story 1" ... "Story 6", each with
scenes, sections Grammar / Vocabulary / Coherence / ..., Expressiveness, Content
& completeness), with Word comments attached to individual feedback lines. Many
comments name several problems ("1 Show partial sentence 2 There is no error").
Feedback lines wrap, so lines are not parsed by hand: for each comment, an LLM
gets her comment, the exact text it is attached to and the surrounding text, and
returns the section, the feedback item it is about, and every problem it names,
as tags from a fixed list.
"""
import csv
import json
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from llm import api_key, cached_json_call, prompt_version

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "data" / "01_extracted" / "feedback_data" / "S0_v2_feedback check.json"
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
OUT = ROOT / "data" / "06_s0v2_labels"
CACHE = OUT / "cache"
SHEET = ROOT / "review" / "06_s0v2_comment_tags.csv"
REPORT = ROOT / "reports" / "06_s0v2_labels.md"

MODEL = "gpt-5.6-terra"
REASONING_EFFORT = "medium"
CONTEXT = 500   # characters of surrounding text shown on each side

TAGS = {
    "false_positive": "the flagged text is not an error / no correction needed / the original is fine",
    "incorrect_correction": "the correction (after →) is wrong, ungrammatical, or still contains an error",
    "partial_sentence": "the feedback shows a partial / truncated sentence that confuses",
    "miscategorized": "the item is in the wrong section or category (e.g. should be Grammar, not Vocabulary)",
    "duplicate": "the item repeats another item",
    "missed_error": "she points out an error the system did not flag",
    "explanation_needed": "the correction is right but the explanation is missing, wrong or should be improved",
    "bad_suggestion": "a vocabulary suggestion is unnecessary, inappropriate, or changes the meaning",
    "bad_expressiveness": "an expressiveness idea is unnecessary, redundant, or inappropriate",
    "content_problem": "the end-of-story content check missed a scene, is wrong, or is unclear",
    "alternative": "she offers an alternative correction or wording, without saying the item is wrong",
    "other": "anything else",
}
SECTIONS = ["Grammar", "Vocabulary", "Coherence", "Content", "Other", "Expressiveness", "Encouragement",
            "Content & completeness", "unclear"]

SYSTEM = f"""You read one comment a Chinese teacher wrote on AI-generated feedback for a learner's story, and record what the comment says. Do not judge whether the teacher is right.

You get the teacher's comment, the exact text it is attached to, and the surrounding feedback (the scene and the section headings are in it).

Return:
- section: the feedback section the commented text is in ({' / '.join(SECTIONS)}).
- item: the feedback item the comment is about, copied from the feedback: "before" (the student's words before →, or the word a suggestion is for) and "after" (the text after →, or "" if there is none). For an expressiveness idea or a content note, before = the first words of that line, after = "".
- tags: every problem or remark the comment makes, from this list (one comment can have several):
""" + "\n".join(f"  {k}: {v}" for k, v in TAGS.items()) + """
- missed: if she names an error the system missed, the student's words and her correction ("" otherwise).
- summary: her point in one short English sentence."""

SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["section", "item", "tags", "missed", "summary"],
    "properties": {
        "section": {"type": "string", "enum": SECTIONS},
        "item": {"type": "object", "additionalProperties": False, "required": ["before", "after"],
                 "properties": {"before": {"type": "string"}, "after": {"type": "string"}}},
        "tags": {"type": "array", "items": {"type": "string", "enum": list(TAGS)}},
        "missed": {"type": "string"},
        "summary": {"type": "string"},
    },
}
PROMPT_VERSION = prompt_version(SYSTEM, SCHEMA)


def story_map(paras, samples):
    """'Story N' heading -> the test sample whose text its first scene starts with."""
    out, current = {}, None
    for p in paras:
        m = re.match(r"^Story\s*(\d+)$", p["text"])
        if m:
            current = int(m.group(1))
            continue
        if current and current not in out:
            body = re.sub(r"^Scene \d+\s*", "", p["text"]).replace("\n", "")[:15]
            hits = [s["sample_id"] for s in samples if body and body in s["text"].replace("\n", "")]
            out[current] = hits[0] if len(hits) == 1 else None
    return out


def para_story(paras):
    """paragraph index -> story number, and -> the latest 'Scene N' above each character."""
    story, cur = {}, None
    for p in paras:
        m = re.match(r"^Story\s*(\d+)$", p["text"])
        if m:
            cur = int(m.group(1))
        story[p["i"]] = cur
    return story


def scene_at(paras, p, c):
    text = "\n".join(x["text"] for x in paras[:p]) + "\n" + paras[p]["text"][:c]
    tail = text[text.rfind("Story "):] if "Story " in text else text
    scenes = re.findall(r"Scene (\d+)", tail)
    return int(scenes[-1]) if scenes else None


def main():
    doc = json.load(open(DOC, encoding="utf-8"))
    paras = doc["paragraphs"]
    samples = json.load(open(CORPUS, encoding="utf-8"))["samples"]
    stories, pstory = story_map(paras, samples), para_story(paras)
    if None in stories.values():
        raise SystemExit(f"could not match every story to a sample: {stories}")

    jobs = []
    for c in doc["comments"]:
        a = c["anchor"]
        p, s, e = a["start"]["p"], a["start"]["c"], a["end"]["c"] if a["end"]["p"] == a["start"]["p"] else None
        text = paras[p]["text"]
        before_ctx = text[max(0, s - CONTEXT):s]
        after_ctx = text[(e if e is not None else s):(e if e is not None else s) + CONTEXT]
        user = (f"Teacher's comment:\n{c['text']}\n\nAttached to:\n{a['text']}\n\n"
                f"Surrounding feedback (the attached text is between ⟦ ⟧):\n{before_ctx}⟦{a['text']}⟧{after_ctx}")
        jobs.append((c, stories[pstory[p]], scene_at(paras, p, s), user))

    api_key()
    with ThreadPoolExecutor(8) as ex:
        results = list(ex.map(lambda j: cached_json_call(CACHE, MODEL, REASONING_EFFORT, SYSTEM, SCHEMA,
                                                         "comment_tags", j[3]), jobs))
    rows = []
    for (c, sid, scene, _), (rec, _cached) in zip(jobs, results):
        o = rec["output"]
        rows.append({"comment_id": c["id"], "sample_id": sid, "scene": scene, "section": o["section"],
                     "before": o["item"]["before"], "after": o["item"]["after"], "tags": o["tags"],
                     "missed": o["missed"], "summary": o["summary"], "comment": c["text"],
                     "anchor": c["anchor"]["text"], "prompt_version": PROMPT_VERSION})
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "comments.jsonl", "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    write_sheet(rows)
    write_report(rows, stories, doc)
    print(f"{len(rows)} comments tagged -> {(OUT / 'comments.jsonl').relative_to(ROOT)}; "
          f"sheet {SHEET.relative_to(ROOT)}; report {REPORT.relative_to(ROOT)}")


def write_sheet(rows):
    SHEET.parent.mkdir(parents=True, exist_ok=True)
    with open(SHEET, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["comment_id", "story", "scene", "section", "item_before", "item_after", "her_comment",
                    "tags", "missed_error", "TAGS_OK (yes / fix)", "CORRECT_TAGS"])
        for r in rows:
            w.writerow([r["comment_id"], r["sample_id"], r["scene"], r["section"], r["before"], r["after"],
                        r["comment"], ", ".join(r["tags"]), r["missed"], "", ""])


def count_items(doc):
    """Rough count of feedback items shown in the reviewed stories: arrows in correction sections."""
    n = Counter()
    for p in doc["paragraphs"]:
        section = None
        for line in p["text"].split("\n"):
            s = line.strip()
            if s in ("Grammar", "Vocabulary", "Coherence", "Content", "Other", "Expressiveness"):
                section = s
            elif s.startswith("Content & completeness"):
                section = "Content & completeness"
            elif section and ("→" in s or s.startswith("At “") or section == "Content & completeness") and s:
                n[section] += 1
    return n


def write_report(rows, stories, doc):
    tags = Counter(t for r in rows for t in r["tags"])
    by_section = Counter((r["section"], t) for r in rows for t in r["tags"])
    shown = count_items(doc)
    L = ["# Step 6 report: her comments on the previous system's feedback (S0)", "",
         f"- {len(rows)} comments on {len(stories)} stories: " + ", ".join(f"Story {k} = {v}" for k, v in stories.items()),
         f"- model {MODEL} ({REASONING_EFFORT}), prompt {PROMPT_VERSION}", "",
         "## What her comments say (a comment can carry several tags)", "",
         "| Tag | Comments | Meaning |", "|---|---|---|"]
    L += [f"| {t} | {n} | {TAGS[t]} |" for t, n in tags.most_common()]
    L += ["", "## By section", "", "| Section | " + " | ".join(TAGS) + " |", "|---|" + "---|" * len(TAGS)]
    for s in SECTIONS:
        if any(by_section[(s, t)] for t in TAGS):
            L.append(f"| {s} | " + " | ".join(str(by_section[(s, t)] or "") for t in TAGS) + " |")
    corr = sum(shown[s] for s in ("Grammar", "Vocabulary", "Coherence", "Content", "Other"))
    fp, inc = tags["false_positive"], tags["incorrect_correction"]
    L += ["", "## The previous system (S0), measured on these 6 stories (18 scenes)", "",
          f"- lines shown in correction sections (approximate count of '→' lines, vocabulary suggestions included): {corr}",
          f"- comments saying **not an error**: {fp} -> {fp / 18:.2f} per scene",
          f"- comments saying the **correction is wrong**: {inc} -> {inc / 18:.2f} per scene",
          f"- comments about **partial sentences**: {tags['partial_sentence']}; **miscategorized**: {tags['miscategorized']}; "
          f"**duplicates**: {tags['duplicate']}; **missed errors** she added: {tags['missed_error']}",
          "", "These are lower bounds: she commented on what she noticed, not necessarily every item.", "",
          "## Every comment", ""]
    for r in rows:
        L.append(f"- {r['sample_id']} scene {r['scene']} [{r['section']}] `{r['before'][:40]}` → `{r['after'][:40]}` "
                 f"— **{', '.join(r['tags'])}** — {r['summary']}")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
