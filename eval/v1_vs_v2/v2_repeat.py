#!/usr/bin/env python3
"""Repeat runs of v2 round S0 on the 6 eval stories, for the consistency check.

    chinese_writing_rag_pipeline_v2/.venv/Scripts/python eval/v1_vs_v2/v2_repeat.py 2 3
        -> eval/v1_vs_v2/v2_runs/r<k>/feedback.json   (same format as v2's runs/S0/feedback.json)

v2 S0 = flags from three finders -> one explanation call per scene (step 15) ->
enrichment per scene (step 16) -> assembled with the content check (steps 10, 17).
Two finders (GEC model, teacher patterns) are deterministic. The LLM finder
(step 6) and the content check (step 10) already have 3 runs each; S0 used run 1
of the finder and the majority-matching content run. Run k here uses finder
run k, content run k, and re-runs steps 15 and 16 with a per-run cache salt --
everything else (prompts, models, rule cards, retrieval) is v2's own code,
imported unchanged. Nothing in chinese_writing_rag_pipeline_v2 is written.
"""
import functools
import importlib.util
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
V2 = REPO / "chinese_writing_rag_pipeline_v2"
sys.path.insert(0, str(V2 / "scripts"))

STORIES = {s["sample_id"] for s in json.load(open(REPO / "eval" / "test_set.json", encoding="utf-8"))["samples"]}


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), V2 / "scripts" / name)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run(k):
    out = HERE / "v2_runs" / f"r{k}"
    out.mkdir(parents=True, exist_ok=True)
    split = json.load(open(V2 / "data" / "03_split" / "split.json", encoding="utf-8"))
    split["test"] = [t for t in split["test"] if t["sample_id"] in STORIES]
    (out / "split.json").write_text(json.dumps(split, ensure_ascii=False), encoding="utf-8")

    # step 15: finder run k, salted explanation calls, everything written under out/
    m15 = load("15_explain.py")
    m15.SPLIT = out / "split.json"
    m15.OUT = out / "15_explain"
    m15.CACHE = m15.OUT / "cache"
    m15.FEEDBACK, m15.REPORT = out / "15_feedback.md", out / "15_explain.md"
    m15.SHEET, m15.INSTRUCTIONS = out / "15_review.csv", out / "15_instructions.md"
    m15.FINDERS = {"06_find_baseline": ("AI checker", lambda c: c["run"] == k and c["sample_id"] in STORIES),
                   "08_find_gec": ("correction model", lambda c: c["sample_id"] in STORIES),
                   "13_find_teacher": ("teacher's pattern/rule", lambda c: c["sample_id"] in STORIES)}
    m15.cached_json_call = functools.partial(m15.cached_json_call, salt=f"repeat-run{k}")
    emb = "embeddings_text-embedding-3-small.jsonl"  # reuse v2's embeddings without appending to its file
    m15.CACHE.mkdir(parents=True, exist_ok=True)
    if not (m15.CACHE / emb).exists():
        shutil.copy(V2 / "data" / "15_explain" / "cache" / emb, m15.CACHE / emb)
    try:
        m15.main()
    except ValueError as e:  # its last line prints the report paths relative to v2's folder; everything is written by then
        if "subpath" not in str(e) and "relative" not in str(e):
            raise

    # step 16: enrichment over this run's items, salted
    m16 = load("16_enrich.py")
    m16.SPLIT, m16.ITEMS = out / "split.json", m15.OUT / "items.jsonl"
    m16.OUT = out / "16_enrich"
    m16.CACHE, m16.REPORT = m16.OUT / "cache", out / "16_enrich.md"
    m16.cached_json_call = functools.partial(m16.cached_json_call, salt=f"repeat-run{k}")
    m16.main()

    # step 17: assemble in S0's format, with content-check run k
    m17 = load("17_assemble_s0.py")
    texts = {s["sample_id"]: s["text"] for s in json.load(open(V2 / "data" / "02_corpus" / "corpus.json", encoding="utf-8"))["samples"]}
    items = [json.loads(l) for l in open(m15.OUT / "items.jsonl", encoding="utf-8")]
    enrich = {(r["sample_id"], r["scene"]): r for r in map(json.loads, open(m16.OUT / "enrich.jsonl", encoding="utf-8"))}
    content = {r["sample_id"]: r for r in map(json.loads, open(V2 / "data" / "10_content" / "checks_test.jsonl", encoding="utf-8"))}
    stories = []
    for t in split["test"]:
        sid = t["sample_id"]
        check = content.get(sid)
        if check:
            check = {**check, "runs": [check["runs"][k - 1]]}  # content_feedback picks from the runs it is given
        scenes = [{"scene": sc["scene"], "text": texts[sid][sc["start"]:sc["end"]],
                   "feedback": m17.scene_feedback([it for it in items if it["sample_id"] == sid and it["scene"] == sc["scene"]],
                                                  enrich.get((sid, sc["scene"])))} for sc in t["scenes"]]
        stories.append({"sample_id": sid, "story_id": t["story_id"], "scenes": scenes, "content": m17.content_feedback(check)})
    (out / "feedback.json").write_text(json.dumps(stories, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"run {k}: wrote {(out / 'feedback.json').relative_to(REPO)}")


if __name__ == "__main__":
    for k in map(int, sys.argv[1:] or ["2", "3"]):
        run(k)
