# Guide Rapide - mon_premier_test.py

## Qu'est-ce que ce script fait ?

Ce script analyse votre document **"Présentation association mairie.docx"** avec LightRAG et vous permet de :
1. Lire automatiquement un fichier Word
2. L'analyser avec l'intelligence artificielle
3. Poser des questions sur son contenu
4. Obtenir des réponses intelligentes

## Avant de commencer

### 1. Configurer votre clé API OpenAI

Éditez le fichier `.env` et remplacez `sk-votre-cle-api` par votre vraie clé :

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Comment obtenir une clé API ?**
1. Allez sur https://platform.openai.com/
2. Créez un compte ou connectez-vous
3. Allez dans "API Keys"
4. Cliquez sur "Create new secret key"
5. Copiez la clé et collez-la dans le fichier `.env`

### 2. Vérifier que le document existe

Assurez-vous que le fichier `Présentation association mairie.docx` est bien dans le dossier LightRAG.

## Lancer le script

Ouvrez un terminal dans le dossier LightRAG et tapez :

```bash
python mon_premier_test.py
```

## Ce qui va se passer

### Phase 1 : Lecture et analyse (1-2 minutes)
Le script va :
1. Lire votre document Word
2. Afficher un aperçu du contenu
3. Analyser le texte avec LightRAG
4. Créer un graphe de connaissances

**Patience** : Cette étape prend du temps la première fois, mais les analyses futures seront plus rapides grâce au cache.

### Phase 2 : Questions automatiques
Le script va automatiquement poser 4 questions sur votre document :
- Quel est l'objet principal de cette présentation ?
- Quelles sont les informations clés mentionnées ?
- Y a-t-il des dates ou événements importants ?
- Quels sont les acteurs mentionnés ?

Vous verrez les réponses s'afficher.

### Phase 3 : Mode interactif
Vous pouvez ensuite poser vos propres questions :

```
❓ Votre question : Quels sont les objectifs de l'association ?
```

Pour quitter, tapez `quit`, `q` ou appuyez sur `Ctrl+C`.

## Exemples de questions à poser

Selon le contenu de votre document, vous pouvez demander :

**Questions générales :**
- Résume-moi le document en 3 points
- Quel est le but de cette présentation ?
- Qui sont les personnes ou organisations mentionnées ?

**Questions spécifiques :**
- Quelles sont les activités de l'association ?
- Y a-t-il un budget mentionné ?
- Quand aura lieu l'événement ?
- Quels sont les besoins exprimés ?

**Questions d'analyse :**
- Quels sont les points forts de cette proposition ?
- Y a-t-il des défis mentionnés ?
- Quelle est la relation entre [X] et [Y] ?

## Modes de recherche

Le script utilise principalement le mode **"hybrid"** (recommandé), mais vous pouvez modifier le code pour tester :

- **naive** : Recherche simple et rapide
- **local** : Cherche dans le contexte proche des mots-clés
- **global** : Cherche dans tout le graphe de connaissances
- **hybrid** : Combine local + global (meilleur équilibre)
- **mix** : Intègre graphe + vecteurs (nécessite un reranker)

Pour changer, modifiez cette ligne dans le code :
```python
param=QueryParam(mode="hybrid")  # Changez "hybrid" par un autre mode
```

## Où sont stockées les données ?

Après la première analyse, les données sont sauvegardées dans le dossier :
```
./mes_donnees_rag/
```

**Avantage** : La prochaine fois que vous lancez le script, il réutilisera ces données et sera beaucoup plus rapide !

**Pour recommencer à zéro** : Supprimez ce dossier.

## Résolution de problèmes

### "AuthenticationError: Invalid API key"
**Problème** : Votre clé API n'est pas valide.
**Solution** : Vérifiez votre fichier `.env` et assurez-vous d'avoir copié toute la clé.

### "FileNotFoundError: Présentation association mairie.docx"
**Problème** : Le document n'est pas trouvé.
**Solution** : Vérifiez que le fichier est bien dans le même dossier que le script.

### Le script est lent
**C'est normal** : L'analyse d'un document peut prendre 1-3 minutes selon sa taille. Les appels à l'API OpenAI prennent du temps.

### "ModuleNotFoundError: No module named 'docx'"
**Problème** : La bibliothèque python-docx n'est pas installée.
**Solution** :
```bash
pip install python-docx
```

### Erreurs d'encodage avec les accents
Si vous voyez des caractères bizarres à la place des accents, essayez de modifier l'encodage :
```python
doc = Document(chemin_fichier)
# Si problème, ajoutez encoding='utf-8' aux print()
```

## Coûts

L'utilisation de l'API OpenAI coûte de l'argent, mais pour un document typique :
- Analyse initiale : ~0,01 à 0,10 € (selon la taille)
- Chaque question : ~0,001 à 0,01 €

**Surveillez vos dépenses** : https://platform.openai.com/usage

## Personnaliser le script

### Changer le document à analyser

Modifiez cette ligne :
```python
DOCUMENT_PATH = "Présentation association mairie.docx"
```

### Ajouter vos propres questions automatiques

Modifiez cette liste :
```python
questions = [
    "Votre question 1 ?",
    "Votre question 2 ?",
    # Ajoutez d'autres questions...
]
```

### Désactiver le mode interactif

Commentez ou supprimez la section "MODE INTERACTIF" dans le code (lignes 130-170 environ).

## Alternative gratuite : Ollama

Si vous ne voulez pas utiliser OpenAI (payant), vous pouvez utiliser Ollama (gratuit, local) :

1. Installez Ollama : https://ollama.ai/
2. Téléchargez les modèles :
   ```bash
   ollama pull qwen2
   ollama pull nomic-embed-text
   ```
3. Modifiez le script pour utiliser Ollama (voir `claude-debutant.md`)

## Aller plus loin

- Lisez `claude.md` pour la documentation complète
- Lisez `claude-debutant.md` pour comprendre les concepts
- Regardez les exemples dans le dossier `examples/`
- Consultez la documentation officielle : https://github.com/HKUDS/LightRAG

## Besoin d'aide ?

- Discord LightRAG : https://discord.gg/yF2MmDJyGJ
- Issues GitHub : https://github.com/HKUDS/LightRAG/issues
- Documentation complète : https://github.com/HKUDS/LightRAG/blob/main/README.md
