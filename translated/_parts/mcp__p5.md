## MCP 实战：技术深度剖析

我们逐步走一遍典型的 MCP 交互流程，把这个机制钉牢，并看一点代码。设想有一个 AI 助手，它想使用某个 MCP 服务器提供的一组工具（比如一个假想的「Neon」数据库服务）。整体流程如下：

1. **连接到 MCP 服务器**——宿主应用（AI 助手）初始化一个 MCP 客户端，并与服务器建立连接。视服务器位置而定，这可能是本地进程（stdio），也可能是远程 HTTP 流（SSE）。在底层，客户端会发送一条 initialize 消息，用于握手协议版本与能力。

2. **发现可用的工具/资源**——客户端接着查询服务器提供了什么。如前所示，它可能发送 {"method": "tools/list"}，然后拿回一份工具定义列表。助手可以用它来告知 LLM（例如把工具列表放进系统提示词，或通过模型的函数 schema，具体取决于实现）。举例来说，用某个 SDK 时，这可能只是一行代码：

const tools = await mcpClient.request({ method: 'tools/list' }, ListToolsResultSchema);

它返回一份结构化的工具列表。每个工具条目都包含名称、描述和输入的 JSON schema，因此 AI 知道自己能做什么。

3. **LLM 选择工具**——当用户向 AI 提出一个需要外部动作的问题时，LLM 会（通常借助提示词工程或函数调用能力）判断应当使用某个工具。例如用户问：「AAPL 股票的最新价格是多少？」LLM 会看出应当调用 get_current_stock_price(company="AAPL", format="USD")。宿主应用捕获这一意图（比如 OpenAI 的函数调用 API 会返回 JSON 格式的函数名与参数）。

4. **通过 MCP 调用工具**——客户端随后向服务器发送 tools/call 请求，带上所选的工具名与参数。前面我们已经看过对应的 JSON 示例。在代码里，用某个 SDK 可能长这样：

const result = await mcpClient.request({
 method: 'tools/call',
 params: { name: toolName, arguments: toolArgs }
}, CallToolResultSchema);

这会让服务器在其一侧执行该工具的处理函数。服务器可能在调用外部 API、执行数据库查询，或执行该工具封装的任何逻辑。结果（可能是简单值，也可能是复杂的 JSON 对象）会通过 MCP 响应的 result 字段返回。

5. **把结果返回给 LLM**——MCP 客户端收到工具的输出。现在宿主应用可以把它整合回 AI 的回复中。在许多智能体方案里，固定套路是把结果注入对话，然后让模型继续。例如，助手可能接着给出：「AAPL 当前股价为 173.22 美元（USD）。」如果使用自动循环，结果可以交给模型（比如作为系统消息追加到对话中，形如「Result of get_current_stock_price: ...」），模型便能带着这条信息继续回答用户的提问。

下面是一个简化示例，演示如何借助 Anthropic 的 Claude（原生支持工具使用）调用工具并把结果用回对话中：

// 1. Send user prompt to LLM with available tools context
const response = await anthropicClient.complete({
 prompt: "User: Can you list my projects?\nAssistant: ",
 model: "claude-3.5",
 tools: tools // list of tools from MCP server
});
for (const msg of response.messages) {
 if (msg.type === 'tool_use') {
 // 2. LLM decided to use a tool
 const { name, args } = msg;
 // 3. Call the tool via MCP
 const toolRes = await mcpClient.request({ method: 'tools/call', params: { name, arguments: args } });
 // 4. Inject tool result and resume LLM
 await anthropicClient.send({ role: 'system', content: `Tool result: ${toolRes.result}` });
 } else {
 // 5. Handle normal LLM reply (tool result likely integrated)
 console.log("Assistant:", msg.content);
 }
}

现实中，框架会替你处理其中大量工作，但上面的伪代码勾勒出了 MCP 在循环里的位置。关键在于：MCP 为工具执行提供了标准化的调用/响应层，AI 智能体的代码可以挂接上去。无论你用的是 OpenAI、Anthropic 还是别的 LLM，MCP 都保持不变——它是模型意图与外部动作之间的黏合剂。

通过使用 MCP，开发者获得了一条清晰、结构化、可扩展 AI 能力的流水线：代码更易维护（因为你调用的是一套通用的 mcpClient.request，而不是在每个地方写服务专属代码），AI 也更强（因为它能接入任何与 MCP 相连的服务）。调试同样更容易——你可以监控 JSON-RPC 消息，确切看到请求了什么、返回了什么，而不必从模型生成的文本里猜线索。

## 早期局限（没有内置认证）

MCP 刚出现时（2024 年底），它提供了工具与数据交换的核心协议，但缺少连接远程服务器的标准化认证机制。在实践中，早期的 MCP 演示与实现常常要求 MCP 服务器在本地或可信环境中运行，此时认证并不构成大问题（因为 AI 与服务器跑在同一台机器上）。例如，开发者可以在本机 localhost 上跑一个 Google Drive 的 MCP 服务器，并预先准备好令牌，再让自己的 AI 应用指向它。但如果要通过互联网使用 MCP，或者对接第三方服务，没有正式的认证流程就会很棘手。

许多早期 MCP 服务器假定用户会在启动时手工向服务器提供凭证或 API 密钥。举例来说，Anthropic 的快速入门指南就建议通过配置或命令行把自己的凭证（API 密钥、令牌）交给预置服务器来运行。这意味着服务器本身能接触到你的密钥，而 MCP 客户端只是信任这台服务器。这对个人或单用户场景可行，但对多用户应用或云端托管的智能体就难以扩展。当时并没有标准化的握手方式，让 AI 智能体能说：「嘿，我被授权代表用户 X 访问这项服务，这是我的凭证。」

本质上，早期 MCP 客户端除了通过带外方式（例如预先共享令牌，或干脆不做认证），没有别的办法向 MCP 服务器完成认证。这是一个显著的局限——MCP 本是为开放、基于互联网而设计的，但缺少认证标准，使其安全的远程使用受到严重掣肘。
