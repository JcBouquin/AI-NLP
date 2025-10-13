# What makes Parlant different from just using OpenAI's API with function calling?

# "Why not just use function calling with GPT-4?"

# "What does Parlant add on top of basic LLM APIs?"

Regarding function calling, when you use OpenAI's API directly with function calling, you're essentially hoping the model will understand when and how to use your functions correctly based on your prompt. While you can get good results in simple scenarios, this approach leaves too much room for interpretation in practices, and thus faces several fundamental challenges as your agent's responsibilities grow.

Consider what happens when you need your agent to follow complex business rules. With direct API usage, while you might include these rules in your system prompt, there's no mechanism to ensure the model actually follows them. The model might understand your rules perfectly but still choose to ignore them if it deems another response more helpful.

Parlant solves this by implementing an active control layer between your business logic and the LLM. Instead of hoping the model calls your functions appropriately, Parlant's engine actively manages when and how functions are called based on your guidelines. Using guidelines, you can even adjust the agent's behavior based on what it learns from each function call's output—something that would require complex prompt engineering and multiple API calls to achieve with direct API usage.
