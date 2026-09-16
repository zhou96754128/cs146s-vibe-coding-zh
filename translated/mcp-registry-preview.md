# MCP 注册表预览（MCP Registry Preview）

今天，我们正式发布模型上下文协议（Model Context Protocol，MCP）注册表（Registry）——一个面向公开可用 MCP 服务器的开放目录与 API，旨在提升服务器的可发现性与易用性。通过标准化服务器的分发与发现方式，我们既扩大了它们的触达范围，也让客户端能更轻松地完成接入。

MCP 注册表现已进入预览（preview）阶段。开始使用：

- 添加你的服务器：请参阅《将服务器添加到 MCP 注册表》指南（面向服务器维护者）
- 获取服务器数据：请参阅《访问 MCP 注册表数据》指南（面向客户端维护者）

# MCP 服务器的单一事实来源（Single Source of Truth）

2025 年 3 月，我们曾表示希望为 MCP 生态构建一个中心化注册表。今天，我们正式宣布：已上线 `https://registry.modelcontextprotocol.io` 作为官方 MCP 注册表。作为 MCP 项目的一部分，MCP 注册表以及一份上级 OpenAPI 规范均为开源——任何人都可以据此构建一个兼容的子注册表（sub-registry）。

我们的目标是标准化服务器的分发与发现方式，提供一个可供子注册表在其之上构建的权威单一事实来源。反过来，这将扩大服务器的触达范围，并帮助客户端更轻松地在整个 MCP 生态中找到服务器。

## 公共与私有子注册表

在构建中心化注册表时，对我们而言很重要的一点是：不要取代社区与各公司已经建立起来的现有注册表。MCP 注册表作为公开可用 MCP 服务器的权威单一事实来源，组织可以基于自定义标准选择创建子注册表。例如：

公共子注册表——比如与各个 MCP 客户端绑定的、带有主观倾向的「MCP 市场（marketplace）」——可以自由地扩充和增强它们从上游 MCP 注册表摄取的数据。每一种 MCP 终端用户角色都有不同的需求，MCP 客户端市场有责任以各自倾向的方式恰当地服务好它们的终端用户。

私有子注册表将存在于那些对隐私与安全有严格要求的组织内部，但 MCP 注册表为这些组织提供了一个可以构建其上的单一上游数据源。至少，我们希望与这些私有实现共享 API 模式（schema），从而使相关的 SDK 与工具能够在整个生态中共享。

无论哪种情况，MCP 注册表都是起点——它是 MCP 服务器维护者发布和维护其自我申报信息的集中位置，供下游消费者加工处理后交付给它们的终端用户。

## 社区驱动的审核机制

MCP 注册表是 MCP 官方的项目，由注册表工作组维护，并采用宽松的开源许可证。社区成员可以提交 issue 来标记违反 MCP 审核指南的服务器——例如包含垃圾内容、恶意代码，或冒充合法服务的条目。注册表维护者随后可将这些条目加入黑名单（denylist），并追溯性地将其从公开访问中移除。

# 开始使用

开始使用：

- 添加你的服务器：请参阅《将服务器添加到 MCP 注册表》指南（面向服务器维护者）
- 获取服务器数据：请参阅《访问 MCP 注册表数据》指南（面向客户端维护者）

本次 MCP 注册表预览旨在帮助我们在全面开放（general availability，GA）之前改进用户体验，不提供数据持久性保证或其他担保。我们建议 MCP 的采用者密切关注其发展，因为在注册表全面开放之前可能会发生破坏性变更（breaking change）。

随着我们继续开发注册表，欢迎在 `modelcontextprotocol/registry` GitHub 仓库上提供反馈与贡献：讨论（Discussion）、问题（Issue）和拉取请求（Pull Request）都欢迎。

# 感谢 MCP 社区

MCP 注册表从一开始就是一项协作成果，我们对广大开发者社区的热情与支持深表感激。

2025 年 2 月，它作为一个草根项目起步：当时 MCP 的创建者 David Soria Parra 和 Justin Spahr-Summers 邀请 PulseMCP 与 Goose 团队协助构建一个中心化的社区注册表。来自 PulseMCP 的注册表维护者 Tadas Antanavicius 与来自 Block 的 Alex Hancock 合作，牵头完成了最初的开发工作。随后，注册表维护者、GitHub 的 MCP 负责人 Toby Padilla 加入，再后来，来自 Anthropic 的 Adam Jones 也加入成为注册表维护者，推动项目走向今天的发布。MCP 注册表开发的首次公告中列出了来自至少 9 家不同公司的 16 位贡献者。

还有许多人做出了关键贡献，让这个项目得以面世：来自 Stacklok 的 Radoslav Dimitrov、来自 GitHub 的 Avinash Sridhar、来自 VS Code 的 Connor Peet、来自 NuGet 的 Joel Verhagen、来自 Last9 的 Preeti Dewani、来自 Microsoft 的 Avish Porwal、Jonathan Hefner，以及众多提供代码评审与开发支持的 Anthropic 和 GitHub 员工。我们同样感谢注册表贡献者名单上的每一位，以及所有参与讨论与 issue 的人。

我们深深感谢每一位投资于这项基础性开源基础设施的人。正是靠着大家的努力，我们得以帮助全世界的开发者与组织构建更可靠、更具上下文感知能力的 AI 应用。谨代表 MCP 社区，向大家致谢。

---

> 来源：`https://registry.modelcontextprotocol.io` 官方公告页面（MCP Registry Preview）。
