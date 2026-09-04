import { getSession } from "@/lib/auth";
import connectDB from "@/lib/db";
import Story from "@/lib/story";
import { assembleFeedbackPrompt } from "@/lib/rag/assembleFeedbackPrompt";
import OpenAI from "openai";
import { NextResponse } from "next/server";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Feedback generation model. A reasoning model handles the 7-rule instruction
// block and the calibration guardrails far better than the previous Groq
// llama-3.3-70b. Note: reasoning models reject a custom `temperature`.
const FEEDBACK_MODEL = "gpt-5.6-terra";
// The prompt is heavily scaffolded (rule cards, guardrails, exemplars, checklist),
// so low reasoning effort is usually enough and much faster. Bump to "medium" if
// feedback quality drops.
const REASONING_EFFORT = "low" as const;

export async function POST(request: Request) {
    try {
        const session = await getSession();
        if (!session?.user) {
            return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
        }

        const { sentence } = await request.json();
        if (!sentence || !sentence.trim()) {
            return NextResponse.json({ error: "No sentence provided" }, { status: 400 });
        }

        await connectDB();
        const story = await Story.findOne({
            userId: session.user.id,
            status: "in_progress",
        });

        const t0 = Date.now();
        const { system, user, retrievedChunkIds } = await assembleFeedbackPrompt(sentence, {
            storyId: story?.storyId || undefined,
        });
        const tRetrieval = Date.now() - t0;

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
        const tLlmStart = Date.now();

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
                    console.error("Feedback stream error:", err);
                    controller.error(err);
                    return;
                }

                console.log(
                    `feedback timing: retrieval ${tRetrieval}ms, llm ${Date.now() - tLlmStart}ms`
                );

                // Persist once the full text is in hand.
                try {
                    if (story) {
                        story.scenes[story.currentSceneIndex].feedback =
                            full || "No feedback available.";
                        story.scenes[story.currentSceneIndex].feedbackChunkIds =
                            retrievedChunkIds;
                        await story.save();
                    }
                } catch (err) {
                    console.error("Feedback save error:", err);
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
        console.error("Feedback error:", error);
        return NextResponse.json(
            { error: "Failed to generate feedback" },
            { status: 500 }
        );
    }
}
