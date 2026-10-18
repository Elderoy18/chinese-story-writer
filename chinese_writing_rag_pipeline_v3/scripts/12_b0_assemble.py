#!/usr/bin/env python3
"""Step 12 (B0) -- assemble the complete feedback per test story, freeze the round,
and write the teacher's documents.

    data/08_b0_vote/items.jsonl (corrections), data/10_b0_enrich/enrich.jsonl,
    data/11_b0_content/checks_test.jsonl, corpus, split
        ->  runs/B0/feedback.json, runs/B0/feedback/<sample>.md
            runs/B0/manifest.json          models, prompt versions, script and data hashes
            runs/B0/scripts/               the scripts exactly as run
            review/B0_feedback_for_teacher.md
            review/B0_labels.csv           one row per correction, for her verdict
            review/B0_labels_instructions.md

Per scene, in this order:
  Corrections  -- each corrected sentence once: the student's clause → the whole
                  clause corrected; under it, every error in it with its own
                  category (Grammar / Vocabulary / Coherence: Reference, 了 / 着 / 在,
                  Connectors) and explanation. One clause can hold errors of
                  several categories, so categories are labelled per error rather
                  than by section heading.
  Vocabulary suggestions -- marked (suggestion): a correct word, a same-level alternative.
  Expressiveness, Encouragement.
After the whole story: Content & completeness (missing scenes, parts to add, wrong
information), built from the content check's majority verdicts.
"""
import hashlib
import json
import shutil
import subprocess
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUN = ROOT / "runs" / "B0"
REVIEW = ROOT / "review"
CORRECTIONS = ROOT / "data" / "08_b0_vote" / "items.jsonl"
ENRICH = ROOT / "data" / "10_b0_enrich" / "enrich.jsonl"
CONTENT = ROOT / "data" / "11_b0_content" / "checks_test.jsonl"
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
SPLIT = ROOT / "data" / "03_split" / "split.json"
STEPS = ["07_b0_write", "08_b0_vote", "10_b0_enrich", "11_b0_content"]

LABEL = {"grammar": "Grammar", "vocabulary": "Vocabulary"}
COHERENCE = {"reference": "Coherence: Reference", "temporality": "Coherence: 了 / 着 / 在", "connectors": "Coherence: Connectors"}


def category(e):
    if e["dimension"] == "coherence":
        return COHERENCE.get(e["coherence_type"], "Coherence")
    return LABEL.get(e["dimension"], e["dimension"].title())


def error_line(e):
    o, c = e["original"], e["correction"]
    change = f"{o} → {c}" if o and c else (f"delete {o}" if o else f"add {c}")
    return f"**{category(e)}** {change}: {e['explanation']}"


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
            scenes.append({"scene": k, "text": s["text"][sc["start"]:sc["end"]],
                           "corrections": [{"before": c["before"], "after": c["after"], "errors": c["errors"],
                                            "start": c["start"], "end": c["end"]}
                                           for c in sorted(corr[(s["sample_id"], k)], key=lambda c: c["start"])],
                           "vocabulary_suggestions": e["vocabulary_suggestions"], "expressiveness": e["expressiveness"],
                           "encouragement": e["encouragement"]})
        stories.append({"sample_id": s["sample_id"], "story_id": s["story_id"], "scenes": scenes,
                        "content": content[s["sample_id"]]["notes"]})
    return stories


def render(story, h="##"):
    L = [f"# Feedback: {story['sample_id']}", ""]
    for sc in story["scenes"]:
        L += [f"{h} Scene {sc['scene']}", "", f"> {sc['text']}", "", "**Corrections**"]
        if sc["corrections"]:
            for c in sc["corrections"]:
                L.append(f"- {c['before']} → {c['after']}")
                L += [f"  - {error_line(e)}" for e in c["errors"]]
        else:
            L.append("- *No corrections.*")
        if sc["vocabulary_suggestions"]:
            L += ["", "**Vocabulary suggestions**"]
            L += [f"- (suggestion) {v['word']} (“{v['phrase']}”) → {v['alternative']} (“{v['new_phrase']}”): {v['note']}"
                  for v in sc["vocabulary_suggestions"]]
        if sc["expressiveness"]:
            L += ["", "**Expressiveness**"]
            L += [f"- After “{x['where']}”: {x['idea']} For example: {x['example']}" for x in sc["expressiveness"]]
        L += ["", f"**Encouragement** {sc['encouragement']}", ""]
    L += [f"{h} Content & completeness (after the whole story)", ""]
    L += [f"- {n}" for n in story["content"]] or ["- The story tells every required scene."]
    return L + [""]


def sha(p):
    return hashlib.sha1(p.read_bytes()).hexdigest()[:12]


