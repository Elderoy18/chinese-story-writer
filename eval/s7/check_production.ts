// Check the app's production prompt path against the live database (no model call):
//   npx tsx eval/s7/check_production.ts
// - the system prompt is byte-identical to the evaluated stage's (eval/runs/<stage>/stage.json);
// - for a few test scenes, the S7-6 mechanisms fire through live Atlas retrieval:
//   pinned cards, sentence-matched rule cards (via rule_example), rule-card triggers,
//   standard fixes, teacher rules with ids, citation instruction;
// - the end-of-story prompt asks for the Scene check.
import fs from "node:fs";
import crypto from "node:crypto";
import path from "node:path";
import dns from "node:dns";

dns.setServers(["1.1.1.1", "8.8.8.8"]);
const ROOT = path.resolve(__dirname, "..", "..");
for (const raw of fs.readFileSync(path.join(ROOT, ".env.local"), "utf8").split(/\r?\n/)) {
    const l = raw.trim();
    if (!l || l.startsWith("#") || !l.includes("=")) continue;
    const i = l.indexOf("=");
    if (!(l.slice(0, i).trim() in process.env)) process.env[l.slice(0, i).trim()] = l.slice(i + 1).trim();
}

async function main() {
    const { assembleFeedbackPrompt, assembleContentPrompt, FEEDBACK_CONFIG, SYSTEM_INSTRUCTIONS } = await import("../../lib/rag/assembleFeedbackPrompt");
    const stage = FEEDBACK_CONFIG.name === "s7-6" ? "S7-6" : "S4";
    const stored = JSON.parse(fs.readFileSync(path.join(ROOT, "eval", "runs", stage, "stage.json"), "utf8"));
    const sha = crypto.createHash("sha256").update(SYSTEM_INSTRUCTIONS).digest("hex").slice(0, 16);
    console.log(`config ${FEEDBACK_CONFIG.name}, effort ${FEEDBACK_CONFIG.reasoningEffort}`);
    console.log(`system prompt identical to evaluated ${stage}: ${sha === stored.system_prompt_sha} (${sha} vs ${stored.system_prompt_sha})`);

    const ts = JSON.parse(fs.readFileSync(path.join(ROOT, "eval", "test_set_h20.json"), "utf8"));
    for (const s of ts.samples.slice(0, 3)) {
        const p = await assembleFeedbackPrompt(s.scenes[1], { storyId: s.story_id, previousScenes: s.scenes.slice(0, 1) });
        const ids = p.retrievedChunkIds;
        console.log(`\n${s.sample_id} scene 2: ${ids.length} chunks`);
        console.log("  rule cards:", ids.filter((x) => x.startsWith("rule_card:")).map((x) => x.slice(10)).join(", "));
        console.log("  found via corrected sentences (rule_example):", ids.filter((x) => x.startsWith("rule_example:")).length);
        console.log("  teacher rules:", ids.filter((x) => x.startsWith("teacher_rule:")).length,
            "| trigger places shown:", (p.user.match(/MAY break this rule/g) ?? []).length,
            "| standard fixes shown:", (p.user.match(/standard fix for this rule/g) ?? []).length,
            "| cards titled by name:", !/### Rule: rule_card:/.test(p.user));
    }
    const s = ts.samples[0];
    const c = await assembleContentPrompt(s.scenes, { storyId: s.story_id });
    console.log(`\nend of story: scene list ${c.retrievedChunkIds.join(", ")} | asks for Scene check: ${/## Scene check/.test(c.system)}`);
    process.exit(0);
}
main();
