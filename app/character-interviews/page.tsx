import { getSession } from "@/lib/auth";
import { redirect } from "next/navigation";
import CharacterInterviews from "./character-interviews";

export default async function CharacterInterviewsPage() {
    const session = await getSession();

    if (!session?.user) {
        redirect("/sign-in");
    }

    return <CharacterInterviews />;
}
