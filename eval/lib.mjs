// Shared helpers for the stage evaluation (see eval/README.md): env + OpenAI
// client, the embedding cache, frozen snapshots with an exact local vector
// search, and stage resolution from eval/stages.json.

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import OpenAI from "openai";

export const EVAL_DIR = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(EVAL_DIR, "..");

// Same models as the app (lib/rag/embed.ts, app/api/story/feedback/route.ts).
export const EMBED_MODEL = "text-embedding-3-small";
export const EMBED_DIM = 1536;
export const FEEDBACK_MODEL = "gpt-5.6-terra";
export const REASONING_EFFORT = "low";

const CACHE_DIR = path.join(EVAL_DIR, "cache");
const CACHE_VECTORS = path.join(CACHE_DIR, "embeddings.f32");
const CACHE_INDEX = path.join(CACHE_DIR, "embeddings.index.json");

/** Minimal .env.local loader (same as scripts/embed-to-mongo.mjs). */
function loadEnvLocal() {
    const envPath = path.join(ROOT, ".env.local");
    if (!fs.existsSync(envPath)) return;
    for (const raw of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
        const line = raw.trim();
        if (!line || line.startsWith("#") || !line.includes("=")) continue;
        const idx = line.indexOf("=");
        const key = line.slice(0, idx).trim();
        if (!(key in process.env)) process.env[key] = line.slice(idx + 1).trim();
    }
}

let client = null;
export function openai() {
    if (!client) {
        loadEnvLocal();
        if (!process.env.OPENAI_API_KEY) throw new Error("OPENAI_API_KEY not set (checked env + .env.local)");
        client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    }
    return client;
}

export function gitCommit() {
    try {
        const sha = execSync("git rev-parse --short HEAD", { cwd: ROOT }).toString().trim();
        const dirty = execSync("git status --porcelain", { cwd: ROOT }).toString().trim() ? "+uncommitted" : "";
        return sha + dirty;
    } catch {
        return "unknown";
    }
}

export const sha = (s) => crypto.createHash("sha256").update(s).digest("hex").slice(0, 16);
export const readJson = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
export function writeJson(p, data) {
    fs.mkdirSync(path.dirname(p), { recursive: true });
    fs.writeFileSync(p, JSON.stringify(data, null, 1) + "\n");
}

export async function withRetry(fn, label) {
    for (let attempt = 0; ; attempt++) {
        try {
            return await fn();
        } catch (err) {
            if (attempt >= 4) throw err;
            const wait = 2 ** attempt * 2000;
            console.log(`  ${label} failed (${err.message}); retrying in ${wait / 1000}s`);
            await new Promise((r) => setTimeout(r, wait));
        }
    }
}

// ---------------------------------------------------------------------------
// Embedding cache: one vector per (model, text), shared by every snapshot and
// by query embeddings, so re-runs cost nothing and use identical vectors.
// ---------------------------------------------------------------------------
let cache = null;
function loadCache() {
    if (cache) return cache;
    cache = new Map();
    if (fs.existsSync(CACHE_INDEX)) {
        const hashes = readJson(CACHE_INDEX).hashes;
        const buf = fs.readFileSync(CACHE_VECTORS);
        const all = new Float32Array(buf.buffer, buf.byteOffset, buf.byteLength / 4);
        hashes.forEach((h, i) => cache.set(h, all.slice(i * EMBED_DIM, (i + 1) * EMBED_DIM)));
    }
    return cache;
}

function saveCache() {
    fs.mkdirSync(CACHE_DIR, { recursive: true });
    const hashes = [...cache.keys()];
    const all = new Float32Array(hashes.length * EMBED_DIM);
    hashes.forEach((h, i) => all.set(cache.get(h), i * EMBED_DIM));
    fs.writeFileSync(CACHE_VECTORS, Buffer.from(all.buffer));
    writeJson(CACHE_INDEX, { model: EMBED_MODEL, dim: EMBED_DIM, hashes });
}

const keyOf = (text) => sha(`${EMBED_MODEL}\n${text}`);

/** Vectors for texts, embedding only those not cached yet. */
export async function embedTexts(texts) {
    const c = loadCache();
    const todo = [...new Set(texts.filter((t) => !c.has(keyOf(t))))];
    for (let i = 0; i < todo.length; i += 128) {
        const batch = todo.slice(i, i + 128);
        const res = await withRetry(
            () => openai().embeddings.create({ model: EMBED_MODEL, input: batch }),
            "embedding batch"
        );
        res.data.forEach((d, j) => c.set(keyOf(batch[j]), Float32Array.from(d.embedding)));
        console.log(`  embedded ${Math.min(i + 128, todo.length)}/${todo.length} new texts`);
    }
    if (todo.length) saveCache();
    return texts.map((t) => c.get(keyOf(t)));
}

