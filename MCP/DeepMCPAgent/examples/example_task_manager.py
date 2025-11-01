"""
Exemple complet : Utilisation de DeepMCPAgent avec un serveur de gestion de tâches

Cet exemple montre comment :
1. Créer un agent qui utilise des outils MCP pour gérer des tâches
2. Interagir avec l'agent via plusieurs requêtes
3. Voir les outils découverts automatiquement
4. Tracer les appels d'outils en temps réel

AVANT DE LANCER :
1. Assurez-vous que le serveur MCP est démarré :
   python examples/servers/task_manager_server.py

2. Configurez votre clé API OpenAI (ou autre modèle) dans un fichier .env :
   OPENAI_API_KEY=votre_cle_ici
"""

import asyncio
from typing import Any

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

from deepmcpagent import HTTPServerSpec, build_deep_agent


def _extract_final_answer(result: Any) -> str:
    """Extraction du message final de la réponse de l'agent."""
    try:
        if isinstance(result, dict) and "messages" in result and result["messages"]:
            last = result["messages"][-1]
            content = getattr(last, "content", None)
            if isinstance(content, str) and content:
                return content
            if isinstance(content, list) and content and isinstance(content[0], dict):
                return content[0].get("text") or str(content)
            return str(last)
        return str(result)
    except Exception:
        return str(result)


async def main() -> None:
    console = Console()
    load_dotenv()
    
    console.print("\n[bold cyan]🤖 DeepMCPAgent - Exemple Gestionnaire de Tâches[/bold cyan]\n")
    
    # Configuration du serveur MCP
    # ⚠️ IMPORTANT: Démarrez task_manager_server.py dans un autre terminal avant de lancer ce script
    servers = {
        "task_manager": HTTPServerSpec(
            url="http://127.0.0.1:8001/mcp",
            transport="http",
        ),
    }
    
    # Choix du modèle LLM
    # Vous pouvez changer pour un autre modèle (Anthropic, Ollama, etc.)
    try:
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        console.print("[green]✓[/green] Modèle OpenAI configuré\n")
    except Exception as e:
        console.print(f"[red]✗[/red] Erreur lors de la configuration du modèle: {e}")
        console.print("[yellow]Assurez-vous d'avoir OPENAI_API_KEY dans votre .env[/yellow]\n")
        return
    
    # Construction de l'agent avec découverte automatique des outils
    console.print("[cyan]🔍 Découverte des outils MCP...[/cyan]")
    try:
        graph, loader = await build_deep_agent(
            servers=servers,
            model=model,
            instructions=(
                "Tu es un assistant intelligent pour la gestion de tâches. "
                "Utilise les outils MCP disponibles pour créer, lister, modifier et supprimer des tâches. "
                "Sois concis et précis dans tes réponses. "
                "Quand tu crées ou modifies des tâches, confirme toujours les actions effectuées."
            ),
            trace_tools=True,  # Active l'affichage des appels d'outils
        )
        console.print("[green]✓[/green] Agent construit avec succès\n")
    except Exception as e:
        console.print(f"[red]✗[/red] Erreur lors de la construction de l'agent: {e}")
        console.print("[yellow]Assurez-vous que le serveur MCP est démarré sur http://127.0.0.1:8001/mcp[/yellow]\n")
        return
    
    # Affichage des outils découverts
    console.print("[cyan]📋 Outils découverts:[/cyan]")
    infos = await loader.list_tool_info()
    infos = list(infos) if infos else []
    
    if infos:
        table = Table(title="Outils MCP Disponibles", show_lines=True, header_style="bold magenta")
        table.add_column("Nom", style="cyan", no_wrap=True)
        table.add_column("Description", style="green")
        for t in infos:
            table.add_row(t.name, t.description or "-")
        console.print(table)
    else:
        console.print("[yellow]⚠ Aucun outil découvert (vérifiez que le serveur MCP est démarré)[/yellow]")
    
    console.print("\n" + "="*70 + "\n")
    
    # Mode interactif ou exécution d'exemples
    mode = Prompt.ask(
        "Choisissez un mode",
        choices=["interactive", "demo"],
        default="demo"
    )
    
    if mode == "demo":
        # Exécution d'exemples automatiques
        examples = [
            "Crée-moi 3 tâches : une tâche haute priorité pour préparer une présentation, "
            "une tâche moyenne priorité pour répondre aux emails, et une tâche basse priorité pour faire les courses.",
            
            "Affiche-moi toutes les tâches en attente",
            
            "Marque la première tâche comme étant en cours",
            
            "Donne-moi des statistiques sur mes tâches",
        ]
        
        for i, query in enumerate(examples, 1):
            console.print(Panel.fit(
                f"[bold]Exemple {i}/{len(examples)}[/bold]\n\n{query}",
                title="Requête Utilisateur",
                style="bold magenta"
            ))
            
            try:
                result = await graph.ainvoke({
                    "messages": [{"role": "user", "content": query}]
                })
                final_text = _extract_final_answer(result)
                
                console.print(Panel(
                    final_text or "(aucun contenu)",
                    title="Réponse de l'Agent",
                    style="bold green"
                ))
            except Exception as e:
                console.print(f"[red]Erreur: {e}[/red]")
            
            console.print("\n" + "-"*70 + "\n")
            await asyncio.sleep(1)  # Petite pause entre les exemples
    
    else:
        # Mode interactif
        console.print("[bold yellow]Mode interactif activé[/bold yellow]")
        console.print("Tapez 'quit' ou 'exit' pour quitter\n")
        
        while True:
            query = Prompt.ask("[bold cyan]Vous[/bold cyan]")
            
            if query.lower() in ["quit", "exit", "q"]:
                console.print("\n[bold yellow]Au revoir ![/bold yellow]\n")
                break
            
            if not query.strip():
                continue
            
            try:
                console.print("[dim]🔄 Traitement en cours...[/dim]\n")
                result = await graph.ainvoke({
                    "messages": [{"role": "user", "content": query}]
                })
                final_text = _extract_final_answer(result)
                
                console.print(Panel(
                    final_text or "(aucun contenu)",
                    title="Agent",
                    style="bold green"
                ))
                console.print()  # Ligne vide
                
            except Exception as e:
                console.print(f"[red]Erreur: {e}[/red]\n")
    
    console.print("[bold cyan]✓ Session terminée[/bold cyan]\n")


if __name__ == "__main__":
    asyncio.run(main())

