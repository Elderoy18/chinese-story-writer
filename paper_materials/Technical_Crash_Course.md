# Technical Crash Course — for writing the RMAL paper

This course aims to get you to the point where you can write the methods section and defend it against a reviewer. It covers:
1. the concepts, in the order the system uses them
2. how your system maps onto them
3. what the special issue will want to see
4. the weak spots a reviewer will find

---

## Part 1 — Concepts, bottom-up

### 1.1 Large language model (LLM)
A model that, given text, predicts the next piece of text, one "token" at a time. A token is roughly a word piece; one Chinese character is often 1–2 tokens.
- Everything it "knows" is fixed in its **weights** (parameters) at training time.
- When you call it, you do not change the weights. You only change the **input** (the "context").

### 1.2 Calling a model through an API
Your app does not use a chat website. The server sends an HTTPS request to a provider and gets text back. Providers used:
- **Groq**, hosting Meta's open-weight Llama 3.3 70B (Rounds 1–2)
- **OpenAI** (Round 3)

A request contains:
- **Messages**, each with a role:
  - `system`: standing instructions ("you are a tutor; follow these rules")
  - `user`: the specific task and data
  - Rounds 1–2 put everything in one `user` message. Round 3 separates fixed rules (`system`) from per-request material (`user`). This is cleaner and easier to document.
- **Model name:** an *alias* such as `gpt-5.6-terra`. The provider can change what an alias points to, so for reproducibility report the name **and the dates of use**.
- **Sampling settings:**
  - **Temperature** controls randomness: 0 means near-deterministic, 1 is the default and more varied. You never set it in Rounds 1–2, so the provider default applied.
  - **Reasoning models** such as `gpt-5.6-terra` "think" internally before answering. They take a **reasoning effort** setting instead of temperature; yours is `low`. They do not allow temperature to be set, so outputs vary between runs and you cannot turn that off.
- **Streaming:** the response arrives word by word. This is only a display feature and has no effect on content.

### 1.3 Prompt engineering and in-context learning
Changing the model's behaviour by changing its input:
- **Zero-shot:** instructions only.
- **Few-shot:** instructions plus worked examples. Round 1 had two format examples per section.
- **Negative examples:** "don't do this". Round 2's "what not to flag" list.
- **In-context learning:** the model imitates patterns in the prompt *for that one request only*. Nothing persists. Round 2's rule list works only because it is re-sent every time.

### 1.4 Fine-tuning (what you did *not* do)
Fine-tuning means further training the model on your own examples so its **weights change**. It needs hundreds or thousands of input→ideal-output pairs, and produces a new model version.

**You never did this.** When the teacher's notes say "trained", the accurate terms are:
- Round 2: **prompt refinement**
- Round 3: **retrieval-augmented generation**

Getting this right matters because reviewers in this field are alert to it.

### 1.5 Embeddings
An embedding model (`text-embedding-3-small`) turns any text into a vector of 1,536 numbers. Texts with similar *meaning* end up with similar vectors, even across languages; this model handles mixed Chinese and English.
- **Similarity** between two vectors is measured by **cosine similarity**: 1 means the same direction, near 0 means unrelated.
- "他走去学校" and the teacher's correction "孩子一直走去张先生的树" get similar vectors because both involve 走去 + place.

### 1.6 Vector search
- All 1,239 library pieces were embedded **once, offline** (`scripts/embed-to-mongo.mjs`) and stored in MongoDB Atlas.
- At request time, the student's scene is embedded and Atlas `$vectorSearch` returns the *k* nearest pieces.
- A **filter** restricts the search to a category (`chunk_type: rule_card`) or a story (`story_id: shennong_chang_baicao`).
- This is **approximate nearest-neighbour search**. `numCandidates` controls how thoroughly it searches; yours uses 100 or more candidates.

### 1.7 Retrieval-augmented generation (RAG)
```
student text ─► embed ─► search library ─► paste top results into prompt ─► LLM ─► feedback
```
The LLM is unchanged. RAG gives it *relevant, expert-authored reference material* at the moment it writes.
- **Benefits:** grounding in the teacher's actual rule explanations, consistency, and an audit trail of what the model saw.
- **Limit:** retrieval is by *similarity*, not by *error detection*. It retrieves rules related to what the student wrote, which is not necessarily the rule the student violated. A student who omits 了 may not trigger the 了 card if nothing else in the text resembles 了 examples.

