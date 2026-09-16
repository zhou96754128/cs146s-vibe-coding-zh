# 构建远程 MCP 服务器（Build a Remote MCP server）

> 来源：Cloudflare 文档（Agents SDK）

本指南将向你展示如何使用 **Streamable HTTP 传输**（当前 MCP 规范标准）在 Cloudflare 上部署你自己的远程 MCP 服务器。你有两种选择：

- **不带身份认证** —— 任何人都可以连接并使用该服务器（无需登录）。

- **带身份认证与授权** —— 用户在访问工具前先登录，你可以根据用户的权限来控制智能体能调用哪些工具。

## 选择一种方案

Agents SDK 提供了多种创建 MCP 服务器的方式。选择适合你用例的方案：

| 方案 | 有状态？ | 需要 Durable Objects？ | 最适合 |
|---|---|---|---|
| `createMcpHandler()` | 否 | 否 | 无状态工具、最简单的搭建 |
| `McpAgent` | 是 | 是 | 有状态工具、每会话状态、elicitation |
| 原生 `WebStandardStreamableHTTPServerTransport` | 否 | 否 | 完全掌控、不依赖 SDK |

- `createMcpHandler()` 是让一个无状态 MCP 服务器跑起来的最快方式。当你的工具不需要每会话状态时用它。

- `McpAgent` 为每个会话提供一个 Durable Object，内置状态管理、elicitation 支持，并同时支持 SSE 与 Streamable HTTP 两种传输。

- 原生传输（Raw transport）让你在不想用 Agents SDK 辅助、想直接使用 `@modelcontextprotocol/sdk` 时获得完全掌控。

## 部署你的第一个 MCP 服务器

你可以先部署一个不带身份认证的公共 MCP 服务器 ↗，之后再添加用户认证和细粒度授权。如果你已经知道自己的服务器需要认证，可以直接跳到下一节。

### 通过仪表盘部署

下面的按钮会引导你完成部署一个示例 MCP 服务器 ↗ 到你的 Cloudflare 账户所需的全部操作：

部署完成后，该服务器将在你的 `workers.dev` 子域上线（例如 `remote-mcp-server-authless.your-account.workers.dev/mcp`）。你可以立即使用 **AI Playground** ↗（一个远程 MCP 客户端）、**MCP inspector** ↗ 或其他 MCP 客户端连接到它。

系统会在你的 GitHub 或 GitLab 账户上为你的 MCP 服务器新建一个 git 仓库，并配置为每次你推送改动或把拉取请求合并到仓库主分支时自动部署到 Cloudflare。你可以克隆这个仓库、在本地开发，并开始用自己的工具定制这个 MCP 服务器。

### 通过 CLI 部署

你可以使用 Wrangler CLI 在本地机器上新建一个 MCP 服务器，并部署到 Cloudflare。

- 打开终端，运行以下命令：

```bash
npm create cloudflare@latest -- remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
# yarn create cloudflare remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
# pnpm create cloudflare@latest remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```

在配置过程中，选择以下选项：

- 对于“Do you want to add an AGENTS.md file to help AI coding tools understand Cloudflare APIs?”，选择 **No**。
- 对于“Do you want to use git for version control?”，选择 **No**。
- 对于“Do you want to deploy your application?”，选择 **No**（我们会先在部署前测试服务器）。

现在，你的 MCP 服务器已搭建好，依赖也已安装。

- 进入项目文件夹：

```bash
cd remote-mcp-server-authless
```

在新项目的目录下，运行以下命令启动开发服务器：

```bash
npm start
# ⎔ Starting local server...[wrangler:info] Ready on http://localhost:8788
```

查看命令输出中的本地端口。在这个例子里，MCP 服务器运行在端口 8788，MCP 端点 URL 是 `http://localhost:8788/mcp`。

- 在本地测试服务器：

在一个新终端里，运行 MCP inspector ↗。MCP inspector 是一个交互式 MCP 客户端，让你能在网页浏览器里连接到你的 MCP 服务器并调用工具。

```bash
npx @modelcontextprotocol/inspector@latest
# 🚀 MCP Inspector is up and running at: http://localhost:5173/?MCP_PROXY_AUTH_TOKEN=46ab..cd3
# 🌐 Opening browser...
```

