# 🏥 Serveur MCP RAG Pharmaceutique avec LangGraph

## 📋 Résumé du Projet

Ce projet implémente un système de **Retrieval-Augmented Generation (RAG)** spécialisé dans l'analyse de documents pharmaceutiques. Il utilise **LangGraph** pour créer un workflow d'agents collaboratifs et **SKLearnVectorStore** pour une recherche sémantique efficace.

### Qu'est-ce que ça fait ?

Le système permet de :
- 🔍 **Interroger intelligemment** des documents pharmaceutiques (médicaments, dermatologie, compléments alimentaires, etc.)
- 🤖 **Utiliser un workflow d'agents** (Researcher → Analyst → Expert) pour analyser les questions
- 💾 **Rechercher rapidement** dans les documents grâce à un vectorstore persistant
- 🔄 **Mettre à jour facilement** les connaissances en rechargeant les documents

---

## 🏗️ Architecture du Système

### 1. Workflow LangGraph (3 Agents Collaboratifs)

```
┌─────────────┐      ┌──────────┐      ┌────────┐
│ RESEARCHER  │ ───> │ ANALYST  │ ───> │ EXPERT │
└─────────────┘      └──────────┘      └────────┘
     ↓                    ↓                 ↓
  Recherche          Synthétise        Répond de
  dans le RAG      les informations    manière experte
```

**Rôles des agents :**
- **🔬 Researcher** : Recherche les informations pertinentes via le vectorstore RAG
- **📊 Analyst** : Synthétise et structure les données trouvées
- **👨‍⚕️ Expert** : Fournit la réponse finale en tant que pharmacien expert

### 2. Système RAG avec Vectorstore

Le système utilise **SKLearnVectorStore** pour stocker et rechercher les documents :

```
Documents (.txt)  ──>  Chunking  ──>  Embeddings  ──>  sklearn_vectorstore.parquet
                      (300 tokens)   (OpenAI)          (Vectorstore persistant)
```

---

## 📦 Le Vectorstore : `sklearn_vectorstore.parquet`

### Qu'est-ce que c'est ?

Le fichier `sklearn_vectorstore.parquet` est un **vectorstore persistant** qui contient :
- ✅ Tous les documents du répertoire `pharmacy_docs/` découpés en chunks
- ✅ Les embeddings vectoriels (OpenAI `text-embedding-3-small`) de chaque chunk
- ✅ Les métadonnées (source, etc.) pour chaque chunk

### Pourquoi c'est important ?

**🚀 Performance et Efficacité :**

| Sans Vectorstore | Avec Vectorstore |
|-----------------|------------------|
| ❌ Recalculer les embeddings à chaque requête | ✅ Embeddings déjà calculés |
| ❌ Très lent (plusieurs secondes) | ✅ Très rapide (< 1 seconde) |
| ❌ Coût API élevé | ✅ Coût minimal (une seule fois) |

**💡 En résumé :** Le vectorstore est créé **une seule fois**, puis **réutilisé** à chaque connexion.

---

## 🔄 Cycle de Vie du Vectorstore

### 1️⃣ Première Initialisation

Lors de la première exécution, le système :

```python
# 1. Charge tous les documents .txt
documents = loader.load()  # Depuis pharmacy_docs/

# 2. Découpe en chunks
splits = text_splitter.split_documents(documents)  
# → Chunks de 300 tokens avec overlap de 20

# 3. Crée les embeddings et le vectorstore
vectorstore = SKLearnVectorStore.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    persist_path="sklearn_vectorstore.parquet",
    serializer="parquet"
)

# 4. Persiste sur le disque
vectorstore.persist()  # → Sauvegarde dans sklearn_vectorstore.parquet
```

**Résultat :** Un fichier `sklearn_vectorstore.parquet` est créé avec tous les embeddings.

### 2️⃣ Connexions Suivantes

Lors des prochaines connexions :

```python
# Si le fichier existe déjà...
if os.path.exists("sklearn_vectorstore.parquet"):
    # → Chargement direct, pas de recalcul !
    vectorstore = SKLearnVectorStore(
        embedding=embeddings,
        persist_path="sklearn_vectorstore.parquet",
        serializer="parquet"
    )
```

**Avantage :** Démarrage instantané, pas besoin de recalculer les embeddings ! 🎯

### 3️⃣ Ajout de Nouveaux Documents

Si vous ajoutez un nouveau fichier `.txt` ou modifiez un document existant :

**Option 1 : Via l'outil MCP**
```python
# Appeler l'outil reload_documents via Claude
→ Reconstruit automatiquement le vectorstore
```

**Option 2 : Via le code Python**
```python
pharmacy_graph.rebuild_vectorstore()
# → Supprime l'ancien vectorstore
# → Recharge tous les documents
# → Recrée les embeddings
# → Persiste le nouveau vectorstore
```

---

## 📂 Structure du Projet

```
langgraph-RAG_pharma-mcp/
│
├── 📄 server.py                    # Serveur MCP principal
├── 📄 pharmacy_graph_RAG.py        # Classe PharmacyGraph (workflow LangGraph)
├── 📄 .env                         # Clé API OpenAI
├── 📄 requirements.txt             # Dépendances Python
│
├── 📁 pharmacy_docs/               # Documents sources
│   ├── medicaments_otc.txt
│   ├── dermatologie.txt
│   ├── complements_alimentaires.txt
│   ├── cosmetiques.txt
│   └── fidelisation_client.txt
│
└── 💾 sklearn_vectorstore.parquet  # Vectorstore persistant (créé automatiquement)
```

