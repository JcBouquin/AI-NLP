# Serveur MCP LangGraph RAG Pharmaceutique

## 📋 Description

Ce serveur MCP (Model Context Protocol) fournit une analyse intelligente de documents pharmaceutiques en utilisant **LangGraph** pour orchestrer un workflow multi-agents et **RAG (Retrieval Augmented Generation)** pour la recherche sémantique dans une base documentaire.

Le système utilise un graphe de traitement avec trois nodes spécialisés qui collaborent pour répondre aux questions :
- **Researcher** : Recherche les informations pertinentes via RAG (recherche sémantique vectorielle)
- **Analyst** : Analyse et synthétise les informations trouvées
- **Expert** : Fournit une réponse experte finale

## 🏗️ Architecture

### Composants principaux

1. **Vectorstore (SKLearn)** : Stocke les embeddings des documents pour la recherche sémantique rapide
   - Format : Parquet (`sklearn_vectorstore.parquet`)
   - Embeddings : OpenAI `text-embedding-3-small`
   - Chunks : 1000 tokens avec overlap de 200

2. **LangGraph Workflow** : Orchestration séquentielle des agents
   ```
   Question → Researcher → Analyst → Expert → Réponse finale
   ```

3. **Documents source** : Fichiers texte dans `pharmacy_docs/`
   - complements_alimentaires.txt
   - cosmetiques.txt
   - dermatologie.txt
   - fidelisation_client.txt
   - medicaments_otc.txt

## 🛠️ Outils disponibles

### 1. `analyze_pharmacy_question`
Analyse une question pharmaceutique en utilisant le workflow LangGraph complet avec RAG.

**Paramètres :**
- `question` (string, requis) : La question à analyser

**Exemple d'utilisation :**
```
Question : "Quels sont les meilleurs compléments alimentaires pour la récupération musculaire ?"
```

**Processus :**
1. Le **Researcher** récupère les 5 chunks les plus pertinents via recherche sémantique
2. L'**Analyst** synthétise les informations trouvées
3. L'**Expert** formule une réponse professionnelle complète

---

### 2. `list_pharmacy_documents`
Liste tous les documents pharmaceutiques disponibles dans le système.

**Paramètres :** Aucun

**Retourne :** Liste des noms de fichiers disponibles

---

### 3. `get_document_content`
Récupère le contenu complet d'un document spécifique.

**Paramètres :**
- `filename` (string, requis) : Nom du fichier (ex: "medicaments_otc.txt")

**Exemple :**
```
filename: "dermatologie.txt"
```

---

### 4. `reload_documents`
Recharge tous les documents depuis le répertoire et reconstruit le vectorstore.

**Paramètres :** Aucun

**Utilité :** Si vous avez ajouté ou modifié des documents dans `pharmacy_docs/`

## 🚀 Installation et Configuration

### Prérequis
- Python 3.10+
- Clé API OpenAI

### Dépendances
```bash
pip install mcp langchain langchain-openai langchain-community langgraph scikit-learn tiktoken
```

### Configuration Claude Desktop

Ajoutez cette section dans `%APPDATA%\Claude\claude_desktop_config.json` :

```json
{
  "mcpServers": {
    "langgraph-RAG_pharma-mcp": {
      "command": "python",
      "args": [
        "C:/Users/kosmo/pycode/mcp/Langgraph_mcp_RAGV1/server.py"
      ],
      "env": {
        "OPENAI_API_KEY": "votre-clé-api-openai"
      }
    }
  }
}
```

### Fichier .env (optionnel)

Créez un fichier `.env` dans le dossier du projet :
```
OPENAI_API_KEY=votre-clé-api-openai
```

## 📊 Fonctionnement du RAG

### 1. Initialisation (première utilisation)
Au premier lancement, le système :
1. Charge tous les documents `.txt` du dossier `pharmacy_docs/`
2. Découpe les documents en chunks de 1000 tokens
3. Crée les embeddings avec OpenAI
4. Sauvegarde le vectorstore dans `sklearn_vectorstore.parquet`

**Note :** Cette étape prend quelques secondes et utilise l'API OpenAI pour créer les embeddings.

### 2. Utilisations suivantes
Le vectorstore est chargé directement depuis le fichier `.parquet`, permettant des recherches ultra-rapides sans recréer les embeddings.

### 3. Recherche sémantique
Lors d'une question :
- Le système recherche les 5 chunks les plus similaires sémantiquement
- Utilise la similarité cosinus sur les embeddings vectoriels
- Retourne les passages les plus pertinents avec leurs sources

## 💡 Cas d'usage

### Exemple 1 : Conseil produit
```
Question : "Quel produit recommander pour les peaux sensibles avec de l'acné ?"

→ Le Researcher trouve les passages pertinents dans dermatologie.txt
→ L'Analyst synthétise les options disponibles
→ L'Expert formule une recommandation professionnelle
```

