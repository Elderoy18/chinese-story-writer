import mongoose, { Schema, Document } from "mongoose";

/**
 * Read model for the `rag_chunks` collection, populated offline by
 * chinese_writing_rag_pipeline/scripts/embed_to_mongo.py. The app never writes
 * to this collection; it only runs $vectorSearch aggregations against it
 * (see lib/rag/retrieve.ts).
 *
 * Chunk types (see chinese_writing_rag_pipeline/docs/design.md):
 *   model_story | sample | correction_item | ai_feedback_item |
 *   content_flag | story_prompt | rule_card | ai_error_card
 */
export interface IRagChunk extends Document<string> {
    _id: string;
    chunk_id: string;
    chunk_type: string;
    text: string;
    // metadata fields vary by chunk_type; the ones the app reads:
    story_id?: string;
    parent_id?: string;
    grammar_tag?: string;
    eval_tag?: string;
    grammar_tags?: string[];
    eval_tags?: string[];
    original_span?: string | null;
    corrected_span?: string | null;
    explanation?: string | null;
    title?: string;
    description?: string;
}

const RagChunkSchema = new Schema<IRagChunk>(
    {
        _id: { type: String },
        chunk_id: { type: String, required: true },
        chunk_type: { type: String, required: true, index: true },
        text: { type: String, required: true },
        story_id: { type: String },
        parent_id: { type: String },
        grammar_tag: { type: String },
        eval_tag: { type: String },
        grammar_tags: { type: [String] },
        eval_tags: { type: [String] },
        original_span: { type: String },
        corrected_span: { type: String },
        explanation: { type: String },
        title: { type: String },
        description: { type: String },
        // `embedding` is stored but never selected into the app — large and unused at read time.
    },
    { collection: "rag_chunks", strict: false }
);

const RagChunk =
    (mongoose.models.RagChunk as mongoose.Model<IRagChunk>) ||
    mongoose.model<IRagChunk>("RagChunk", RagChunkSchema);

export default RagChunk;