// ---------------------------------------------------------------------------
// Snapshots + local retriever (exact cosine; OpenAI vectors are unit length,
// so the dot product is the cosine). Mirrors lib/rag/retrieve.ts.
// ---------------------------------------------------------------------------
export function snapshotDir(name) {
    return path.join(EVAL_DIR, "snapshots", name);
}

export async function loadSnapshot(name) {
    const dir = snapshotDir(name);
    if (!fs.existsSync(path.join(dir, "chunks.jsonl"))) {
        throw new Error(`no snapshot ${name} -- run: python eval/make_snapshot.py ${name}`);
    }
    const docs = fs.readFileSync(path.join(dir, "chunks.jsonl"), "utf8").split("\n").filter(Boolean)
        .map((l) => JSON.parse(l))
        .map((c) => ({ chunk_id: c.chunk_id, chunk_type: c.chunk_type, text: c.text, ...c.metadata }));
    const vectors = await embedTexts(docs.map((d) => d.text));
    return { name, manifest: readJson(path.join(dir, "manifest.json")), docs, vectors };
}

export function makeRetriever(snap) {
    const byId = new Map(snap.docs.map((d, i) => [d.chunk_id, i]));
    return {
        async search(text, { chunkTypes, k = 5, storyId, grammarTag }) {
            const [q] = await embedTexts([text.replace(/\s+/g, " ").trim()]);
            const scored = [];
            snap.docs.forEach((d, i) => {
                if (!chunkTypes.includes(d.chunk_type) || (storyId && d.story_id !== storyId)) return;
                if (grammarTag && !(d.grammar_tags ?? []).includes(grammarTag)) return;
                const v = snap.vectors[i];
                let s = 0;
                for (let j = 0; j < EMBED_DIM; j++) s += q[j] * v[j];
                scored.push({ ...d, score: s });
            });
            return scored.sort((a, b) => b.score - a.score).slice(0, k);
        },
        async byIds(ids) {
            return ids.filter((id) => byId.has(id)).map((id) => ({ ...snap.docs[byId.get(id)], score: 1 }));
        },
        async byType(type) {
            return snap.docs.filter((d) => d.chunk_type === type)
                .sort((a, b) => (a.chunk_id < b.chunk_id ? -1 : 1))
                .map((d) => ({ ...d, score: 1 }));
        },
    };
}

// ---------------------------------------------------------------------------
// Stages: eval/stages.json. A stage either sets `flags` or `extends` another
// stage and changes some of: flags, snapshot, fragments (prompt fragment name
// -> text, or a path ending in .txt/.md relative to eval/), extraRules.
// ---------------------------------------------------------------------------
const NO_FLAGS = { critique: false, sceneList: false, vocab: false, coherence: false, critiqueRetrieval: false, vocabExamples: false };

export function resolveStage(id, stages = readJson(path.join(EVAL_DIR, "stages.json")).stages) {
    const def = stages[id];
    if (!def) throw new Error(`unknown stage ${id} (known: ${Object.keys(stages).join(", ")})`);
    const base = def.extends
        ? resolveStage(def.extends, stages)
        : { flags: NO_FLAGS, snapshot: "base", testSet: "test_set.json", overrides: { fragments: {}, extraRules: [] }, chain: [] };
    const fragments = { ...base.overrides.fragments };
    for (const [name, value] of Object.entries(def.fragments ?? {})) {
        const file = path.join(EVAL_DIR, value);
        fragments[name] = /\.(txt|md)$/.test(value) && fs.existsSync(file)
            ? fs.readFileSync(file, "utf8").trim()
            : value;
    }
    return {
        id,
        label: def.label ?? id,
        chain: [...base.chain, id],
        flags: { ...base.flags, ...(def.flags ?? {}) },
        snapshot: def.snapshot ?? base.snapshot,
        // Which held-out stories the stage runs on (file in eval/); inherited like snapshot.
        testSet: def.testSet ?? base.testSet,
        // Reasoning effort for the feedback model; inherited; unset = REASONING_EFFORT.
        reasoningEffort: def.reasoningEffort ?? base.reasoningEffort,
        overrides: { fragments, extraRules: [...base.overrides.extraRules, ...(def.extraRules ?? [])] },
        note: def.note ?? "",
    };
}

export const sampleKey = (sampleId) => sampleId.replace(/[^A-Za-z0-9_-]+/g, "_");
export const runDir = (stageId) => path.join(EVAL_DIR, "runs", stageId);
