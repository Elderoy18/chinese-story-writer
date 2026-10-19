// Write the app's S7-6 configuration from the evaluated stage definition, so production
// runs exactly what the evaluation measured:
//
//   node eval/s7/export_production_config.mjs [stage]      (default S7-6)
//     -> lib/rag/s7_6Config.ts  (flags, prompt overrides, reasoning effort)
//
// Re-run whenever the stage (or a prompt override file it uses) changes.
import fs from "node:fs";
import path from "node:path";
import { ROOT, resolveStage } from "../lib.mjs";

const stageId = process.argv[2] ?? "S7-6";
const s = resolveStage(stageId);
const out =
    `// GENERATED from eval/stages.json (stage ${stageId}, resolved with its prompt overrides) by\n` +
    "// eval/s7/export_production_config.mjs -- do not edit by hand; regenerate instead, so the\n" +
    "// app runs exactly the configuration the evaluation measured.\n" +
    'import type { StageFlags, PromptOverrides } from "@/lib/rag/promptStages";\n\n' +
    `export const S7_6_FLAGS: StageFlags = ${JSON.stringify(s.flags, null, 4)};\n\n` +
    `export const S7_6_OVERRIDES: PromptOverrides = ${JSON.stringify(s.overrides, null, 4)};\n\n` +
    `export const S7_6_REASONING_EFFORT = ${JSON.stringify(s.reasoningEffort)} as const;\n`;
fs.writeFileSync(path.join(ROOT, "lib", "rag", "s7_6Config.ts"), out);
console.log(`wrote lib/rag/s7_6Config.ts from ${stageId}`);