MCP Inspector 会在你的网页浏览器中启动。你也可以手动打开浏览器访问 `http://localhost:5173` 来启动它。查看命令输出中 MCP Inspector 运行的本地端口。在这个例子里，MCP Inspector 服务于端口 5173。

- 在 MCP inspector 中，输入你的 MCP 服务器 URL（`http://localhost:8788/mcp`），点击 **Connect**。选择 **List Tools** 即可显示你的 MCP 服务器暴露的工具。

- 现在你可以把 MCP 服务器部署到 Cloudflare 了。在项目目录下运行：

```bash
npx wrangler@latest deploy
```

如果你已经为这个带 MCP 服务器的 Worker 连接了一个 git 仓库，也可以通过把改动推送到仓库主分支或合并拉取请求来部署。

MCP 服务器将部署到你的 `*.workers.dev` 子域：`https://remote-mcp-server-authless.your-account.workers.dev/mcp`。

- 要测试远程 MCP 服务器，取你已部署服务器的 URL（`https://remote-mcp-server-authless.your-account.workers.dev/mcp`），把它输入到运行在 `http://localhost:5173` 的 MCP inspector 中。

现在，你已经拥有了一个 MCP 客户端可以连接的远程 MCP 服务器。

## 通过本地代理从 MCP 客户端连接

现在你的远程 MCP 服务器已经运行，你可以使用 `mcp-remote` 本地代理 ↗ 把 Claude Desktop 或其他 MCP 客户端连接到它——即使你的 MCP 客户端在客户端侧不支持远程传输或授权也能做到。这让你能用真实的 MCP 客户端测试与远程 MCP 服务器的交互体验。

例如，从 Claude Desktop 连接：

- 更新你的 Claude Desktop 配置，指向你的 MCP 服务器 URL：

```json
{ "mcpServers": { "math": { "command": "npx", "args": [ "mcp-remote", "https://remote-mcp-server-authless.your-account.workers.dev/mcp" ] } } }
```

重启 Claude Desktop 以加载 MCP 服务器。完成后，Claude 就能调用你的远程 MCP 服务器了。

- 要测试，可以让 Claude 使用你的某个工具。例如：

> 你能用 math 工具把 23 和 19 加起来吗？

Claude 应当调用该工具，并展示由远程 MCP 服务器生成的结果。

要了解如何与其他 MCP 客户端一起使用远程 MCP 服务器，请参阅《Test a Remote MCP Server》。

## 添加身份认证

你之前部署的公共 MCP 服务器示例允许任何客户端在无需登录的情况下连接并调用工具。要为你的 MCP 服务器添加用户认证，你可以集成 **Cloudflare Access** 或某个第三方服务作为 OAuth 提供方。你的 MCP 服务器处理安全的登录流程，并签发 MCP 客户端可以用来进行认证工具调用的访问令牌。用户用 OAuth 提供方登录，并授权其 AI 智能体使用细粒度权限来与你的 MCP 服务器暴露的工具交互。

### Cloudflare Access OAuth

你可以配置 MCP 服务器通过 Cloudflare Access 要求用户认证。Cloudflare Access 充当身份聚合器，校验用户邮箱、来自你现有身份提供方（如 GitHub 或 Google）的信号，以及 IP 地址、设备证书等其他属性。当用户连接 MCP 服务器时，他们会被提示登录已配置的身份提供方，只有通过你的 Access 策略才会被授予访问权限。

关于分步部署指南，请参阅《Secure MCP servers with Access for SaaS》。

### 第三方 OAuth

你可以把 MCP 服务器连接到任何支持 OAuth 2.0 规范的 OAuth 提供方，包括 GitHub、Google、Slack、Stytch、Auth0、WorkOS 等等。

下面的例子演示如何使用 GitHub 作为 OAuth 提供方。

#### 第 1 步 —— 新建一个 MCP 服务器

运行以下命令，新建一个带 GitHub OAuth 的 MCP 服务器：

