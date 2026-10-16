/**
 * Two-pass feedback with structured JSON output.
 *
 *   Pass 1 (find):  the model lists candidate errors in the scene as JSON
 *                   (exact span, category, rule name, short reason). Each span is
 *                   checked against the student's text; spans that do not occur
 *                   there are dropped.
 *   Retrieval:      for each surviving candidate, the rule card named by its
 *                   rule, the teacher's corrections labelled with that rule that
 *                   are most similar to the span, and (for word problems) the
 *                   most similar entries of the teacher's vocabulary error list.
 *   Pass 2 (write): the model confirms or rejects each candidate (and may add
 *                   missed ones) and writes the feedback as JSON. Every quoted
 *                   span is checked against the student's text again; items that
 *                   fail are dropped. The JSON is rendered to the same Markdown
 *                   sections the app shows.
 *
 * The LLM call is injected (JsonLLM), so this file has no network code and runs
 * both in the app and in the evaluation harness.
 */
import {
    buildSystemPrompt,
    findTeacherRuleHits,
    formatErrorCard,
    formatRuleCard,
    formatTeacherRules,
    matchVocabTriggers,
    PRIORITY_EVAL_CARD_IDS,
    PRIORITY_RULE_CARD_IDS,
    type AssembleOpts,
    type PromptOverrides,
    type RetrievedChunk,
    type Retriever,
    type StageFlags,
} from "./promptStages.ts";

/** One structured-output call: returns the parsed JSON object. */
export type JsonLLM = (call: {
    pass: "find" | "write";
    system: string;
    user: string;
    schemaName: string;
    schema: Record<string, unknown>;
}) => Promise<unknown>;

const CATEGORIES = ["grammar", "vocabulary", "reference", "temporality", "conjunction"] as const;
type Category = (typeof CATEGORIES)[number];

export interface Candidate {
    span: string;
    category: Category;
    rule: string;
    why: string;
}

const MAX_CANDIDATES = 15;
const EXAMPLES_PER_CANDIDATE = 2;
const VOCAB_PER_CANDIDATE = 2;

// ---------------------------------------------------------------------------
// Span checking
// ---------------------------------------------------------------------------
const squash = (s: string) => s.replace(/\s+/g, "");
const bare = (s: string) => s.replace(/[\s\p{P}\p{S}]/gu, "");

/** True if the quoted span occurs in the student's text (ignoring spaces, then punctuation). */
export function spanInText(span: string, text: string): boolean {
    if (!span.trim()) return false;
    if (squash(text).includes(squash(span))) return true;
    const b = bare(span);
    return b.length > 0 && bare(text).includes(b);
}

// ---------------------------------------------------------------------------
// Schemas (OpenAI structured outputs, strict mode: every property required)
// ---------------------------------------------------------------------------
const obj = (properties: Record<string, unknown>) => ({
    type: "object",
    properties,
    required: Object.keys(properties),
    additionalProperties: false,
});
const str = { type: "string" };

const FIND_SCHEMA = obj({
    errors: {
        type: "array",
        items: obj({ span: str, category: { type: "string", enum: [...CATEGORIES] }, rule: str, why: str }),
    },
});

const WRITE_SCHEMA = obj({
    corrections: {
        type: "array",
        items: obj({ original: str, corrected: str, explanation: str, kind: { type: "string", enum: ["grammar", "vocabulary"] } }),
    },
    vocabulary_suggestions: {
        type: "array",
        items: obj({ word: str, phrase: str, alternatives: { type: "array", items: obj({ word: str, explanation: str }) } }),
    },
    coherence: {
        type: "array",
        items: obj({
            type: { type: "string", enum: ["Reference", "Temporality", "Conjunction"] },
            original: str,
            corrected: str,
            explanation: str,
        }),
    },
    expressiveness: { type: "array", items: str },
    encouragement: str,
});

interface WriteOutput {
    corrections: { original: string; corrected: string; explanation: string; kind: string }[];
    vocabulary_suggestions: { word: string; phrase: string; alternatives: { word: string; explanation: string }[] }[];
    coherence: { type: string; original: string; corrected: string; explanation: string }[];
    expressiveness: string[];
    encouragement: string;
}

