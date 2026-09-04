# Hierarchical RAG for Chinese-Writing Feedback — Design Doc

## 1. What's in the source documents

Five Word documents, three genuinely different data types:

| File | Type | Content |
|---|---|---|
| `4 stories model story.docx` | **model** | 4 near-perfect exemplar stories (神农尝百草, 孟母三迁, 嫦娥奔月, 张骞出使西域). No feedback — these are the target quality bar. |
| `孟母 samples with Teacher feedback.docx` | **teacher_only** | 51 student attempts at 孟母三迁, each with line-by-line teacher corrections + content-coverage notes ("Miss N scene(s): ..."). No AI feedback here. |
| `神农 samples with Teacher feedback.docx` | **teacher_only** | 52 student attempts at 神农尝百草, same structure. |
| `Student_Examples_Corrections.docx` | **ai_reviewed** | 3 student pear-story attempts, each with teacher feedback *and* AI feedback *and* the teacher's own critique ("My comment") of every AI feedback item. |
| `Pear_Story_Corrections.docx` | **ai_reviewed** | 1 longer, 3-scene creative pear-story narrative, same triple structure. |

Parsing these five files programmatically (`scripts/parse_corpus.py`) produced:

- 913 atomic teacher correction items (original span → corrected span, why)
- 67 AI feedback items, **all 67** paired with the teacher's "My comment" critique
- 97 content-coverage flags (missing plot scenes, wrong information, coherence problems)
- 4 model stories

This is real signal, not filler: it's simultaneously (a) a large bank of gold-standard grammar corrections, (b) a rare *contrastive* dataset showing exactly where and how an LLM's feedback goes wrong, and (c) an implicit, teacher-authored checklist of what a complete 孟母三迁 / 神农尝百草 retelling has to contain.

## 2. Why hierarchical (not flat) chunking

A flat "one chunk per paragraph" RAG store would bury the atomic pedagogical unit — a single original→corrected→why triple — inside long paragraphs mixing several unrelated corrections, and would give no way to retrieve "the general rule" separately from "one instance of it." The corpus itself is naturally a tree, so the chunking follows it, with a second, cross-cutting index layered on top:

```
story_prompt (6: one per writing task)
 ├── model_story (4)                         -- the target/reference text
 └── sample (109: one per student attempt)   -- parent for everything below
      ├── correction_item (913)              -- atomic: span, fix, why, grammar_tags
      ├── ai_feedback_item (67)              -- atomic: AI's claim + teacher's verdict
      └── content_flag (97)                  -- missing scene / wrong info / coherence

rule_card (31)       -- cross-cutting: all correction_items sharing a grammar_tag,
                         aggregated into one "how to explain this rule" card with
                         examples pulled from across every sample and every doc
ai_error_card (12)    -- cross-cutting: all ai_feedback_items sharing an eval_tag
                         (the 5 documented AI failure modes), aggregated into a
                         calibration card
```

Every chunk is a flat record — `{chunk_id, chunk_type, text, metadata}` — in one collection, filterable by `chunk_type`, `story_id`, `grammar_tags`, `eval_tags`, `doc_type`. The tree structure lives in `metadata.parent_id`, enabling **small-to-big retrieval**: search finds a precise `correction_item`, then the retriever can expand to its parent `sample` for full context when the generator needs to see the whole original story (demonstrated in `local_demo.py`, Demo 4).

This gives the feedback-generation pipeline four independent ways to pull exactly what it needs for a new student essay:
1. **By content similarity** — "here's a new sentence with error X, show me similar corrected examples" → `correction_item` search.
2. **By rule** — "explain the 了-completion rule with examples" → `rule_card` lookup, one clean card instead of re-deriving the explanation each time and risking an inconsistent one.
3. **By story** — "what does a complete 孟母三迁 retelling need to contain?" → `story_prompt` anchor card, which carries an auto-derived scene checklist (see §4).
4. **By failure mode** — "make sure the generator doesn't repeat these specific AI mistakes" → `ai_error_card`, injected as guardrails regardless of lexical match to the current story (see §5).

## 3. Tagging layer

Two keyword/regex taggers (`scripts/tagging.py`) run over the raw teacher text to produce the `grammar_tags` and `eval_tags` metadata that the cross-cutting cards are built from:

