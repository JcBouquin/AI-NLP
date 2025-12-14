# Guide LightRAG pour Débutants

Bienvenue dans ce guide destiné aux personnes qui découvrent LightRAG et la programmation en intelligence artificielle !

## C'est quoi LightRAG ?

Imagine que tu as une énorme bibliothèque de documents. LightRAG, c'est comme avoir un bibliothécaire super intelligent qui :
- Lit et comprend tous tes documents
- Organise les informations de manière intelligente dans un "graphe de connaissances"
- Peut répondre à tes questions en utilisant ces informations

C'est ce qu'on appelle un système **RAG** (Retrieval-Augmented Generation) : il récupère les bonnes informations et génère des réponses pertinentes.

## De quoi as-tu besoin ?

### 1. Python

Python est un langage de programmation. Pour vérifier si tu l'as déjà :

**Sur Windows** :
```bash
python --version
```

Tu devrais voir quelque chose comme `Python 3.10.x` ou plus récent. Si ce n'est pas le cas, télécharge Python depuis https://www.python.org/downloads/

**Important** : Pendant l'installation de Python, coche la case "Add Python to PATH" !

### 2. Une clé API OpenAI

OpenAI, c'est l'entreprise qui a créé ChatGPT. Pour utiliser LightRAG, tu auras besoin d'une clé API :

