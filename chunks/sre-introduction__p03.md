 
Provisioning combines both change management and capacity planning. In our experience, provisioning must be conducted quickly and only when necessary, as capacity is expensive. This exercise must also be done correctly or capacity doesnât work when needed. Adding new capacity often involves spinning up a new instance or location, making significant modification to existing systems (configuration files, load balancers, networking), and validating that the new capacity performs and delivers correct results. Thus, it is a riskier operation than load shifting, which is often done multiple times per hour, and must be treated with a corresponding degree of extra caution.

 
 
 
## Efficiency and Performance

 
Efficient use of resources is important any time a service cares about money. Because SRE ultimately controls provisioning, it must also be involved in any work on utilization, as utilization is a function of how a given service works and how it is provisioned. It follows that paying close attention to the provisioning strategy for a service, and therefore its utilization, provides a very, very big lever on the serviceâs total costs.

 
Resource use is a function of demand (load), capacity, and software efficiency. SREs predict demand, provision capacity, and can modify the software. These three factors are a large part (though not the entirety) of a serviceâs efficiency.

 
Software systems become slower as load is added to them. A slowdown in a service equates to a loss of capacity. At some point, a slowing system stops serving, which corresponds to infinite slowness. SREs provision to meet a capacity target at a specific response speed, and thus are keenly interested in a serviceâs performance. SREs and product developers will (and should) monitor and modify a service to improve its performance, thus adding capacity and improving efficiency.8

 
 
 
 
# The End of the Beginning

 
Site Reliability Engineering represents a significant break from existing industry best practices for managing large, complicated services. Motivated originally by familiarityâ"as a software engineer, this is how I would want to invest my time to accomplish a set of repetitive tasks"âit has become much more: a set of principles, a set of practices, a set of incentives, and a field of endeavor within the larger software engineering discipline. The rest of the book explores the SRE Way in detail.

 
 
6Vice President, Google Engineering, founder of Google SRE

7See Disaster Role Playing.

8For further discussion of how this collaboration can work in practice, see Communications: Production Meetings.
 
 
 
 

 
 
 
 
 
Previous

 
Part I - Introduction

 
 
 
 
 
Next

 
Chapter 2 - The Production Environment at Google, from the Viewpoint of an SRE

 
 
 
Copyright Â© 2017 Google, Inc. Published by O'Reilly Media, Inc. Licensed under CC BY-NC-ND 4.0