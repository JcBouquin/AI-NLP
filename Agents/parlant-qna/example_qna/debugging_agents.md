# How do you debug when your agent isn't behaving as expected?

Debugging AI agent behavior has traditionally been challenging because it's hard to understand why an agent made specific decisions. Parlant addresses this by making the decision-making process transparent and traceable.

When your agent generates a response, Parlant records which guidelines were considered, how the agent interpreted them in-context, which ones were deemed relevant, and how they influenced the final response. This creates a clear trail you can follow to understand exactly why your agent behaved in a certain way.

For example, if your agent unexpectedly declines a refund request, you can trace its decision-making process: Did it check the order date? Which guidelines about refund eligibility were activated? Did any conflicting guidelines come into play? This visibility makes it much easier to identify whether the issue is with the guidelines themselves or with how they're being applied.

The debugging process becomes similar to debugging regular code - you can set up test cases, examine the decision flow, and identify exactly where behavior diverges from your expectations. This makes it possible to fix issues systematically rather than through haphazard trial and error.
