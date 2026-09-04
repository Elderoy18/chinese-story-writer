"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { X, PlayCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

interface Question {
    question: string;
    options: string[];
    correctIndex: number;
}

interface Story {
    id: number;
    title: string;
    description: string;
    videoId: string;
    retellId?: string;   // corpus story_id — set only if this story supports "retell in your own words"
    questions: Question[];
}

const stories: Story[] = [
    {
        id: 1,
        title: "《神农尝草》",
        description: "“Shennong Tastes the Hundred Herbs” is an ancient Chinese myth with no known author. One of its earlier records appears in the Huainanzi (《淮南子》), compiled by Liu An (刘安) and others during the Western Han dynasty (西汉).",
        videoId: "LMGF2iZtvm0",
        retellId: "shennong_chang_baicao",
        questions: [
            {
                question: "Which plant is poisonous?",
                options: ["夹竹桃 (jiāzhútáo) Oleander", "灵芝 (língzhī) Linzhi mushroom", "茶 tea leaf"],
                correctIndex: 0,
            },
            {
                question: "2 Why did 神农 feel better later?",
                options: ["He ate the 夹竹桃(jiāzhútáo) Oleander", "He lied down for a while ", "He ate the 灵芝 (língzhī) Linzhi mushroom"],
                correctIndex: 2,
            },
        ],
    },
    {
        id: 2,
        title: "《孟母三迁》",
        description: "“Mencius’s Mother Moves Three Times” is a famous ancient Chinese story about education. It was recorded relatively early in Biographies of Exemplary Women (Lienü Zhuan, 《列女传》), compiled by Liu Xiang (刘向) during the Western Han dynasty (西汉).",
        videoId: "_f4RiobBY0Q",
        questions: [
            {
                question: "孟子的妈妈/孟母为什么要离开墓地？ Why did Mencius’ mother move away from the graveyard?",
                options: ["they cannot afford it", "Mencius’s mother cannot find a job", "Mencius’s imitation of making sacrificial offerings caused troubles"],
                correctIndex: 2,
            },
            {
                question: "孟母为什么要离开城市中心? Why did Mencius’ mother move away from the city center? ",
                options: ["they cannot afford it", "Mencius’s mother cannot find a job", "Mencius’s imitation of buying and selling goods affected his study"],
                correctIndex: 2,
            },
            {
                question: "搬到学校旁边对孟子有什么影响？ What influence was “moving to a place near school” on Mencius? ",
                options: ["he found a job ", "he started to read and study", "he became good at doing business"],
                correctIndex: 2,
            },
        ],
    },
    {
        id: 3,
        title: "《张骞出使西域》",
        description: "“Zhang Qian’s Mission to the Western Regions” is a famous historical story from ancient China. It is recorded mainly in the Records of the Grand Historian (Shiji, 《史记》), written by Sima Qian (司马迁) during the Western Han dynasty (西汉).",
        videoId: "_f4RiobBY0Q",
        retellId: "shennong_chang_baicao",
        questions: [
            {
                question: "张骞为什么要去大月氏？Why did Zhang Qian go to Great Yuezhi?",
                options: ["Han government wanted to have trade with Great Yuezhi", "Han government wanted to attack Great Yuezhi", "Han government wanted to attack Xiongnu with Great Yuezhi"],
                correctIndex: 2,
            },
            {
                question: "为什么甘父是使团的向导？ Why was Ganfu the guide of the diplomatic corps?",
                options: ["he used to be the slave of Han and spoke Chinese well", "he used to be the slave of Xiongnu and knew the terrain well", "he used to be the slave of Great Yuezhi and knew the terrain well"],
                correctIndex: 1,
            },
            {
                question: "张骞为什么放了十年羊? Why had Zhang Qian herded sheep for ten years?",
                options: ["he was taken to prisoner by Xiongnu", "he found this job in Xiongnu", "he was taken prisoner by Dayuan"],
                correctIndex: 2,
            },
            {
                question: "Question 4?",
                options: ["Option A", "Option B", "Option C", "Option D"],
                correctIndex: 0,
            },
            {
                question: "Question 5?",
                options: ["Option A", "Option B", "Option C", "Option D"],
                correctIndex: 3,
            },
        ],
    },
    {
        id: 4,
        title: "《嫦娥奔月》",
        description: "“Chang’e Flies to the Moon” is an ancient Chinese myth with no known author. One of its earlier records appears in the Huainanzi (《淮南子》), compiled by Liu An (刘安) and others during the Western Han dynasty (西汉)",
        videoId: "_f4RiobBY0Q",
        retellId: "shennong_chang_baicao",
        questions: [
            {
                question: "Question 1?",
                options: ["Option A", "Option B", "Option C", "Option D"],
                correctIndex: 0,
            },
            {
                question: "Question 2?",
                options: ["Option A", "Option B", "Option C", "Option D"],
                correctIndex: 1,
            },
            {
                question: "Question 3?",
                options: ["Option A", "Option B", "Option C", "Option D"],
                correctIndex: 2,
            },
            {
                question: "Question 4?",
                options: ["Option A", "Option B", "Option C", "Option D"],
                correctIndex: 0,
            },
            {
                question: "Question 5?",
                options: ["Option A", "Option B", "Option C", "Option D"],
                correctIndex: 3,
            },
        ],
    },
];

