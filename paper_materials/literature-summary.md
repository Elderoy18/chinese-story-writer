# Literature Summary: Automatic Essay Multi-Dimensional Scoring with Fine-Tuning & RAG

## Overview
This document contains detailed literature extractions across 17 papers in the field of Automatic Essay Scoring (AES), Automated Writing Evaluation (AWE), Second Language (L2) Assessment, Large Language Models (LLMs), and Retrieval-Augmented Generation (RAG). Each entry systematically details:
1. Title
2. Authors
3. Year
4. Gap
5. Contribution
6. Method
7. Paper Structure
8. Relevance to RAG for language education and writing feedback

---

### 1. Integration of Big Data and Artificial Intelligence in Constructing Learners’ Individualized Feedback System
* **Title**: Integration of Big Data and Artificial Intelligence in Constructing Learners’ Individualized Feedback System
* **Authors**: Chen, Parameshachari
* **Year**: 2023
* **Gap**: Limited integration between AI feedback tools, text-structure analysis, and personalized writing instruction for second language (L2) learners.
* **Contribution**: Proposes an AI-based individualized feedback system with front-end and back-end support units that evaluate structure, context, style, and rhetoric to improve writing quality.
* **Method**: Experimental design dividing 65 intermediate Chinese L2 English learners into experimental and control groups to evaluate multi-draft essay task gains across 8 error categories.
* **Paper Structure**: Introduction (Framing AI in language education) → Literature Review → System Architecture & Implementation → Experimental Design & Findings → Conclusion.
* **Relevance to RAG**: Demonstrates the necessity of retrieving background databases and rubrics to provide context-aware, multi-dimensional feedback in CALL environments.

---

### 2. From Prompting to Preference Optimization: A Comparative Study of LLM-based Automated Essay Scoring
* **Title**: From Prompting to Preference Optimization: A Comparative Study of LLM-based Automated Essay Scoring
* **Authors**: Minh Hoang Nguyen, Vu Hoang Pham, Xuan Thanh Huynh, Phuc Hong Mai, Vinh The Nguyen, Quang Nhut Huynh, Huy Tien Nguyen, Tung Le
* **Year**: 2026
* **Gap**: Prior automated essay scoring (AES) studies analyze individual techniques (prompting, regression, or ranking) in isolation without systematically comparing fine-tuning, prompting, RAG, and preference optimization on a unified L2 benchmark.
* **Contribution**: Provides the first comprehensive comparison of major LLM-based AES paradigms on IELTS Writing Task 2, showing that combining supervised fine-tuning ($k$-SFT) with RAG achieves top performance ($F_1$-score 93%).
* **Method**: Evaluates four paradigms: (1) discriminative encoder fine-tuning, (2) in-context learning/prompting, (3) LoRA instruction tuning + RAG, and (4) SFT + Direct Preference Optimization (DPO) + RAG on 10,328 IELTS essays.
* **Paper Structure**: Introduction → Related Work → Methodology (4 Paradigms & RAG) → Experiments & Results → Discussion & Case Study → Conclusion.
* **Relevance to RAG**: Directly evaluates RAG by retrieving exemplar essays and criterion-specific rubrics to ground LLM-as-a-Judge scoring, significantly reducing hallucinations and improving score calibration for borderline L2 essays.

---

### 3. Can GPT-4 do L2 analytic assessment?
* **Title**: Can GPT-4 do L2 analytic assessment?
* **Authors**: Stefano Bannò, Hari Krishna Vydana, Kate M. Knill, Mark J. F. Gales
* **Year**: 2024
* **Gap**: Uncertainty regarding whether zero-shot or few-shot LLMs can replace or complement human raters in fine-grained multi-trait L2 analytic writing assessment.
* **Contribution**: Assesses GPT-4's capability to grade 9 CEFR-aligned analytic dimensions (linguistic and pragmatic) for L2 English essays and compares performance against fine-tuned Longformer baselines.
* **Method**: Uses a hybrid pipeline combining Longformer-based holistic score prediction with GPT-4 zero-shot prompting to predict 9 analytic criterion scores across CEFR levels.
* **Paper Structure**: Introduction → Related Work → Dataset & L2 Analytic Framework → GPT-4 Analytic Grader Pipeline → Experimental Results → Conclusion.
* **Relevance to RAG**: Highlights how supplying explicit CEFR criteria descriptions within prompt context enhances prompt-based LLM grading consistency.

