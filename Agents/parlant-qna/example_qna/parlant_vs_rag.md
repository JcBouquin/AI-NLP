# How does Parlant handle conversations differently from frameworks like LlamaIndex or similar RAG solutions?

# "What's the difference between Parlant's approach and typical RAG implementation?"

# "How does Parlant compare to document-retrieval based agents?"

Traditional RAG frameworks like LlamaIndex focus primarily on helping your agent find and use relevant information from your documents. While this is valuable, it addresses only part of the challenge of building reliable agents. Think of it like giving someone access to a great library—they can find information, but that doesn't ensure they'll use it appropriately.

Parlant takes a fundamentally different approach. Instead of just focusing on information retrieval, it actively manages how your agent uses any information it has access to. When your agent retrieves information—whether from documents, APIs, or databases—Parlant's engine evaluates this information against your guidelines to determine how it should be used.

For example, imagine a customer asking about product features. A typical RAG implementation would find relevant product documentation and generate a response based on it. Parlant goes further: it might find the same documentation, but then apply guidelines about how to approach the topic of premium features with free-tier customers, and ensure the response follows your specific communication protocols.