type View = "grid" | "video" | "quiz" | "results";

export default function TraditionalStories() {
    const router = useRouter();
    const [view, setView] = useState<View>("grid");
    const [selectedStory, setSelectedStory] = useState<Story | null>(null);
    const [answers, setAnswers] = useState<(number | null)[]>([]);
    const [videoStarted, setVideoStarted] = useState(false);

    function handleSelectStory(story: Story) {
        setSelectedStory(story);
        setAnswers(new Array(story.questions.length).fill(null));
        setView("video");
        setVideoStarted(false);
    }

    function handleClose() {
        setSelectedStory(null);
        setAnswers([]);
        setView("grid");
        setVideoStarted(false);
    }

    function handleStartQuiz() {
        setView("quiz");
    }

    function handleSelectAnswer(questionIndex: number, optionIndex: number) {
        const updated = [...answers];
        updated[questionIndex] = optionIndex;
        setAnswers(updated);
    }

    function handleSubmitQuiz() {
        setView("results");
    }

    function handleDownloadResults() {
        if (!selectedStory) return;

        const score = answers.filter(
            (a, i) => a === selectedStory.questions[i].correctIndex
        ).length;

        const printWindow = window.open("", "_blank");
        if (!printWindow) return;

        printWindow.document.write(`
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Quiz Results - ${selectedStory.title}</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        max-width: 600px;
                        margin: 60px auto;
                        padding: 0 40px;
                        color: #000;
                        line-height: 1.6;
                    }
                    h1 { font-size: 24px; margin-bottom: 4px; }
                    h2 { font-size: 16px; font-weight: normal; color: #555; margin-bottom: 24px; }
                    .score { font-size: 20px; font-weight: bold; margin-bottom: 32px; }
                    .question { margin-bottom: 24px; }
                    .question-text { font-weight: bold; margin-bottom: 8px; }
                    .answer { padding: 4px 0; }
                    .correct { color: #16a34a; }
                    .incorrect { color: #dc2626; }
                    .correct-answer { color: #16a34a; font-size: 14px; }
                </style>
            </head>
            <body>
                <h1>${selectedStory.title} — Quiz Results</h1>
                <div class="score">Score: ${score} / ${selectedStory.questions.length}</div>
                ${selectedStory.questions.map((q, i) => {
                    const studentAnswer = answers[i];
                    const isCorrect = studentAnswer === q.correctIndex;
                    return `
                        <div class="question">
                            <div class="question-text">${i + 1}. ${q.question}</div>
                            <div class="answer ${isCorrect ? "correct" : "incorrect"}">
                                Your answer: ${studentAnswer !== null ? q.options[studentAnswer] : "No answer"} 
                                ${isCorrect ? "✓" : "✗"}
                            </div>
                            ${!isCorrect ? `<div class="correct-answer">Correct answer: ${q.options[q.correctIndex]}</div>` : ""}
                        </div>
                    `;
                }).join("")}
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

    const score = selectedStory
        ? answers.filter((a, i) => a === selectedStory.questions[i].correctIndex).length
        : 0;

    const allAnswered = answers.every((a) => a !== null);

    // --- VIEWS ---

    if (view === "grid") {
        return (
            <div className="container mx-auto px-4 py-16">
                <div className="mx-auto max-w-5xl">
                    <div className="mb-12">
                        <h1 className="text-4xl font-bold text-black mb-2">
                            Traditional Stories
                        </h1>
                        <p className="text-muted-foreground text-lg">
                            Watch classic Chinese stories and improve your listening comprehension.
                        </p>
                    </div>
                    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                        {stories.map((story) => (
                            <div
                                key={story.id}
                                onClick={() => handleSelectStory(story)}
                                className="group rounded-xl border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                            >
                                <div className="relative aspect-video bg-gray-100 overflow-hidden">
                                    <img
                                        src={`https://img.youtube.com/vi/${story.videoId}/hqdefault.jpg`}
                                        alt={story.title}
                                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                                    />
                                    <div className="absolute inset-0 bg-black/20 flex items-center justify-center">
                                        <div className="bg-white/90 rounded-full p-3 group-hover:scale-110 transition-transform">
                                            <div className="bg-white/90 rounded-full p-3 group-hover:scale-110 transition-transform">
                                                <svg
                                                    className="h-5 w-5 text-primary"
                                                    viewBox="0 0 24 24"
                                                    fill="currentColor"
                                                >
                                                    <polygon points="5,3 19,12 5,21" />
                                                </svg>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className="p-4">
                                    <h2 className="font-semibold text-black mb-1 group-hover:text-primary transition-colors">
                                        {story.title}
                                    </h2>
                                    <p className="text-sm text-muted-foreground">
                                        {story.description}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        );
    }

    if (view === "video" && selectedStory) {
        return (
            <div className="container mx-auto px-4 py-16">
                <div className="mx-auto max-w-3xl">
                    <button
                        onClick={handleClose}
                        className="flex items-center gap-2 text-sm text-muted-foreground hover:text-black mb-6 transition-colors"
                    >
                        <X className="h-4 w-4" /> Back to stories
                    </button>
                    <h1 className="text-3xl font-bold text-black mb-6">
                        {selectedStory.title}
                    </h1>
                    <div className="aspect-video rounded-xl overflow-hidden border border-gray-200 shadow-sm mb-8">
                        <div className="relative aspect-video rounded-xl overflow-hidden border border-gray-200 shadow-sm mb-8">
                            {!videoStarted ? (
                                <div
                                    onClick={() => setVideoStarted(true)}
                                    className="cursor-pointer w-full h-full relative"
                                >
                                    <img
                                        src={`https://img.youtube.com/vi/${selectedStory.videoId}/hqdefault.jpg`}
                                        alt={selectedStory.title}
                                        className="w-full h-full object-cover"
                                    />
                                    <div className="absolute inset-0 bg-black/30 flex items-center justify-center">
                                        <div className="bg-white/90 rounded-full p-5 hover:scale-110 transition-transform">
                                            <div className="bg-white/90 rounded-full p-4 hover:scale-110 transition-transform">
                                                <svg
                                                    className="h-8 w-8 text-primary"
                                                    viewBox="0 0 24 24"
                                                    fill="currentColor"
                                                >
                                                    <polygon points="5,3 19,12 5,21" />
                                                </svg>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <iframe
                                    src={`https://www.youtube.com/embed/${selectedStory.videoId}?autoplay=1`}
                                    title={selectedStory.title}
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                    allowFullScreen
                                    className="w-full h-full"
                                />
                            )}
                        </div>
                    </div>
                    <div className="flex justify-end">
                        <Button size="lg" onClick={handleStartQuiz}>
                            Take Quiz →
                        </Button>
                    </div>
                </div>
            </div>
        );
    }

    if (view === "quiz" && selectedStory) {
        return (
            <div className="container mx-auto px-4 py-16">
                <div className="mx-auto max-w-2xl">
                    <div className="mb-8">
                        <p className="text-sm text-muted-foreground mb-1">
                            {selectedStory.title}
                        </p>
                        <h1 className="text-3xl font-bold text-black">Story Quiz</h1>
                        <p className="text-muted-foreground mt-2">
                            Answer all 5 questions about the story.
                        </p>
                    </div>

                    <div className="flex flex-col gap-8 mb-8">
                        {selectedStory.questions.map((q, qi) => (
                            <div key={qi}>
                                <p className="font-medium text-black mb-3">
                                    {qi + 1}. {q.question}
                                </p>
                                <div className="flex flex-col gap-2">
                                    {q.options.map((option, oi) => (
                                        <button
                                            key={oi}
                                            onClick={() => handleSelectAnswer(qi, oi)}
                                            className={`text-left px-4 py-3 rounded-lg border transition-colors ${
                                                answers[qi] === oi
                                                    ? "border-primary bg-primary/10 text-black"
                                                    : "border-gray-200 hover:border-primary/50 text-gray-700"
                                            }`}
                                        >
                                            {option}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="flex justify-between items-center">
                        <button
                            onClick={() => setView("video")}
                            className="text-sm text-muted-foreground hover:text-black transition-colors"
                        >
                            ← Back to video
                        </button>
                        <Button
                            size="lg"
                            onClick={handleSubmitQuiz}
                            disabled={!allAnswered}
                        >
                            Submit Quiz →
                        </Button>
                    </div>
                </div>
            </div>
        );
    }

    if (view === "results" && selectedStory) {
        return (
            <div className="container mx-auto px-4 py-16">
                <div className="mx-auto max-w-2xl">
                    <div className="mb-8">
                        <p className="text-sm text-muted-foreground mb-1">
                            {selectedStory.title}
                        </p>
                        <h1 className="text-3xl font-bold text-black">Quiz Results</h1>
                    </div>

                    {/* score */}
                    <div className="rounded-xl border border-gray-200 p-6 text-center mb-8">
                        <p className="text-muted-foreground mb-1">Your score</p>
                        <p className="text-5xl font-bold text-primary mb-1">
                            {score}/{selectedStory.questions.length}
                        </p>
                        <p className="text-muted-foreground text-sm">
                            {score === selectedStory.questions.length
                                ? "Perfect score! 🎉"
                                : score >= 3
                                ? "Good job! Keep it up."
                                : "Keep practicing — you'll get there!"}
                        </p>
                    </div>

                    {/* question breakdown */}
                    <div className="flex flex-col gap-4 mb-8">
                        {selectedStory.questions.map((q, i) => {
                            const studentAnswer = answers[i];
                            const isCorrect = studentAnswer === q.correctIndex;
                            return (
                                <div
                                    key={i}
                                    className={`rounded-lg border p-4 ${
                                        isCorrect
                                            ? "border-green-200 bg-green-50"
                                            : "border-red-200 bg-red-50"
                                    }`}
                                >
                                    <p className="font-medium text-black mb-2">
                                        {i + 1}. {q.question}
                                    </p>
                                    <p className={`text-sm ${isCorrect ? "text-green-700" : "text-red-700"}`}>
                                        Your answer: {studentAnswer !== null ? q.options[studentAnswer] : "No answer"} {isCorrect ? "✓" : "✗"}
                                    </p>
                                    {!isCorrect && (
                                        <p className="text-sm text-green-700 mt-1">
                                            Correct answer: {q.options[q.correctIndex]}
                                        </p>
                                    )}
                                </div>
                            );
                        })}
                    </div>

                    {/* next steps */}
                    <div className="flex flex-col gap-3 rounded-xl border border-gray-200 p-6">
                        {selectedStory.retellId && (
                            <Button
                                size="lg"
                                className="w-full"
                                onClick={() =>
                                    router.push(`/write-your-own?retell=${selectedStory.retellId}`)
                                }
                            >
                                Tell the Story in Your Own Words →
                            </Button>
                        )}
                        <Button
                            size="lg"
                            variant={selectedStory.retellId ? "outline" : "default"}
                            className="w-full"
                            onClick={handleDownloadResults}
                        >
                            Download Results as PDF
                        </Button>
                    </div>
                </div>
            </div>
        );
    }
}