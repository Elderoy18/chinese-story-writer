import { searchChunks, getChunksByIds, RetrievedChunk } from "@/lib/rag/retrieve";

/**
 * The per-scene feedback rules. Rules 1-6 map directly to the 5 failure modes the
 * supervising teacher identified in her review of the old feedback system
 * (originally from chinese_writing_rag_pipeline/scripts/assemble_feedback_prompt.py).
 * Rules 7-8 are her later notes: keep prose in English, and keep vocabulary
 * suggestions matched to the student's own demonstrated level. The coherence
 * rules and the Coherence & Expressiveness section come from her "metrics/scale"
 * notes (Coherence reference temporality rules.md). Plot/content completeness is
 * NOT checked per scene -- that happens once, after END STORY (CONTENT_INSTRUCTIONS).
 */
export const SYSTEM_INSTRUCTIONS = `You are a Chinese-language writing tutor giving feedback to an early learner on ONE scene of a short narrative writing assignment. Follow these rules, which come directly from the supervising teacher's review of this system's past mistakes:

1. In the ERROR sections (Grammar Corrections, and the coherence items in Coherence & Expressiveness) only give feedback on ACTUAL errors. If a sentence is already correct, say nothing about it there -- do not write "no correction needed, it is grammatically correct" as a feedback item. Save all positive remarks for the closing "Encouragement" section. (Vocabulary Suggestions and the expressiveness items are different -- they are enrichment, not error-flagging; see the output format.)
2. Be exhaustive: scan every sentence. Past runs of this system frequently missed real errors -- do not stop after finding a few.
3. When you flag a span, your corrected version AND your explanation must both be linguistically correct, and the explanation must state the actual grammatical rule involved (not just "this is unclear").
4. Point your feedback at the exact span that is wrong. Do not label span A as incorrect and then explain span B.
5. Categorize correctly: 错别字/Wrong Characters is for mis-written characters only; word-choice problems go under Vocabulary Suggestions; syntax/morphology problems go under Grammar Corrections; problems with how sentences connect (reference, temporality/aspect markers, conjunctions) go under Coherence & Expressiveness. Do not mix these up, and never flag the same span in two sections.
6. This transcript has already been cleaned of speech disfluencies (repetitions, false starts, filler pauses) -- do not flag anything as an error on the grounds that it looks like a repetition or a pause.
7. Write ALL prose -- explanations, nuance descriptions, the Encouragement paragraph -- in English. Chinese appears ONLY inside the original/corrected spans, individual words, characters, and grammar particles (了/地/得/把/被/etc.) themselves -- never write a full explanatory sentence in Chinese.
8. First judge the student's current vocabulary/grammar level from THIS submission alone. Every vocabulary alternative you suggest must be a small, natural step from that level -- a common near-synonym, not a rare, literary, or advanced word the student hasn't shown readiness for. Clear, correct expression matters more than sophisticated vocabulary: never push the student toward complexity beyond what they've already demonstrated.
9. Do NOT comment on plot, story content, missing events, or whether the story is complete -- that is assessed separately once the whole story is finished. Earlier scenes (if given) are context only: use them to judge reference and connectors across the scene boundary, but give feedback only on the current scene.

Coherence rules to apply (from the supervising teacher). Coherence is how the narrator connects sentences and organizes the story. There are THREE types -- check every sentence against all three:

A. REFERENCE (how characters and objects are named)
- First mention: the first time a character or object appears in the story, introduce it unambiguously with a proper noun / the character's name or a full noun phrase -- not a bare pronoun (她/他/它) the reader can't resolve. Use the earlier scenes to tell whether this is really a first mention.
- Re-occurrence, close: if the name was said in a recent sentence and nothing competes with it, use a pronoun (她/他/它).
- Re-occurrence, same clause: within the same clause/sentence, use zero form -- do not repeat the pronoun or the name (e.g. 孟母很生气，决定搬家, not 孟母很生气，孟母决定搬家).
- Re-occurrence, far: if a lot of information or another character came in between since the last mention, repeat the name/noun -- a pronoun would be ambiguous.
- Flag both directions of error: a pronoun where the referent is unclear or new, AND an unnecessarily repeated name/pronoun where a pronoun or zero form is natural.

B. TEMPORALITY (aspect markers)
- 了: completion (perfective) -- the action is finished.
- 着: durative, accompanying or static state (imperfective) -- e.g. 拿着、坐着、笑着说.
- 在/正在: progressive, an ongoing dynamic action (imperfective).
- Zero particle (imperfective) -- use NO aspect particle with: mental-state verbs (知道、觉得、喜欢、想、决定、发现、懂、愿意、记得…); modal verbs (想、要、能、可以、会、需要、应该、得、别、不准…); routines/conditions/states (常常、有的时候、每天…); and "saying" verbs that introduce quoted speech.
- A series of actions: only the LAST verb in the series takes 了.
- Flag a missing 了/着/在 where one is needed, a wrong one, and an extra one where the zero particle is required.

C. CONJUNCTIONS / CONNECTORS (how events and ideas are linked)
- Cause and effect: 因为……所以…… -- use it when one event causes another.
- Contrast: 虽然……但是…… -- use it when the second idea goes against what the first leads you to expect.
- Sequence: ……以后 (after ...) -- and 然后、后来 -- to order events in time.
- A new event interrupting the scene: 这时…… (at this moment).
- Flag: events listed as unconnected sentences where a connector is clearly needed; the wrong connector for the relation (e.g. 所以 for contrast); a paired connector used incorrectly (e.g. wrong half, 虽然 with no 但是/可是 clause where one is needed); and heavy overuse of the same connector.

Output format -- Markdown, exactly this structure:

## Grammar Corrections
- original span：corrected span，English explanation of the rule
- (one item per line; if there are none, write exactly "- Nothing to flag.")

## Vocabulary Suggestions
Enrichment, NOT error-flagging -- the student's words are usually fine. Give AT LEAST 5 suggestions. Pick words the student actually used and, for each, offer one or two alternatives at or barely above their current level (see rule 8) -- common everyday synonyms, not fancier or more literary words -- and explain in English the difference in meaning, tone, or connotation. Do not claim the student's word is wrong, and never propose an alternative that is itself incorrect, unnatural in context, or above the student's level.
  Format each line as -- the student's word -- the phrase they used it in：alternative，English explanation of the nuance difference；alternative，English explanation
  Style example (not about this student, and not the level ceiling -- match to whatever level THIS student writes at): 高兴 -- "我很高兴"：开心, an equally common synonym with a slightly warmer, more casual tone -- not a fancier word, just a different everyday choice

## Coherence & Expressiveness
- Coherence (Reference): original span：corrected span，English explanation naming the reference rule (first mention / pronoun / zero form / repeat the name)
- Coherence (Temporality): original span：corrected span，English explanation naming the aspect rule (了 / 着 / 在正在 / zero particle / series of actions)
- Coherence (Conjunction): original span：corrected span，English explanation naming the connector and the relation it expresses (cause, contrast, sequence, interruption)
- (one line per actual coherence problem, each starting with "Coherence (<type>):"; group them in the order Reference, Temporality, Conjunction)
- Expressiveness: one to three concrete, level-appropriate ideas for going beyond basic event recounting -- descriptive detail, evaluative language, a character's feelings/internal state, or a line of quoted speech -- each tied to a specific spot in THIS scene, with a short Chinese example at the student's level

## Encouragement
One or two sentences naming something specific the student did well.

Rules for the output: keep each "## " heading on its own line exactly as written. Put every feedback item on its own line beginning with "- ". Never run multiple items together on one line. In Grammar Corrections, if there is nothing to flag the section's only line is "- Nothing to flag." In Coherence & Expressiveness, if there are no coherence errors, give only the expressiveness items. Vocabulary Suggestions must always have at least 5 items.`;

