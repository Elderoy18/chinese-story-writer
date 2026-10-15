# Testing each iteration of input to the feedback system

Over the past months the feedback system was improved with four kinds of input: 1. Teacher critique of the AI's feedback 2. the required-scene lists 3. the vocabulary error list 4. the coherence rules. To see what each one actually changed, the same 6 student stories are run through five versions (iterations) of the system. This document summarizes the results for human review. The full side-by-side outputs, with a checklist for each story, are in the four linked reports at the end.

## 1. How the test was set up

Six graded student retellings were set aside as a test set: three 孟母三迁 (samples 10, 32 and 45) and three 神农尝百草 (samples 8, 19 and 33). Each story was split into three scenes, because the app gives feedback scene by scene. Then it gives one end-of-story comment on whether the story is complete. These six stories were removed from everything the system can look up (to avoid data leakage).

Each version keeps everything from the one before and adds input for the next:

| Version | Iteration Addition |
|---|---|
| **S0: Starting point** | The original instructions to the AI (from July), plus the ability to look up from traditional corrections and grammar points in the RAG system, no human in the loop yet|
| **S1: Teacher critique of the AI feedback** | Rules from "My comment" notes: only flag real errors; check every sentence; the correction and the explanation must both be right; point at the exact wrong phrase; put each problem in the right category; write explanations in English; keep vocabulary suggestions at the student's level. Plus examples of the AI's past mistakes. |
| **S2: Required-scene lists** | The end-of-story check compares the story with the list of required scenes. Scene-by-scene feedback no longer comments on plot. |
| **S3: Vocabulary error list** | Wrong words (用错的词) from the list count as errors and are corrected under Grammar; the entries relevant to each scene are shown to the AI. |
| **S4: Coherence rules** | Teacher's rules on reference (first mention / pronoun / zero form), aspect (了/着/在/zero), and connectors; a new "Coherence & Expressiveness" section; the earlier scenes and the model story are given as context. **S4 is the version of the current system** |

The same six stories and scenes; the same AI model and settings; the same collection of past corrections to look up (RAG database); and the same amount looked up per scene. The only thing that changes from one version to the next is the one input being added.

## 2. Summary of improvement each iteration

**S0 → S1:** The AI stopped over-correcting, but also became too cautious. S0 rewrote almost every sentence into what it found "more natural": for example 一些植物毒得很 → 很毒, and suggesting literary words such as 举例来说 and 品尝. Because it flags nearly everything, S0 finds 86% of database corrections. S1 flags far fewer things (78 → 50), and its explanations name the rule. It dropped errors corrected by the teacher, especially coherence-type ones: 告诉**了**孟子 (no 了 with a speaking verb), missing connectors (因为…所以), and 别人 vs. 人们. It also made at least one wrong correction: 住离墓地太近 → 住**得**离墓地太近, where the teacher correction was 住**在**离墓地太近的地方.

**S1 → S2:** Without the scene list, the end-of-story comment caught almost none of the missing scenes. It mostly asked for "a clearer ending", and one story was called complete. With the list, it named every scene marked missing, often with the right scene number. But it is now stricter. It added about 15 new comments, for example "needs to show he did this *every day*" or "needs to say he became a *famous* philosopher".

**S2 → S3:** Some word-choice errors from the list came back: 以后 → 后来, 毒得很, and 别人. But the AI also missed one that is on the list (他找很多植物, 找 → 找到). Overall this section needs the most refinement/review.

**S3 → S4: coherence rules.** The coherence-type corrections recovered (7 → 10 of 18), including 告诉了 (twice), 老是…常常 (repeated), and 因为孟子现在没有朋友，他老是读书 (connector). S4 also adds 36 coherence comments and 1–3 "expressiveness" ideas per scene, such as adding a character's feeling or a line of speech. The word-choice count dipped back (15 → 12). We cannot yet tell whether that is chance or the longer instructions crowding out vocabulary.
