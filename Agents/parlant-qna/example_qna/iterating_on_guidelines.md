# How do you manage guidelines across different environments (development, staging, production)?

# "What's the best practice for testing guideline changes before production?"

# "How do you handle guideline versioning in Parlant?"

Parlant treats guidelines as code, which means you can use familiar development practices for managing them. Your guidelines are stored as JSON files, allowing you to use standard version control tools like Git to track changes, create branches for new features, and manage deployments across environments.

A typical workflow might look like this: When developing new functionality, you create a branch in your repository and add or modify guidelines in your development environment. You can test these changes using Parlant's built-in chat interface, which lets you simulate conversations and verify that your guidelines produce the expected behavior.

Once you're satisfied with the changes in development, you can create a pull request to promote these changes to staging. Other team members can review the guideline changes just like they would review code changes. This is particularly valuable because it allows business stakeholders to verify that the guidelines accurately reflect their requirements before they reach production.

The JSON format of guidelines makes it easy to diff changes and understand exactly what's being modified. You can see which conditions are being added or updated, making it easier to reason about the impact of changes before they're deployed.
