#!/usr/bin/env python3
"""Step 9 (B0) -- an independent check of every voted correction; drop when unsure.

    data/08_b0_vote/items.jsonl, OpenAI  ->  data/09_b0_verify/items.jsonl   (run = "verified")
                                             data/09_b0_verify/decisions.jsonl

One call per scene sees the scene and its voted corrections, and for each one
answers three questions:
  1. Is the student's clause DEFINITELY wrong (not a style preference)?
  2. Is the corrected clause right: grammatical, natural, keeps the meaning, and
     fixes every error in the clause?
  3. Is the dimension right (grammar / vocabulary / coherence: reference,
     temporality, connectors)?
A correction is kept only if 1 and 2 are both clearly yes. The checker may move
an item to the right dimension (3), but it never changes a correction or adds
one -- so this step can only remove or re-file, never add.
"""
import json
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

from b0_lib import COHERENCE_TYPES, DIMENSIONS, ROOT, load
from llm import api_key, cached_json_call, prompt_version

IN = ROOT / "data" / "08_b0_vote" / "items.jsonl"
SPLIT_SCENES = None
OUT = ROOT / "data" / "09_b0_verify"
CACHE = OUT / "cache"
MODEL = "gpt-5.6-terra"
REASONING_EFFORT = "medium"

SYSTEM = """You are checking corrections that an automatic system made to a beginner learner's Chinese story, before a teacher sees them. A wrong correction, or a correction of something that is not wrong, is much worse than a missed error, so be strict: when in doubt, reject.

For each numbered correction answer:
- is_error: "yes" only if the student's clause is definitely wrong in Chinese (a teacher would mark it); "no" if it is acceptable, merely less elegant, or a matter of style; "unsure" otherwise.
- correction_ok: "yes" only if the corrected clause is grammatical, natural, keeps the student's meaning, and contains no remaining error; "no" or "unsure" otherwise.
- dimension / coherence_type: the right category for the main error -- grammar (structure, word order, particles other than aspect, measure words), vocabulary (a wrong word), or coherence: reference (naming characters/objects: first mention, pronoun, zero form, repeated name), temporality (aspect: 了 / 着 / 在 / 正在 / zero particle), connectors (linking clauses and events). coherence_type is "" unless the dimension is coherence.
- reason: one short English sentence."""

SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["checks"],
    "properties": {"checks": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "required": ["n", "is_error", "correction_ok", "dimension", "coherence_type", "reason"],
        "properties": {"n": {"type": "integer"},
                       "is_error": {"type": "string", "enum": ["yes", "no", "unsure"]},
                       "correction_ok": {"type": "string", "enum": ["yes", "no", "unsure"]},
                       "dimension": {"type": "string", "enum": DIMENSIONS},
                       "coherence_type": {"type": "string", "enum": COHERENCE_TYPES + [""]},
                       "reason": {"type": "string"}}}}},
}
VERSION = prompt_version(SYSTEM, SCHEMA)


def main():
    _, split, samples = load()
    items = [json.loads(l) for l in open(IN, encoding="utf-8")]
    scene_span = {(t["sample_id"], k + 1): (sc["start"], sc["end"]) for t in split["test"] for k, sc in enumerate(t["scenes"])}
    by_scene = defaultdict(list)
    for it in items:
        by_scene[(it["sample_id"], it["scene"])].append(it)
    jobs = []
    for (sid, k), its in sorted(by_scene.items()):
        s0, s1 = scene_span[(sid, k)]
        lines = "\n".join(f"{n}. {it['before']}  →  {it['after']}   [{it['dimension']}"
                          + (f": {it['coherence_type']}" if it["coherence_type"] else "") + "]"
                          for n, it in enumerate(its, 1))
        jobs.append(((sid, k), its, f"Scene:\n{samples[sid]['text'][s0:s1]}\n\nCorrections to check:\n{lines}"))
    api_key()
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda j: cached_json_call(CACHE, MODEL, REASONING_EFFORT, SYSTEM, SCHEMA, "verify", j[2]), jobs))

    OUT.mkdir(parents=True, exist_ok=True)
    kept, outcome = [], Counter()
    with open(OUT / "decisions.jsonl", "w", encoding="utf-8") as dec:
        for (key, its, _), (rec, _) in zip(jobs, res):
            checks = {c["n"]: c for c in rec["output"]["checks"]}
            for n, it in enumerate(its, 1):
                c = checks.get(n)
                keep = bool(c) and c["is_error"] == "yes" and c["correction_ok"] == "yes"
                refiled = bool(c) and (c["dimension"], c["coherence_type"]) != (it["dimension"], it["coherence_type"])
                outcome["kept" if keep else ("no check returned" if not c else
                        "not an error" if c["is_error"] == "no" else "correction wrong" if c["correction_ok"] == "no" else "unsure")] += 1
                dec.write(json.dumps({"sample_id": it["sample_id"], "scene": it["scene"], "before": it["before"],
                                      "after": it["after"], "check": c, "kept": keep}, ensure_ascii=False) + "\n")
                if keep:
                    new = {**it, "run": "verified"}
                    if refiled:
                        new.update(dimension=c["dimension"], coherence_type=c["coherence_type"] if c["dimension"] == "coherence" else "",
                                   refiled_from=f"{it['dimension']}:{it['coherence_type']}")
                    kept.append(new)
    with open(OUT / "items.jsonl", "w", encoding="utf-8") as fh:
        for it in kept:
            fh.write(json.dumps(it, ensure_ascii=False) + "\n")
    json.dump({"model": MODEL, "reasoning_effort": REASONING_EFFORT, "prompt_version": VERSION},
              open(OUT / "run_info.json", "w", encoding="utf-8"), indent=1)
    print(f"{len(items)} voted items in {len(jobs)} scenes: {dict(outcome)}; "
          f"{sum(1 for k in kept if 'refiled_from' in k)} re-filed -> {(OUT / 'items.jsonl').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