---

### 4. Automatic Essay Multi-Dimensional Scoring with Fine-Tuning and Multiple Regression
* **Title**: Automatic Essay Multi-Dimensional Scoring with Fine-Tuning and Multiple Regression
* **Authors**: Kun Sun, Rong Wang
* **Year**: 2024
* **Gap**: Traditional AES focuses mainly on overall holistic scores, lacking multi-dimensional analytic scoring mechanisms that incorporate essay prompts, requirements, and topic metadata.
* **Contribution**: Proposes a multi-dimensional scoring architecture combining fine-tuned transformer classifiers, multiple regression, and contrastive learning to process essay topic and requirement metadata.
* **Method**: Fine-tunes pre-trained transformer backbones using joint multi-trait regression objectives augmented with contrastive representation learning.
* **Paper Structure**: Introduction → Methodology (Technical Route & Contrastive Learning) → Experimental Setup → Results & Analysis → Conclusion & Appendix.
* **Relevance to RAG**: Demonstrates the importance of integrating prompt metadata and requirement contexts into scoring models, laying the groundwork for retrieval-augmented prompt conditioning.

---

### 5. Comparison of Scoring Rationales Between Large Language Models and Human Raters
* **Title**: Comparison of Scoring Rationales Between Large Language Models and Human Raters
* **Authors**: Haowei Hua, Hong Jiao, Dan Song
* **Year**: 2025
* **Gap**: Lack of understanding regarding whether LLM scoring rationales align semantically with certified human rater explanations during essay grading.
* **Contribution**: Compares scores and qualitative rationale embeddings between 7 LLMs (GPT-3.5, GPT-4, GPT-4o, Gemini 1.5, Gemini 2.0, Claude 3.5 Sonnet, OpenAI o1) and AP Chinese human raters.
* **Method**: Uses few-shot prompting across 7 LLMs on 30 AP Chinese essays; evaluates score consistency with QWK/NMI and rationale alignment using SBERT embeddings, Cosine Similarity, and PCA.
* **Paper Structure**: Introduction → Related Work → Experimental Setup & Model Prompting → Evaluation Metrics (QWK, NMI, Cosine Similarity, PCA) → Summary & Discussion.
* **Relevance to RAG**: Demonstrates that high-performing LLMs produce rationales closely aligned with human raters, validating the use of retrieved exemplar rationales in RAG-based formative feedback systems.

---

### 6. Towards an Evaluation Methodology for AI in Second Language Education
* **Title**: Towards an Evaluation Methodology for AI in Second Language Education: Lessons Learned from Developing L2-Bench
* **Authors**: James Edgell, Wm. Matthew Kennedy, Isaac Pattis, Ben Knight, Danielle Carvalho, Elizabeth Wonnacott
* **Year**: 2026
* **Gap**: Absence of standardized, context-specific evaluation benchmarks for LLM pedagogical capabilities in second language learning experience design.
* **Contribution**: Develops a 12-competency, 31-subcompetency L2 learning experience design taxonomy and pilot validation methodology for benchmark task items.
* **Method**: Combines expert-curated task design, LLM response generation (Claude Sonnet), and pilot validation ($N=39$) with Krippendorff's alpha and Cronbach's alpha statistical testing.
* **Paper Structure**: Introduction → Related Work → L2-Bench Methodology & Construct → Pilot Study & Iteration → Practitioner Validation Study Design → Conclusion.
* **Relevance to RAG**: Outlines how retrieved pedagogical rubrics and reference gold-standard answers are required for LLM-as-a-Judge auto-scorers to evaluate complex open-ended educational tasks.

---

### 7. Beyond Accuracy: Evaluating AI Systems in Language Education
* **Title**: Beyond Accuracy: Evaluating AI Systems in Language Education
* **Authors**: James Edgell, Wm. Matthew Kennedy, Isaac Pattis, Ben Knight, Danielle Carvalho, Elizabeth Wonnacott
* **Year**: 2026
* **Gap**: Conventional AI benchmarks measure simple NLP accuracy rather than sociotechnical validity, task authenticity, and pedagogical suitability in L2 classrooms.
* **Contribution**: Establishes a statistical framework (L2-Bench) combining mixed-effects models, A/B preference testing, and auto-scorer calibration for language education.
* **Method**: Conducts pilot and full-scale practitioner evaluations using a hierarchical taxonomy and LLM-as-a-Judge auto-scoring pipelines evaluating isolated rubric criteria.
* **Paper Structure**: Introduction → Construct Development → Auto-scorer & Evaluation Protocol → Pilot Validation & Results → Practitioner Design → Conclusion.
* **Relevance to RAG**: Highlights that auto-scorers need in-context retrieved task rubrics and reference context to achieve high inter-judge agreement when evaluating open-ended student responses.

