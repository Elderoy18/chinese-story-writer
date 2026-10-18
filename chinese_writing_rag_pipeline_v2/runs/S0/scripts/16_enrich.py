#!/usr/bin/env python3
"""Step 16 -- the enrichment part of each scene's feedback: expressiveness
ideas, vocabulary suggestions, and encouragement.

    corpus (model stories), split, data/04_parse/parses.jsonl, data/15_explain/items.jsonl,
    raw/basic_data/Coherence reference temporality rules.md
        ->  data/16_enrich/enrich.jsonl      one scene per line
            reports/16_enrich.md             expressiveness profile + examples

    python scripts/16_enrich.py

These are not error corrections, so there is no answer key: quality is judged
by the teacher on the assembled feedback (step 17).

Her definitions (her rubric, basic data):
  Expressiveness -- going beyond basic event recounting: descriptive detail,
                    evaluative language, internal-state terms, quoted speech.
  Vocabulary     -- appropriate and accurate use, complexity/variety;
                    "vocabulary suggestions": richer vocabulary. Kept separate
                    from word-choice ERRORS, which step 15 already corrects.

Expressiveness profile (HanLP, no LLM), per scene and for the model story,
per 100 characters: descriptive words (adjectives: VA, JJ), feeling/thinking
words (觉得, 想, 高兴, 害怕 ...), and quoted speech. The gaps tell the LLM what
this scene lacks compared with the native model version of the same story.

One LLM call per scene, with: her definitions, the model story (the source of
ideas: what characters see, feel and say at this point), earlier scenes, the
profile, and the words step 15 already corrected (never suggested again).
Code checks that every quoted clause and word occurs in the scene, and drops
vocabulary suggestions on a corrected span.
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
PARSES = ROOT / "data" / "04_parse" / "parses.jsonl"
ITEMS = ROOT / "data" / "15_explain" / "items.jsonl"
RUBRIC = ROOT / "raw" / "basic_data" / "Coherence reference temporality rules.md"
OUT = ROOT / "data" / "16_enrich"
CACHE = OUT / "cache"
REPORT = ROOT / "reports" / "16_enrich.md"

MODEL = "gpt-5.6-terra"
REASONING_EFFORT = "medium"
WORKERS = 8
FEELING = {"觉得", "想", "心想", "认为", "希望", "担心", "害怕", "怕", "高兴", "开心", "快乐", "难过", "伤心", "生气", "着急",
           "吃惊", "惊讶", "失望", "满意", "喜欢", "爱", "讨厌", "感到", "感觉", "后悔", "舒服", "不舒服", "紧张", "放心", "好奇",
           "孤单", "无聊", "骄傲", "感激", "幸福", "痛苦", "疼"}

SYSTEM = """You write the enrichment part of the feedback a beginner learner of Chinese gets for ONE scene of a narrative they are retelling. Errors have already been corrected elsewhere; this part helps the learner write richer. The supervising teacher's definitions:
- Expressiveness: going beyond basic event recounting -- descriptive detail, evaluative language, a character's feelings or internal state, quoted speech.
- Vocabulary suggestions: richer vocabulary -- for words the learner used correctly but plainly.

Write three parts:
1. expressiveness: one to three concrete ideas, each tied to one spot in the CURRENT scene.
   - where: the learner's clause it belongs to, copied EXACTLY.
   - idea: one English sentence (what to add: a feeling, what a character says, a detail of how something looks).
   - example: a short Chinese example at the learner's own level -- simple words they already use.
   Draw the ideas from what the model version of the story tells at this point (what characters see, feel and say), rewritten at the learner's level -- never ask them to copy its sentences. Use the measurements to target what this scene lacks most.
2. vocabulary_suggestions: one to three words the learner used CORRECTLY but plainly.
   - word and phrase: the word and the short phrase it appears in, both copied EXACTLY from the scene.
   - alternatives: one or two words that are a small, natural step up (more precise or vivid, still common), each with an English note on the difference in meaning or tone.
   Never pick a word listed as already corrected, and never suggest the learner's word is wrong.
