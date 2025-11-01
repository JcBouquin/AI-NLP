# 📋 Exemple : Gestionnaire de Tâches avec DeepMCPAgent

Cet exemple démontre comment utiliser **DeepMCPAgent** pour créer un agent IA qui gère des tâches via un serveur MCP.

## 🎯 Ce que cet exemple montre

- ✅ Création d'un serveur MCP avec plusieurs outils personnalisés
- ✅ Découverte automatique des outils par DeepMCPAgent
- ✅ Utilisation d'un agent LangChain avec ces outils
- ✅ Mode démo automatique et mode interactif
- ✅ Traçage des appels d'outils en temps réel

## 🚀 Installation

Assurez-vous d'avoir installé les dépendances :

```bash
pip install "deepmcpagent[deep,examples]"
pip install python-dotenv langchain-openai rich
```

## 📝 Configuration

Créez un fichier `.env` à la racine du projet avec votre clé API :

```env
OPENAI_API_KEY=votre_cle_openai_ici
```

> 💡 **Astuce** : Vous pouvez utiliser d'autres modèles (Anthropic, Ollama, etc.) en modifiant `example_task_manager.py`

## ▶️ Utilisation

### Étape 1 : Démarrer le serveur MCP

Dans un **premier terminal**, lancez le serveur MCP :

```bash
python examples/servers/task_manager_server.py
```

Vous devriez voir :
```
🚀 Démarrage du serveur TaskManager MCP sur http://127.0.0.1:8001/mcp
📋 Outils disponibles: create_task, list_tasks, update_task, delete_task, get_task_stats
```

**⚠️ Important** : Gardez ce terminal ouvert pendant l'exécution de l'exemple !

### Étape 2 : Lancer l'exemple

Dans un **second terminal**, lancez l'exemple :

```bash
python examples/example_task_manager.py
```

## 🎮 Modes d'utilisation

### Mode Démo (par défaut)

L'exemple exécute automatiquement plusieurs requêtes pour démontrer les capacités :

1. Création de 3 tâches avec différentes priorités
2. Liste des tâches en attente
3. Mise à jour d'une tâche (marquer comme "en cours")
4. Affichage des statistiques

### Mode Interactif

Choisissez `interactive` quand on vous le demande pour dialoguer avec l'agent :

```
Choisissez un mode [interactive/demo]: interactive
```

Vous pouvez alors poser des questions comme :
- "Crée-moi une tâche pour préparer ma présentation"
- "Quelles sont mes tâches en cours ?"
- "Marque la tâche #1 comme terminée"
- "Supprime toutes les tâches terminées"

## 🛠️ Outils disponibles

Le serveur MCP expose 5 outils :

| Outil | Description |
|-------|-------------|
| `create_task` | Créer une nouvelle tâche avec titre, description et priorité |
| `list_tasks` | Lister les tâches (avec filtres optionnels) |
| `update_task` | Modifier une tâche existante |
| `delete_task` | Supprimer une tâche |
| `get_task_stats` | Obtenir des statistiques sur toutes les tâches |

## 📊 Ce que vous verrez

- **Outils découverts** : Tableau montrant tous les outils MCP disponibles
- **Appels d'outils** : Chaque utilisation d'un outil est affichée en temps réel (grâce à `trace_tools=True`)
- **Réponses de l'agent** : Les réponses de l'IA avec les résultats des opérations

## 🔍 Comprendre le code

### Serveur MCP (`task_manager_server.py`)

- Utilise **FastMCP** pour créer un serveur HTTP/SSE
- Expose des fonctions Python comme outils MCP via `@mcp.tool()`
- Stocke les données en mémoire (base de données simple)

### Agent (`example_task_manager.py`)

- **HTTPServerSpec** : Configure la connexion au serveur MCP
- **build_deep_agent()** : Construit l'agent avec découverte automatique des outils
- **LangChain ChatOpenAI** : Modèle LLM utilisé (facilement remplaçable)
- **trace_tools=True** : Active l'affichage des appels d'outils pour le debugging

## 💡 Personnalisation

### Changer le modèle LLM

Dans `example_task_manager.py`, remplacez :

```python
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o-mini")
```

Par exemple, pour Anthropic :

```python
from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(model="claude-3-5-sonnet-20241022")
```

### Ajouter des outils au serveur

Dans `task_manager_server.py`, ajoutez simplement :

```python
@mcp.tool()
def mon_nouvel_outil(param1: str, param2: int) -> dict:
    """Description de ce que fait l'outil."""
    # Votre logique ici
    return {"result": "..."}
```

L'agent découvrira automatiquement le nouvel outil !

### Changer le port

Modifiez le port dans les deux fichiers :
- **Serveur** : `mcp.run(..., port=8001, ...)`
- **Client** : `url="http://127.0.0.1:8001/mcp"`

## 🐛 Dépannage

### Erreur : "Failed to initialize agent"
- ✅ Vérifiez que le serveur MCP est démarré sur le bon port
- ✅ Vérifiez l'URL dans `HTTPServerSpec`

### Erreur : "OPENAI_API_KEY not found"
- ✅ Créez un fichier `.env` avec votre clé API
- ✅ Ou exportez la variable d'environnement : `export OPENAI_API_KEY=...`

### Aucun outil découvert
- ✅ Vérifiez que le serveur est accessible : `curl http://127.0.0.1:8001/mcp`
- ✅ Vérifiez les logs du serveur pour les erreurs

## 📚 Pour aller plus loin

- [Documentation DeepMCPAgent](https://cryxnet.github.io/DeepMCPAgent/)
- [Documentation FastMCP](https://gofastmcp.com/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