### Exemple 2 : Stratégie de vente
```
Question : "Comment améliorer la fidélisation des clients en pharmacie ?"

→ Recherche dans fidelisation_client.txt
→ Synthèse des meilleures pratiques
→ Recommandations actionnables
```

### Exemple 3 : Information médicament
```
Question : "Quelles sont les interactions possibles entre l'ibuprofène et les anticoagulants ?"

→ Recherche dans medicaments_otc.txt
→ Analyse des contre-indications
→ Conseil pharmaceutique expert
```

## 🔧 Personnalisation

### Ajouter de nouveaux documents
1. Placez vos fichiers `.txt` dans le dossier `pharmacy_docs/`
2. Utilisez l'outil `reload_documents` pour reconstruire le vectorstore

### Modifier les paramètres du retriever
Dans `pharmacy_graph_RAG.py` ligne 76-79 :
```python
self.retriever = self.vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5},  # Nombre de chunks à récupérer
)
```

### Modifier la taille des chunks
Dans `pharmacy_graph_RAG.py` ligne 145-148 :
```python
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000,    # Taille des chunks
    chunk_overlap=200,  # Overlap entre chunks
)
```

### Changer le modèle LLM
Dans `pharmacy_graph_RAG.py` ligne 66 :
```python
self.llm = ChatOpenAI(temperature=0.2, model="gpt-4o-mini")
```

Modèles disponibles : `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, etc.

## 📁 Structure du projet

```
Langgraph_mcp_RAGV1/
├── server.py                        # Serveur MCP principal
├── pharmacy_graph_RAG.py            # Classe PharmacyGraph avec workflow LangGraph
├── pharmacy_docs/                   # Documents source
│   ├── complements_alimentaires.txt
│   ├── cosmetiques.txt
│   ├── dermatologie.txt
│   ├── fidelisation_client.txt
│   └── medicaments_otc.txt
├── sklearn_vectorstore.parquet      # Vectorstore (créé automatiquement)
├── .env                             # Configuration API (optionnel)
├── pyproject.toml                   # Métadonnées du projet
└── claude.md                        # Cette documentation
```

## 🐛 Dépannage

### Le vectorstore n'est pas créé
- Vérifiez que le dossier `pharmacy_docs/` contient des fichiers `.txt`
- Vérifiez que votre clé API OpenAI est valide
- Consultez les logs dans Claude Desktop

### Erreur "No module named..."
```bash
pip install --upgrade mcp langchain langchain-openai langchain-community langgraph scikit-learn tiktoken
```

### Le serveur ne démarre pas
- Vérifiez le chemin Python dans la configuration Claude Desktop
- Assurez-vous que le fichier `server.py` est au bon emplacement
- Vérifiez les logs d'erreur dans Claude Desktop

### Recherches peu pertinentes
- Augmentez le paramètre `k` du retriever (plus de chunks récupérés)
- Réduisez la `chunk_size` pour des chunks plus précis
- Améliorez la qualité des documents source

## 📈 Performance

### Temps de traitement
- **Première initialisation** : 10-30 secondes (création des embeddings)
- **Chargement du vectorstore** : < 1 seconde
- **Recherche sémantique** : < 200ms
- **Analyse complète (question → réponse)** : 5-15 secondes

### Coûts API OpenAI
- **Embeddings** (première fois) : ~0.001$ par document
- **Requêtes LLM** : ~0.01-0.05$ par question (selon le modèle)

## 🔐 Sécurité

- Ne commitez jamais votre fichier `.env` avec votre clé API
- Utilisez des variables d'environnement pour la clé API en production
- Le vectorstore ne contient que des embeddings (pas de données sensibles lisibles)

## 📚 Ressources

- [Documentation LangGraph](https://langchain-ai.github.io/langgraph/)
- [Documentation LangChain](https://python.langchain.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)

## 📝 Notes techniques

### Pourquoi SKLearnVectorStore ?
- Léger et rapide pour des datasets < 10k documents
- Sérialisation Parquet pour un stockage efficace
- Pas besoin de serveur externe (vs Chroma, Pinecone)

### Workflow séquentiel vs parallèle
Le graphe LangGraph utilise un flux séquentiel pour garantir que :
1. Le Researcher trouve d'abord les informations
2. L'Analyst les synthétise avec le contexte complet
3. L'Expert formule une réponse cohérente basée sur l'analyse

### Gestion des chemins
Le système utilise des **chemins absolus** pour éviter les problèmes de working directory :
```python
script_dir = os.path.dirname(os.path.abspath(__file__))
```

Cela garantit que le vectorstore est toujours créé au bon endroit, peu importe d'où le serveur est lancé.

---

**Version** : 1.0.0
**Auteur** : Serveur MCP LangGraph RAG Pharmaceutique
**Licence** : MIT
