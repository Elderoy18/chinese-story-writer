// Compare two stage runs side by side for teacher review, or summarize several.
//
//   node eval/compare.mjs <before> <after>        -> eval/reports/<before>_vs_<after>.md (bare bones)
//   node eval/compare.mjs <before> <after> --full -> ..._full.md (+ scores, corrections, checklists)
//   node eval/compare.mjs --summary S0 S1 S2 ...   -> eval/reports/summary.md
//
// Automatic score ("teacher corrections found"): for each of the teacher's corrections in a
// held-out sample, did the feedback's error sections (Grammar Corrections and
// the coherence items) point at the same place? Approximate -- it matches the
// teacher's original span against the text the feedback quotes, so it shows
// recall of locations, not whether the fix or explanation is right. That, and
// anything flagged that the teacher did not flag, is for the teacher to judge.

import fs from "node:fs";
import path from "node:path";
import { EVAL_DIR, readJson, runDir, sampleKey } from "./lib.mjs";

// Teacher-correction rule groups, so each iteration's own target can be read off.
const GROUPS = {
    "coherence (reference / aspect / connectors)": [
        "character_introduction_first_mention", "ambiguous_reference", "reference_form", "redundancy_delete",
        "aspect_le_completed", "aspect_zhe_durative", "aspect_zai_progressive", "coherence_connectives",
    ],
    "word choice (vocab-list type)": ["word_choice", "word_class_misuse", "verb_object_collocation"],
    "wrong story content": ["wrong_information_content"],
};
const OTHER = "other grammar";

const norm = (s) => (s ?? "").replace(/[\s\p{P}\p{S}]/gu, "");

function longestCommon(a, b) {
    let best = 0;
    let prev = new Array(b.length + 1).fill(0);
    for (let i = 1; i <= a.length; i++) {
        const cur = new Array(b.length + 1).fill(0);
        for (let j = 1; j <= b.length; j++) {
            if (a[i - 1] === b[j - 1]) {
                cur[j] = prev[j - 1] + 1;
                if (cur[j] > best) best = cur[j];
            }
        }
        prev = cur;
    }
    return best;
}