---

### 8. L2-Bench: An Evaluation Benchmark for Measuring LLM Capabilities in Second Language Education
* **Title**: L2-Bench: An Evaluation Benchmark for Measuring LLM Capabilities in Second Language Education
* **Authors**: James Edgell, Wm. Matthew Kennedy, Ben Knight, Danielle Carvalho, Martin Ku, Isaac Pattis
* **Year**: 2026
* **Gap**: Lack of open-source benchmarks evaluating LLM performativity on practical learning experience design principles across diverse L2 educational contexts.
* **Contribution**: Releases L2-Bench—a validated dataset of 1,000+ task-response pairs across 12 competencies validated by 221 global expert practitioners, benchmarking leading frontier models.
* **Method**: Hybrid human-AI authoring pipeline; rubric-based pass/fail scoring; automated LLM-as-a-Judge evaluation optimized via chain-of-thought and reference answer conditioning.
* **Paper Structure**: Abstract → Introduction → L2-Bench Construct & Validation → Benchmarking Results → Discussion → Conclusion & Appendices.
* **Relevance to RAG**: Leverages RAG within the evaluation pipeline by feeding retrieved task contexts, consensus criteria, and reference answers to LLM judges to ensure stable autograding.

---

### 9. Evaluating L2 Chinese Writing with LLM-derived Probabilistic Metrics and Classical Linguistic Metrics
* **Title**: Evaluating L2 Chinese Writing with LLM-derived Probabilistic Metrics and Classical Linguistic Metrics
* **Authors**: Jingying Hu, Yan Cong
* **Year**: 2026
* **Gap**: Standard AWE features fail to capture internal model predictability (surprisal/perplexity) and semantic continuity (embedding-based coherence) in low-resource L2 Chinese writing.
* **Contribution**: Proposes an interpretable pipeline integrating LLM token surprisal, global/local embedding coherence, and classical linguistic metrics for CEFR proficiency classification.
* **Method**: Extracts token/local/global surprisal and contextual embedding similarity from DeepSeek-R1-Distill-Llama-8B, Taiwan-LLM-7B, and GPT-2 Chinese; evaluates 4 ML classifiers across CEFR A2–C1 essays.
* **Paper Structure**: Abstract → Introduction → Feature Extraction Pipeline → Evaluation & Interpretation (Statistical Tests & ML) → Results & Error Analysis → Conclusion.
* **Relevance to RAG**: Demonstrates how embedding-based semantic similarity metrics quantify global discourse coherence, providing a retrieval-based metric framework for L2 essay evaluation.

---

### 10. LAWE-CL2: Multi-agent LLM-based Automated Writing Evaluation System
* **Title**: LAWE-CL2: Multi-agent LLM-based automated writing evaluation system integrating linguistic features with fine-tuning for Chinese L2 writing assessment
* **Authors**: Xuelin Wang, Qihao Yang, Yuxin Hao, Zhijun Wang, Sijia Guo
* **Year**: 2026
* **Gap**: Chinese L2 AWE research lacks integrated scoring and feedback pipelines, suffering from single-agent evaluation bias, limited linguistic reasoning, and uncalibrated feedback.
* **Contribution**: Proposes LAWE-CL2, combining multidimensional linguistic features in prompts, a 3-agent collaborative scoring/adjudication framework, and synthetic feedback fine-tuning.
* **Method**: Uses 52 linguistic indices in advanced prompts, 2 primary rater agents (GPT-4.1-mini & DeepSeek-V3) + 1 meta-arbitrator agent (Qwen3-80B), and fine-tunes Qwen3-8B/GPT-4.1-nano.
* **Paper Structure**: Introduction → Related Work → LAWE-CL2 Methodology → Multi-Agent Scoring & Fine-Tuning Setup → Results → Discussion → Conclusion.
* **Relevance to RAG**: Highlights how retrieving multidimensional benchmark distributions and passing prior agent feedback to a meta-agent enhances evidence-grounded scoring and feedback.

---

