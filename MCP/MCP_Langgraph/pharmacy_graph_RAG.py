"""
Module contenant la classe PharmacyGraph pour l'analyse de documents pharmaceutiques avec LangGraph et RAG
"""

import os
import re
import tiktoken
from typing import TypedDict, Annotated

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages


class GraphState(TypedDict):
    """État partagé entre les nodes du graphe"""

    question: str
    research_output: str
    analysis_output: str
    final_answer: str
    messages: Annotated[list, add_messages]


class PharmacyGraph:
    """Workflow LangGraph pour la recherche pharmaceutique avec RAG"""

    def __init__(
        self,
        docs_directory=None,
        vectorstore_path=None,
    ):
        """
        Initialise le workflow LangGraph avec RAG

        Args:
            docs_directory: Chemin vers le répertoire contenant les documents
            vectorstore_path: Chemin vers le fichier vectorstore
        """
        # Obtenir le répertoire du script actuel
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Définir les chemins par défaut relatifs au script
        if docs_directory is None:
            self.docs_directory = os.path.join(script_dir, "pharmacy_docs")
        else:
            self.docs_directory = docs_directory

        if vectorstore_path is None:
            self.vectorstore_path = os.path.join(script_dir, "sklearn_vectorstore.parquet")
        else:
            self.vectorstore_path = vectorstore_path

        print(f"📁 Répertoire des documents: {self.docs_directory}")
        print(f"💾 Chemin du vectorstore: {self.vectorstore_path}")

        # Initialiser le dictionnaire des documents
        self.documents = {}

        # Initialiser le LLM
        self.llm = ChatOpenAI(temperature=0.2, model="gpt-4o-mini")

        # Initialiser ou charger le vectorstore
        self.vectorstore = self._initialize_vectorstore()

        # Charger les documents dans self.documents si pas déjà fait
        if not self.documents:
            self._load_documents_list()

        # Créer le retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5},  # Récupère les 5 chunks les plus pertinents
        )

        # Construire le graphe
        self.graph = self._build_graph()

    def _load_documents_list(self):
        """
        Charge la liste des documents dans self.documents sans recréer le vectorstore
        """
        if not os.path.exists(self.docs_directory):
            print(f"⚠️ Le répertoire {self.docs_directory} n'existe pas")
            return

        # Charger tous les fichiers .txt
        for filename in os.listdir(self.docs_directory):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.docs_directory, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.documents[filename] = f.read()
                except Exception as e:
                    print(f"⚠️ Erreur lors de la lecture de {filename}: {e}")

        print(f"📚 {len(self.documents)} documents chargés dans le dictionnaire")

    def count_tokens(self, text: str, model: str = "cl100k_base") -> int:
        """
        Compte le nombre de tokens dans le texte en utilisant tiktoken.

        Args:
            text (str): Le texte à compter
            model (str): Le modèle de tokenizer à utiliser (default: cl100k_base pour GPT-4)

        Returns:
            int: Nombre de tokens dans le texte
        """
        encoder = tiktoken.get_encoding(model)
        return len(encoder.encode(text))

    def _load_documents(self):
        """
        Charge tous les documents depuis le répertoire pharmacy_docs

        Returns:
            list: Liste de documents LangChain
        """
        print(f"Chargement des documents depuis {self.docs_directory}...")

        if not os.path.exists(self.docs_directory):
            print(f"Erreur: Le répertoire {self.docs_directory} n'existe pas")
            return []

        # Utiliser DirectoryLoader pour charger tous les fichiers .txt
        loader = DirectoryLoader(
            self.docs_directory,
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )

        documents = loader.load()

        print(f"✅ Chargé {len(documents)} documents")

        # Peupler le dictionnaire documents et afficher les infos
        for i, doc in enumerate(documents):
            filename = os.path.basename(doc.metadata.get("source", "Unknown"))
            tokens = self.count_tokens(doc.page_content)
            print(f"  {i+1}. {filename} ({tokens} tokens)")

            # Ajouter au dictionnaire documents
            self.documents[filename] = doc.page_content

        # Compter les tokens totaux
        total_tokens = sum(self.count_tokens(doc.page_content) for doc in documents)
        print(f"Total tokens dans les documents: {total_tokens}")

        return documents

    def _split_documents(self, documents):
        """
        Découpe les documents en chunks pour un meilleur retrieval

        Args:
            documents (list): Liste de documents à découper

        Returns:
            list: Liste de documents découpés
        """
        print("Découpage des documents en chunks...")

        # Initialiser le text splitter avec tiktoken
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000,  # Chunks plus petits pour la pharmacie
            chunk_overlap=200,  # Overlap pour maintenir le contexte
        )

        # Découper les documents
        split_docs = text_splitter.split_documents(documents)

        print(f"✅ Créé {len(split_docs)} chunks depuis les documents")

        # Compter les tokens totaux
        total_tokens = sum(self.count_tokens(doc.page_content) for doc in split_docs)
        print(f"Total tokens dans les chunks: {total_tokens}")

        return split_docs

    def _create_vectorstore(self, splits):
        """
        Crée un vectorstore depuis les chunks de documents

        Args:
            splits (list): Liste de documents découpés à embedder

        Returns:
            SKLearnVectorStore: Vectorstore contenant les documents embeddés
        """
        print("Création du SKLearnVectorStore...")

        # Initialiser les embeddings OpenAI
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # Créer le vectorstore
        vectorstore = SKLearnVectorStore.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_path=self.vectorstore_path,
            serializer="parquet",
        )

        print("✅ SKLearnVectorStore créé avec succès")

        # Persister le vectorstore
        vectorstore.persist()

        # Afficher le chemin absolu du vectorstore
        abs_path = os.path.abspath(self.vectorstore_path)
        print(f"✅ Vectorstore persisté dans {self.vectorstore_path}")
        print(f"🎯 CHEMIN ABSOLU DU VECTORSTORE: {abs_path}")

        return vectorstore

    def _initialize_vectorstore(self):
        """
        Initialise ou charge le vectorstore

        Returns:
            SKLearnVectorStore: Vectorstore prêt à l'emploi
        """
        # Si le vectorstore existe déjà, le charger
        if os.path.exists(self.vectorstore_path):
            print(
                f"Chargement du vectorstore existant depuis {self.vectorstore_path}..."
            )
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            vectorstore = SKLearnVectorStore(
                embedding=embeddings,
                persist_path=self.vectorstore_path,
                serializer="parquet",
            )
            print("✅ Vectorstore chargé avec succès")
            return vectorstore

        # Sinon, créer un nouveau vectorstore
        print("Création d'un nouveau vectorstore...")
        documents = self._load_documents()

        if not documents:
            raise ValueError("Aucun document trouvé dans le répertoire pharmacy_docs")

        splits = self._split_documents(documents)
        vectorstore = self._create_vectorstore(splits)

        return vectorstore

    def rebuild_vectorstore(self):
        """
        Reconstruit le vectorstore depuis les documents sources
        Utile si les documents ont été modifiés
        """
        print("Reconstruction du vectorstore...")

        # Supprimer l'ancien vectorstore s'il existe
        if os.path.exists(self.vectorstore_path):
            os.remove(self.vectorstore_path)
            print(f"Ancien vectorstore supprimé: {self.vectorstore_path}")

        # Créer un nouveau vectorstore
        documents = self._load_documents()
        splits = self._split_documents(documents)
        self.vectorstore = self._create_vectorstore(splits)

        # Recréer le retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": 5}
        )

        print("✅ Vectorstore reconstruit avec succès")

    def researcher_node(self, state: GraphState) -> GraphState:
        """
        Node Chercheur : Recherche les informations pertinentes via RAG
        """
        question = state["question"]

        # Récupérer les documents pertinents via le retriever
        retrieved_docs = self.retriever.invoke(question)

        # Créer le contexte à partir des documents récupérés
        context = "\n\n=== DOCUMENTS PERTINENTS TROUVÉS ===\n"
        for i, doc in enumerate(retrieved_docs):
            source = os.path.basename(doc.metadata.get("source", "Unknown"))
            context += (
                f"\n--- Extrait {i+1} (Source: {source}) ---\n{doc.page_content}\n"
            )

        prompt = f"""Tu es un chercheur pharmaceutique expérimenté avec une connaissance
approfondie des médicaments, des suppléments et des produits de santé.

Tu as accès aux extraits de documents suivants, récupérés par recherche sémantique:
{context}

QUESTION: {question}

TÂCHE: Analyse ces extraits et identifie toutes les informations pertinentes pour répondre à cette question.
Extrais les passages clés, les données importantes et toute information utile.

FORMAT DE SORTIE: Liste des informations pertinentes trouvées dans les extraits, avec références aux sources."""

        response = self.llm.invoke(prompt)

        state["research_output"] = response.content
        state["messages"] = [("system", f"[RESEARCHER] {response.content}")]

        return state

    def analyst_node(self, state: GraphState) -> GraphState:
        """
        Node Analyste : Analyse et synthétise les informations trouvées
        """
        question = state["question"]
        research_output = state["research_output"]

        prompt = f"""Tu es un analyste de données spécialisé dans le domaine pharmaceutique.
Tu excelles dans la synthèse d'informations complexes et la présentation de données
de manière claire et concise.

QUESTION INITIALE: {question}

INFORMATIONS TROUVÉES PAR LE CHERCHEUR:
{research_output}

TÂCHE: Analyse ces informations et crée une synthèse structurée qui répond à la question.
Organise les données de manière logique et hiérarchisée.

FORMAT DE SORTIE: Synthèse structurée des informations pertinentes avec organisation claire."""

        response = self.llm.invoke(prompt)

        state["analysis_output"] = response.content
        state["messages"].append(("system", f"[ANALYST] {response.content}"))

        return state

    def expert_node(self, state: GraphState) -> GraphState:
        """
        Node Expert : Fournit la réponse finale experte
        """
        question = state["question"]
        analysis_output = state["analysis_output"]

        prompt = f"""Tu es un pharmacien avec des décennies d'expérience dans la vente et
la recommandation de produits pharmaceutiques. Tu comprends les besoins des clients
et sais comment communiquer des informations médicales complexes de manière accessible.

QUESTION: {question}

ANALYSE FOURNIE:
{analysis_output}

TÂCHE: En te basant sur l'analyse fournie, réponds de manière complète et précise à la question.
Utilise ton expertise pour fournir une réponse professionnelle, structurée et fiable.

FORMAT DE SORTIE: Réponse complète et précise à la question, rédigée de manière professionnelle et accessible."""

        response = self.llm.invoke(prompt)

        state["final_answer"] = response.content
        state["messages"].append(("system", f"[EXPERT] {response.content}"))

        return state

    def _build_graph(self) -> StateGraph:
        """
        Construit le graphe LangGraph avec les 3 nodes séquentiels
        """
        # Créer le graphe
        workflow = StateGraph(GraphState)

        # Ajouter les nodes
        workflow.add_node("researcher", self.researcher_node)
        workflow.add_node("analyst", self.analyst_node)
        workflow.add_node("expert", self.expert_node)

        # Définir les edges (flux séquentiel)
        workflow.set_entry_point("researcher")
        workflow.add_edge("researcher", "analyst")
        workflow.add_edge("analyst", "expert")
        workflow.add_edge("expert", END)

        # Compiler le graphe
        return workflow.compile()

    def answer_question(self, question: str) -> str:
        """
        Répond à une question en utilisant le workflow LangGraph avec RAG

        Args:
            question: La question posée

        Returns:
            Réponse à la question
        """
        # État initial
        initial_state = {
            "question": question,
            "research_output": "",
            "analysis_output": "",
            "final_answer": "",
            "messages": [],
        }

        # Exécuter le graphe
        result = self.graph.invoke(initial_state)

        # Retourner la réponse finale
        return result["final_answer"]

    def get_stats(self):
        """
        Retourne des statistiques sur le vectorstore

        Returns:
            dict: Statistiques du système RAG
        """
        # Compter les documents dans le vectorstore
        # Note: SKLearnVectorStore ne fournit pas directement un count
        # On peut utiliser une requête factice pour estimer

        stats = {
            "vectorstore_path": self.vectorstore_path,
            "vectorstore_exists": os.path.exists(self.vectorstore_path),
            "docs_directory": self.docs_directory,
            "retriever_k": 5,
            "llm_model": "gpt-4o-mini",
            "embedding_model": "text-embedding-3-small",
        }

        return stats
