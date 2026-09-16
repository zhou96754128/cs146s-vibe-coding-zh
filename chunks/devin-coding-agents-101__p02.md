 
 
 
 
### Teach it to verify its own work

 
When giving feedback, go beyond simply pointing out issues ("This function isn't working"). Clearly articulate your testing process to enable the agent to independently verify future tasks. For testing patterns you'll frequently repeat, integrate these into your agent's permanent knowledge base (See Add to your agent's knowledge base).

 
 
#### Example:

 
In Devin, we actively prompt users to save essential testing procedures to the agent's ongoing memory, streamlining future interactions.

 
 
 
 
### Increase test coverage in AI hot spots

 
Currently, agents aren't fully capable of interactively testing all scenarios thoroughly. Enhancing test coverage in areas heavily modified by AI ensures greater confidence in the agent's output. Solid tests mean that code that appears correct can be confidently merged without worry.

 
 
#### Example:

 
Our team strengthened unit tests in a critical section of our codebase before entrusting our AI to translate the implementation from Python to C.

 
 

 
 
(Advanced)

 
## Automating Workflows

 
Agents can respond to incoming events much faster than humans, and they're a lot more willing to do boring, repetitive work, than their human counterparts.

 
 
 
### Create Shortcuts for Your Most Repetitive Work

 
Engineering teams frequently encounter repetitive, routine tasks. These are perfect candidates for automation with agents. Common examples include:

 
 
 - feature flag removal

 - dependency upgrades

 - fixing and adding tests on new feature PRs

 
 
 
 
 
To set this up efficiently, an experienced engineer typically creates a robust, reusable prompt template [2] In Devin, these are called playbooks that can run repeatedly for these scenarios.

 
 
#### Example:

 
One of our customers automatically triggers three agents dedicated to writing unit tests whenever new features are developed.

 
 
 
 
### Intelligent Code Review & Enforcement

 
While specialized tools for fast code review exist [3] Such as Greptile and CodeRabbit , autonomous agents can be an interesting option to deliver more accurate insights, particularly if they've already indexed the functionality of your repositories.

 
 
#### Example:

 
At Cognition, we like to maintain a list of the most common mistakes engineers make and we commit this list to the codebase. Then, instead of writing classical lint rules to catch these (which is often not possible), we have an agent run on every new PRs to check for these mistakes.

 
 
 
 
### Hook into incidents and alerts

 
You can also set up autonomous agents to trigger automatically in response to specific events. For example, Devin provides an accessible API, and other agents can be integrated into custom workflows via CLI commands. These setups work especially well alongside MCPs to ingest third-party error logs.

 
⚠️When it comes to triaging issues in production services, AI's debugging skills are not that great. Instead of asking the AI to fix bugs end-to-end as they come up, it is often more practical to ask the AI to just flag the most suspicious errors, changes, etc.

 

 
 
(Advanced)

 
## Customization & Improving Performance

 
 
 
### Environment Setup

 
Nothing slows down an agent faster than an incomplete or mismatched environment. To keep things running smoothly, align your agent's setup exactly with your team's. This includes language versions, package dependencies, and automated checks. For example, pre-commit should be installed in the agent's environment and environment configurations (secrets, language versions, virtual environments, browser logins) should be sourced automatically using tools like .envrc or custom configuration of .bashrc

 
 
#### Example:

 
We set up our agent's browser with pre-authenticated logins, removing the hassle of manual authentication and making testing much easier.

 
 
 
 
### Build Custom CLI Tools and MCPs

 
MCPs are widely available and are quick to set up and experiment with connecting your agent to external tools [4] In Devin, MCPs are still in beta as we're figuring out the best way to support them. Please contact us for access!. But many people overlook setting up simple CLI scripts for your agents. As a simple example, you could give your agent a script to pull information about a linear ticket given a ticket ID. You might also want to give your agent a tool to perform common parts of a workflow reliably, such as a script for restarting the local development environment.

 
 
#### Example:

 
We have a customer who has had a lot of success with creating a CLI tool that surfaces only the first failing test in a test suite. The CLI prompts the agent to focus on only that test with detailed error information, and this CLI leads the agent to have higher success and faster completion rates on long tasks.

 
 
 
 
### Add to your agent's knowledge base

 
If your agent makes some common mistakes, it's a great time to codify your feedback in the agent's knowledge base. In Devin, there is a dedicated knowledge management system. Many products offer .rules files, .md files for the agent to permanently ingest. Don't just give it guidelines on the framework you're using, but also tell it about the overall architecture of your project. Tell it what type of testing is common for different kinds of tasks, how to run important commands and which tools you recommend using.

 
 
#### Example:

 
We give our agent knowledge about the specific procedure it should follow when adding a new service route. The information includes every place it needs to add boilerplate in the frontend and backend. As a result, these tasks are now easily delegated to our AI.

 
 

 
 
Practical Considerations

 
## Limitations of Autonomous Agents

 
 
 
### Limited debugging skills

 
Bugs reports can be deceptively simple. But many bugs often require not only access to databases and logs, but also a level of debugging that is greater than most AI agents today. If using AI to aid in debugging, we recommend asking for a list of probable root causes rather than trying to debug and fix everything itself. Then, a human can decide based on their own experience which one is the real root cause. But once the cause is known, agents can still be quite helpful at implementing the fix.

 
 
 
### Poor fine-grained visual reasoning

 
Generally models today don't have great visual reasoning capabilities at the level of details needed to match screenshots of designs or Figma mockups. They are most reliable on visuals that can be described at the level of code (ex. giving it code from Figma). If you want it to match your visual style, you should use a good design system with reusable components.

 
 
 
### Knowledge Cutoffs

 
Whenever you want to work with a new library, you should explicitly point it to the latest docs. Otherwise, most agents will assume the old patterns from these libraries due to knowledge cutoffs in the pretrained base models. A good agent can overcome this if you point it to docs, but you must be mindful of this (remember, the agent doesn't even know that there are new versions of these libraries).

 

 
 
Practical Considerations

 
## Managing Time and Minimizing Losses

 
Not all times you use an agent will result in success. In 2025, there is some real variance in the outcomes of these agents. Part of the job involves learning how to use agents in such a way to maximize the chance of running into successful outcomes while minimizing wasted time and tokens.

 
 
 
### Be willing to cut your losses earlier

 
A common mistake for people who are new to using agents is that they commit to making an interaction successful, even when an agent's work is veering off track. If you ever find yourself thinking "it's ignoring my instructions" or "this thing is going in circles", you should be ok discontinuing that conversation or manually taking over. Sending more messages is more likely a sign of the inherent complexity of your task being higher than the agent's capabilities rather than some simple mistake that can be corrected.

 
 
 
### Diversifying your experiments

 
If you're new to working with agents, we recommend diversifying your bets at the start. Try a range of different prompts and ideas. Double down on the types of tasks you see the agents naturally performing well on - and cut your losses on the ones they don't. Don't feel a need to force your agents to find success every time.

 
 
 
### Start fresh when you aren't making progress

 
Starting over is the right answer a lot more often with agents than with humans. If you've given an agent a task and it is struggling to address feedback or correct course, starting fresh with a new agent and all of the instructions up front can often get to success much faster. The ability of an agent to correct a messed-up environment is much worse than its ability to spit out fresh code from scratch.

 

 
 
Practical Considerations

 
## Security and Permissioning

 
 
 
### Create accounts for your agent

 
A throwaway email is helpful for safe testing of sites. Create custom IAM roles for your agent if it needs to access cloud resources.

 
### Give it a development / staging environment

 
Ideally the agent uses the same testing setup as the engineers on your team. We suggest avoiding giving access to production services entirely. When using remote agents, you can run fully isolated test environments on the agent's remote machine.

 
 
 
### Readonly API keys

 
Where possible, give it readonly access. We find it is still helpful for humans to manually run any script that interacts with outside services.

 

 
 
Practical Considerations

 
## Big Changes Ahead

 
We firmly believe that software engineers aren't going anywhere. Even as coding agents become smarter and more capable, deep technical expertise and intimate knowledge of your codebase remain invaluable. True ownership of your projects, your systems, and your code is more critical now than ever. On our team today, engineers are expected to oversee multiple systems while still maintaining deep understanding and thoughtful judgment. As automation amplifies your impact, the ability to juggle parallel tasks won't just become possible; It'll become essential. We're excited to share the insights we've gathered while preparing our own organization for this shift, so you and your team can also thrive in the evolving world of software development.