// GENERATED from eval/stages.json (stage S7-6, resolved with its prompt overrides) by
// eval/s7/export_production_config.mjs -- do not edit by hand; regenerate instead, so the
// app runs exactly the configuration the evaluation measured.
import type { StageFlags, PromptOverrides } from "@/lib/rag/promptStages";

export const S7_6_FLAGS: StageFlags = {
    "critique": true,
    "sceneList": true,
    "vocab": true,
    "coherence": true,
    "critiqueRetrieval": false,
    "vocabExamples": true,
    "teacherRules": true,
    "noSceneNumbers": true,
    "citeRules": true,
    "sceneVerdicts": true,
    "ruleCardTriggers": true,
    "sentenceCards": true
};

export const S7_6_OVERRIDES: PromptOverrides = {
    "fragments": {
        "rule8": "8. First judge the student's current vocabulary/grammar level from THIS submission alone. Vocabulary suggestions help the student learn words worth knowing: look for words that are correct but plain, general, or vague (like 好了, 新, 写, 麻烦, 随便 in the teacher's examples) where a more precise or more vivid word exists. The point of a suggestion is precision: the alternative must say more exactly how much, which kind, or in what way (好了 -> 好多了 / 痊愈了; 新 -> 陌生 / 未尝过的; 随便 -> 胡乱 / 贸然). A more written word can come with that, but a more formal tone alone is never a reason to suggest a word (not 玩 -> 玩耍, 死 -> 丧命, 住 -> 居住). Every suggestion must keep the student's meaning, keep the same strength (neither weaker nor exaggerated), fit the neighbouring words and the grammar of the sentence, and suit the tone of the story. Do not suggest an alternative for a word that is already precise and fitting -- an equally common synonym is not a suggestion.",
        "vocabOutput": "## Vocabulary Suggestions\nWords worth learning, NOT error-flagging. Pick 1-3 words the student used that are correct but plain, general, or vague, and for each offer one or two alternatives that are more precise or more expressive in this exact sentence (see rule 8 and the teacher's examples in the user message). Before keeping a suggestion, put it into the student's sentence and check that the sentence is still correct, natural, and means the same thing; drop it if not. Write exactly \"- No suggestions.\" only if no word in this scene has such an alternative. Do not claim the student's word is wrong -- if it IS wrong, it belongs in Grammar Corrections instead, and must not also appear here.\n  Format each line as -- the student's word -- the phrase they used it in：alternative，English explanation of what it adds in this context；alternative，English explanation\n  Style example (one of the teacher's): 写 -- \"他也写了每个植物的大小、长短和颜色\"：记下, emphasizes recording the discovery so that it is kept；记载, more written, often used for recording information or knowledge",
        "outputRules": "Rules for the output: keep each \"## \" heading on its own line exactly as written. Put every feedback item on its own line beginning with \"- \". Never run multiple items together on one line. In Grammar Corrections, if there is nothing to flag the section's only line is \"- Nothing to flag.\" In Vocabulary Suggestions, if no word needs a suggestion the section's only line is \"- No suggestions.\" In Coherence & Expressiveness, if there are no coherence errors, give only the expressiveness items.",
        "grammarHeading": "Grammar & Vocabulary Corrections"
    },
    "extraRules": []
};

export const S7_6_REASONING_EFFORT = "medium" as const;
