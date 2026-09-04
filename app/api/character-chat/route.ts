import { getSession } from "@/lib/auth";
import connectDB from "@/lib/db";
import CharacterChat from "@/lib/characterChat";
import { getCharacter, buildPersonaPrompt } from "@/lib/characters";
import OpenAI from "openai";
import { NextResponse } from "next/server";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const CHAT_MODEL = "gpt-5.6-terra";
// Conversational persona chat, not deep analysis -- low effort keeps replies snappy.
const REASONING_EFFORT = "low" as const;

// GET ?characterId=xxx -> existing transcript (or empty)
export async function GET(request: Request) {
    try {
        const session = await getSession();
        if (!session?.user) {
            return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
        }

        const characterId = new URL(request.url).searchParams.get("characterId") || "";
        if (!getCharacter(characterId)) {
            return NextResponse.json({ error: "Unknown character" }, { status: 400 });
        }

        await connectDB();
        const chat = await CharacterChat.findOne({ userId: session.user.id, characterId });
        return NextResponse.json({ messages: chat?.messages ?? [] });
    } catch (error) {
        console.error("Character chat history error:", error);
        return NextResponse.json({ error: "Failed to load chat" }, { status: 500 });
    }
}

// POST { characterId, message } -> streamed in-character reply, persisted both ways
export async function POST(request: Request) {
    try {
        const session = await getSession();
        if (!session?.user) {
            return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
        }

        const { characterId, message } = await request.json();
        const character = getCharacter(characterId);
        if (!character) {
            return NextResponse.json({ error: "Unknown character" }, { status: 400 });
        }
        if (!message || !message.trim()) {
            return NextResponse.json({ error: "No message provided" }, { status: 400 });
        }

        await connectDB();
        let chat = await CharacterChat.findOne({ userId: session.user.id, characterId });
        if (!chat) {
            chat = await CharacterChat.create({ userId: session.user.id, characterId, messages: [] });
        }

        // Persist the student's turn immediately so it isn't lost if the LLM call fails.
        chat.messages.push({ role: "user", content: message, createdAt: new Date() });
        await chat.save();

        const llmMessages = [
            { role: "system" as const, content: buildPersonaPrompt(character) },
            ...chat.messages.map((m) => ({ role: m.role, content: m.content })),
        ];

        const llmStream = await openai.chat.completions.create({
            model: CHAT_MODEL,
            reasoning_effort: REASONING_EFFORT,
            stream: true,
            messages: llmMessages,
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
                    console.error("Character chat stream error:", err);
                    controller.error(err);
                    return;
                }

                try {
                    chat.messages.push({
                        role: "assistant",
                        content: full || "……",
                        createdAt: new Date(),
                    });
                    await chat.save();
                } catch (err) {
                    console.error("Character chat save error:", err);
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
        console.error("Character chat error:", error);
        return NextResponse.json({ error: "Failed to generate reply" }, { status: 500 });
    }
}
