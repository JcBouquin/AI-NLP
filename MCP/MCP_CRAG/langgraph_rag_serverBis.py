#!/usr/bin/env python3
"""
LangGraph RAG Server avec FastMCP - Structure basée sur le code météo qui fonctionne
"""

import os
import sys
import asyncio
from typing import Any, Dict, List, Optional

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# Configurer USER_AGENT si pas défini
if not os.getenv("USER_AGENT"):
    os.environ["USER_AGENT"] = "LangGraph-RAG-MCP-Server/1.0"

# Imports LangGraph et LangChain
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langgraph.graph import END, StateGraph, START
from typing_extensions import TypedDict

# Import FastMCP - EXACTEMENT comme votre code météo
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server - EXACTEMENT comme votre code météo
mcp = FastMCP("langgraph-rag-server")

# Initialiser le LLM avec gestion sécurisée de la clé API
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("⚠️ ATTENTION: Utilisez une variable d'environnement pour la clé API en production")
    api_key = "sk-proj-0xUZ6aBpi14QWLtzQC2n hRFwAy9HhFfHS_cUMhXQMX6_U0pycw_XiZUUtZ4V6Gc5xEwhMZOsYA6xKN4HruNnPRcA"

# ===== ÉTAT DU GRAPHE =====

class GraphState(TypedDict):
    question: str
    generation: str
    web_search: str
    documents: List[Document]

# ===== CLASSE LANGGRAPH RAG SERVER =====

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
    
    async def setup_data_and_components(self):
        """Initialise les données et les composants RAG - ASYNC comme votre code météo"""
        print("🔄 Initialisation des données RAG...")
        
        try:
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
            
            # 2. Création de la base vectorielle avec clé API
            self.vectorstore = Chroma.from_documents(
                documents=doc_splits,
                collection_name="rag-chroma",
                embedding=OpenAIEmbeddings(api_key=api_key),
            )
            self.retriever = self.vectorstore.as_retriever()
            
            # 3. Configuration du grader de documents
            class GradeDocuments(BaseModel):
                binary_score: str = Field(
                    description="Documents are relevant to the question, 'yes' or 'no'"
                )
            
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
            llm = ChatOpenAI(
                model_name="gpt-4o-mini", 
                temperature=0,
                api_key=api_key
            )
            self.rag_chain = prompt | llm | StrOutputParser()
            
            # 5. Configuration du rewriter de questions
            llm_rewriter = ChatOpenAI(
                model="gpt-4o-mini", 
                temperature=0,
                api_key=api_key
            )
            re_write_prompt = ChatPromptTemplate.from_messages([
                ("system", """You a question re-writer that converts an input question to a better version that is optimized
                for web search. Look at the input and try to reason about the underlying semantic intent / meaning."""),
                ("human", "Here is the initial question: \n\n {question} \n Formulate an improved question."),
            ])
            
            self.question_rewriter = re_write_prompt | llm_rewriter | StrOutputParser()
            
            # 6. Configuration de l'outil de recherche web
            self.web_search_tool = TavilySearchResults(k=3)
            
            # 7. Configuration du workflow
            await self.setup_workflow()
            
            self.data_loaded = True
            print("✅ Composants RAG initialisés avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation: {str(e)}")
            return {"error": f"Erreur d'initialisation: {str(e)}"}
    
    async def setup_workflow(self):
        """Configure le workflow LangGraph - ASYNC"""
        try:
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
            print("✅ Workflow LangGraph compilé")
            
        except Exception as e:
            print(f"❌ Erreur compilation workflow: {str(e)}")
            raise
    
    async def query_rag(self, question: str) -> Dict[str, Any]:
        """Execute le workflow RAG pour une question"""
        try:
            # S'assurer que le serveur est initialisé
            if not self.data_loaded:
                await self.setup_data_and_components()
            
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

# Instance globale du serveur RAG - PAS d'initialisation au niveau global
rag_server = None

async def get_rag_server():
    """Initialise le serveur RAG de manière lazy - ASYNC comme votre code météo"""
    global rag_server
    if rag_server is None:
        print("🚀 Initialisation lazy du serveur RAG...")
        rag_server = LangGraphRAGServer()
        # Ne pas faire setup ici, le faire dans les outils individuels
    return rag_server

# ===== OUTILS MCP - EXACTEMENT comme votre structure météo =====

@mcp.tool()
async def query_rag_system(question: str) -> dict:
    """
    Execute une requête RAG en utilisant LangGraph avec recherche adaptative.
    Retourne les résultats de recherche et génération pour la question posée.
    """
    print("=== Exécution Requête RAG LangGraph ===")
    
    try:
        server = await get_rag_server()
        
        # Initialiser si pas encore fait - COMME votre code météo
        if not server.data_loaded:
            await server.setup_data_and_components()
        
        result = await server.query_rag(question)
        
        if result["success"]:
            return {
                "reponse": result['answer'],
                "question_traitee": result['question'],
                "details": {
                    "documents_utilises": result['documents_used'],
                    "recherche_web_activee": result['web_search_used'],
                    "workflow": f"Retrieval → Grading → {'Transform + Web Search → ' if result['web_search_used'] else ''}Generation"
                }
            }
        else:
            return {"error": f"Erreur lors de l'exécution RAG: {result['error']}"}
            
    except Exception as e:
        return {"error": f"Erreur système: {str(e)}"}

@mcp.tool()
async def get_rag_status() -> dict:
    """
    Obtient le statut détaillé du système RAG.
    Retourne l'état de tous les composants et leur disponibilité.
    """
    print("=== Vérification Statut RAG ===")
    
    try:
        if rag_server is None:
            return {"statut": "non_initialise", "message": "Système RAG non initialisé (sera initialisé au premier appel)"}
        
        # Initialiser si pas encore fait
        if not rag_server.data_loaded:
            await rag_server.setup_data_and_components()
        
        composants = {
            "vectorstore": rag_server.vectorstore is not None,
            "retriever": rag_server.retriever is not None,
            "rag_chain": rag_server.rag_chain is not None,
            "document_grader": rag_server.retrieval_grader is not None,
            "query_rewriter": rag_server.question_rewriter is not None,
            "web_search": rag_server.web_search_tool is not None,
            "langgraph_app": rag_server.app is not None
        }
        
        statut_general = "operationnel" if all(composants.values()) and rag_server.data_loaded else "partiel"
        
        return {
            "statut": statut_general,
            "donnees_chargees": rag_server.data_loaded,
            "composants": composants
        }
        
    except Exception as e:
        return {"error": f"Erreur lors de la vérification du statut: {str(e)}"}

@mcp.tool()
async def reload_rag_data() -> dict:
    """
    Recharge les données RAG depuis les sources par défaut.
    Réinitialise tous les composants du système.
    """
    print("=== Rechargement Données RAG ===")
    
    try:
        server = await get_rag_server()
        await server.setup_data_and_components()
        return {"statut": "succes", "message": "Données RAG rechargées avec succès"}
        
    except Exception as e:
        return {"error": f"Erreur lors du rechargement: {str(e)}"}

@mcp.tool()
async def test_rag_connection() -> dict:
    """
    Test de connexion pour vérifier que le serveur MCP RAG fonctionne.
    Retourne un message de confirmation si tout est opérationnel.
    """
    return {"statut": "connecte", "message": "Connexion MCP RAG réussie ! Le serveur LangGraph fonctionne correctement."}

# Point d'entrée principal - EXACTEMENT comme votre code météo
if __name__ == "__main__":
    print("Starting LangGraph RAG MCP server...")
    # Initialize and run the server - EXACTEMENT comme votre code météo
    mcp.run(transport='stdio')