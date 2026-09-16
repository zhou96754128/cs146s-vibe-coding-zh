If the haystack is composed of coherent essays, a randomly inserted needle may disrupt the logical flow of ideas, making it more noticeable. In contrast, in a shuffled haystack of randomly ordered sentences, the needle may blend in more easily since the overall context lacks structure. This follows the assumption that models are sensitive to the logical flow of context—processing it in a structured, order-sensitive manner.

Surprisingly, we find that structural coherence consistently hurts model performance.

Although it seems counterintuitive, models perform worse when the haystack preserves a logical flow of ideas. Shuffling the haystack and removing local coherence consistently improves performance.

## Experiment#

To assess the impact of haystack structure, we create two variants:
 - Original: preserves the natural flow of ideas within each excerpt
- Shuffled: sentences are randomly reordered throughout the haystack to maintain the same overall topic but without logical continuity
 Haystack Structure: Sample Experimental Setup 
## Results#

Across all 18 models and needle-haystack configurations, we observe a consistent pattern that models perform better on shuffled haystacks than on logically structured ones.
 Haystack Structure: Averaged Performance Across 18 Models for Original vs Shuffled Haystacks 
These results may have some implications for the model’s internal processing: structural patterns of inputs could influence how the attention mechanism is applied, particularly as input length increases.

While out of scope for this report, this points to a potential direction for interpretability research in how attention is influenced by input structure. Understanding these structural influences that arise with increased input length could help explain these long context failure patterns.

# LongMemEval#

To evaluate these models in a more realistic setting, we use LongMemEval, a long-context benchmark for conversational question-answering.

Using long inputs for chat assistants is a common approach for maintaining relevant history for subsequent chats. To incorporate “memory” into a chat assistant, a naive approach would be to include the full chat history into the prompt for following chats. This requires the model to perform two tasks, typically performed in one call: find relevant parts of the conversation history (retrieval), then synthesize them in a way that is useful to an incoming query (reasoning).

In an ideal case, the model would be given only the relevant parts so it can focus solely on reasoning. Adding irrelevant context adds the additional step of identifying what is relevant, forcing the model to perform two tasks simultaneously.

We systematically test the effect of adding this additional step with increased input length through two conditions:
 - Focused input, containing only the relevant parts and so the model just has to do simple reasoning.
- Full input, which utilizes the full 113k token LongMemEval input that includes irrelevant context. In this case, the model has to perform retrieval across the long context in addition to reasoning.
 
We verify that the models are highly capable of succeeding on the focused inputs, then observe consistent performance degradation with the full inputs. This performance drop suggests that adding irrelevant context, and thereby adding an additional step of retrieval, significantly impacts a model’s ability to maintain reliable performance.

## Experiment#

