#!/usr/bin/env python3
"""Pick the held-out test samples and freeze them into eval/test_set.json.

Held-out samples are removed from the retrieval snapshot (make_snapshot.py), so
the model never sees their own corrections; the teacher's corrections and
content flags for them become the gold reference each stage is scored against.

Selection (deterministic): 孟母 and 神农 samples only -- Pear samples are left
out because their AI critiques are part of the S1 guardrail cards. Eligible
samples have 8-14 sentences, at least 5 teacher corrections and at least one
"Miss ... scene" flag; N per story are taken evenly spaced by sample number.
Each sample is split into 3 contiguous scenes of whole sentences, since the app
gives feedback scene by scene.

Run once; afterwards the file is the fixed test set (re-running overwrites it).
    python eval/make_test_set.py [--per-story 3]
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPELINE = ROOT / "chinese_writing_rag_pipeline"
sys.path.insert(0, str(PIPELINE / "scripts"))
from tagging import split_correction  # noqa: E402

STORIES = ["mengmu_san_qian", "shennong_chang_baicao"]
N_SCENES = 3
SENTENCE = re.compile(r"[^。！？!?]+[。！？!?]*[”」\"]?")


def sentences(text):
    return [s.strip() for s in SENTENCE.findall(text) if s.strip()]


def split_scenes(sents, n):
    """n contiguous groups of whole sentences, as equal in length as possible."""
    total = sum(len(s) for s in sents)
    scenes, cur, done = [], [], 0
    for i, s in enumerate(sents):
        cur.append(s)
        done += len(s)
        left_sents, left_scenes = len(sents) - i - 1, n - len(scenes) - 1
        if left_scenes and (done >= total * (len(scenes) + 1) / n or left_sents == left_scenes):
            scenes.append("".join(cur))
            cur = []
    scenes.append("".join(cur))
    return [s for s in scenes if s]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-story", type=int, default=3)
    args = ap.parse_args()

    corpus = json.load(open(PIPELINE / "extracted/basic_corpus.json", encoding="utf-8"))
    rules = json.load(open(PIPELINE / "raw/correction_rules.json", encoding="utf-8"))["rules"]

    picked = []
    for story in STORIES:
        eligible = [
            s for s in corpus["samples"]
            if s["story_id"] == story
            and 8 <= len(sentences(s["raw_text"])) <= 14
            and len(s["teacher_correction_items"]) >= 5
            and any(f.startswith("Miss") for f in s["content_flags"])
        ]
        eligible.sort(key=lambda s: int(s["sample_num"]))
        step = len(eligible) / args.per_story
        picked += [eligible[int(i * step + step / 2)] for i in range(args.per_story)]

    samples = []
    for s in picked:
        gold = []
        for raw in s["teacher_correction_items"]:
            sp = split_correction(raw)
            gold.append({"text": raw, "original_span": sp["original_span"],
                         "corrected_span": sp["corrected_span"], "explanation": sp["explanation"],
                         "rules": rules.get(raw, [])})
        samples.append({
            "sample_id": s["sample_id"],
            "story_id": s["story_id"],
            "raw_text": s["raw_text"],
            "scenes": split_scenes(sentences(s["raw_text"]), N_SCENES),
            "gold": {"corrections": gold, "content_flags": s["content_flags"]},
        })

    out = {
        "_about": "Held-out test samples for the stage evaluation (see eval/README.md). "
                  "Excluded from every retrieval snapshot; gold = the teacher's own corrections "
                  "and content flags for each sample.",
        "samples": samples,
    }
    path = ROOT / "eval/test_set.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    for s in samples:
        print(f"{s['sample_id']}: {len(s['scenes'])} scenes, "
              f"{len(s['gold']['corrections'])} gold corrections, {len(s['gold']['content_flags'])} content flags")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
