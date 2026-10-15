// Embed a snapshot's chunks into the local cache (eval/cache/), so stage runs
// need no further corpus embedding. Only texts not cached yet cost anything.
//   node eval/embed_snapshot.mjs <name>
import { loadSnapshot } from "./lib.mjs";

const name = process.argv[2];
if (!name) {
    console.error("usage: node eval/embed_snapshot.mjs <name>");
    process.exit(1);
}
const snap = await loadSnapshot(name);
console.log(`Snapshot ${name}: ${snap.docs.length} chunks embedded and cached.`);
