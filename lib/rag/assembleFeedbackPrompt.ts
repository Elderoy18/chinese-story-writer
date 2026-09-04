import { searchChunks, getChunksByIds, RetrievedChunk } from "@/lib/rag/retrieve";

/**
 * The feedback rules. Rules 1-7 map directly to the 5 failure modes the
 * supervising teacher identified in her review of the old feedback system
 * (originally from chinese_writing_rag_pipeline/scripts/assemble_feedback_prompt.py).
 * Rules 8-9 are her later notes: keep prose in English, and keep vocabulary
 * suggestions matched to the student's own demonstrated level.
 */
export const SYSTEM_INSTRUCTIONS = `You are a Chinese-language writing tutor giving feedback to an early learner on a short narrative writing assignment. Follow these rules, which come directly from the supervising teacher's review of this system's past mistakes:

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

Rules for the output: keep each "## " heading on its own line exactly as written. Put every feedback item on its own line beginning with "- ". Never run multiple items together on one line. In Grammar Corrections and Content & Coverage, if there is nothing to flag the section's only line is "- Nothing to flag." -- but Vocabulary Suggestions must always have at least 5 items.`;

/**
 * Extra instruction appended only for retellings, where "Content & Coverage" has
 * a real checklist to compare against.
 */
const RETELLING_NOTE = `This is a RETELLING of a known story. The required plot beats and a model version are given below. In "Content & Coverage", check the student's retelling against every required beat: name each beat that is missing, out of order, or misremembered. Beats the student covered correctly do NOT need to be listed.`;

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
 * correction exemplars, always-inject the calibration guardrails, and (for a
 * retelling) the story's model exemplar + derived scene checklist, then assemble
 * the final prompt for the feedback LLM.
 */
export async function assembleFeedbackPrompt(
    studentText: string,
    opts: AssembleOpts = {}
): Promise<AssembledPrompt> {
    const { storyId, topRules = 4, topCalibration = 3, topExamples = 3 } = opts;
    const isRetelling = Boolean(storyId);

    const [ruleHits, exampleHits, calibrationAll, storyCards] = await Promise.all([
        searchChunks(studentText, { chunkTypes: ["rule_card"], k: topRules }),
        searchChunks(studentText, {
            chunkTypes: ["correction_item"],
            k: topExamples,
            storyId: isRetelling ? storyId : undefined,
        }),
        getChunksByIds(PRIORITY_EVAL_CARD_IDS),
        isRetelling
            ? getChunksByIds([`story_prompt:${storyId}`, `model_story:${storyId}`])
            : Promise.resolve([] as RetrievedChunk[]),
    ]);
    const calibrationHits = calibrationAll.slice(0, topCalibration);

    const parts: string[] = [];

    // Retelling context first, so it frames everything below.
    if (isRetelling && storyCards.length) {
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

    parts.push(`## Student's story to review\n${studentText}`);

    const retrievedChunkIds = [
        ...storyCards.map((h) => h.chunk_id),
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
