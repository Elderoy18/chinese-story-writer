import { getSession } from "@/lib/auth";
import { redirect } from "next/navigation";
import connectDB from "@/lib/db";
import Story from "@/lib/story";
import StoryWriter from "./story-writer";

export default async function WriteYourOwnPage() {
    const session = await getSession();

    if (!session?.user) {
        redirect("/sign-in");
    }

    await connectDB();

    const story = await Story.findOne({
        userId: session.user.id,
        status: "in_progress"
    }).lean();

    // convert ObjectIds to plain strings so Next.js can pass to client component
    const serialized = story ? JSON.parse(JSON.stringify(story)) : null;

    return <StoryWriter initialStory={serialized} />;
}