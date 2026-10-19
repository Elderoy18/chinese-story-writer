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

/**
 * The same clean-up for text that arrives in pieces (a streamed model response).
 * Text is passed on a whole line at a time, so a citation is never shown half-written
 * and the "## Scene check" section is held back until the next "## " heading.
 *   const f = displayStreamFilter();  out(f.push(delta)) ... out(f.flush())
 */
export function displayStreamFilter() {
    let pending = "";
    let inSceneCheck = false;
    const line = (l: string): string => {
        if (/^##\s*Scene check/i.test(l)) {
            inSceneCheck = true;
            return "";
        }
        if (/^##\s/.test(l)) inSceneCheck = false;
        return inSceneCheck ? "" : stripCitations(l) + "\n";
    };
    return {
        push(delta: string): string {
            pending += delta;
            let out = "";
            let nl: number;
            while ((nl = pending.indexOf("\n")) >= 0) {
                out += line(pending.slice(0, nl));
                pending = pending.slice(nl + 1);
            }
            return out;
        },
        flush(): string {
            const out = pending ? line(pending).replace(/\n$/, "") : "";
            pending = "";
            return out;
        },
    };
}
