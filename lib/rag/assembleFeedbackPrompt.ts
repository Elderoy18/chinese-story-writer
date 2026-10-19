import { searchChunks, getChunksByIds, getChunksByType } from "@/lib/rag/retrieve";
import {
    assembleStagePrompt,
    assembleStageContentPrompt,
    buildSystemPrompt,
    PRODUCTION_FLAGS,
    type AssembleOpts,
    type AssembledPrompt,
    type PromptOverrides,
    type Retriever,
    type StageFlags,
} from "@/lib/rag/promptStages";
import { S7_6_FLAGS, S7_6_OVERRIDES, S7_6_REASONING_EFFORT } from "@/lib/rag/s7_6Config";

export { CONTENT_INSTRUCTIONS } from "@/lib/rag/promptStages";
export type { AssembledPrompt } from "@/lib/rag/promptStages";

/**
 * Which evaluated configuration the app runs, chosen by the FEEDBACK_CONFIG
 * environment variable:
 *   "s7-6" (default) -- stage S7-6, the configuration the supervising teacher chose
 *                       after the S7 evaluation (eval/S7_plan.md): her rules and
 *                       critique cards, rule citations and standard fixes, the
 *                       end-of-story scene check, rule-card triggers and rule cards
 *                       found through the student sentences she corrected; reasoning
 *                       effort medium. Flags and prompt text are generated from the
 *                       evaluated stage (lib/rag/s7_6Config.ts).
 *   "s4"             -- the previous production setup (S1-S4 iterations, low effort),
 *                       kept as an instant fallback: set FEEDBACK_CONFIG=s4 and
 *                       restart, no code change.
 * Rules 1-6 of the system prompt map to the 5 failure modes the teacher found in
 * the old feedback system; plot/content completeness is checked once, after END
 * STORY (assembleContentPrompt), not per scene.
 */
interface FeedbackConfig {
    name: "s7-6" | "s4";
    flags: StageFlags;
    overrides: PromptOverrides;
    reasoningEffort: "low" | "medium";
}

const CONFIGS: Record<FeedbackConfig["name"], FeedbackConfig> = {
    "s7-6": { name: "s7-6", flags: S7_6_FLAGS, overrides: S7_6_OVERRIDES, reasoningEffort: S7_6_REASONING_EFFORT },
    s4: { name: "s4", flags: PRODUCTION_FLAGS, overrides: {}, reasoningEffort: "low" },
};

export const FEEDBACK_CONFIG: FeedbackConfig =
    CONFIGS[(process.env.FEEDBACK_CONFIG ?? "s7-6").trim().toLowerCase() as FeedbackConfig["name"]] ?? CONFIGS["s7-6"];

export const SYSTEM_INSTRUCTIONS = buildSystemPrompt(FEEDBACK_CONFIG.flags, FEEDBACK_CONFIG.overrides);

/** Production retrieval: Atlas $vectorSearch over rag_chunks. */
const atlasRetriever: Retriever = {
    search: (text, opts) => searchChunks(text, opts),
    byIds: getChunksByIds,
    byType: getChunksByType,
};

/**
 * The prompt for one student scene under the active configuration: pinned and
 * retrieved rule cards, calibration guardrails, the teacher's rules, vocabulary
 * entries, correction exemplars, earlier scenes and the model story.
 */
export function assembleFeedbackPrompt(
    studentText: string,
    opts: AssembleOpts = {}
): Promise<AssembledPrompt> {
    return assembleStagePrompt(studentText, opts, FEEDBACK_CONFIG.flags, atlasRetriever, FEEDBACK_CONFIG.overrides);
}

/**
 * End-of-story content prompt: the whole story, plus (for a retelling) the
 * teacher's required scenes to check completeness against. The model story is
 * not used here -- it is the per-scene reference for expressiveness.
 */
export function assembleContentPrompt(
    scenes: string[],
    opts: { storyId?: string } = {}
): Promise<AssembledPrompt> {
    return assembleStageContentPrompt(scenes, opts, FEEDBACK_CONFIG.flags, atlasRetriever, FEEDBACK_CONFIG.overrides);
}