### 1.8 Chunking, and why yours is hierarchical
"Chunking" means cutting source documents into retrievable pieces. You cut along the documents' natural structure, and added two summary layers across it:
- `story_prompt` (6) → `model_story` (4) and `sample` (109) → `correction_item` (913), `ai_feedback_item` (67), `content_flag` (97)
- **Cross-cutting layers:**
  - `rule_card` (31): all corrections sharing a grammar tag, as one card
  - `ai_error_card` (12): all AI mistakes of one type, as one card

The atomic unit is one teacher correction: *original → corrected, because rule*. That unit is exactly what you want to retrieve. `parent_id` links each correction back to its full sample, which is known as "small-to-big" retrieval.

### 1.9 Heuristic tagging
`scripts/tagging.py` assigns grammar tags and AI-failure tags using **regular expressions** (keyword patterns) over the teacher's English shorthand. Examples:
- "了completed" → `aspect_le_completed`
- "no need to revise" → `false_positive_unneeded_correction`

These are **not machine learning**: they are transparent, auditable and reproducible, but imperfect.
- Coverage: 32% of corrections got a grammar tag; 81% of critiques got a failure tag.
- **In the paper:** call them "rule-based keyword coding" and report these coverage numbers.
- **If you have time:** the teacher checks a sample of tags, and you report agreement.

### 1.10 Derived content checklist
The plot-beat checklists come from counting how often the teacher wrote "Miss N scene(s): X" across the 51 and 52 samples.
- This is a **data-derived content specification**: the construct definition for "content coverage" comes from the teacher's own grading behaviour.
- That is a nice point for a *construct specification* paper.

### 1.11 The app stack, in one paragraph for a methods section
The platform is a Next.js web application hosted on Vercel. User accounts are handled by Better Auth; data lives in MongoDB Atlas. For each scene a student writes, the server:
1. embeds the text
2. retrieves reference chunks with Atlas Vector Search
3. assembles a two-part prompt
4. calls the OpenAI API
5. streams the Markdown response to the browser
6. stores the response with the IDs of the retrieved chunks

---

## Part 2 — What exactly happens on one request (Round 3)

Following [route.ts](../app/api/story/feedback/route.ts) and [assembleFeedbackPrompt.ts](../lib/rag/assembleFeedbackPrompt.ts):

1. The student clicks **End Scene**. The browser sends `{ sentence }`, the scene text only.
2. The server checks login and finds the student's in-progress story. If the story has a `storyId`, it is a retelling.
3. Four lookups run in parallel:
   - 4 nearest `rule_card`s
   - 3 nearest `correction_item`s, only from the same story if it is a retelling
   - 3 fixed `ai_error_card`s by ID
   - for a retelling, the `model_story` and `story_prompt` (checklist) cards
4. The user message is built in this order:
   1. retelling note, model story, plot beats
   2. rule cards
   3. calibration cards
   4. correction exemplars
   5. the student's text
5. The system message holds the 9 rules and the output format.
6. `gpt-5.6-terra` is called with reasoning effort `low`, streaming.
7. When the response ends, `feedback` and `feedbackChunkIds` are saved on the scene.

**Retrieval is keyed on the whole scene.** One vector represents the entire scene, so a scene with five different errors gets one blended search. Retrieving per sentence, or per detected error, would be more precise. Present this as a design choice or future work.

---

## Part 3 — Framing it for this special issue

The call asks for method-focused work on:
- construct specification
- item development
- scoring and feedback
- quality assurance
- validation strategies: prompt/model-version documentation, reliability and validity evidence, fairness, transparency and auditability, human-in-the-loop

Your strongest angle is **a documented, human-in-the-loop development method for GenAI writing feedback, with the teacher's critique converted into system components**.

### What maps to the call

| CFP theme | Your evidence |
|---|---|
| Prompt and model-version documentation | Three rounds with exact prompts (git history), models, providers and dates; Appendix A of the answers document |
| Human-in-the-loop workflow | Teacher reviews every AI item ("My comment"), and those critiques are turned into rules, calibration cards and checklists |
| Transparency and auditability | Every Round 3 feedback is stored with the IDs of the retrieved evidence, so the exact prompt can be rebuilt |
| Construct specification | The feedback categories evolved: 错别字 added, then dropped; vocabulary *suggestion* vs *correction*; content coverage added. The checklist is derived from teacher annotations |
| Quality assurance / "distortion" | A taxonomy of 11 AI feedback failure types coded from 67 teacher critiques. Plus the finding that **hand-encoding the teacher's rules into the prompt introduced new errors**: the simplified 爬上梯子 rule and the invented "missing subject" rule were reproduced by the model. A clear, publishable "GenAI can distort" example |

