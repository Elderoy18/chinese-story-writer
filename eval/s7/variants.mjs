// Variant inputs for the retrieval / generation / end-to-end consistency split
// (eval/S7_plan.md, Phase 2; the paper's paraphrase consistency, adapted).
//
//   node eval/s7/variants.mjs <stage> [--modes fixed,own] [--limit N]
//     -> eval/runs/<stage>/variants/<variant_id>.json
//
// For each of her corrections on the test set (a "target error"), the variant
// is its scene with HER OTHER corrections in that scene applied, so the target
// error is the only one left and stays word for word. The same error, a
// different input -- built from her data, no LLM rewriting.
//
// Each variant is run once in up to two modes:
//   fixed -- the generator gets the ORIGINAL scene's retrieved chunks (its stored
//            prompt, with the scene text swapped): differences = generation only.
//   own   -- the variant does its own retrieval (assembleStagePrompt): the whole
//            pipeline varies, as for any new input = end-to-end.
// The original scene's runs (eval/runs/<stage>*/) are the comparison.
// Scored by eval/s7/variants_score.py.

import fs from "node:fs";
import path from "node:path";
import { assembleStagePrompt, buildSystemPrompt } from "../../lib/rag/promptStages.ts";
import {
    EVAL_DIR, FEEDBACK_MODEL, REASONING_EFFORT, loadSnapshot, makeRetriever, openai, readJson,
    resolveStage, runDir, sampleKey, withRetry, writeJson,
} from "../lib.mjs";

const args = process.argv.slice(2);
const stageId = args[0];
if (!stageId || stageId.startsWith("--")) {
    console.error("usage: node eval/s7/variants.mjs <stage> [--modes fixed,own] [--limit N]");
    process.exit(1);
}
const mIdx = args.indexOf("--modes");
const modes = mIdx > -1 ? args[mIdx + 1].split(",") : ["fixed", "own"];
const lIdx = args.indexOf("--limit");
const limit = lIdx > -1 ? Number(args[lIdx + 1]) : Infinity;
const CONCURRENCY = 6;

const stage = resolveStage(stageId);
const effort = stage.reasoningEffort ?? REASONING_EFFORT;
const testSet = readJson(path.join(EVAL_DIR, stage.testSet));
const retriever = makeRetriever(await loadSnapshot(stage.snapshot));
const system = buildSystemPrompt(stage.flags, stage.overrides);
const outDir = path.join(runDir(stageId), "variants");
fs.mkdirSync(outDir, { recursive: true });

const ERROR_OPS = new Set(["replace", "delete", "insert"]);
const firstAlt = (s) => (s ?? "").split("/")[0];

function sceneOffsets(text, scenes) {
    const out = [];
    let pos = 0;
    for (const sc of scenes) {
        pos = text.indexOf(sc, pos);
        out.push([pos, pos + sc.length]);
        pos += sc.length;
    }
    return out;
}

/** Apply edits (whole-story positions) inside [lo, hi) of text; return the new scene text
 *  and a function mapping an old position in the scene to its new position. */
function applyEdits(text, lo, hi, edits) {
    const sorted = [...edits].sort((a, b) => a.start - b.start);
    let out = "", pos = lo;
    const shifts = []; // [oldPos, delta after it]
    let delta = 0;
    for (const e of sorted) {
        if (e.start < pos) continue; // overlapping: skip
        out += text.slice(pos, e.start) + firstAlt(e.corrected);
        delta += firstAlt(e.corrected).length - (e.end - e.start);
        shifts.push([e.end, delta]);
        pos = e.end;
    }
    out += text.slice(pos, hi);
    const map = (p) => {
        let d = 0;
        for (const [at, dl] of shifts) if (p >= at) d = dl;
        return p - lo + d;
    };
    return { text: out, map };
}

