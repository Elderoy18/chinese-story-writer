"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Loader2 } from "lucide-react";

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
    status: "draft" | "complete";
    regenerateUsed: boolean;
}

interface Story {
    _id: string;
    status: "in_progress" | "complete";
    currentSceneIndex: number;
    scenes: Scene[];
}

type View = "hub" | "scaffolding" | "feedback" | "title" | "complete";

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
    // start a new story
    async function handleStartStory() {
        const res = await fetch("/api/story", { method: "POST" });
        const data = await res.json();
        setStory(data.story);
        setView("scaffolding");
    }
    const canEndStory = story ? story.scenes.filter(s => s.status === "complete").length >= 2 : false;
    
    // save scaffolding to DB
    async function handleSave() {
        setIsSaving(true);
        await fetch("/api/story", {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ scaffolding, sentence }),
        });
        setIsSaving(false);
    }

    async function handleNextScene() {
        const res = await fetch("/api/story", { method: "PUT" });
        const data = await res.json();
        setStory(data.story);
        // reset the form fields for the new scene
        setScaffolding({ characters: "", objects: "", actions: "", descriptions: "" });
        setSentence("");
        setView("scaffolding");
    }

    // end scene - save and move to feedback view
    async function handleEndScene() {
        console.log("handleEndScene called");
        if (!sentence.trim()) {
            alert("Please fill in the 'In Your Own Words' box before ending the scene.");
            return;
        }
        console.log("sentence is filled, saving...");
        await handleSave();
        console.log("saved, switching to feedback view");
        setView("feedback");
    }

    async function handleEndStory() {
        const res = await fetch("/api/story/complete", {
            method: "PATCH",
        });
        const data = await res.json();
        setStory(data.story); // add this line
        setView("title");
    }

    async function handleDownloadPDF() {
        const { jsPDF } = await import("jspdf");
        const doc = new jsPDF();

        const title = storyTitle || "My Chinese Story";
        const scenes = story?.scenes.filter(s => s.status === "complete") || [];

        // title
        doc.setFontSize(22);
        doc.text(title, 105, 20, { align: "center" });

        // scenes as plain paragraphs
        doc.setFontSize(12);
        doc.setFont("helvetica", "normal");
        let y = 40;
        scenes.forEach((scene) => {
            const lines = doc.splitTextToSize(scene.sentence, 170);
            doc.text(lines, 20, y);
            y += lines.length * 7 + 10;

            if (y > 270) {
                doc.addPage();
                y = 20;
            }
        });

        doc.save(`${title}.pdf`);
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
                            ) : (
                                "Save Progress"
                            )}
                        </Button>
                        <Button onClick={handleEndScene}>
                            END SCENE →
                        </Button>
                    </div>
                </div>
            </div>
        );
    }

    if (view === "feedback") {
        return (
            <div className="flex min-h-screen flex-col items-center justify-center gap-6">
                <h1 className="text-3xl font-bold text-black">Scene Feedback</h1>
                <p className="text-muted-foreground">AI feedback and video will appear here.</p>
                <div className="flex gap-4">
                    <Button variant="outline" onClick={() => setView("scaffolding")}>
                        REGENERATE
                    </Button>
                    <Button onClick={handleNextScene}>
                        NEXT SCENE →
                    </Button>
                    <Button 
                        variant="outline" 
                        onClick={handleEndStory}
                        disabled={!canEndStory}
                        title={!canEndStory ? "Complete at least 3 scenes to end your story" : ""}
                    >
                        END STORY
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
            <div className="flex min-h-screen flex-col items-center justify-center gap-6">
                <h1 className="text-3xl font-bold text-black">
                    {storyTitle || "My Chinese Story"}
                </h1>
                <p className="text-muted-foreground">
                    Your story is ready to download!
                </p>
                {/* preview the sentences */}
                <div className="max-w-xl w-full flex flex-col gap-4">
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
                <Button size="lg" onClick={handleDownloadPDF}>
                    Download as PDF
                </Button>
            </div>
        );
    }
}