## Comparing MCP to other approaches
 
#### MCP
 
#### Custom Integrations
 
#### ChatGPT Plugins
 
#### LangChain & Frameworks
 
#### Integration Speed
 
#### Integration Speed
 
✅ Fast, plug-and-play
 
❌ Slow, custom code
 
⚠️ Medium, proprietary
 
⚠️ Medium, custom code
 
#### Authentication
 
#### Authentication
 
✅ OAuth standard
 
❌ Manual API keys
 
⚠️ Plugin-specific OAuth
 
❌ Varies by implementation
 
#### Interaction Type
 
#### Interaction Type
 
✅ Continuous & context-rich
 
❌ Ad-hoc interactions
 
❌ Single-shot interactions
 
⚠️ Context limited
 
#### Open Standard
 
#### Open Standard
 
✅ Yes
 
❌ No
 
❌ No
 
⚠️ Framework-dependent
 
Let’s compare a few approaches that existed before or alongside MCP:
 - Custom Integrations & API Key Management: The most common traditional approach was to write custom code for each service and supply the LLM with credentials (API keys or tokens) to use those integrations. For example, you might write a Python function to query an API, give the LLM the ability to call that function, and manually handle the API key in your backend. This approach is labor-intensive and doesn’t scale – each new data source requires new code, and each environment must securely manage API keys. It often led to brittle systems, since every integration was unique. By contrast, MCP centralizes and standardizes these interactions: the AI agent just needs to handle the MCP protocol, and any MCP server (for any service) will work in a plug-and-play way. New servers can be added without changing the client’s code at all. Moreover, MCP provides a formal structure for authentication (discussed later) so that handing API keys to the AI isn’t done ad-hoc but through a secure protocol.
- ChatGPT Plugins (OpenAI Plugins): In 2023, OpenAI introduced a plugins system for ChatGPT that allowed models to call external APIs defined by an OpenAPI spec. This was an early step toward standardized tool use, but it has limitations. Each plugin is essentially its own mini-integration (with its own API schema and authentication), and they need to be built/hosted individually. Only certain platforms (like ChatGPT or Bing Chat) can use those plugins, since it was a proprietary approach. Plugins also were mostly one-shot calls – the model would call an API and get info, without a persistent connection or ongoing exchange. MCP differs in that it’s open and universal (not tied to one provider or interface) and it supports rich two-way interactions and continuous context. Think of ChatGPT plugins as specialized tools in a closed toolbox, whereas MCP is an open-standard toolkit that any developer or AI platform can utilize. MCP’s standardized auth (especially OAuth) also means it can handle secure access to user data in a more uniform way than the plugin-by-plugin OAuth flows in ChatGPT’s system. In summary, ChatGPT plugins showed the value of standardizing API access for LLMs, but MCP takes it further by making it an open protocol and by enabling a persistent “conversation” between AI and services.
- LLM Tool Frameworks (LangChain, Agentic libraries): Before MCP, many developers used frameworks like LangChain to give models tools. In these setups, you define a set of tool functions (with descriptions) and the agent’s prompting logic so the LLM can decide to use them. This works, but each tool still requires custom implementation behind the scenes – LangChain ended up with hundreds of tool integrations maintained in its library. Essentially, LangChain provided a developer-facing standard (a Python class interface) for integrating tools into an agent’s codebase, but nothing for the model to dynamically discover new tools at runtime. MCP is complementary to these frameworks, shifting the standardization to be model-facing. With MCP, an agent can discover and use any tool that an MCP server provides, even if the agent’s code didn’t explicitly include that tool ahead of time. In fact, LangChain has added support so it can treat MCP servers as just another tool source – meaning an agent built with LangChain can call MCP tools easily, leveraging the growing ecosystem of MCP servers. The difference is that MCP formalizes the interface over a protocol (JSON-RPC, with metadata, etc.), making it easier to plug into different environments, not just Python frameworks. Similarly, OpenAI’s native function calling feature can be seen as handling the formatting of a function call (the model outputs a JSON function call), whereas MCP handles the execution of that call in a standardized way . OpenAI’s function calling and MCP often work in tandem: the LLM produces a structured call, and the MCP client/server execute it and return the result, which together enables seamless tool use.
 
In essence, MCP isn’t the first attempt to connect LLMs with external APIs – but it learns from those past approaches (plugins, tool libraries, etc.) and unifies the solution. It provides an open, model-agnostic protocol that simplifies integration and authentication. Particularly around security and auth, MCP’s design (with OAuth support) avoids the patchwork of per-plugin keys or giving raw API keys to the model. Instead, authentication can be handled in a consistent, standardized flow as part of the protocol – a major step up from the status quo.

