Cognition Team June 2025 15 minute read

 
# Coding Agents 101: The Art of Actually Getting Things Done

 
The year is 2025. Coding agents aren't magic, but they're about the closest thing we have. We've noticed some engineers, in particular at the senior-to-staff level, finding success faster than others. Here we share some top lessons sourced from the experience of our customers and ourselves.

 About this guide: 
 
 
## Product-agnostic

 
We discuss tips that will help you be successful with any coding agent.

 
 
 
## Tactical

 
We offer our favorite bits of actionable advice.

 
 
 
## Technical

 
While coding agents can be valuable to many, this guide is written with engineers in mind.

 
 
 
 
Developer tooling has been rapidly evolving. Ten years ago, it was autocomplete and intellisense, capable of suggesting method names and carrying out programmatic refactors. Four years ago, it was copilots and tab complete, capable of writing the next couple lines of code for you. Two years ago, it was generative chatbots, capable of assisting your development and generating entire files for you. Today, it is autonomous agents, capable of taking initial descriptions to final pull requests with little human intervention. We've focused on realizing this vision over the past two years by building Devin. Now, interest in autonomous agents is reaching new heights, especially with recent releases of similar products [1] Other than Devin, some recent releases include Codex by OpenAI and Jules by Google. Some local agents like Cursor and Claude Code can be run in parallel workspaces to replicate a similar effect.. These agents can appear in many forms, including web apps, mobile apps, and integrations within popular tools like Slack, GitHub, Linear, and Jira.

 
 
 
While a human paired with an AI assistant can achieve more than any AI alone, an autonomous agent's ability to handle tasks end to end allows for a new level of multi-tasking, turning every engineer into an engineering manager.

 
 
 
Adapting to working effectively alongside these new AI colleagues can take some time. Interestingly, we've observed that senior-to-staff level engineers tend to adopt and become proficient with these tools the fastest. Ultimately, these tools will become commonplace across all levels of engineering. Based on our experience and customer feedback, we want to share key insights and lessons learned to help everyone successfully integrate these tools into their workflows.

 

 
 
(Getting Started)

 
## Prompting Basics

 
These fundamental guidelines will help you effectively interact with coding agents in 2025. If you take nothing else away, you should at least remember these.

 
 
 
### Say how you want things done, not just what

 
Think of the agent as a junior coding partner whose decision-making can be unreliable. Simple tasks can be described directly, but for more complex tasks, clearly outline your preferred approach from the outset. Providing the agent with the overall architecture and logic upfront not only boosts its chances of success but also reduces your time reviewing code, as you will already be familiar with the intended method.

 
 
#### Example:

 
Instead of "add unit tests," specify the functionality to test, identify important edge cases, and clarify what needs mocking, if anything.

 
 
 
 
### Tell the agent where to start

 
Think about where you'd start if you were handling the task yourself. Even if you don't know specific file or function names, mention the repository, relevant documentation, and key components involved. Clearly indicating these elements minimizes wasted effort and confusion.

 
 
#### Example:

 
"Please add support for Google models to our code. You should look at the latest docs [here](link) and create a new implementation file in the model groups directory"

 
 
 
 
### Practice defensive prompting

 
Imagine giving the same prompt to a new intern. Where would confusion or errors likely arise? Anticipate these points and proactively clarify your instructions to avoid ambiguity.

 
 
#### Example:

 
"Please fix the C++ bindings for our search module to pass the new unit tests. Be careful, you will probably need to recompile the bindings each time you change the code before you test."

 
 
 
 
### Give access to CI, tests, types, and linters

 
Much of the magic of agents comes from their ability to fix their own mistakes and iterate against error messages. Providing strong feedback loops through tools like type checkers, linters, and unit tests greatly enhances their performance. Consider typed Python over plain Python, or TypeScript over JavaScript. Teach your agent how to run common checks and tests, ensuring it has all necessary packages and access rights. If the agent can interact with a browser, provide clear instructions on running your front-end development environment.

 
 
#### Example:

 
Our team transitioned from mostly untyped Python SDKs to exclusively typed SDKs (this is also a good task ideally for coding agents).

 
 
 
 
### Leverage your expertise

 
Everything above becomes easier when you're familiar with your codebase. Even simple tasks benefit from your ability to verify logic and results. Human oversight remains essential—ultimately, you hold responsibility for the final correctness of the code. Ownership and verification will continue to be critical responsibilities for human engineers, even as these tools become increasingly sophisticated.

 

 
 
(Getting Started)

 
## Using Agents in your Workflow

 
Once you've got the basics of talking to an agent down, it's time to bring these AI helpers into your daily workflow. Here are some practical ways to make agents part of your routine:

 
 
 
### Take on new tasks immediately

 
Imagine a teammate messaging you, "Hey, could we build X quickly?" or "We need to tweak Y." Instead of letting it interrupt your flow, just send a quick prompt to an autonomous agent to investigate or make the change. This frees you to stay focused on your main tasks. Got an interesting side project idea? Need to quickly prototype something, scrape data, or reproduce research? Delegate to your agent and circle back later.

 
 
