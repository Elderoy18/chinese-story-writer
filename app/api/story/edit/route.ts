import { getSession } from "@/lib/auth";
import connectDB from "@/lib/db";
import Story from "@/lib/story";
import { NextResponse } from "next/server";

// PATCH - save final edited sentences after end-of-story edit
export async function PATCH(request: Request) {
    try {
        const session = await getSession();
        if (!session?.user) {
            return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
        }

        const body = await request.json();
        const { editedSentences } = body;
        // editedSentences: string[] — one per completed scene in order

        await connectDB();

        const story = await Story.findOne({
            userId: session.user.id,
            status: "complete"
        });

        if (!story) {
            return NextResponse.json({ error: "No completed story found" }, { status: 404 });
        }

        const completedScenes = story.scenes.filter((s: any) => s.status === "complete");

        completedScenes.forEach((scene: any, index: number) => {
            const edited = editedSentences[index];
            if (edited && edited !== scene.sentence) {
                scene.finalSentence = edited;
                scene.sentence = edited;
                scene.wasEdited = true;
            } else {
                scene.finalSentence = scene.sentence;
                scene.wasEdited = false;
            }
        });

        story.endStoryEditUsed = true;

        await story.save();

        return NextResponse.json({ story });

    } catch (error) {
        return NextResponse.json({ error: "Failed to save edits" }, { status: 500 });
    }
}