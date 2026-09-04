import OpenAI from "openai";

// MUST match EMBED_MODEL in chinese_writing_rag_pipeline/scripts/embed_to_mongo.py
// and numDimensions in chinese_writing_rag_pipeline/docs/atlas_setup.md.
// If you change this, re-embed the corpus and rebuild the Atlas index.
export const EMBED_MODEL = "text-embedding-3-small";
export const EMBED_DIM = 1536;

let client: OpenAI | null = null;

function getClient(): OpenAI {
    if (!client) {
        if (!process.env.OPENAI_API_KEY) {
            throw new Error("OPENAI_API_KEY is not set");
        }
        client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    }
    return client;
}

/** Embed one query string with the same model used to index the RAG corpus. */
export async function embedText(text: string): Promise<number[]> {
    const input = text.replace(/\s+/g, " ").trim();
    const res = await getClient().embeddings.create({
        model: EMBED_MODEL,
        input,
    });
    return res.data[0].embedding;
}