### 11. Self-Referential Analytic Assessment: A Profile-Based Approach
* **Title**: Self-Referential Analytic Assessment: A Profile-Based Approach to Evaluating L2 Writing with LLMs
* **Authors**: Stefano Bannò et al. / Cambridge ALTA Project
* **Year**: 2025
* **Gap**: Traditional rank-based metrics (PCC, QWK) in AES mask diagnostic failures due to inter-trait correlations and the halo effect (where overall proficiency skews specific sub-scales).
* **Contribution**: Introduces a self-referential (ipsative) evaluation framework that measures intra-learner profile deviations (relative strengths and weaknesses) using Rasch-calibrated fair average scores.
* **Method**: Evaluates GPT-4.1, Qwen 2.5 72B, and Llama 3.1 70B on 140 ICNALE GRA essays annotated by 12 Rasch-infit-filtered human raters across 10 analytic aspects.
* **Paper Structure**: Introduction → Related Work → Experimental Setup (Data, Rasch Calibration, Prompts) → Limitations of Rank Metrics → Self-Referential Framework → Results & Conclusion.
* **Relevance to RAG**: Demonstrates that LLMs excel at detecting specific diagnostic weaknesses when conditioned on standardized learner profile baselines and rubrics.

---

### 12. LLMs can Perform Multi-Dimensional Analytic Writing Assessments
* **Title**: LLMs can Perform Multi-Dimensional Analytic Writing Assessments: A Case Study of L2 Graduate-Level Academic English Writing
* **Authors**: Zhengxiang Wang, Veronika Makarova, Zhi Li, Jordan Kodner, Owen Rambow
* **Year**: 2025
* **Gap**: Evaluating multi-dimensional writing feedback comments manually is labor-intensive, and existing automated metrics fail to measure feedback specificity and helpfulness.
* **Contribution**: Releases a corpus of 141 L2 graduate literature reviews annotated across 9 criteria and proposes ProEval—an interpretable, problem-focused evaluation framework for feedback quality.
* **Method**: Evaluates GPT-4o, Gemini-1.5-Flash, and Llama-3 70B under 3 interaction modes; ProEval extracts problems, classifies location/suggestions/corrections, and checks relevance.
* **Paper Structure**: Abstract → Introduction → Corpus Overview → ProEval Evaluation Framework → Baselines & Experiments → Further Analyses → Conclusion.
* **Relevance to RAG**: Uses structured prompt instructions with writing topic bibliographies and criteria definitions, demonstrating how RAG-style grounded prompts increase feedback specificity.

---

### 13. Combining the Fine-Tuned GPT Model and Linguistic Complexity Indices in Assessing L2 Spanish Writing
* **Title**: Combining the Fine-Tuned GPT Model and Linguistic Complexity Indices in Assessing Second Language (L2) Spanish Writing
* **Authors**: Pengzhan Yang, Wenqian Huang, Guangyuan Yao
* **Year**: 2025
* **Gap**: Automated essay scoring in non-English languages (like L2 Spanish) often relies solely on LLM prompting or fine-tuning without incorporating domain-specific fine-grained linguistic complexity indices.
* **Contribution**: Demonstrates that combining fine-tuned GPT models with automated clausal/phrasal linguistic complexity indices enhances AES accuracy for L2 Spanish learners.
* **Method**: Extracts fine-grained syntactic and lexical complexity features from Spanish learner corpora (CEDEL2) and integrates them with fine-tuned GPT predictions.
* **Paper Structure**: Introduction → Literature Review → Corpus & Feature Extraction → Model Fine-Tuning & Hybrid Integration → Results & Discussion → Conclusion.
* **Relevance to RAG**: Shows that supplementing generative models with retrieved/computed linguistic complexity profiles improves scoring stability and feedback validity in non-English L2 assessment.

---

### 14. GURUS: A Genre-Based Automated Writing Evaluation System
* **Title**: GURUS: A Genre-Based Automated Writing Evaluation System Incorporating Move Analysis and Sentence Reconstruction for L2 Academic Writing
* **Authors**: Bo-Ren Mau, Hui-Hsien Feng
* **Year**: 2025
* **Gap**: Existing AWE tools focus on low-level surface grammar rather than sentence-level rhetorical move structure (Objective, Method, Results, Conclusions) in academic abstract writing.
* **Contribution**: Proposes GURUS, an AWE system providing indirect corrective feedback (move probability classification via XGBoost) and direct corrective feedback (sentence reconstruction via T5 generators).
* **Method**: Trains an XGBoost classifier on 1.7M OMRC-tagged sentences using vectorized similarity, verb categories, POS ratios, and lexical complexity; uses KeyBERT and 4 T5-small generators for sentence reconstruction.
* **Paper Structure**: Introduction → Literature Review → Methodology (Classifier & T5 Generators) → Results (Classification & Reconstruction Quality) → Web Interface Implementation → Conclusion.
* **Relevance to RAG**: Integrates KeyBERT keyword retrieval with T5 sequence generators, exemplifying how retrieval-augmented keyword conditioning generates rhetorically aligned sentence reconstructions.

