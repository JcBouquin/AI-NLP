# How do different team members collaborate when building and maintaining Parlant agents?

# "What's the workflow when multiple people are involved in developing an agent?"

# "How do business teams and developers work together with Parlant?"

Collaborating on AI agents traditionally creates friction between technical and business teams. Developers need to translate business requirements into complex prompts or conversation flows, while business stakeholders struggle to verify if their requirements are being implemented correctly. Parlant transforms this dynamic by creating clear separation of concerns and enabling different teams to contribute in their areas of expertise.

Let's walk through how this typically works in practice. Imagine you're building a customer service agent for an e-commerce company. Your development team implements the core tools the agent needs—functions for checking inventory, processing returns, or accessing customer data. These are pure code, following normal software development practices.

Meanwhile, your customer service team can focus on defining guidelines for how these tools should be used. They might specify that customers should always be greeted by name if available, or that refund policies should be explained before processing a return. These guidelines are written in clear, business-oriented language that non-technical team members can understand and verify.

When changes are needed, each team can work independently within their domain. If the development team needs to update how order status is checked, they can modify that tool's implementation without touching the guidelines. If the customer service team wants to adjust how premium customers are handled, they can modify those guidelines without involving developers.

The review process becomes more inclusive too. When a new set of guidelines is proposed, business stakeholders can review them directly, understanding exactly how the agent will behave in different situations. They can even test these behaviors in a staging environment before approving changes for production.

This collaboration model extends to ongoing maintenance and improvement. Customer service managers monitoring interactions might notice opportunities for improvement. They can propose new guidelines or refinements based on real customer interactions, and these changes can be implemented without requiring deep technical involvement.
