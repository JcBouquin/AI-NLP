"""
Exemple pédagogique : Orchestrateur + 3 sous-agents (deepagents + Claude)
==========================================================================

Objectif :
    Un agent "orchestrateur" reçoit la question de l'utilisateur, l'analyse,
    puis délègue à UN des 3 sous-agents spécialisés selon le domaine détecté :

        1. research_agent   -> questions factuelles / recherche web
        2. code_agent        -> questions techniques / génération de code
        3. writer_agent       -> rédaction, reformulation, synthèse de texte

    L'orchestrateur ne fait JAMAIS le travail lui-même : il route et,
    si besoin, enchaîne plusieurs sous-agents (ex: recherche -> rédaction).

Pré-requis :
    pip install deepagents langchain-anthropic tavily-python python-dotenv

Variables d'environnement nécessaires (.env) :
    ANTHROPIC_API_KEY=...
    TAVILY_API_KEY=...        # pour l'outil de recherche web

Visualisation :
    Ce script peut tourner seul (agent.invoke(...)) OU être exposé via
    LangGraph CLI pour être inspecté dans LangSmith Studio (voir le
    fichier langgraph.json fourni à côté).
"""

import os
from typing import Literal
from dotenv import load_dotenv
from tavily import TavilyClient
from deepagents import create_deep_agent

load_dotenv()

# ---------------------------------------------------------------------------
# 1. OUTILS — les fonctions concrètes que les sous-agents peuvent appeler
# ---------------------------------------------------------------------------

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
) -> dict:
    """Effectue une recherche web et retourne les résultats les plus pertinents."""
    return tavily_client.search(query, max_results=max_results, topic=topic)


def run_python_snippet(code: str) -> str:
    """
    Exécute un court extrait Python et retourne stdout/stderr.
    ATTENTION : démo pédagogique uniquement — à sandboxer en production
    (voir tool_configs / HumanInTheLoopConfig de deepagents).
    """
    import io
    import contextlib

    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            exec(code, {})
        return buffer.getvalue() or "(exécution réussie, aucune sortie)"
    except Exception as e:
        return f"Erreur d'exécution : {e}"


# ---------------------------------------------------------------------------
# 2. SOUS-AGENTS — chacun a son propre system_prompt, ses outils, et peut
#    même utiliser un modèle différent (ici on garde Claude partout).
# ---------------------------------------------------------------------------

research_subagent = {
    "name": "research-agent",
    "description": (
        "À utiliser pour toute question factuelle nécessitant une recherche "
        "d'information à jour (actualité, données chiffrées, vérification de faits)."
    ),
    "system_prompt": (
        "Tu es un assistant de recherche rigoureux. Utilise l'outil "
        "internet_search pour vérifier les faits avant de répondre. "
        "Cite tes sources de manière concise. Ne réponds jamais de mémoire "
        "seule si l'information peut être périmée."
    ),
    "tools": [internet_search],
    "model": "anthropic:claude-sonnet-4-6",
}

code_subagent = {
    "name": "code-agent",
    "description": (
        "À utiliser pour toute question technique : écrire, expliquer, "
        "déboguer ou exécuter du code."
    ),
    "system_prompt": (
        "Tu es un ingénieur logiciel senior. Écris du code clair et testé. "
        "Quand c'est pertinent, utilise run_python_snippet pour vérifier "
        "que ton code fonctionne avant de le présenter."
    ),
    "tools": [run_python_snippet],
    "model": "anthropic:claude-sonnet-4-6",
}

writer_subagent = {
    "name": "writer-agent",
    "description": (
        "À utiliser pour la rédaction, la reformulation, le résumé ou "
        "l'amélioration stylistique d'un texte. N'effectue PAS de recherche "
        "factuelle elle-même."
    ),
    "system_prompt": (
        "Tu es un rédacteur professionnel. Ton rôle est de structurer, "
        "reformuler ou résumer un contenu de façon claire et fluide, "
        "en respectant le ton demandé par l'utilisateur."
    ),
    "tools": [],  # pas d'outils : pur travail de langage
    "model": "anthropic:claude-sonnet-4-6",
}

subagents = [research_subagent, code_subagent, writer_subagent]

# ---------------------------------------------------------------------------
# 3. ORCHESTRATEUR — le "deep agent" principal
#    Son seul rôle : comprendre la demande et déléguer au bon sous-agent
#    via l'outil `task` (injecté automatiquement par deepagents).
# ---------------------------------------------------------------------------

ORCHESTRATOR_PROMPT = """\
Tu es un orchestrateur. Tu ne réponds JAMAIS directement aux questions
de fond. Ton seul travail est d'analyser la demande de l'utilisateur et
de la déléguer au sous-agent le plus adapté via l'outil `task` :

- research-agent : question factuelle, actualité, vérification de données
- code-agent     : question technique, code, debug
- writer-agent   : rédaction, reformulation, résumé

Si la demande combine plusieurs besoins (ex: "recherche X puis rédige un
résumé"), enchaîne les délégations dans l'ordre logique : recherche
d'abord, rédaction ensuite. Une fois le ou les sous-agents terminés,
synthétise brièvement le résultat final pour l'utilisateur.
"""

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    instructions=ORCHESTRATOR_PROMPT,
    subagents=subagents,
)


# ---------------------------------------------------------------------------
# 4. POINT D'ENTRÉE — exécution directe en local (sans Studio)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # --- Visualisation statique de la structure du graphe -----------------
    # `agent` est un CompiledStateGraph standard : get_graph() fonctionne
    # exactement comme sur n'importe quel graphe LangGraph "à la main".
    try:
        png_bytes = agent.get_graph().draw_mermaid_png()
        with open("orchestrator_graph.png", "wb") as f:
            f.write(png_bytes)
        print("Graphe exporté -> orchestrator_graph.png")
    except Exception as e:
        print(f"Export PNG impossible ({e}), export du code Mermaid brut :")
        print(agent.get_graph().draw_mermaid())

    # --- Exécution des questions de test -----------------------------------
    questions = [
        "Quel est le taux directeur actuel de la BCE ?",
        "Écris une fonction Python qui calcule la suite de Fibonacci.",
        "Reformule ce texte de façon plus formelle : 'le truc marche pas bien'",
    ]

    for q in questions:
        print(f"\n{'=' * 70}\nQUESTION : {q}\n{'=' * 70}")
        result = agent.invoke({"messages": [{"role": "user", "content": q}]})
        print(result["messages"][-1].content)
