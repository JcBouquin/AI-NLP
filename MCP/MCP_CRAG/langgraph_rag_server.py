#!/usr/bin/env python3
"""
Serveur MCP pour intégrer LangGraph RAG avec Claude Desktop - Version moderne avec @mcp.tools
"""

import asyncio
import os
from typing import Any, Dict, List, Optional
import mcp
from mcp import types

# Imports LangGraph et LangChain
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langgraph.graph import END, StateGraph, START
from typing_extensions import TypedDict

class GraphState(TypedDict):
    question: str
    generation: str
    web_search: str
    documents: List[Document]

class LangGraphRAGServer:
    def __init__(self):
        self.app = None
        self.vectorstore = None
        self.retriever = None
        self.rag_chain = None
        self.retrieval_grader = None
        self.question_rewriter = None
        self.web_search_tool = None
        self.data_loaded = False
        
        # Initialiser les composants
        self.setup_data_and_components()
        self.setup_workflow()
    
    def setup_data_and_components(self):
        """Initialise les données et les composants RAG"""
        print("🔄 Initialisation des données RAG...")
        
        # 1. Chargement et traitement des documents
        urls = [
            "https://lilianweng.github.io/posts/2023-06-23-agent/",
            "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
            "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
        ]
        
        docs = [WebBaseLoader(url).load() for url in urls]
        docs_list = [item for sublist in docs for item in sublist]
        
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=250, chunk_overlap=0
        )
        doc_splits = text_splitter.split_documents(docs_list)
        
        # 2. Création de la base vectorielle
        self.vectorstore = Chroma.from_documents(
            documents=doc_splits,
            collection_name="rag-chroma",
            embedding=OpenAIEmbeddings(),
        )
        self.retriever = self.vectorstore.as_retriever()
        
        # 3. Configuration du grader de documents
        class GradeDocuments(BaseModel):
            binary_score: str = Field(
                description="Documents are relevant to the question, 'yes' or 'no'"
            )
        # Initialiser le LLM avec gestion sécurisée de la clé API
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
                # ⚠️ À remplacer par une variable d'environnement en production
                print("⚠️ ATTENTION: Utilisez une variable d'environnement pour la clé API en production")
                api_key = "sk-proj-0xUZ6aBpi14Q FwAy9HhFfHS_cUMhXQMX6_U0pycw_XiZUUtZ4V6Gc5xEwhMZOsYA6xKN4HruNnPRcA"

        llm_grader = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0,
                api_key=api_key
        )
        structured_llm_grader = llm_grader.with_structured_output(GradeDocuments)
        
        grade_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a grader assessing relevance of a retrieved document to a user question.
            If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant.
            Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""),
            ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
        ])
        
        self.retrieval_grader = grade_prompt | structured_llm_grader
        
        # 4. Configuration de la chaîne RAG
        prompt = hub.pull("rlm/rag-prompt")
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        self.rag_chain = prompt | llm | StrOutputParser()
        
        # 5. Configuration du rewriter de questions
        llm_rewriter = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
        re_write_prompt = ChatPromptTemplate.from_messages([
            ("system", """You a question re-writer that converts an input question to a better version that is optimized
            for web search. Look at the input and try to reason about the underlying semantic intent / meaning."""),
            ("human", "Here is the initial question: \n\n {question} \n Formulate an improved question."),
        ])
        
        self.question_rewriter = re_write_prompt | llm_rewriter | StrOutputParser()
        
        # 6. Configuration de l'outil de recherche web
        self.web_search_tool = TavilySearchResults(k=3)
        
        self.data_loaded = True
        print("✅ Composants RAG initialisés avec succès")
    
    def setup_workflow(self):
        """Configure le workflow LangGraph"""
        workflow = StateGraph(GraphState)
        
        # Ajouter les nœuds
        workflow.add_node("retrieve", self.retrieve)
        workflow.add_node("grade_documents", self.grade_documents)
        workflow.add_node("generate", self.generate)
        workflow.add_node("transform_query", self.transform_query)
        workflow.add_node("web_search_node", self.web_search)
        
        # Construire le graphe
        workflow.add_edge(START, "retrieve")
        workflow.add_edge("retrieve", "grade_documents")
        workflow.add_conditional_edges(
            "grade_documents",
            self.decide_to_generate,
            {
                "transform_query": "transform_query",
                "generate": "generate",
            },
        )
        workflow.add_edge("transform_query", "web_search_node")
        workflow.add_edge("web_search_node", "generate")
        workflow.add_edge("generate", END)
        
        # Compiler
        self.app = workflow.compile()
    
    async def query_rag(self, question: str) -> Dict[str, Any]:
        """Execute le workflow RAG pour une question"""
        try:
            initial_state = {
                "question": question,
                "generation": "",
                "web_search": "No",
                "documents": []
            }
            
            # Exécuter le workflow
            result = await self.app.ainvoke(initial_state)
            
            return {
                "success": True,
                "question": result["question"],
                "answer": result["generation"],
                "documents_used": len(result["documents"]),
                "web_search_used": result.get("web_search", "No") == "Yes"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "question": question
            }
    
    # Fonctions de nœuds LangGraph
    def retrieve(self, state):
        """Retrieve documents"""
        print("---RETRIEVE---")
        question = state["question"]
        documents = self.retriever.get_relevant_documents(question)
        return {"documents": documents, "question": question}
    
    def generate(self, state):
        """Generate answer"""
        print("---GENERATE---")
        question = state["question"]
        documents = state["documents"]
        generation = self.rag_chain.invoke({"context": documents, "question": question})
        return {"documents": documents, "question": question, "generation": generation}
    
    def grade_documents(self, state):
        """Determines whether the retrieved documents are relevant to the question."""
        print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
        question = state["question"]
        documents = state["documents"]
        
        filtered_docs = []
        web_search = "No"
        for d in documents:
            score = self.retrieval_grader.invoke(
                {"question": question, "document": d.page_content}
            )
            grade = score.binary_score
            if grade == "yes":
                print("---GRADE: DOCUMENT RELEVANT---")
                filtered_docs.append(d)
            else:
                print("---GRADE: DOCUMENT NOT RELEVANT---")
                web_search = "Yes"
                continue
        return {"documents": filtered_docs, "question": question, "web_search": web_search}
    
    def transform_query(self, state):
        """Transform the query to produce a better question."""
        print("---TRANSFORM QUERY---")
        question = state["question"]
        documents = state["documents"]
        better_question = self.question_rewriter.invoke({"question": question})
        return {"documents": documents, "question": better_question}
    
    def web_search(self, state):
        """Web search based on the question"""
        print("---WEB SEARCH---")
        question = state["question"]
        documents = state.get("documents", [])
        
        try:
            docs = self.web_search_tool.invoke({"query": question})
            
            if isinstance(docs, list):
                content_list = []
                for d in docs:
                    if isinstance(d, dict) and "content" in d:
                        content_list.append(d["content"])
                    elif isinstance(d, str):
                        content_list.append(d)
                
                if content_list:
                    web_results = Document(page_content="\n".join(content_list))
                    documents.append(web_results)
            elif isinstance(docs, str):
                web_results = Document(page_content=docs)
                documents.append(web_results)
            else:
                web_results = Document(page_content=str(docs))
                documents.append(web_results)
            
            print(f"Added documents from web search")
            
        except Exception as e:
            print(f"Error during web search: {str(e)}")
            error_doc = Document(page_content=f"Web search error: {str(e)}")
            documents.append(error_doc)
        
        return {"documents": documents}
    
    def decide_to_generate(self, state):
        """Determines whether to generate an answer, or re-generate a question."""
        print("---ASSESS GRADED DOCUMENTS---")
        web_search = state["web_search"]
        
        if web_search == "Yes":
            print("---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---")
            return "transform_query"
        else:
            print("---DECISION: GENERATE---")
            return "generate"

