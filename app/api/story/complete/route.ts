import { getSession } from "@/lib/auth";
import connectDB from "@/lib/db";
import Story from "@/lib/story";
import { NextResponse } from "next/server";

export async function PATCH() {
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
        story.scenes[sceneIndex].originalSentence = story.scenes[sceneIndex].sentence;
        story.scenes[sceneIndex].sceneCompletedAt = new Date();
        story.status = "complete";
        story.storyCompletedAt = new Date();

        // calculate total character count (Chinese doesn't use spaces)
        const totalChars = story.scenes.reduce((sum: number, scene: any) => {
            return sum + (scene.sentence?.length || 0);
        }, 0);
        story.totalWordCount = totalChars;

        await story.save();

        return NextResponse.json({ story });

    } catch (error) {
        return NextResponse.json({ error: "Failed to complete story" }, { status: 500 });
    }
}