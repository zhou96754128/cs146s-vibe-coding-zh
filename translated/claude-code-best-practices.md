# Claude Code 概览（Claude Code Overview）

> 来源：Anthropic《Claude Code 文档 · 入门篇 · 概览（Getting started / Overview）》

Claude Code 是一个由 AI 驱动的编程助手，帮助你构建功能、修复 bug 并自动化开发任务。它能理解你的整个代码库，并跨多个文件和工具协作以完成任务。

## 开始使用

选择你的环境开始使用。大多数使用场景都需要 Claude 订阅或 Anthropic Console 账户。终端 CLI 和 VS Code 也支持第三方提供商。

### 终端（Terminal）

面向在终端中直接使用 Claude Code 的全功能 CLI。你可以在命令行中编辑文件、运行命令并管理整个项目。要安装 Claude Code，可使用以下任一方式：原生安装（推荐）、Homebrew、WinGet。

macOS、Linux、WSL：

```
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell：

```
irm https://claude.ai/install.ps1 | iex
```

Windows CMD：

```
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

如果你看到 `The token '&&' is not a valid statement separator`，说明你正处在 PowerShell 而非 CMD 中，请改用上面的 PowerShell 命令（在 PowerShell 中提示符显示为 `PS C:\`）。Windows 需要先安装 Git for Windows（如尚未安装，请先安装）。原生安装会在后台自动更新，让你始终保持最新版本。

```
brew install --cask claude-code
```

Homebrew 安装不会自动更新，请定期运行 `brew upgrade claude-code` 以获取最新功能和安全修复。

```
winget install Anthropic.ClaudeCode
```

WinGet 安装不会自动更新，请定期运行 `winget upgrade Anthropic.ClaudeCode` 以获取最新功能和安全修复。

然后在任意项目中启动 Claude Code：

```
cd your-project
claude
```

首次使用时会被提示登录。就这样！继续阅读「快速入门 →」。如需更多安装选项、手动更新或卸载说明，请参阅「高级安装」；如遇问题，请访问「故障排查」。

### VS Code

VS Code 扩展可直接在你的编辑器内提供行内 diff、@ 提及、计划审阅和对话历史。

可在扩展视图（Mac 为 Cmd+Shift+X，Windows/Linux 为 Ctrl+Shift+X）中搜索「Claude Code」来安装。安装后，打开命令面板（Cmd+Shift+P / Ctrl+Shift+P），输入「Claude Code」，选择「Open in New Tab」即可。

### 桌面应用（Desktop app）

一个可在 IDE 或终端之外运行 Claude Code 的独立应用。你可以可视化地审阅 diff、并排运行多个会话、安排定期任务，并启动云端会话。

安装后，启动 Claude、登录，然后点击 Code 标签即可开始编程。需要付费订阅。

### 网页（Web）

无需本地设置，直接在浏览器中运行 Claude Code。可以启动长时间运行的任务并在完成后回来查看、处理本地没有的仓库，或并行运行多个任务。支持桌面浏览器和 Claude iOS 应用。在 claude.ai/code 开始编程。

### JetBrains

面向 IntelliJ IDEA、PyCharm、WebStorm 及其他 JetBrains IDE 的插件，支持交互式 diff 查看和选区上下文共享。从 JetBrains Marketplace 安装 Claude Code 插件并重启 IDE。

## 你能做什么

以下是你使用 Claude Code 的一些方式：

**自动化你一直拖延的工作。** Claude Code 处理那些消耗你一天时间的琐碎任务：为未测试的代码编写测试、修复整个项目的 lint 错误、解决合并冲突、更新依赖，以及编写发布说明。

```
claude "write tests for the auth module, run them, and fix any failures"
```

**构建功能、修复 bug。** 用自然语言描述你想要什么。Claude Code 会规划方案、跨多个文件编写代码，并验证其是否可用。对于 bug，粘贴一条错误信息或描述症状。Claude Code 会在你的代码库中追踪问题、定位根因并实现修复。更多示例见「常见工作流」。

**创建提交和拉取请求。** Claude Code 直接与 git 协作。它会暂存更改、编写提交信息、创建分支并打开拉取请求。

```
claude "commit my changes with a descriptive message"
```

在 CI 中，你可以借助 GitHub Actions 或 GitLab CI/CD 自动化代码评审和 issue 分诊。

**用 MCP 连接你的工具。** 模型上下文协议（Model Context Protocol，MCP）是一个将 AI 工具连接到外部数据源的开放标准。借助 MCP，Claude Code 可以读取你在 Google Drive 中的设计文档、更新 Jira 中的工单、从 Slack 拉取数据，或使用你自己的自定义工具。

**用指令、技能与钩子进行定制。** CLAUDE.md 是你添加到项目根目录的一个 markdown 文件，Claude Code 会在每个会话开始时读取它。你可以用它设定编码规范、架构决策、首选库和评审清单。Claude 还会在工作时构建自动记忆，跨会话保存诸如构建命令、调试心得等经验，而无需你手动编写。你可以创建自定义命令来打包团队可复用的重复工作流，例如 /review-pr 或 /deploy-staging。钩子（hooks）允许你在 Claude Code 动作前后运行 shell 命令，例如每次编辑文件后自动格式化，或在提交前运行 lint。

**运行智能体团队、构建自定义智能体。** 同时派生出多个 Claude Code 智能体，让它们并行处理任务的不同部分。一个牵头智能体协调工作、分配子任务并合并结果。对于完全自定义的工作流，Agent SDK 让你能基于 Claude Code 的工具与能力构建自己的智能体，并完全掌控编排、工具访问与权限。

**用 CLI 进行管道、脚本与自动化。** Claude Code 可组合，并遵循 Unix 哲学。你可以把日志管道给它、在 CI 中运行它，或与其他工具串联：

```
# 分析最近的日志输出
tail -200 app.log | claude -p "Slack me if you see any anomalies"

