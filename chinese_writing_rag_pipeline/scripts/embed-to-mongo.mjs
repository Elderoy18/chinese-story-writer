// Node port of embed_to_mongo.py -- no Python / conda required.
//
// Reads chunks/chunks.jsonl, embeds each chunk's text with OpenAI
// text-embedding-3-small (1536-dim), and upserts one doc per chunk (keyed on
// chunk_id) into `chinese-writer-data.rag_chunks` -- the collection the Next
// app's lib/rag/retrieve.ts runs $vectorSearch against.
//
// Run from anywhere:
//   node chinese_writing_rag_pipeline/scripts/embed-to-mongo.mjs
//   node chinese_writing_rag_pipeline/scripts/embed-to-mongo.mjs --dry-run
//
// Uses the `openai` + `mongodb` packages already in the app's node_modules and
// reads MONGODB_URI / OPENAI_API_KEY from the repo-root .env.local.
//
// After a successful run, create the Atlas Vector Search index once -- see
// chinese_writing_rag_pipeline/docs/atlas_setup.md

import fs from "node:fs";
import path from "node:path";
import dns from "node:dns";
import { fileURLToPath } from "node:url";
import OpenAI from "openai";
import { MongoClient } from "mongodb";

// Match lib/auth.ts: this machine's default resolver is unreliable for some
// lookups; force public DNS so the Atlas shard hostnames resolve.
dns.setServers(["1.1.1.1", "8.8.8.8"]);

const EMBED_MODEL = "text-embedding-3-small"; // keep in sync with lib/rag/embed.ts
const EMBED_DIM = 1536;
const DB_NAME = "chinese-writer-data";
const COLLECTION = "rag_chunks";
const BATCH_SIZE = 128;

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PIPELINE_ROOT = path.resolve(HERE, "..");
const REPO_ROOT = path.resolve(HERE, "..", "..");
const CHUNKS_PATH = path.join(PIPELINE_ROOT, "chunks", "chunks.jsonl");

const dryRun = process.argv.includes("--dry-run");

/** Minimal .env.local loader (no dotenv dependency). */
function loadEnvLocal() {
    const envPath = path.join(REPO_ROOT, ".env.local");
    if (!fs.existsSync(envPath)) return;
    for (const raw of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
        const line = raw.trim();
        if (!line || line.startsWith("#") || !line.includes("=")) continue;
        const idx = line.indexOf("=");
        const key = line.slice(0, idx).trim();
        const val = line.slice(idx + 1).trim();
        if (!(key in process.env)) process.env[key] = val;
    }
}

/** Promote metadata to top-level fields; keep arrays as arrays. */
function toDoc(chunk) {
    return {
        _id: chunk.chunk_id,
        chunk_id: chunk.chunk_id,
        chunk_type: chunk.chunk_type,
        text: chunk.text,
        ...chunk.metadata,
    };
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function embedBatch(client, texts) {
    for (let attempt = 0; attempt < 5; attempt++) {
        try {
            const res = await client.embeddings.create({
                model: EMBED_MODEL,
                input: texts,
            });
            return res.data.map((d) => d.embedding);
        } catch (err) {
            const wait = 2 ** attempt * 1000;
            console.log(`  embed batch failed (${err.message}); retrying in ${wait / 1000}s`);
            await sleep(wait);
        }
    }
    throw new Error("embedding failed after retries");
}

async function main() {
    loadEnvLocal();

    if (!process.env.OPENAI_API_KEY) {
        console.error("OPENAI_API_KEY not set (checked env + .env.local)");
        process.exit(1);
    }
    if (!process.env.MONGODB_URI && !dryRun) {
        console.error("MONGODB_URI not set (checked env + .env.local)");
        process.exit(1);
    }

    const chunks = fs
        .readFileSync(CHUNKS_PATH, "utf8")
        .split(/\r?\n/)
        .filter((l) => l.trim())
        .map((l) => JSON.parse(l));
    console.log(`Loaded ${chunks.length} chunks from ${CHUNKS_PATH}`);

    const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

    const embeddings = [];
    for (let i = 0; i < chunks.length; i += BATCH_SIZE) {
        const batch = chunks.slice(i, i + BATCH_SIZE);
        const vecs = await embedBatch(openai, batch.map((c) => c.text));
        embeddings.push(...vecs);
        console.log(`  embedded ${Math.min(i + BATCH_SIZE, chunks.length)}/${chunks.length}`);
    }

    if (embeddings.length !== chunks.length) {
        throw new Error(`got ${embeddings.length} vectors for ${chunks.length} chunks`);
    }
    if (embeddings[0].length !== EMBED_DIM) {
        throw new Error(`expected ${EMBED_DIM}-dim vectors, got ${embeddings[0].length}`);
    }

    if (dryRun) {
        console.log("--dry-run: skipping Mongo write");
        return;
    }

    const mongo = new MongoClient(process.env.MONGODB_URI);
    try {
        await mongo.connect();
        const coll = mongo.db(DB_NAME).collection(COLLECTION);
        const ops = chunks.map((chunk, idx) => {
            const doc = toDoc(chunk);
            doc.embedding = embeddings[idx];
            doc.embed_model = EMBED_MODEL;
            return {
                replaceOne: { filter: { _id: doc._id }, replacement: doc, upsert: true },
            };
        });
        const res = await coll.bulkWrite(ops, { ordered: false });
        const total = await coll.countDocuments({});
        console.log(
            `Upserted into ${DB_NAME}.${COLLECTION}: ${res.upsertedCount} inserted, ` +
                `${res.modifiedCount} updated, ${total} total docs`
        );
        console.log("\nNext: create the Atlas Vector Search index -> chinese_writing_rag_pipeline/docs/atlas_setup.md");
    } finally {
        await mongo.close();
    }
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
