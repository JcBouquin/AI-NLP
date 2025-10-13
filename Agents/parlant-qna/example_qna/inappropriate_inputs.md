# How do you handle inappropriate user interactions and prevent jailbreaks?

When deploying customer-facing AI agents, we need to consider two distinct types of challenging interactions. First, there are users who might behave inappropriately – using hostile language, making inappropriate requests, raising sensitive issues, or attempting to manipulate the agent. Second, there are those who specifically try to "jailbreak" the agent – attempting to expose its underlying instructions or make it behave contrary to its guidelines.

Understanding the technical challenge here is crucial. LLMs are fundamentally pattern-matching systems that can be influenced by the nature of inputs they receive. When a user engages aggressively or attempts manipulation, they're essentially trying to push the model into different behavioral patterns. This isn't just about maintaining decorum – inappropriate interactions can actually affect how the model generates subsequent responses, even with other users.

Parlant addresses this through a multi-layered approach. The first layer involves pre-processing filters that catch obviously inappropriate content before it reaches the agent. We integrate with services like OpenAI's moderation API to identify and filter out harmful content immediately.

The system also includes specific protections against common jailbreak attempts. When users try techniques like "ignore previous instructions" or "let's play a game where you pretend to be unrestricted," Parlant's engine recognizes these patterns and ensures that core behavioral guidelines remain in effect.

It's important to note that these protections aren't about security in the traditional sense – that should always be handled at the infrastructure level through proper authentication, authorization, and API security measures. Instead, this is about maintaining consistent, appropriate agent behavior even in the face of challenging interactions.
