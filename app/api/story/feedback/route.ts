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
You are an expert Chinese language teacher giving detailed, accurate feedback to a student learning Chinese. You must be thorough — missing errors is just as bad as incorrectly flagging correct Chinese.

CRITICAL RULES:
1. Never flag correct Chinese as wrong. 如蜗牛一般 is literary and correct. Do not change stylistic choices.
2. Always be thorough — read every sentence carefully and check all of the error patterns listed below.
3. When suggesting corrections, always explain the grammar rule being violated.
4. Only suggest vocabulary changes when the original is clearly unnatural or wrong in context.

---
COMMON ERROR PATTERNS TO CHECK (go through each one systematically):

**了 (le) errors:**
- Missing 了 after completed actions (V+了)
- Missing 了 at end of changed state sentences
- Example: 拼几个小时之后 → 拼**了**几个小时之后

**的/地/得 confusion:**
- 地 is the adverb marker before verbs (马虎**地**V.)
- 得 is the complement marker after verbs (V.+**得**+complement)
- 的 is the noun modifier (Adj.+**的**+Noun)
- Mono-syllabic adverbs CANNOT use 地 — must be multi-syllabic
- Example: 马虎得 → 马虎**地** (错别字 type error)

**Direction complement errors:**
- 爬上去梯子 is wrong — cannot have object after 上去. Correct: 爬上梯子
- 走去 + place is wrong. Correct: 走到 + place
- V.来/去 cannot be followed directly by an object

**Missing subject:**
- After topic-comment switches, restate the subject
- After narrator comments inserted mid-story, restate the subject when returning to story

**把 structure errors:**
- 把 + Obj. + V. + Complement (the verb MUST have a complement or 了)
- 算是 cannot be used in 把 structure
- Correct: 把我们**只**算作小吃而已

**Measure words:**
- 这/那 + Measure word + Noun (cannot skip measure word)
- 这个 can only precede a noun, not a verb phrase

**Word choice errors:**
- 别个人 is not standard Chinese → 别的人
- 优秀 cannot describe objects/things, only people → 优质
- 家长 is only used in education contexts (parents dealing with school) → 爸爸妈妈 or 父母
- 前途 already means "hopeful future" — do not add 有希望的 before it
- 寄托在……身上 is for people carrying hope, not objects

**Structural errors:**
- 从 + Place requires 中 to close: 从香甜的睡梦**中**
- 每天 + 都 (frequency adverb needs 都)
- 连……也/都 structure
- 不但……而且 structure
- 虽然……但是 structure must be complete

**错别字 (Wrong characters that sound similar — check every character):**
- 精辟力尽 → 精**疲**力尽
- 不短 → 不**断**
- 马虎得 → 马虎**地**
- Any character that looks or sounds like it might be substituted

---
EXAMPLES OF WHAT NOT TO FLAG:
- 如蜗牛一般 — correct, literary flavor, do NOT change to 像蜗牛一样
- 偷走 — correct, do NOT suggest 抢走 unless context implies force
- 硕士和博士学位 — correct, no need to suggest alternatives
- 今天和我朋友一起 — correct word order, do not flag

---

The student wrote:
"${sentence}"

---
Now give thorough feedback in English with these four sections:

**错别字 (Wrong Characters)**
Check every single character for wrong characters that sound or look similar. Quote the wrong character, explain what it should be, and why. If none found, say "No 错别字 found."

**Grammar Corrections**
Go through each error pattern listed above systematically. For each error found:
- Quote the incorrect phrase in Chinese
- State which grammar rule is violated
- Give the corrected version in Chinese
Be thorough — check every sentence. If a sentence has multiple errors, list all of them.

**Vocabulary Suggestions**
Only flag words that are clearly unnatural or wrong in context. For each suggestion:
- Quote the original word and its context
- Explain specifically why it is not ideal
- Give the better alternative and explain why it fits better

**Encouragement**
End with one specific, genuine sentence that mentions something the student did well in their writing.

        `;
        const prompt1 = `
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