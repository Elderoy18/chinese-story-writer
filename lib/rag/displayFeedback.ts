/**
 * What learners (and the teacher reviewing feedback) see, from the model's raw feedback.
 *
 * The raw text carries two things meant only for the system and its evaluation:
 *   - rule citations at the end of each error item (S7-2: "[rule: aspect_le_completed]",
 *     "[teacher rule: bieren]", "[vocab list]", "[rule: none]") -- they make the model commit
 *     to one rule and let the evaluation check retrieval vs generation;
 *   - the end-of-story "## Scene check" section (S7-3: one verdict per required scene) --
 *     learners see only the bulleted list of missed content (eval/S7_plan.md, D4).
 * Both stay in the stored raw feedback; this removes them for display.
 * eval/export_feedback.py applies the same rules to the review markdown.
 */

const CITATION = /\s*\[(?:rule|teacher rule)\s*:[^\]\n]*\]|\s*\[vocab list\]/gi;

/** Remove the rule citations from feedback text. */
export function stripCitations(text: string): string {
    return text.replace(CITATION, "");
}

/** Remove the "## Scene check" section (up to the next "## " heading). */
export function stripSceneCheck(text: string): string {
    return text.replace(/^##\s*Scene check[^\n]*\n[\s\S]*?(?=^##\s|(?![\s\S]))/m, "");
}

/** Learner-facing version of scene or end-of-story feedback. */
export function feedbackForDisplay(text: string): string {
    return stripSceneCheck(stripCitations(text)).replace(/\n{3,}/g, "\n\n").trim();
}
