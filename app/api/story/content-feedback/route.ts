import { getSession } from "@/lib/auth";
import connectDB from "@/lib/db";
import Story from "@/lib/story";
import { assembleContentPrompt } from "@/lib/rag/assembleFeedbackPrompt";
import OpenAI from "openai";
import { NextResponse } from "next/server";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Same model/effort as the per-scene feedback route (app/api/story/feedback).
const FEEDBACK_MODEL = "gpt-5.6-terra";
const REASONING_EFFORT = "low" as const;

// POST - end-of-story feedback on overall content completeness. Called once
// after END STORY; grammar/vocab/coherence were already covered per scene.
export async function POST(request: Request) {
    try {
        const session = await getSession();
        if (!session?.user) {
            return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
        }

        const { id } = await request.json();
        if (!id) {
            return NextResponse.json({ error: "No story id provided" }, { status: 400 });
        }

        await connectDB();
        const story = await Story.findOne({
            _id: id,
            userId: session.user.id,
            status: "complete",
        });
        if (!story) {
            return NextResponse.json({ error: "No completed story found" }, { status: 404 });
        }

        const scenes: string[] = story.scenes
            .filter((s: any) => s.status === "complete" && s.sentence)
            .map((s: any) => s.sentence);

        const { system, user, retrievedChunkIds } = await assembleContentPrompt(scenes, {
            storyId: story.storyId || undefined,
        });

        const llmStream = await openai.chat.completions.create({
            model: FEEDBACK_MODEL,
            reasoning_effort: REASONING_EFFORT,
            stream: true,
            messages: [
                { role: "system", content: system },
                { role: "user", content: user },
            ],
        });

        const encoder = new TextEncoder();
        let full = "";

        const body = new ReadableStream<Uint8Array>({
            async start(controller) {
                try {
                    for await (const chunk of llmStream) {
                        const delta = chunk.choices[0]?.delta?.content ?? "";
                        if (delta) {
                            full += delta;
                            controller.enqueue(encoder.encode(delta));
                        }
                    }
                } catch (err) {
                    console.error("Content feedback stream error:", err);
                    controller.error(err);
                    return;
                }

                // Persist once the full text is in hand.
                try {
                    story.contentFeedback = full || "No feedback available.";
                    story.contentFeedbackChunkIds = retrievedChunkIds;
                    await story.save();
                } catch (err) {
                    console.error("Content feedback save error:", err);
                }
                controller.close();
            },
        });

        return new Response(body, {
            headers: {
                "Content-Type": "text/plain; charset=utf-8",
                "Cache-Control": "no-store",
                "X-Accel-Buffering": "no",
            },
        });
    } catch (error) {
        console.error("Content feedback error:", error);
        return NextResponse.json(
            { error: "Failed to generate content feedback" },
            { status: 500 }
        );
    }
}
