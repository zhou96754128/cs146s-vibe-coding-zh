For every unique combination of needle type, haystack topic, and haystack structure, we test each model across:
 - 8 input lengths
- 11 needle positions
 
We evaluate each model across its maximum context window with temperature=0 unless that setting is incompatible (i.e. o3) or explicitly discouraged (i.e. Qwen’s “thinking mode”). For Qwen models, we apply the YaRN method [13] to extend from 32,768 to 131,072 tokens.

We include models in both standard and “thinking mode” where applicable.

We evaluate model outputs using an aligned GPT-4.1 judge, using our method outlined in the appendix.

We note some rare instances of a model refusing to attempt the task (69 out of 194,480 total LLM calls—0.035%). For example, Claude Opus 4 may sometimes have an empty output with stop_reason=”refusal”.

# Needle-Question Similarity#

In real-world applications, models are often expected to handle ambiguous tasks and identify relevant information without relying on exact lexical matches. For example, when an agent is given a task involving a large corpus to search through, users rarely specify precise keywords for relevant parts. Instead, the model must infer relevance.

We vary the similarity of our needle-question pairs, quantified by the cosine similarity of their embeddings. We find that as needle-question similarity decreases, model performance degrades more significantly with increasing input length. This reflects more realistic scenarios where exact question-answer matches are rare, and semantic ambiguity compounds the challenge of long input processing.

## Experiment#

We source our haystack content from two domains: Paul Graham essays (as in the original NIAH experiment), and arXiv papers. For each haystack topic (PG essays, arXiv), we first determine common themes to guide our question and needle writing.

We use clustering to identify the most common topics that appear for a given corpus:
 - Chunk documents into 1-3 sentence chunks
- Embed each chunk using text-embedding-3-large
- Use UMAP [14] for dimensionality reduction with the following parameters: n_neighbors=30, min_dist=0.05, n_components=50, random_state=42
- Use HDBSCAN [15] to create clusters with the following parameters: min_cluster_size=10, min_samples=15
- Get 20 representative chunks for the largest clusters using maximal marginal relevance (MMR)
- Manually examine the largest clusters to determine their themes and style
 
Using this method, we identify writing advice as a common topic for PG essays, often in anecdotal form. For arXiv papers, we identify information retrieval as a common topic, specifically re-ranking.

We write a corresponding question for each topic:
 

PG essays: "What was the best writing advice I got from my college classmate?"

arXiv papers: "Which low-latency reranker is preferred for scientific domains?"

 Questions for Paul Graham essays & arXiv papers 
Before writing our needles, we verify that answers to these questions do not exist in the haystack content:
 - We store our previously computed haystack chunk embeddings in a vector database.
- Query top-10 results from that vector database with our question embedding.
- Manually examine these results to verify that they do not answer the given question.
 
This sets up a fair testing environment as it ensures that alternative answers do not exist, and any incorrect answers are due to model hallucinations.

For each question, we write 8 needles that each belong to the large cluster which we verify using approximate predictions. Needles that belong to the writing/retrieval cluster with >0.9 probability are considered to topically blend into the haystack. We manually write these needles to avoid data contamination.

For the 8 needles, we also vary the level of ambiguity, quantified through the following method:
 - Using an embedding model, we compute embeddings for needle and question and their cosine similarity.
- Repeat across five embedding models (text-embedding-3-small, text-embedding-3-large, jina-embeddings-v3, voyage-3-large, and all-MiniLM-L6-v2).
 
For the PG essays topic, our needles range from 0.445-0.775 needle-question similarity with NIAH: Needle-Question Similarity (thinking/non-thinking modes of the same model are treated separately) - arXiv haystack/arXiv needles 
 High Performance: upper 33% performance 
 Blue: high-similarity needles (upper 50% similarity) 
 Red: low-similarity needles (lower 50% similarity) 
At short input lengths, the models perform well even on low-similarity pairs. We see this most clearly in the high/medium-performance models, demonstrating that these models are capable of succeeding at this task for all needle-question pairs.

The observed performance degradation at longer input lengths is not due to the intrinsic difficulty of the needle-question pairing. By holding the needle-question pair fixed and varying only the amount of irrelevant content, we isolate input size as the primary factor in performance decline.

We also examine whether needle position influences performance. Testing across 11 needle positions, we find no notable variation in performance for this specific NIAH task.

# Impact of Distractors#

It has already been established with older models that distractors degrade model performance and have non-uniform impact. Newer models are claimed to reliably handle any distractor, but does this hold true as input length increases?

Our experiments reveal that the impact of distractors and their non-uniformity amplifies as input length grows across models, including the latest state-of-the-art models. We also observe distinct behaviors across model families in how they deal with ambiguity.

