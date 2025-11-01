"""
Serveur MCP exemple : Gestionnaire de tâches
Ce serveur expose des outils pour gérer une liste de tâches (todo list).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fastmcp import FastMCP

# Base de données simple en mémoire
tasks_db: list[dict[str, Any]] = []
task_counter = 0

mcp = FastMCP("TaskManager")


@mcp.tool()
def create_task(title: str, description: str = "", priority: str = "medium") -> dict[str, Any]:
    """Créer une nouvelle tâche.
    
    Args:
        title: Le titre de la tâche
        description: Description optionnelle de la tâche
        priority: Priorité ('low', 'medium', 'high')
    
    Returns:
        Dictionnaire avec les détails de la tâche créée
    """
    global task_counter
    task_counter += 1
    
    task = {
        "id": task_counter,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    }
    tasks_db.append(task)
    return {
        "success": True,
        "task": task,
        "message": f"Tâche '{title}' créée avec succès (ID: {task_counter})"
    }


@mcp.tool()
def list_tasks(status: str | None = None, priority: str | None = None) -> dict[str, Any]:
    """Lister toutes les tâches, avec filtres optionnels.
    
    Args:
        status: Filtrer par statut ('pending', 'in_progress', 'completed')
        priority: Filtrer par priorité ('low', 'medium', 'high')
    
    Returns:
        Liste des tâches correspondant aux critères
    """
    filtered = tasks_db
    
    if status:
        filtered = [t for t in filtered if t.get("status") == status]
    
    if priority:
        filtered = [t for t in filtered if t.get("priority") == priority]
    
    return {
        "count": len(filtered),
        "tasks": filtered,
        "total_tasks": len(tasks_db)
    }


@mcp.tool()
def update_task(task_id: int, title: str | None = None, description: str | None = None, 
                status: str | None = None, priority: str | None = None) -> dict[str, Any]:
    """Mettre à jour une tâche existante.
    
    Args:
        task_id: ID de la tâche à mettre à jour
        title: Nouveau titre (optionnel)
        description: Nouvelle description (optionnel)
        status: Nouveau statut ('pending', 'in_progress', 'completed') (optionnel)
        priority: Nouvelle priorité ('low', 'medium', 'high') (optionnel)
    
    Returns:
        Dictionnaire avec le résultat de la mise à jour
    """
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    
    if not task:
        return {
            "success": False,
            "message": f"Tâche avec ID {task_id} non trouvée"
        }
    
    if title:
        task["title"] = title
    if description is not None:
        task["description"] = description
    if status:
        if status in ["pending", "in_progress", "completed"]:
            task["status"] = status
        else:
            return {
                "success": False,
                "message": f"Statut invalide: {status}. Utilisez 'pending', 'in_progress', ou 'completed'"
            }
    if priority:
        if priority in ["low", "medium", "high"]:
            task["priority"] = priority
        else:
            return {
                "success": False,
                "message": f"Priorité invalide: {priority}. Utilisez 'low', 'medium', ou 'high'"
            }
    
    task["updated_at"] = datetime.now().isoformat()
    
    return {
        "success": True,
        "task": task,
        "message": f"Tâche {task_id} mise à jour avec succès"
    }


@mcp.tool()
def delete_task(task_id: int) -> dict[str, Any]:
    """Supprimer une tâche.
    
    Args:
        task_id: ID de la tâche à supprimer
    
    Returns:
        Dictionnaire avec le résultat de la suppression
    """
    global tasks_db
    initial_count = len(tasks_db)
    tasks_db = [t for t in tasks_db if t["id"] != task_id]
    
    if len(tasks_db) < initial_count:
        return {
            "success": True,
            "message": f"Tâche {task_id} supprimée avec succès"
        }
    else:
        return {
            "success": False,
            "message": f"Tâche avec ID {task_id} non trouvée"
        }


@mcp.tool()
def get_task_stats() -> dict[str, Any]:
    """Obtenir des statistiques sur les tâches.
    
    Returns:
        Statistiques détaillées sur toutes les tâches
    """
    total = len(tasks_db)
    by_status = {}
    by_priority = {}
    
    for task in tasks_db:
        status = task.get("status", "unknown")
        priority = task.get("priority", "unknown")
        
        by_status[status] = by_status.get(status, 0) + 1
        by_priority[priority] = by_priority.get(priority, 0) + 1
    
    return {
        "total_tasks": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "completed": by_status.get("completed", 0),
        "pending": by_status.get("pending", 0),
        "in_progress": by_status.get("in_progress", 0)
    }


if __name__ == "__main__":
    print("🚀 Démarrage du serveur TaskManager MCP sur http://127.0.0.1:8001/mcp")
    print("📋 Outils disponibles: create_task, list_tasks, update_task, delete_task, get_task_stats")
    
    # Serveur sur un port différent pour éviter les conflits avec math_server
    mcp.run(transport="http", host="127.0.0.1", port=8001, path="/mcp")