# 在 CI 中自动化翻译
claude -p "translate new strings into French and raise a PR for review"

# 跨文件的批量操作
git diff main --name-only | claude -p "review these changed files for security issues"
```

完整的命令与标志见「CLI 参考」。

**安排定期任务。** 让 Claude 按计划运行，自动化重复性工作：早上的 PR 评审、夜间 CI 失败分析、每周依赖审计，或 PR 合并后同步文档。云端计划任务运行在 Anthropic 托管的基础设施上，即使你的电脑关机也照常运行。你可以从网页、桌面应用，或在 CLI 中运行 /schedule 来创建。

- 桌面计划任务运行在你的机器上，可直接访问本地文件与工具
- /loop 可在 CLI 会话内重复一个提示词，用于快速轮询

**随时随地工作。** 会话并不绑定于单一界面。随着上下文变化，你可以在不同环境之间迁移工作：

- 离开工位，仍可用「远程控制」（Remote Control）从手机或任意浏览器继续工作
- 用「消息派发」（Message Dispatch）从手机派发任务，并打开它创建的桌面会话
- 在网页或 iOS 应用上启动长时间任务，再用 claude --teleport 拉取到你的终端
- 用 /desktop 把终端会话交给桌面应用，进行可视化 diff 审阅
- 从团队聊天路由任务：在 Slack 中 @Claude 并附上 bug 报告，就能收到一个拉取请求

## 在任何地方使用 Claude Code

每个界面都连接到同一个底层 Claude Code 引擎，因此你的 CLAUDE.md 文件、设置和 MCP 服务器在所有界面上都能用。除了上面的终端、VS Code、JetBrains、桌面与网页环境，Claude Code 还与 CI/CD（持续集成 / 持续交付）、聊天和浏览器工作流集成：

| 我想…… | 最佳选择 |
| --- | --- |
| 从手机或另一台设备继续本地会话 | 远程控制（Remote Control） |
| 把 Telegram、Discord、iMessage 或自有 webhook 的事件推入会话 | Channels |
| 本地启动任务、在移动端继续 | 网页或 Claude iOS 应用 |
| 按固定计划运行 Claude | 云端计划任务或桌面计划任务 |
| 自动化 PR 评审与 issue 分诊 | GitHub Actions 或 GitLab CI/CD |
| 每个 PR 都自动获得代码评审 | GitHub Code Review |
| 把 Slack 的 bug 报告路由为拉取请求 | Slack |
| 调试线上 Web 应用 | Chrome |
| 为自有工作流构建自定义智能体 | Agent SDK |

## 下一步

安装 Claude Code 后，这些指南可助你深入：

- 快速入门：走完你的第一个真实任务，从探索代码库到提交一个修复
- 存储指令与记忆：用 CLAUDE.md 文件和自动记忆给 Claude 持久指令
- 常见工作流与最佳实践：充分发挥 Claude Code 的模式
- 设置：为你的工作流定制 Claude Code
- 故障排查：常见问题的解决方案
- code.claude.com：演示、定价与产品详情

---

来源：Anthropic《Claude Code 文档 · 入门篇 · 概览（Getting started / Overview）》
