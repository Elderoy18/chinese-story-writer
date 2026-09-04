import connectDB from "@/lib/db";
import RagChunk from "@/lib/rag/ragChunk";
import { embedText } from "@/lib/rag/embed";

// Must match the index name created in
// chinese_writing_rag_pipeline/docs/atlas_setup.md
const VECTOR_INDEX = "rag_vec";

export interface RetrievedChunk {
    chunk_id: string;
    chunk_type: string;
    text: string;
    score: number;
    story_id?: string;
    parent_id?: string;
    grammar_tag?: string;
    eval_tag?: string;
    original_span?: string | null;
    corrected_span?: string | null;
    explanation?: string | null;
    title?: string;
}

interface SearchOpts {
    chunkTypes: string[];
    storyId?: string;
    k?: number;
}

const PROJECTION = {
    _id: 0,
    chunk_id: 1,
    chunk_type: 1,
    text: 1,
    story_id: 1,
    parent_id: 1,
    grammar_tag: 1,
    eval_tag: 1,
    original_span: 1,
    corrected_span: 1,
    explanation: 1,
    title: 1,
    score: { $meta: "vectorSearchScore" },
} as const;

/**
 * Semantic search over the RAG corpus with a hard chunk_type filter (and an
 * optional story_id filter). Direct port of local_demo.py `search` /
 * retrieve.py `search`, backed by Atlas $vectorSearch instead of TF-IDF/Chroma.
 */
export async function searchChunks(
    queryText: string,
    { chunkTypes, storyId, k = 5 }: SearchOpts
): Promise<RetrievedChunk[]> {
    await connectDB();
    const queryVector = await embedText(queryText);

    const filter: Record<string, unknown> = {
        chunk_type: { $in: chunkTypes },
    };
    if (storyId) filter.story_id = storyId;

    const rows = await RagChunk.aggregate<RetrievedChunk>([
        {
            $vectorSearch: {
                index: VECTOR_INDEX,
                path: "embedding",
                queryVector,
                numCandidates: Math.max(100, k * 15),
                limit: k,
                filter,
            },
        },
        { $project: PROJECTION },
    ]);

    return rows;
}

/**
 * Fetch specific chunks by id (e.g. the always-injected ai_error_card:* and,
 * later, story_prompt:* / model_story:* cards). Returns them in the requested
 * order, silently skipping any that are missing from the corpus.
 */
export async function getChunksByIds(ids: string[]): Promise<RetrievedChunk[]> {
    if (ids.length === 0) return [];
    await connectDB();
    const docs = await RagChunk.find(
        { _id: { $in: ids } },
        {
            _id: 0,
            chunk_id: 1,
            chunk_type: 1,
            text: 1,
            story_id: 1,
            parent_id: 1,
            grammar_tag: 1,
            eval_tag: 1,
            title: 1,
        }
    ).lean<RetrievedChunk[]>();

    const byId = new Map(docs.map((d) => [d.chunk_id, d]));
    return ids
        .map((id) => byId.get(id))
        .filter((d): d is RetrievedChunk => Boolean(d))
        .map((d) => ({ ...d, score: 1 }));
}
