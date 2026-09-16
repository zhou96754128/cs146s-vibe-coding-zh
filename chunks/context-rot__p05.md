We employ LLM judges to evaluate outputs for our NIAH and LongMemEval experiments. These judges are calibrated to human judgment through the following process:
 - A subset of model outputs are manually labeled as incorrect/correct (~500 outputs for NIAH, ~600 outputs for LongMemEval)
- GPT-4.1 is used to label the same subset of model outputs as incorrect/correct.
- An alignment score is calculated by measuring the proportion of human-model aligned judgements.
- The prompt is iterated on based on manual inspection of misalignments.
- Steps 2-4 are repeated until an alignment score > 0.99 is achieved.
 
## Models Tested#

Not all 18 models are included in each experiement due to context window or thinking_budget constraints.

### Anthropic#
 - Claude Opus 4
- Claude Sonnet 4
- Claude Sonnet 3.7
- Claude Sonnet 3.5
- Claude Haiku 3.5
 
### OpenAI#
 - o3
- GPT-4.1
- GPT-4.1 mini
- GPT-4.1 nano
- GPT-4o
- GPT-4 Turbo
- GPT-3.5 Turbo
 
### Google#
 - Gemini 2.5 Pro
- Gemini 2.5 Flash
- Gemini 2.0 Flash
 
### Alibaba#
 - Qwen3-235B-A22B
- Qwen3-32B
- Qwen3-8B
 
## Embedding Models Used#
 - text-embedding-3-small
- text-embedding-3-large
- jina-embeddings-v3 (input_type='text-matching')
- voyage-3-large (input_type=None)
- all-MiniLM-L6-v2
 
## Needle-Question Similarity#

Note: thinking/non-thinking modes of the same model are treated separately
 Needle-Question Similarity - arXiv haystack/PG essay needles Needle-Question Similarity - PG essay haystack/PG essay needles Needle-Question Similarity - PG essay haystack/arXiv needles 
As mentioned in our Needle-Haystack Similarity results, we note this one occurance in which models perform exceptionally well compared to the other needle-haystack combinations. On its own, it may seem that the high performance models have uniform performance. However, such uniformity for these models does not hold across the rest of the experiments.

## Impact of Distractors#
 Impact of Distractors: Performance by Number of Distractors - arXiv haystack/arXiv needles Impact of Distractors: Performance by Individual Distractors - arXiv haystack/arXiv needles Impact of Distractors: Performance by Number of Distractors - PG essay haystack/PG essay needles Impact of Distractors: Performance by Individual Distractors - PG essay haystack/PG essay needles Impact of Distractors: Performance by Number of Distractors - PG essay haystack/arXiv needles Impact of Distractors: Performance by Individual Distractors - PG essay haystack/arXiv needles Impact of Distractors: Failure Analysis - arXiv haystack/arXiv needles Impact of Distractors: Failure Analysis - PG essay haystack/PG essay needles Impact of Distractors: Failure Analysis - PG essay haystack/arXiv needles 
## Repeated Words#
 Repeated Words: Position Accuracy - GPT Family Repeated Words: Position Accuracy - Gemini Family Repeated Words: Position Accuracy - Qwen Family Repeated Words: Word Count Difference - GPT Family Repeated Words: Word Count Difference - Gemini Family Repeated Words: Word Count Difference - Qwen Family © 2026 
### Product
 Database Sync Enterprise Package Search MCP Docs Status Contact 
### Follow
 GitHub X YouTube 
### Company
 About Changelog Careers 
### Legal
 Privacy Terms Security