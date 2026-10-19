// Back up (or restore) the live rag_chunks collection, embeddings included.
//
//   node chinese_writing_rag_pipeline/scripts/backup-rag-chunks.mjs
//       -> chinese_writing_rag_pipeline/backups/rag_chunks_<date>.jsonl  (one document per line)
//   node chinese_writing_rag_pipeline/scripts/backup-rag-chunks.mjs --restore <file>
//       replaces the whole collection with the backup (asks for no confirmation: run it
//       only to undo a deploy). The vector index is untouched either way.
//
// Backups are not committed (backups/ is git-ignored). Reads MONGODB_URI from .env.local.
import fs from "node:fs";
import path from "node:path";
import dns from "node:dns";
import { fileURLToPath } from "node:url";
import { MongoClient } from "mongodb";

dns.setServers(["1.1.1.1", "8.8.8.8"]); // as lib/auth.ts
const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(HERE, "..", "..");
const BACKUPS = path.resolve(HERE, "..", "backups");

for (const raw of fs.readFileSync(path.join(REPO_ROOT, ".env.local"), "utf8").split(/\r?\n/)) {
    const l = raw.trim();
    if (!l || l.startsWith("#") || !l.includes("=")) continue;
    const i = l.indexOf("=");
    if (!(l.slice(0, i).trim() in process.env)) process.env[l.slice(0, i).trim()] = l.slice(i + 1).trim();
}

const client = new MongoClient(process.env.MONGODB_URI);
await client.connect();
const coll = client.db("chinese-writer-data").collection("rag_chunks");
try {
    const r = process.argv.indexOf("--restore");
    if (r > -1) {
        const file = process.argv[r + 1];
        const docs = fs.readFileSync(file, "utf8").split("\n").filter(Boolean).map((l) => JSON.parse(l));
        await coll.deleteMany({});
        for (let i = 0; i < docs.length; i += 500) await coll.insertMany(docs.slice(i, i + 500), { ordered: false });
        console.log(`restored ${docs.length} documents from ${file}; collection now ${await coll.countDocuments({})}`);
    } else {
        fs.mkdirSync(BACKUPS, { recursive: true });
        const file = path.join(BACKUPS, `rag_chunks_${new Date().toISOString().slice(0, 19).replace(/[:T]/g, "-")}.jsonl`);
        const out = fs.createWriteStream(file);
        let n = 0;
        for await (const doc of coll.find({})) {
            out.write(JSON.stringify(doc) + "\n");
            n++;
        }
        await new Promise((res) => out.end(res));
        console.log(`backed up ${n} documents -> ${path.relative(REPO_ROOT, file)}`);
    }
} finally {
    await client.close();
}