// ---------------------------------------------------------------------------
// Prompts
// ---------------------------------------------------------------------------
function findSystemPrompt(f: StageFlags, coherenceRules: string): string {
    return [
        "You are the first pass of a feedback system for an early learner of Chinese who wrote ONE scene of a short narrative. Your only job is to FIND errors -- do not explain them to the student.",
        "",
        "List every actual error in the scene: grammar errors, wrong or unsuitable words (用错的词)" +
            (f.coherence ? ", and coherence errors (reference, temporality/aspect, conjunctions)." : "."),
        "- Only actual errors. A phrase that is acceptable Chinese gets no entry, even if another wording is possible.",
        "- Be exhaustive: check every sentence and every clause. Past versions of this system missed many real errors.",
        "- span: copy the wrong part from the student's scene exactly, character for character -- as short as possible while still containing the whole error (a few characters up to one clause). Never rewrite it.",
        "- category: grammar | vocabulary (a wrong or unsuitable word) | reference | temporality | conjunction.",
        "- rule: the name of the rule from the rule list that best matches, or \"other\".",
        "- why: one short English phrase saying what is wrong.",
        "- The text has been cleaned of speech disfluencies; do not flag repetitions as pauses. Do not judge plot or story content.",
        ...(f.coherence ? ["", coherenceRules] : []),
    ].join("\n");
}

const COHERENCE_START = "Coherence rules to apply";

const JSON_OUTPUT_NOTE = `OUTPUT FORMAT OVERRIDE -- return JSON matching the given schema instead of Markdown. The fields map to the sections described above: "corrections" = the error-correction section (kind "grammar" or "vocabulary"), "vocabulary_suggestions" = Vocabulary Suggestions, "coherence" = the coherence items, "expressiveness" = the expressiveness ideas, "encouragement" = Encouragement. An empty section is an empty array -- do not write "Nothing to flag" or "No suggestions" items. Every "original" and every "phrase" must be copied character for character from the student's scene; items whose quoted text does not appear in the scene are discarded.`;

// ---------------------------------------------------------------------------
// Rendering (same Markdown the single-pass prompt produces)
// ---------------------------------------------------------------------------
export function renderMarkdown(out: WriteOutput, f: StageFlags, overrides: PromptOverrides): string {
    const heading = overrides.fragments?.grammarHeading ?? "Grammar Corrections";
    const L: string[] = [`## ${heading}`];
    L.push(...(out.corrections.length ? out.corrections.map((c) => `- ${c.original}：${c.corrected}，${c.explanation}`) : ["- Nothing to flag."]));
    L.push("", "## Vocabulary Suggestions");
    L.push(
        ...(out.vocabulary_suggestions.length
            ? out.vocabulary_suggestions.map(
                  (v) => `- ${v.word} -- “${v.phrase}”：` + v.alternatives.map((a) => `${a.word}，${a.explanation}`).join("；")
              )
            : ["- No suggestions."])
    );
    if (f.coherence) {
        L.push("", "## Coherence & Expressiveness");
        L.push(...out.coherence.map((c) => `- Coherence (${c.type}): ${c.original}：${c.corrected}，${c.explanation}`));
        L.push(...out.expressiveness.map((e) => `- Expressiveness: ${e}`));
    }
    L.push("", "## Encouragement", out.encouragement);
    return L.join("\n");
}

// ---------------------------------------------------------------------------
// The two passes
// ---------------------------------------------------------------------------
export interface TwoPassResult {
    feedback: string; // rendered Markdown
    retrievedChunkIds: string[];
    find: { system: string; user: string; candidates: Candidate[]; dropped: (Candidate & { reason: string })[] };
    write: { system: string; user: string; output: WriteOutput; dropped: { section: string; item: unknown; reason: string }[] };
}