/** Heading kind for a feedback line: works for "## Grammar Corrections" and S0's "1. **Grammar Corrections**". */
function headingKind(line) {
    const t = line.trim();
    if (!(/^#{1,6}\s/.test(t) || /^(\d+[.)]\s*)?\*\*[^*]+\*\*/.test(t))) return null;
    const l = t.toLowerCase();
    if (l.includes("grammar")) return "grammar";
    if (l.includes("vocab")) return "vocab";
    if (l.includes("coherence") || l.includes("expressive")) return "coherence";
    if (l.includes("encourag")) return "encouragement";
    if (l.includes("content")) return "content";
    return null;
}

/** The error-flagging text of one feedback: Grammar + coherence items (not expressiveness). */
function errorText(feedback) {
    const parts = { pre: [], grammar: [], vocab: [], coherence: [], encouragement: [], content: [] };
    let cur = "pre";
    for (const line of feedback.split("\n")) {
        const k = headingKind(line);
        if (k) {
            cur = k;
            continue;
        }
        parts[cur].push(line);
    }
    const coherence = parts.coherence.filter((l) => !/^\s*[-*]\s*Expressiveness/i.test(l));
    return [...parts.grammar, ...coherence].join("\n");
}

function countItems(text) {
    return text.split("\n").filter((l) => /^\s*([-*•]|\d+[.)])\s+\S/.test(l) || /Incorrect phrase/.test(l))
        .filter((l) => !/Nothing to flag/i.test(l)).length;
}

function groupsOf(rules) {
    const g = Object.entries(GROUPS).filter(([, rs]) => rules.some((r) => rs.includes(r))).map(([name]) => name);
    return g.length ? g : [OTHER];
}

function loadRun(stage) {
    const dir = runDir(stage);
    if (!fs.existsSync(path.join(dir, "stage.json"))) throw new Error(`no run for ${stage} -- node eval/run_stage.mjs ${stage}`);
    const testSet = readJson(path.join(EVAL_DIR, "test_set.json"));
    const samples = {};
    for (const s of testSet.samples) {
        const f = path.join(dir, `${sampleKey(s.sample_id)}.json`);
        if (fs.existsSync(f)) samples[s.sample_id] = readJson(f);
    }
    return { stage: readJson(path.join(dir, "stage.json")), samples, testSet };
}

/** Per sample: which teacher corrections each run located, and how many items it flagged. */
function score(sample, run) {
    if (!run) return null;
    const err = norm(run.scenes.map((s) => errorText(s.feedback)).join("\n"));
    const located = sample.gold.corrections.map((g) => {
        const span = norm(g.original_span);
        if (!span) return null; // unscorable: no original span in the teacher's line
        const need = span.length <= 4 ? span.length : Math.max(4, Math.ceil(span.length * 0.5));
        return longestCommon(span, err) >= need;
    });
    const flagged = run.scenes.reduce((n, s) => n + countItems(errorText(s.feedback)), 0);
    const chars = run.scenes.reduce((n, s) => n + s.feedback.length, 0);
    return { located, flagged, chars };
}

function aggregate(testSet, run) {
    const total = {};
    let flagged = 0, chars = 0, scenes = 0;
    for (const s of testSet.samples) {
        const sc = score(s, run.samples[s.sample_id]);
        if (!sc) continue;
        flagged += sc.flagged;
        chars += sc.chars;
        scenes += s.scenes.length;
        s.gold.corrections.forEach((g, i) => {
            if (sc.located[i] === null) return;
            for (const key of ["all", ...groupsOf(g.rules)]) {
                total[key] ??= [0, 0];
                total[key][1]++;
                if (sc.located[i]) total[key][0]++;
            }
        });
    }
    return { total, flagged, avgChars: scenes ? Math.round(chars / scenes) : 0 };
}

const pct = ([a, b] = [0, 0]) => (b ? `${a}/${b} (${Math.round((100 * a) / b)}%)` : "–");
/** Feedback as a blockquote; its own "## Section" headings become bold lines so they
 *  don't compete with the report's headings. */
const quote = (text) => text.trim().split("\n")
    .map((l) => l.replace(/^\s*#{1,6}\s+(.+?)\s*$/, "**$1**"))
    .map((l) => `> ${l}`).join("\n");
const groupKeys = ["all", ...Object.keys(GROUPS), OTHER];

function summaryTable(runs, testSet) {
    const aggs = runs.map((r) => aggregate(testSet, r));
    const rows = [
        `| | ${runs.map((r) => `**${r.stage.id}** ${r.stage.label}`).join(" | ")} |`,
        `|---|${runs.map(() => "---").join("|")}|`,
        ...groupKeys.map((k) => `| Teacher corrections found: ${k} | ${aggs.map((a) => pct(a.total[k])).join(" | ")} |`),
        `| Error items flagged (all scenes) | ${aggs.map((a) => a.flagged).join(" | ")} |`,
        `| Avg feedback length per scene (chars) | ${aggs.map((a) => a.avgChars).join(" | ")} |`,
    ];
    return rows.join("\n");
}

/** Stage label without the leading "+ " used in stages.json ("+ Coherence rules" -> "Coherence rules"). */
const bareLabel = (st) => st.label.replace(/^\+\s*/, "");

/**
 * Side-by-side report for the teacher. Default: bare bones -- the two stages,
 * then per story each scene with both feedbacks and the end-of-story feedback.
 * With full = true it also has the model/snapshot details, the summary table,
 * the teacher's corrections with found/not-found marks, and review checklists.
 */
function pairReport(a, b, full = false) {
    const { testSet } = a;
    const L = [];
    L.push(`# ${a.stage.id}-${b.stage.id}: ${bareLabel(b.stage)}`, "");
    L.push(`- **Before (${a.stage.id})**: ${bareLabel(a.stage)}. ${a.stage.note}`);
    L.push(`- **After (${b.stage.id})**: ${bareLabel(b.stage)}. ${b.stage.note}`);
    if (full) {
        L.push(`- Model ${b.stage.model} (reasoning ${b.stage.reasoning_effort}); snapshots ${a.stage.snapshot} → ${b.stage.snapshot}; ` +
            `test set: ${testSet.samples.length} held-out samples, 1 run each.`);
        L.push(`- Generated ${new Date().toISOString().slice(0, 16).replace("T", " ")} by eval/compare.mjs. Full prompts: eval/runs/<stage>/.`, "");
        L.push("## Summary", "", summaryTable([a, b], testSet), "");
        L.push("*Teacher corrections found* = the teacher's correction was pointed at in the feedback's error sections " +
            "(approximate span match). It does not check that the fix or explanation is right, and does not " +
            "count extra items the teacher did not flag -- see the review below.", "");
    } else {
        L.push("", "");
    }

    for (const s of testSet.samples) {
        const ra = a.samples[s.sample_id], rb = b.samples[s.sample_id];
        if (full) {
            const sa = score(s, ra), sb = score(s, rb);
            L.push("---", "", `## ${s.sample_id} (${s.story_id})`, "");
            L.push("**Teacher's corrections**", "");
            L.push(`| # | Teacher correction | Rules | ${a.stage.id} | ${b.stage.id} |`, "|---|---|---|---|---|");
            s.gold.corrections.forEach((g, i) => {
                const mark = (sc) => (!sc ? "–" : sc.located[i] === null ? "n/a" : sc.located[i] ? "✓" : "✗");
                L.push(`| ${i + 1} | ${g.text.replace(/\|/g, "/")} | ${g.rules.join(", ")} | ${mark(sa)} | ${mark(sb)} |`);
            });
            L.push("", `**Teacher's content flags:** ${s.gold.content_flags.join(" / ") || "none"}`, "");
        } else {
            L.push(`## ${s.sample_id} (${s.story_id})`, "");
        }

        s.scenes.forEach((text, i) => {
            L.push(`### Scene ${i + 1}`, "", quote(text), "");
            L.push(`#### ${a.stage.id} (before)`, "", ra ? quote(ra.scenes[i].feedback) : "_not run_", "");
            L.push(`#### ${b.stage.id} (after)`, "", rb ? quote(rb.scenes[i].feedback) : "_not run_", "");
        });
        L.push("### End-of-story content feedback", "");
        L.push(`#### ${a.stage.id} (before)`, "", ra ? quote(ra.content.feedback) : "_not run_", "");
        L.push(`#### ${b.stage.id} (after)`, "", rb ? quote(rb.content.feedback) : "_not run_", "");

        if (full) {
            L.push("### Teacher review", "");
            s.scenes.forEach((_, i) => L.push(`- Scene ${i + 1} -- better: [ ] before  [ ] after  [ ] same. Notes:`));
            L.push("- End-of-story -- better: [ ] before  [ ] after  [ ] same. Notes:", "");
        }
    }

    if (full) {
        L.push("---", "", `## Verdict on ${b.stage.id}`, "");
        L.push(`- [ ] Accept ${b.stage.id} as it is`);
        L.push(`- [ ] Refine ${b.stage.id} -- what should change (rules, wording, vocab entries, scenes):`, "");
    }
    return L.join("\n");
}

const args = process.argv.slice(2);
const outDir = path.join(EVAL_DIR, "reports");
fs.mkdirSync(outDir, { recursive: true });

if (args[0] === "--summary") {
    const runs = args.slice(1).map(loadRun);
    if (!runs.length) throw new Error("usage: node eval/compare.mjs --summary S0 S1 ...");
    const out = path.join(outDir, "summary.md");
    fs.writeFileSync(out, `# Stage summary\n\n${summaryTable(runs, runs[0].testSet)}\n`);
    console.log(fs.readFileSync(out, "utf8"));
    console.log(`Wrote ${path.relative(process.cwd(), out)}`);
} else {
    const full = args.includes("--full");
    const stages = args.filter((x) => x !== "--full");
    if (stages.length !== 2) throw new Error("usage: node eval/compare.mjs <before> <after> [--full]");
    const [a, b] = stages.map(loadRun);
    const out = path.join(outDir, `${stages[0]}_vs_${stages[1]}${full ? "_full" : ""}.md`);
    fs.writeFileSync(out, pairReport(a, b, full));
    console.log(summaryTable([a, b], a.testSet));
    console.log(`\nWrote ${path.relative(process.cwd(), out)}`);
}
