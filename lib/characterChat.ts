import mongoose, { Schema, Document } from "mongoose";

export interface IChatMessage {
    role: "user" | "assistant";
    content: string;
    createdAt: Date;
}

export interface ICharacterChat extends Document {
    userId: string;
    characterId: string;
    messages: IChatMessage[];
}

const ChatMessageSchema = new Schema<IChatMessage>(
    {
        role: { type: String, enum: ["user", "assistant"], required: true },
        content: { type: String, required: true },
        createdAt: { type: Date, default: Date.now },
    },
    { _id: false }
);

const CharacterChatSchema = new Schema<ICharacterChat>(
    {
        userId: { type: String, required: true },
        characterId: { type: String, required: true },
        messages: { type: [ChatMessageSchema], default: [] },
    },
    { timestamps: true }
);

// One ongoing transcript per (student, character) pair -- same "single active
// doc" pattern as Story, so a teacher reviewing later sees one coherent thread.
CharacterChatSchema.index({ userId: 1, characterId: 1 }, { unique: true });

const CharacterChat =
    (mongoose.models.CharacterChat as mongoose.Model<ICharacterChat>) ||
    mongoose.model<ICharacterChat>("CharacterChat", CharacterChatSchema);

export default CharacterChat;