// Guard: a stage's prompts are still exactly what its stored run used.
//
// Re-renders, from the current code and the stage's frozen snapshot, every prompt
// the stage sent (per scene: system prompt, user prompt, retrieved chunk ids; per
// story: the end-of-story content prompt) and compares them with the prompts
// stored in eval/runs/<stage>/. Any difference means a code or data change has
// altered that stage -- run it after every change to lib/rag/ or the pipeline,
// so S6 stays available unchanged for side-by-side testing.
//
//   node eval/check_stage_unchanged.mjs            (checks S6)
//   node eval/check_stage_unchanged.mjs S6 S5
//
// No LLM calls; query embeddings come from eval/cache (an embedding call is made
// only for a scene text not in the cache). Exit code 1 on any difference.

import fs from "node:fs";
import path from "node:path";
import {
    assembleStagePrompt,
    assembleStageContentPrompt,
    buildSystemPrompt,
} from "../lib/rag/promptStages.ts";
import { loadSnapshot, makeRetriever, readJson, resolveStage, runDir, sha } from "./lib.mjs";

const stages = process.argv.slice(2).length ? process.argv.slice(2) : ["S6"];
const sameList = (a, b) => JSON.stringify(a ?? []) === JSON.stringify(b ?? []);

async function check(stageId) {
    const stage = resolveStage(stageId);
    if (stage.flags.twoPass) throw new Error(`${stageId}: two-pass stages are not covered by this check`);
    const dir = runDir(stageId);
    const stored = readJson(path.join(dir, "stage.json"));
    const retriever = makeRetriever(await loadSnapshot(stage.snapshot));
    const diffs = [];

    const system = buildSystemPrompt(stage.flags, stage.overrides);
    if (sha(system) !== stored.system_prompt_sha) diffs.push("system prompt (stage.json)");

    const files = fs.readdirSync(dir).filter((f) => f.endsWith(".json") && f !== "stage.json").sort();
    let nScenes = 0;
    for (const f of files) {
        const run = readJson(path.join(dir, f));
        const texts = run.scenes.map((s) => s.text);
        const opts = { storyId: run.story_id };
        for (let i = 0; i < texts.length; i++) {
            const p = await assembleStagePrompt(texts[i], { ...opts, previousScenes: texts.slice(0, i) },
                stage.flags, retriever, stage.overrides);
            const s = run.scenes[i];
            const where = `${run.sample_id} scene ${i + 1}`;
            if (sha(p.system) !== s.prompt.system_sha) diffs.push(`${where}: system prompt`);
            if (p.user !== s.prompt.user) diffs.push(`${where}: user prompt`);
            if (!sameList(p.retrievedChunkIds, s.retrieved)) diffs.push(`${where}: retrieved chunks`);
            nScenes++;
        }
        const c = await assembleStageContentPrompt(texts, opts, stage.flags, retriever, stage.overrides);
        if (c.system !== run.content.prompt.system) diffs.push(`${run.sample_id} content: system prompt`);
        if (c.user !== run.content.prompt.user) diffs.push(`${run.sample_id} content: user prompt`);
        if (!sameList(c.retrievedChunkIds, run.content.retrieved)) diffs.push(`${run.sample_id} content: retrieved chunks`);
    }
    if (diffs.length) {
        console.log(`${stageId}: CHANGED -- ${diffs.length} difference(s):`);
        for (const d of diffs) console.log(`  - ${d}`);
        return false;
    }
    console.log(`${stageId}: identical (${nScenes} scene prompts + ${files.length} content prompts, snapshot ${stage.snapshot})`);
    return true;
}

let ok = true;
for (const s of stages) ok = (await check(s)) && ok;
process.exitCode = ok ? 0 : 1;