- **`tag_grammar_text`** — 29 grammar/discourse tags (aspect markers 了/着/过, 把/被 constructions, measure words, directional complements, etc.), matched against the actual English rule-shorthand this teacher consistently writes (e.g. "了completed", "direction complement", "在+Place"). Coverage: ~32% of the 913 correction items match at least one named rule; the rest are still fully indexed (raw text + embedding), just without a rule-card link — many are one-off content/semantic fixes that don't reduce to a named grammar point, and that's expected, not a parsing gap.
- **`tag_ai_eval_text`** — 11 tags directly modeling the 5 issues described: `missed_error`, `incorrect_correction`, `correct_fix_wrong_or_missing_explanation`, `false_positive_unneeded_correction`, `disfluency_false_positive`, `misleading_no_error_framing`, `misdirected_feedback`, `miscategorized_error_type`, `grammatical_but_semantically_off`, `disputed_rule_claim`, `validated_correct`. Coverage: 54/67 (81%) of "My comment" critiques match at least one tag; 13 fall to `unclassified` and are worth a manual pass.

**These are heuristic, not learned, classifiers** — deliberately, so they're auditable and cheap to re-run as the corpus grows. They should be spot-checked periodically rather than trusted blindly; `docs/demo_output.txt` and the tag-coverage numbers above are the honest baseline to compare future edits against.

## 4. Content-coverage checklist (auto-derived, not hand-authored)

Rather than hand-writing "what scenes does 孟母三迁 need," the pipeline derives it directly from the teacher's own 89 "Miss N scene(s)" annotations across the 51+52 reviewed samples, deduplicating near-identical phrasings and counting frequency:

```
孟母 moved to the neighborhood near the market, 孟子 imitated how to buy and sell   (flagged missing in 41/51 samples)
孟母 moved from the market to the neighborhood near a school, 孟子 started to study   (flagged missing in 30/51 samples)
孟母 decided to move away from the graveyard because 孟子 imitated offering sacrifices (flagged missing in 23/51 samples)
孟子 becomes a famous philosopher                                                     (flagged missing in 4/51 samples)
```

This is grounded, frequency-ranked, and free — no separate curation pass needed for 孟母三迁 / 神农尝百草. It's attached to each story's `story_prompt` chunk (`chunks/scene_checklists.json` has the raw form) and is what lets the generator check *content completeness*, not just grammar — directly answering "AI并不能找到...miss了很多需要改的问题" for the content dimension, where the 3 ai_reviewed samples (single stories, not batches) don't have this signal, which is exactly why only the 51/52-sample teacher-only docs support it.

The 4 model stories serve the same role for stories without a derived checklist (张骞出使西域, 嫦娥奔月, and as a qualitative reference even where a checklist exists) — full-text comparison instead of a bullet checklist.

## 5. Directly addressing the 5 issues from the teacher's notes

