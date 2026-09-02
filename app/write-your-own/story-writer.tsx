"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Loader2 } from "lucide-react";
import ReactMarkdown from "react-markdown";

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
}

interface Story {
    _id: string;
    status: "in_progress" | "complete";
    currentSceneIndex: number;
    scenes: Scene[];
    endStoryEditUsed: boolean;
}

type View = "hub" | "scaffolding" | "feedback" | "review" | "edit" | "title" | "complete";

interface Props {
    initialStory: Story | null;
}

export default function StoryWriter({ initialStory }: Props) {
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
    const [editedSentences, setEditedSentences] = useState<string[]>([]);

    // derived state
    const currentScene = story ? story.scenes[story.currentSceneIndex] : null;
    const completedScenes = story ? story.scenes.filter(s => s.status === "complete") : [];
    const canEndStory = completedScenes.length >= 2;
    const canRegenerate = currentScene ? !currentScene.regenerateUsed : false;

    async function handleStartStory() {
        const res = await fetch("/api/story", { method: "POST" });
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

        // fetch AI feedback
        setIsLoadingFeedback(true);
        setView("feedback");
        const res = await fetch("/api/story/feedback", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ scaffolding, sentence }),
        });
        const data = await res.json();
        setFeedback(data.feedback || "No feedback available.");
        setIsLoadingFeedback(false);
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
        const res = await fetch("/api/story/edit", {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ editedSentences }),
        });
        const data = await res.json();
        setStory(JSON.parse(JSON.stringify(data.story)));
        setView("title");
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
                    p { font-size: 16px; margin-bottom: 20px; }
                    @media print { body { margin: 40px auto; } }
                </style>
            </head>
            <body>
                <h1>${title}</h1>
                ${scenes.map(scene => `<p>${scene.sentence}</p>`).join("")}
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
                    .feedback { font-size: 14px; }
                    @media print { body { margin: 40px auto; } }
                </style>
            </head>
            <body>
                <h1>${title} — Feedback Summary</h1>
                ${scenes.map((scene, i) => `
                    <h2>Scene ${i + 1}</h2>
                    <h3>Your sentence:</h3>
                    <div class="sentence">${scene.sentence}</div>
                    <div class="feedback">${scene.feedback || "No feedback recorded."}</div>
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
        return (
            <div className="flex min-h-screen flex-col items-center justify-center gap-6">
                <h1 className="text-4xl font-bold text-black">Write Your Own Story</h1>
                <p className="text-muted-foreground text-lg max-w-md text-center">
                    Write a Chinese story scene by scene. Get AI feedback and a generated video for each scene.
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
                <div className="mb-8">
                    <p className="text-sm text-muted-foreground mb-1">Scene {currentSceneNumber}</p>
                    <h1 className="text-3xl font-bold text-black">Build Your Scene</h1>
                    <p className="text-muted-foreground mt-2">
                        Fill in what comes to mind — these boxes are optional but will help guide your writing and the AI video.
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

                <div className="mb-8 rounded-lg border border-primary/20 p-6 bg-primary/5">
                    <p className="text-sm font-medium text-primary mb-3">AI Feedback</p>
                    {isLoadingFeedback ? (
                        <div className="flex items-center gap-2 text-muted-foreground">
                            <Loader2 className="h-4 w-4 animate-spin" />
                            Generating feedback...
                        </div>
                    ) : (
                        <div className="text-black prose prose-sm max-w-none">
                            <ReactMarkdown
                                components={{
                                    p: ({ children }) => <p className="mb-3">{children}</p>,
                                    strong: ({ children }) => <strong className="font-semibold text-black">{children}</strong>,
                                    ul: ({ children }) => <ul className="list-disc pl-5 mb-3 space-y-1">{children}</ul>,
                                    li: ({ children }) => <li className="text-black">{children}</li>,
                                }}
                            >
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
                        <Button onClick={handleNextScene} disabled={isLoadingFeedback}>
                            NEXT SCENE →
                        </Button>
                        <Button
                            variant="outline"
                            onClick={handleEndStory}
                            disabled={!canEndStory || isLoadingFeedback}
                            title={!canEndStory ? "Complete at least 3 scenes to end your story" : ""}
                        >
                            END STORY
                        </Button>
                    </div>
                </div>

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

                {/* feedback summary */}
                <div className="mb-8">
                    <h2 className="text-lg font-semibold text-black mb-4">Feedback Summary</h2>
                    <div className="flex flex-col gap-6">
                        {completedScenes.map((scene, index) => (
                            <div key={index} className="rounded-lg border border-primary/20 p-5 bg-primary/5">
                                <p className="text-sm font-medium text-primary mb-3">Scene {index + 1} Feedback</p>
                                <div className="text-black prose prose-sm max-w-none">
                                    <ReactMarkdown
                                        components={{
                                            p: ({ children }) => <p className="mb-2">{children}</p>,
                                            strong: ({ children }) => <strong className="font-semibold text-black">{children}</strong>,
                                            ul: ({ children }) => <ul className="list-disc pl-5 mb-2 space-y-1">{children}</ul>,
                                            li: ({ children }) => <li className="text-black">{children}</li>,
                                        }}
                                    >
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
                    >
                        ← Back
                    </Button>
                    <Button
                        className="flex-1"
                        onClick={handleConfirmEdits}
                    >
                        Confirm Edits →
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
                    {story?.scenes
                        .filter(s => s.status === "complete")
                        .map((scene, index) => (
                            <div key={index} className="rounded-lg border border-gray-200 p-4">
                                <p className="text-sm font-medium text-muted-foreground mb-1">
                                    Scene {index + 1}
                                </p>
                                <p className="text-black">{scene.sentence}</p>
                            </div>
                        ))
                    }
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