# Installation et Configuration de LightRAG

Ce document résume tout ce qui a été installé et configuré pour utiliser LightRAG avec votre document "Présentation association mairie.docx".

## Ce qui a été installé

### 1. LightRAG (version 1.4.9.9)
- Installé en mode éditable depuis le repository GitHub
- Toutes les dépendances de base sont installées
- `python-docx` installé pour lire les fichiers Word

### 2. Fichiers créés

Quatre fichiers ont été créés dans le dossier `LightRAG/` :

#### `mon_premier_test.py`
**Le fichier principal pour analyser votre document**
- Lit automatiquement le fichier Word
- Analyse le contenu avec LightRAG
- Pose 4 questions automatiques sur le document
- Mode interactif pour poser vos propres questions

#### `verifier_installation.py`
**Script de vérification avant de commencer**
- Vérifie que Python est correctement installé
- Vérifie tous les modules nécessaires
- Vérifie la configuration de la clé API
- Vérifie que votre document existe

#### `claude.md`
**Documentation technique complète**
- Pour utilisateurs avec connaissances en programmation
- Toutes les fonctionnalités avancées
- Configuration des différents backends
- Résolution de problèmes

#### `claude-debutant.md`
**Guide pour débutants (20 ans)**
- Explications simples et accessibles
- Installation pas à pas
- Exemples commentés
- Glossaire des termes techniques

#### `GUIDE_RAPIDE.md`
**Guide rapide d'utilisation**
- Comment configurer la clé API
- Comment lancer le programme
- Exemples de questions
- Résolution des problèmes courants

#### `.env`
**Fichier de configuration**
- Contient votre clé API OpenAI (à configurer)

## Étapes pour commencer

### 1. Configurer votre clé API OpenAI

**IMPORTANT** : Vous devez d'abord obtenir une clé API OpenAI

1. Allez sur https://platform.openai.com/api-keys
2. Créez un compte ou connectez-vous
3. Cliquez sur "Create new secret key"
4. Copiez la clé (elle commence par `sk-proj-...`)
5. Ouvrez le fichier `.env` dans le dossier LightRAG
6. Remplacez `sk-votre-cle-api` par votre vraie clé

Exemple :
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 2. Vérifier que tout est prêt

Ouvrez un terminal dans le dossier LightRAG et lancez :

```bash
python verifier_installation.py
```

Ce script va vérifier :
- ✓ Python 3.12.4 (compatible)
- ✓ Tous les modules nécessaires
- ✓ Votre document (Présentation association mairie.docx - 25,923 octets)
- ✓ LightRAG version 1.4.9.9
- ⚠ Clé API (à configurer)

### 3. Lancer l'analyse de votre document

Une fois la clé API configurée :

```bash
python mon_premier_test.py
```

## Ce qui va se passer

### Phase 1 : Analyse initiale (1-3 minutes)
Le programme va :
1. Lire votre document Word
2. Afficher un aperçu du contenu
3. Analyser le texte avec l'IA
4. Créer un graphe de connaissances
5. Sauvegarder les données dans `./mes_donnees_rag/`

**Note** : Cette phase est la plus longue, mais les analyses suivantes seront beaucoup plus rapides grâce au cache.

### Phase 2 : Questions automatiques
Le programme posera automatiquement 4 questions sur votre document :
- Quel est l'objet principal de cette présentation ?
- Quelles sont les informations clés mentionnées ?
- Y a-t-il des dates ou événements importants ?
- Quels sont les acteurs mentionnés ?

### Phase 3 : Mode interactif
Vous pourrez ensuite poser vos propres questions :

```
❓ Votre question : [tapez votre question ici]
```

Pour quitter : tapez `quit`, `q` ou `Ctrl+C`

## Exemples de questions à poser

Selon le contenu de votre document sur l'association et la mairie :

**Questions générales :**
- Résume-moi le document en 3 points principaux
- Quel est l'objectif de cette présentation ?
- Qui sont les interlocuteurs ou organisations mentionnés ?

**Questions spécifiques :**
- Quelles sont les activités proposées par l'association ?
- Y a-t-il un budget ou des montants mentionnés ?
- Quelles sont les dates importantes ?
- Quels sont les besoins exprimés ?

**Questions d'analyse :**
- Quels sont les points forts de cette proposition ?
- Y a-t-il des défis ou obstacles mentionnés ?
- Quelle est la relation entre l'association et la mairie ?

## Structure des fichiers

