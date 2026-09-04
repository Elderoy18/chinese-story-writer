import { getSession } from "@/lib/auth";
import { redirect } from "next/navigation";
import connectDB from "@/lib/db";
import Story from "@/lib/story";
import { getRetelling } from "@/lib/retellings";
import StoryWriter from "./story-writer";

export default async function WriteYourOwnPage({
    searchParams,
}: {
    searchParams: Promise<{ retell?: string }>;
}) {
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

    // Resume: surface the video link if the in-progress story is a retelling.
    // Fresh: ?retell=<corpus story_id> offers to start that retelling.
    const { retell } = await searchParams;
    const retelling = serialized
        ? getRetelling(serialized.storyId)
        : getRetelling(retell);

    return <StoryWriter initialStory={serialized} retelling={retelling} />;
}
