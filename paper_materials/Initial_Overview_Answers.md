# AI Feedback System — Technical History (answers to Initial_Overview.md)

Reconstructed from the code repository (git history), the RAG pipeline folder, the annotated Word documents, and a read-only count of the app's database. Where a fact is inferred rather than recorded, it is marked **(inferred)**. Where something could not be found, it is marked **(not found)**.

---

## 0. Summary: what the "rounds" were

The system went through three versions. The dates come from the git history and from the dates on saved outputs in the database.

| | Round 1 — baseline prompt | Round 2 — teacher-informed rule prompt | Round 3 — retrieval-augmented system (RAG) |
|---|---|---|---|
| **In use** | by ~29 July 2026 | ~31 July → end of August 2026 | late August → present (committed 4 Sept 2026) |
| **Model** | Meta Llama 3.3 70B (`llama-3.3-70b-versatile`) | same | OpenAI `gpt-5.6-terra` (reasoning model, low effort). An earlier Round 3 build may have used OpenAI `gpt-4.1`; see §1 |
| **Accessed via** | Groq API | Groq API | OpenAI API |
| **What the AI was given** | a short instruction + 2 examples per section + the student's scene | a long instruction listing error patterns and "do-not-flag" examples taken from your Round 1 comments + the student's scene | fixed rules from your Round 2 review + reference material from your annotated documents, selected for each student text + the student's scene |
| **Output sections** | Grammar · Vocabulary · Encouragement & Next Steps | 错别字 · Grammar · Vocabulary · Encouragement | Grammar · Vocabulary · Content & Coverage · Encouragement |
| **Outputs you reviewed** | `Pear_Story_Corrections.docx` (3 scenes, 25 AI items) | `Student_Examples_Corrections.docx` (3 stories, 42 AI items) | none yet (46 saved in the database; see §5) |

**Evidence for which round produced which document.** The wording of each document's AI feedback matches one prompt word for word:
- **Pear Story:** uses the Round 1 format "Incorrect phrase … / Formula … / Correct …" and "Word … / Context … / Alternatives …".
- **Student Examples:** has the 错别字 section and phrases that exist only in the Round 2 prompt:
  - "missing subject after the topic-comment switch"
  - "V.来/去 cannot be followed directly by an object"

---

## 1. Model and technical setup

