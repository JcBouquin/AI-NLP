# How do you handle sensitive business logic across guidelines?

Think of it like separation of concerns in software development. Your secure business logic lives in your own infrastructure, accessed through tools you control. Guidelines then specify the circumstances under which these tools should be used and how their results should be interpreted.

For example, if you're building a banking agent, instead of putting credit assessment rules in guidelines, you might have a guideline that says "Before discussing loan options, check customer eligibility through the credit assessment tool." The actual credit assessment logic remains in your secure systems, while the guideline manages when and how to use this information.
