- Threat Research Center
- Threat Research
- Malware
 
 
 Malware 
 
# AI Agents Are Here. So Are the Threats.

 
 
 21 min read 
 
 
 Related Products Prisma SASE Secure Access Service Edge (SASE) Unit 42 AI Security Assessment Unit 42 Incident Response 
 
 
 
 
 
 
 - By:Jay Chen
- Royce Lu
 - Published:May 1, 2025
 - Categories:Malware
- Threat Research
 
 - Tags:Agentic AI
- AI
- BOLA
- GenAI
- Prompt injection
 
 
 
 
 - 

 - 

 
 
 
 Share 
 - 

 - 

 - 

 - 

 - 

 - 

 - 

 
 
 
 
 
 
 
 
 
 
 
 
 
 
## Executive Summary

Agentic applications are programs that leverage AI agents — software designed to autonomously collect data and take actions toward specific objectives — to drive their functionality. As AI agents are becoming more widely adopted in real-world applications, understanding their security implications is critical. This article investigates ways attackers can target agentic applications, presenting nine concrete attack scenarios that result in outcomes such as information leakage, credential theft, tool exploitation and remote code execution.

To assess how widely applicable these risks are, we implemented two functionally identical applications using different open-source agent frameworks — CrewAI and AutoGen — and executed the same attacks on both. Our findings show that most vulnerabilities and attack vectors are largely framework-agnostic, arising from insecure design patterns, misconfigurations and unsafe tool integrations, rather than flaws in the frameworks themselves.

We also propose defense strategies for each attack scenario, analyzing their effectiveness and limitations. To support reproducibility and further research, we’ve open-sourced the source code and datasets on GitHub.

### Key Findings

 
- Prompt injection is not always necessary to compromise an AI agent. Poorly scoped or unsecured prompts can be exploited without explicit injections.

- Mitigation: Enforce safeguards in agent instructions to explicitly block out-of-scope requests and extraction of instruction or tool schema.

- Prompt injection remains one of the most potent and versatile attack vectors, capable of leaking data, misusing tools or subverting agent behavior.

- Mitigation: Deploy content filters to detect and block prompt injection attempts at runtime.

- Misconfigured or vulnerable tools significantly increase the attack surface and impact.

- Mitigation: Sanitize all tool inputs, apply strict access controls and perform routine security testing, such as with Static Application Security Testing (SAST), Dynamic Application Security Testing (DAST) or Software Composition Analysis (SCA).

- Unsecured code interpreters expose agents to arbitrary code execution and unauthorized access to host resources and networks.

- Mitigation: Enforce strong sandboxing with network restrictions, syscall filtering and least-privilege container configurations.

- Credential leakage, such as exposed service tokens or secrets, can lead to impersonation, privilege escalation or infrastructure compromise.

- Mitigation: Use a data loss prevention (DLP) solution, audit logs and secret management services to protect sensitive information.

- No single mitigation is sufficient. A layered, defense-in-depth strategy is necessary to effectively reduce risk in agentic applications.

- Mitigation: Combine multiple safeguards across agents, tools, prompts and runtime environments to build resilient defenses.

 

It is important to emphasize that neither CrewAI nor AutoGen are inherently vulnerable. The attack scenarios in this study highlight systemic risks rooted in language models’ limitation in resisting prompt injection and misconfigurations or vulnerabilities in the integrated tool — not in any specific framework. Therefore, our findings and recommended mitigations are broadly applicable across agentic applications, regardless of the underlying frameworks.

Palo Alto Networks redefines AI security with Prisma AIRS (AI Runtime Security) — delivering real-time protection for your AI applications, models, data, and agents. By intelligently analyzing network traffic and application behavior, Prisma AIRS proactively detects and prevents sophisticated threats like prompt injection, denial-of-service attacks, and data exfiltration. With seamless, inline enforcement at both the network and API levels.

Meanwhile, AI Access Security offers deep visibility and precise control over third-party generative AI (GenAI) use. This helps prevent shadow AI risks, data leakage and malicious content in AI outputs through policy enforcement and user activity monitoring. Together, these solutions provide a layered defense that safeguards both the operational integrity of AI systems and the secure use of external AI tools.

A Unit 42 AI Security Assessment can help you proactively identify the threats most likely to target your AI environment.

If you think you might have been compromised or have an urgent matter, contact the Unit 42 Incident Response team.

 
 
 
 Related Unit 42 Topics 
 GenAI , Prompt Injection 
 
 
 

## An Overview of the AI Agent

An AI agent is a software program designed to autonomously collect data from its environment, process information and take actions to achieve specific objectives without direct human intervention. These agents are typically powered by AI models — most notably large language models (LLMs) — which serve as their core reasoning engines.

