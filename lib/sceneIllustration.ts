import OpenAI from "openai";
import type { IScaffolding } from "@/lib/story";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Fast text model to turn the scene into a clean illustration prompt.
const PROMPT_MODEL = "gpt-5.6-terra";
// Check current OpenAI pricing before scaling this up -- gpt-image-1 is the
// budget tier; gpt-image-1.5 / gpt-image-2 cost more for higher fidelity.
const IMAGE_MODEL = "gpt-image-1";
const STYLE_DIRECTIVE =
    "Style: warm, gentle children's storybook illustration, soft colors, painterly brushwork, consistent whimsical art style.";

async function buildIllustrationPrompt(
    scaffolding: IScaffolding | undefined,
    sentence: string
): Promise<string> {
    const completion = await openai.chat.completions.create({
        model: PROMPT_MODEL,
        reasoning_effort: "low",
        messages: [
            {
                role: "system",
                content: `You are an art director writing prompts for a children's storybook illustrator. Given a scene from a student's Chinese story -- their raw planning notes and the sentence they wrote, which may contain grammar mistakes -- write ONE vivid, concrete illustration prompt in English, 2-4 sentences, describing exactly what should be depicted: setting, characters, actions, mood. Interpret past any grammar mistakes to what the student clearly meant.

Rules:
- Do not include any Chinese characters, English text, or any legible writing/signage in the description -- the image must not contain legible text of any kind.
- Keep the content wholesome and age-appropriate for a young language learner.
- Never mention that this is based on a student's writing, and don't explain yourself -- output only the prompt.
- End with this exact line: "${STYLE_DIRECTIVE}"`,
            },
            {
                role: "user",
                content: `Planning notes -- Characters: ${scaffolding?.characters || "(none given)"}; Objects: ${scaffolding?.objects || "(none given)"}; Actions: ${scaffolding?.actions || "(none given)"}; Descriptions: ${scaffolding?.descriptions || "(none given)"}

Student's sentence (Chinese, may contain errors): ${sentence}`,
            },
        ],
    });

    return completion.choices[0]?.message?.content?.trim() || `${sentence}\n${STYLE_DIRECTIVE}`;
}

export interface SceneIllustration {
    imageUrl: string;
    imagePrompt: string;
}

/** Generate one scene's illustration: build the prompt, then call the image model. */
export async function generateSceneIllustration(
    scaffolding: IScaffolding | undefined,
    sentence: string
): Promise<SceneIllustration> {
    const imagePrompt = await buildIllustrationPrompt(scaffolding, sentence);

    const imageResponse = await openai.images.generate({
        model: IMAGE_MODEL,
        prompt: imagePrompt,
        size: "1024x1024",
        quality: "medium",
        output_format: "jpeg",
        output_compression: 80,
        n: 1,
    });

    const b64 = imageResponse.data?.[0]?.b64_json;
    if (!b64) {
        throw new Error("Image generation returned no image");
    }

    return { imageUrl: `data:image/jpeg;base64,${b64}`, imagePrompt };
}
