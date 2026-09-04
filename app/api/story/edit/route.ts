import { getSession } from "@/lib/auth";
import connectDB from "@/lib/db";
import Story from "@/lib/story";
import { generateSceneIllustration } from "@/lib/sceneIllustration";
import { NextResponse } from "next/server";

// PATCH - save final edited sentences after end-of-story edit, and (re)generate
// the illustration for any scene whose text actually changed, or that never
// got one (e.g. the illustration was still generating when the student moved
// on to the next scene).
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

        // (Re)generate illustrations for edited scenes, and backfill any scene
        // that never got one (e.g. it was still generating when the student
        // clicked NEXT SCENE / END STORY before it finished saving). Runs in
        // parallel, best-effort -- a failure here just leaves that scene's
        // previous image (or no image) in place.
        const needsImage = completedScenes.filter((s: any) => s.wasEdited || !s.imageUrl);
        await Promise.all(
            needsImage.map(async (scene: any) => {
                try {
                    const { imageUrl, imagePrompt } = await generateSceneIllustration(
                        scene.scaffolding,
                        scene.sentence
                    );
                    scene.imageUrl = imageUrl;
                    scene.imagePrompt = imagePrompt;
                } catch (err) {
                    console.error(`Illustration regeneration failed for scene ${scene.sceneNumber}:`, err);
                }
            })
        );

        story.endStoryEditUsed = true;

        await story.save();

        return NextResponse.json({ story });

    } catch (error) {
        return NextResponse.json({ error: "Failed to save edits" }, { status: 500 });
    }
}