1. Va sur https://platform.openai.com/
2. Crée un compte ou connecte-toi
3. Va dans "API Keys" et crée une nouvelle clé
4. **IMPORTANT** : Copie cette clé et garde-la en sécurité (tu ne pourras la voir qu'une seule fois)

Note : Utiliser l'API OpenAI coûte de l'argent, mais c'est très peu cher pour débuter (quelques centimes pour des tests). Tu peux aussi utiliser des alternatives gratuites comme Ollama (expliqué plus bas).

### 3. Un éditeur de code

Je te recommande **Visual Studio Code** (gratuit) : https://code.visualstudio.com/

## Installation pas à pas

### Étape 1 : Ouvrir un terminal

**Sur Windows** :
- Appuie sur `Windows + R`
- Tape `cmd` et appuie sur Entrée

**Sur Mac/Linux** :
- Cherche "Terminal" dans tes applications

### Étape 2 : Créer un dossier pour ton projet

```bash
# Va dans ton dossier Documents (ou où tu veux)
cd Documents

# Crée un nouveau dossier
mkdir mon_projet_lightrag

# Entre dans ce dossier
cd mon_projet_lightrag
```

### Étape 3 : Télécharger LightRAG

```bash
git clone https://github.com/HKUDS/LightRAG.git
cd LightRAG
```

Si tu n'as pas Git, télécharge-le depuis https://git-scm.com/downloads

### Étape 4 : Installer LightRAG

```bash
python -m pip install -e .
```

Cette commande va télécharger et installer tous les composants nécessaires. Ça peut prendre quelques minutes.

### Étape 5 : Vérifier que ça marche

```bash
python -c "import lightrag; print('Ça marche !')"
```

Si tu vois "Ça marche !", c'est bon !

## Ton premier programme LightRAG

### Étape 1 : Créer un fichier pour ta clé API

Crée un fichier nommé `.env` dans le dossier LightRAG (attention au point au début) :

```
OPENAI_API_KEY=sk-ta-cle-api-ici
```

Remplace `sk-ta-cle-api-ici` par ta vraie clé API OpenAI.

### Étape 2 : Créer ton premier script

Crée un fichier `mon_premier_test.py` :

```python
import os
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from lightrag.utils import setup_logger

# Active les messages d'information
setup_logger("lightrag", level="INFO")

# Dossier où seront stockées les données
WORKING_DIR = "./mes_donnees"
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

async def main():
    print("🚀 Démarrage de LightRAG...")

    # Créer le système LightRAG
    rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func=openai_embed,
        llm_model_func=gpt_4o_mini_complete,
    )

    # ÉTAPE SUPER IMPORTANTE : Initialiser le système
    await rag.initialize_storages()
    print("✅ LightRAG est prêt !")

    # Ajouter du texte à la base de connaissances
    print("\n📚 Ajout d'informations...")
    texte = """
    Python est un langage de programmation créé par Guido van Rossum en 1991.
    Il est très populaire pour l'intelligence artificielle et l'analyse de données.
    Python est connu pour sa syntaxe simple et lisible.
    """
    await rag.ainsert(texte)
    print("✅ Informations ajoutées !")

    # Poser une question
    print("\n❓ Je pose une question...")
    question = "Qui a créé Python ?"
    reponse = await rag.aquery(
        question,
        param=QueryParam(mode="hybrid")
    )

    print(f"\n💬 Question : {question}")
    print(f"📝 Réponse : {reponse}")

    # Fermer proprement
    await rag.finalize_storages()
    print("\n👋 Terminé !")

# Lancer le programme
if __name__ == "__main__":
    asyncio.run(main())
```

### Étape 3 : Lancer ton programme

```bash
python mon_premier_test.py
```

Tu devrais voir des messages s'afficher et obtenir une réponse à ta question !

## Comprendre le code

Décomposons ce qui se passe :

```python
from lightrag import LightRAG, QueryParam
```
Cette ligne importe (charge) les outils dont on a besoin.

```python
rag = LightRAG(...)
```
On crée notre "assistant intelligent".

```python
await rag.initialize_storages()
```
On prépare l'endroit où seront stockées les informations. **Ne jamais oublier cette ligne !**

```python
await rag.ainsert(texte)
```
On donne du texte à lire à notre assistant. Il va l'analyser et créer un graphe de connaissances.

```python
reponse = await rag.aquery(question, ...)
```
On pose une question et on récupère la réponse.

## Les différents modes de recherche

Quand tu poses une question, tu peux choisir comment chercher la réponse :

```python
param=QueryParam(mode="naive")    # Simple et rapide
param=QueryParam(mode="local")    # Cherche dans le contexte proche
param=QueryParam(mode="global")   # Cherche dans toutes les connaissances
param=QueryParam(mode="hybrid")   # Combine local et global (recommandé !)
```

## Exemple pratique : Analyser un livre

Créons un programme qui lit un livre et répond à des questions dessus :

```python
import os
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from lightrag.utils import setup_logger

setup_logger("lightrag", level="INFO")

WORKING_DIR = "./livres"
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

async def analyser_livre():
    # Créer LightRAG
    rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func=openai_embed,
        llm_model_func=gpt_4o_mini_complete,
    )
    await rag.initialize_storages()

    # Lire un fichier texte
    print("📖 Lecture du livre...")
    with open("mon_livre.txt", "r", encoding="utf-8") as f:
        contenu = f.read()

    # Analyser le livre
    print("🧠 Analyse en cours...")
    await rag.ainsert(contenu)

    # Poser plusieurs questions
    questions = [
        "Quels sont les personnages principaux ?",
        "Quel est le thème principal du livre ?",
        "Où se déroule l'histoire ?"
    ]

    for question in questions:
        print(f"\n❓ {question}")
        reponse = await rag.aquery(
            question,
            param=QueryParam(mode="hybrid")
        )
        print(f"💬 {reponse}")

    await rag.finalize_storages()

asyncio.run(analyser_livre())
```

Pour utiliser ce programme :
1. Crée un fichier `mon_livre.txt` avec n'importe quel texte
2. Lance `python analyser_livre.py`

## Utiliser Ollama (alternative gratuite à OpenAI)

Si tu ne veux pas payer pour OpenAI, tu peux utiliser **Ollama** qui fait tourner des modèles d'IA sur ton ordinateur (gratuit mais plus lent).

### Installation d'Ollama

1. Télécharge Ollama : https://ollama.ai/
2. Installe-le
3. Ouvre un terminal et tape :

```bash
ollama pull qwen2
ollama pull nomic-embed-text
```

### Code avec Ollama

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

## Erreurs courantes et solutions

### "ModuleNotFoundError: No module named 'lightrag'"

**Problème** : Python ne trouve pas LightRAG.

**Solution** :
```bash
cd LightRAG
python -m pip install -e .
```

### "AuthenticationError: Invalid API key"

**Problème** : Ta clé API OpenAI n'est pas valide.

**Solution** :
- Vérifie que tu as bien copié toute la clé (elle commence par `sk-`)
- Vérifie que ton fichier `.env` est dans le bon dossier
- Assure-toi que tu as du crédit sur ton compte OpenAI

### "AttributeError: __aenter__"

**Problème** : Tu as oublié d'initialiser les storages.

**Solution** : Ajoute cette ligne après avoir créé `rag` :
```python
await rag.initialize_storages()
```

### Le programme est très lent

**C'est normal !** L'analyse de texte par IA prend du temps. La première fois est la plus longue car il doit tout analyser. Les fois suivantes, le système utilise un cache et c'est plus rapide.

## Conseils pour débuter

1. **Commence petit** : Teste avec de petits textes (quelques paragraphes) avant d'analyser de gros documents

2. **Sauvegarde ta clé API** : Ne la partage jamais et ne la mets pas dans ton code directement, utilise toujours le fichier `.env`

3. **Lis les messages d'erreur** : Ils te disent souvent exactement ce qui ne va pas

4. **Expérimente** : Change les modes de recherche (`naive`, `local`, `global`, `hybrid`) et vois les différences

5. **Commence avec OpenAI** : C'est plus simple pour débuter. Tu pourras essayer Ollama plus tard

6. **Surveille tes coûts** : Va sur https://platform.openai.com/usage pour voir combien tu dépenses

## Projet d'exercice

Essaie de créer un programme qui :
1. Lit plusieurs fichiers texte (tes cours, par exemple)
2. Les analyse avec LightRAG
3. Crée un petit quiz en posant des questions
4. Compare tes réponses avec celles de l'IA

## Ressources pour aller plus loin

- **Documentation officielle** : https://github.com/HKUDS/LightRAG
- **Tutoriel vidéo** : https://www.youtube.com/watch?v=g21royNJ4fw
- **Discord** : https://discord.gg/yF2MmDJyGJ (pour poser des questions)
- **Cours Python gratuit** : https://www.codecademy.com/learn/learn-python-3

## Glossaire (mots techniques expliqués)

- **API** : Interface de Programmation d'Application. C'est comme une prise électrique pour les programmes.
- **Async/Await** : Mots-clés Python pour les opérations asynchrones (qui peuvent prendre du temps).
- **Embedding** : Transformation du texte en nombres que l'ordinateur peut comprendre.
- **LLM** : Large Language Model. Un modèle d'IA entraîné sur énormément de texte.
- **Query** : Requête, question qu'on pose au système.
- **RAG** : Retrieval-Augmented Generation. Récupération d'infos + génération de réponse.
- **Storage** : Stockage, endroit où sont sauvegardées les données.

## Besoin d'aide ?

Si tu bloques :
1. Relis cette documentation
2. Vérifie que tu as bien suivi toutes les étapes
3. Cherche ton message d'erreur sur Google
4. Demande sur le Discord de LightRAG
5. Regarde les exemples dans le dossier `examples/`

## Un dernier conseil

N'aie pas peur de faire des erreurs ! La programmation, c'est beaucoup d'essais et d'erreurs. Même les développeurs professionnels passent la majorité de leur temps à débugger (corriger des erreurs).

Bonne chance et amuse-toi bien avec LightRAG ! 🚀