function buildVariants() {
    const variants = [];
    for (const s of testSet.samples) {
        const offs = sceneOffsets(s.raw_text, s.scenes);
        const edits = s.gold.aligned_edits.filter((e) => e.start != null && ERROR_OPS.has(e.op) && e.her_decision !== "no");
        const byLine = new Map();
        for (const e of edits) byLine.set(e.her_line, [...(byLine.get(e.her_line) ?? []), e]);
        s.gold.corrections.forEach((g, li) => {
            const target = byLine.get(g.text);
            if (!target) return;
            const si = offs.findIndex(([lo, hi]) => lo <= target[0].start && target[0].start <= hi);
            const [lo, hi] = offs[si];
            if (!target.every((e) => lo <= e.start && e.end <= hi)) return; // spans two scenes
            const overlapsTarget = (e) => target.some((t) => e.start < Math.max(t.end, t.start + 1) && t.start < Math.max(e.end, e.start + 1));
            const others = edits.filter((e) => e.her_line !== g.text && lo <= e.start && e.end <= hi && !overlapsTarget(e));
            if (!others.length) return; // nothing else to change: the variant would equal the original
            const { text, map } = applyEdits(s.raw_text, lo, hi, others);
            const tStart = Math.min(...target.map((e) => e.start)), tEnd = Math.max(...target.map((e) => e.end));
            const vStart = map(tStart), vEnd = map(tEnd);
            if (text.slice(vStart, vEnd) !== s.raw_text.slice(tStart, tEnd)) throw new Error(`target moved: ${s.sample_id} ${g.text}`);
            variants.push({
                variant_id: `${sampleKey(s.sample_id)}_s${si + 1}_c${li}`, sample_id: s.sample_id, story_id: s.story_id,
                scene: si + 1, her_line: g.text, rules: g.rules, original_scene: s.scenes[si], variant_scene: text,
                previous_scenes: s.scenes.slice(0, si),
                target_original: { start: tStart - lo, end: tEnd - lo },
                target_variant: { start: vStart, end: vEnd },
                target_edits_variant: target.map((e) => ({ ...e, start: map(e.start), end: map(e.end) })),
                n_other_edits_applied: others.length,
            });
        });
    }
    return variants;
}

async function complete(user) {
    const t0 = Date.now();
    const res = await withRetry(() => openai().chat.completions.create({
        model: FEEDBACK_MODEL, reasoning_effort: effort,
        messages: [{ role: "system", content: system }, { role: "user", content: user }],
    }), "variant feedback call");
    return { text: res.choices[0]?.message?.content ?? "", usage: res.usage, ms: Date.now() - t0 };
}

async function runVariant(v) {
    const out = path.join(outDir, `${v.variant_id}.json`);
    const rec = fs.existsSync(out) ? readJson(out) : { ...v, stage: stageId, model: FEEDBACK_MODEL, reasoning_effort: effort };
    const orig = readJson(path.join(runDir(stageId), `${sampleKey(v.sample_id)}.json`)).scenes[v.scene - 1];
    rec.original_retrieved = orig.retrieved;
    if (modes.includes("own") && !rec.own) {
        const p = await assembleStagePrompt(v.variant_scene, { storyId: v.story_id, previousScenes: v.previous_scenes },
            stage.flags, retriever, stage.overrides);
        rec.own = { retrieved: p.retrievedChunkIds, user: p.user, ...(await complete(p.user)) };
    }
    if (modes.includes("fixed") && !rec.fixed) {
        const header = "## Student's scene to review\n";
        const i = orig.prompt.user.lastIndexOf(header + v.original_scene);
        if (i < 0) throw new Error(`stored prompt has no scene section: ${v.variant_id}`);
        const user = orig.prompt.user.slice(0, i) + header + v.variant_scene + orig.prompt.user.slice(i + header.length + v.original_scene.length);
        rec.fixed = { retrieved: orig.retrieved, user, ...(await complete(user)) };
    }
    writeJson(out, rec);
}

const variants = buildVariants().slice(0, limit);
writeJson(path.join(outDir, "_index.json"), { stage: stageId, modes, n: variants.length, ids: variants.map((v) => v.variant_id) });
console.log(`${stageId}: ${variants.length} variants (modes: ${modes.join(", ")}) -> ${path.relative(process.cwd(), outDir)}`);
let next = 0, done = 0, failed = 0;
await Promise.all(Array.from({ length: CONCURRENCY }, async () => {
    while (next < variants.length) {
        const v = variants[next++];
        try {
            await runVariant(v);
        } catch (e) {
            failed++;
            console.error(`FAILED ${v.variant_id}: ${e.message}`);
        }
        if (++done % 20 === 0) console.log(`  ${done}/${variants.length}`);
    }
}));
console.log(failed ? `${failed} variant(s) failed -- re-run to retry` : `${stageId}: variants complete.`);
process.exitCode = failed ? 1 : 0;
