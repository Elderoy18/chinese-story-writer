import mongoose, { Schema, Document } from "mongoose";

export interface ICorrection extends Document {
    type: "correction" | "negative";
    studentPhrase: string;
    correctedVersion: string;
    rule: string;
    explanation: string;
    errorType: "wrongCharacter" | "grammar" | "vocabulary" | "structure";
    doNotFlag: boolean;
    embedding: number[];
    source: string;
    createdAt: Date;
}

const CorrectionSchema = new Schema<ICorrection>(
    {
        type: { 
            type: String, 
            enum: ["correction", "negative"], 
            required: true 
        },
        studentPhrase: { type: String, required: true },
        correctedVersion: { type: String, default: "" },
        rule: { type: String, required: true },
        explanation: { type: String, required: true },
        errorType: { 
            type: String, 
            enum: ["wrongCharacter", "grammar", "vocabulary", "structure"],
            required: true
        },
        doNotFlag: { type: Boolean, default: false },
        embedding: { type: [Number], default: [] },
        source: { type: String, default: "teacher" },
    },
    { timestamps: true }
);

const Correction = mongoose.models.Correction || 
    mongoose.model<ICorrection>("Correction", CorrectionSchema);

export default Correction;