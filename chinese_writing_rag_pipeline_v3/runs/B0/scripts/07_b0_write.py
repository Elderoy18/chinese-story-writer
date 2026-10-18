#!/usr/bin/env python3
"""Step 7 (B0) -- write clause-level corrections for every test scene, 3 runs.

    corpus, split, train edits (basic data only), OpenAI
        ->  data/07_b0_write/raw.jsonl       one record per scene x run: the model's items, checked
            data/07_b0_write/items.jsonl     every item that passed the checks, in scorer format

B0 uses BASIC DATA ONLY: her graded samples (as retrieved examples), her coherence
rubric (dimension definitions). Nothing from the feedback data.

One call per scene and run reads the whole scene and returns items at the CLAUSE
level: the student's clause exactly as written, the fully corrected clause (every
error in it fixed, so the "after" is never a fragment or still wrong), and the
individual errors in it, each with a dimension (grammar / vocabulary /
coherence: reference / temporality / connectors) and a short explanation.
Precision first: only definite errors; anything uncertain is left out.

Her 6 nearest train corrections (by the student's clause) are shown as examples
of her standard; they are examples, not candidates.

Code checks, which only drop: the clause must occur in the scene; it is widened
to whole clauses; the corrected clause must differ; two items on overlapping
clauses keep the first. An aspect-particle-only change (了/着/过/在/正在) is
filed under coherence: temporality by rule, as her rubric does.
"""
import json
import re
from concurrent.futures import ThreadPoolExecutor
from difflib import SequenceMatcher

from b0_lib import COHERENCE_TYPES, DIMENSIONS, ROOT, Examples, clause_span, load, test_scenes
from llm import api_key, cached_json_call, prompt_version

OUT = ROOT / "data" / "07_b0_write"
CACHE = OUT / "cache"
MODEL = "gpt-5.6-terra"
REASONING_EFFORT = "medium"
N_RUNS = 3


def rubric_text(corpus):
    return "\n\n".join(f"{s['heading']}\n{s['text']}" for s in corpus["rubric"] if s["text"])


SYSTEM_TEMPLATE = """You correct one scene of a short Chinese story written by a beginner learner of Chinese. Another scene may come before it; judge only the scene marked for review, but use the earlier scenes as context (e.g. whether a character has been introduced).

PRECISION FIRST. A wrong correction or a correction of something that is not an error is much worse than a missed error. Flag something only if you are certain it is an error a Chinese teacher would correct in a beginner's story. Do not flag style preferences, alternatives that are merely also possible, or things that are acceptable. If unsure, leave it out.

Work clause by clause (a clause ends at ，。！？；：). For each clause that contains at least one definite error, return ONE item:
- clause: the student's clause, copied EXACTLY, character for character, without its final punctuation.
- corrected: the whole clause rewritten with EVERY error in it fixed -- it must be grammatical, natural, keep the student's meaning and words wherever possible, and contain no remaining error. Change only what is wrong.
- errors: each error in the clause separately:
  - original: the wrong words (as in the clause); correction: what replaces them ("" if they are deleted; for an insertion, original = the word before the insertion point and correction = that word plus the inserted words)
  - dimension: grammar | vocabulary | coherence
  - coherence_type: for coherence only -- reference (how characters/objects are named: first mention, pronoun, zero form, repeating the name), temporality (aspect: 了 / 着 / 在 / 正在 / zero particle), connectors (how clauses and events are linked); "" otherwise
  - explanation: one or two short English sentences giving the rule, for a beginner.
A wrong word is vocabulary; word order, structure, particles other than aspect, measure words are grammar; aspect markers, reference and connectors are coherence. Do not report plot or story-content problems.

The teacher's definitions of the dimensions:
{rubric}

You also see corrections the teacher made in OTHER learners' stories, in clauses similar to this scene's. They show what she corrects and how; do not copy them unless the same error is really in this scene."""

SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["items"],
    "properties": {"items": {"type": "array", "items": {
        "type": "object", "additionalProperties": False, "required": ["clause", "corrected", "errors"],
        "properties": {
            "clause": {"type": "string"}, "corrected": {"type": "string"},
            "errors": {"type": "array", "items": {
                "type": "object", "additionalProperties": False,
                "required": ["original", "correction", "dimension", "coherence_type", "explanation"],
                "properties": {"original": {"type": "string"}, "correction": {"type": "string"},
                               "dimension": {"type": "string", "enum": DIMENSIONS},
                               "coherence_type": {"type": "string", "enum": COHERENCE_TYPES + [""]},
                               "explanation": {"type": "string"}}}}}}}},
}

