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
    originalSentence: string;
    regeneratedSentence: string;
    finalSentence: string;
    sceneStartedAt: Date;
    sceneCompletedAt: Date;
    feedback: string;
    regenerateUsed: boolean;
    status: "draft" | "complete";
    wasEdited: boolean;
    videoUrl: string;
}


export interface IStory extends Document {
    userId: string;
    status: "in_progress" | "complete";
    currentSceneIndex: number;
    scenes: IScene[];
    endStoryEditUsed: boolean;        // lowercase boolean
    errorPatterns: {                  // array of objects, not string
        errorType: string;
        count: number;
        sceneNumber: number;
    }[];
    totalWordCount: number;           // lowercase number
    storyCompletedAt: Date;
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

    // three stages of progression
    sentence: { type: String, default: "" },
    originalSentence: { type: String, default: "" },
    regeneratedSentence: { type: String, default: "" },
    finalSentence: { type: String, default: "" },

    feedback: { type: String, default: "" },
    regenerateUsed: { type: Boolean, default: false },
    status: { type: String, enum: ["draft", "complete"], default: "draft" },

    // research timing
    sceneStartedAt: { type: Date },
    sceneCompletedAt: { type: Date },
    wasEdited: { type: Boolean, default: false },         // was finalSentence different?
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
        
        // end-of-story edit tracking
        endStoryEditUsed: { type: Boolean, default: false },
        
        // research: error patterns (populated by RAG system later)
        errorPatterns: [{
            errorType: String,    // "了 omission", "direction complement", etc.
            count: Number,
            sceneNumber: Number,
        }],
        
        // story metrics
        totalWordCount: { type: Number, default: 0 },   // calculated on complete
        storyCompletedAt: { type: Date },
    },
    { timestamps: true }
);

const Story = mongoose.models.Story || mongoose.model<IStory>("Story", StorySchema);

export default Story;