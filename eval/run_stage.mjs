// Run one stage over the held-out test set and save everything needed to judge
// and reproduce it: per scene the exact system + user prompt, retrieved chunk
// ids and the feedback; per sample the end-of-story content prompt + feedback.
//
//   node eval/run_stage.mjs <stage> [--samples id,id] [--force]
//
// Output: eval/runs/<stage>/<sample>.json (skipped if present unless --force)
// and eval/runs/<stage>/stage.json (the resolved stage + rendered system prompt).

import fs from "node:fs";
import path from "node:path";
import {
    assembleStagePrompt,
    assembleStageContentPrompt,
    buildSystemPrompt,
} from "../lib/rag/promptStages.ts";
import {
    EVAL_DIR, FEEDBACK_MODEL, REASONING_EFFORT, gitCommit, loadSnapshot, makeRetriever,
    openai, readJson, resolveStage, runDir, sampleKey, sha, withRetry, writeJson,
} from "./lib.mjs";

const args = process.argv.slice(2);
const stageId = args[0];
if (!stageId || stageId.startsWith("--")) {
    console.error("usage: node eval/run_stage.mjs <stage> [--samples id,id] [--force]");
    process.exit(1);
}
const force = args.includes("--force");
const sIdx = args.indexOf("--samples");
const only = sIdx > -1 ? new Set(args[sIdx + 1].split(",")) : null;

const stage = resolveStage(stageId);
const testSet = readJson(path.join(EVAL_DIR, "test_set.json"));
const snap = await loadSnapshot(stage.snapshot);
const retriever = makeRetriever(snap);
const commit = gitCommit();
const systemPrompt = buildSystemPrompt(stage.flags, stage.overrides);

writeJson(path.join(runDir(stageId), "stage.json"), {
    ...stage,
    model: FEEDBACK_MODEL,
    reasoning_effort: REASONING_EFFORT,
    snapshot_manifest: snap.manifest,
    system_prompt_sha: sha(systemPrompt),
    system_prompt: systemPrompt,
});

async function complete(prompt) {
    const t0 = Date.now();
    const res = await withRetry(
        () => openai().chat.completions.create({
            model: FEEDBACK_MODEL,
            reasoning_effort: REASONING_EFFORT,
            messages: [
                { role: "system", content: prompt.system },
                { role: "user", content: prompt.user },
            ],
        }),
        "feedback call"
    );
    return { text: res.choices[0]?.message?.content ?? "", usage: res.usage, ms: Date.now() - t0 };
}

async function runSample(sample) {
    const out = path.join(runDir(stageId), `${sampleKey(sample.sample_id)}.json`);
    if (fs.existsSync(out) && !force) {
        console.log(`${sample.sample_id}: already run (use --force to redo)`);
        return;
    }
    const opts = { storyId: sample.story_id };
    const scenes = [];
    for (let i = 0; i < sample.scenes.length; i++) {
        const prompt = await assembleStagePrompt(
            sample.scenes[i], { ...opts, previousScenes: sample.scenes.slice(0, i) },
            stage.flags, retriever, stage.overrides
        );
        const res = await complete(prompt);
        scenes.push({ scene: i + 1, text: sample.scenes[i], prompt: { system_sha: sha(prompt.system), user: prompt.user },
            retrieved: prompt.retrievedChunkIds, feedback: res.text, usage: res.usage, ms: res.ms });
        console.log(`${sample.sample_id}: scene ${i + 1}/${sample.scenes.length} done (${(res.ms / 1000).toFixed(0)}s)`);
    }
    const cprompt = await assembleStageContentPrompt(sample.scenes, opts, stage.flags, retriever, stage.overrides);
    const cres = await complete(cprompt);
    writeJson(out, {
        stage: stageId,
        sample_id: sample.sample_id,
        story_id: sample.story_id,
        created: new Date().toISOString(),
        git_commit: commit,
        snapshot: stage.snapshot,
        model: FEEDBACK_MODEL,
        reasoning_effort: REASONING_EFFORT,
        scenes,
        content: { prompt: { system: cprompt.system, user: cprompt.user }, retrieved: cprompt.retrievedChunkIds,
            feedback: cres.text, usage: cres.usage, ms: cres.ms },
    });
    console.log(`${sample.sample_id}: done -> ${path.relative(process.cwd(), out)}`);
}

const samples = testSet.samples.filter((s) => !only || only.has(s.sample_id));
console.log(`Stage ${stageId} (${stage.label}) on ${samples.length} samples, snapshot ${stage.snapshot}, model ${FEEDBACK_MODEL}`);
const results = await Promise.allSettled(samples.map(runSample));
const failed = results.filter((r) => r.status === "rejected");
for (const f of failed) console.error("FAILED:", f.reason?.message ?? f.reason);
console.log(failed.length ? `${failed.length} sample(s) failed -- re-run to retry them` : `Stage ${stageId} complete.`);
process.exitCode = failed.length ? 1 : 0;
