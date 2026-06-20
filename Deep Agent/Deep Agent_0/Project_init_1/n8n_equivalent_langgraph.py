"""
Équivalent LangGraph + Claude du workflow n8n "TEST_GenAlgoDoc"
==================================================================

Pipeline séquentiel avec validation humaine à chaque étape :

    upload fichier
        -> Agent SQL (doc technique)
            -> validation (accept/deny+commentaire) -> boucle si refus
        -> Agent métier (doc fonctionnelle à partir de la doc technique)
            -> validation (accept/deny+commentaire) -> boucle si refus
        -> Agent template (HTML A->F à partir de la doc métier)
        -> extraction email
        -> envoi mail

Différences structurelles avec n8n :
    - n8n: chaque "Agent" + son "Text Classifier" sont 2 nodes séparés,
      reliés par des connexions explicites dessinées à la main.
    - LangGraph: même logique, mais exprimée comme un graphe d'état codé.
      Le routage (accept -> continuer / deny -> boucler) est une
      "conditional_edge" : une fonction Python qui lit le state et
      retourne le nom du nœud suivant.

Pré-requis :
    pip install langgraph langchain-anthropic python-dotenv

Variables d'environnement (.env) :
    ANTHROPIC_API_KEY=...
"""

import os
from typing import TypedDict, Literal, Optional
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

model = ChatAnthropic(model="claude-sonnet-4-6", temperature=0)

# ---------------------------------------------------------------------------
# 1. STATE — l'équivalent du "JSON qui circule entre les nodes" dans n8n
# ---------------------------------------------------------------------------

class DocState(TypedDict):
    sql_text: str                      # contenu du fichier uploadé
    user_comment: Optional[str]         # commentaire de l'utilisateur lors d'une relance
    technical_doc: Optional[str]        # sortie Agent SQL
    business_doc: Optional[str]         # sortie Agent métier
    html_doc: Optional[str]             # sortie Agent template
    email: Optional[str]                # adresse mail extraite


# ---------------------------------------------------------------------------
# 2. PROMPTS SYSTEME — repris du JSON n8n (raccourcis ici pour la démo,
#    à coller intégralement en prod)
# ---------------------------------------------------------------------------

SQL_AGENT_SYSTEM_PROMPT = """\
Tu es un analyste SQL Server spécialisé en rétro-ingénierie de scripts
multi-statements. Produis une description STRICTEMENT SYNTAXIQUE et
SÉQUENTIELLE du code SQL fourni (statement par statement, fiches par
temp table, section Questions/ambiguïtés). Termine par une demande de
validation à l'utilisateur contenant l'intégralité du texte final.
[... reprendre ici l'intégralité du prompt n8n "Agent SQL" ...]
"""

BUSINESS_AGENT_SYSTEM_PROMPT = """\
Tu es un expert Data Science consultant. Transforme la documentation
technique fournie en documentation métier claire, sans jamais utiliser
de SQL ni de noms de tables/colonnes techniques. Commence par
"## TITRE: Documentation métier – <Nom algo>" et termine par une
demande de validation à l'utilisateur.
[... reprendre ici l'intégralité du prompt n8n "Agent métier" ...]
"""

TEMPLATE_AGENT_SYSTEM_PROMPT = """\
Tu es un agent de mise en forme documentaire. Transforme le contenu
métier en HTML autonome et complet, structuré en sections A à F
(Contexte, Définition de marché, Diagramme, Règles métiers, Résultats,
Commentaires/Issues). Retourne UNIQUEMENT du HTML.
[... reprendre ici l'intégralité du prompt n8n "Agent template" ...]
"""


# ---------------------------------------------------------------------------
# 3. NODES — équivalent de chaque "node" n8n
# ---------------------------------------------------------------------------

def sql_agent_node(state: DocState) -> dict:
    """Équivalent du node 'Agent SQL'."""
    comment_block = (
        f"\nL'utilisateur a un commentaire : {state['user_comment']}\n"
        "Conserve toute la documentation et modifie seulement ce qui est concerné."
        if state.get("user_comment")
        else "\nAucun commentaire."
    )
    messages = [
        {"role": "system", "content": SQL_AGENT_SYSTEM_PROMPT},
        {"role": "user", "content": state["sql_text"] + comment_block},
    ]
    response = model.invoke(messages)
    return {"technical_doc": response.content, "user_comment": None}


def validate_technical_doc_node(state: DocState) -> Command[Literal["business_agent", "sql_agent"]]:
    """
    Équivalent du node 'Validation de la doc technique' (textClassifier).
    interrupt() met le graphe en pause et attend la réponse humaine,
    exactement comme le node de chat n8n attend la réponse de l'utilisateur.
    """
    user_response = interrupt({
        "question": "Voici la documentation technique. Valides-tu, ou as-tu un commentaire ?",
        "doc": state["technical_doc"],
    })
    if user_response.get("decision") == "accept":
        return Command(goto="business_agent")
    else:
        return Command(
            goto="sql_agent",
            update={"user_comment": user_response.get("comment", "")},
        )


