#!/usr/bin/env python3
"""Step 10 (B0) -- vocabulary suggestions, expressiveness ideas and encouragement
for every test scene.

    corpus (scenes, model stories, rubric), step 8 corrections, OpenAI
        ->  data/10_b0_enrich/enrich.jsonl    one record per scene

Basic data only: the model story of the story being retold and the teacher's
rubric definitions of vocabulary and expressiveness.

Precision first here too -- a suggestion that is not clearly better, or an idea
the scene already implies, is noise:
- vocabulary: at most 2 per scene, and none if no word clearly benefits. Only for a
  word used correctly; the alternative must be at the same everyday level (not
  formal or literary), keep the meaning, and fit the student's sentence AS IT IS.
  If it would need a different structure, the suggestion says so (shows the phrase).
- expressiveness: at most 2 per scene, at most one per clause; it must add
  something the scene does not already say or imply, be grounded in the model
  story or the student's own story (never new story facts), and its Chinese
  example must be simple and correct.
- encouragement: one or two sentences on something specific done well.
Code checks drop anything whose quoted text is not in the scene, any vocabulary
suggestion on a word inside a corrected clause, and extra ideas on one clause.
"""
import json
from concurrent.futures import ThreadPoolExecutor

from b0_lib import ROOT, load, test_scenes
from llm import api_key, cached_json_call, prompt_version

CORRECTIONS = ROOT / "data" / "08_b0_vote" / "items.jsonl"
OUT = ROOT / "data" / "10_b0_enrich"
CACHE = OUT / "cache"
MODEL = "gpt-5.6-terra"
REASONING_EFFORT = "medium"
MAX_VOCAB, MAX_IDEAS = 2, 2

SYSTEM_TEMPLATE = """You write the enrichment part of the feedback a beginner learner of Chinese gets for ONE scene of a story they are retelling. Errors are corrected elsewhere. Quality over quantity: every item must be clearly useful; an empty list is better than a weak item.

The teacher's definitions:
{definitions}

1. vocabulary_suggestions (0 to {max_vocab}): only for a word the learner used CORRECTLY, where a different everyday word would be clearly more precise or vivid in THIS sentence. Skip words that are already good.
   - word, phrase: the word and the short phrase it is in, both copied EXACTLY from the scene.
   - alternative: ONE word at the same everyday level as the learner's (never formal, literary or rare), that keeps the meaning and fits the sentence.
   - new_phrase: the learner's phrase rewritten with the alternative -- it must be correct Chinese; if the alternative needs a different structure, show it here.
   - note: one English sentence on the difference.
2. expressiveness (0 to {max_ideas}): ideas for going beyond recounting events -- a feeling or thought, a short line of speech, a detail of what something looks like. At most one idea per clause.
   - where: the learner's clause it belongs after, copied EXACTLY.
   - idea: one English sentence. It must add something the scene does not already say or clearly imply.
   - example: a short, correct Chinese sentence using simple words the learner already knows.
   Ground every idea in the model story at this point or in the learner's own story: never add events, people or facts that are not in the story.
3. encouragement: one or two English sentences naming something specific the learner did well in this scene.
English prose throughout; Chinese only for words and examples."""

SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["vocabulary_suggestions", "expressiveness", "encouragement"],
    "properties": {
        "vocabulary_suggestions": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["word", "phrase", "alternative", "new_phrase", "note"],
            "properties": {k: {"type": "string"} for k in ["word", "phrase", "alternative", "new_phrase", "note"]}}},
        "expressiveness": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["where", "idea", "example"],
            "properties": {k: {"type": "string"} for k in ["where", "idea", "example"]}}},
        "encouragement": {"type": "string"},
    },
}


def definitions(corpus):
    sec = next((s["text"] for s in corpus["rubric"] if "metric" in s["heading"].lower()), "")
    return "\n".join(l for l in sec.splitlines() if "Vocabulary" in l or "Expressiveness" in l)


def main():
    corpus, split, samples = load()
    system = SYSTEM_TEMPLATE.format(definitions=definitions(corpus), max_vocab=MAX_VOCAB, max_ideas=MAX_IDEAS)
    version = prompt_version(system, SCHEMA)
    models = {m["story_id"]: m["text"] for m in corpus["model_stories"]}
    corr = [json.loads(l) for l in open(CORRECTIONS, encoding="utf-8")]
    jobs = []
    for s, k, s0, s1, earlier in test_scenes(split, samples):
        scene = s["text"][s0:s1]
        fixed = [c["before"] for c in corr if c["sample_id"] == s["sample_id"] and c["scene"] == k]
        prev = "\n".join(f"Scene {i + 1}: {t}" for i, t in enumerate(earlier))
        user = (f"Model version of the story (for ideas only, never to copy):\n{models.get(s['story_id'], '(none)')}\n\n"
                + (f"The learner's earlier scenes:\n{prev}\n\n" if prev else "")
                + "Clauses already corrected (do not suggest vocabulary inside them):\n"
                + ("\n".join(f"- {f}" for f in fixed) or "(none)")
                + f"\n\nScene to enrich:\n{scene}")
        jobs.append((s, k, s0, s1, fixed, user))
    api_key()
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda j: cached_json_call(CACHE, MODEL, REASONING_EFFORT, system, SCHEMA, "enrich", j[5]), jobs))

    OUT.mkdir(parents=True, exist_ok=True)
    drops = {"vocabulary: text not in scene": 0, "vocabulary: inside a corrected clause": 0,
             "expressiveness: clause not in scene": 0, "expressiveness: second idea on a clause": 0}
    n_v = n_e = 0
    with open(OUT / "enrich.jsonl", "w", encoding="utf-8") as fh:
        for (s, k, s0, s1, fixed, _), (rec, _) in zip(jobs, res):
            scene, o = s["text"][s0:s1], rec["output"]
            vocab = []
            for v in o["vocabulary_suggestions"][:MAX_VOCAB]:
                if v["phrase"] not in scene or v["word"] not in v["phrase"]:
                    drops["vocabulary: text not in scene"] += 1
                elif any(v["phrase"] in f or v["word"] in f for f in fixed):
                    drops["vocabulary: inside a corrected clause"] += 1
                else:
                    vocab.append(v)
            ideas, used = [], set()
            for e in o["expressiveness"][:MAX_IDEAS]:
                where = e["where"].strip().rstrip("，。！？；：")
                if not where or where not in scene:
                    drops["expressiveness: clause not in scene"] += 1
                elif where in used:
                    drops["expressiveness: second idea on a clause"] += 1
                else:
                    used.add(where)
                    ideas.append({**e, "where": where})
            n_v += len(vocab)
            n_e += len(ideas)
            fh.write(json.dumps({"sample_id": s["sample_id"], "scene": k, "vocabulary_suggestions": vocab,
                                 "expressiveness": ideas, "encouragement": o["encouragement"]}, ensure_ascii=False) + "\n")
    json.dump({"model": MODEL, "reasoning_effort": REASONING_EFFORT, "prompt_version": version},
              open(OUT / "run_info.json", "w", encoding="utf-8"), indent=1)
    print(f"{len(jobs)} scenes: {n_v} vocabulary suggestions, {n_e} expressiveness ideas; dropped {drops}")


if __name__ == "__main__":
    main()
