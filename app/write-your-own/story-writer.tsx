"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Loader2 } from "lucide-react";
import ReactMarkdown from "react-markdown";
import type { Components } from "react-markdown";
import type { Retelling } from "@/lib/retellings";

// Shared renderer for the LLM feedback markdown: section headings ("## Grammar
// Corrections") in bold, one feedback item per line.
const feedbackMarkdownComponents: Components = {
    h1: ({ children }) => <h2 className="font-bold text-black text-[15px] mt-5 mb-2 first:mt-0">{children}</h2>,
    h2: ({ children }) => <h2 className="font-bold text-black text-[15px] mt-5 mb-2 first:mt-0">{children}</h2>,
    h3: ({ children }) => <h3 className="font-semibold text-black mt-4 mb-1">{children}</h3>,
    p: ({ children }) => <p className="mb-3">{children}</p>,
    strong: ({ children }) => <strong className="font-semibold text-black">{children}</strong>,
    ul: ({ children }) => <ul className="list-disc pl-5 mb-3 space-y-1.5">{children}</ul>,
    li: ({ children }) => <li className="text-black">{children}</li>,
};

// Convert the same feedback markdown to printable HTML for the PDF export.
function feedbackToHtml(md: string): string {
    const esc = (s: string) =>
        s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    const inline = (s: string) => s.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    let html = "";
    let inList = false;
    const closeList = () => {
        if (inList) {
            html += "</ul>";
            inList = false;
        }
    };
    for (const raw of md.split(/\r?\n/)) {
        const line = raw.trim();
        if (!line) {
            closeList();
            continue;
        }
        const heading = line.match(/^#{1,4}\s+(.*)$/);
        if (heading) {
            closeList();
            html += `<p class="fb-h">${esc(heading[1])}</p>`;
            continue;
        }
        const item = line.match(/^[-*]\s+(.*)$/);
        if (item) {
            if (!inList) {
                html += "<ul>";
                inList = true;
            }
            html += `<li>${inline(esc(item[1]))}</li>`;
            continue;
        }
        closeList();
        html += `<p>${inline(esc(line))}</p>`;
    }
    closeList();
    return html;
}

interface Scaffolding {
    characters: string;
    objects: string;
    actions: string;
    descriptions: string;
}

interface Scene {
    sceneNumber: number;
    scaffolding: Scaffolding;
    sentence: string;
    originalSentence: string;
    regeneratedSentence: string;
    finalSentence: string;
    status: "draft" | "complete";
    regenerateUsed: boolean;
    feedback: string;
    wasEdited: boolean;
    imageUrl: string;
}

interface Story {
    _id: string;
    status: "in_progress" | "complete";
    storyId: string;
    currentSceneIndex: number;
    scenes: Scene[];
    endStoryEditUsed: boolean;
}

// Grid of scene illustrations, 3 per row, used on the review and complete
// screens. Scenes without an image (generation failed, or hasn't finished yet)
// are skipped rather than showing a broken tile.
function SceneImageGrid({ scenes }: { scenes: Scene[] }) {
    const illustrated = scenes
        .map((scene, index) => ({ scene, index }))
        .filter(({ scene }) => scene.imageUrl);

    if (illustrated.length === 0) {
        return <p className="text-sm text-muted-foreground">No illustrations yet.</p>;
    }

    return (
        <div className="grid grid-cols-3 gap-3">
            {illustrated.map(({ scene, index }) => (
                <div key={index} className="overflow-hidden rounded-lg border border-gray-200">
                    <img src={scene.imageUrl} alt={`Illustration for scene ${index + 1}`} className="w-full" />
                    <p className="p-1.5 text-center text-xs text-muted-foreground">Scene {index + 1}</p>
                </div>
            ))}
        </div>
    );
}

type View = "hub" | "scaffolding" | "feedback" | "review" | "edit" | "title" | "complete";

interface Props {
    initialStory: Story | null;
    retelling: Retelling | null;
}

export default function StoryWriter({ initialStory, retelling }: Props) {
    const [view, setView] = useState<View>(initialStory ? "scaffolding" : "hub");
    const [story, setStory] = useState<Story | null>(initialStory);
    const [scaffolding, setScaffolding] = useState<Scaffolding>(
        initialStory
            ? initialStory.scenes[initialStory.currentSceneIndex].scaffolding
            : { characters: "", objects: "", actions: "", descriptions: "" }
    );
    const [sentence, setSentence] = useState(
        initialStory
            ? initialStory.scenes[initialStory.currentSceneIndex].sentence
            : ""
    );
    const [isSaving, setIsSaving] = useState(false);
    const [storyTitle, setStoryTitle] = useState("");
    const [feedback, setFeedback] = useState("");
    const [isLoadingFeedback, setIsLoadingFeedback] = useState(false);
    const [isGeneratingImage, setIsGeneratingImage] = useState(false);
    const [editedSentences, setEditedSentences] = useState<string[]>([]);
    const [isConfirmingEdits, setIsConfirmingEdits] = useState(false);

    // derived state
    const currentScene = story ? story.scenes[story.currentSceneIndex] : null;
    const completedScenes = story ? story.scenes.filter(s => s.status === "complete") : [];
    const canEndStory = completedScenes.length >= 2;
    const canRegenerate = currentScene ? !currentScene.regenerateUsed : false;

    async function handleStartStory() {
        const res = await fetch("/api/story", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(retelling ? { storyId: retelling.storyId } : {}),
        });
        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            alert(data.error || "Could not start a new story.");
            return;
        }
        const data = await res.json();
        setStory(JSON.parse(JSON.stringify(data.story)));
        setView("scaffolding");
    }

    async function handleSave() {
        setIsSaving(true);
        await fetch("/api/story", {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ scaffolding, sentence }),
        });
        setIsSaving(false);
    }

    // Runs alongside feedback generation, not blocking it. Best-effort: if it
    // fails, the scene simply has no illustration -- feedback still works.
    async function generateSceneImage(currentSentence: string, currentScaffolding: Scaffolding) {
        setIsGeneratingImage(true);
        try {
            const res = await fetch("/api/story/image", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ scaffolding: currentScaffolding, sentence: currentSentence }),
            });
            if (res.ok) {
                const data = await res.json();
                if (data.imageUrl) {
                    setStory((prev) => {
                        if (!prev) return prev;
                        const updatedScenes = [...prev.scenes];
                        updatedScenes[prev.currentSceneIndex] = {
                            ...updatedScenes[prev.currentSceneIndex],
                            imageUrl: data.imageUrl,
                        };
                        return { ...prev, scenes: updatedScenes };
                    });
                }
            }
        } catch {
            // non-fatal
        } finally {
            setIsGeneratingImage(false);
        }
    }

    async function handleEndScene() {
        if (!sentence.trim()) {
            alert("Please fill in the 'In Your Own Words' box before ending the scene.");
            return;
        }

        // save scaffolding + sentence + lock originalSentence
        setIsSaving(true);
        await fetch("/api/story", {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ scaffolding, sentence, saveOriginal: true }),
        });
        setIsSaving(false);

        // fetch AI feedback (streamed) and the scene illustration in parallel
        setIsLoadingFeedback(true);
        setFeedback("");
        setView("feedback");
        generateSceneImage(sentence, scaffolding);

        const res = await fetch("/api/story/feedback", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ sentence }),
        });

        if (!res.ok || !res.body) {
            setFeedback("Sorry — feedback could not be generated. Please try again.");
            setIsLoadingFeedback(false);
            return;
        }

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let acc = "";
        let gotFirstChunk = false;
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            if (!gotFirstChunk) {
                gotFirstChunk = true;
                setIsLoadingFeedback(false);
            }
            acc += decoder.decode(value, { stream: true });
            setFeedback(acc);
        }
        setIsLoadingFeedback(false);
        if (!acc) setFeedback("No feedback available.");
    }

    async function handleRegenerate() {
        // save regeneratedSentence before going back
        await fetch("/api/story", {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ scaffolding, sentence, regenerateUsed: true }),
        });

        if (story) {
            const updatedScenes = [...story.scenes];
            updatedScenes[story.currentSceneIndex] = {
                ...updatedScenes[story.currentSceneIndex],
                regenerateUsed: true,
            };
            setStory({ ...story, scenes: updatedScenes });
        }

        setFeedback("");
        setView("scaffolding");
    }

    async function handleNextScene() {
        const res = await fetch("/api/story", { method: "PUT" });
        const data = await res.json();
        setStory(JSON.parse(JSON.stringify(data.story)));
        setScaffolding({ characters: "", objects: "", actions: "", descriptions: "" });
        setSentence("");
        setFeedback("");
        setView("scaffolding");
    }

    async function handleEndStory() {
        const res = await fetch("/api/story/complete", { method: "PATCH" });
        const data = await res.json();
        const serialized = JSON.parse(JSON.stringify(data.story));
        setStory(serialized);
        // initialize editedSentences with current sentences
        const completed = serialized.scenes.filter((s: Scene) => s.status === "complete");
        setEditedSentences(completed.map((s: Scene) => s.sentence));
        setView("review");
    }

    async function handleConfirmEdits() {
        // Edited scenes get their illustration regenerated server-side before
        // this responds, so it can take a while -- show that on the button.
        setIsConfirmingEdits(true);
        try {
            const res = await fetch("/api/story/edit", {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ editedSentences }),
            });
            const data = await res.json();
            setStory(JSON.parse(JSON.stringify(data.story)));
            setView("title");
        } finally {
            setIsConfirmingEdits(false);
        }
    }

    function handleDownloadStoryPDF() {
        const title = storyTitle || "My Chinese Story";
        const scenes = story?.scenes.filter(s => s.status === "complete") || [];

        const printWindow = window.open("", "_blank");
        if (!printWindow) return;

        printWindow.document.write(`
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>${title}</title>
                <style>
                    body {
                        font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", sans-serif;
                        max-width: 600px;
                        margin: 60px auto;
                        padding: 0 40px;
                        color: #000;
                        line-height: 1.8;
                    }
                    h1 { text-align: center; font-size: 28px; margin-bottom: 40px; }
                    h2 { font-size: 20px; margin: 48px 0 16px; page-break-before: always; }
                    p { font-size: 16px; margin-bottom: 20px; }
                    .gallery { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
                    .gallery figure { margin: 0; }
                    .gallery img { display: block; width: 100%; border-radius: 6px; }
                    .gallery figcaption { text-align: center; font-size: 12px; color: #555; margin-top: 4px; }
                    @media print { body { margin: 40px auto; } }
                </style>
            </head>
            <body>
                <h1>${title}</h1>
                ${scenes.map(scene => `<p>${scene.sentence}</p>`).join("")}
                ${scenes.some(s => s.imageUrl) ? `
                    <h2>Illustrations</h2>
                    <div class="gallery">
                        ${scenes.map((scene, i) => scene.imageUrl ? `
                            <figure>
                                <img src="${scene.imageUrl}" alt="">
                                <figcaption>Scene ${i + 1}</figcaption>
                            </figure>
                        ` : "").join("")}
                    </div>
                ` : ""}
            </body>
            </html>
        `);
        printWindow.document.close();
        printWindow.focus();
        setTimeout(() => { printWindow.print(); printWindow.close(); }, 500);
    }

    function handleDownloadFeedbackPDF() {
        const title = storyTitle || "My Chinese Story";
        const scenes = story?.scenes.filter(s => s.status === "complete") || [];

        const printWindow = window.open("", "_blank");
        if (!printWindow) return;

        printWindow.document.write(`
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>${title} — Feedback Summary</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        max-width: 600px;
                        margin: 60px auto;
                        padding: 0 40px;
                        color: #000;
                        line-height: 1.7;
                    }
                    h1 { font-size: 24px; margin-bottom: 4px; }
                    h2 { font-size: 18px; margin-top: 32px; margin-bottom: 8px; color: #333; }
                    h3 { font-size: 14px; color: #555; margin-bottom: 8px; font-weight: normal; }
                    .sentence { background: #f5f5f5; padding: 12px; border-radius: 6px; margin-bottom: 12px; font-family: "Microsoft YaHei", sans-serif; }
                    .thumb { display: block; max-width: 220px; border-radius: 6px; margin-bottom: 12px; }
                    .feedback { font-size: 14px; }
                    .feedback .fb-h { font-weight: bold; color: #000; margin: 16px 0 6px; }
                    .feedback ul { margin: 0 0 12px; padding-left: 22px; }
                    .feedback li { margin-bottom: 6px; }
                    @media print { body { margin: 40px auto; } }
                </style>
            </head>
            <body>
                <h1>${title} — Feedback Summary</h1>
                ${scenes.map((scene, i) => `
                    <h2>Scene ${i + 1}</h2>
                    ${scene.imageUrl ? `<img class="thumb" src="${scene.imageUrl}" alt="">` : ""}
                    <h3>Your sentence:</h3>
                    <div class="sentence">${scene.sentence}</div>
                    <div class="feedback">${scene.feedback ? feedbackToHtml(scene.feedback) : "No feedback recorded."}</div>
                `).join("")}
            </body>
            </html>
        `);
        printWindow.document.close();
        printWindow.focus();
        setTimeout(() => { printWindow.print(); printWindow.close(); }, 500);
    }

    // --- VIEWS ---

    if (view === "hub") {
        if (retelling) {
            return (
                <div className="flex min-h-screen flex-col items-center justify-center gap-6 px-4">
                    <p className="text-sm font-medium text-primary">Retell the story</p>
                    <h1 className="text-4xl font-bold text-black">{retelling.title}</h1>
                    <p className="text-muted-foreground text-lg max-w-md text-center">
                        Now that you&apos;ve watched the video and taken the quiz, tell the story
                        in your own words — scene by scene, in Chinese. You&apos;ll get feedback
                        on your grammar and on how completely you retold the story.
                    </p>
                    <a
                        href={`https://www.youtube.com/watch?v=${retelling.videoId}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm font-medium text-primary hover:underline"
                    >
                        ▶ Rewatch the video first
                    </a>
                    <Button size="lg" onClick={handleStartStory}>
                        Tell the Story in My Own Words
                    </Button>
                </div>
            );
        }
        return (
            <div className="flex min-h-screen flex-col items-center justify-center gap-6">
                <h1 className="text-4xl font-bold text-black">Write Your Own Story</h1>
                <p className="text-muted-foreground text-lg max-w-md text-center">
                    Write a Chinese story scene by scene. Get AI feedback and a generated illustration for each scene.
                </p>
                <Button size="lg" onClick={handleStartStory}>
                    Start New Story
                </Button>
            </div>
        );
    }

    if (view === "scaffolding") {
        const currentSceneNumber = story ? story.currentSceneIndex + 1 : 1;
        return (
            <div className="container mx-auto max-w-2xl px-4 py-12">
                {retelling && (
                    <div className="mb-6 flex items-center justify-between gap-4 rounded-lg border border-primary/20 bg-primary/5 p-4">
                        <p className="text-sm text-black">
                            You&apos;re retelling <span className="font-semibold">{retelling.title}</span>.
                        </p>
                        <a
                            href={`https://www.youtube.com/watch?v=${retelling.videoId}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="whitespace-nowrap text-sm font-medium text-primary hover:underline"
                        >
                            ▶ Rewatch the video
                        </a>
                    </div>
                )}
                <div className="mb-8">
                    <p className="text-sm text-muted-foreground mb-1">Scene {currentSceneNumber}</p>
                    <h1 className="text-3xl font-bold text-black">Build Your Scene</h1>
                    <p className="text-muted-foreground mt-2">
                        Fill in what comes to mind — these boxes are optional but will help guide your writing and the AI illustration.
                    </p>
                </div>

                <div className="flex flex-col gap-6">
                    <div>
                        <label className="text-sm font-medium text-black mb-1 block">
                            Characters <span className="text-muted-foreground font-normal">(optional)</span>
                        </label>
                        <Input
                            placeholder="Who is in this scene?"
                            value={scaffolding.characters}
                            onChange={(e) => setScaffolding({ ...scaffolding, characters: e.target.value })}
                        />
                    </div>
                    <div>
                        <label className="text-sm font-medium text-black mb-1 block">
                            Objects <span className="text-muted-foreground font-normal">(optional)</span>
                        </label>
                        <Input
                            placeholder="What objects are important?"
                            value={scaffolding.objects}
                            onChange={(e) => setScaffolding({ ...scaffolding, objects: e.target.value })}
                        />
                    </div>
                    <div>
                        <label className="text-sm font-medium text-black mb-1 block">
                            Actions <span className="text-muted-foreground font-normal">(optional)</span>
                        </label>
                        <Input
                            placeholder="What is happening?"
                            value={scaffolding.actions}
                            onChange={(e) => setScaffolding({ ...scaffolding, actions: e.target.value })}
                        />
                    </div>
                    <div>
                        <label className="text-sm font-medium text-black mb-1 block">
                            Descriptions <span className="text-muted-foreground font-normal">(optional)</span>
                        </label>
                        <Input
                            placeholder="How does it look, feel, sound?"
                            value={scaffolding.descriptions}
                            onChange={(e) => setScaffolding({ ...scaffolding, descriptions: e.target.value })}
                        />
                    </div>
                    <div>
                        <label className="text-sm font-medium text-black mb-1 block">
                            In Your Own Words <span className="text-red-500">*</span>
                        </label>
                        <Textarea
                            placeholder="Now try to write this scene in Chinese in your own words..."
                            className="min-h-32"
                            value={sentence}
                            onChange={(e) => setSentence(e.target.value)}
                        />
                    </div>
                    <div className="flex justify-between pt-2">
                        <Button variant="outline" onClick={handleSave} disabled={isSaving}>
                            {isSaving ? (
                                <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Saving...</>
                            ) : "Save Progress"}
                        </Button>
                        <Button onClick={handleEndScene} disabled={isSaving}>
                            END SCENE →
                        </Button>
                    </div>
                </div>
            </div>
        );
    }

    if (view === "feedback") {
        return (
            <div className="container mx-auto max-w-2xl px-4 py-12">
                <div className="mb-8">
                    <p className="text-sm text-muted-foreground mb-1">
                        Scene {story ? story.currentSceneIndex + 1 : 1}
                    </p>
                    <h1 className="text-3xl font-bold text-black">Scene Feedback</h1>
                </div>

                <div className="mb-6 rounded-lg border border-gray-200 p-4 bg-gray-50">
                    <p className="text-sm font-medium text-muted-foreground mb-1">Your sentence</p>
                    <p className="text-black">{sentence}</p>
                </div>

                <div className="mb-6 overflow-hidden rounded-lg border border-gray-200 bg-gray-50">
                    {isGeneratingImage ? (
                        <div className="flex aspect-square items-center justify-center gap-2 text-muted-foreground">
                            <Loader2 className="h-4 w-4 animate-spin" />
                            Illustrating your scene...
                        </div>
                    ) : currentScene?.imageUrl ? (
                        <img
                            src={currentScene.imageUrl}
                            alt="Illustration of your scene"
                            className="w-full"
                        />
                    ) : null}
                </div>

                <div className="mb-8 rounded-lg border border-primary/20 p-6 bg-primary/5">
                    <p className="text-sm font-medium text-primary mb-3">AI Feedback</p>
                    {isLoadingFeedback ? (
                        <div className="flex items-center gap-2 text-muted-foreground">
                            <Loader2 className="h-4 w-4 animate-spin" />
                            Generating feedback...
                        </div>
                    ) : (
                        <div className="text-black prose prose-sm max-w-none">
                            <ReactMarkdown components={feedbackMarkdownComponents}>
                                {feedback}
                            </ReactMarkdown>
                        </div>
                    )}
                </div>

                <div className="flex gap-4 justify-between">
                    <div className="flex gap-2">
                        {canRegenerate ? (
                            <Button variant="outline" onClick={handleRegenerate} disabled={isLoadingFeedback}>
                                REGENERATE
                            </Button>
                        ) : (
                            <Button variant="outline" disabled>REGENERATE</Button>
                        )}
                    </div>
                    <div className="flex gap-2">
                        <Button onClick={handleNextScene} disabled={isLoadingFeedback || isGeneratingImage}>
                            NEXT SCENE →
                        </Button>
                        <Button
                            variant="outline"
                            onClick={handleEndStory}
                            disabled={!canEndStory || isLoadingFeedback || isGeneratingImage}
                            title={!canEndStory ? "Complete at least 3 scenes to end your story" : ""}
                        >
                            END STORY
                        </Button>
                    </div>
                </div>

                {isGeneratingImage && (
                    <p className="text-sm text-muted-foreground mt-4">
                        Finishing your scene's illustration before you continue...
                    </p>
                )}
                {!canRegenerate && (
                    <p className="text-sm text-muted-foreground mt-4">
                        You have used your regeneration for this scene.
                    </p>
                )}
                {!canEndStory && (
                    <p className="text-sm text-muted-foreground mt-2">
                        Complete at least 3 scenes before ending your story.
                    </p>
                )}
            </div>
        );
    }

    if (view === "review") {
        return (
            <div className="container mx-auto max-w-2xl px-4 py-12">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-black">Your Full Story</h1>
                    <p className="text-muted-foreground mt-2">
                        Read through your complete story and all the feedback before deciding whether to make any final edits.
                    </p>
                </div>

                {/* full story */}
                <div className="mb-8">
                    <h2 className="text-lg font-semibold text-black mb-4">Story</h2>
                    <div className="flex flex-col gap-4">
                        {completedScenes.map((scene, index) => (
                            <div key={index} className="rounded-lg border border-gray-200 p-4">
                                <p className="text-sm font-medium text-muted-foreground mb-1">Scene {index + 1}</p>
                                <p className="text-black">{scene.sentence}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* illustrations */}
                <div className="mb-8">
                    <h2 className="text-lg font-semibold text-black mb-4">Illustrations</h2>
                    <SceneImageGrid scenes={completedScenes} />
                </div>

                {/* feedback summary */}
                <div className="mb-8">
                    <h2 className="text-lg font-semibold text-black mb-4">Feedback Summary</h2>
                    <div className="flex flex-col gap-6">
                        {completedScenes.map((scene, index) => (
                            <div key={index} className="rounded-lg border border-primary/20 p-5 bg-primary/5">
                                <p className="text-sm font-medium text-primary mb-3">Scene {index + 1} Feedback</p>
                                <div className="text-black prose prose-sm max-w-none">
                                    <ReactMarkdown components={feedbackMarkdownComponents}>
                                        {scene.feedback || "No feedback recorded."}
                                    </ReactMarkdown>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* action buttons */}
                <div className="flex flex-col gap-3">
                    <Button
                        className="w-full"
                        onClick={() => setView("edit")}
                    >
                        Edit My Story →
                    </Button>
                    <Button
                        variant="outline"
                        className="w-full"
                        onClick={() => setView("title")}
                    >
                        Finalize and Download My Story →
                    </Button>
                </div>
            </div>
        );
    }

    if (view === "edit") {
        return (
            <div className="container mx-auto max-w-2xl px-4 py-12">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-black">Edit Your Story</h1>
                    <p className="text-muted-foreground mt-2">
                        Make any final changes — add details, improve flow, or connect ideas between scenes.
                    </p>
                </div>

                <div className="flex flex-col gap-6 mb-8">
                    {completedScenes.map((scene, index) => (
                        <div key={index}>
                            <label className="text-sm font-medium text-black mb-2 block">
                                Scene {index + 1}
                            </label>
                            <Textarea
                                className="min-h-28"
                                value={editedSentences[index] || ""}
                                onChange={(e) => {
                                    const updated = [...editedSentences];
                                    updated[index] = e.target.value;
                                    setEditedSentences(updated);
                                }}
                            />
                        </div>
                    ))}
                </div>

                <div className="flex gap-3">
                    <Button
                        variant="outline"
                        onClick={() => setView("review")}
                        className="flex-1"
                        disabled={isConfirmingEdits}
                    >
                        ← Back
                    </Button>
                    <Button
                        className="flex-1"
                        onClick={handleConfirmEdits}
                        disabled={isConfirmingEdits}
                    >
                        {isConfirmingEdits ? (
                            <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Updating illustrations...</>
                        ) : "Confirm Edits →"}
                    </Button>
                </div>
            </div>
        );
    }

    if (view === "title") {
        return (
            <div className="flex min-h-screen flex-col items-center justify-center gap-6">
                <h1 className="text-3xl font-bold text-black">Give Your Story a Title</h1>
                <p className="text-muted-foreground">This will appear on your downloadable story.</p>
                <Input
                    className="max-w-sm text-center text-lg"
                    placeholder="My Chinese Story"
                    value={storyTitle}
                    onChange={(e) => setStoryTitle(e.target.value)}
                />
                <Button
                    size="lg"
                    onClick={() => setView("complete")}
                    disabled={!storyTitle.trim()}
                >
                    Generate My Story →
                </Button>
            </div>
        );
    }

    if (view === "complete") {
        return (
            <div className="container mx-auto max-w-2xl px-4 py-12">
                <div className="mb-8 text-center">
                    <h1 className="text-3xl font-bold text-black mb-2">
                        {storyTitle || "My Chinese Story"}
                    </h1>
                    <p className="text-muted-foreground">Your story is complete!</p>
                </div>

                {/* full story preview */}
                <div className="flex flex-col gap-4 mb-8">
                    {completedScenes.map((scene, index) => (
                        <div key={index} className="rounded-lg border border-gray-200 p-4">
                            <p className="text-sm font-medium text-muted-foreground mb-1">
                                Scene {index + 1}
                            </p>
                            <p className="text-black">{scene.sentence}</p>
                        </div>
                    ))}
                </div>

                {/* illustrations */}
                <div className="mb-8">
                    <h2 className="text-lg font-semibold text-black mb-4">Illustrations</h2>
                    <SceneImageGrid scenes={completedScenes} />
                </div>

                {/* download buttons */}
                <div className="flex flex-col gap-3">
                    <Button size="lg" className="w-full" onClick={handleDownloadStoryPDF}>
                        Download Story PDF
                    </Button>
                    <Button size="lg" variant="outline" className="w-full" onClick={handleDownloadFeedbackPDF}>
                        Download Feedback Summary
                    </Button>
                </div>
            </div>
        );
    }
}