def business_agent_node(state: DocState) -> dict:
    """Équivalent du node 'Agent métier'."""
    comment_block = (
        f"\nL'utilisateur a un commentaire : {state['user_comment']}\n"
        "Conserve toute la documentation métier et modifie seulement ce qui est concerné."
        if state.get("user_comment")
        else "\nAucun commentaire."
    )
    messages = [
        {"role": "system", "content": BUSINESS_AGENT_SYSTEM_PROMPT},
        {"role": "user", "content": state["technical_doc"] + comment_block},
    ]
    response = model.invoke(messages)
    return {"business_doc": response.content, "user_comment": None}


def validate_business_doc_node(state: DocState) -> Command[Literal["template_agent", "business_agent"]]:
    """Équivalent du node 'Validation de la doc métier'."""
    user_response = interrupt({
        "question": "Voici la documentation métier. Valides-tu, ou as-tu un commentaire ?",
        "doc": state["business_doc"],
    })
    if user_response.get("decision") == "accept":
        return Command(goto="template_agent")
    else:
        return Command(
            goto="business_agent",
            update={"user_comment": user_response.get("comment", "")},
        )


def template_agent_node(state: DocState) -> dict:
    """Équivalent du node 'Agent template' (génère le HTML A->F)."""
    messages = [
        {"role": "system", "content": TEMPLATE_AGENT_SYSTEM_PROMPT},
        {"role": "user", "content": state["business_doc"]},
    ]
    response = model.invoke(messages)
    return {"html_doc": response.content}


def extract_email_node(state: DocState) -> dict:
    """Équivalent du node 'Extraction mail' (informationExtractor)."""
    user_input = interrupt({
        "question": "La documentation est prête ! À quelle adresse mail l'envoyer ?",
    })
    return {"email": user_input.get("email", "")}


def send_email_node(state: DocState) -> dict:
    """Équivalent du node 'Envoi mail' (emailSend)."""
    # Remplacer par un vrai envoi SMTP en production.
    print(f"[SIMULATION] Email envoyé à {state['email']}")
    print(f"Sujet : Documentation métier")
    print(f"Corps (HTML) : {state['html_doc'][:200]}...")
    return {}


# ---------------------------------------------------------------------------
# 4. CONSTRUCTION DU GRAPHE — équivalent des "connections" du JSON n8n
# ---------------------------------------------------------------------------

builder = StateGraph(DocState)

builder.add_node("sql_agent", sql_agent_node)
builder.add_node("validate_technical_doc", validate_technical_doc_node)
builder.add_node("business_agent", business_agent_node)
builder.add_node("validate_business_doc", validate_business_doc_node)
builder.add_node("template_agent", template_agent_node)
builder.add_node("extract_email", extract_email_node)
builder.add_node("send_email", send_email_node)

builder.add_edge(START, "sql_agent")
builder.add_edge("sql_agent", "validate_technical_doc")
# Le routage accept/deny est géré DANS validate_technical_doc_node via Command(goto=...)
# -> pas besoin de add_conditional_edges ici.

builder.add_edge("business_agent", "validate_business_doc")
builder.add_edge("template_agent", "extract_email")
builder.add_edge("extract_email", "send_email")
builder.add_edge("send_email", END)

# MemorySaver est OBLIGATOIRE pour pouvoir interrupt()/reprendre le graphe.
graph = builder.compile(checkpointer=MemorySaver())


# ---------------------------------------------------------------------------
# 5. EXEMPLE D'EXÉCUTION — montre le cycle interrupt -> resume
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "demo-1"}}

    sql_script = "SELECT * INTO #tmp FROM FtDelivery WHERE ValidityFlag = 1"

    # 1er appel : démarre le graphe, qui va s'arrêter au premier interrupt()
    result = graph.invoke({"sql_text": sql_script}, config=config)
    print("Graphe en pause :", result["__interrupt__"])

    # Reprise après validation "accept" de la doc technique
    result = graph.invoke(
        Command(resume={"decision": "accept"}), config=config
    )
    print("Graphe en pause :", result["__interrupt__"])

    # Reprise après validation "accept" de la doc métier
    result = graph.invoke(
        Command(resume={"decision": "accept"}), config=config
    )
    print("Graphe en pause :", result["__interrupt__"])

    # Reprise après saisie de l'email
    result = graph.invoke(
        Command(resume={"email": "test@iqvia.com"}), config=config
    )
    print("Terminé :", result)
