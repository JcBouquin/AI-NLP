"""
Module contenant la classe PharmacyResearchCrew pour l'analyse de documents pharmaceutiques
"""

from crewai import Agent, Task, Crew, Process
from typing import List
import os
from langchain_openai import ChatOpenAI


class PharmacyResearchCrew:
    """Équipe d'agents pour la recherche pharmaceutique"""

    def __init__(self, docs_directory="./pharmacy_docs"):
        """
        Initialise l'équipe de recherche

        Args:
            docs_directory: Chemin vers le répertoire contenant les documents
        """
        self.docs_directory = docs_directory

        # Charger tous les documents en mémoire
        self.documents = self._load_all_documents()

        # Initialisation des agents
        self.researcher = self._create_researcher()
        self.analyst = self._create_analyst()
        self.expert = self._create_expert()

    def _load_all_documents(self):
        """Charge tous les documents dans un dictionnaire"""
        docs = {}
        if not os.path.exists(self.docs_directory):
            # Logging désactivé pour éviter l'interférence avec MCP
            return docs

        for filename in os.listdir(self.docs_directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.docs_directory, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        docs[filename] = f.read()
                except Exception as e:
                    # Logging désactivé pour éviter l'interférence avec MCP
                    pass
        return docs

    def _create_researcher(self) -> Agent:
        """Crée l'agent chercheur"""
        docs_context = "\n=== DOCUMENTS DISPONIBLES ===\n"

        for filename, content in self.documents.items():
            docs_context += f"\n--- {filename} ---\n{content}\n"

        return Agent(
            role="Chercheur Pharmaceutique",
            goal="Trouver toutes les informations pertinentes sur les produits pharmaceutiques dans les documents fournis",
            backstory=f"""Tu es un chercheur pharmaceutique expérimenté avec une connaissance
            approfondie des médicaments, des suppléments et des produits de santé.

            Tu as accès aux documents suivants:
            {docs_context}

            Utilise ces documents pour répondre aux questions.""",
            verbose=False,
            allow_delegation=True,
        )

    def _create_analyst(self) -> Agent:
        """Crée l'agent analyste"""
        return Agent(
            role="Analyste de Données Pharmaceutiques",
            goal="Analyser et synthétiser les informations sur les produits pharmaceutiques",
            backstory="""Tu es un analyste de données spécialisé dans le domaine pharmaceutique.
            Tu excelles dans la synthèse d'informations complexes et la présentation de données
            de manière claire et concise.""",
            verbose=False,
            allow_delegation=True,
        )

    def _create_expert(self) -> Agent:
        """Crée l'agent expert"""
        return Agent(
            role="Expert en Pharmacie",
            goal="Fournir des réponses précises et fiables sur les produits pharmaceutiques",
            backstory="""Tu es un pharmacien avec des décennies d'expérience dans la vente et
            la recommandation de produits pharmaceutiques. Tu comprends les besoins des clients
            et sais comment communiquer des informations médicales complexes de manière accessible.""",
            llm=ChatOpenAI(temperature=0.2, model="gpt-4o-mini"),
            verbose=False,
            allow_delegation=False,
        )

    def create_task_for_question(self, question: str) -> List[Task]:
        """
        Crée les tâches pour répondre à une question

        Args:
            question: La question posée

        Returns:
            Liste des tâches à effectuer
        """
        research_task = Task(
            description=f"""Rechercher des informations sur: '{question}'
            
            Analyse tous les documents disponibles dans ton backstory et extrais les informations pertinentes.""",
            expected_output="Liste des informations pertinentes trouvées dans les documents",
            agent=self.researcher,
        )

        analysis_task = Task(
            description=f"Analyser les informations trouvées pour: '{question}'",
            expected_output="Synthèse structurée des informations pertinentes",
            agent=self.analyst,
            context=[research_task],
        )

        expert_task = Task(
            description=f"Répondre à la question: '{question}'",
            expected_output="Réponse complète et précise à la question",
            agent=self.expert,
            context=[analysis_task],
        )

        return [research_task, analysis_task, expert_task]

    def answer_question(self, question: str) -> str:
        """
        Répond à une question en utilisant l'équipe d'agents

        Args:
            question: La question posée

        Returns:
            Réponse à la question
        """
        tasks = self.create_task_for_question(question)

        crew = Crew(
            agents=[self.researcher, self.analyst, self.expert],
            tasks=tasks,
            verbose=False,
            process=Process.sequential,
        )

        result = crew.kickoff()
        return str(result)
