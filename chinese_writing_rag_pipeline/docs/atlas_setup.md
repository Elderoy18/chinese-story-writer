# Atlas Vector Search setup for `rag_chunks`

One-time setup. After running the embed script — `node scripts/embed-to-mongo.mjs`
(or the Python equivalent `scripts/embed_to_mongo.py`), which populates the
`rag_chunks` collection in the `chinese-writer-data` database — create a Vector
Search index so `lib/rag/retrieve.ts` can run `$vectorSearch`.

## Index definition

- **Database / collection:** `chinese-writer-data` / `rag_chunks`
- **Index name:** `rag_vec` (must match `VECTOR_INDEX` in `lib/rag/retrieve.ts`)
- **Type:** Vector Search (not the classic Search index)

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1536,
      "similarity": "cosine"
    },
    { "type": "filter", "path": "chunk_type" },
    { "type": "filter", "path": "story_id" },
    { "type": "filter", "path": "grammar_tags" },
    { "type": "filter", "path": "eval_tags" }
  ]
}
```

`numDimensions: 1536` matches `text-embedding-3-small`. If you switch embedding
models, update this number, `EMBED_MODEL` in `embed_to_mongo.py`, and
`EMBED_MODEL` in `lib/rag/embed.ts`, then re-embed.

## Option A - Atlas UI

Atlas → your cluster → **Atlas Search** → **Create Search Index** →
**JSON Editor** → **Vector Search** → pick `chinese-writer-data.rag_chunks`,
name it `rag_vec`, paste the JSON above, create. Build takes ~1 minute.

## Option B - from a script (M10+ clusters, or Atlas CLI / local dev)

`createSearchIndex` is only supported on some tiers. If yours supports it:

```js
db.rag_chunks.createSearchIndex("rag_vec", "vectorSearch", {
  fields: [
    { type: "vector", path: "embedding", numDimensions: 1536, similarity: "cosine" },
    { type: "filter", path: "chunk_type" },
    { type: "filter", path: "story_id" },
    { type: "filter", path: "grammar_tags" },
    { type: "filter", path: "eval_tags" },
  ],
});
```

## Verify

```js
db.rag_chunks.aggregate([
  { $vectorSearch: {
      index: "rag_vec",
      path: "embedding",
      queryVector: Array(1536).fill(0.01),
      numCandidates: 50,
      limit: 3,
      filter: { chunk_type: { $in: ["rule_card"] } }
  }},
  { $project: { chunk_id: 1, chunk_type: 1, _score: { $meta: "vectorSearchScore" } } }
])
```

Should return 3 `rule_card` rows. If it errors with "index not found", the
index is still building or the name doesn't match.
