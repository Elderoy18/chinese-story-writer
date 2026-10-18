_Sign up Sign in_ Cc) 

_Open in app_ 

_Search Write_ 



_LLM_ ~~+~~ _Generative Ai Tools_ ~~+~~ _Rag_ ~~+~~ _Mlops_ ~~+~~ _NLP_ 

# **_9 Methods to Enhance the Performance of a LLM RAG Application_** 



<!-- Start of picture text -->
@<br><!-- End of picture text -->

_Tam Nguyen Follow 8 min read · Nov 19, 2023_ CC) _150 1_ Q a 

It is easy to prototype your first LLM RAG (Retrieval Augmented Generation) application, e.g. using this <u>chat-langchain template with below architecture.</u> 



<!-- Start of picture text -->
perme >> > > ay > C=) > newer<br>|<br>| ———_<br><!-- End of picture text -->

_Image by LangChain_ 

But it is hard to make it work well. In this article, I gather and share some approaches to enhance the performance of the LLM RAG application. 

For more details, please refer to references I mention in each section. 

## **_1. Store message histories and user feedbacks_** 

Chat histories and user feedbacks are important for the application analytics. We will use them later in a next session. 



<!-- Start of picture text -->
[_catecton | [__enaananeis| [ent seein] [<br>name ‘ok:| collection_uuid 1 JFx] session wis pox! rks] userwia bo name<br>metadata vector_embedding \ 04 F2| embedding_uuids \ metadata ‘ created_at<br>created_at document generated_question| | created_at \ updated_at<br>updated_at metadata distance_scrores ‘ . updated_at '<br>created_at chat_type re analysis_uuid<br>updated_at metadata \ message type<br>created_at sof ex2 cession_wuia<br>updated_at message<br>created_at<br><!-- End of picture text -->

In an above schema, 1 collection should have multiple embeddings. 1 user can have many chat sessions, and in each chat session, we store the messages (between human and AI) and their analytical information such as generated questions (condense questions or questions after query transformations), retrieved chunks and corresponding distance scores, user feedback, .etc. 

## **_2. Start evaluating your application_** 

A naive RAG app can have some challenges, e.g.: bad retrieval (low precision, low recall, outdated information), bad response generation (hallucination, irrelevance, toxicity/bias), .etc. 

Before improving it, we need a way to measure its performance. We can use the following <u>ragas metrics for the evaluation.</u> 



<!-- Start of picture text -->
Retriever Generator<br>context_precision faithfulness - answer_similarity<br>verifyGiven a question and a context, How factually accurate is the generated answer. typasures if the generated answer is<br>is usefulif the informationin answeringin the given the question.context PenalizesEnsures claims output not deducedalign with from the context. the context. :hosimilarGoes to a ongroundeaetruths answer.obora Goese.<br>Penalizes redundant information. Calculated using the question, answer and context. i 9<br>Can requiredit___context_recallretrieve toall answerthe relevant the question.: information airs hee ianswer_relevancyme generated= answer Athe uestion,|| ( answer_correctnesspre=  bas e on -<br>usingGauges the the annotated recall of answer the retnevedicontaxt as a reference. lowPenalizesDeriveddirectly  redundancyfontthe responseth  addresses or4 incompleteness.the question. ii__ (answer_similaribut faithfulness| is calculatedhs ithfulness)/2, by<br>Based on the groud_truths and context. ferived from the question and answer. | question, groud_truths and answer.<br><!-- End of picture text -->

Because some scores need `ground_truth` , there are 2 ways to create the labeled evaluation dataset: 

- Human-annotated labeled dataset: we can use some real questions and answers that users give good feedback from the first method `chat_analysis` table. 

- Generated labeled dataset (good for cold start): Prompt GPT-4 Turbo to generate questions from each chunk or multiple chunks to get pairs of question & doc chunks. Then run above pairs of question & context through GPT-4 Turbo to generate answer. 

Eventually we can run through this labeled dataset with above pre-defined metrics and use GPT-4 Turbo as an evaluator/judge. 

For a better observation, we should also use some LLMOps platforms such as <u>LangSmith, MLflow or integrate DeepEval in CI/CD pipelines.</u> 

**_3._** **_<u>Multi-vector retriever</u>_** 

When splitting documents for retrieval, there are often conflicting desires: 

- We may want to have small chunks, so that their embeddings can most accurately reflect their meaning. If too long, then the embeddings can lose meaning. 

- We also want to have long enough documents that the contexts are retained. Separating the document many times by `separators` and `chunk_size` sometimes breaks the context unexpectedly. It's also hard to 

- combine the chunks in a right order to form the meaningful document for a prompt context. 

Below approaches allow us to balance precise embeddings and context retention by splitting documents into smaller chunks for embedding but retrieving larger text information or even the whole original document for the prompt context, since many LLM models nowadays support long context window, e.g. GPT-4 Turbo supports 128,000 tokens. 



<!-- Start of picture text -->
Small chunks: The data is indexed by a subset of the documents<br>——<br>— I \@uooDooOe<br>=<===-|— we =<br>Parentdocuments Child documents Vector database<br>Hypothetical Queries: The data is indexed by the possible questions about it<br>== What questions jA_mN —<br>| | > documentdoes the = SeononsS. = | = |<br>answer? _ggeanesa~— \<br>OOOO] _|<br>Vector database<br>Summaries: The data is indexed by its summary<br>| : =| thesummaryCreateadocumentof |"|_/ @ssssss0~— =eaeessss-— \\ | = : |<br>| | zz Vector database ||<br><!-- End of picture text -->

_Image by TheAiEdge_ 

### **_<u>Parent Document Retriever</u>_** 

- Instead of indexing entire documents, data is divided into smaller chunks, referred to as Parent and Child documents. 

- Child documents are indexed for better representation of specific concepts, while parent documents are retrieved to ensure context retention. 

- Sometimes, the full documents can be too big to retrieve them as is. In that case, first split the raw documents into larger chunks, and then split 

them into smaller chunks. We then index the smaller chunks, but on retrieval we retrieve the larger chunks (but still not the full documents). 

### **_Hypothetical Questions_** 

- Documents are processed to generate potential questions they might answer. 

- These questions are then indexed for better representation of specific concepts, while parent documents are retrieved to ensure context retention. 

### **_Summaries_** 

- Instead of indexing the entire document, a summary of the document is created and indexed. 

- Similarly, the parent document is retrieved in the application. 

## **_4. Query transformations_** 

Because the original query can not be always optimal to retrieve for the LLM, especially in the real world. The user often doesn’t provide the full context and thinks about the question from a specific angle. 

Query transformation deals with transformations of the user’s question before passing to the embedding model. Below are a few variations of query transform methods and their sample prompt implementation. They are all using an LLM to generate a new or multiple new queries. 

1. <u>Rewrite-Retrieve-Read</u> 

2. <u>Hypothetical Document Embeddings (HyDE)</u> 

3. <u>Follow-up question to condensed/standalone one</u> 

4. <u>RAG Fusion</u> 

5. <u>Step-Back Prompting</u> 

6. <u>Multi Query Retrieval / Expansion</u> 

We can also combine multiple query transformation techniques to get the best result e.g. 



<!-- Start of picture text -->
; oe Multi Query _ —<br>| Question : >| Expansion ; > yD - EmbGen rat on e dd i ng |<br><!-- End of picture text -->

## **_5. Query construction for retrieval optimization_** 

### **_<u>Self-querying</u>_** 

Do you remember a `metadata` column in an above `embedding` table? We can include additional information such as author, genre, rating, the date it was written, …, and any information about the document beyond the text itself. We can define a schema and store the metadata in a structured way alongside the vector representation. 

#### Get Tam Nguyen’s stories in your inbox 

_Join Medium for free to get updates from this writer._ 

_Enter your email Subscribe_ 

_Remember me for faster sign in_ 

With the database metadata schema, we use LLM to construct a structured query from the question to filter the document chunks. At the same time, the question is also converted into its vector representation for the similarity 

search. This kind of hybrid retrieval approaches are likely to become more and more common when RAG becomes a more widely adopted strategy. 



<!-- Start of picture text -->
What's a highly rated Query: "film"<br>(above 8.5) science  — — — cue -- Filter: gt("rating”: 8.5)<br>fiction film? eq("genre™: "science fiction")<br>\ ' ae<br>fl ! ’<br>ebedding, model H -<br>i'-<br>_<br>|H<br>| Metadata' - ~ “ Hybrid.<br>Representationresent 7 L-— vere | Text Query<br><!-- End of picture text -->

### **_<u>Time-weighted retriever</u>_** 

In some cases, the information contained in the documents is only relevant if it is recent enough. In the context of a time-weighted retriever, the data is retrieved based on the hybrid score between semantic similarity and the age of the document. The algorithm for scoring it can be: 

```
semantic_similarity + (1.0 - decay_rate) ^ hours_passed
```

### **_<u>Other query constructions</u>_** 

<u>Text-to-SQL</u> 

- <u>Text-To-SQL+semantic</u> 

- <u>Text-to-Cypher</u> 



<!-- Start of picture text -->
Pipeline Datastore Data Types<br>Retrieved<br>P Documents<br>L+<br>Natural Text-to-SQL+semantic { ee Structured + unstructured il<br>language an<br>Text-to-Cypher rap)<br>Beabane<br>Relational<br>Text-to-SQLf= jf Mostly structured<br><!-- End of picture text -->

_Image by LangChain_ 

## **_6. Document selection optimization_** 

### **_<u>Re-ranking</u>_** 

After first-stage retrieval (lexical/keyword-based search or semantic/embedding-based search), doing re-ranking as a second stage to rank retrieved documents using relevance scores. 



<!-- Start of picture text -->
Query Vastly improved ordering and<br>abegulsiny approves relevance to query<br>Vv Vv<br>60000068 f a —— #1<br>6000066 Search<br>Rea >| Gemantic a ——— > Rerank >| 2 ==<br>I ETETETETEE) or Keyword) a ~<br>66500006 i ——$_— J no E==<br>Ast Stage 2nd Stage<br>Millions of documents Initial Search Results Improved Search Results<br>in a text archive<br><!-- End of picture text -->

_Image by Cohere_ 

### **_<u>Maximal Marginal Relevance (MMR)</u>_** 

Sometimes we retrieve more than we actually need, there can be similar documents capturing the same information. The MMR metric penalizes redundant information. 

The reranking is an iterative process where we measure the similarity of the vectors to the query and the similarity of the vectors to the vectors we have already re-ranked, end up with a vector similar to the query but dissimilar to the vectors we already reranked. 

## **_7._** **_<u>Context Optimization</u>_** 

Now that we have selected the correct documents to answer the question, we need to figure out how we will pass data as context for the LLM to answer the question. 



<!-- Start of picture text -->
‘Stuff<br>Final<br>| | Prompt i<br>{| Extractainal summary | ~ lem<br>Docs 7 | tom the documents ;<br>7 Fits in LLM<br>context window<br>S<_ Does not fit in LLM<br>*<_ contoxt window<br>ON, Map Reduce<br>“aBSS Final<br>at ‘ canninmimeieinemmecnneineieeas Summary<br>Ht ie ' {| Prompt :<br>bit || Ba apy [es eal) Corp | =P| | Extract<br>Ht | tpegroupof coco H 1 | em summaryfinal summaryast | =m :i<br><!-- End of picture text -->

_Image by LangChain_ 

- <u>Stuffing is the simplest method to pass data to the language model. It</u> concatenates the text of those documents and pass it to the prompt. 

- <u>MapReduce implements a multi-stage summarization. It is a technique</u> for summarizing large pieces of text by first summarizing smaller chunks of text and then combining those summaries into a single summary. Instead of summarization, we can also iterate through the documents to extract the information likely to answer the question. 

- <u>Refine method is an alternative method to deal with large document</u> summarization. It works by first running an initial prompt on a small chunk of data, generating some output. Then, for each subsequent document, the output from the previous document is passed in along with the new document, and the LLM is asked to refine the output based on the new document. 

- <u>Map-rerank strategy iterates through each document and tries to answer</u> the question along with a score on how well the question was answered. We can then pick the answer with the highest score. 

##### Search this file… 

|`1`||**stuff**|
|---|---|---|
|`2`|Pros|Only makes a single call to the LLM. When generating text, the LLM has access to all the data at once.|
|`3`|Cons|Most LLMs have a context length, and for large documents (or many documents) this will not work as it will result|
||||
|**llm-**|**summar**|**view raw**<br>**ization.csv**hosted with❤by**GitHub**|



## **_8._** **_<u>Multimodal RAG</u>_** 

When dealing with semi-structured or unstructured data e.g. tables, text, and images, we might need multimodal LLM and/or multimodal embeddings, below are some options: 



<!-- Start of picture text -->
Multi-Vector Retriever __ RetrieveOptionraw image1:<br>‘<br>t MuitimodaluM ||<br>Multimodal Embedding Hi @ . Answer<br>Table Summary, H = ‘<br>Option2:<br>Documents H =a] us |<br>—— H QD Answer<br>Saas<br>. Text Text Embedding BE3 [6 | Retrieve imageOption summary3: but pass<br>Taltmmey i ‘raw image to LLM forMutinodal synthesis |<br>= in| H: @QuM || answer<br><!-- End of picture text -->

_Image by LangChain_ 

1. Use multimodal embeddings (such as CLIP) to embed images and text together. Retrieve either using similarity search, but simply link to images in a docstore. Pass raw images and text chunks to a multimodal LLM for synthesis. 

2. Use a multimodal LLM (such as GPT4-V, LLaVA, or FUYU-8b) to produce text summaries from images. Embed and retrieve text summaries using a text embedding model. And, again, reference raw text chunks or tables from a docstore for answer synthesis by the LLM. Then exclude image from the docstore, instead pass image text summary to LLM or use a multi-modal LLM for synthesis, with raw image and raw table, text. 

## **_9._** **_<u>Agents</u>_** 

Last but not least, you may not only build the RAG app to answer questions from documents, we can have multiple tools to augment the LLM app, or <u>route question between multiple datastores. An agent uses the LLM to</u> choose a sequence of actions to take to solve a problem. 



<!-- Start of picture text -->
|I<br>e)--|=. (=)I<br>| |<br>Observation Action!<br>I<br>' —_ |<br>| I<br>‘---| Toot \«--/<br>ay<br><!-- End of picture text -->

The Agent can consist of some key components: 

- The Agent Core: This is the central component of the agent responsible for making decisions. It is powered by the LLM and a prompt that includes the agent’s personality, background context, and prompting strategies. 

- Tools and Toolkits: Tools are functionalities that the agent can access and utilize to perform specific tasks. Toolkits are collections of related tools that work together to accomplish specific objectives. There are two important design considerations around tools: giving the agent access to the right tools and describing the tools in a way that is most helpful to the agent. 

There are some types of agents we should first start with: 

- <u>ReAct</u> 

- <u>OpenAI functions</u> 

- <u>OpenAI assistants</u> 

## **_Conclusion_** 

I suggest to read all above methods and other <u>RAG Strategies from Open AI,</u> then pick the ones that are most relevant to your use case. You can also combine multiple approaches to get the best result. For example, the first architecture can be turned to a below one. 



<!-- Start of picture text -->
a Seay a6.—_ t=<br><!-- End of picture text -->

If you find this article useful, please give it a clap and share it with your friends. Also kindly checkout a <u>generative_ai repo that contains some</u> generative AI techniques and follow me in <u>LinkedIn.</u> 

Thanks for reading! 



<!-- Start of picture text -->
LLM + Generative Ai Tools + Rag + Mlops + NLP +<br><!-- End of picture text -->



### _Written by Tam Nguyen_ 

_92 followers · 29 following_ 



<!-- Start of picture text -->
Follow<br><!-- End of picture text -->

_Lead AI/ML Engineer specializing in Agentic AI, Multi-agent systems, A2A, MCP, RAG, OCR/IDP & LLMOps. Gym-loving dad_ 🏋️‍♂️ _building the autonomous future._ 

