# LangGraph  

This directory demonstrates the fundamentals of LangGraph framework for building structured conversations and workflows with Language Models.

## 🔄 Core Concepts
- State Management with TypedDict
- Graph-based workflow control
- Sequential processing pipelines
- Interactive chat systems
## RAG in LangGraph 

Concepts in LangGraph
RAG (Retrieval-Augmented Generation)
Definition: RAG is a technique that combines text generation by language models with the retrieval of relevant documents from external sources. This allows for more accurate and contextual responses by using up-to-date information.

Agentic RAG
Definition: Agentic RAG uses AI agents to enhance the capabilities of traditional RAG systems. These agents can decide when and how to retrieve additional information, rewrite queries for better searches, and integrate real-time data to provide more accurate responses.

CRAG (Corrective Retrieval-Augmented Generation)
Definition: CRAG is an improved version of RAG that includes steps for verifying and correcting retrieved documents before generating responses. This ensures that the information used is relevant and accurate, reducing errors and misleading information.

Self-RAG (Self-Reflective Retrieval-Augmented Generation)
Definition: Self-RAG is an approach where the language model uses reflective mechanisms to evaluate and correct retrieved information. This includes steps for query rewriting and adaptive retrieval to improve the relevance and accuracy of generated responses.

## 📚 Examples Included
### Basic Implementations
- State Graph Creation
- Data Filtering Workflows
- Chat Response Management
- Custom Node Implementation

### Use Cases
- Movies Filtering System
- Sales Data Analysis
- Interactive Chat Flows
- State-based Data Processing

## 🛠️ Requirements
```bash
langgraph
langchain
```

## 📋 Contents
- `LangGrph-basics.ipynb`: Step-by-step tutorial and examples
- Core implementation patterns
- Practical workflow examples

## 🎯 Features Demonstrated
- Graph-based Flow Control
- State Management
- Data Processing Pipelines
- Error Handling
- Custom Node Creation

## 💡 Key Concepts
- StateGraph Implementation
- Node Configuration
- Edge Definition
- State Management
- Workflow Control

## 📝 Note
These examples serve as a foundation for understanding LangGraph's capabilities in building structured LLM applications.
