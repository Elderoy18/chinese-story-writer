import { getSession } from "@/lib/auth";
import connectDB from "@/lib/db";
import Story from "@/lib/story";
import { getRetelling } from "@/lib/retellings";
import { NextResponse } from "next/server";

// GET - fetch the user's current story
export async function GET() {
    try {
        const session = await getSession();
        if (!session?.user) {
            return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
        }

        await connectDB();

        const story = await Story.findOne({ 
            userId: session.user.id,
            status: "in_progress"
        });

        return NextResponse.json({ story });

    } catch (error) {
        return NextResponse.json({ error: "Failed to fetch story" }, { status: 500 });
    }
}

// POST - create a new story
export async function POST(request: Request) {
    try {
        const session = await getSession();
        if (!session?.user) {
            return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
        }

        // optional: { storyId } to start a retelling instead of a free-write
        let storyId = "";
        try {
            const body = await request.json();
            if (body?.storyId && getRetelling(body.storyId)) {
                storyId = body.storyId;
            }
        } catch {
            // no body — free-write
        }

        await connectDB();

        const existing = await Story.findOne({
            userId: session.user.id,
            status: "in_progress"
        });

        if (existing) {
            return NextResponse.json(
                { error: "You already have a story in progress" },
                { status: 400 }
            );
        }

        const story = await Story.create({
            userId: session.user.id,
            status: "in_progress",
            storyId,
            currentSceneIndex: 0,
            scenes: [
                {
                    sceneNumber: 1,
                    scaffolding: {
                        characters: "",
                        objects: "",
                        actions: "",
                        descriptions: "",
                    },
                    sentence: "",
                    originalSentence: "",
                    regeneratedSentence: "",
                    finalSentence: "",
                    status: "draft",
                    sceneStartedAt: new Date(),
                }
            ]
        });

        return NextResponse.json({ story }, { status: 201 });

    } catch (error) {
        return NextResponse.json({ error: "Failed to create story" }, { status: 500 });
    }
}

// PATCH - save scaffolding, sentence, originalSentence, or regeneratedSentence
export async function PATCH(request: Request) {
    try {
        const session = await getSession();
        if (!session?.user) {
            return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
        }

        const body = await request.json();
        const { scaffolding, sentence, regenerateUsed, saveOriginal, saveRegenerated } = body;

        await connectDB();

        const story = await Story.findOne({
            userId: session.user.id,
            status: "in_progress"
        });

        if (!story) {
            return NextResponse.json({ error: "No story in progress" }, { status: 404 });
        }

        const sceneIndex = story.currentSceneIndex;
        console.log("saveOriginal:", saveOriginal);
        console.log("regenerateUsed on scene:", story.scenes[sceneIndex].regenerateUsed);
        console.log("originalSentence already set:", !!story.scenes[sceneIndex].originalSentence);

        story.scenes[sceneIndex].scaffolding = scaffolding;
        story.scenes[sceneIndex].sentence = sentence;

        if (regenerateUsed !== undefined) {
            story.scenes[sceneIndex].regenerateUsed = regenerateUsed;
        }
        // freeze originalSentence when END SCENE is clicked
        // freeze originalSentence ONLY if it hasn't been set yet
        if (saveOriginal && !story.scenes[sceneIndex].originalSentence) {
            story.scenes[sceneIndex].originalSentence = sentence;
            story.scenes[sceneIndex].sceneCompletedAt = new Date();
        }

        // save regeneratedSentence when REGENERATE is clicked
        if (saveOriginal && story.scenes[sceneIndex].regenerateUsed) {
            story.scenes[sceneIndex].regeneratedSentence = sentence;
        }

        await story.save();

        return NextResponse.json({ story });

    } catch (error) {
        return NextResponse.json({ error: "Failed to save scene" }, { status: 500 });
    }
}

// PUT - complete current scene and start next one
export async function PUT() {
    try {
        const session = await getSession();
        if (!session?.user) {
            return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
        }

        await connectDB();

        const story = await Story.findOne({
            userId: session.user.id,
            status: "in_progress"
        });

        if (!story) {
            return NextResponse.json({ error: "No story in progress" }, { status: 404 });
        }

        const sceneIndex = story.currentSceneIndex;

        story.scenes[sceneIndex].status = "complete";

        story.scenes.push({
            sceneNumber: sceneIndex + 2,
            scaffolding: {
                characters: "",
                objects: "",
                actions: "",
                descriptions: "",
            },
            sentence: "",
            originalSentence: "",
            regeneratedSentence: "",
            finalSentence: "",
            feedback: "",
            videoUrl: "",
            regenerateUsed: false,
            status: "draft",
            sceneStartedAt: new Date(),
        });

        story.currentSceneIndex = sceneIndex + 1;

        await story.save();

        return NextResponse.json({ story });

    } catch (error) {
        return NextResponse.json({ error: "Failed to advance scene" }, { status: 500 });
    }
}