## Experiment#

From each haystack topic (PG essays and arXiv papers), we take a needle with high needle-question similarity (second highest out of eight), and manually write 4 distractors:
 

Question: "What was the best writing advice I got from my college classmate?"

Needle: "I think the best writing tip I received from my college classmate was to write every week."

Distractors:
 - "The best writing tip I received from my college professor was to write everyday."
- "The worst writing advice I got from my college classmate was to write each essay in five different styles."
- "The best writing advice I got from my classmate was to write each essay in three different styles, this was back in high school."
- "I thought the best writing advice I got from my college classmate was to write each essay in four different styles, but not anymore."
 

 Distractors for Paul Graham Essay Topic & Needle with High Needle-Question Similarity 
Instead of testing all eight needles with distractors, we use one needle with high needle-question similarity to create a condition in which the needle should be relatively easy to identify. We see from previous results that models generally perform well on this needle across input lengths due to high needle-question similarity, which allows us to better isolate and measure the impact of distractors alone.

We run three test conditions:
 - No distractors (baseline): Needle only
- Single distractor: Needle + one distractor (randomly positioned)
- Multiple distractors: Needle + all four distractors, randomly positioned throughout the haystack
 Impact of Distractors - Three Conditions 
## Results#

Even a single distractor reduces performance relative to the baseline (needle only), and adding four distractors compounds this degradation further.
 Impact of Distractors: Performance by Number of Distractors - arXiv haystack/PG essay needles 
We are also able to see that distractors do not have uniform impact. For example, in our arXiv haystack and PG essay needle combination, we can see that distractor 3 (red) causes greater performance decline relative to the other distractors.
 Impact of Distractors: Performance by Individual Distractors - arXiv haystack/PG essay needles 
To further investigate this non-uniform impact, we analyze the failed attempts of various models in the 4-distractor condition. For the arXiv haystack and PG essay needle combination, we see that distractors 2 and 3 appear most frequently in hallucinated responses across models.
 Impact of Distractors: Failure Analysis - arXiv haystack/PG essay needles 
These failures also reveal model-specific differences in handling ambiguity. Claude models consistently exhibit the lowest hallucination rates. Specifically, Claude Sonnet 4 and Opus 4 are particularly conservative and tend to abstain when uncertain, explicitly stating that no answer can be found. In contrast, GPT models show the highest rates of hallucination, often generating confident but incorrect responses when distractors are present.
 
# Needle-Haystack Similarity#

In long-context tasks, irrelevant context is often treated as a neutral placeholder to scale up input length. It’s typically assumed that the content of this irrelevant context doesn't matter, as long as it doesn’t directly interfere with the task.

However, a natural question arises: does the needle-haystack similarity influence task difficulty at all? Intuitively, if the needle blends in with the content of the haystack, the model may have greater difficulty in extracting the needle.

Our findings reveal that needle-haystack similarity has a non-uniform effect on model performance.

## Experiment#

Using the needles from our needle-question similarity experiment, we set up our experiment to test the impact of needle-haystack similarity.

We measure needle-haystack similarity by embedding the haystack and retrieving the top five most similar chunks for each needle, then averaging their cosine similarity scores. This process is repeated across five different embedding models for robustness.

In the PG essay haystack, PG essay needles have an average needle-haystack similarity score of 0.529 with a variation of 0.101, while arXiv needles average 0.368 needle-haystack similarity with a variation of 0.111. Conversely, in the arXiv haystack, arXiv needles average 0.654 needle-haystack similarity with a variation of 0.0858, whereas PG-essay needles score lower at 0.394 needle-haystack similarity with a variation of 0.105.

On each haystack, we test semantically similar needles against unrelated needles. For instance, we place both PG essay and arXiv needles within a Paul Graham essay haystack to compare the two conditions:
 Needle-Haystack Similarity: Experimental Setup 
## Results#

We test both PG essay and arXiv needles in two haystack types: Paul Graham essays and arXiv papers. In the Paul Graham essay haystack, arXiv needles perform significantly better relative to the PG essay needles; in other words, models perform better when the needle does not semantically blend in with its haystack. In the arXiv haystack, however, we observe only minimal performance differences between our arXiv and PG essay needles.
 Needle-Haystack Similarity Results 
Testing across only two topics is insufficient to draw a generalizable conclusion that higher needle-haystack similarity degrades model performance on this task. This does highlight, however, the non-uniform nature of long-context processing. Even when task structure and needle-question similarity are held constant, changing the semantic similarity between the needle and the haystack can influence results. This points to an underexplored area in long-context benchmarks and a meaningful direction for future research.

# Haystack Structure#

Aside from needle-haystack similarity, we also consider the structural pattern of the haystack.