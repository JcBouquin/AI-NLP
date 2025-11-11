"""
Serveur MCP pour l'analyse de documents pharmaceutiques avec LangGraph
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Any
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import mcp.types as types

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == "win32":
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Désactiver les warnings et logs qui interfèrent avec MCP
logging.getLogger().setLevel(logging.CRITICAL)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Charger le fichier .env si présent
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()

from pharmacy_graph_RAG import PharmacyGraph

# Configuration de l'API Key OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY doit être définie dans les variables d'environnement ou dans le fichier .env"
    )

# Initialisation du serveur MCP
server = Server("langgraph-pharmacy-mcp")

# Instance globale de PharmacyGraph
pharmacy_graph = None


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    Liste des outils disponibles dans le serveur MCP
    """
    return [
        Tool(
            name="analyze_pharmacy_question",
            description="""
            Analyse une question sur les produits pharmaceutiques en utilisant un workflow LangGraph.
            Le workflow comprend trois nodes (researcher, analyst, expert) qui travaillent ensemble
            pour fournir une réponse complète basée sur les documents disponibles.
            
            Args:
                question (str): La question à analyser concernant les produits pharmaceutiques,
                               les réglementations, les stratégies de vente, etc.
            
            Returns:
                str: Réponse détaillée et structurée à la question
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "La question sur les produits pharmaceutiques à analyser",
                    }
                },
                "required": ["question"],
            },
        ),
        Tool(
            name="list_pharmacy_documents",
            description="""
            Liste tous les documents pharmaceutiques disponibles dans le système.
            
            Returns:
                str: Liste des noms de fichiers disponibles pour l'analyse
            """,
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_document_content",
            description="""
            Récupère le contenu complet d'un document spécifique.
            
            Args:
                filename (str): Nom du fichier à récupérer (ex: "medicaments.txt")
            
            Returns:
                str: Contenu du document
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Nom du fichier à récupérer",
                    }
                },
                "required": ["filename"],
            },
        ),
        Tool(
            name="reload_documents",
            description="""
            Recharge tous les documents depuis le répertoire pharmacy_docs.
            Utile si de nouveaux documents ont été ajoutés.
            
            Returns:
                str: Message de confirmation avec le nombre de documents rechargés
            """,
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[TextContent]:
    """
    Gestionnaire d'appels d'outils
    """
    global pharmacy_graph

    # Initialiser pharmacy_graph si nécessaire
    if pharmacy_graph is None:
        # Utilise les chemins absolus par défaut définis dans PharmacyGraph
        pharmacy_graph = PharmacyGraph()

    try:
        if name == "analyze_pharmacy_question":
            question = arguments.get("question")
            if not question:
                return [
                    TextContent(type="text", text="❌ Erreur: La question est requise")
                ]

            # Analyser la question avec LangGraph
            result = pharmacy_graph.answer_question(question)

            return [TextContent(type="text", text=f"✅ Analyse complète:\n\n{result}")]

        elif name == "list_pharmacy_documents":
            if not pharmacy_graph.documents:
                return [
                    TextContent(
                        type="text",
                        text="⚠️ Aucun document disponible dans le répertoire pharmacy_docs",
                    )
                ]

            doc_list = "\n".join(
                [f"- {filename}" for filename in pharmacy_graph.documents.keys()]
            )
            return [
                TextContent(
                    type="text", text=f"📚 Documents disponibles:\n\n{doc_list}"
                )
            ]

        elif name == "get_document_content":
            filename = arguments.get("filename")
            if not filename:
                return [
                    TextContent(
                        type="text", text="❌ Erreur: Le nom du fichier est requis"
                    )
                ]

            if filename not in pharmacy_graph.documents:
                return [
                    TextContent(
                        type="text",
                        text=f"❌ Erreur: Le document '{filename}' n'existe pas",
                    )
                ]

            content = pharmacy_graph.documents[filename]
            return [
                TextContent(type="text", text=f"📄 Contenu de {filename}:\n\n{content}")
            ]

        elif name == "reload_documents":
            # Réinitialiser l'instance avec les chemins absolus par défaut
            pharmacy_graph = PharmacyGraph()

            # Forcer la reconstruction du vectorstore
            pharmacy_graph.rebuild_vectorstore()

            # Compter les documents chargés
            num_docs = len(pharmacy_graph.documents)

            return [
                TextContent(
                    type="text",
                    text=f"✅ {num_docs} document(s) rechargé(s) avec succès",
                )
            ]

        else:
            return [TextContent(type="text", text=f"❌ Outil inconnu: {name}")]

    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"❌ Erreur lors de l'exécution de l'outil '{name}': {str(e)}",
            )
        ]


async def main():
    """Point d'entrée principal du serveur MCP"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="langgraph-pharmacy-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
