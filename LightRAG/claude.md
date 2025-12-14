# Guide d'Installation et d'Utilisation de LightRAG

## Vue d'ensemble

LightRAG est un système RAG (Retrieval-Augmented Generation) simple et rapide qui utilise des graphes de connaissances pour améliorer la récupération d'informations et la génération de réponses.

## Prérequis

- Python 3.10 ou supérieur
- Une clé API OpenAI (ou un autre fournisseur LLM supporté)
- 4 Go de RAM minimum (recommandé : 8 Go+)

## Installation

### Installation de base

L'installation a déjà été effectuée dans ce répertoire. Le package a été installé en mode éditable :

```bash
cd LightRAG
pip install -e .
```

### Installation avec des fonctionnalités supplémentaires

Pour installer avec l'API et l'interface Web :
```bash
pip install -e ".[api]"
```

Pour une installation complète hors ligne (avec tous les backends de stockage et LLM) :
```bash
pip install -e ".[offline]"
```

### Vérification de l'installation

```bash
python -c "import lightrag; print('LightRAG version:', lightrag.__version__)"
```

Version installée : **1.4.9.9**

## Configuration

### Variables d'environnement

Créez un fichier `.env` dans le répertoire du projet :

```bash
# API OpenAI (requis pour le fonctionnement de base)
OPENAI_API_KEY=sk-votre-cle-api

# Modèle LLM (optionnel, défaut : gpt-4o-mini)
LLM_MODEL=gpt-4o-mini

# Modèle d'embedding (optionnel, défaut : text-embedding-3-small)
EMBEDDING_MODEL=text-embedding-3-small

# Paramètres de performance
MAX_ASYNC=4
TOP_K=60
CHUNK_TOP_K=20
```

## Utilisation de base

### Exemple minimal

Créez un fichier `demo.py` :

```python
import os
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from lightrag.utils import setup_logger

setup_logger("lightrag", level="INFO")

WORKING_DIR = "./rag_storage"
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

async def initialize_rag():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func=openai_embed,
        llm_model_func=gpt_4o_mini_complete,
    )
    # IMPORTANT : Initialisation requise
    await rag.initialize_storages()
    return rag

async def main():
    try:
        # Initialiser le système RAG
        rag = await initialize_rag()

        # Insérer du texte
        await rag.ainsert("Votre texte à indexer ici...")

        # Effectuer une recherche hybride
        result = await rag.aquery(
            "Quelle est la question ?",
            param=QueryParam(mode="hybrid")
        )
        print(result)

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if rag:
            await rag.finalize_storages()

if __name__ == "__main__":
    asyncio.run(main())
```

### Modes de requête disponibles

- **naive** : Recherche de base sans techniques avancées
- **local** : Se concentre sur les informations dépendantes du contexte
- **global** : Utilise les connaissances globales
- **hybrid** : Combine les méthodes locale et globale
- **mix** : Intègre le graphe de connaissances et la récupération vectorielle (recommandé avec reranker)

### Exemple avec fichier texte

```python
# Télécharger un exemple de document
# curl https://raw.githubusercontent.com/gusye1234/nano-graphrag/main/tests/mock_data.txt > ./book.txt

async def main():
    rag = await initialize_rag()

    # Lire et insérer le contenu du fichier
    with open("./book.txt", "r", encoding="utf-8") as f:
        content = f.read()
        await rag.ainsert(content)

    # Interroger avec différents modes
    modes = ["naive", "local", "global", "hybrid"]
    for mode in modes:
        print(f"\n--- Mode : {mode} ---")
        result = await rag.aquery(
            "Quels sont les thèmes principaux de cette histoire ?",
            param=QueryParam(mode=mode)
        )
        print(result)

    await rag.finalize_storages()
```

## Fonctionnalités avancées

### Insertion par lots

```python
# Insérer plusieurs documents
documents = ["Texte 1", "Texte 2", "Texte 3"]
await rag.ainsert(documents)

# Avec IDs personnalisés
await rag.ainsert(documents, ids=["id1", "id2", "id3"])
```

### Gestion du graphe de connaissances

```python
# Créer une entité
entity = rag.create_entity("Google", {
    "description": "Entreprise technologique multinationale",
    "entity_type": "company"
})

# Créer une relation
relation = rag.create_relation("Google", "Gmail", {
    "description": "Google développe et opère Gmail",
    "keywords": "développe opère service",
    "weight": 2.0
})

# Modifier une entité
updated_entity = rag.edit_entity("Google", {
    "description": "Filiale d'Alphabet Inc., fondée en 1998"
})
```

