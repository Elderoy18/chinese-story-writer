#!/usr/bin/env python3
"""Step 16 (B1) -- assemble the complete feedback per test story in the agreed
format, freeze round B1, and write the teacher's documents.

    data/14_b1_vote/items.jsonl (error lines), data/15_b1_enrich/enrich.jsonl,
    data/11_b0_content/checks_test.jsonl (content check, unchanged from B0), corpus, split
        ->  runs/B1/feedback.json, runs/B1/feedback/<sample>.md, runs/B1/manifest.json, runs/B1/scripts/
            review/B1_feedback_for_teacher.md, review/B1_labels.csv + review/B1_labels_instructions.md

Per scene:
    Grammar and Vocab Corrections
    - 原文：改正，explanation                          (grammar and wrong-word errors)
    Coherence: Reference / Temporality / Conjunction
    - **Reference** 原文：改正，explanation          (each line labelled with its type)
    Expressiveness
    New Words                                         (suggestions for words that are correct -- not errors)
    Encouragement
After the whole story: Content & completeness.
"""
import csv
import hashlib
import json
import shutil
import subprocess
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUN = ROOT / "runs" / "B1"
REVIEW = ROOT / "review"
CORRECTIONS = ROOT / "data" / "14_b1_vote" / "items.jsonl"
ENRICH = ROOT / "data" / "15_b1_enrich" / "enrich.jsonl"
CONTENT = ROOT / "data" / "11_b0_content" / "checks_test.jsonl"
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
SPLIT = ROOT / "data" / "03_split" / "split.json"
STEPS = ["13_b1_write", "14_b1_vote", "15_b1_enrich", "11_b0_content"]
COHERENCE = {"reference": "Reference", "temporality": "Temporality", "conjunction": "Conjunction"}


def category(c):
    return "Grammar and Vocab" if c["section"] == "grammar_vocab" else f"Coherence: {COHERENCE[c['coherence_type']]}"


def line(c):
    return f"{c['before']}：{c['after']}，{c['explanation']}"


def build():
    corpus = json.load(open(CORPUS, encoding="utf-8"))
    split = json.load(open(SPLIT, encoding="utf-8"))
    samples = {s["sample_id"]: s for s in corpus["samples"]}
    corr = defaultdict(list)
    for l in open(CORRECTIONS, encoding="utf-8"):
        it = json.loads(l)
        corr[(it["sample_id"], it["scene"])].append(it)
    enrich = {(r["sample_id"], r["scene"]): r for r in map(json.loads, open(ENRICH, encoding="utf-8"))}
    content = {r["sample_id"]: r for r in map(json.loads, open(CONTENT, encoding="utf-8"))}
    stories = []
    for t in split["test"]:
        s = samples[t["sample_id"]]
        scenes = []
        for k, sc in enumerate(t["scenes"], 1):
            e = enrich[(s["sample_id"], k)]
            cs = sorted(corr[(s["sample_id"], k)], key=lambda c: c["start"])
            scenes.append({"scene": k, "text": s["text"][sc["start"]:sc["end"]],
                           "corrections": [{x: c[x] for x in ("before", "after", "explanation", "section", "coherence_type",
                                                               "start", "end")} for c in cs],
                           "vocabulary_suggestions": e["vocabulary_suggestions"], "expressiveness": e["expressiveness"],
                           "encouragement": e["encouragement"]})
        stories.append({"sample_id": s["sample_id"], "story_id": s["story_id"], "scenes": scenes,
                        "content": content[s["sample_id"]]["notes"]})
    return stories


def render_scenes(story, h):
    L = []
    for sc in story["scenes"]:
        gv = [c for c in sc["corrections"] if c["section"] == "grammar_vocab"]
        co = sorted([c for c in sc["corrections"] if c["section"] == "coherence"],
                    key=lambda c: (list(COHERENCE).index(c["coherence_type"]), c["start"]))
        L += [f"{h} Scene {sc['scene']}", "", f"> {sc['text']}", "",
              "**Grammar and Vocab Corrections**", *([f"- {line(c)}" for c in gv] or ["- Nothing to flag."]), "",
              "**Coherence: Reference / Temporality / Conjunction**",
              *([f"- **{COHERENCE[c['coherence_type']]}** {line(c)}" for c in co] or ["- Nothing to flag."]), "",
              "**Expressiveness**",
              *([f"- After “{x['where']}”: {x['idea']} For example: {x['example']}" for x in sc["expressiveness"]]
                or ["- No suggestions."]), "",
              "**New Words**",
              *([f"- {v['word']} (“{v['phrase']}”)：{v['alternative']} (“{v['new_phrase']}”)，{v['note']}"
                 for v in sc["vocabulary_suggestions"]] or ["- No suggestions."]), "",
              f"**Encouragement** {sc['encouragement']}", ""]
    L += [f"{h} Content & completeness (after the whole story)", ""]
    L += [f"- {n}" for n in story["content"]] or ["- The story tells every required scene."]
    return L + [""]


def sha(p):
    return hashlib.sha1(p.read_bytes()).hexdigest()[:12]