def freeze(stories):
    RUN.mkdir(parents=True, exist_ok=True)
    (RUN / "feedback").mkdir(exist_ok=True)
    json.dump(stories, open(RUN / "feedback.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for st in stories:
        (RUN / "feedback" / f"{st['sample_id'].replace('#', '_')}.md").write_text("\n".join(render(st)), encoding="utf-8")
    scripts = RUN / "scripts"
    if scripts.exists():
        shutil.rmtree(scripts)
    shutil.copytree(ROOT / "scripts", scripts, ignore=shutil.ignore_patterns("__pycache__"))
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain", "."], cwd=ROOT, capture_output=True, text=True).stdout.strip())
    except OSError:
        commit, dirty = "", None
    infos = {s: json.load(open(ROOT / "data" / s / "run_info.json", encoding="utf-8"))
             for s in STEPS if (ROOT / "data" / s / "run_info.json").exists()}
    for v in infos.values():
        v.pop("system", None)
    infos["11_b0_content"] = {"prompt": "calibrated content check (core vs details + her train decisions); see reports/11_b0_content_test.md"}
    manifest = {"round": "B0", "date": date.today().isoformat(), "data": "basic data only", "git_commit": commit,
                "git_uncommitted_changes": dirty, "steps": infos,
                "scripts": {p.name: sha(p) for p in sorted((ROOT / "scripts").glob("*.py"))},
                "inputs": {str(p.relative_to(ROOT)): sha(p) for p in [CORRECTIONS, ENRICH, CONTENT, CORPUS, SPLIT]}}
    json.dump(manifest, open(RUN / "manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def teacher_docs(stories):
    REVIEW.mkdir(exist_ok=True)
    L = ["# New feedback system (round B0) -- for review", "",
         "This round was built only from the basic materials: the graded student stories, the model stories,",
         "the required-scene lists and the coherence rules. None of the comments on earlier AI feedback were",
         "used yet. The corrections of these 20 stories were not available to the system.", "",
         "Changes from the previous round, following the comments on it:", "",
         "- Each correction shows the **whole sentence** (clause) before → after, with every error in it fixed,",
         "  so the corrected version should be complete and correct.",
         "- Each error inside a sentence is labelled with its own category (Grammar, Vocabulary, or Coherence:",
         "  Reference / 了着在 / Connectors). There is no Content or Other category among the corrections.",
         "- A correction is shown only if at least two of three independent runs of the system made it.",
         "- Fewer vocabulary suggestions and expressiveness ideas, only where clearly useful.",
         "- The content check lists each missing scene in the wording of the required-scene list.", "",
         "Each correction can be judged in `B0_labels.csv` (see `B0_labels_instructions.md`).", ""]
    for st in stories:
        L += render(st, h="###")[0:0] + [f"## {st['sample_id']}", ""] + render(st, h="###")[2:]
    (REVIEW / "B0_feedback_for_teacher.md").write_text("\n".join(L), encoding="utf-8")

    import csv
    with open(REVIEW / "B0_labels.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["story", "scene", "student_sentence", "corrected_sentence", "errors_and_categories",
                    "VERDICT (right / correction wrong / not an error)", "CATEGORY_OK (yes / no)", "NOTE"])
        for st in stories:
            for sc in st["scenes"]:
                for c in sc["corrections"]:
                    w.writerow([st["sample_id"], sc["scene"], c["before"], c["after"],
                                "\n".join(f"[{category(e)}] {e['original']} → {e['correction']}" for e in c["errors"]), "", "", ""])
    (REVIEW / "B0_labels_instructions.md").write_text(LABEL_INSTRUCTIONS, encoding="utf-8")


LABEL_INSTRUCTIONS = """# Judging the corrections (B0_labels.csv)

Each row is one correction the system would show a student: the student's sentence, the corrected
sentence, and the errors in it with their categories.

- **VERDICT**: `right` -- a real error and the corrected sentence is correct; `correction wrong` -- there is
  an error, but the corrected sentence is wrong or still contains an error; `not an error` -- the original
  was fine.
- **CATEGORY_OK**: `yes` if every error is in the right category, `no` otherwise (a note on which is welcome).
- **NOTE**: anything else, in any language.

The answers are kept and reused: a correction judged once is not asked again in later rounds.
"""


def main():
    stories = build()
    freeze(stories)
    teacher_docs(stories)
    n = sum(len(sc["corrections"]) for st in stories for sc in st["scenes"])
    print(f"{len(stories)} stories: {n} corrections, "
          f"{sum(len(sc['vocabulary_suggestions']) for st in stories for sc in st['scenes'])} vocabulary suggestions, "
          f"{sum(len(sc['expressiveness']) for st in stories for sc in st['scenes'])} expressiveness ideas, "
          f"{sum(len(st['content']) for st in stories)} content notes")
    print(f"Frozen: {(RUN / 'manifest.json').relative_to(ROOT)}; for the teacher: review/B0_feedback_for_teacher.md, review/B0_labels.csv")


if __name__ == "__main__":
    main()
