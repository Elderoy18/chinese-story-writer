#!/usr/bin/env python3
"""Step 17 -- assemble the complete feedback for every test story and freeze
the system as round S0 (basic data only; before any of the teacher's
human-in-the-loop input).

    data/15_explain/items.jsonl (errors), data/16_enrich/enrich.jsonl
    (vocabulary suggestions, expressiveness, encouragement), data/10_content/checks_test.jsonl
    (end-of-story content)
        ->  runs/S0/feedback.json                 everything, per story and scene
            runs/S0/feedback/<sample>.md          what one learner would see
            runs/S0/manifest.json                 the frozen system: models, prompt versions,
                                                  settings, file hashes, git commit
            runs/S0/scripts/                      copy of every script as run
            review/S0_feedback_for_teacher.md     all 20 stories with their feedback (teacher)
            review/S0_story_ratings.csv           one row per story, for her ratings

    python scripts/17_assemble_s0.py

Per scene, in the order a learner sees it:
  Corrections -- grouped by her dimensions: Grammar, Vocabulary, Coherence
                 (reference / temporality / connectors), Content, Other;
                 "(suggestion)" marks the softly worded ones
  Vocabulary suggestions -- enrichment for words used correctly
  Expressiveness -- ideas for going beyond recounting events
  Encouragement
After the last scene: Content & completeness -- from the content check (the
run whose verdicts match the majority of its 3 runs).
"""
import csv
import hashlib
import json
import re
import shutil
import subprocess
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
SPLIT = ROOT / "data" / "03_split" / "split.json"
ITEMS = ROOT / "data" / "15_explain" / "items.jsonl"
ENRICH = ROOT / "data" / "16_enrich" / "enrich.jsonl"
CONTENT = ROOT / "data" / "10_content" / "checks_test.jsonl"
RUN = ROOT / "runs" / "S0"
TEACHER_DOC = ROOT / "review" / "S0_feedback_for_teacher.md"
RATINGS = ROOT / "review" / "S0_story_ratings.csv"

SECTIONS = {"grammar": "Grammar", "word_choice": "Vocabulary", "coherence_reference": "Coherence: reference",
            "coherence_temporality": "Coherence: 了 / 着 / 在", "coherence_connectors": "Coherence: connectors",
            "content": "Content", "other": "Other"}
clean = lambda s: re.sub(r'["}\]\[,]{3,}', "", s or "").strip()


def scene_feedback(items, enrich):
    out = {"corrections": [], "vocabulary_suggestions": [], "expressiveness": [], "encouragement": ""}
    for dim in SECTIONS:
        for it in sorted([it for it in items if it["dimension"] == dim], key=lambda it: it["start"]):
            fix = f"{it['original'] or '∅'} → {it['corrected'] or '(delete)'}" if it["corrected"] is not None else f"⟦{it['original']}⟧"
            out["corrections"].append({"section": SECTIONS[dim], "strength": it["strength"], "correction": fix,
                                       "explanation": clean(it["explanation"]), "item_id": it["item_id"]})
    if enrich:
        out["vocabulary_suggestions"] = [{"word": v["word"], "phrase": v["phrase"],
                                          "alternatives": [{"word": a["word"], "note": clean(a["note"])} for a in v["alternatives"]]}
                                         for v in enrich["vocabulary_suggestions"]]
        out["expressiveness"] = [{"where": e["where"], "idea": clean(e["idea"]), "example": clean(e["example"])} for e in enrich["expressiveness"]]
        out["encouragement"] = clean(enrich["encouragement"])
    return out


def content_feedback(check):
    if not check:
        return []
    best = max(check["runs"], key=lambda r: sum(v["verdict"] == m for v, m in zip(r["verdicts"], check["majority"])))
    lines = [clean(f) for f in best["feedback"]]
    lines += [f"Wrong information: “{w['learner_text']}” — {clean(w['problem'])}" for w in best["wrong_information"]]
    return lines