A defining feature of AI agents is their ability to connect AI models to external functions or tools, allowing them to autonomously decide which tools to use in pursuit of their objectives. A function or tool is an external capability — like an API, database or service — that the agent can call to perform specific tasks beyond the model's built-in knowledge. This integration enables them to reason through given tasks, plan solutions and execute actions effectively to achieve their goals. In more complex scenarios, multiple AI agents can collaborate as a team — each handling different aspects of a problem — to solve larger and more intricate challenges collectively. ​

AI agents have diverse applications across various sectors. In customer service, they power chatbots and virtual assistants to handle inquiries efficiently. In finance, they assist with fraud detection and portfolio management. Healthcare can also utilize AI agents for patient monitoring and diagnostic support.

Figure 1 is a typical AI Agent architecture that shows how an agent uses an LLM to plan, reason and act through an execution loop. It connects to external tools via function calling to perform tasks such as accessing code, data or human input.

 Figure 1. AI agent architecture. 

The agent could also incorporate memory — both short- and long-term — to retain context and enhance decision-making. Applications interact with the agent by sending requests and receiving results through input and output interfaces, typically exposed as APIs.

## Security Risks of AI Agents

As AI agents are typically built on LLMs, they inherit many of the security risks outlined in the OWASP Top 10 for LLMs, such as prompt injection, sensitive data leakage and supply chain vulnerabilities. However, AI agents go beyond traditional LLM applications by integrating external tools that are often built in various programming languages and frameworks.

Including these external tools exposes the LLMs to classic software threats like SQL injection, remote code execution and broken access control. This expanded attack surface, combined with the agent’s ability to interact with external systems or even the physical world, makes securing AI agents particularly critical.

The recently published article OWASP Agentic AI Threats and Mitigation highlights these emerging threats. Below is a summary of key threats relevant to the attack scenarios demonstrated in the next section:

 
- Prompt injection: Attackers sneak in hidden or misleading instructions to a GenAI system, attempting to cause the application to deviate from its intended behavior. This can cause the agent to behave in unexpected ways, like ignoring given rules and policies, revealing sensitive information or using tools to take unintended actions.

- Tool misuse: Attackers manipulate the agent — often through deceptive prompts — to abuse its integrated tools. This can involve triggering unintended actions or exploiting vulnerabilities within the tools, potentially resulting in harmful or unauthorized execution.

- Intent breaking and goal manipulation: Attackers target an AI agent’s ability to plan and pursue objectives by subtly altering its perceived goals or reasoning process. Attackers exploit these vulnerabilities to redirect the agent’s actions away from its original intent. A common tactic includes agent hijacking, where adversarial inputs distort the agent’s understanding and decision-making.

- Identity spoofing and impersonation: Attackers exploit weak or compromised authentication to pose as legitimate AI agents or users. A major risk is the theft of agent credentials, which can allow attackers to access tools, data or systems under a false identity.

- Unexpected RCE and code attacks: Attackers exploit the AI agent’s ability to execute code. By injecting malicious code, they can gain unauthorized access to elements of the execution environment, like the internal network and host file system. This poses serious risks, especially when agents have access to sensitive data or privileged tools.

- Agent communication poisoning: Attackers target the interactions between AI agents by injecting attacker-controlled information into their communication channels. This can disrupt collaborative workflows, degrade coordination and manipulate collective decision-making — especially in multi-agent systems where trust and accurate information exchange are critical.

- Resource overload: Attackers exploit the AI agent’s allocated resources by overwhelming their compute, memory or service limits. This can degrade performance, disrupt operations and make the application unresponsive, impacting all the users of the application.

 

## Simulated Attacks on AI Agents

To investigate the security risks of AI agents, we developed a multi-user and multi-agent investment advisory assistant using two popular open-source agent frameworks: CrewAI and AutoGen. Both implementations are functionally identical and share the same instructions, language models and tools.

This setup highlights that the security risks are not specific to any framework or model. Instead, they stem from misconfigurations or insecure design introduced during agent development. It is important to note that CrewAI or AutoGen frameworks are NOT vulnerable.

Figure 2 illustrates the architecture of the investment advisory assistant, which consists of three cooperating agents: the orchestration agent, news agent and stock agent.

 Figure 2. Investment advisory assistant architecture. 
 
- Orchestration agent: This agent manages the user interaction. It interprets user requests, delegates tasks to the appropriate agents, consolidates their outputs and delivers final responses back to the user.

- News agent: This agent gathers and summarizes the latest financial news about a specific company or industry. It is equipped with two tools:

Search engine tool: This tool uses Google to retrieve URLs pointing to relevant financial news. We use CrewAI’s implementation of SerperDevTool.

- Web content reader tool: This tool fetches and extracts text content from a given webpage. We use CrewAI’s implementation of ScrapeWebsiteTool.

 
 
- Stock agent: This agent helps users manage their stock portfolios, including viewing transaction history, buying or selling stocks, retrieving historical stock prices and generating visualizations. It uses three tools:

Database tool: This tool provides functions to read from or update the portfolio database, sell or buy stocks, and view transaction history.