### What is missing for a validation paper
You currently have *qualitative, per-round teacher critique*. Reviewers will want numbers. A feasible design before 15 October:

1. **Held-out test set.** Take 10–20 learner texts that are **not in the RAG library**. New 神农 retellings are ideal.
   - If you must reuse the pear stories, rebuild the library without them first. Otherwise the calibration cards contain the answers verbatim; this is known as **data leakage**.
2. **Gold standard.** The teacher annotates each text: every error, its category and its correction.
3. **Run each round's system on each text.** Rounds 1 and 2 are still in git and can be re-run if the Groq model is still available.
4. **Score each AI item against the gold standard:**
   - **Precision:** the share of AI-flagged errors that are real errors (measures false positives)
   - **Recall:** the share of real errors the AI found (measures missed errors)
   - **Correction accuracy** and **explanation accuracy** (right rule named?)
   - **Category accuracy** (grammar, vocabulary or 错别字 correct?)
   - **Content-beat recall** for retellings
5. **Reliability:**
   - Run the same text 3–5 times per round and report agreement between runs. Reasoning models are not deterministic.
   - If a second rater can code a subset, report inter-rater agreement: Cohen's κ for categories, or percent agreement.
6. **Fairness (light touch):** break results down by proficiency level or text length. Does the AI over-correct weaker writers more?

Even a small, well-documented study (for example 15 texts × 3 rounds × 3 runs) fits a *methods* special issue if it is framed as a validation *protocol* with pilot evidence.

---

## Part 4 — Weak spots a reviewer will find (fix or disclose)

1. **"Training."** No model was trained. Use "prompt refinement" and "RAG".
2. **Model drift and aliases.** Report the dates; log the exact model version in any new run.
3. **Only 3 of 5 "always-on" guardrail cards are actually sent** (`topCalibration = 3` slices the list). The design document says 5, and says the "missed error" card is always included, which it is not. Either fix the code before collecting data, or describe what actually runs.
4. **The design document's model name is out of date** (`gpt-4.1` vs `gpt-5.6-terra`). Confirm which model produced any outputs you quote.
5. **Round 2 was evaluated partly on the sample its rules came from.** Say so.
6. **Round 3 library contains the evaluation samples.** Leakage risk for any before/after comparison (see Part 3).
7. **Category inconsistencies in the current prompt:**
   - Rule 5 mentions 错别字, but there is no 错别字 section.
   - Rule 5 sends word-choice *problems* to Vocabulary Suggestions, while the format says Vocabulary is enrichment and must not call words wrong.
   - Resolve this with the teacher, since it defines the construct.
8. **Per-scene isolation.** The AI never sees the whole story or the planning boxes.
9. **Heuristic tags.** Keyword rules with partial coverage; report coverage and ideally spot-check them.
10. **Similarity is not diagnosis.** Retrieval finds related rules, not necessarily the violated one.
11. **Sample sizes.** 67 critiqued AI items over 2 rounds; 12 failure-mode cards, one of which (misdirected feedback) has a single example.
12. **Ethics.** The live database holds real student writing (21 stories from 4 accounts at last count). Confirm consent and ethics status before quoting any of it.

---

## Part 5 — Glossary (for the paper's terminology)

- **LLM:** large language model.
- **API:** programmatic interface; here, how the server calls the model.
- **System / user message:** fixed instructions / per-request content.
- **Temperature / reasoning effort:** randomness setting / amount of internal "thinking" in reasoning models.
- **Zero-shot / few-shot:** instructions only / instructions plus examples.
- **In-context learning:** behaviour shaped by the prompt, with no weight change.
- **Fine-tuning:** further training that changes the model's weights (not used).
- **Embedding:** numeric vector representing a text's meaning.
- **Cosine similarity:** closeness of two embeddings.
- **Vector search / ANN:** finding the nearest embeddings quickly.
- **RAG:** retrieval-augmented generation; retrieving reference text into the prompt.
- **Chunk:** one retrievable piece of the reference corpus.
- **Hierarchical chunking / small-to-big:** chunks linked parent-to-child; retrieve small, expand to big.
- **Data leakage:** evaluation data present in the system's inputs, which inflates results.
- **Precision / recall:** correctness of flags / completeness of flags.
- **Cohen's κ:** chance-corrected agreement between two raters.