---

## 🚀 Installation et Utilisation

### Prérequis

```bash
pip install -r requirements.txt
```

### Configuration

Créer un fichier `.env` avec votre clé API OpenAI :
```
OPENAI_API_KEY=sk-...
```

### Démarrage du Serveur MCP

Le serveur se lance via le fichier de configuration MCP de Claude Desktop.

### Utilisation via Claude

**1. Analyser une question :**
```
"Quels sont les points de valorisation de l'expertise en dermatologie ?"
```

**2. Lister les documents disponibles :**
```
"Liste les documents pharmaceutiques disponibles"
```

**3. Voir le contenu d'un document :**
```
"Montre-moi le contenu de medicaments_otc.txt"
```

**4. Recharger les documents (après modification) :**
```
"Recharge les documents pharmaceutiques"
```

---

## 🛠️ Outils MCP Disponibles

| Outil | Description |
|-------|-------------|
| `analyze_pharmacy_question` | Analyse une question avec le workflow LangGraph + RAG |
| `list_pharmacy_documents` | Liste tous les fichiers .txt dans pharmacy_docs/ |
| `get_document_content` | Récupère le contenu complet d'un document |
| `reload_documents` | Recharge les documents et reconstruit le vectorstore |

---

## 🔍 Processus de Recherche RAG

Quand vous posez une question :

```
Question posée par l'utilisateur
         ↓
┌─────────────────────────────────┐
│  1. RESEARCHER NODE             │
│  → Recherche dans vectorstore   │
│  → Récupère les 5 chunks les    │
│    plus pertinents (similarity) │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│  2. ANALYST NODE                │
│  → Synthétise les infos         │
│  → Structure la réponse         │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│  3. EXPERT NODE                 │
│  → Répond en tant qu'expert     │
│  → Format professionnel         │
└─────────────────────────────────┘
         ↓
    Réponse finale
```

---

## 💡 Points Clés à Retenir

### ✅ Persistance du Vectorstore
- Le fichier `sklearn_vectorstore.parquet` est **persistant**
- Il est créé **une seule fois** à la première utilisation
- Il est **réutilisé automatiquement** aux connexions suivantes
- **Pas besoin de le recréer** à chaque démarrage !

### ✅ Mise à Jour des Documents
- Pour ajouter/modifier des documents : placez les fichiers dans `pharmacy_docs/`
- Appelez l'outil `reload_documents` pour reconstruire le vectorstore
- Le nouveau vectorstore remplace l'ancien

### ✅ Optimisation
- Tous les documents sont indexés dans **un seul fichier** `.parquet`
- Recherche ultra-rapide grâce aux embeddings pré-calculés
- Pas de recalcul à chaque requête = économie de temps et coûts API

---

## 📊 Statistiques Techniques

- **Modèle LLM** : `gpt-4o-mini` (via OpenAI)
- **Modèle d'Embeddings** : `text-embedding-3-small` (OpenAI)
- **Taille des Chunks** : 300 tokens
- **Overlap des Chunks** : 20 tokens
- **Nombre de résultats RAG** : 5 documents les plus similaires
- **Format Vectorstore** : Parquet (via SKLearnVectorStore)

---

## 🎯 Cas d'Usage Typiques

### Exemple 1 : Recherche d'Information
```
Question : "Quels sont les médicaments OTC les plus vendus ?"
→ Le système recherche dans medicaments_otc.txt
→ Extrait les informations pertinentes
→ Fournit une réponse structurée
```

### Exemple 2 : Analyse Multi-Documents
```
Question : "Compare les stratégies de fidélisation et les conseils en dermatologie"
→ Le système recherche dans fidelisation_client.txt ET dermatologie.txt
→ Synthétise les informations des deux sources
→ Fournit une analyse comparative
```

### Exemple 3 : Mise à Jour des Connaissances
```
1. Ajouter nouveau_medicament.txt dans pharmacy_docs/
2. Appeler reload_documents
3. Le nouveau document est indexé dans le vectorstore
4. Prêt à répondre aux questions sur le nouveau médicament !
```

---

## 🐛 Dépannage

### Le vectorstore ne se crée pas
- Vérifier que le répertoire `pharmacy_docs/` existe
- Vérifier qu'il contient des fichiers `.txt`
- Vérifier que `OPENAI_API_KEY` est bien définie

### Les réponses ne sont pas à jour
- Utiliser l'outil `reload_documents` pour reconstruire le vectorstore
- Le système charge automatiquement le nouveau vectorstore

### Erreur d'encodage
- Tous les fichiers `.txt` doivent être encodés en **UTF-8**

---

## 📚 Technologies Utilisées

- **LangGraph** : Workflow d'agents orchestrés
- **LangChain** : Framework RAG et gestion des documents
- **OpenAI** : LLM (gpt-4o-mini) et Embeddings (text-embedding-3-small)
- **SKLearnVectorStore** : Vectorstore persistant avec sérialisation Parquet
- **MCP (Model Context Protocol)** : Interface avec Claude Desktop

---

## 📝 License

Ce projet est destiné à un usage éducatif et professionnel dans le domaine pharmaceutique.

---

## 🤝 Contribution

Pour améliorer le système :
1. Ajouter de nouveaux documents dans `pharmacy_docs/`
2. Appeler `reload_documents` pour mettre à jour le vectorstore
3. Tester les nouvelles capacités de recherche

---


**Développé avec ❤️ pour optimiser l'analyse de documents pharmaceutiques**
