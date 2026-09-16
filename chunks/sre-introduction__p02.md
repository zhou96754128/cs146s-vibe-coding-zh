 
Despite these net gains, the SRE model is characterized by its own distinct set of challenges. One continual challenge Google faces is hiring SREs: not only does SRE compete for the same candidates as the product development hiring pipeline, but the fact that we set the hiring bar so high in terms of both coding and system engineering skills means that our hiring pool is necessarily small. As our discipline is relatively new and unique, not much industry information exists on how to build and manage an SRE team (although hopefully this book will make strides in that direction!). And once an SRE team is in place, their potentially unorthodox approaches to service management require strong management support. For example, the decision to stop releases for the remainder of the quarter once an error budget is depleted might not be embraced by a product development team unless mandated by their management.

 
 
 
 
# Tenets of SRE

 
While the nuances of workflows, priorities, and day-to-day operations vary from SRE team to SRE team, all share a set of basic responsibilities for the service(s) they support, and adhere to the same core tenets. In general, an SRE team is responsible for the availability, latency, performance, efficiency, change management, monitoring, emergency response, and capacity planning of their service(s). We have codified rules of engagement and principles for how SRE teams interact with their environmentânot only the production environment, but also the product development teams, the testing teams, the users, and so on. Those rules and work practices help us to maintain our focus on engineering work, as opposed to operations work.

 
The following section discusses each of the core tenets of Google SRE.

 
 
## Ensuring a Durable Focus on Engineering

 
As already discussed, Google caps operational work for SREs at 50% of their time. Their remaining time should be spent using their coding skills on project work. In practice, this is accomplished by monitoring the amount of operational work being done by SREs, and redirecting excess operational work to the product development teams: reassigning bugs and tickets to development managers, [re]integrating developers into on-call pager rotations, and so on. The redirection ends when the operational load drops back to 50% or lower. This also provides an effective feedback mechanism, guiding developers to build systems that donât need manual intervention. This approach works well when the entire organizationâSRE and development alikeâunderstands why the safety valve mechanism exists, and supports the goal of having no overflow events because the product doesnât generate enough operational load to require it.

 
When they are focused on operations work, on average, SREs should receive a maximum of two events per 8â12-hour on-call shift. This target volume gives the on-call engineer enough time to handle the event accurately and quickly, clean up and restore normal service, and then conduct a postmortem. If more than two events occur regularly per on-call shift, problems canât be investigated thoroughly and engineers are sufficiently overwhelmed to prevent them from learning from these events. A scenario of pager fatigue also wonât improve with scale. Conversely, if on-call SREs consistently receive fewer than one event per shift, keeping them on point is a waste of their time.

 
Postmortems should be written for all significant incidents, regardless of whether or not they paged; postmortems that did not trigger a page are even more valuable, as they likely point to clear monitoring gaps. This investigation should establish what happened in detail, find all root causes of the event, and assign actions to correct the problem or improve how it is addressed next time. Google operates under a blame-free postmortem culture, with the goal of exposing faults and applying engineering to fix these faults, rather than avoiding or minimizing them.

 
 
 
## Pursuing Maximum Change Velocity Without Violating a Serviceâs SLO

 
Product development and SRE teams can enjoy a productive working relationship by eliminating the structural conflict in their respective goals. The structural conflict is between pace of innovation and product stability, and as described earlier, this conflict often is expressed indirectly. In SRE we bring this conflict to the fore, and then resolve it with the introduction of an error budget.

 
The error budget stems from the observation that 100% is the wrong reliability target for basically everything (pacemakers and anti-lock brakes being notable exceptions). In general, for any software service or system, 100% is not the right reliability target because no user can tell the difference between a system being 100% available and 99.999% available. There are many other systems in the path between user and service (their laptop, their home WiFi, their ISP, the power gridâ¦) and those systems collectively are far less than 99.999% available. Thus, the marginal difference between 99.999% and 100% gets lost in the noise of other unavailability, and the user receives no benefit from the enormous effort required to add that last 0.001% of availability.

 
If 100% is the wrong reliability target for a system, what, then, is the right reliability target for the system? This actually isnât a technical question at allâitâs a product question, which should take the following considerations into account:

 
 - What level of availability will the users be happy with, given how they use the product?

 - What alternatives are available to users who are dissatisfied with the productâs availability?

 - What happens to usersâ usage of the product at different availability levels?

 
 