### Suppression de données

```python
# Supprimer par entité
await rag.adelete_by_entity("Google")

# Supprimer par relation
await rag.adelete_by_relation("Google", "Gmail")

# Supprimer par ID de document
await rag.adelete_by_doc_id("doc-12345")
```

### Export de données

```python
# Export en CSV
rag.export_data("knowledge_graph.csv")

# Export en Excel
rag.export_data("graph_data.xlsx", file_format="excel")

# Export avec vecteurs
rag.export_data("complete_data.csv", include_vector_data=True)
```

## Utilisation avec d'autres fournisseurs LLM

### Ollama

```python
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import wrap_embedding_func_with_attrs
import numpy as np

@wrap_embedding_func_with_attrs(embedding_dim=768, max_token_size=8192)
async def embedding_func(texts: list[str]) -> np.ndarray:
    return await ollama_embed.func(texts, embed_model="nomic-embed-text")

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=ollama_model_complete,
    llm_model_name='qwen2',
    llm_model_kwargs={"options": {"num_ctx": 32768}},
    embedding_func=embedding_func,
)
```

### Hugging Face

```python
from lightrag.llm.hf import hf_model_complete, hf_embed
from transformers import AutoModel, AutoTokenizer

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=hf_model_complete,
    llm_model_name='meta-llama/Llama-3.1-8B-Instruct',
    embedding_func=EmbeddingFunc(
        embedding_dim=384,
        func=lambda texts: hf_embed(
            texts,
            tokenizer=AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2"),
            embed_model=AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        )
    ),
)
```

## Backends de stockage

### PostgreSQL (solution tout-en-un)

```python
# Variables d'environnement
POSTGRES_URI=postgresql://user:password@localhost:5432/lightrag

rag = LightRAG(
    working_dir=WORKING_DIR,
    kv_storage="PGKVStorage",
    vector_storage="PGVectorStorage",
    graph_storage="PGGraphStorage",
    doc_status_storage="PGDocStatusStorage",
)
```

### Neo4j (recommandé pour les graphes en production)

```python
# Variables d'environnement
NEO4J_URI=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

rag = LightRAG(
    working_dir=WORKING_DIR,
    graph_storage="Neo4JStorage",
)
```

## Serveur API LightRAG

Pour lancer l'interface Web et l'API REST :

```bash
# Copier et configurer l'environnement
cp env.example .env
# Éditer .env avec vos clés API

# Lancer le serveur
lightrag-server

# Ou avec Gunicorn (production)
lightrag-gunicorn
```

Interface accessible à : `http://localhost:8020`

## Résolution de problèmes

### Erreur : `AttributeError: __aenter__`

Solution : Toujours appeler `await rag.initialize_storages()` après la création de l'instance.

### Erreur lors du changement de modèle d'embedding

Solution : Supprimer le répertoire de données (sauf `kv_store_llm_response_cache.json` si vous souhaitez conserver le cache).

### Contexte insuffisant avec Ollama

Solution : Augmenter `num_ctx` à au moins 32768 tokens :
```python
llm_model_kwargs={"options": {"num_ctx": 32768}}
```

## Bonnes pratiques

1. **Initialisation** : Toujours initialiser les storages avant utilisation
2. **Modèles d'embedding** : Ne jamais changer de modèle d'embedding sans reconstruire l'index
3. **Taille de contexte** : LLM avec au moins 32 KB de contexte (64 KB recommandé)
4. **Paramètres LLM** : Minimum 32 milliards de paramètres pour de meilleurs résultats
5. **Reranker** : Utiliser un reranker avec le mode "mix" pour de meilleures performances
6. **Cache** : Activer le cache LLM pour réduire les coûts (`enable_llm_cache=True`)

## Ressources

- Documentation officielle : https://github.com/HKUDS/LightRAG
- Article de recherche : https://arxiv.org/abs/2410.05779
- Discord communautaire : https://discord.gg/yF2MmDJyGJ
- Tutoriel détaillé : https://learnopencv.com/lightrag

## Exemples de code

Le répertoire `examples/` contient de nombreux exemples :
- `lightrag_openai_demo.py` : Démonstration avec OpenAI
- `lightrag_ollama_demo.py` : Démonstration avec Ollama
- `rerank_example.py` : Utilisation du reranking
- `generate_query.py` : Génération de requêtes

## Commandes utiles

```bash
# Nettoyer le cache LLM
lightrag-clean-llmqc

# Télécharger les caches pour déploiement hors ligne
lightrag-download-cache

# Lancer les tests
pytest tests/
```