## MCP in action: technical deep dive

Let’s walk through a typical MCP interaction step-by-step to solidify how it works, and look at a bit of code. Imagine we have an AI assistant that wants to use an MCP server providing a set of tools (say, for a hypothetical “Neon” database service). The high-level flow is:

1. Connect to the MCP Server – The host application (AI assistant) initializes an MCP client and establishes a connection to the server. Depending on the server location, this could be via a local process (stdio) or a remote HTTP stream (SSE). Under the hood, the client sends an initialize message to handshake protocol versions and capabilities.

2. Discover Available Tools/Resources – The client then queries what the server offers. As shown earlier, it might send {"method": "tools/list"} and get back a list of tool definitions. The assistant can use this to inform the LLM (for example, by including the tool list in a system prompt or via the model’s function schema, depending on implementation). For instance, using an SDK, this could be one line of code like:

const tools = await mcpClient.request({ method: 'tools/list' }, ListToolsResultSchema);which returns a structured list of tools. Each tool entry has a name, description, and JSON schema for inputs, so the AI knows what it can do.

3. LLM Chooses a Tool – When a user asks the AI something that requires external action, the LLM determines (often via prompt engineering or function calling capabilities) that a certain tool should be used. For example, user asks: “What’s the latest price of AAPL stock?” The LLM sees it should call get_current_stock_price(company="AAPL", format="USD"). The host application captures this intent (e.g., OpenAI’s function calling API would return a function name and arguments in JSON).

4. Invoke the Tool via MCP – The client now sends a tools/call request to the server with the chosen tool name and parameters. We saw an example JSON for this earlier. In code, using an SDK, it might look like:

const result = await mcpClient.request({
 method: 'tools/call',
 params: { name: toolName, arguments: toolArgs }
}, CallToolResultSchema);This will cause the server to execute the tool’s handler on its side. The server might be calling an external API, performing a database query, or whatever logic that tool encapsulates. The result (could be a simple value or a complex JSON object) is sent back in a result field of the MCP response.

5. Return the Result to the LLM – The MCP client receives the tool’s output. Now the host application can integrate that back into the AI’s response. In many agent setups, the pattern is to inject the result into the conversation and ask the model to continue. For example, the assistant might then present: “The current stock price of AAPL is $173.22 (USD).” If using an automated loop, the result can be given to the model (perhaps appended to the conversation as a system message like “Result of get_current_stock_price: ...”) and the model can continue answering the user’s query with that information in mind.

Here’s a simplified illustration of calling a tool and using the result in a conversation using Anthropic’s Claude (which natively supports tool use):

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
In reality, frameworks handle a lot of this for you, but the above pseudo-code sketches how MCP fits into the loop. The key point is that MCP provides the standardized call/response layer for tool execution, which the AI agent code can hook into. Whether you’re using OpenAI, Anthropic, or another LLM, MCP stays the same – it’s the glue between the model’s intents and the external actions.

By using MCP, developers get a clear, structured pipeline for extending AI capabilities. The code becomes more maintainable (since you’re calling a generic mcpClient.request rather than service-specific code in each place) and the AI becomes more powerful (since it can tap into any MCP-connected service). Debugging is also easier – you can monitor the JSON-RPC messages to see exactly what was requested and returned, rather than parsing model-generated text for clues.

## Early limitations (no built-in authentication)

When MCP first emerged (late 2024), it offered the core protocol for tool and data exchange, but it lacked a standardized authentication mechanism for connecting to remote servers. In practice, early MCP demos and implementations often required running the MCP server locally or in a trusted environment, where authentication wasn’t a big concern (since the AI and server ran on the same machine). For example, developers could run an MCP server for Google Drive on their localhost with a pre-obtained token, then point their AI app to it. But using MCP over the internet or with third-party services was tricky without a formal auth flow.

Many initial MCP servers assumed the user would manually provide credentials or API keys to the server at startup. As an example, Anthropic’s quickstart suggested running pre-built servers by supplying your own credentials (API keys, tokens) via config or command-line. That means the server itself had access to your keys and the MCP client just trusted that server. While this works for personal or single-user scenarios, it doesn’t scale well for multi-user applications or cloud-hosted agents. There was no standard handshake for an AI agent to say, “Hey, I’m allowed to access this service on behalf of User X; here are my credentials.”

Essentially, early MCP clients had no way to authenticate to an MCP server except by out-of-band means (like pre-sharing a token or running without auth). This was a notable limitation – MCP was designed to be open and internet-based, but without an auth standard, secure remote use was handicapped.