The business or the product must establish the systemâs availability target. Once that target is established, the error budget is one minus the availability target. A service thatâs 99.99% available is 0.01% unavailable. That permitted 0.01% unavailability is the serviceâs error budget. We can spend the budget on anything we want, as long as we donât overspend it.

 
So how do we want to spend the error budget? The development team wants to launch features and attract new users. Ideally, we would spend all of our error budget taking risks with things we launch in order to launch them quickly. This basic premise describes the whole model of error budgets. As soon as SRE activities are conceptualized in this framework, freeing up the error budget through tactics such as phased rollouts and 1% experiments can optimize for quicker launches.

 
The use of an error budget resolves the structural conflict of incentives between development and SRE. SREâs goal is no longer "zero outages"; rather, SREs and product developers aim to spend the error budget getting maximum feature velocity. This change makes all the difference. An outage is no longer a "bad" thingâit is an expected part of the process of innovation, and an occurrence that both development and SRE teams manage rather than fear.

 
 
 
## Monitoring

 
Monitoring is one of the primary means by which service owners keep track of a systemâs health and availability. As such, monitoring strategy should be constructed thoughtfully. A classic and common approach to monitoring is to watch for a specific value or condition, and then to trigger an email alert when that value is exceeded or that condition occurs. However, this type of email alerting is not an effective solution: a system that requires a human to read an email and decide whether or not some type of action needs to be taken in response is fundamentally flawed. Monitoring should never require a human to interpret any part of the alerting domain. Instead, software should do the interpreting, and humans should be notified only when they need to take action.

 
There are three kinds of valid monitoring output:

 
 Alerts 
 Signify that a human needs to take action immediately in response to something that is either happening or about to happen, in order to improve the situation. 
 Tickets 
 Signify that a human needs to take action, but not immediately. The system cannot automatically handle the situation, but if a human takes action in a few days, no damage will result. 
 Logging 
 No one needs to look at this information, but it is recorded for diagnostic or forensic purposes. The expectation is that no one reads logs unless something else prompts them to do so. 
 
 
 
 
## Emergency Response

 
Reliability is a function of mean time to failure (MTTF) and mean time to repair (MTTR) [Sch15]. The most relevant metric in evaluating the effectiveness of emergency response is how quickly the response team can bring the system back to healthâthat is, the MTTR.

 
Humans add latency. Even if a given system experiences more actual failures, a system that can avoid emergencies that require human intervention will have higher availability than a system that requires hands-on intervention. When humans are necessary, we have found that thinking through and recording the best practices ahead of time in a "playbook" produces roughly a 3x improvement in MTTR as compared to the strategy of "winging it." The hero jack-of-all-trades on-call engineer does work, but the practiced on-call engineer armed with a playbook works much better. While no playbook, no matter how comprehensive it may be, is a substitute for smart engineers able to think on the fly, clear and thorough troubleshooting steps and tips are valuable when responding to a high-stakes or time-sensitive page. Thus, Google SRE relies on on-call playbooks, in addition to exercises such as the "Wheel of Misfortune,"7 to prepare engineers to react to on-call events.

 
 
 
## Change Management

 
SRE has found that roughly 70% of outages are due to changes in a live system. Best practices in this domain use automation to accomplish the following:

 
 - Implementing progressive rollouts

 - Quickly and accurately detecting problems

 - Rolling back changes safely when problems arise

 
 
This trio of practices effectively minimizes the aggregate number of users and operations exposed to bad changes. By removing humans from the loop, these practices avoid the normal problems of fatigue, familiarity/contempt, and inattention to highly repetitive tasks. As a result, both release velocity and safety increase.

 
 
 
## Demand Forecasting and Capacity Planning

 
Demand forecasting and capacity planning can be viewed as ensuring that there is sufficient capacity and redundancy to serve projected future demand with the required availability. Thereâs nothing particularly special about these concepts, except that a surprising number of services and teams donât take the steps necessary to ensure that the required capacity is in place by the time it is needed. Capacity planning should take both organic growth (which stems from natural product adoption and usage by customers) and inorganic growth (which results from events like feature launches, marketing campaigns, or other business-driven changes) into account.

 
Several steps are mandatory in capacity planning:

 
 - An accurate organic demand forecast, which extends beyond the lead time required for acquiring capacity

 - An accurate incorporation of inorganic demand sources into the demand forecast

 - Regular load testing of the system to correlate raw capacity(servers, disks, and so on) to service capacity

 
 
Because capacity is critical to availability, it naturally follows that the SRE team must be in charge of capacity planning, which means they also must be in charge of provisioning.

 
 
 
## Provisioning