# What's the typical development workflow when building an agent with Parlant?

# "How do I go from idea to deployed agent with Parlant?"

# "What's the step-by-step process for developing a Parlant agent?"

Building an agent with Parlant is designed to follow a natural progression that aligns with how organizations typically develop and refine their customer service processes. Let's walk through the typical workflow.

You begin by implementing your core business tools—these are the functions your agent needs to accomplish its tasks. For example, if you're building a customer service agent, you might create tools for checking order status, processing returns, or accessing customer information. These tools are just regular API calls or functions that encapsulate your business logic.

Once your tools are in place, you start with a basic set of guidelines that define fundamental behaviors. Think of this like training a new customer service representative on the essential protocols. You might begin with guidelines about how to greet customers, when to check their account status, or how to handle basic inquiries.

The key difference from traditional development becomes apparent in the testing phase. Instead of having to predict and script out every possible conversation flow, you can start with a minimal set of guidelines and observe how your agent handles real interactions. When you notice situations where the agent's behavior could be improved, you simply add or refine guidelines to address these specific cases.

This creates a highly iterative development process. You might deploy your agent to a test environment, observe its interactions, and continuously refine its behavior through new or updated guidelines. Because changes take effect immediately and can be tested in isolation, you can rapidly iterate based on feedback from stakeholders or actual usage patterns.