```
LightRAG/
├── mon_premier_test.py          ← Votre programme principal
├── verifier_installation.py     ← Script de vérification
├── .env                          ← Configuration (clé API)
├── Présentation association mairie.docx  ← Votre document
├── claude.md                     ← Documentation technique
├── claude-debutant.md           ← Guide débutant
├── GUIDE_RAPIDE.md              ← Guide rapide
├── README_KOSMO.md              ← Ce fichier
└── mes_donnees_rag/             ← Données analysées (créé automatiquement)
    ├── kv_store_full_docs.json
    ├── kv_store_text_chunks.json
    ├── kv_store_llm_response_cache.json
    ├── graph_chunk_entity_relation.graphml
    └── vdb_chunks.json
```

## Coûts estimés

Utilisation de l'API OpenAI (payant) :
- **Analyse initiale** : ~0,05 à 0,15 € (selon la taille du document)
- **Chaque question** : ~0,002 à 0,01 €

Pour un usage typique (1 analyse + 10 questions) : **~0,10 à 0,25 €**

Surveillez vos dépenses : https://platform.openai.com/usage

## Alternative gratuite

Si vous ne voulez pas utiliser OpenAI, vous pouvez utiliser **Ollama** (gratuit, fonctionne localement) :

1. Installez Ollama : https://ollama.ai/
2. Téléchargez les modèles :
   ```bash
   ollama pull qwen2
   ollama pull nomic-embed-text
   ```
3. Modifiez `mon_premier_test.py` (voir `claude-debutant.md` pour les détails)

**Avantage** : Gratuit, fonctionne hors ligne
**Inconvénient** : Plus lent, moins performant, nécessite un bon ordinateur

## Résolution de problèmes

### "AuthenticationError: Invalid API key"
**Cause** : Clé API incorrecte ou non configurée
**Solution** : Vérifiez votre fichier `.env` et assurez-vous d'avoir copié toute la clé

### "FileNotFoundError: Présentation association mairie.docx"
**Cause** : Document introuvable
**Solution** : Vérifiez que le fichier est dans le bon dossier

### Le programme est très lent
**C'est normal** : L'analyse prend du temps (appels API + traitement IA)
La première fois : 1-3 minutes
Les fois suivantes : beaucoup plus rapide (cache)

### Erreur d'encodage ou caractères bizarres
**Cause** : Problème d'encodage Windows
**Solution** : Le script a été conçu pour gérer cela, mais si problème persiste, contactez-moi

### "ModuleNotFoundError"
**Cause** : Module manquant
**Solution** : Lancez `python verifier_installation.py` pour identifier et installer le module manquant

## Commandes utiles

```bash
# Vérifier l'installation
python verifier_installation.py

# Lancer l'analyse
python mon_premier_test.py

# Vérifier la version de LightRAG
python -c "import lightrag; print(lightrag.__version__)"

# Installer un module manquant (exemple)
pip install python-docx

# Nettoyer et recommencer l'analyse
rm -rf mes_donnees_rag/  # ou supprimez le dossier manuellement
```

## Prochaines étapes

1. **Configurez votre clé API** dans le fichier `.env`
2. **Lancez la vérification** : `python verifier_installation.py`
3. **Analysez votre document** : `python mon_premier_test.py`
4. **Explorez les guides** :
   - `GUIDE_RAPIDE.md` pour débuter
   - `claude-debutant.md` pour comprendre les concepts
   - `claude.md` pour les fonctionnalités avancées

## Besoin d'aide ?

- **Documentation locale** : Lisez les fichiers `.md` créés
- **Documentation officielle** : https://github.com/HKUDS/LightRAG
- **Discord** : https://discord.gg/yF2MmDJyGJ
- **Tutoriel vidéo** : https://www.youtube.com/watch?v=g21royNJ4fw
- **Article détaillé** : https://learnopencv.com/lightrag

## Notes importantes

1. **Cache** : Les données analysées sont sauvegardées. Pour recommencer à zéro, supprimez `mes_donnees_rag/`

2. **Sécurité** : Ne partagez JAMAIS votre clé API. Ne commitez pas le fichier `.env` sur GitHub.

3. **Performance** : La première analyse est lente, mais les suivantes sont rapides grâce au cache LLM.

4. **Qualité** : Les réponses dépendent de la qualité du document et de la clarté des questions.

## Contact

Si vous avez des questions ou rencontrez des problèmes, n'hésitez pas à :
- Consulter les guides créés
- Lire la documentation officielle
- Rejoindre le Discord de LightRAG

Bon travail avec LightRAG ! 🚀
