# How do you structure guidelines to keep them maintainable as they grow?

When your agent starts handling more complex situations, guideline organization becomes crucial. Think of it like maintaining a large codebase - without proper structure, it can quickly become unmanageable.

The key is to make each guideline focused and specific rather than trying to handle multiple scenarios in one. Instead of a complex guideline that tries to handle all aspects of refund processing, you might have several smaller guidelines: one for determining refund eligibility, another for explaining policies, and a third for processing the actual refund.

This modular, decoupled approach makes it easier to review, update, and debug guidelines. When something needs to change, you can modify the specific guideline that handles that behavior without worrying about unintended effects on other parts of your agent's behavior.
