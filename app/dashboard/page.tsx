import { getSession } from "@/lib/auth";
import { redirect } from "next/navigation";
import { BookOpen, MessageCircle, PenLine } from "lucide-react";
import connectDB from "@/lib/db";
import Story from "@/lib/story";
import Link from "next/link";

export default async function Dashboard() {
    const session = await getSession();

    if (!session?.user) {
        redirect("/sign-in");
    }

    await connectDB();

    const story = await Story.findOne({
        userId: session.user.id,
        status: "in_progress"
    }).lean();

    const hasStoryInProgress = !!story;

    return (
        <div className="container mx-auto px-4 py-16">
            <div className="mx-auto max-w-4xl">
                {/* Greeting */}
                <div className="mb-12 text-center">
                    <h1 className="text-4xl font-bold text-black mb-2">
                        Welcome back, {session.user.name}!
                    </h1>
                    <p className="text-muted-foreground text-lg">
                        What would you like to do today?
                    </p>
                </div>

                {/* 3 Cards */}
                <div className="grid gap-6 md:grid-cols-3">
                    <Link href="/traditional-stories">
                        <div className="flex flex-col items-center text-center p-8 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer">
                            <div className="mb-4 inline-flex h-14 w-14 items-center justify-center rounded-full bg-primary/10">
                                <BookOpen className="h-7 w-7 text-primary" />
                            </div>
                            <h2 className="text-xl font-semibold text-black mb-2">
                                Traditional Stories
                            </h2>
                            <p className="text-muted-foreground text-sm">
                                Watch AI-generated videos of classic Chinese stories with annotations and quizzes.
                            </p>
                        </div>
                    </Link>

                    <Link href="/write-your-own">
                        <div className="flex flex-col items-center text-center p-8 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer">
                            <div className="mb-4 inline-flex h-14 w-14 items-center justify-center rounded-full bg-primary/10">
                                <PenLine className="h-7 w-7 text-primary" />
                            </div>
                            <h2 className="text-xl font-semibold text-black mb-2">
                                Write Your Own
                            </h2>
                            <p className="text-muted-foreground text-sm">
                                {hasStoryInProgress
                                    ? "You have a story in progress. Pick up where you left off!"
                                    : "Write your own Chinese story scene by scene with AI feedback and video generation."
                                }
                            </p>
                            {hasStoryInProgress && (
                                <span className="mt-3 inline-flex items-center gap-1 text-xs font-medium text-primary">
                                    <span className="h-2 w-2 rounded-full bg-primary animate-pulse" />
                                    In Progress — Scene {(story as any).currentSceneIndex + 1}
                                </span>
                            )}
                        </div>
                    </Link>

                    <Link href="/character-interviews">
                        <div className="flex flex-col items-center text-center p-8 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer">
                            <div className="mb-4 inline-flex h-14 w-14 items-center justify-center rounded-full bg-primary/10">
                                <MessageCircle className="h-7 w-7 text-primary" />
                            </div>
                            <h2 className="text-xl font-semibold text-black mb-2">
                                Character Interviews
                            </h2>
                            <p className="text-muted-foreground text-sm">
                                Chat with characters from the stories in Chinese and practice your conversational skills.
                            </p>
                        </div>
                    </Link>
                </div>
            </div>
        </div>
    );
}