def render_scene(fb, heading_level="###"):
    L = []
    if fb["corrections"]:
        current = None
        for c in fb["corrections"]:
            if c["section"] != current:
                current = c["section"]
                L.append(f"**{current}**")
            L.append(f"- {'(suggestion) ' if c['strength'] == 'suggestion' else ''}{c['correction']}: {c['explanation']}")
    else:
        L.append("*(No corrections.)*")
    if fb["vocabulary_suggestions"]:
        L += ["", "**Vocabulary suggestions**"]
        L += [f"- {v['word']} (“{v['phrase']}”) → " + "; ".join(f"{a['word']}: {a['note']}" for a in v["alternatives"])
              for v in fb["vocabulary_suggestions"]]
    if fb["expressiveness"]:
        L += ["", "**Expressiveness**"]
        L += [f"- At “{e['where']}”: {e['idea']} For example: {e['example']}" for e in fb["expressiveness"]]
    if fb["encouragement"]:
        L += ["", f"**Encouragement** {fb['encouragement']}"]
    return L


def sha(path):
    return hashlib.sha1(Path(path).read_bytes()).hexdigest()[:12]


def main():
    texts = {s["sample_id"]: s["text"] for s in json.load(open(CORPUS, encoding="utf-8"))["samples"]}
    split = json.load(open(SPLIT, encoding="utf-8"))
    items = [json.loads(l) for l in open(ITEMS, encoding="utf-8")]
    enrich = {(r["sample_id"], r["scene"]): r for r in map(json.loads, open(ENRICH, encoding="utf-8"))}
    content = {r["sample_id"]: r for r in map(json.loads, open(CONTENT, encoding="utf-8"))}

    stories = []
    for t in split["test"]:
        sid = t["sample_id"]
        scenes = [{"scene": sc["scene"], "text": texts[sid][sc["start"]:sc["end"]],
                   "feedback": scene_feedback([it for it in items if it["sample_id"] == sid and it["scene"] == sc["scene"]],
                                              enrich.get((sid, sc["scene"])))} for sc in t["scenes"]]
        stories.append({"sample_id": sid, "story_id": t["story_id"], "scenes": scenes, "content": content_feedback(content.get(sid))})

    RUN.mkdir(parents=True, exist_ok=True)
    (RUN / "feedback.json").write_text(json.dumps(stories, ensure_ascii=False, indent=1), encoding="utf-8")
    (RUN / "feedback").mkdir(exist_ok=True)
    for s in stories:
        L = [f"# Feedback: {s['sample_id']}", ""]
        for sc in s["scenes"]:
            L += [f"## Scene {sc['scene']}", "", f"> {sc['text']}", "", *render_scene(sc["feedback"]), ""]
        L += ["## Content & completeness (after the whole story)", "", *([f"- {c}" for c in s["content"]] or ["- Every required scene is told."]), ""]
        (RUN / "feedback" / f"{s['sample_id'].replace('#', '_')}.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    freeze()
    write_teacher_doc(stories)
    write_ratings(stories)
    n = Counter()
    for s in stories:
        for sc in s["scenes"]:
            f = sc["feedback"]
            n["corrections"] += len(f["corrections"])
            n["suggestions (soft)"] += sum(c["strength"] == "suggestion" for c in f["corrections"])
            n["vocabulary suggestions"] += len(f["vocabulary_suggestions"])
            n["expressiveness ideas"] += len(f["expressiveness"])
        n["content notes"] += len(s["content"])
    print(f"{len(stories)} stories assembled: {dict(n)}")
    print(f"Frozen: {RUN.relative_to(ROOT)}/manifest.json; for the teacher: {TEACHER_DOC.relative_to(ROOT)}, {RATINGS.relative_to(ROOT)}")


def freeze():
    """Record exactly what S0 is: scripts (copied), models, prompt versions, settings, data hashes, git state."""
    snap = RUN / "scripts"
    if snap.exists():
        shutil.rmtree(snap)
    shutil.copytree(ROOT / "scripts", snap, ignore=shutil.ignore_patterns("__pycache__"))
    run_infos = {}
    for p in sorted((ROOT / "data").glob("*/run_info.json")):
        if p.parent.name.startswith("14_"):
            continue  # judge v1: measured, not part of S0
        run_infos[p.parent.name] = json.load(open(p, encoding="utf-8"))
    run_infos["10_content"] = {"prompt": "v3 (core vs details + her past decisions), see scripts/10_content.py"}
    for name in ("taxonomy.json",):
        p = ROOT / "data" / "11_categories" / name
        run_infos["11_categories"] = {"prompt_version": json.load(open(p, encoding="utf-8"))["prompt_version"]}
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    manifest = {
        "round": "S0",
        "description": "Basic data only (graded samples, model stories, scene lists, coherence rubric); before any of the teacher's "
                       "human-in-the-loop input. Errors: LLM finder (1 run) + GEC model + teacher finder (her patterns + HanLP "
                       "checks), merged, one correction per place by rule, explained from her rule cards and nearest past corrections "
                       "(no judging step). Enrichment: expressiveness, vocabulary suggestions, encouragement. Content: calibrated "
                       "scene check (v3).",
        "date": date.today().isoformat(),
        "git_commit": git("rev-parse", "HEAD"),
        "git_uncommitted_changes": bool(git("status", "--porcelain", "--", ".")),
        "models": {"llm": "gpt-5.6-terra (OpenAI)", "embeddings": "text-embedding-3-small (OpenAI)",
                   "parser": "HanLP CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH", "gec": "HillZhang/real_learner_bart_CGEC"},
        "steps": run_infos,
        "scripts_sha1": {p.name: sha(p) for p in sorted((ROOT / "scripts").glob("*.py"))},
        "data_sha1": {str(p.relative_to(ROOT)).replace("\\", "/"): sha(p) for p in [
            CORPUS, SPLIT, ROOT / "data/05_align/edits_train.jsonl", ROOT / "data/05_align/edits_test.jsonl",
            ROOT / "data/11_categories/taxonomy.json", ROOT / "data/12_rule_cards/cards.json",
            ROOT / "data/13_find_teacher/patterns.json", ITEMS, ENRICH, CONTENT]},
    }
    for info in manifest["steps"].values():
        info.pop("system_prompt", None)
    (RUN / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")


def write_teacher_doc(stories):
    L = ["# Feedback from the new system (round S0) on 20 student stories", "",
         "This document shows the complete feedback the new feedback system gives on 20 of the graded student",
         "retellings (10 of 孟母三迁, 10 of 神农尝百草). Each story is split into three scenes, the way the app",
         "gives feedback scene by scene; after the last scene comes the check on the story's content.", "",
         "Round S0 uses only the teacher's original materials: her corrections on the graded samples, the model",
         "stories, her required-scene lists, and her coherence rules. None of her later comments on earlier AI",
         "feedback has been used yet. Her corrections of these 20 stories were NOT available to the system; they",
         "are used only to measure it.", "",
         "Per scene the feedback has four parts:", "",
         "- **Corrections**, grouped as Grammar, Vocabulary, Coherence (reference; 了/着/在; connectors), Content.",
         "  Items marked *(suggestion)* are less certain and are worded as a possible improvement.",
         "  [∅ → X] means X is added; [X → (delete)] means X is removed; ⟦X⟧ is a comment on X.",
         "- **Vocabulary suggestions**: words used correctly, with richer alternatives.",
         "- **Expressiveness**: ideas for going beyond recounting events (feelings, speech, detail).",
         "- **Encouragement**.", "",
         "Her ratings per story go in `S0_story_ratings.csv`; comments can also be written directly into this",
         "document.", ""]
    for s in stories:
        L += ["---", "", f"## {s['sample_id']}", ""]
        for sc in s["scenes"]:
            L += [f"### Scene {sc['scene']}", "", f"> {sc['text']}", "", *render_scene(sc["feedback"]), ""]
        L += ["### Content & completeness (after the whole story)", "",
              *([f"- {c}" for c in s["content"]] or ["- Every required scene is told."]), ""]
    TEACHER_DOC.write_text("\n".join(L) + "\n", encoding="utf-8")


def write_ratings(stories):
    cols = ["story", "CORRECTIONS (1-5)", "VOCABULARY_SUGGESTIONS (1-5)", "EXPRESSIVENESS (1-5)", "ENCOURAGEMENT (1-5)",
            "CONTENT_CHECK (1-5)", "OVERALL (1-5)", "TEACHER_NOTE"]
    kept = {}
    if RATINGS.exists():
        with open(RATINGS, encoding="utf-8-sig", newline="") as fh:
            kept = {r["story"]: r for r in csv.DictReader(fh)}
    with open(RATINGS, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for s in stories:
            k = kept.get(s["sample_id"], {})
            w.writerow([s["sample_id"], *[k.get(c, "") for c in cols[1:]]])


if __name__ == "__main__":
    main()
