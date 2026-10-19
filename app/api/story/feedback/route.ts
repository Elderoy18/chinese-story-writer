import { getSession } from "@/lib/auth";
import connectDB from "@/lib/db";
import Story from "@/lib/story";
import { assembleFeedbackPrompt, FEEDBACK_CONFIG } from "@/lib/rag/assembleFeedbackPrompt";
import { displayStreamFilter, feedbackForDisplay } from "@/lib/rag/displayFeedback";
import OpenAI from "openai";
import { NextResponse } from "next/server";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Feedback generation model. A reasoning model handles the rule block and the
// calibration guardrails far better than the previous Groq llama-3.3-70b.
// Note: reasoning models reject a custom `temperature`. Reasoning effort comes from
// the active configuration (FEEDBACK_CONFIG: medium for S7-6, low for the S4 fallback).
const FEEDBACK_MODEL = "gpt-5.6-terra";

// The S7-6 configuration reasons at medium effort: in the evaluation a scene took up to
// ~60 s (median ~30 s). Allow 120 s so the platform default (60 s on some Vercel plans)
// does not cut feedback off mid-stream.
export const maxDuration = 120;

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

        // Earlier scenes give the model context for cross-scene coherence
        // (e.g. whether a pronoun's referent was already introduced).
        const previousScenes: string[] = story
            ? story.scenes
                  .slice(0, story.currentSceneIndex)
                  .filter((s: any) => s.status === "complete" && s.sentence)
                  .map((s: any) => s.sentence)
            : [];

        const t0 = Date.now();
        const { system, user, retrievedChunkIds } = await assembleFeedbackPrompt(sentence, {
            storyId: story?.storyId || undefined,
            previousScenes,
        });
        const tRetrieval = Date.now() - t0;

        const llmStream = await openai.chat.completions.create({
            model: FEEDBACK_MODEL,
            reasoning_effort: FEEDBACK_CONFIG.reasoningEffort,
            stream: true,
            messages: [
                { role: "system", content: system },
                { role: "user", content: user },
            ],
        });

        const encoder = new TextEncoder();
        let full = ""; // raw model text, with the rule citations the learner never sees
        const display = displayStreamFilter();
        const tLlmStart = Date.now();

        const body = new ReadableStream<Uint8Array>({
            async start(controller) {
                try {
                    for await (const chunk of llmStream) {
                        const delta = chunk.choices[0]?.delta?.content ?? "";
                        if (delta) {
                            full += delta;
                            const shown = display.push(delta);
                            if (shown) controller.enqueue(encoder.encode(shown));
                        }
                    }
                    const rest = display.flush();
                    if (rest) controller.enqueue(encoder.encode(rest));
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
                        // feedback = what the learner sees (and sees again on reload);
                        // feedbackRaw = the model's text with its rule citations, for analysis.
                        story.scenes[story.currentSceneIndex].feedback =
                            feedbackForDisplay(full) || "No feedback available.";
                        story.scenes[story.currentSceneIndex].feedbackRaw = full;
                        story.scenes[story.currentSceneIndex].feedbackConfig = FEEDBACK_CONFIG.name;
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
