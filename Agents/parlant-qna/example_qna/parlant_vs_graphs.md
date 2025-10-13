# How do you handle complex decision trees in Parlant compared to graph-based frameworks?

# "How does Parlant manage complex conversation flows?"

# "Do I need to map out all possible conversation paths in Parlant?"

Traditional graph-based frameworks, such as LangGraph, require you to explicitly map out conversation flows, creating decision trees that cover every possible path a conversation might take. This becomes exponentially complex as your agent's capabilities grow, often resulting in rigid, hard-to-maintain systems.

Parlant approaches this challenge differently. Instead of pre-defining conversation paths, you define guidelines about how your agent should handle different situations. The engine then dynamically determines which guidelines apply based on the current context and any information it discovers along the way.

Consider a technical support scenario. In a graph-based system, you might need to create branches for every possible combination of user problems, account types, and support tiers. With Parlant, you instead define guidelines like "verify account status first" or "check recent support tickets before suggesting solutions." The agent can then navigate complex situations naturally while still following your business rules. This creates more flexible conversations while actually being easier to maintain and update.