Given a chat history between a user and assistant, the model’s task is to answer a question relating to part of that chat history.
 LongMemEval - Examples by Question Type [[2](#longmemeval-source)] 
We use LongMemEval_s and filter for tasks that fall under the knowledge update, temporal reasoning, and multi-session categories. We then manually clean this dataset as some questions are too ambiguous and/or can not be answered, filtering out 38 prompts to end up with 306 total prompts. These prompts average out to ~113k tokens.

These long prompts mostly consist of content irrelevant to the question, and sometimes distractors which may seem relevant to the question. We compare performance of the models on these long prompts to a focused version, which only contains the relevant parts to answer the question.

Focused prompts average to ~300 tokens, which are derived from the originally labeled dataset and manual adjustments.

Model outputs were judged using an aligned LLM judge (GPT-4.1 with >99% alignment to human judgment).

## Results#

Across all models, we see significantly higher performance on focused prompts compared to full prompts.
 LongMemEval Results - Claude Family 
The Claude models exhibit the most pronounced gap between focused and full prompt performance. This discrepancy is largely driven by abstentions that arise with ambiguity, leading to model uncertainty, similar to this model family’s behavior with distractors in NIAH. This behavior is most evident in Claude Opus 4 and Sonnet 4, which appear to be particularly conservative under ambiguity, leading to lower performance on full prompts relative to that of the older Claude models.
 

Question: How many days passed between the day I attended the gardening workshop and the day I planted the tomato saplings?

Correct Answer: 6 days. 7 days (including the last day) is also acceptable.

Model Output: I cannot determine the number of days between the gardening workshop and planting the tomato saplings becuase the specific dates for these events are not provided in the chat history.

 LongMemEval - Claude Sonnet 4 (non-thinking) on full prompt containing the dates 
The trend of stronger performance on focused prompts holds across the GPT, Gemini, and Qwen model families as well. For models that support thinking modes, we see notable gains on both focused and full prompts when enabled. However, we still see a performance gap between the two input lengths even with full reasoning capabilities on the latest models.
 LongMemEval Results - GPT Family LongMemEval Results - Gemini Family LongMemEval Results - Qwen Family 
We also observe patterns among specific question types. In non-thinking mode, models generally perform best on knowledge-update, followed by multi-session, then temporal reasoning—for both focused and full prompts. However, when thinking is enabled, this ranking shifts to: knowledge update, temporal-reasoning, then multi-session.
 LongMemEval Results by Question Type - Claude Opus 4 
# Repeated Words#

Our previous experiments explore how input length alone affects model performance. But what happens when output length scales with input? Since these models are autoregressive, a model’s output also belongs to its input; each token is generated conditionally on the input and generated tokens up to that point.

Consider a basic program that repeats a string n times—it produces the same output every time. For a task this trivial, we’d expect these models to be just as reliable, and we’d like to treat them as computing systems.

However, our findings show that even for these straightforward tasks, model performance becomes non-uniform as context length, encompassing both input and output lengths, grows.

## Experiment#

We design a controlled task in which the model must replicate a sequence of repeated words, with a single unique word inserted at a specific position. The prompt explicitly instructs the model to reproduce the input text exactly.

One example prompt is:
 

Simply replicate the following text, output the exact same text: apple apple apple apple apples apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple

 Repeated Words - Sample Prompt Containing 'apple' as the repeated word, and 'apples' as the unique word 
For a given word combination, we create 1090 variations of context lengths and unique word indices:
 - Number of words: 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000
- Index:Every possible position for num_words 
We perform this task for the following word combinations:
 - Common word: “apple” | unique word: “apples”
- Common word: “apples” | unique word: “apple”
- Common word: “golden” | unique word: “Golden”
- Common word: “orange” | unique word: “run”
- Common word: “orange” | unique word: “San Francisco”
- Common word: “San Francisco” | unique word: “sf”
- Common word: “Golden Gate Bridge” | unique word: “Golden Gate Park”
 
Note: “San Francisco” = 1 word, “Golden Gate Bridge/Park” = 1 word

Model configurations:
 - max_output_tokens = input_tokens *2 (up to model’s maximum output token limit, which is typically lower for older models)
- temperature = 0
- thinking = max(0, minimum_thinking_budget)
 
We account for reasoning models by either setting their thinking budgets to 0 or the minimum value, such as 128 tokens for Gemini 2.5 Pro. We exclude OpenAI’s o3 as it does not support token-based thinking budgets and cannot be configured with a fixed output length, which is essential for maintaining consistency across evaluations.

Scores are calculated by normalized Levenshtein distance.

We encounter cases of models not attempting the task, which we determine by:
 - Empty outputs with a stop reason (i.e. finish_reason='content_filter’ for GPT-3.5 turbo)
- Non-empty outputs, but with invalid outputs:
- Pure observations with no attempt:
 

I notice there's a discrepancy in the text. The word "apples" appears once in the original text (instead of "apple"), located in what appears to be around line 89 or 90 of the text block. Since you asked me to replicate the exact same text, I should point out this difference. Would you like me to:
 - Replicate it exactly as shown (with the one instance of "apples")
- Correct it to "apple" to match the pattern
- Simply proceed with replicating it exactly as is Please let me know how you'd like me to proceed.
 

 Repeated Words - Claude Opus 4 output - Refusals to answer:
 

I’m sorry, but I can’t help with that

 Repeated Words - GPT-4.1 output - Random outputs:
 

-\n-\n--\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-...

 Repeated Words - Gemini 2.5 Pro output 
We exclude such cases, and separately note the percentage of refusals and common patterns in our results. We only include cases in which the task was attempted, including cases with starting phrases such as:
 

I notice there's a discrepancy in the text. At one point, "apple" changes to "apples" (with an 's'). I'll replicate the text exactly as provided:

apple apple apple apple apple apple apple apple apple...

 Repeated Words - Claude Opus 4 output 
With these instances, we use the same scoring process to slightly penalize the model for not following exact instructions.

We exclude GPT-3.5 turbo entirely since the model refused to generate an output for 60.29% of tasks due to finish_reason='content_filter’.

We analyze outputs along several dimensions:
 - Normalized Levenshtein distance
- Presence and position of unique word
Correct: Unique word is present and appears at the correct index
- Incorrect position: Unique word appears, but at the wrong index
 - Word count difference (number of words in input - number of words generated)
 
## Results#

As context length increases, performance consistently degrades across all models. In this experiment, input length is directly proportional to output length, unlike our previous tests in which output length remained relatively fixed at a short length. This setting allows us to assess the models’ ability to reliably reproduce long sequences.

We also observe patterns where models do not attempt the task, which appears across all model families.
 Repeated Words - Claude Family 
We observe that Sonnet 3.5 (red) outperforms the newer Claude models up to its maximum output token count of 8192. Opus 4 (blue), while exhibiting the slowest degradation rate, is also the only model in this family to refuse the task (2.89% of attempts).