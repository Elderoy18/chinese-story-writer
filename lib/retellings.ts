/**
 * Retelling prompts: stories a student can retell "in their own words" after
 * watching the video + taking the quiz on the Traditional Stories page.
 *
 * The key is the corpus `story_id` used by the RAG pipeline — it must match a
 * `story_prompt:<id>` / `model_story:<id>` chunk in `rag_chunks` (see
 * chinese_writing_rag_pipeline/chunks/chunks.jsonl), and the `retellId` on the
 * story in app/traditional-stories/page.tsx. The required scenes come from the
 * teacher's scene list (chinese_writing_rag_pipeline/raw/story_scenes.md).
 *
 * To add one: add the story to raw/story_scenes.md (and a model story) and
 * re-run the pipeline, give the story a `retellId` in
 * app/traditional-stories/page.tsx, then add an entry here.
 */
export interface ReferenceWord {
    en: string;           // English gloss / label
    zh: string;           // Chinese term, with pinyin and any note as given
}

export interface Retelling {
    storyId: string;      // corpus story_id
    title: string;        // Chinese title shown to the student
    videoId: string;      // YouTube id, for the "rewatch" link while writing
    words: ReferenceWord[]; // vocab shown in the "You're retelling ..." banner (hidden if empty)
}

export const RETELLINGS: Record<string, Retelling> = {
    shennong_chang_baicao: {
        storyId: "shennong_chang_baicao",
        title: "神农尝百草",
        videoId: "0R55VdnZ-Ec",
        words: [
            { en: "Ancient time", zh: "古代 (gǔdài)" },
            { en: "Plants", zh: "植物 (zhíwù)" },
            { en: "Umbrella", zh: "伞 (sǎn)" },
            { en: "Linzhi mushroom", zh: "灵芝 (língzhī) (the mushroom)" },
            { en: "Poison", zh: "毒 (dú)" },
            { en: "Oleander", zh: "夹竹桃 (jiāzhútáo) (the yellow flower)" },
        ],
    },
    mengmu_san_qian: {
        storyId: "mengmu_san_qian",
        title: "孟母三迁",
        videoId: "0R55VdnZ-Ec",
        words: [
            { en: "Ancient time", zh: "古代 (gǔdài)" },
            { en: "Graveyard", zh: "墓地 (mùdì)" },
            { en: "Make sacrificial offerings", zh: "祭拜 (jìbài)" },
            { en: "Become", zh: "成为 (chéngwéi)" },
        ],
    },
    zhang_qian_chu_shi_xi_yu: {
        storyId: "zhang_qian_chu_shi_xi_yu",
        title: "张骞出使西域",
        videoId: "0R55VdnZ-Ec",
        words: [
            { en: "To grab (take sb. by force)", zh: "抢(qiǎng)" },
            { en: "Friendly", zh: "友好" },
            { en: "To attack", zh: "攻(gōng)打" },
            { en: "Diplomatic corps", zh: "使团 (shǐtuán)" },
            { en: "Guide", zh: "向导 (xiàngdǎo)" },
            { en: "To take prisoner", zh: "俘虏 (fúlǔ)" },
            { en: "Slave", zh: "奴隶 (núlì)" },
            { en: "To herd sheep", zh: "放羊 (fàngyáng)" },
            { en: "To escape", zh: "逃 (táo)" },
            { en: "King/queen", zh: "国王/女王" },
            { en: "Army", zh: "军(jūn)队" },
            { en: "War", zh: "战争 (zhànzhēng)" },
        ],
    },
    chang_e_ben_yue: {
        storyId: "chang_e_ben_yue",
        title: "嫦娥奔月",
        videoId: "0R55VdnZ-Ec",
        words: [
            { en: "God, goddess", zh: "神仙 (shénxiān)" },
            { en: "Human world (on the ground)", zh: "人间 (rénjiān)" },
            { en: "Sun", zh: "太阳 (tàiyang)" },
            { en: "To shoot (using an arrow)", zh: "射(shè)" },
            { en: "Supernatural power", zh: "法力 (fǎlì)" },
            { en: "Moon", zh: "月亮 (yuèliang)" },
        ],
    },
};

export function getRetelling(storyId: string | null | undefined): Retelling | null {
    if (!storyId) return null;
    return RETELLINGS[storyId] ?? null;
}