---

### 15. ARGUS: A Neuro-Symbolic System Integrating GNNs and LLMs
* **Title**: ARGUS: A Neuro-Symbolic System Integrating GNNs and LLMs for Actionable Feedback on English Argumentative Writing
* **Authors**: L. Ye, S. Zhang
* **Year**: 2025
* **Gap**: Existing AWE systems treat essay evaluation as a black box or target sentence-level grammar, ignoring macro-level logical flaws and argument structure.
* **Contribution**: Introduces ARGUS, a neuro-symbolic framework combining T5 argument graph parsing, Relational Graph Convolutional Networks (GCN) for flaw detection, and T5 feedback generation.
* **Method**: Parses essays into argument graphs (Claims, Premises, Major Claims), detects 7 structural flaws via Relational GCN, and conditions a T5-Large generator on flaw embeddings and essay context.
* **Paper Structure**: Introduction → Related Work (AWE, Argument Mining, Neuro-Symbolic AI) → ARGUS Framework Architecture → Experimental Setup → Results → Conclusion.
* **Relevance to RAG**: Uses graph-structured retrieval and flaw embeddings to condition feedback generation, demonstrating how structured symbolic context prevents hallucinated feedback in writing revision.

---

### 16. CorreGram: Using Corpus Data and Automated Written Corrective Feedback
* **Title**: CorreGram: Using Corpus Data and Automated Written Corrective Feedback in Spanish L2/Heritage Writing
* **Authors**: Sam Davidson
* **Year**: 2024 / 2025
* **Gap**: Written corrective feedback tools for Spanish L2/Heritage learners suffer from rigid 'one-size-fits-all' error correction, ignoring learner L1 background and proficiency levels.
* **Contribution**: Builds CorreGram, a Spanish AWE web app integrating demographic-adapted mT5 GEC models, ERRANT-SP error extraction, and multi-step template/LLM implicit feedback.
* **Method**: Fine-tunes mT5 GEC on synthetic and real learner data (COWS-L2H corpus) conditioned on L1 and course level; extracts edits with ERRANT-SP; generates multi-stage implicit feedback via templates and zero-shot GPT-4.
* **Paper Structure**: Introduction → Pedagogical Background → Technical Background (GEC & LLMs) → Corpus Studies → Model Training → Feedback Generation → Web App Implementation → Conclusion.
* **Relevance to RAG**: Retrieves error-type templates and conditions generative LLM prompts on aligned original and corrected sentence pairs, providing targeted, scaffolded feedback.

---

### 17. Grammatical Error Feedback Generation through Grammatical Lineups
* **Title**: Grammatical Error Feedback Generation through Grammatical Lineups
* **Authors**: Stefano Bannò et al. / Cambridge ALTA Project
* **Year**: 2024 / 2025
* **Gap**: Free-form natural language feedback for essay grammar lacks reference gold standards, making automatic evaluation of feedback quality without manual human annotation extremely difficult.
* **Contribution**: Proposes an implicit, reference-free evaluation framework for Grammatical Error Feedback (GEF) using "grammatical lineups" (foils of essays with varying correction levels: 0%, 25%, 50%, 75%, 100%).
* **Method**: Generates essay foils via GECToR, Gramformer, and GPT-4o; prompts Llama 3 8B, GPT-3.5, and GPT-4o for GEF; evaluates matching accuracy using LLM-as-a-Judge discrimination against lineups and ERRANT M2 files.
* **Paper Structure**: Introduction → Related Work → Grammatical Error Feedback Concept → Grammatical Lineup Framework → Experimental Setup → Results → Discussion & Conclusion.
* **Relevance to RAG**: Demonstrates how feeding retrieved ERRANT M2 error edit files and parallel corrected sentences into LLM prompts produces accurate, comprehensive, and non-lexically-biased feedback.
