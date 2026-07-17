import { getSession } from "@/lib/auth";
import connectDB from "@/lib/db";
import Story from "@/lib/story";
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
export async function POST() {
    try {
        const session = await getSession();
        if (!session?.user) {
            return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
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
                    status: "draft",
                }
            ]
        });

        return NextResponse.json({ story }, { status: 201 });

    } catch (error) {
        return NextResponse.json({ error: "Failed to create story" }, { status: 500 });
    }
}

// PATCH - save scaffolding for current scene
export async function PATCH(request: Request) {
    try {
        const session = await getSession();
        if (!session?.user) {
            return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
        }

        const body = await request.json();
        const { scaffolding, sentence } = body;

        await connectDB();

        const story = await Story.findOne({
            userId: session.user.id,
            status: "in_progress"
        });

        if (!story) {
            return NextResponse.json({ error: "No story in progress" }, { status: 404 });
        }

        const sceneIndex = story.currentSceneIndex;

        story.scenes[sceneIndex].scaffolding = scaffolding;
        story.scenes[sceneIndex].sentence = sentence;

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

        // mark current scene as complete
        story.scenes[sceneIndex].status = "complete";

        // add a new blank scene
        story.scenes.push({
            sceneNumber: sceneIndex + 2,
            scaffolding: {
                characters: "",
                objects: "",
                actions: "",
                descriptions: "",
            },
            sentence: "",
            feedback: "",
            videoUrl: "",
            regenerateUsed: false,
            status: "draft",
        });

        // advance the index
        story.currentSceneIndex = sceneIndex + 1;

        await story.save();

        return NextResponse.json({ story });

    } catch (error) {
        return NextResponse.json({ error: "Failed to advance scene" }, { status: 500 });
    }
}