### Round 1
- **Model:** `llama-3.3-70b-versatile` (Meta Llama 3.3, 70 billion parameters), hosted by Groq and called through the `groq-sdk` library.
- **Also in the code, unused:** Google `gemini-2.0-flash-lite`. It is commented out, so it was tried or kept as a fallback. No outputs from it were found.
- **Access:** server-side API call from the web app, not a chat interface.
- **Settings:**
  - No temperature, token limit or system message was set, so the provider's defaults applied. Groq's documented default temperature is 1.0 (please check this against Groq's documentation).
  - The whole prompt was sent as one "user" message.
- **Dates:** committed 29 July 2026 (commit `9cb5fe1`, "full feedback set up"). The writing pages it plugs into were built 17 July (commit `a23b565`).

### Round 2
- **Model, access and settings:** unchanged from Round 1. Only the prompt changed.
- **Dates:** the database holds 18 scene feedbacks dated 31 July that contain the 错别字 section, which only the Round 2 prompt asks for. So Round 2 was live by 31 July. It was committed on 2 September (commit `0f3b661`). The Round 1 prompt stayed in the same file as an unused variable, `prompt1`, which is a useful record of the change.

### Round 3
- **Feedback model:** `gpt-5.6-terra`, an OpenAI reasoning model, called through the `openai` library.
  - Reasoning effort is set to `low`.
  - Temperature cannot be set on this model.
  - The feedback is streamed, so the student sees it appear word by word.
- **Retrieval model:** OpenAI `text-embedding-3-small`. It turns text into 1,536 numbers so that similar texts can be found; see §2 and §7.
- **Reference store:** MongoDB Atlas Vector Search, in the app's existing database (collection `rag_chunks`, index `rag_vec`).
- **Dates:**
  - The pipeline files are dated 1–2 September.
  - The database holds retrieval-logged outputs for scenes started between 28 August and 10 September.
  - The code was committed 4 September (commit `5dd463a`, "final working version before publishing").
- **Possible sub-version (inferred):** the design document written with the pipeline says the feedback model was `gpt-4.1`. The committed code uses `gpt-5.6-terra` and adds two rules (8 and 9) and a stricter output format. So there were probably two Round 3 versions:
  - **3a:** `gpt-4.1` with 7 rules
  - **3b:** `gpt-5.6-terra` with 9 rules

  Only 3b is preserved in the code. **Emma to confirm.**

### Other AI in the app (not part of feedback)
- Scene illustrations: `gpt-5.6-terra` writes the image prompt and `gpt-image-1` draws it.
- Character interviews: `gpt-5.6-terra`.

These are separate features. They are mentioned only for completeness.

---

## 2. System workflow / architecture

### What the student does
1. The student chooses **Write Your Own** (free writing) or, after watching the 神农尝百草 video and taking its quiz, **Tell the Story in Your Own Words** (a retelling).
2. For each scene, the student fills in planning boxes (characters, objects, actions, descriptions), then writes the scene in Chinese in the **"In Your Own Words"** box.
3. The student clicks **End Scene**. The scene text is saved and sent for feedback. An illustration is generated at the same time.
4. The feedback appears on a **Scene Feedback** page. The student may **revise the scene once** and get new feedback, then move to the next scene.
5. At the end, the student sees all scenes with all feedback, can make one final round of edits, and can download a PDF feedback summary.

### What the AI receives (all rounds)
- **Only the text of the current scene.** The AI does *not* see:
  - the planning boxes. They are sent to the server but never included in the prompt.
  - earlier scenes of the same story.
  - the student's level or identity.
- Each scene is therefore judged in isolation. This matters for content and coherence feedback, and should be stated as a limitation.

### Round 1 and 2 data flow
```
student's scene text
      │
      ▼
[fixed prompt text] + scene text ──► Llama 3.3 70B (Groq) ──► feedback text
                                                                 │
                                        saved in database ◄──────┤
                                        shown to student ◄───────┘
```

### Round 3 data flow
```
student's scene text
      │
      ├─► converted to a "meaning fingerprint" (embedding)
      │        │
      │        ▼
      │   search the reference library (1,239 pieces cut from your annotated documents):
      │     • 4 most similar GRAMMAR RULE CARDS
      │     • 3 most similar REAL TEACHER CORRECTIONS
      │         (in a retelling, only from that story's samples)
      │     • 3 fixed "AI MISTAKES TO AVOID" cards (always the same 3)
      │     • retelling only: the MODEL STORY + the REQUIRED PLOT-BEAT CHECKLIST
      │
      ▼
 SYSTEM message: the 9 rules + output format
 USER message:   the retrieved reference material + the student's scene
      │
      ▼
 gpt-5.6-terra (OpenAI) ──► feedback streamed to the student's screen
      │
      └─► saved in the database together with the IDs of the reference pieces it was given
```

The saved reference-piece IDs are an audit trail. For every Round 3 feedback, we can reconstruct exactly which rule cards and correction examples the AI was shown.

### How feedback is displayed
The feedback is Markdown text: headings plus one bullet per item. The app renders it as formatted text and uses the same text for the PDF summary. The app does not check or change the AI's wording.

---

## 3. Prompts and system instructions

The full verbatim texts are in **Appendix A**. This section summarises what changed.

### Round 1
A short prompt with three sections and two developer-written examples for each.
- **Level:** it told the model the student is a "beginner to intermediate learner".
- **Grammar:** it asked for the incorrect phrase, the grammar "formula", and the corrected version, and to "try to catch ALL grammar mistakes".
- **Vocabulary:** it asked for "more advanced or natural vocabulary", aiming for 5 suggestions.

### Round 2 — what was added
The model and access were unchanged; the prompt was rewritten around your Round 1 comments on the Pear Story.
- **Persona:** "expert Chinese language teacher … missing errors is just as bad as incorrectly flagging correct Chinese."
- **Critical rules:**
  - never flag correct Chinese
  - check every sentence
  - always explain the rule
  - suggest vocabulary changes only when the original is clearly wrong
- **A checklist of error patterns** written from your corrections:
  - 了 omission
  - 的/地/得, including the rule that one-syllable adverbs cannot take 地
  - directional complements
  - missing subject
  - 把 structure
  - measure words
  - a word-choice list: 别个人, 优秀 vs 优质, 家长, 前途, 寄托在……身上
  - paired structures: 从…中, 每天都, 连…也, 不但…而且, 虽然…但是
  - 错别字 examples: 精疲力尽, 不断, 马虎地
- **"Examples of what not to flag",** taken from your "My comment" critiques:
  - 如蜗牛一般
  - 偷走
  - 硕士和博士学位
  - 今天和我朋友一起
- **Section changes:**
  - new 错别字 (Wrong Characters) section
  - Vocabulary narrowed from "suggest more advanced words" to "only clearly unnatural or wrong words"
  - "Next Steps" dropped

### Round 3 — what was added
- The prompt was split into a **system message** (fixed rules) and a **user message** (retrieved reference material plus the student's text).
- **Rules 1–7** map one-to-one to the problems you identified in your Round 2 review:
  1. only flag actual errors; praise goes in Encouragement
  2. be exhaustive
  3. corrections and explanations must be correct and name the rule
  4. point at the exact span
  5. categorise correctly
  6. input is already cleaned of speech disfluencies
  7. check story content and descriptive detail
- **Rules 8–9** were added in version 3b from your later notes:
  8. all explanations in English
  9. judge the student's level from this submission and keep vocabulary suggestions a small step above it
- **Stricter output format:**
  - Markdown headings
  - "- Nothing to flag." when a section is empty
  - Vocabulary redefined as *enrichment*, with at least 5 items
- **Retelling note:** in a retelling, an extra instruction tells the AI to check the text against every required plot beat.

### Other prompt versions
- The Python prototype (`chinese_writing_rag_pipeline/scripts/assemble_feedback_prompt.py`) contains the 7-rule version with a looser format (version 3a).
- A complete example of an assembled Round 3 prompt, about 2,700 tokens, for a made-up 孟母三迁 retelling, is saved at `chinese_writing_rag_pipeline/chunks/example_assembled_prompt.txt`.
- No other prompt versions were found in the repository.

---

## 4. Reference materials provided to the AI

| Material | Round introduced | How it reached the AI |
|---|---|---|
| **Rubric / formal assessment criteria** | never | There was no separate rubric. The criteria are implicit in the prompt's sections and rules. |
| **Your feedback on student stories** | R2 (indirectly), R3 (directly) | **R2:** Emma hand-distilled your Pear Story and Student Example 1 corrections into the prompt's error-pattern list. **R3:** your corrections from all five documents were parsed automatically into **913 individual corrections** (original → corrected, and why). The AI sees the 3 most similar for each submission, plus **31 "rule cards"** that group your corrections by grammar point. |
| **Your critiques of the AI ("My comment")** | R2 (4 do-not-flag examples), R3 (all 67) | **R3:** all 67 critiques were sorted into 11 "AI failure mode" types and grouped into **12 calibration cards**, each with real examples of the AI's mistake and your verdict. Three are always shown to the AI (see §7). |
| **Native-speaker model story** | R3 | 4 model stories: 神农尝百草, 孟母三迁, 嫦娥奔月, 张骞出使西域. They are shown to the AI only in a retelling of that story; in the app today that means only 神农尝百草. |
| **Plot-beat checklist** | R3 | Derived automatically from your "Miss N scene(s): …" notes across the 51 孟母 and 52 神农 samples, ranked by how often each beat was missing (for example, "another person in brown came by and had a conversation with 神农", missing in 40 of 52). Retellings only. |
| **Examples of learner responses** | R3 | 109 learner samples in total: 51 孟母, 52 神农, 3 pear-story retellings, and 3 scenes of the creative pear narrative. They are stored whole; the AI sees individual corrections from them, not whole stories. |
| **Vocabulary-error examples / list** | R2 (hard-coded list), R3 (retrieved) | **R2:** a fixed list of about 6 word-choice errors in the prompt. **R3:** there is no separate list. Word-choice corrections are among the 913 corrections and are retrieved when similar. |
| **Grammar rule descriptions** | R3 | One-line descriptions for about 29 grammar points, written by the developer and checked against your terminology (for example "了completed", "V. + directional complement + Place + 来/去"). |
| **Developer-written format examples** | R1 | Two examples per section (the 才/就 and 被…着 grammar examples; the 漂亮/精彩 and 安静/宁静 vocabulary examples). Removed in R2. |

**Source files in the repository:**
- Word documents: `chinese_writing_rag_pipeline/raw/`
- Parsed text: `chinese_writing_rag_pipeline/extracted/`
  - `all_my_comments.txt` lists all 67 of your AI critiques
- Final library of 1,239 pieces: `chinese_writing_rag_pipeline/chunks/chunks.jsonl`

---

## 5. AI outputs

### Round 1 — `Pear_Story_Corrections.docx` (3-scene creative narrative)
Representative problems you identified:
- **Over-correction of literary style:** 如蜗牛一般 → 像蜗牛一样. Your comment: "如蜗牛一般 is perfectly right and has more literate flavor."
- **Incorrect vocabulary alternatives:** 携走 for 偷走; 饿叫 for 叫.
- **Alternatives above level or too strong:** 低贱 / 卑微 for 地位低.
- **Unneeded "corrections":** 硕士和博士学位; 今天和我朋友一起; 开始改革经济以来.
- **Missed errors:** 秋季期间; many others ("AI feedback missed other places that should be revised").
- **Correct fix, no explanation:** 乱地 → 乱七八糟, without the one-syllable adverb + 地 rule.

### Round 2 — `Student_Examples_Corrections.docx` (3 spoken pear-story retellings)
Representative problems:
- **The prompt's own rule wording carried into the output.**
  - The prompt said "爬上去梯子 is wrong … Correct: 爬上梯子" and "V.来/去 cannot be followed directly by an object".
  - The AI output "张先生爬上梯子".
  - Your correction was 爬上梯子去 ("去 can follow the Obj.").
  - The developer's simplified version of your rule was reproduced by the AI.
- **An invented rule over-applied.**
  - The prompt added "Missing subject: after topic-comment switches, restate the subject". This generalised your single comment about a narrator aside in the Pear Story.
  - The AI then asked for subjects in several places where omission is fine.
  - Your comment: "I don't think Chinese has 'missing subject' rule."
- **Disfluency false positives.** The AI's quotes contain repetitions that are not in the cleaned text ("小王和那，那筐梨子倒", "他拿，他拿梨的时候", "也，也"). So the AI was given the uncleaned spoken transcript and flagged speech repetitions as writing errors.
- **Misleading "no error" framing:** "The grammar rule violated is the direction complement error. However … No correction needed."
- **Misdirected feedback:** span "这个戴围巾的男人拿多梨" flagged, but the explanation was about "他拿梨的时候".
- **Miscategorisation:** 糊涂 and 热死了 listed as 错别字 (they are vocabulary, and fine as written); a vocabulary item duplicating a grammar item.
- **Correct fix, wrong explanation:** "missing a verb or a preposition" when the real problem was a missing 了.

### Round 3 (most recent)
- **The database holds 46 Round 3 scene feedbacks** from 28 August–10 September, 24 of them 神农尝百草 retellings. Each is stored with the student's original text, any revised text, the final text, timings, and the IDs of the reference material the AI was given.
- **Not yet exported.** An automated safety check blocked my export because it would copy student-written text and account data. Emma can export it with your agreement on handling (for example, pseudonymised IDs only).
- **Round 1 also has saved outputs.** The same database holds 18 Round 2 scene feedbacks from 31 July, which may give more before-and-after material.
- **A comparable before-and-after set can be produced** by re-running the Round 1 and Round 2 samples through Round 3. **Caution:** those samples, your corrections of them, and the AI's earlier mistakes on them are all *inside* the Round 3 reference library. A naive re-run would let the AI "see the answers". A fair comparison needs either new samples or a Round 3 library rebuilt without those samples. Emma can set this up.

---

## 6. Human feedback and refinement process

| After | What you provided | What changed next | How it was implemented |
|---|---|---|---|
| **Round 1** | Line-by-line teacher corrections of the Pear Story, plus a "My comment" verdict on each of the 25 AI items. Teacher corrections on Student Example 1 were also written at this stage. | Round 2 prompt | Emma read the comments and **hand-wrote** them into the prompt: an error-pattern checklist with your examples, 4 "do not flag" examples, a new 错别字 section, and a narrower Vocabulary section. |
| **Round 2** | "My comment" on all 42 AI items for the 3 Student Examples, plus your summary notes in Chinese naming 5 recurring problems: missed errors; disfluency and missing content; misleading "no correction needed"; feedback on the wrong span; miscategorisation and wrong explanations. You also supplied the 孟母 (51) and 神农 (52) graded sample sets and the 4 model stories. | Round 3 | 1. The 5 problems became system rules 1–7. 2. All five Word documents were parsed automatically into the reference library. 3. Your "My comment" texts were auto-sorted into failure-mode cards. 4. Your "Miss N scene" notes became plot-beat checklists. 5. The model was changed to OpenAI. |
| **Round 3 (early)** | Later notes asking that all explanations be in English and that vocabulary suggestions match the student's level rather than push advanced words. | Round 3b | Added as rules 8 and 9. The Vocabulary section was reworded as enrichment with a worked example, at least 5 items. |

**Methodological note on Round 2:** its prompt was partly built from your corrections of Student Example 1, and was then evaluated on that same sample. Results on that sample are therefore somewhat optimistic.

**Not found in the repository:** your Chinese summary notes with the 5 issues. They are quoted and paraphrased in the design document, for example "AI并不能找到……miss了很多需要改的问题". Could you send the original?

---

## 7. What "training" meant

**The AI model was never trained or fine-tuned.** Its internal parameters were never changed in any round. Everything happened in what the model is *given to read* each time it produces feedback. In technical terms:

| Round | Technique | Plain explanation |
|---|---|---|
| R1 | **Zero-shot instruction prompting** with two format examples per section | We told the model what to do and showed it the layout. |
| R2 | **Prompt engineering** / **in-context learning** from hand-distilled expert rules, plus **negative examples** | We rewrote the instructions using the teacher's corrections, and listed things *not* to flag. The model reads these every time. It does not remember them between requests. |
| R3 | **Retrieval-augmented generation (RAG)** + rule-based system prompt + **model change** | For each student text, the system searches a library built from the teacher's annotated documents and pastes the most relevant rules, corrections and "AI mistakes to avoid" into the model's input. This is described in more detail below. |

**How the Round 3 search works.**
- Every piece of the library, and every new student text, is converted into an "embedding": a list of 1,536 numbers that encodes meaning. Texts with similar meaning get similar numbers.
- The system retrieves the library pieces whose numbers are closest to the student's text.
- A 了-omission sentence, for example, tends to retrieve the 了 rule card and your 了 corrections.

**How the library was organised.** Two parts used simple, human-readable keyword rules rather than machine learning:
- **Grammar-point tags:** they matched the teacher's own shorthand, such as "了completed" or "direction complement". About 32% of the 913 corrections matched a named grammar point; the rest are still searchable.
- **Failure-mode tags on the "My comment" texts:** for example "no need to revise" → *false positive*; "did not capture" → *missed error*. 54 of the 67 critiques matched at least one type.

**Suggested wording for the paper:** "iterative expert-informed prompt refinement, followed by retrieval-augmented generation grounded in a teacher-annotated corpus". Avoid "trained", which reviewers will read as fine-tuning.

**The three guardrail cards.** Five failure-mode cards are listed as "always inject". Because of a size limit in the code, only the first three are actually sent:

1. false positive / unneeded correction
2. misleading "no error" framing
3. misdirected feedback

These are listed as always-on but are **not** sent: "miscategorised error type" and "disfluency false positive". "Missed error", which the design document describes as always-on, is not sent either. Those problems are addressed only by the written rules (rules 2, 5 and 6). We should either describe the system as it actually runs, or fix this before collecting new data.

---

## 8. Feedback categories

| Category | R1 | R2 | R3 (current) |
|---|---|---|---|
| 错别字 / Wrong characters | — | ✔ own section | ✘ no section. Rule 5 still mentions it, so wrong characters presumably appear under Grammar (inconsistency) |
| Grammar | ✔ phrase / formula / correction | ✔ rule + correction | ✔ span → correction, English rule explanation |
| Vocabulary | ✔ "more advanced or natural" (enrichment, 5) | ✔ only clearly wrong or unnatural words (correction) | ✔ enrichment only, at least 5, at or just above the student's level |
| Discourse / coherence | — | — (only via "structural errors" in the checklist) | — no separate category. The Python 3a version put coherence under Content |
| Content (e.g. "miss X scene") | — | — | ✔ **Content & Coverage**: missing or misremembered plot beats against the checklist (retellings); a general content check (free writing) |
| Expressiveness / description | — | — | partial. Rule 7 asks the AI to "note if the writing lacks sufficient descriptive detail" under Content & Coverage |
| Encouragement | ✔ + "next steps" | ✔ | ✔ one or two sentences, specific; the only place for praise |

### "Vocabulary suggestions" vs "vocabulary corrections"
The system has never had a separate vocabulary-*correction* category.
- **R1:** Vocabulary meant suggestions of better words.
- **R2:** Vocabulary meant corrections of wrong words.
- **R3:** Vocabulary is explicitly **enrichment**. The prompt says: "the student's words are usually fine … do not claim the student's word is wrong". But Rule 5 says "word-choice problems go under Vocabulary Suggestions".

So in the current version an actual word-choice error has no clearly defined home. Examples are 农人 → 农民, 优秀 → 优质, and 遛 (used only for dogs). It may be softened into a "suggestion" or placed under Grammar.

**Recommendation:** add a **Vocabulary Corrections** section (errors: wrong word for the context, collocation, register), separate from **Vocabulary Suggestions** (optional alternatives to acceptable words). Consider restoring **错别字** and adding **Discourse & Coherence**. This is a decision for you, as it defines the assessment construct.

---

## 9. Version history

| Date | Commit | What changed (feedback-relevant) |
|---|---|---|
| 22 Jun 2026 | `604de39` | Project created |
| 17 Jul 2026 | `a23b565` | Scene-by-scene writing pages; no AI feedback yet |
| 29 Jul 2026 | `9cb5fe1` | **Round 1** feedback: Llama 3.3 70B via Groq; Gemini commented out |
| (31 Jul 2026) | — | **Round 2** prompt in use (from database outputs; not committed until 2 Sept) |
| 2 Sep 2026 | `0f3b661` | Round 2 prompt committed; Round 1 kept as `prompt1`; a planned "Correction" database model was defined but never used |
| 1–2 Sep 2026 | (not committed separately) | RAG pipeline built: parsing, tagging, 1,239-piece library, design document |
| 4 Sep 2026 | `5dd463a` | **Round 3** committed: RAG, OpenAI `gpt-5.6-terra`, 9 rules, retelling mode for 神农尝百草, streaming, reference IDs logged |
| 10 Sep 2026 | `e64791d` | "changes for meeting": interface and retelling vocabulary only; feedback logic unchanged |

### Files available for the manuscript
- **Prompts:**
  - R1 and R2: `git show 9cb5fe1:app/api/story/feedback/route.ts` and `git show 0f3b661:app/api/story/feedback/route.ts`
  - R3: `lib/rag/assembleFeedbackPrompt.ts`
  - 3a: `chinese_writing_rag_pipeline/scripts/assemble_feedback_prompt.py`
  - All reproduced in Appendix A below.
- **Design document:** `chinese_writing_rag_pipeline/docs/design.md`. Its model name (`gpt-4.1`) and its claim that 5 cards are always injected are out of date.
- **Retrieval test run:** `chinese_writing_rag_pipeline/docs/demo_output.txt`
- **Full example prompt:** `chinese_writing_rag_pipeline/chunks/example_assembled_prompt.txt`
- **Plot-beat checklists:** `chinese_writing_rag_pipeline/chunks/scene_checklists.json`
- **Annotated source documents:** `chinese_writing_rag_pipeline/raw/*.docx`

### Not found
- **Screenshots:** none in the repository. They can be taken from the running app.
- **Round 3a code:** not committed.
- **Request logs:** the server logs only timing, not prompts. The full Round 3 prompt can be rebuilt from the saved reference IDs.
- **Your Chinese summary notes:** see §6.

---

## 10. Anything else relevant to reproducing the system

1. **Model versions are aliases, not fixed snapshots.**
   - `llama-3.3-70b-versatile` and `gpt-5.6-terra` are provider aliases, and the provider may update what they point to.
   - For the paper, report the model name, the provider, the access dates, and the settings (Round 3: reasoning effort *low*; no temperature control; Rounds 1–2: provider defaults).
   - For any new data collection, we should log the exact model version returned by each API call.
2. **Output variability.** Only Round 3 has any control (reasoning effort). The same text submitted twice can produce different feedback. A reliability check (same texts run several times) would address this.
3. **Per-scene isolation.** The AI never sees the whole story or the planning boxes, so feedback on coherence across scenes is impossible by design.
4. **Revision data.** For every scene, the app stores:
   - the original text
   - the text after one feedback-driven revision, if used
   - the final edited text
   - whether it was edited
   - start and end times

   These could support a study of how students take up the AI feedback.
5. **Input modality.** In the app students type, so there are no speech disfluencies. Rule 6 is therefore always true in-app. It matters only if spoken transcripts are fed in, as in Round 2.
6. **Content checklist coverage.**
   - 孟母三迁 and 神农尝百草 have derived checklists.
   - Only 神农尝百草 is available as an in-app retelling.
   - Other stories fall back to the model story, or, for free writing, to no content reference at all.
7. **Data use.** The reference library contains no student names; samples are numbered. The live database holds student accounts and writing, so ethics approval and consent status for the Round 3 data should be confirmed before any outputs are quoted in the paper.

---

## Appendix A — Verbatim prompts

### A1. Round 1 (commit `9cb5fe1`, Llama 3.3 70B via Groq; sent as a single user message; `${sentence}` = the student's scene)

```
You are a Chinese language teacher giving feedback to a student who is learning Chinese.
The student wrote this sentence in Chinese:
"${sentence}"

Please provide feedback in English with three sections:
1. **Grammar Corrections**(bold title). Please indicate the incorrect phrase, the general grammar formula it should follow, and then the correct version. If there are no grammar mistakes, say so. 
    Example 1: Incorrect phrase "我早上九点就出门了！结果迟到了" / Formula, 谁 + (时间) + 才 + (做太早的动作) / Correct, "我早上九点才出门了！结果迟到了"
    Example 2: Incorrect phrase "你被爱了" / Formula, 谁 + 被 + （动作）+ 着/ Correct, "你被爱着". 
    Please insert a blank line before starting each new grammar correction.
    Try to catch ALL grammar mistakes, especially major ones.
2. **Vocabulary Suggestions**(bold title). Suggest more advanced or natural vocabulary they could use. Indicate the specific word that could be better, then the alternative options and explain the conntation of both the word in question and the alternatives.
    Example 1: Word, "漂亮” / Context, "他在决赛中打了一场漂亮的比赛" / Alternatives, 精彩的比赛 emphasizes that the game was exciting, impressive, and enjoyable to watch, while 漂亮 evaluates how well the game was played.
    Example 2: Word, “安静” / Context, “晚上，湖边非常安静” / Alternatives, 宁静 emphasizes a peaceful, calm atmosphere and has a more literary and emotionally positive feeling, while 安静 simply means that there is little noise or activity.
    It describes the experience or content of the game. Please write the explaination in english. 
    Please insert a blank line before starting each new vocab suggestion.
    Please aim to give 5 word choice suggestions.
3. **Encouragement and Next Steps**(bold title).
    (not bold): End with one sentence of genuine encouragement about a specific thing they did well. Perhaps the flow is good, the description is vivid, the thoughts are sophisticated, etc. Then also one line for what to focus on next time.

Keep your feedback concise, clear, and encouraging. The student is a beginner to intermediate learner.
```

### A2. Round 2 (commit `0f3b661`, same model and settings)

```
You are an expert Chinese language teacher giving detailed, accurate feedback to a student learning Chinese. You must be thorough — missing errors is just as bad as incorrectly flagging correct Chinese.

CRITICAL RULES:
1. Never flag correct Chinese as wrong. 如蜗牛一般 is literary and correct. Do not change stylistic choices.
2. Always be thorough — read every sentence carefully and check all of the error patterns listed below.
3. When suggesting corrections, always explain the grammar rule being violated.
4. Only suggest vocabulary changes when the original is clearly unnatural or wrong in context.

---
COMMON ERROR PATTERNS TO CHECK (go through each one systematically):

**了 (le) errors:**
- Missing 了 after completed actions (V+了)
- Missing 了 at end of changed state sentences
- Example: 拼几个小时之后 → 拼**了**几个小时之后

**的/地/得 confusion:**
- 地 is the adverb marker before verbs (马虎**地**V.)
- 得 is the complement marker after verbs (V.+**得**+complement)
- 的 is the noun modifier (Adj.+**的**+Noun)
- Mono-syllabic adverbs CANNOT use 地 — must be multi-syllabic
- Example: 马虎得 → 马虎**地** (错别字 type error)

**Direction complement errors:**
- 爬上去梯子 is wrong — cannot have object after 上去. Correct: 爬上梯子
- 走去 + place is wrong. Correct: 走到 + place
- V.来/去 cannot be followed directly by an object

**Missing subject:**
- After topic-comment switches, restate the subject
- After narrator comments inserted mid-story, restate the subject when returning to story

**把 structure errors:**
- 把 + Obj. + V. + Complement (the verb MUST have a complement or 了)
- 算是 cannot be used in 把 structure
- Correct: 把我们**只**算作小吃而已

**Measure words:**
- 这/那 + Measure word + Noun (cannot skip measure word)
- 这个 can only precede a noun, not a verb phrase

**Word choice errors:**
- 别个人 is not standard Chinese → 别的人
- 优秀 cannot describe objects/things, only people → 优质
- 家长 is only used in education contexts (parents dealing with school) → 爸爸妈妈 or 父母
- 前途 already means "hopeful future" — do not add 有希望的 before it
- 寄托在……身上 is for people carrying hope, not objects

**Structural errors:**
- 从 + Place requires 中 to close: 从香甜的睡梦**中**
- 每天 + 都 (frequency adverb needs 都)
- 连……也/都 structure
- 不但……而且 structure
- 虽然……但是 structure must be complete

**错别字 (Wrong characters that sound similar — check every character):**
- 精辟力尽 → 精**疲**力尽
- 不短 → 不**断**
- 马虎得 → 马虎**地**
- Any character that looks or sounds like it might be substituted

---
EXAMPLES OF WHAT NOT TO FLAG:
- 如蜗牛一般 — correct, literary flavor, do NOT change to 像蜗牛一样
- 偷走 — correct, do NOT suggest 抢走 unless context implies force
- 硕士和博士学位 — correct, no need to suggest alternatives
- 今天和我朋友一起 — correct word order, do not flag

---

The student wrote:
"${sentence}"

---
Now give thorough feedback in English with these four sections:

**错别字 (Wrong Characters)**
Check every single character for wrong characters that sound or look similar. Quote the wrong character, explain what it should be, and why. If none found, say "No 错别字 found."

**Grammar Corrections**
Go through each error pattern listed above systematically. For each error found:
- Quote the incorrect phrase in Chinese
- State which grammar rule is violated
- Give the corrected version in Chinese
Be thorough — check every sentence. If a sentence has multiple errors, list all of them.

**Vocabulary Suggestions**
Only flag words that are clearly unnatural or wrong in context. For each suggestion:
- Quote the original word and its context
- Explain specifically why it is not ideal
- Give the better alternative and explain why it fits better

**Encouragement**
End with one specific, genuine sentence that mentions something the student did well in their writing.
```

### A3. Round 3b — current system message (`lib/rag/assembleFeedbackPrompt.ts`, `gpt-5.6-terra`, reasoning effort low)

```
You are a Chinese-language writing tutor giving feedback to an early learner on a short narrative writing assignment. Follow these rules, which come directly from the supervising teacher's review of this system's past mistakes:

1. In the ERROR sections (Grammar Corrections, Content & Coverage) only give feedback on ACTUAL errors. If a sentence is already correct, say nothing about it there -- do not write "no correction needed, it is grammatically correct" as a feedback item. Save all positive remarks for the closing "Encouragement" section. (Vocabulary Suggestions is different -- it is enrichment, not error-flagging; see the output format.)
2. Be exhaustive: scan every sentence. Past runs of this system frequently missed real errors -- do not stop after finding a few.
3. When you flag a span, your corrected version AND your explanation must both be linguistically correct, and the explanation must state the actual grammatical rule involved (not just "this is unclear").
4. Point your feedback at the exact span that is wrong. Do not label span A as incorrect and then explain span B.
5. Categorize correctly: 错别字/Wrong Characters is for mis-written characters only; word-choice problems go under Vocabulary Suggestions; syntax/morphology problems go under Grammar Corrections. Do not mix these up.
6. This transcript has already been cleaned of speech disfluencies (repetitions, false starts, filler pauses) -- do not flag anything as an error on the grounds that it looks like a repetition or a pause.
7. After grammar/vocabulary feedback, separately check story CONTENT: note any plot points that are missing or misremembered, and note if the writing lacks sufficient descriptive detail.
8. Write ALL prose -- explanations, nuance descriptions, the Encouragement paragraph -- in English. Chinese appears ONLY inside the original/corrected spans, individual words, characters, and grammar particles (了/地/得/把/被/etc.) themselves -- never write a full explanatory sentence in Chinese.
9. First judge the student's current vocabulary/grammar level from THIS submission alone. Every vocabulary alternative you suggest must be a small, natural step from that level -- a common near-synonym, not a rare, literary, or advanced word the student hasn't shown readiness for. Clear, correct expression matters more than sophisticated vocabulary: never push the student toward complexity beyond what they've already demonstrated.

Output format -- Markdown, exactly this structure:

## Grammar Corrections
- original span：corrected span，English explanation of the rule
- (one item per line; if there are none, write exactly "- Nothing to flag.")

## Vocabulary Suggestions
Enrichment, NOT error-flagging -- the student's words are usually fine. Give AT LEAST 5 suggestions. Pick words the student actually used and, for each, offer one or two alternatives at or barely above their current level (see rule 9) -- common everyday synonyms, not fancier or more literary words -- and explain in English the difference in meaning, tone, or connotation. Do not claim the student's word is wrong, and never propose an alternative that is itself incorrect, unnatural in context, or above the student's level.
  Format each line as -- the student's word -- the phrase they used it in：alternative，English explanation of the nuance difference；alternative，English explanation
  Style example (not about this student, and not the level ceiling -- match to whatever level THIS student writes at): 高兴 -- "我很高兴"：开心, an equally common synonym with a slightly warmer, more casual tone -- not a fancier word, just a different everyday choice

## Content & Coverage
- missing or misremembered plot point，what the story actually needs

## Encouragement
One or two sentences naming something specific the student did well.

Rules for the output: keep each "## " heading on its own line exactly as written. Put every feedback item on its own line beginning with "- ". Never run multiple items together on one line. In Grammar Corrections and Content & Coverage, if there is nothing to flag the section's only line is "- Nothing to flag." -- but Vocabulary Suggestions must always have at least 5 items.
```

**Retelling add-on** (prepended to the user message for 神农尝百草 retellings):
```
This is a RETELLING of a known story. The required plot beats and a model version are given below. In "Content & Coverage", check the student's retelling against every required beat: name each beat that is missing, out of order, or misremembered. Beats the student covered correctly do NOT need to be listed.
```

**User message structure** (assembled per submission):
1. retelling only: the retelling note, the model story, and the required plot beats
2. "Relevant grammar rule cards": the 4 most similar
3. "AI-feedback calibration guardrails": the 3 fixed cards
4. "Nearby real correction exemplars": the 3 most similar teacher corrections
5. "Student's story to review": the scene text

### A4. Round 3a — 7-rule version (`chinese_writing_rag_pipeline/scripts/assemble_feedback_prompt.py`)
Rules 1–7 are the same as above, with slightly different wording in rules 1 and 7. There are no rules 8–9. The output format was loose: "three sections — Grammar Corrections, Vocabulary Suggestions, and Content & Coverage (missing/incorrect plot points, coherence) — each as a list of 'original span：corrected span，explanation' items (empty if nothing to flag), followed by a short Encouragement paragraph".