| Issue (teacher's Chinese notes) | How the RAG design addresses it |
|---|---|
| **1. AI misses many needed corrections** | `ai_error_card:missed_error` (8 examples) injected as a guardrail every time; system prompt explicitly instructs exhaustive scanning (see `assemble_feedback_prompt.py`). |
| **2. Feedback for disfluencies that should be cleaned away** | `ai_error_card:disfluency_false_positive` (4 examples) + explicit instruction #6 in the system prompt: the input has already been cleaned, don't flag repetition/pause artifacts. |
| **2. Missing content/detail errors ("miss one event")** | §4's auto-derived scene checklist + `content_flag` chunks as retrievable exemplars of how the teacher phrases a missing-scene note. |
| **3. "No correction needed" feedback is misleading; only flag real errors, put good writing in encouragement** | `ai_error_card:misleading_no_error_framing` + `false_positive_unneeded_correction` (12 examples, the largest calibration category) + system-prompt instruction #1. |
| **4. Feedback pointed at the wrong span (A flagged, B explained)** | `ai_error_card:misdirected_feedback` + instruction #4. Only 1 clean example matched the current tagger — worth a manual audit pass since this failure mode is likely under-tagged (see §3 caveat). |
| **5. Miscategorization (vocabulary-in-grammar, wrong-characters-that-are-really-vocabulary) + still-missing/still-wrong-explanation issues** | `ai_error_card:miscategorized_error_type` (4 examples) + `correct_fix_wrong_or_missing_explanation` (7 examples) + `incorrect_correction` (10 examples) + instruction #5. |

## 6. What's runnable now vs. what needs your environment

This sandbox has **no outbound network access to huggingface.co** (confirmed: PyPI and npm resolve, huggingface.co does not), so the actual embedding model can't be downloaded here. Two parallel tracks were built:

- **Production track** (`scripts/embed_and_index.py`, `scripts/retrieve.py`) — sentence-transformers (default: `intfloat/multilingual-e5-small`, chosen because the corpus mixes Chinese story text with English rule explanations and needs a genuinely multilingual model) + a persistent Chroma collection. Written to run as-is in a normal environment; not executed here.
- **Verification track** (`scripts/local_demo.py`) — a TF-IDF + jieba retriever, pure PyPI, no downloads, actually run in this session. It proves the chunk structure, metadata filtering, and small-to-big parent expansion all work correctly (see `docs/demo_output.txt` for the full run — 4 demos: rule retrieval for a new directional-complement error, calibration-card retrieval for a "misleading no-error" meta-query, story-scoped scene-checklist lookup, and parent expansion). TF-IDF is lexical, not semantic, so retrieval quality here is a lower bound, not the real ceiling — swap in the production track for actual deployment.

`scripts/assemble_feedback_prompt.py` ties it together: given one new, unseen student story, it retrieves the right story_prompt + model exemplar + rule_cards + ai_error_cards + nearby correction_item exemplars and assembles the full ~2,700-token prompt that would go to the feedback-generating LLM (saved to `chunks/example_assembled_prompt.txt`). This is the actual integration point for your app: call this (with the real embedding retriever swapped in) whenever a student submits a story, then send the assembled prompt to whichever LLM generates the feedback.

## 7. Running it

```bash
pip install -r requirements.txt

# 1. Parse the 5 docx files into structured JSON
python scripts/extract_json.py
python scripts/parse_corpus.py      # -> extracted/corpus.json

# 2. Build the hierarchical chunk set
python scripts/chunk_builder.py     # -> chunks/chunks.jsonl (1,239 chunks)

# 3a. Verify locally (no downloads needed)
python scripts/local_demo.py

# 3b. Real semantic index + retrieval (needs network access to huggingface.co)
python scripts/embed_and_index.py --model intfloat/multilingual-e5-small
python scripts/retrieve.py "他走去学校" --chunk-types rule_card correction_item

# 4. See the full retrieval-augmented prompt for a new submission
python scripts/assemble_feedback_prompt.py
```

## 8. Notes for the broader project (anonymized user data flow)

This corpus itself needs no anonymization — samples are already just numbers (`mengmu_samples#7`), no real student names appear anywhere in the source docs. For the live application (students submitting new stories, the LLM feedback being generated and logged), the natural extension of this same chunk schema is to write new `sample` / `correction_item` / `content_flag` records under a pseudonymous `sample_id` (e.g. a random or hashed session id rather than any student-identifying field) the same way `mengmu_samples#7` is keyed today, and to keep that id → real-identity mapping in a separate, access-controlled store rather than in the RAG/vector database at all. Happy to design that flow in detail as a follow-up — it's a separate concern from the chunking work done here (retrieval corpus vs. operational user-data store) and is worth its own pass once the feedback-generation loop itself is working.

## 9. Known limitations / next steps

- Grammar and eval tagging are heuristic (see §3); worth a manual review pass, especially for `misdirected_feedback` (likely under-tagged at just 1 hit) and the 13 `unclassified` AI-eval comments.
- `correction_item.corrected_span` / `.explanation` splitting is a best-effort heuristic (comma-before-first-ASCII-letter); `raw_text` is always preserved as ground truth and is what actually gets embedded, so this only affects the *metadata* fields, not retrieval.
- No scene checklist could be derived for 嫦娥奔月 / 张骞出使西域 or the two `ai_reviewed` pear-story docs (no "Miss scene" annotations exist for them) — full-text comparison against the model story is the fallback there; if you start collecting batches of student attempts at those prompts the same way as 孟母/神农, the checklist will emerge automatically the same way.
- The production embedding track (`embed_and_index.py`) could not be executed in this sandbox (no huggingface.co access) — please run steps 3b in your own environment before relying on it, and sanity-check retrieval quality against the TF-IDF baseline in `docs/demo_output.txt`.

## 10. App integration — what was actually wired up

The Chroma/sentence-transformers "production track" in §6 is one valid deployment. The deployed Next.js app uses a different stack it already has:

- **Embeddings:** OpenAI `text-embedding-3-small` (1536-dim), for both the corpus and the query. Set once in `scripts/embed_to_mongo.py` and `lib/rag/embed.ts` — change one, change both, re-embed.
- **Vector store:** the app's existing MongoDB Atlas database (`chinese-writer-data`), collection `rag_chunks`, one Atlas Vector Search index `rag_vec` (`docs/atlas_setup.md`). No new infrastructure, no Python at request time.
- **Feedback LLM:** OpenAI `gpt-4.1` (replaces the old Groq `llama-3.3-70b` single static prompt).

Build / deploy sequence:

```bash
# offline, one-time (and whenever the corpus changes):
python scripts/extract_json.py && python scripts/parse_corpus.py
python scripts/chunk_builder.py                      # -> chunks/chunks.jsonl

# embed + load into Atlas (reads repo-root .env.local). Node port -- no Python:
node chinese_writing_rag_pipeline/scripts/embed-to-mongo.mjs
#   (scripts/embed_to_mongo.py is the equivalent Python version; use whichever
#    runtime has working network access. chunks.jsonl is already built, so the
#    parse/chunk steps above only need re-running when the corpus changes.)

# then create the Atlas index once: docs/atlas_setup.md
```

At request time, `app/api/story/feedback/route.ts` calls `assembleFeedbackPrompt(sentence)`
(`lib/rag/`), which runs the §6 retrieval — `rule_card` ×4 + `correction_item` ×3 by
similarity, `ai_error_card` guardrails always-injected — and sends the assembled prompt
(the §5 `SYSTEM_INSTRUCTIONS` as the system message, retrieved context + student story as
the user message) to `gpt-4.1`. Retrieved `chunk_id`s are stored on the scene
(`Story.scenes[i].feedbackChunkIds`) for later analysis.

**Free-write scope:** grammar + calibration retrieval only — `story_prompt` / `model_story` /
scene-checklist cards are not pulled when `story.storyId` is empty. Retellings (§11) add them.

## 11. Retelling prompts and the content checklist (implemented)

### What determines the checklist

The scene checklist is **not hand-authored**. `chunk_builder.py::build_scene_checklists()`
derives it entirely from the teacher's own "Miss N scene(s): …" annotations across the
51 孟母 + 52 神农 graded samples:

1. For each sample, `parse_content_flag()` (`tagging.py`) picks out flags of type
   `miss_scene` and splits their body on `；`/`;` into individual missing-scene phrases.
2. Each phrase is normalized (`dedup_key`: collapse whitespace, strip trailing
   punctuation, lowercase) so near-identical phrasings from different samples collapse
   to one key.
3. Per story, count how many distinct samples flagged each normalized scene as missing.
4. The checklist = those scenes ordered by that count, each carrying `times_flagged_missing`.

For 孟母三迁 this yields exactly four beats (move away from graveyard 23×, move near
market + imitate trade 41×, move near school + start studying 30×, becomes a philosopher
4×). Stored in `chunks/scene_checklists.json` and baked into the `story_prompt:<story_id>`
chunk text. It is grounded, frequency-ranked, and free — re-running the pipeline on more
graded samples refines it with no code change. Only 孟母 / 神农 have the annotation volume
to support it; 嫦娥奔月 / 张骞 / pear stories fall back to full-text comparison against
`model_story`.

### How a retelling works in the app

1. `Story.storyId` (`lib/story.ts`) holds a corpus `story_id`; `""` = free-write.
2. `lib/retellings.ts` is the registry — a story qualifies as a retelling only if it has
   **both** an in-app video and a non-empty scene checklist. Today that's **神农尝百草
   only** (孟母三迁 has the checklist but no video; 后羿射日 has a video but no corpus
   support). Adding one = add a video row in `app/traditional-stories/page.tsx`, a
   `story_prompt` chunk with a checklist, and a `RETELLINGS` entry.
3. Entry point: the Traditional Stories quiz-results screen shows "Tell the Story in Your
   Own Words →" (only when `story.retellId` is set) → `/write-your-own?retell=<id>`.
   `write-your-own/page.tsx` resolves the id and hands `StoryWriter` a `retelling` prop;
   the hub screen and each scaffolding screen carry a "▶ Rewatch the video" link.
4. `POST /api/story` accepts `{ storyId }` (validated against `RETELLINGS`) and stores it.
5. The feedback route loads the story, passes `story.storyId` to `assembleFeedbackPrompt`.
   When set, it prepends a retelling instruction + `model_story:<id>` + `story_prompt:<id>`
   (the beat checklist) and scopes `correction_item` retrieval to `story_id: <id>`.
6. The LLM's "Content & Coverage" section then has real signal — it checks the retelling
   against the required beats and flags missing/misremembered ones, directly addressing
   issue #2 in the teacher's notes.

One story at a time: an in-progress free-write takes precedence, so `?retell=` is ignored
until that story is finished or abandoned.