# Initialiser le serveur RAG
rag_server = LangGraphRAGServer()

# Définition des outils avec @mcp.tools
@mcp.tools
async def query_rag_system(question: str) -> str:
    """
    Execute une requête RAG en utilisant LangGraph avec recherche adaptative.
    
    Args:
        question: La question à poser au système RAG
    
    Returns:
        La réponse générée par le système RAG avec les détails d'exécution
    """
    result = await rag_server.query_rag(question)
    
    if result["success"]:
        response = f"""**Réponse RAG:** {result['answer']}

**Détails de l'exécution:**
- Question traitée: {result['question']}
- Documents utilisés: {result['documents_used']}
- Recherche web activée: {'Oui' if result['web_search_used'] else 'Non'}"""
    else:
        response = f"**Erreur lors de l'exécution RAG:**\n{result['error']}"
    
    return response

@mcp.tools
async def get_rag_status() -> str:
    """
    Obtient le statut du système RAG.
    
    Returns:
        Le statut actuel du système RAG
    """
    if rag_server.app and rag_server.data_loaded:
        return "✅ Système RAG LangGraph opérationnel et données chargées"
    elif rag_server.app:
        return "⚠️ Système RAG initialisé mais données non chargées"
    else:
        return "❌ Système RAG non initialisé"

@mcp.tools
async def reload_rag_data(urls: Optional[List[str]] = None) -> str:
    """
    Recharge les données RAG depuis les sources.
    
    Args:
        urls: URLs optionnelles à charger (utilise les URLs par défaut si non spécifié)
    
    Returns:
        Statut du rechargement des données
    """
    try:
        if urls:
            # TODO: Implémenter le rechargement avec URLs personnalisées
            pass
        
        # Pour l'instant, on recharge avec les données par défaut
        rag_server.setup_data_and_components()
        return "✅ Données RAG rechargées avec succès"
    except Exception as e:
        return f"❌ Erreur lors du rechargement: {str(e)}"

# Point d'entrée principal
async def main():
    async with mcp.stdio_server() as server:
        await server.run()

if __name__ == "__main__":
    asyncio.run(main())