```bash
npm create cloudflare@latest -- my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
# yarn create cloudflare my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
# pnpm create cloudflare@latest my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

现在，你的 MCP 服务器已搭建好，依赖也已安装。进入项目文件夹：

```bash
cd my-mcp-server-github-auth
```

你会注意到，在示例 MCP 服务器中，如果打开 `src/index.ts`，主要区别在于 `defaultHandler` 被设置成了 `GitHubHandler`：

```typescript
import GitHubHandler from "./github-handler";
export default new OAuthProvider({
  apiRoute: "/mcp",
  apiHandler: MyMCP.serve("/mcp"),
  defaultHandler: GitHubHandler,
  authorizeEndpoint: "/authorize",
  tokenEndpoint: "/token",
  clientRegistrationEndpoint: "/register",
});
```

这确保你的用户被重定向到 GitHub 进行认证。不过要让这一切运转起来，你需要在下面的步骤里创建 OAuth 客户端应用。

#### 第 2 步 —— 创建 OAuth App

你需要创建两个 GitHub OAuth Apps ↗，才能把 GitHub 用作 MCP 服务器的认证提供方——一个用于本地开发，一个用于生产环境。

#### 第 2.1 步 —— 为本地开发新建 OAuth App

访问 `github.com/settings/developers` ↗，用以下设置新建一个 OAuth App：

- Application name: `My MCP Server (local)`
- Homepage URL: `http://localhost:8788`
- Authorization callback URL: `http://localhost:8788/callback`

- 对于刚创建的 OAuth App，把它的 client ID 添加为 `GITHUB_CLIENT_ID`，并生成一个 client secret，把它作为 `GITHUB_CLIENT_SECRET` 添加到项目根目录下的 `.env` 文件中（用于在本地开发时设置密钥）。

```bash
touch .env
echo 'GITHUB_CLIENT_ID="your-client-id"' >> .env
echo 'GITHUB_CLIENT_SECRET="your-client-secret"' >> .env
cat .env
```

运行以下命令启动开发服务器：

```bash
npm start
```

你的 MCP 服务器现在运行在 `http://localhost:8788/mcp`。

- 在一个新终端里，运行 MCP inspector ↗。MCP inspector 是一个交互式 MCP 客户端，让你能在网页浏览器里连接到你的 MCP 服务器并调用工具。

```bash
npx @modelcontextprotocol/inspector@latest
```

在网页浏览器中打开 MCP inspector：

```bash
open http://localhost:5173
```

在 inspector 中，输入你的 MCP 服务器 URL：`http://localhost:8788/mcp`。

- 在右侧主面板中，点击 **OAuth Settings** 按钮，然后点击 **Quick OAuth Flow**。

你应当会被重定向到 GitHub 登录或授权页面。授权 MCP 客户端（即 inspector）访问你的 GitHub 账户后，你会被重定向回 inspector。

- 点击侧边栏中的 **Connect**，你应当能看到 **List Tools** 按钮，它会列出你的 MCP 服务器暴露的工具。

#### 第 2.2 步 —— 为生产环境新建 OAuth App

你需要重复第 2.1 步，为生产环境再新建一个 OAuth App。

- 访问 `github.com/settings/developers` ↗，用以下设置新建一个 OAuth App：

- Application name: `My MCP Server (production)`
- Homepage URL: 输入你已部署 MCP 服务器的 `workers.dev` URL（例如 `worker-name.account-name.workers.dev`）
- Authorization callback URL: 输入你已部署 MCP 服务器的 `workers.dev` URL 的 `/callback` 路径（例如 `worker-name.account-name.workers.dev/callback`）

- 对于刚创建的 OAuth App，使用 Wrangler CLI 添加 client ID 和 client secret：

```bash
npx wrangler secret put GITHUB_CLIENT_ID
npx wrangler secret put GITHUB_CLIENT_SECRET
npx wrangler secret put COOKIE_ENCRYPTION_KEY # 在这里添加任意随机字符串，例如 openssl rand -hex 32
```

**设置一个 KV 命名空间**

a. 创建 KV 命名空间：

```bash
npx wrangler kv namespace create "OAUTH_KV"
```

b. 用生成的 KV ID 更新 `wrangler.jsonc` 文件：

```json
{ "kvNamespaces": [ { "binding": "OAUTH_KV", "id": "<你的 KV ID>" } ] }
```

把 MCP 服务器部署到你的 Cloudflare `workers.dev` 域：

```bash
npm run deploy
```

使用 AI Playground ↗、MCP Inspector 或其他 MCP 客户端连接到运行在 `worker-name.account-name.workers.dev/mcp` 的服务器，并用 GitHub 完成认证。

## 下一步

- **MCP 工具** —— 给你的 MCP 服务器添加工具。
- **授权** —— 定制身份认证与授权。

---

> 来源：Cloudflare 文档《构建远程 MCP 服务器（Build a Remote MCP server）》