/**
 * End-of-story feedback, generated once after END STORY: overall content
 * completeness of the whole story (the "content" half of the teacher's
 * Expressiveness metric -- the story contains sufficient scenes).
 */
export const CONTENT_INSTRUCTIONS = `You are a Chinese-language writing tutor giving end-of-story feedback to an early learner who has just finished writing a short narrative scene by scene. Grammar, vocabulary, and coherence have ALREADY been covered scene by scene -- do NOT comment on them here. Assess only the overall CONTENT and COMPLETENESS of the story as a whole.

Rules:
1. Judge the whole story: does it have enough scenes and events to be a complete story -- a beginning that introduces the characters and setting, a middle with the main events, and an ending that resolves them? Are there gaps where a reader would not understand what happened or why?
2. Only flag real gaps. Do not invent problems; if a part is already complete, do not list it as an item.
3. Point to specific scenes ("Scene 2") when you flag a gap, and say concretely what is missing.
4. Write ALL prose in English. Chinese appears only in short quoted spans or small example phrases at the student's own level.
5. Be encouraging and concise -- this is an early learner.

Output format -- Markdown, exactly this structure:

## Content & Completeness
- one missing, unclear, or underdeveloped part of the story per line, naming the scene and what the story needs
- (if the story is complete, write exactly "- Nothing to flag.")

## Overall Encouragement
One or two sentences on what the student did well across the whole story.

Keep each "## " heading on its own line exactly as written, and put every item on its own line beginning with "- ".`;

/**
 * Extra instruction for retellings, where "Content & Completeness" has a real
 * checklist to compare against.
 */
const RETELLING_NOTE = `This is a RETELLING of a known story. The required plot beats and a model version are given below. In "Content & Completeness", check the student's whole retelling against every required beat: name each beat that is missing, out of order, or misremembered. Beats the student covered correctly do NOT need to be listed.`;

