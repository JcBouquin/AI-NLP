# How is building an agent in Parlant different from using LangChain?

# "If I'm already using LangChain, why would I switch to Parlant?"

# "What can Parlant do that LangChain can't?"

The fundamental difference lies in how these frameworks approach agent behavior. LangChain focuses on chaining together low-level LLM requests—you create sequences of steps like "first search this document, then summarize the results, then generate a response." While this is powerful for building complex processing workflows, this rigid approach is creates mechanical, unnatural conversation experiences for customer-facing scenarios.

Let's use a real example. Imagine you're building a support agent that needs to handle refund requests. In LangChain, you might create a chain that checks order status, retrieves refund policies, and generates a response. But ensuring the agent consistently applies your refund rules becomes increasingly complex as you add more conditions and edge cases. You end up building elaborate chains trying to account for every possible scenario.

Parlant approaches this differently. Instead of creating chains of operations, you refine the agent's behavior iteratively through pinpointed guidelines on how to handle different situations and circumstances. Parlant's structured guidance system is prebaked with a number of practical features, allowing you to easily tailor the behavior to specific customers, and to have the agents handle edge-cases reliably and consistently according to your instructions.
