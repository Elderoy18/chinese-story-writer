import mongoose, { Schema, Document } from "mongoose";

// TypeScript types
export interface IScaffolding {
    characters: string;
    objects: string;
    actions: string;
    descriptions: string;
}

export interface IScene {
    sceneNumber: number;
    scaffolding: IScaffolding;
    sentence: string;
    feedback: string;
    videoUrl: string;
    regenerateUsed: boolean;
    status: "draft" | "complete";
}

export interface IStory extends Document {
    userId: string;
    status: "in_progress" | "complete";
    currentSceneIndex: number;
    scenes: IScene[];
    createdAt: Date;
    updatedAt: Date;
}

// Mongoose schemas
const ScaffoldingSchema = new Schema<IScaffolding>({
    characters: { type: String, default: "" },
    objects: { type: String, default: "" },
    actions: { type: String, default: "" },
    descriptions: { type: String, default: "" },
});

const SceneSchema = new Schema<IScene>({
    sceneNumber: { type: Number, required: true },
    scaffolding: { type: ScaffoldingSchema, default: () => ({}) },
    sentence: { type: String, default: "" },
    feedback: { type: String, default: "" },
    videoUrl: { type: String, default: "" },
    regenerateUsed: { type: Boolean, default: false },
    status: { type: String, enum: ["draft", "complete"], default: "draft" },
});

const StorySchema = new Schema<IStory>(
    {
        userId: { type: String, required: true },
        status: { 
            type: String, 
            enum: ["in_progress", "complete"], 
            default: "in_progress" 
        },
        currentSceneIndex: { type: Number, default: 0 },
        scenes: { type: [SceneSchema], default: [] },
    },
    { timestamps: true }
);

const Story = mongoose.models.Story || mongoose.model<IStory>("Story", StorySchema);

export default Story;