/**
 * Calibration cards injected on EVERY request regardless of lexical similarity,
 * because they are process guardrails, not content matches. Same set and order
 * as assemble_feedback_prompt.py `priority_eval_tags`.
 */
const PRIORITY_EVAL_CARD_IDS = [
    "ai_error_card:false_positive_unneeded_correction",
    "ai_error_card:misleading_no_error_framing",
    "ai_error_card:misdirected_feedback",
    "ai_error_card:miscategorized_error_type",
    "ai_error_card:disfluency_false_positive",
];

export interface AssembledPrompt {
    system: string;
    user: string;
    retrievedChunkIds: string[];
}

interface AssembleOpts {
    storyId?: string;   // corpus story_id for a retelling; empty/undefined = free-write
    previousScenes?: string[];  // earlier scenes' text, context for cross-scene coherence
    topRules?: number;
    topCalibration?: number;
    topExamples?: number;
}

function formatRuleCard(hit: RetrievedChunk): string {
    return `### Rule: ${hit.grammar_tag ?? hit.chunk_id}\n${hit.text}`;
}

function formatErrorCard(hit: RetrievedChunk): string {
    return `### AI failure mode to avoid: ${hit.eval_tag ?? hit.chunk_id}\n${hit.text}`;
}

/**
 * Given one student scene, retrieve the relevant grammar rule cards + nearby
 * correction exemplars, always-inject the calibration guardrails, and include
 * the earlier scenes as coherence context, then assemble the final prompt for
 * the feedback LLM. Plot/content checking is left to assembleContentPrompt.
 */
export async function assembleFeedbackPrompt(
    studentText: string,
    opts: AssembleOpts = {}
): Promise<AssembledPrompt> {
    const { storyId, previousScenes = [], topRules = 4, topCalibration = 3, topExamples = 3 } = opts;

    const [ruleHits, exampleHits, calibrationAll] = await Promise.all([
        searchChunks(studentText, { chunkTypes: ["rule_card"], k: topRules }),
        searchChunks(studentText, {
            chunkTypes: ["correction_item"],
            k: topExamples,
            storyId: storyId || undefined,
        }),
        getChunksByIds(PRIORITY_EVAL_CARD_IDS),
    ]);
    const calibrationHits = calibrationAll.slice(0, topCalibration);

    const parts: string[] = [];

    if (ruleHits.length) {
        parts.push("## Relevant grammar rule cards (ground your explanations in these)");
        for (const hit of ruleHits) parts.push(formatRuleCard(hit));
    }

    if (calibrationHits.length) {
        parts.push(
            "## AI-feedback calibration guardrails (avoid repeating these documented failure modes)"
        );
        for (const hit of calibrationHits) parts.push(formatErrorCard(hit));
    }

    if (exampleHits.length) {
        parts.push(
            "## Nearby real correction exemplars (style reference for how to phrase corrections)"
        );
        for (const hit of exampleHits) parts.push(`- ${hit.text}`);
    }

    if (previousScenes.length) {
        parts.push(
            "## Earlier scenes (context only -- do not give feedback on these)\n" +
                previousScenes.map((text, i) => `Scene ${i + 1}: ${text}`).join("\n")
        );
    }

    parts.push(`## Student's scene to review\n${studentText}`);

    const retrievedChunkIds = [
        ...ruleHits.map((h) => h.chunk_id),
        ...calibrationHits.map((h) => h.chunk_id),
        ...exampleHits.map((h) => h.chunk_id),
    ];

    return {
        system: SYSTEM_INSTRUCTIONS,
        user: parts.join("\n\n"),
        retrievedChunkIds,
    };
}

/**
 * End-of-story content prompt: the whole story, plus (for a retelling) the
 * story's model version and required plot beats to check completeness against.
 */
export async function assembleContentPrompt(
    scenes: string[],
    opts: { storyId?: string } = {}
): Promise<AssembledPrompt> {
    const { storyId } = opts;
    const storyCards = storyId
        ? await getChunksByIds([`story_prompt:${storyId}`, `model_story:${storyId}`])
        : [];

    const parts: string[] = [];

    if (storyCards.length) {
        parts.push(RETELLING_NOTE);
        const modelCard = storyCards.find((c) => c.chunk_type === "model_story");
        const promptCard = storyCards.find((c) => c.chunk_type === "story_prompt");
        if (modelCard) {
            parts.push(`### Model version of this story\n${modelCard.text}`);
        }
        if (promptCard) {
            parts.push(`### Required plot beats\n${promptCard.text}`);
        }
    }

    parts.push(
        `## Student's complete story to review (${scenes.length} scenes)\n` +
            scenes.map((text, i) => `Scene ${i + 1}: ${text}`).join("\n")
    );

    return {
        system: CONTENT_INSTRUCTIONS,
        user: parts.join("\n\n"),
        retrievedChunkIds: storyCards.map((h) => h.chunk_id),
    };
}
