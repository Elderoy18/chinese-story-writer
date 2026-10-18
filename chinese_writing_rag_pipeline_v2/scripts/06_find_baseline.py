#!/usr/bin/env python3
"""Step 6 -- the baseline finder: an LLM lists the errors in each test scene,
with NO teacher material (no rules, examples, notes or corrections).

    data/02_corpus/corpus.json, data/03_split/split.json
        ->  data/06_find_baseline/candidates.jsonl   one candidate error per line
            data/06_find_baseline/cache/             one LLM response per scene per run

    python scripts/06_find_baseline.py

The app gives feedback scene by scene, so each test story is fed as its 3
scenes (step 3), each with the earlier scenes as context. Every scene is run
N_RUNS times: the runs show how much the finder varies, and their union shows
how much recall repeated runs can buy.

The finder returns text, not positions (the characters that are wrong plus a
few characters either side), which code locates in the scene -- the same
convention as the answer key (step 5), so the two can be compared by position
in step 7.

Standard library only; needs OPENAI_API_KEY.
"""
import json
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from llm import api_key, cached_json_call, prompt_version

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
SPLIT = ROOT / "data" / "03_split" / "split.json"
OUT_DIR = ROOT / "data" / "06_find_baseline"
CACHE = OUT_DIR / "cache"

MODEL = "gpt-5.6-terra"
REASONING_EFFORT = "medium"
N_RUNS = 3
WORKERS = 8

SYSTEM = """You are an experienced teacher of Chinese as a foreign language. A beginner-to-intermediate learner is writing a short narrative -- a retelling of a traditional Chinese story -- one scene at a time. Find every error in the CURRENT scene.

An error is anything a native-speaking Chinese teacher would correct: grammar and word order, aspect particles (了/着/过), measure words, a wrong or unnatural word, missing or extra words, how sentences connect (a pronoun or name that is unclear or wrongly chosen, a missing or wrong connector), and wrong characters. Do not flag punctuation, and do not flag something only because a more elegant wording exists.

Be exhaustive: check every clause. If you are unsure whether something is an error, include it with confidence "low" -- a later step checks every item.

For each error:
- original: the learner characters that are wrong, copied EXACTLY from the current scene; "" if something is missing.
- corrected: the minimal correction of those characters ("" to delete them).
- before / after: up to 4 learner characters immediately before and after "original", copied EXACTLY, so the error can be located. Use "" only at the start or end of the scene.
- type: grammar | word_choice | reference | aspect | connector | other
- confidence: high | low
- why: a short English phrase.

One item per error: if a clause has two separate problems, list them separately, and correct only the characters that must change.
Earlier scenes are context only (e.g. to know whether a character has already been introduced): list errors in the current scene only.

EXAMPLE (another learner)
current scene: 他昨天去商店，买三本书。他很喜欢看书了。
errors:
{"original":"","corrected":"了","before":"商店，买","after":"三本书。","type":"aspect","confidence":"high","why":"completed action needs 了"}
{"original":"了","corrected":"","before":"喜欢看书","after":"。","type":"aspect","confidence":"high","why":"no 了 after a lasting state"}"""

SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["errors"],
    "properties": {"errors": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "required": ["original", "corrected", "before", "after", "type", "confidence", "why"],
        "properties": {
            "original": {"type": "string"}, "corrected": {"type": "string"},
            "before": {"type": "string"}, "after": {"type": "string"},
            "type": {"type": "string", "enum": ["grammar", "word_choice", "reference", "aspect", "connector", "other"]},
            "confidence": {"type": "string", "enum": ["high", "low"]},
            "why": {"type": "string"},
        }}}},
}
PROMPT_VERSION = prompt_version(SYSTEM, SCHEMA)


def scene_input(text, scenes, k):
    earlier = [text[s["start"]:s["end"]] for s in scenes[:k]]
    lines = []
    if earlier:
        lines.append("earlier scenes (context only):\n" + "\n".join(f"scene {i + 1}: {t}" for i, t in enumerate(earlier)))
    lines.append(f"current scene: {text[scenes[k]['start']:scenes[k]['end']]}")
    return "\n\n".join(lines)


def place(text, r0, r1, e):
    """Story position of a candidate from its text + context; None if not found."""
    orig, b, a = e["original"], e["before"], e["after"]
    for pre, post in ((b, a), (b, ""), ("", a), ("", "")):
        needle = pre + orig + post
        if not needle:
            continue
        hits = [m.start() for m in re.finditer(re.escape(needle), text[r0:r1])]
        if len(hits) == 1 or (hits and pre and post):
            st = r0 + hits[0] + len(pre)
            return st, st + len(orig)
    return None


def main():
    corpus = json.load(open(CORPUS, encoding="utf-8"))
    split = json.load(open(SPLIT, encoding="utf-8"))
    texts = {s["sample_id"]: s["text"] for s in corpus["samples"]}

    jobs = []
    for t in split["test"]:
        text = texts[t["sample_id"]]
        for k, sc in enumerate(t["scenes"]):
            user = scene_input(text, t["scenes"], k)
            for run in range(1, N_RUNS + 1):
                jobs.append((t["sample_id"], t["story_id"], sc, user, run))

    api_key()
    print(f"{len(jobs)} calls ({len(jobs) // N_RUNS} scenes x {N_RUNS} runs), model {MODEL} ({REASONING_EFFORT}), prompt {PROMPT_VERSION}")
    with ThreadPoolExecutor(WORKERS) as pool:
        results = list(pool.map(lambda j: cached_json_call(CACHE, MODEL, REASONING_EFFORT, SYSTEM, SCHEMA, "errors",
                                                          j[3], salt=f"run{j[4]}"), jobs))

    rows, usage, unplaced = [], Counter(), 0
    for (sid, story, sc, _, run), (rec, _) in zip(jobs, results):
        usage.update({k: v for k, v in rec.get("usage", {}).items() if isinstance(v, int)})
        text = texts[sid]
        for m, e in enumerate(rec["output"]["errors"]):
            pos = place(text, sc["start"], sc["end"], e)
            unplaced += pos is None
            op = "insert" if not e["original"] else "delete" if not e["corrected"] else "replace"
            rows.append({"cand_id": f"{sid}/scene{sc['scene']}/run{run}/c{m}", "sample_id": sid, "story_id": story,
                         "scene": sc["scene"], "run": run, "op": op,
                         "start": pos[0] if pos else None, "end": pos[1] if pos else None,
                         **{k: e[k] for k in ("original", "corrected", "before", "after", "type", "confidence", "why")}})

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    meta = {"model": MODEL, "reasoning_effort": REASONING_EFFORT, "prompt_version": PROMPT_VERSION,
            "n_runs": N_RUNS, "system_prompt": SYSTEM, "tokens": dict(usage)}
    (OUT_DIR / "run_info.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(OUT_DIR / "candidates.jsonl", "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(rows)} candidates ({unplaced} could not be located) -> data/06_find_baseline/candidates.jsonl")
    print(f"tokens {dict(usage)}")


if __name__ == "__main__":
    main()
