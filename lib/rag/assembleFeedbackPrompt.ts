import { searchChunks, getChunksByIds, getChunksByType } from "@/lib/rag/retrieve";
import {
    assembleStagePrompt,
    assembleStageContentPrompt,
    buildSystemPrompt,
    PRODUCTION_FLAGS,
    type AssembleOpts,
    type AssembledPrompt,
    type Retriever,
} from "@/lib/rag/promptStages";

export { CONTENT_INSTRUCTIONS } from "@/lib/rag/promptStages";
export type { AssembledPrompt } from "@/lib/rag/promptStages";

/**
 * The per-scene feedback prompt the app sends: every human-in-the-loop
 * iteration switched on (see lib/rag/promptStages.ts for each stage's pieces).
 * Rules 1-6 map directly to the 5 failure modes the supervising teacher
 * identified in her review of the old feedback system. Rules 7-8 are her later
 * notes: keep prose in English, and keep vocabulary suggestions matched to the
 * student's own demonstrated level. The coherence rules and the Coherence &
 * Expressiveness section come from her "metrics/scale" notes. Plot/content
 * completeness is NOT checked per scene -- that happens once, after END STORY
 * (CONTENT_INSTRUCTIONS).
 */
export const SYSTEM_INSTRUCTIONS = buildSystemPrompt(PRODUCTION_FLAGS);

/** Production retrieval: Atlas $vectorSearch over rag_chunks. */
const atlasRetriever: Retriever = {
    search: (text, opts) => searchChunks(text, opts),
    byIds: getChunksByIds,
    byType: getChunksByType,
};

/**
 * Given one student scene, always-inject the reference/temporality rule cards,
 * retrieve the relevant grammar rule cards + nearby correction exemplars,
 * always-inject the calibration guardrails, include the earlier scenes as
 * coherence context, add the teacher's vocabulary error entries that match the
 * scene, then assemble the final prompt for the feedback LLM. Plot/content
 * checking is left to assembleContentPrompt.
 */
export function assembleFeedbackPrompt(
    studentText: string,
    opts: AssembleOpts = {}
): Promise<AssembledPrompt> {
    return assembleStagePrompt(studentText, opts, PRODUCTION_FLAGS, atlasRetriever);
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
    return assembleStageContentPrompt(scenes, opts, PRODUCTION_FLAGS, atlasRetriever);
}