ASPECT = re.compile(r"^(了|着|过|在|正在)$")
squash = lambda s: re.sub(r"[\s，。！？、；：,.!?;:“”‘’\"'（）()…—]", "", s or "")


def user_message(scene_text, earlier, examples):
    ex = "\n".join(f"- {r['clause']}  →  {r['original'] or '∅'} → {r['corrected'] or '(delete)'}"
                   + (f"  ({r['note']})" if r["note"] else "") for r in examples)
    prev = "\n".join(f"Scene {i + 1}: {t}" for i, t in enumerate(earlier))
    return ((f"Earlier scenes (context only):\n{prev}\n\n" if prev else "")
            + f"The teacher's corrections in other learners' similar clauses:\n{ex or '(none)'}\n\n"
            + f"Scene to review:\n{scene_text}")


def aspect_only(err):
    """True if the error only adds or removes an aspect particle."""
    o, c = err["original"], err["correction"]
    if c.startswith(o):
        return bool(ASPECT.match(c[len(o):]))
    if o.startswith(c):
        return bool(ASPECT.match(o[len(c):]))
    return False


def dimension_of(errors):
    """The item's dimension: its first error's, with aspect-only changes as temporality."""
    e = errors[0]
    if aspect_only(e):
        return "coherence", "temporality"
    return e["dimension"], e["coherence_type"] if e["dimension"] == "coherence" else ""


def check(out, sample, s0, s1):
    """Model items -> located, checked items (and the reasons for anything dropped)."""
    text = sample["text"]
    kept, dropped = [], []
    for it in out.get("items", []):
        clause = it["clause"].strip().rstrip("，。！？；：,!?;:")
        pos = text.find(clause, s0, s1) if clause else -1
        if pos < 0:
            dropped.append((it, "clause not in the scene"))
            continue
        if squash(it["corrected"]) == squash(clause) or not it["errors"]:
            dropped.append((it, "no change"))
            continue
        cs, ce = clause_span(text, pos, pos + len(clause))
        ce = min(ce, s1)
        if any(k["start"] < ce and cs < k["end"] for k in kept):
            dropped.append((it, "overlaps an earlier item"))
            continue
        # keep the student's own clause text and its trailing punctuation outside the item
        cs, ce = pos, pos + len(clause)
        dim, ctype = dimension_of(it["errors"])
        kept.append({"start": cs, "end": ce, "before": clause, "after": it["corrected"].strip().rstrip("，。！？；：,!?;:"),
                     "dimension": dim, "coherence_type": ctype, "errors": it["errors"]})
    return kept, dropped


def main():
    corpus, split, samples = load()
    system = SYSTEM_TEMPLATE.format(rubric=rubric_text(corpus))
    version = prompt_version(system, SCHEMA)
    scenes = test_scenes(split, samples)
    examples = Examples(samples)
    jobs = []
    for s, k, s0, s1, earlier in scenes:
        scene_text = s["text"][s0:s1]
        msg = user_message(scene_text, earlier, examples.for_scene(scene_text))
        for run in range(1, N_RUNS + 1):
            jobs.append((s, k, s0, s1, run, msg))
    api_key()
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda j: cached_json_call(CACHE, MODEL, REASONING_EFFORT, system, SCHEMA, "scene_corrections",
                                                     j[5], salt=f"run{j[4]}"), jobs))
    OUT.mkdir(parents=True, exist_ok=True)
    n_items = n_drop = 0
    with open(OUT / "raw.jsonl", "w", encoding="utf-8") as raw, open(OUT / "items.jsonl", "w", encoding="utf-8") as items:
        for (s, k, s0, s1, run, msg), (rec, _) in zip(jobs, res):
            kept, dropped = check(rec["output"], s, s0, s1)
            raw.write(json.dumps({"sample_id": s["sample_id"], "scene": k, "run": run, "user": msg,
                                  "kept": kept, "dropped": [{"item": i, "reason": r} for i, r in dropped],
                                  "usage": rec["usage"]}, ensure_ascii=False) + "\n")
            for it in kept:
                items.write(json.dumps({"sample_id": s["sample_id"], "scene": k, "run": run, "strength": "error", **it},
                                       ensure_ascii=False) + "\n")
            n_items += len(kept)
            n_drop += len(dropped)
    json.dump({"model": MODEL, "reasoning_effort": REASONING_EFFORT, "prompt_version": version, "n_runs": N_RUNS,
               "system": system}, open(OUT / "run_info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(jobs)} calls ({len(scenes)} scenes x {N_RUNS} runs), prompt {version}: "
          f"{n_items} items kept, {n_drop} dropped by the checks -> {(OUT / 'items.jsonl').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
