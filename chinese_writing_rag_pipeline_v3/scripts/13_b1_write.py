#!/usr/bin/env python3
"""Step 13 (B1) -- one feedback line per error for every test scene, 3 runs.

    corpus, split, train edits (basic data only), OpenAI
        ->  data/13_b1_write/raw.jsonl      one record per scene x run
            data/13_b1_write/items.jsonl    every line that passed the checks, in scorer format

What changed from B0 (after the comparison with S6):
- One line per ERROR, as the teacher writes corrections: the student's phrase：the
  corrected phrase，explanation. The phrase is the shortest COMPLETE phrase that
  contains the error (never a fragment), and the corrected phrase fixes every
  error inside it, so it is always fully correct.
- Two categories only: Grammar and Vocab Corrections (grammar AND wrong words --
  no grammar/vocabulary boundary to get wrong), or Coherence: Reference /
  Temporality / Conjunction. A phrase is never flagged in both.
- Coherence is checked against her rubric written out in full (A/B/C below: the
  same rules as her "Coherence reference temporality rules" sheet, spelled out
  so every clause is checked against all three) -- B0 passed the rubric only in
  its shorthand and missed e.g. first mentions. Reference is narrowed to what
  her train corrections show she flags: first mention (41 corrections), a
  repeated name/pronoun inside one sentence (39), an unclear pronoun; she
  changes a repeated name to a pronoun in a new sentence only 2 times across
  655 uses of 孟子/神农, so that is never flagged (the first B1 run did, and
  26 of its 55 lines at places she did not mark were exactly that).
- Explanations state WHAT is wrong and WHY (the rule) in one or two plain English
  sentences. Her train corrections are shown as examples of what she corrects;
  her notes are shorthand, so the substance is reused, never the shorthand.
Basic data only: her train corrections and her rubric. Nothing from the feedback data.

Code checks (drop only): the phrase must occur in the scene; the correction must
differ; lines on overlapping phrases within one run keep the first. An edit that
only adds or removes 了/着/过/在/正在 is filed as Coherence: Temporality, as her
rubric does.
"""
import json
import re
from concurrent.futures import ThreadPoolExecutor

from b0_lib import ROOT, Examples, load, test_scenes
from llm import api_key, cached_json_call, prompt_version

OUT = ROOT / "data" / "13_b1_write"
CACHE = OUT / "cache"
MODEL = "gpt-5.6-terra"
REASONING_EFFORT = "medium"
N_RUNS = 3

SYSTEM = """You give error feedback on ONE scene of a short Chinese story written by a beginner learner of Chinese. Earlier scenes, if given, are context only (e.g. to tell whether a character was already introduced); give feedback only on the scene to review.

PRECISION FIRST. A wrong correction, or a correction of something that is not an error, is much worse than a missed error. Flag only definite errors a Chinese teacher would correct in a beginner's story -- not style preferences or merely different wordings. If unsure, leave it out. But do check every sentence: do not stop after a few.

Return one item per error:
- section: "grammar_vocab" for grammar errors AND wrong or unsuitable words (word order, structure, particles other than aspect markers, measure words, collocations, wrong word choice); "coherence" for how sentences connect (the A/B/C rules below).
- coherence_type: reference | temporality | conjunction for coherence; "" otherwise.
- original: the student's words, copied EXACTLY, character for character: the shortest COMPLETE phrase that contains the error -- a phrase a reader understands on its own (e.g. 喜欢玩在墓地里, 他每天在文学家的房子上学), never a cut-off fragment.
- corrected: that phrase with the error fixed. If the phrase contains another error too, fix it here as well (and do not report it again), so the corrected phrase is completely correct, natural, and keeps the student's meaning and words wherever possible.
- explanation: one or two plain English sentences for a beginner: what is wrong and why -- the rule, said in full words (e.g. "A place phrase with 在 comes before the verb in Chinese, so say 在墓地里玩."). No shorthand or formula notation.
Never flag the same words twice. Do not report plot or story-content problems.

Coherence rules (from the supervising teacher) -- check EVERY sentence against all three:

A. REFERENCE (how characters and objects are named)
- First mention: the first time a character appears in the story, introduce them briefly with a noun phrase that says who they are (e.g. 有一个小男孩叫孟子), not only a name or a bare pronoun. Use the earlier scenes to tell whether it is really the first mention.
- Re-occurrence, same clause or sentence: use the zero form -- do not repeat the name or pronoun (孟母很生气，决定搬家, not 孟母很生气，孟母决定搬家). Flag a repeated name or pronoun inside one sentence.
- Re-occurrence, far: if much information or another character came in between, repeat the name -- a pronoun would be unclear. Flag a pronoun or vague noun (这个孩子, 别人, 那个人) whose referent is unclear.
- Re-occurrence, close, in a NEW sentence: a pronoun is natural, but repeating the name is also acceptable -- do NOT flag a name used again in a new sentence, and do not replace it with a pronoun. (The teacher almost never makes that change; it is not an error.)

B. TEMPORALITY (aspect markers)
- 了: completion -- the action is finished. 着: a durative, accompanying or static state (拿着, 坐着, 笑着说). 在/正在: an ongoing dynamic action.
- Zero particle (no 了/着/过) with: mental-state verbs (知道, 觉得, 喜欢, 想, 决定, 发现, 懂, 愿意, 记得 ...); modal verbs (想, 要, 能, 可以, 会, 需要, 应该, 得, 别, 不准 ...); routines, conditions and states (常常, 有的时候, 每天 ...); and saying verbs that introduce quoted speech.
- In a series of actions, only the last verb takes 了.
- Flag a missing 了/着/在 where one is needed, a wrong one, and an extra one where the zero particle is required.

C. CONJUNCTIONS (how events and ideas are linked)
- Cause and effect: 因为……所以……. Contrast: 虽然……但是……. Sequence: ……以后, 然后, 后来. A new event interrupting: 这时…….
- Flag: events listed as unconnected sentences where a connector is clearly needed; the wrong connector for the relation; a paired connector used incorrectly; heavy overuse of one connector.

You also see corrections the teacher made in OTHER learners' stories, in clauses similar to this scene's: they show what she treats as errors. Do not copy them unless the same error is really in this scene."""

SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["errors"],
    "properties": {"errors": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "required": ["section", "coherence_type", "original", "corrected", "explanation"],
        "properties": {"section": {"type": "string", "enum": ["grammar_vocab", "coherence"]},
                       "coherence_type": {"type": "string", "enum": ["reference", "temporality", "conjunction", ""]},
                       "original": {"type": "string"}, "corrected": {"type": "string"},
                       "explanation": {"type": "string"}}}}},
}
VERSION = prompt_version(SYSTEM, SCHEMA)
ASPECT = re.compile(r"^(了|着|过|在|正在)$")
squash = lambda s: re.sub(r"[\s，。！？、；：,.!?;:“”‘’\"'（）()…—]", "", s or "")


def user_message(scene_text, earlier, examples):
    ex = "\n".join(f"- in “{r['clause']}”: {r['original'] or '(nothing)'} → {r['corrected'] or '(deleted)'}"
                   + (f"   [her note: {r['note']}]" if r["note"] else "") for r in examples)
    prev = "\n".join(f"Scene {i + 1}: {t}" for i, t in enumerate(earlier))
    return ((f"Earlier scenes (context only):\n{prev}\n\n" if prev else "")
            + f"The teacher's corrections in other learners' similar clauses:\n{ex or '(none)'}\n\n"
            + f"Scene to review:\n{scene_text}")


def aspect_only(o, c):
    """The phrase changes only by adding or removing one aspect particle."""
    if len(c) > len(o):
        o, c = c, o
    for i in range(len(o)):
        for j in range(i + 1, min(i + 3, len(o)) + 1):
            if ASPECT.match(o[i:j]) and o[:i] + o[j:] == c:
                return True
    return False


def check(out, sample, s0, s1):
    text = sample["text"]
    kept, dropped = [], []
    for e in out.get("errors", []):
        orig = e["original"].strip().strip("，。！？；：,!?;:")
        pos = text.find(orig, s0, s1) if orig else -1
        if pos < 0:
            dropped.append((e, "phrase not in the scene"))
            continue
        if squash(e["corrected"]) == squash(orig):
            dropped.append((e, "no change"))
            continue
        item = {"start": pos, "end": pos + len(orig), "before": orig, "after": e["corrected"].strip().strip("，。！？；：,!?;:"),
                "section": e["section"], "coherence_type": e["coherence_type"] if e["section"] == "coherence" else "",
                "explanation": e["explanation"]}
        if aspect_only(squash(item["before"]), squash(item["after"])):
            item.update(section="coherence", coherence_type="temporality")
        if item["section"] == "coherence" and not item["coherence_type"]:
            dropped.append((e, "coherence without a type"))
            continue
        if any(k["start"] < item["end"] and item["start"] < k["end"] for k in kept):
            dropped.append((e, "overlaps an earlier line"))
            continue
        kept.append(item)
    return kept, dropped


def main():
    _, split, samples = load()
    examples = Examples(samples)
    jobs = []
    for s, k, s0, s1, earlier in test_scenes(split, samples):
        scene_text = s["text"][s0:s1]
        msg = user_message(scene_text, earlier, examples.for_scene(scene_text))
        for run in range(1, N_RUNS + 1):
            jobs.append((s, k, s0, s1, run, msg))
    api_key()
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda j: cached_json_call(CACHE, MODEL, REASONING_EFFORT, SYSTEM, SCHEMA, "scene_errors",
                                                     j[5], salt=f"run{j[4]}"), jobs))
    OUT.mkdir(parents=True, exist_ok=True)
    n_k = n_d = 0
    with open(OUT / "raw.jsonl", "w", encoding="utf-8") as raw, open(OUT / "items.jsonl", "w", encoding="utf-8") as items:
        for (s, k, s0, s1, run, msg), (rec, _) in zip(jobs, res):
            kept, dropped = check(rec["output"], s, s0, s1)
            raw.write(json.dumps({"sample_id": s["sample_id"], "scene": k, "run": run, "user": msg, "kept": kept,
                                  "dropped": [{"item": i, "reason": r} for i, r in dropped]}, ensure_ascii=False) + "\n")
            for it in kept:
                items.write(json.dumps({"sample_id": s["sample_id"], "scene": k, "run": run, "strength": "error",
                                        "dimension": it["section"] + (":" + it["coherence_type"] if it["coherence_type"] else ""),
                                        **it}, ensure_ascii=False) + "\n")
            n_k += len(kept)
            n_d += len(dropped)
    json.dump({"model": MODEL, "reasoning_effort": REASONING_EFFORT, "prompt_version": VERSION, "n_runs": N_RUNS},
              open(OUT / "run_info.json", "w", encoding="utf-8"), indent=1)
    print(f"{len(jobs)} calls, prompt {VERSION}: {n_k} lines kept, {n_d} dropped -> {(OUT / 'items.jsonl').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