def freeze(stories):
    (RUN / "feedback").mkdir(parents=True, exist_ok=True)
    json.dump(stories, open(RUN / "feedback.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for st in stories:
        md = [f"# Feedback: {st['sample_id']}", ""] + render_scenes(st, "##")
        (RUN / "feedback" / f"{st['sample_id'].replace('#', '_')}.md").write_text("\n".join(md), encoding="utf-8")
    if (RUN / "scripts").exists():
        shutil.rmtree(RUN / "scripts")
    shutil.copytree(ROOT / "scripts", RUN / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain", "."], cwd=ROOT, capture_output=True, text=True).stdout.strip())
    except OSError:
        commit, dirty = "", None
    infos = {s: json.load(open(ROOT / "data" / s / "run_info.json", encoding="utf-8"))
             for s in STEPS if (ROOT / "data" / s / "run_info.json").exists()}
    infos["15_b1_enrich"] = {**infos.get("15_b1_enrich", {}),
                             "script": "10_b0_enrich.py --corrections data/14_b1_vote/items.jsonl --out data/15_b1_enrich"}
    infos["11_b0_content"] = {"prompt": "calibrated content check (core vs details + her train decisions)"}
    json.dump({"round": "B1", "date": date.today().isoformat(), "data": "basic data only", "git_commit": commit,
               "git_uncommitted_changes": dirty, "steps": infos,
               "scripts": {p.name: sha(p) for p in sorted((ROOT / "scripts").glob("*.py"))},
               "inputs": {str(p.relative_to(ROOT)): sha(p) for p in [CORRECTIONS, ENRICH, CONTENT, CORPUS, SPLIT]}},
              open(RUN / "manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


INTRO = [
    "# New feedback system (round B1) -- for review", "",
    "This round was built only from the basic materials: the graded student stories, the model stories, the",
    "required-scene lists and the coherence rules. None of the comments on earlier AI feedback were used yet.",
    "The corrections of these 20 stories were not available to the system.", "",
    "Per scene: Grammar and Vocab Corrections; Coherence (each line labelled Reference, Temporality or",
    "Conjunction); Expressiveness; New Words (suggestions for words that are correct); Encouragement. After the",
    "story: Content & completeness. Each correction is one line -- the student's words：the corrected words，what",
    "is wrong and why. The corrected words are a complete phrase with every error in it fixed. A correction is",
    "shown only if at least two of three independent runs of the system made it.", "",
    "Each correction can be judged in `B1_labels.csv` (see `B1_labels_instructions.md`).", ""]

LABEL_INSTRUCTIONS = """# Judging the corrections (B1_labels.csv)

Each row is one correction the system would show a student: its category, the student's words, the
corrected words and the explanation.

- **VERDICT**: `right` -- a real error and the correction is right; `correction wrong` -- there is an error,
  but the corrected words are wrong or still contain an error; `not an error` -- the original was fine.
- **CATEGORY_OK**: `yes` if the category is right, `no` otherwise.
- **EXPLANATION_OK**: `yes` if the explanation says correctly what is wrong and why, `no` otherwise.
- **NOTE**: anything else, in any language.

The answers are kept and reused: a correction judged once is not asked again in later rounds.
"""


def teacher_docs(stories):
    REVIEW.mkdir(exist_ok=True)
    L = list(INTRO)
    for st in stories:
        L += [f"## {st['sample_id']}", ""] + render_scenes(st, "###")
    (REVIEW / "B1_feedback_for_teacher.md").write_text("\n".join(L), encoding="utf-8")
    with open(REVIEW / "B1_labels.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["story", "scene", "category", "student_words", "corrected_words", "explanation",
                    "VERDICT (right / correction wrong / not an error)", "CATEGORY_OK (yes / no)",
                    "EXPLANATION_OK (yes / no)", "NOTE"])
        for st in stories:
            for sc in st["scenes"]:
                for c in sc["corrections"]:
                    w.writerow([st["sample_id"], sc["scene"], category(c), c["before"], c["after"], c["explanation"],
                                "", "", "", ""])
    (REVIEW / "B1_labels_instructions.md").write_text(LABEL_INSTRUCTIONS, encoding="utf-8")


def main():
    stories = build()
    freeze(stories)
    teacher_docs(stories)
    cs = [c for st in stories for sc in st["scenes"] for c in sc["corrections"]]
    print(f"{len(stories)} stories: {sum(c['section'] == 'grammar_vocab' for c in cs)} grammar/vocab lines, "
          f"{sum(c['section'] == 'coherence' for c in cs)} coherence lines, "
          f"{sum(len(sc['vocabulary_suggestions']) for st in stories for sc in st['scenes'])} new words, "
          f"{sum(len(sc['expressiveness']) for st in stories for sc in st['scenes'])} expressiveness ideas")
    print(f"Frozen: {(RUN / 'manifest.json').relative_to(ROOT)}; teacher: review/B1_feedback_for_teacher.md, review/B1_labels.csv")


if __name__ == "__main__":
    main()
