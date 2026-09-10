"use client";

import { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2, ArrowLeft, Send, Download } from "lucide-react";
import { CHARACTERS, type CharacterProfile } from "@/lib/characters";

interface ChatMessage {
    role: "user" | "assistant";
    content: string;
}

type View = "grid" | "chat";

export default function CharacterInterviews() {
    const [view, setView] = useState<View>("grid");
    const [character, setCharacter] = useState<CharacterProfile | null>(null);
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [input, setInput] = useState("");
    const [isLoadingHistory, setIsLoadingHistory] = useState(false);
    const [isSending, setIsSending] = useState(false);
    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, view]);

    async function handleSelectCharacter(c: CharacterProfile) {
        setCharacter(c);
        setView("chat");
        setInput("");
        setIsLoadingHistory(true);

        const res = await fetch(`/api/character-chat?characterId=${c.id}`);
        const data: { messages?: ChatMessage[] } = await res.json();

        if (data.messages && data.messages.length > 0) {
            setMessages(data.messages.map((m) => ({ role: m.role, content: m.content })));
        } else {
            // Fresh chat: show the character's canned Chinese opener locally.
            setMessages([{ role: "assistant", content: c.openingLine.zh }]);
        }
        setIsLoadingHistory(false);
    }

    function handleBackToGrid() {
        setView("grid");
        setCharacter(null);
        setMessages([]);
    }

    async function handleSend() {
        if (!character || !input.trim() || isSending) return;
        const userMessage = input.trim();
        setInput("");
        setMessages((prev) => [
            ...prev,
            { role: "user", content: userMessage },
            { role: "assistant", content: "" },
        ]);
        setIsSending(true);

        const res = await fetch("/api/character-chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ characterId: character.id, message: userMessage }),
        });

        if (!res.ok || !res.body) {
            setMessages((prev) => {
                const updated = [...prev];
                updated[updated.length - 1] = {
                    role: "assistant",
                    content: "(Something went wrong — please try again.)",
                };
                return updated;
            });
            setIsSending(false);
            return;
        }

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let acc = "";
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            acc += decoder.decode(value, { stream: true });
            setMessages((prev) => {
                const updated = [...prev];
                updated[updated.length - 1] = { role: "assistant", content: acc };
                return updated;
            });
        }
        setIsSending(false);
    }

    function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
        if (e.key === "Enter") {
            e.preventDefault();
            handleSend();
        }
    }

    // Downloads the conversation only -- character + student turns, no student ID.
    // Same print-window approach as the story / feedback PDF exports.
    function handleDownloadConversation() {
        if (!character) return;
        const transcript = messages.filter((m) => m.content.trim());
        if (transcript.length === 0) return;

        const esc = (s: string) =>
            s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        const title = `${character.name}（${character.englishName}）— Interview`;

        const printWindow = window.open("", "_blank");
        if (!printWindow) return;

        printWindow.document.write(`
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>${esc(title)}</title>
                <style>
                    body {
                        font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", sans-serif;
                        max-width: 600px;
                        margin: 60px auto;
                        padding: 0 40px;
                        color: #000;
                        line-height: 1.7;
                    }
                    h1 { font-size: 22px; margin-bottom: 4px; }
                    h2 { font-size: 15px; font-weight: normal; color: #555; margin: 0 0 28px; }
                    .turn { margin-bottom: 18px; }
                    .speaker { font-weight: bold; margin-bottom: 4px; }
                    .text { white-space: pre-wrap; }
                    @media print { body { margin: 40px auto; } }
                </style>
            </head>
            <body>
                <h1>${esc(character.name)}（${esc(character.englishName)}）— Interview</h1>
                <h2>${esc(character.storyTitle)}</h2>
                ${transcript
                    .map(
                        (m) => `
                    <div class="turn">
                        <div class="speaker">${m.role === "user" ? "学生" : esc(character.name)}</div>
                        <div class="text">${esc(m.content.trim())}</div>
                    </div>`
                    )
                    .join("")}
            </body>
            </html>
        `);
        printWindow.document.close();
        printWindow.focus();
        setTimeout(() => {
            printWindow.print();
            printWindow.close();
        }, 500);
    }

    if (view === "grid") {
        return (
            <div className="container mx-auto px-4 py-16">
                <div className="mx-auto max-w-5xl">
                    <div className="mb-12">
                        <h1 className="text-4xl font-bold text-black mb-2">Character Interviews</h1>
                        <p className="text-muted-foreground text-lg">
                            Chat with characters from the stories in Chinese and practice your conversational skills.
                        </p>
                    </div>
                    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                        {Object.values(CHARACTERS).map((c) => (
                            <div
                                key={c.id}
                                onClick={() => handleSelectCharacter(c)}
                                className="flex flex-col items-center text-center p-8 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                            >
                                <div className="mb-4 text-4xl">{c.emoji}</div>
                                <h2 className="font-semibold text-black mb-1">
                                    {c.name}{" "}
                                </h2>
                                <h2 className="font-semibold text-black mb-1">
                                    <span className="text-muted-foreground font-normal">{c.englishName}</span>
                                </h2>
                                <p className="text-sm text-muted-foreground">{c.storyTitle}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        );
    }

    // --- chat view ---
    return (
        <div className="container mx-auto max-w-2xl px-4 py-12">
            <div className="mb-4 flex items-center gap-3">
                <button
                    onClick={handleBackToGrid}
                    className="text-muted-foreground hover:text-black"
                    aria-label="Back to characters"
                >
                    <ArrowLeft className="h-5 w-5" />
                </button>
                <div className="text-2xl">{character?.emoji}</div>
                <div>
                    <h1 className="text-lg font-bold text-black">
                        {character?.name}{" "}
                        <span className="text-muted-foreground font-normal text-sm">
                            ({character?.englishName})
                        </span>
                    </h1>
                    <p className="text-xs text-muted-foreground">{character?.storyTitle}</p>
                </div>
                <Button
                    variant="outline"
                    size="sm"
                    className="ml-auto"
                    onClick={handleDownloadConversation}
                    disabled={isLoadingHistory || messages.filter((m) => m.content.trim()).length === 0}
                >
                    <Download className="h-4 w-4" />
                    Download
                </Button>
            </div>

            <div className="h-[65vh] overflow-y-auto rounded-lg border border-gray-200 bg-gray-50 p-4 mb-4 flex flex-col gap-3">
                {isLoadingHistory ? (
                    <div className="flex h-full items-center justify-center text-muted-foreground">
                        <Loader2 className="h-5 w-5 animate-spin" />
                    </div>
                ) : (
                    messages.map((m, i) => {
                        if (m.role === "user") {
                            return (
                                <div
                                    key={i}
                                    className="self-end max-w-[80%] rounded-lg bg-primary text-primary-foreground px-4 py-2"
                                >
                                    {m.content}
                                </div>
                            );
                        }
                        const isStreamingThis = isSending && i === messages.length - 1;
                        return (
                            <div
                                key={i}
                                className="self-start max-w-[80%] rounded-lg border border-gray-200 bg-white px-4 py-2"
                            >
                                <p className="text-black">
                                    {m.content.trim() || (isStreamingThis ? "…" : "")}
                                </p>
                            </div>
                        );
                    })
                )}
                <div ref={bottomRef} />
            </div>

            <div className="flex gap-2">
                <Input
                    placeholder="Type in Chinese..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={isSending || isLoadingHistory}
                />
                <Button onClick={handleSend} disabled={isSending || isLoadingHistory || !input.trim()}>
                    {isSending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                </Button>
            </div>
        </div>
    );
}
