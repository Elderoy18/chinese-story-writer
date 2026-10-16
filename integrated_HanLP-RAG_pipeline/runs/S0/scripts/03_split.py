#!/usr/bin/env python3
"""Step 3 -- set aside the test samples, before anything is built from the data.

    data/02_corpus/corpus.json  ->  data/03_split/split.json
                                    reports/03_split.md

Every later step that learns from the teacher's data (rule cards, mined error
patterns, detector rules, retrieval index) reads only the TRAIN samples. The
TEST samples are used only to evaluate.

Test set (approach b): TEST_PER_STORY samples per graded story, always
including the 6 samples of the first pipeline's test set, so results on those
6 can still be compared with the S0-S6 runs. The rest are taken evenly spaced
by sample number among the eligible samples (at least MIN_FEEDBACK feedback
lines, so there is something to find). The Pear Story (4 samples, a different
task) stays in train.

Each test sample is also split into N_SCENES contiguous scenes of whole
sentences of about equal length, since the app gives feedback scene by scene.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
OUT = ROOT / "data" / "03_split" / "split.json"
REPORT = ROOT / "reports" / "03_split.md"

TEST_STORIES = ["mengmu_san_qian", "shennong_chang_baicao"]
TEST_PER_STORY = 10
MIN_FEEDBACK = 3
N_SCENES = 3
# The first pipeline's test set (eval/test_set.json), kept for comparison.
FIRST_PIPELINE_TEST = [
    "mengmu_samples#10", "mengmu_samples#32", "mengmu_samples#45",
    "shennong_samples#8", "shennong_samples#19", "shennong_samples#33",
]


def evenly_spaced(items, n):
    if n <= 0 or not items:
        return []
    if n >= len(items):
        return list(items)
    step = len(items) / n
    return [items[int(step * i + step / 2)] for i in range(n)]


def split_scenes(sentences, n):
    """Contiguous groups of whole sentences, about equal in characters.
    Returns [{scene, sentence_ids, start, end}]."""
    total = sum(len(s["text"]) for s in sentences)
    scenes, cur, done = [], [], 0
    for i, s in enumerate(sentences):
        cur.append(s)
        done += len(s["text"])
        left_sents, left_scenes = len(sentences) - i - 1, n - len(scenes) - 1
        if left_scenes and (done >= total * (len(scenes) + 1) / n or left_sents == left_scenes):
            scenes.append(cur)
            cur = []
    if cur:
        scenes.append(cur)
    return [{"scene": k + 1, "sentence_ids": [s["sid"] for s in sc], "start": sc[0]["start"], "end": sc[-1]["end"]}
            for k, sc in enumerate(scenes)]


def main():
    corpus = json.load(open(CORPUS, encoding="utf-8"))
    samples = corpus["samples"]
    by_id = {s["sample_id"]: s for s in samples}
    missing = [i for i in FIRST_PIPELINE_TEST if i not in by_id]
    if missing:
        raise SystemExit(f"First-pipeline test samples not in the corpus: {missing}")

    test = []
    for story in TEST_STORIES:
        pool = [s for s in samples if s["story_id"] == story]
        fixed = [s for s in pool if s["sample_id"] in FIRST_PIPELINE_TEST]
        eligible = [s for s in pool if s not in fixed and len(s["feedback"]) >= MIN_FEEDBACK]
        test += fixed + evenly_spaced(eligible, TEST_PER_STORY - len(fixed))
    test_ids = {s["sample_id"] for s in test}
    train = [s for s in samples if s["sample_id"] not in test_ids]

    out = {
        "about": "Test samples are held out of every step that learns from the teacher's data. scenes: the test sample split as the app would see it.",
        "test": [{
            "sample_id": s["sample_id"],
            "story_id": s["story_id"],
            "first_pipeline_test": s["sample_id"] in FIRST_PIPELINE_TEST,
            "scenes": split_scenes(s["sentences"], N_SCENES),
        } for s in sorted(test, key=lambda s: (s["story_id"] != TEST_STORIES[0], s["sample_num"]))],
        "train": [s["sample_id"] for s in train],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    write_report(out, by_id, train)
    print(f"test {len(out['test'])}, train {len(train)} -> {OUT.relative_to(ROOT)}")
    print(f"Report: {REPORT.relative_to(ROOT)}")


def stats(rows):
    n = len(rows) or 1
    fb = sum(len(s["feedback"]) for s in rows)
    return (len(rows), round(sum(len(s["text"]) for s in rows) / n), round(fb / n, 1),
            round(sum(len(s["text"]) for s in rows) / max(fb, 1), 1),
            sum(1 for s in rows if any(f["type"] == "miss_scene" for f in s["content_flags"])))


def write_report(out, by_id, train):
    test = [by_id[t["sample_id"]] for t in out["test"]]
    L = ["# Step 3 report: test / train split", "",
         f"{TEST_PER_STORY} test samples per story ({', '.join(TEST_STORIES)}), including the first pipeline's 6.",
         "Everything else -- including all Pear Story samples -- is train.", "",
         "## Are test and train alike?", "",
         "| Story | Set | Samples | Avg characters | Avg feedback lines | Characters per feedback line | With a missing-scene flag |",
         "|---|---|---|---|---|---|---|"]
    for story in TEST_STORIES:
        for name, rows in (("test", [s for s in test if s["story_id"] == story]), ("train", [s for s in train if s["story_id"] == story])):
            L.append(f"| {story} | {name} | " + " | ".join(str(x) for x in stats(rows)) + " |")
    L += ["", "(Characters per feedback line is a rough measure of how error-dense a story is: lower = more errors.)", "",
          "## Test samples", "",
          "| Sample | In first pipeline's test | Feedback lines | Scenes (characters) |", "|---|---|---|---|"]
    for t in out["test"]:
        s = by_id[t["sample_id"]]
        sizes = ", ".join(str(sc["end"] - sc["start"]) for sc in t["scenes"])
        L.append(f"| {t['sample_id']} | {'yes' if t['first_pipeline_test'] else ''} | {len(s['feedback'])} | {sizes} |")
    t0 = out["test"][0]
    s0 = by_id[t0["sample_id"]]
    L += ["", f"## Scene split example: {t0['sample_id']}", ""]
    L += [f"- Scene {sc['scene']}: {s0['text'][sc['start']:sc['end']]}" for sc in t0["scenes"]]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