export async function runTwoPass(
    studentText: string,
    opts: AssembleOpts,
    f: StageFlags,
    r: Retriever,
    llm: JsonLLM,
    overrides: PromptOverrides = {}
): Promise<TwoPassResult> {
    const { storyId } = opts;
    const previousScenes = f.coherence ? opts.previousScenes ?? [] : [];
    const writeSystem = buildSystemPrompt(f, overrides) + "\n\n" + JSON_OUTPUT_NOTE;
    const coherenceRules = writeSystem.includes(COHERENCE_START)
        ? writeSystem.slice(writeSystem.indexOf(COHERENCE_START), writeSystem.indexOf("Output format --"))
        : "";

    const none = Promise.resolve([] as RetrievedChunk[]);
    const [ruleCards, teacherRules, vocabAll, vocabSemantic, pinnedRules, guardrails, suggestionExamples, modelStory] =
        await Promise.all([
            r.byType("rule_card"),
            f.teacherRules ? r.byType("teacher_rule") : none,
            f.vocab ? r.byType("vocab_error") : none,
            f.vocab ? r.search(studentText, { chunkTypes: ["vocab_error"], k: 3 }) : none,
            f.coherence ? r.byIds(PRIORITY_RULE_CARD_IDS) : none,
            r.byIds(PRIORITY_EVAL_CARD_IDS),
            f.vocabExamples ? r.byType("vocab_suggestion_example") : none,
            f.coherence && storyId ? r.byIds([`model_story:${storyId}`]) : none,
        ]);
    const cardByRule = new Map(ruleCards.map((c) => [c.grammar_tag ?? c.chunk_id.replace(/^rule_card:/, ""), c]));
    const teacherHits = findTeacherRuleHits(studentText, teacherRules);
    const vocabHits = f.vocab ? matchVocabTriggers(studentText, vocabAll, storyId || undefined) : [];
    for (const v of vocabSemantic) if (!vocabHits.some((h) => h.chunk_id === v.chunk_id)) vocabHits.push(v);

    // ---- pass 1: find -------------------------------------------------------
    const ruleList = [...cardByRule.entries()].map(([rule, card]) => `- ${rule}: ${card.text.split("\n")[1] ?? ""}`);
    const findUser = [
        previousScenes.length
            ? "## Earlier scenes (context only -- do not list errors in these)\n" + previousScenes.map((t) => `- ${t}`).join("\n")
            : "",
        teacherRules.length ? formatTeacherRules(teacherRules, teacherHits) : "",
        vocabHits.length
            ? "## Teacher's vocabulary error list -- entries that may apply to this scene\n" + vocabHits.map((h) => `- ${h.text}`).join("\n")
            : "",
        "## Rule list (use these names in \"rule\")\n" + ruleList.join("\n"),
        `## Student's scene\n${studentText}`,
    ].filter(Boolean).join("\n\n");
    const findSystem = findSystemPrompt(f, coherenceRules);
    const found = (await llm({ pass: "find", system: findSystem, user: findUser, schemaName: "candidate_errors", schema: FIND_SCHEMA })) as {
        errors: Candidate[];
    };

    const candidates: Candidate[] = [];
    const findDropped: (Candidate & { reason: string })[] = [];
    for (const c of found.errors ?? []) {
        if (!spanInText(c.span, studentText)) findDropped.push({ ...c, reason: "span not in the student's text" });
        else if (candidates.some((k) => squash(k.span) === squash(c.span) && k.rule === c.rule)) findDropped.push({ ...c, reason: "duplicate" });
        else if (candidates.length >= MAX_CANDIDATES) findDropped.push({ ...c, reason: "over the candidate limit" });
        else candidates.push(c);
    }

    // ---- retrieval per candidate ------------------------------------------
    const usedCards = new Map<string, RetrievedChunk>();
    const evidence = await Promise.all(
        candidates.map(async (c) => {
            const card = cardByRule.get(c.rule);
            if (card) usedCards.set(card.chunk_id, card);
            let examples = card
                ? await r.search(c.span, { chunkTypes: ["correction_item"], k: EXAMPLES_PER_CANDIDATE, grammarTag: c.rule })
                : [];
            if (!examples.length) {
                examples = await r.search(c.span, { chunkTypes: ["correction_item"], k: EXAMPLES_PER_CANDIDATE, storyId: storyId || undefined });
            }
            const vocab = f.vocab && c.category === "vocabulary"
                ? await r.search(c.span, { chunkTypes: ["vocab_error"], k: VOCAB_PER_CANDIDATE })
                : [];
            return { c, card, examples, vocab };
        })
    );

    // ---- pass 2: write ----------------------------------------------------
    const parts: string[] = [];
    const cards = [...pinnedRules, ...[...usedCards.values()].filter((c) => !pinnedRules.some((p) => p.chunk_id === c.chunk_id))];
    if (cards.length) {
        parts.push("## Rule cards for the candidate errors (ground your explanations in these)");
        for (const card of cards) parts.push(formatRuleCard(card));
    }
    if (guardrails.length) {
        parts.push("## AI-feedback calibration guardrails (avoid repeating these documented failure modes)");
        for (const g of guardrails) parts.push(formatErrorCard(g));
    }
    if (teacherRules.length) parts.push(formatTeacherRules(teacherRules, []));
    if (suggestionExamples.length) {
        parts.push(
            "## The teacher's examples of good vocabulary suggestions (models of what is worth suggesting: the student's word is correct but plain or general, and each alternative is more precise or expressive in that sentence while keeping its meaning. Use them as models of judgement and format, not as words to reuse; write your own explanations in English)"
        );
        for (const s of suggestionExamples) parts.push(`- ${s.text}`);
    }
    if (modelStory.length) {
        parts.push(
            "## Model version of this story (reference for Expressiveness ideas only -- do NOT use it to judge plot, content, or missing scenes, and do not ask the student to copy its sentences)\n" +
                modelStory[0].text
        );
    }
    if (previousScenes.length) {
        parts.push("## Earlier scenes (context only -- do not give feedback on these)\n" + previousScenes.map((t) => `- ${t}`).join("\n"));
    }
    parts.push(
        "## Candidate errors from a first pass, each with the teacher's material for it\n" +
            "Confirm a candidate only if it really is an error, and write its correction and explanation from the rule card and the teacher's examples. Reject candidates that are acceptable Chinese. You may add an error the first pass missed.\n\n" +
            (evidence.length
                ? evidence
                      .map(({ c, card, examples, vocab }, i) =>
                          [
                              `### Candidate ${i + 1}: “${c.span}” (${c.category}; rule: ${card ? c.rule : "other"}) -- ${c.why}`,
                              ...examples.map((e) => `- teacher's correction of a similar error: ${e.text}`),
                              ...vocab.map((v) => `- teacher's vocabulary list: ${v.text}`),
                          ].join("\n")
                      )
                      .join("\n\n")
                : "(none found)")
    );
    parts.push(`## Student's scene to review\n${studentText}`);
    const writeUser = parts.join("\n\n");

    const raw = (await llm({ pass: "write", system: writeSystem, user: writeUser, schemaName: "feedback", schema: WRITE_SCHEMA })) as WriteOutput;

    // ---- check every quoted span against the student's text ---------------
    const dropped: { section: string; item: unknown; reason: string }[] = [];
    const keep = <T>(section: string, items: T[], quoted: (t: T) => string[]) =>
        items.filter((it) => {
            const bad = quoted(it).find((q) => !spanInText(q, studentText));
            if (bad !== undefined) dropped.push({ section, item: it, reason: `“${bad}” is not in the student's text` });
            return bad === undefined;
        });
    const output: WriteOutput = {
        corrections: keep("corrections", raw.corrections ?? [], (c) => [c.original]),
        vocabulary_suggestions: keep("vocabulary_suggestions", raw.vocabulary_suggestions ?? [], (v) => [v.phrase, v.word]),
        coherence: f.coherence ? keep("coherence", raw.coherence ?? [], (c) => [c.original]) : [],
        expressiveness: f.coherence ? raw.expressiveness ?? [] : [],
        encouragement: raw.encouragement ?? "",
    };

    const retrievedChunkIds = [
        ...cards.map((c) => c.chunk_id),
        ...guardrails.map((g) => g.chunk_id),
        ...teacherRules.map((t) => t.chunk_id),
        ...vocabHits.map((v) => v.chunk_id),
        ...suggestionExamples.map((s) => s.chunk_id),
        ...modelStory.map((m) => m.chunk_id),
        ...new Set(evidence.flatMap((e) => [...e.examples, ...e.vocab].map((x) => x.chunk_id))),
    ];

    return {
        feedback: renderMarkdown(output, f, overrides),
        retrievedChunkIds,
        find: { system: findSystem, user: findUser, candidates, dropped: findDropped },
        write: { system: writeSystem, user: writeUser, output, dropped },
    };
}
