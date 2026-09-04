import { getSession } from "@/lib/auth";
import connectDB from "@/lib/db";
import Story from "@/lib/story";
import { generateSceneIllustration } from "@/lib/sceneIllustration";
import { NextResponse } from "next/server";

export async function POST(request: Request) {
    try {
        const session = await getSession();
        if (!session?.user) {
            return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
        }

        const { scaffolding, sentence } = await request.json();
        if (!sentence || !sentence.trim()) {
            return NextResponse.json({ error: "No sentence provided" }, { status: 400 });
        }

        await connectDB();
        const story = await Story.findOne({
            userId: session.user.id,
            status: "in_progress",
        });
        if (!story) {
            return NextResponse.json({ error: "No story in progress" }, { status: 404 });
        }

        const { imageUrl, imagePrompt } = await generateSceneIllustration(scaffolding, sentence);

        story.scenes[story.currentSceneIndex].imageUrl = imageUrl;
        story.scenes[story.currentSceneIndex].imagePrompt = imagePrompt;
        await story.save();

        return NextResponse.json({ imageUrl });
    } catch (error) {
        console.error("Scene image error:", error);
        return NextResponse.json({ error: "Failed to generate image" }, { status: 500 });
    }
}
