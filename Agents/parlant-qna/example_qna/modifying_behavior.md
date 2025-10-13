# How does updating agent behavior differ in Parlant versus other frameworks?

# "How do I modify my agent's responses once it's deployed?"

# "What's involved in changing how my agent handles specific situations?"

In most frameworks, modifying agent behavior often requires changing prompts, updating training data, or revising conversation flows. These changes can have unpredictable effects because it's hard to ensure new instructions don't conflict with existing ones.

Parlant's approach is more systematic. When you want to change how your agent handles a situation, you modify or add specific guidelines. The engine automatically checks these changes for conflicts with existing guidelines before applying them. More importantly, because message generation in Parlant evaluates and selects relevant guidelines dynamically, you gets clear insights into why your agent made specific decisions, and adjust the configuration accordingly.

For example, if you notice your agent isn't being empathetic enough with frustrated customers, you don't need to modify a complex conversation tree or retrain a model. You can add a guideline about detecting customer frustration and specifying how to respond. Parlant will then automatically incorporate this guideline whenever it detects the relevant conditions, while also maintaining all other aspects of your agent's behavior.
