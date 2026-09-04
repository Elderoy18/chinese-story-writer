/**
 * Retelling prompts: stories a student can retell "in their own words" after
 * watching the video + taking the quiz on the Traditional Stories page.
 *
 * The key is the corpus `story_id` used by the RAG pipeline — it must match a
 * `story_prompt:<id>` / `model_story:<id>` chunk in `rag_chunks` (see
 * chinese_writing_rag_pipeline/chunks/chunks.jsonl). Only stories that have BOTH
 * an in-app video and a derived scene checklist belong here.
 *
 * To add one: give it a `story_prompt` chunk with a non-empty scene checklist
 * (re-run the pipeline on graded samples), add a matching video to
 * app/traditional-stories/page.tsx, then add an entry here.
 */
export interface Retelling {
    storyId: string;      // corpus story_id
    title: string;        // Chinese title shown to the student
    videoId: string;      // YouTube id, for the "rewatch" link while writing
}

export const RETELLINGS: Record<string, Retelling> = {
    shennong_chang_baicao: {
        storyId: "shennong_chang_baicao",
        title: "神农尝百草",
        videoId: "_f4RiobBY0Q",
    },
    // mengmu_san_qian: has a checklist but no in-app video yet.
};

export function getRetelling(storyId: string | null | undefined): Retelling | null {
    if (!storyId) return null;
    return RETELLINGS[storyId] ?? null;
}
