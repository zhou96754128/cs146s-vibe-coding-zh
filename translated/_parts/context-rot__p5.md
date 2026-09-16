我们使用 LLM 评判器（LLM judge）来评估 NIAH 与 LongMemEval 实验的输出。这些评判器通过以下流程校准到人类判断：
 - 对一部分模型输出进行人工标注，标为错误/正确（NIAH 约 500 条输出，LongMemEval 约 600 条输出）
- 使用 GPT-4.1 对同一批模型输出进行错误/正确标注
- 通过统计人类判断与模型判断相一致的比例，计算得到对齐分数
- 根据对不一致案例的人工检查来迭代提示词
- 重复第 2-4 步，直到对齐分数 > 0.99


## 受测模型

由于上下文窗口或 thinking_budget 的限制，并非所有 18 个模型都出现在每个实验中。

### Anthropic
 - Claude Opus 4
- Claude Sonnet 4
- Claude Sonnet 3.7
- Claude Sonnet 3.5
- Claude Haiku 3.5


### OpenAI
 - o3
- GPT-4.1
- GPT-4.1 mini
- GPT-4.1 nano
- GPT-4o
- GPT-4 Turbo
- GPT-3.5 Turbo


### Google
 - Gemini 2.5 Pro
- Gemini 2.5 Flash
- Gemini 2.0 Flash


### Alibaba
 - Qwen3-235B-A22B
- Qwen3-32B
- Qwen3-8B


## 使用的嵌入模型
 - text-embedding-3-small
- text-embedding-3-large
- jina-embeddings-v3（input_type='text-matching'）
- voyage-3-large（input_type=None）
- all-MiniLM-L6-v2


## 针与问题的相似度

注：同一模型的思考/非思考模式被分开对待
 针-问题相似度 —— arXiv 草堆/PG 文章针 针-问题相似度 —— PG 文章草堆/PG 文章针 针-问题相似度 —— PG 文章草堆/arXiv 针
如我们在「针-草堆相似度」结果中所述，我们注意到这一处例外：模型在该组合下的表现异常地好，远超其他针-草堆组合。单看这一处，可能会以为这些高性能模型的表现是均匀的。然而，这种均匀性并未在其余实验中成立。

## 干扰项的影响
 干扰项的影响：按干扰项数量统计的表现 —— arXiv 草堆/arXiv 针 干扰项的影响：按单个干扰项统计的表现 —— arXiv 草堆/arXiv 针 干扰项的影响：按干扰项数量统计的表现 —— PG 文章草堆/PG 文章针 干扰项的影响：按单个干扰项统计的表现 —— PG 文章草堆/PG 文章针 干扰项的影响：按干扰项数量统计的表现 —— PG 文章草堆/arXiv 针 干扰项的影响：按单个干扰项统计的表现 —— PG 文章草堆/arXiv 针 干扰项的影响：失败分析 —— arXiv 草堆/arXiv 针 干扰项的影响：失败分析 —— PG 文章草堆/PG 文章针 干扰项的影响：失败分析 —— PG 文章草堆/arXiv 针
## 重复词
 重复词：位置准确率 —— GPT 系列 重复词：位置准确率 —— Gemini 系列 重复词：位置准确率 —— Qwen 系列 重复词：词数差 —— GPT 系列 重复词：词数差 —— Gemini 系列 重复词：词数差 —— Qwen 系列 © 2026
### 产品
 数据库 同步 企业版 包 搜索 MCP 文档 状态 联系
### 关注
 GitHub X YouTube
### 公司
 关于 更新日志 招聘
### 法律
 隐私 条款 安全
