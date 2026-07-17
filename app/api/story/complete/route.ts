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

        // mark the last scene complete too
        const sceneIndex = story.currentSceneIndex;
        story.scenes[sceneIndex].status = "complete";
        story.status = "complete";

        await story.save();

        return NextResponse.json({ story });

    } catch (error) {
        return NextResponse.json({ error: "Failed to complete story" }, { status: 500 });
    }
}