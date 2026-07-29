import { getSession } from "@/lib/auth";
import connectDB from "@/lib/db";
import Story from "@/lib/story";
import { GoogleGenerativeAI } from "@google/generative-ai";
import Groq from "groq-sdk";
import { NextResponse } from "next/server";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);
const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

export async function POST(request: Request) {
    try {
        const session = await getSession();
        if (!session?.user) {
            return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
        }

        const body = await request.json();
        const { scaffolding, sentence } = body;

        // build prompt
        const prompt = `
You are a Chinese language teacher giving feedback to a student who is learning Chinese.
The student wrote this sentence in Chinese:
"${sentence}"

Please provide feedback in English with three sections:
1. **Grammar Corrections**(bold title). Please indicate the incorrect phrase, the general grammar formula it should follow, and then the correct version. If there are no grammar mistakes, say so. 
    Example 1: Incorrect phrase "我早上九点就出门了！结果迟到了" / Formula, 谁 + (时间) + 才 + (做太早的动作) / Correct, "我早上九点才出门了！结果迟到了"
    Example 2: Incorrect phrase "你被爱了" / Formula, 谁 + 被 + （动作）+ 着/ Correct, "你被爱着". 
    Please insert a blank line before starting each new grammar correction.
    Try to catch ALL grammar mistakes, especially major ones.
2. **Vocabulary Suggestions**(bold title). Suggest more advanced or natural vocabulary they could use. Indicate the specific word that could be better, then the alternative options and explain the conntation of both the word in question and the alternatives.
    Example 1: Word, "漂亮” / Context, "他在决赛中打了一场漂亮的比赛" / Alternatives, 精彩的比赛 emphasizes that the game was exciting, impressive, and enjoyable to watch, while 漂亮 evaluates how well the game was played.
    Example 2: Word, “安静” / Context, “晚上，湖边非常安静” / Alternatives, 宁静 emphasizes a peaceful, calm atmosphere and has a more literary and emotionally positive feeling, while 安静 simply means that there is little noise or activity.
    It describes the experience or content of the game. Please write the explaination in english. 
    Please insert a blank line before starting each new vocab suggestion.
    Please aim to give 5 word choice suggestions.
3. **Encouragement and Next Steps**(bold title).
    (not bold): End with one sentence of genuine encouragement about a specific thing they did well. Perhaps the flow is good, the description is vivid, the thoughts are sophisticated, etc. Then also one line for what to focus on next time.

Keep your feedback concise, clear, and encouraging. The student is a beginner to intermediate learner.
        `;

    // Gemini API setup
        // const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash-lite" });
        // const result = await model.generateContent(prompt);
        // const feedback = result.response.text();

    //Groq API setup
        const completion = await groq.chat.completions.create({
                messages: [{ role: "user", content: prompt }],
                model: "llama-3.3-70b-versatile",
            });

        const feedback = completion.choices[0]?.message?.content || "No feedback available.";

        await connectDB();

        const story = await Story.findOne({
            userId: session.user.id,
            status: "in_progress"
        });

        if (story) {
            // const sceneIndex = story.currentSceneIndex;
            // story.scenes[sceneIndex].feedback = feedback;
            story.scenes[story.currentSceneIndex].feedback = feedback;
            await story.save();
        }

        return NextResponse.json({ feedback });

    } catch (error) {
        console.error("Feedback error:", error);
        return NextResponse.json({ error: "Failed to generate feedback" }, { status: 500 });
    }
}