3. encouragement: one or two English sentences naming something specific the learner did well in this scene.
English prose throughout; Chinese only for words and examples. Keep it simple and encouraging."""

SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["expressiveness", "vocabulary_suggestions", "encouragement"],
    "properties": {
        "expressiveness": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["where", "idea", "example"],
            "properties": {"where": {"type": "string"}, "idea": {"type": "string"}, "example": {"type": "string"}}}},
        "vocabulary_suggestions": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["word", "phrase", "alternatives"],
            "properties": {"word": {"type": "string"}, "phrase": {"type": "string"},
                           "alternatives": {"type": "array", "items": {
                               "type": "object", "additionalProperties": False, "required": ["word", "note"],
                               "properties": {"word": {"type": "string"}, "note": {"type": "string"}}}}}}},
        "encouragement": {"type": "string"},
    },
}


def profile(tokens, text):
    """Per 100 characters: descriptive words, feeling/thinking words, quoted speech."""
    n = max(len(re.sub(r"\s", "", text)), 1) / 100
    desc = sum(1 for t in tokens if t["pos"] in ("VA", "JJ"))
    feel = sum(1 for t in tokens if t["text"] in FEELING)
    speech = len(re.findall(r"[“\"]|[说道问喊]：", text))
    return {"descriptive": round(desc / n, 1), "feelings": round(feel / n, 1), "speech": round(speech / n, 1)}


def main():
    api_key()
    corpus = json.load(open(CORPUS, encoding="utf-8"))
    texts = {s["sample_id"]: s["text"] for s in corpus["samples"]}
    models = {m["story_id"]: m["text"] for m in corpus["model_stories"]}
    split = json.load(open(SPLIT, encoding="utf-8"))
    units = [json.loads(l) for l in open(PARSES, encoding="utf-8")]
    items = [json.loads(l) for l in open(ITEMS, encoding="utf-8")]
    rubric = RUBRIC.read_text(encoding="utf-8")
    defs = "\n".join(l for l in rubric.splitlines() if l.startswith(("- **Vocabulary", "- **Expressiveness")))

    model_prof = {}
    for sid_story, mtext in models.items():
        toks = [t for u in units if u["kind"] == "model_sentence" and u["source"]["story_id"] == sid_story for t in u["tokens"]]
        model_prof[sid_story] = profile(toks, mtext)

    jobs = []
    for t in split["test"]:
        sid, text = t["sample_id"], texts[t["sample_id"]]
        stoks = [dict(tok, s=tok["story_start"]) for u in units if u["kind"] == "student_sentence" and u["source"]["sample_id"] == sid
                 for tok in u["tokens"]]
        for k, sc in enumerate(t["scenes"]):
            scene = text[sc["start"]:sc["end"]]
            prof = profile([x for x in stoks if sc["start"] <= x["s"] < sc["end"]], scene)
            corrected = [it for it in items if it["sample_id"] == sid and it["scene"] == sc["scene"]]
            L = [f"TEACHER'S DEFINITIONS:\n{defs}", "", f"MODEL VERSION OF THE STORY (native; source of ideas):\n{models[t['story_id']]}", ""]
            earlier = [text[x["start"]:x["end"]] for x in t["scenes"][:k]]
            if earlier:
                L.append("EARLIER SCENES (context only):\n" + "\n".join(earlier) + "\n")
            mp = model_prof[t["story_id"]]
            L += [f"CURRENT SCENE:\n{scene}", "",
                  f"MEASUREMENTS per 100 characters (this scene vs. the model story): descriptive words {prof['descriptive']} vs {mp['descriptive']}; "
                  f"feeling/thinking words {prof['feelings']} vs {mp['feelings']}; quoted speech {prof['speech']} vs {mp['speech']}", "",
                  "ALREADY CORRECTED (do not suggest these words): " + ("; ".join(sorted({it["original"] for it in corrected if it["original"]})) or "none")]
            jobs.append({"sample_id": sid, "story_id": t["story_id"], "scene": sc["scene"], "start": sc["start"], "end": sc["end"],
                         "text": scene, "profile": prof, "corrected": corrected, "user": "\n".join(L)})

    with ThreadPoolExecutor(WORKERS) as pool:
        recs = list(pool.map(lambda j: cached_json_call(CACHE, MODEL, REASONING_EFFORT, SYSTEM, SCHEMA, "enrichment", j["user"]), jobs))

    rows, usage, dropped = [], Counter(), Counter()
    for j, (rec, _) in zip(jobs, recs):
        usage.update({k: v for k, v in rec.get("usage", {}).items() if isinstance(v, int)})
        out = rec["output"]
        expr = [e for e in out["expressiveness"] if e["where"] and e["where"] in j["text"]]
        dropped["expressiveness: clause not in scene"] += len(out["expressiveness"]) - len(expr)
        vocab = []
        for v in out["vocabulary_suggestions"]:
            pos = j["text"].find(v["word"])
            if not v["word"] or pos < 0 or v["phrase"] not in j["text"]:
                dropped["vocabulary: word not in scene"] += 1
                continue
            s = j["start"] + pos
            if any(it["start"] < s + len(v["word"]) and s < max(it["end"], it["start"] + 1) for it in j["corrected"]):
                dropped["vocabulary: word already corrected"] += 1
                continue
            vocab.append(v)
        rows.append({"sample_id": j["sample_id"], "story_id": j["story_id"], "scene": j["scene"], "profile": j["profile"],
                     "expressiveness": expr, "vocabulary_suggestions": vocab, "encouragement": out["encouragement"]})

    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "enrich.jsonl", "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    (OUT / "run_info.json").write_text(json.dumps({"model": MODEL, "reasoning_effort": REASONING_EFFORT,
                                                   "prompt_version": prompt_version(SYSTEM, SCHEMA), "tokens": dict(usage)}, indent=1),
                                       encoding="utf-8")
    write_report(rows, model_prof, usage, dropped)
    print(f"{len(rows)} scenes; expressiveness ideas {sum(len(r['expressiveness']) for r in rows)}, vocabulary suggestions "
          f"{sum(len(r['vocabulary_suggestions']) for r in rows)}; dropped {dict(dropped)}; tokens {dict(usage)}")


def write_report(rows, model_prof, usage, dropped):
    avg = lambda key, rs: round(sum(r["profile"][key] for r in rs) / max(len(rs), 1), 1)
    L = ["# Step 16 report: expressiveness, vocabulary suggestions, encouragement", "",
         f"- {len(rows)} scenes; tokens {dict(usage)}; dropped by the checks: {dict(dropped) or 'none'}", "",
         "## Expressiveness profile (per 100 characters)", "",
         "| Story | Who | Descriptive words | Feeling/thinking words | Quoted speech |", "|---|---|---|---|---|"]
    for story in sorted({r["story_id"] for r in rows}):
        rs = [r for r in rows if r["story_id"] == story]
        L.append(f"| {story} | learners (test scenes) | {avg('descriptive', rs)} | {avg('feelings', rs)} | {avg('speech', rs)} |")
        mp = model_prof[story]
        L.append(f"| {story} | model story | {mp['descriptive']} | {mp['feelings']} | {mp['speech']} |")
    L += ["", "## Examples (first 6 scenes)", ""]
    for r in rows[:6]:
        L += [f"**{r['sample_id']} scene {r['scene']}**", ""]
        L += [f"- Expressiveness ({e['where']}): {e['idea']} e.g. {e['example']}" for e in r["expressiveness"]]
        L += [f"- Vocabulary: {v['word']} (“{v['phrase']}”) → " + "; ".join(f"{a['word']}: {a['note']}" for a in v["alternatives"])
              for v in r["vocabulary_suggestions"]]
        L += [f"- Encouragement: {r['encouragement']}", ""]
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
