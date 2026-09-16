# 局限性与未来工作

我们的实验表明，LLM 在不同上下文长度下表现并不一致，即便是面对简单任务也是如此。然而，本评测并未穷尽真实世界的用例。在实践中，长上下文应用往往要复杂得多，需要综合或多步推理。基于我们的发现，我们预期在这些条件下性能下降会更加严重。

我们的结果对未来长上下文评测工作也有启示。一个常见的局限——在以往的长上下文基准工作中也被指出过——是倾向于把输入长度与任务难度混为一谈，因为更长的输入往往会引入更复杂的推理。我们的实验聚焦于把输入长度作为变量加以隔离，并保持任务难度恒定。一个重要的未来工作方向是厘清：模型性能下降中，有多少源于任务本身的固有难度，又有多少源于其有效处理长上下文的能力。

我们也没有解释这种性能下降背后的机制。我们的观察表明，上下文的某些结构属性——例如相关信息的位置或重复方式——会影响模型行为，但我们对为何如此并没有确定答案。要研究这些效应，需要对机制可解释性做更深入的探究，这超出了本报告的范围。

更广泛地说，我们的发现指向了上下文工程（context engineering）的重要性：对模型上下文窗口的精心构造与管理。信息在模型上下文中呈现的位置与方式会强烈影响任务表现，这使上下文工程成为优化模型性能的一个有意义的未来工作方向。

# 结论

通过实验，我们证明 LLM 在不同输入长度下并不能保持稳定表现。即便是在非词汇检索或文本复现这样简单的任务上，我们也看到随着输入长度增长，性能的不均匀性不断增加。

我们的结果凸显了在现有基准之外进行更严格长上下文评测的必要性，也凸显了上下文工程的重要性。相关信息是否出现在模型的上下文中并非全部关键；更关键的是这些信息是如何被呈现的。我们证明，即便是能力最强的模型也对此敏感，因此有效的上下文工程对于可靠表现至关重要。

# 脚注


[1]（2025 年 7 月 16 日）由 Kiran Vodrahalli（Google Deepmind）补充 Latent List 相关洞见并作出澄清


[2] 示例的原始来源：https://arxiv.org/pdf/2410.10813

# 参考文献


[1] Kamradt, G. (2023). Needle In A Haystack - Pressure Testing LLMs [GitHub Repository]. Link


[2] Wu, D., Wang, H., Yu, W., Zhang, Y., Chang, K.-W., and Yu, D. (2025). LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory. arXiv preprint arXiv:2410.10813. Link


[3] Gemini Team, Georgiev, P., Lei, V. I., Burnell, R., Bai, L., Gulati, A., Tanzer, G., Vincent, D., Pan, Z., Wang, S., et al. (2024). Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. arXiv preprint arXiv:2403.05530. Link


[4] OpenAI, Kumar, A., Yu, J., Hallman, J., Pokrass, M., Goucher, A., Ganesh, A., Cheng, B., McKinzie, B., Zhang, B., Koch, C., et al. (2025). Introducing GPT-4.1 in the API. Link


[5] Meta AI, (2025). The Llama 4 herd: The beginning of a new era of natively multimodal AI innovation. Link


[6] Modarressi, A., Deilamsalehy, H., Dernoncourt, F., Bui, T., Rossi, R. A., Yoon, S., and Schütze, H. (2025). NoLiMa: Long-Context Evaluation Beyond Literal Matching. arXiv preprint arXiv:2502.05167. Link


[7] Fu, H. Y., Shrivastava, A., Moore, J., West, P., Tan, C., and Holtzman, A. (2025). AbsenceBench: Language Models Can't Tell What's Missing. arXiv preprint arXiv:2506.11440. Link


[8] Vodrahalli, K., Ontanon, S., Tripuraneni, N., Xu, K., Jain, S., Shivanna, R., Hui, J., Dikkala, N., Kazemi, M., Fatemi, B., et al. (2024). Michelangelo: Long Context Evaluations Beyond Haystacks via Latent Structure Queries. arXiv preprint arXiv:2409.12640. Link


[9] openai. (2025). mrcr [Dataset]. Hugging Face. Link


[10] openai. (2025). graphwalks [Dataset]. Hugging Face. Link


[11] Shi, F., Chen, X., Misra, K., Scales, N., Dohan, D., Chi, E., Schärli, N., and Zhou, D. (2023). Large Language Models Can Be Easily Distracted by Irrelevant Context. arXiv preprint arXiv:2302.00093. Link


[12] jamescalam. (2024). ai-arxiv2 [Dataset]. Hugging Face. Link


[13] Peng, B., Quesnelle, J., Fan, H., and Shippole, E. (2023). YaRN: Efficient Context Window Extension of Large Language Models. arXiv preprint arXiv:2309.00071. Link


[14] McInnes, L., Healy, J., and Melville, J. (2020). UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction. arXiv preprint arXiv:1802.03426. Link


[15] Campello, R. J. G. B., Moulavi, D., and Sander, J. (2013). Density-Based Clustering Based on Hierarchical Density Estimates. In Pei, J., Tseng, V. S., Cao, L., Motoda, H., and Xu, G. (Eds.), Advances in Knowledge Discovery and Data Mining (PAKDD 2013), Lecture Notes in Computer Science, vol 7819. Springer, Berlin, Heidelberg. Link

# 附录

清洗后的 LongMemEval 数据集以及所用到的针/干扰项可在此处下载。

## LLM 评判器对齐：