#### Example:

 
Many teams simply tag @Devin on Slack when discussing bug fixes or minor feature updates.

 
 
 
 
### Code on the go

 
Picture yourself commuting or traveling when an urgent bug pops up, or you realize you might have left a mistake in your code. No worries! Autonomous agents often support mobile access, letting you address these issues instantly. Whether through Slack's mobile app or a dedicated mobile app, many agents let you resolve problems on the go, even if your wifi is sketchy.

 
 
#### Example:

 
Having this optionality has made our own team much more productive on car rides and flights.

 
 
 
 
### Hand off your chores

 
Stuck bisecting for old commits or updating documentation for a new feature? Hand these repetitive tasks off to your agent. You'll save precious time and stay focused on more creative and impactful work.

 
 
#### Example:

 
In our team, it is common for an engineer to ship a change and then have an agent update all the relevant docs & user-facing copy.

 
 
 
 
### Skip the analysis paralysis

 
Stuck deciding if a refactor will actually simplify your code? Can't choose between two architectural approaches? Have your agent implement both options. With concrete examples to compare, decision-making becomes straightforward, and you won't hurt any feelings by discarding a solution.

 
 
#### Example:

 
When choosing between Lexical and Slate for text boxes, we had agents implement each. Slate won out for delivering the better end result.

 
 
 
 
### Set up preview deployments

 
Set your CI/CD pipeline to automatically create preview deployments with each new PR, giving you an instant live URL. This is particularly handy when reviewing frontend tasks completed by AI agents.

 
 
#### Example:

 
Vercel is a deployment platform that makes preview deployments super easy.

 
 

 
 
(Intermediate)

 
## Delegating Larger Tickets

 
-->
 
 
 
 
 
 As the size and complexity of your pull requests grow beyond just a few files, handling them in a single pass becomes challenging. Yet, mastering how to delegate medium-to-large tasks (typically 1-6 hours of work) is where autonomous agents give the highest ROI. Rather than saving just a few minutes, you can reclaim hours of productivity. Smaller tasks might work effortlessly, but stretching the capabilities of agents to handle larger tasks brings the biggest returns.

 
 
 
### Automate your first drafts

 
For substantial tasks, using an autonomous agent to create an initial draft of your PR can kickstart progress and dramatically cut down your workload. Success here depends on clearly communicating your desired approach upfront. Think of yourself as the architect guiding junior developers. Clear, detailed instructions help avoid spending unnecessary time correcting fundamental misunderstandings in the agent's code.

 
 
 
 
 
 
 Domain 
 Drafting 
 Refining 
 
 
 
 
 Journalism 
 Journalist collects initial information, writes first draft of article 
 The editor reviews drafts, fact checks, polishes, and finalizes for publication. 
 
 
 Restaurant 
 Line cooks prep ingredients and make preliminary dishes. 
 The sous chef adds seasonings and adjusts the dish to taste better, before it is sent to diners. 
 
 
 Coding 
 Autonomous agents get started on tasks based on initial plans and creating first draft solutions 
 Human developer reviews the draft PRs, gives feedback, and adds manual refinements before merging 
 
 
 
 
 
 
 
🛑 Remember, large tasks aren't completely hands-free (yet). Expect multiple feedback cycles for more challenging assignments, and anticipate some manual refinements for polish. A realistic goal is around 80% time savings, not complete automation, with your expertise remaining vital for verification and final quality assurance.

 
 
 
### Co-develop a PRD

 
For tasks that are complex or vaguely defined, collaborating with your autonomous agent to create a detailed plan can be highly effective. It's perfectly okay if you initially don't know every nuance or requirement. Start by prompting your agent to explore discovery questions, like "How does our authentication system function?" or "Which services might be impacted?" You can also ask the agent to identify specific relevant code targets for you to confirm early on.

 
Certain agents, such as Devin and Claude Code, offer dedicated planning modes that focus on reading and exploring existing code rather than immediately modifying it. If you'd prefer deeper preparation before delegating a task, specialized codebase search tools like deepwiki.com and Devin Search can quickly provide insights into your codebase, helping streamline the process.

 
 
 
### Set checkpoints

 
For multi-part tasks, especially those involving multiple codebases, establish clear checkpoints along the way:

 
Plan → Implement chunk → Test → Fix → Checkpoint review → Next chunk

 
Explicitly request pauses after each significant phase, particularly for complex features built across multiple layers (e.g., database, backend, frontend). Use these checkpoints to ensure implementation aligns with your expectations, clarify doubts (ex. "Explain the auth process and confirm its security"), and correct course early to avoid cascading issues.

 
 
 
 
#### Example:

 
"I want you to implement this feature that will span our database, backend, and multiple frontend interfaces. Please first plan out the database schema changes needed, and let me know when that is done so I can apply the migration." -> "Now please implement the backend changes and add tests to make sure XYZ works. Let me know when that is done" -> "Now implement the changes in both our web and mobile interfaces to call the new backend endpoint"