## 结论

智能体应用同时继承了 LLM 与工具所带来的漏洞。攻击者可以滥用 AI 智能体、以非预期的方式使用工具，并提取敏感数据。要降低这些风险，必须采用纵深防御策略——既包含传统安全控制，也包含面向 AI 的防护措施，例如提示加固、输入校验、安全的工具集成与运行时监控。随着智能体应用持续演进，安全团队必须同步调整自己的防御手段。

我们建议安全团队采用 Palo Alto Networks Prisma AIRS，用来发现（Discover）、评估（Assess）并保护（Protect）企业范围内正在部署的 AI 智能体。如需事件响应支持，可联系 Unit 42 事件响应团队：

| 地区 | 联系电话 |
| --- | --- |
| 北美 | +1 (866) 486-4842 |
| 英国 | +44.20.3743.3660 |
| 欧洲 / 中东 | +31.20.299.3130 |
| 亚洲 | +65.6983.8730 |
| 日本 | +81.50.1790.0200 |
| 澳大利亚 | +61.2.4062.7950 |
| 印度 | 00080005045107 |

你也可以加入 Cyber Threat Alliance（网络威胁联盟），与成员共享威胁情报。

## 附加资源

- 股票咨询助手示例（GitHub 仓库）
- CrewAI：[官方文档](https://docs.crewai.com/)、[代码仓库](https://github.com/crewAIInc/crewAI)
- CrewAI 工具：[SerperDevTool](https://docs.crewai.com/tools/serperdevtool)、[ScrapeWebsiteTool](https://docs.crewai.com/tools/scrapewebsitetool)、[层级流程 Hierarchical Process](https://docs.crewai.com/how-to/hierarchical-process)
- AutoGen：[官方文档](https://microsoft.github.io/autogen/stable/)、[代码仓库](https://github.com/microsoft/autogen)
- Swarm：[官方文档](https://github.com/openai/swarm)
- Google Cloud：[虚拟机元数据](https://cloud.google.com/compute/docs/metadata/overview)
- OWASP：[LLM 应用十大风险](https://genai.owasp.org/llm-top-10/)
- OWASP：[Agentic AI 威胁与缓解措施](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
- OWASP：[面向 LLM 与 GenAI 应用的智能体安全](https://genai.owasp.org/)

### 标签

Agentic AI、AI 智能体、提示注入、工具滥用、数据外泄、云安全、LLM 安全、威胁研究

### 目录

- 引言与背景
- 智能体应用的威胁模型
- 攻击场景 1：提取智能体指令
- 攻击场景 2：提取智能体工具 Schema
- 攻击场景 3：获取对内部网络的未授权访问
- 攻击场景 4：通过挂载卷外泄敏感数据
- 攻击场景 5：通过元数据服务外泄服务账号访问令牌
- 攻击场景 6：利用 SQL 注入与 BOLA 访问未授权数据
- 攻击场景 7：通过间接提示注入外泄对话历史
- 保护与缓解
- 结论

### 相关文章

- Threat Brief：Axios 供应链攻击的广泛影响
- 面向 AI 智能体的 OWASP Top 10
- 云环境中的身份与权限滥用

### 相关恶意软件资源

- 威胁简报与恶意软件家族档案（详见 Unit 42 威胁研究中心的持续更新）
