# Comment lancer le programme - Guide pas à pas

## 1. Vérification : Où se trouve votre document ?

Votre document **"Présentation association mairie.docx"** se trouve ici :

```
C:\Users\kosmo\pycode\LightRAG\Présentation association mairie.docx
```

**Taille** : 25,923 octets (25 Ko)
**Dernière modification** : 14 décembre 2024

### Pour vérifier vous-même :

#### Option 1 : Avec l'explorateur Windows
1. Ouvrez l'explorateur de fichiers (Windows + E)
2. Allez dans : `C:\Users\kosmo\pycode\LightRAG\`
3. Vous devriez voir le fichier "Présentation association mairie.docx"

#### Option 2 : Avec un terminal
```bash
cd C:\Users\kosmo\pycode\LightRAG
dir "Présentation*"
```

Vous devriez voir :
```
Présentation association mairie.docx
```

---

## 2. Comment lancer le programme ?

### ÉTAPE A : Ouvrir un terminal (invite de commandes)

#### Méthode 1 - Via Windows :
1. Appuyez sur `Windows + R`
2. Tapez `cmd`
3. Appuyez sur Entrée

#### Méthode 2 - Via l'explorateur :
1. Ouvrez le dossier `C:\Users\kosmo\pycode\LightRAG\`
2. Dans la barre d'adresse, tapez `cmd` et appuyez sur Entrée
   (Le terminal s'ouvrira directement dans ce dossier !)

#### Méthode 3 - Via le menu Démarrer :
1. Clic droit sur le bouton Démarrer
2. Cliquez sur "Terminal" ou "Windows PowerShell"

---

### ÉTAPE B : Aller dans le bon dossier

Si vous n'êtes pas déjà dans le dossier LightRAG, tapez :

```bash
cd C:\Users\kosmo\pycode\LightRAG
```

Pour vérifier que vous êtes au bon endroit :
```bash
dir
```

Vous devriez voir tous les fichiers, dont :
- `mon_premier_test.py`
- `Présentation association mairie.docx`
- `.env`
- etc.

---

### ÉTAPE C : Vérifier l'installation (IMPORTANT - À FAIRE D'ABORD)

Avant de lancer le programme principal, vérifiez que tout est prêt :

```bash
python verifier_installation.py
```

#### Ce que vous devriez voir :

```
================================================================
       VERIFICATION DE L'INSTALLATION LIGHTRAG
================================================================

[Python] Version : 3.12.4
   [OK] Version compatible (>= 3.10)

[Modules] Verification des modules Python :
   [OK] LightRAG
   [OK] python-docx (pour lire les fichiers Word)
   [OK] python-dotenv (pour lire le fichier .env)
   [OK] openai (pour communiquer avec OpenAI)

[Config] Verification du fichier .env :
   [OK] Le fichier .env existe
   [OK] Cle API configuree (commence par sk-proj-...)   ← IMPORTANT !

[Document] Verification du document :
   [OK] 'Présentation association mairie.docx' existe (25,923 octets)

[LightRAG] Verification de LightRAG :
   [OK] LightRAG version 1.4.9.9 installe

============================================================
RESUME
============================================================
[OK] Python
[OK] Modules
[OK] Fichier .env          ← DOIT ÊTRE [OK] !
[OK] Document
[OK] LightRAG

==> TOUT EST PRET !
```

#### ⚠️ Si vous voyez "[ATTENTION]" ou "[PROBLEME]" :

**Pour la clé API** :
```
[ATTENTION] Vous devez remplacer la cle par votre vraie cle API
```

**Solution** :
1. Ouvrez le fichier `.env` avec un éditeur de texte (Notepad, VSCode, etc.)
2. Remplacez `sk-votre-cle-api` par votre vraie clé OpenAI
3. Sauvegardez le fichier
4. Relancez `python verifier_installation.py`

---

### ÉTAPE D : Lancer le programme principal

Une fois que TOUT EST [OK], lancez :

```bash
python mon_premier_test.py
```

---

## 3. Ce qui va se passer (étape par étape)

### Phase 1 : Démarrage (5 secondes)
```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║          🤖 LIGHTRAG - ANALYSEUR DE DOCUMENTS 🤖              ║
    ║                                                              ║
    ║  Ce programme va analyser votre document avec LightRAG      ║
    ║  et vous permettre de poser des questions dessus            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝

🚀 DÉMARRAGE DE LIGHTRAG
```

### Phase 2 : Lecture du document (10 secondes)
```
📖 LECTURE DU DOCUMENT
📄 Lecture du fichier : Présentation association mairie.docx
✅ Document lu avec succès ! (X caractères)

📝 Aperçu du contenu (200 premiers caractères) :
------------------------------------------------------------
[Début de votre document]
------------------------------------------------------------
```

### Phase 3 : Analyse par l'IA (1-3 minutes) ⏳
```
🧠 ANALYSE DU DOCUMENT PAR LIGHTRAG
⏳ Analyse en cours... (cela peut prendre 1-2 minutes)
   LightRAG est en train de :
   - Découper le texte en morceaux
   - Identifier les entités (personnes, organisations, concepts)
   - Créer des relations entre les entités
   - Construire un graphe de connaissances

✅ Document analysé et indexé avec succès !
```

**⚠️ IMPORTANT** : Cette phase est la plus longue. Ne fermez pas le programme ! Vous verrez des messages de log défiler. C'est normal.

### Phase 4 : Questions automatiques (2-3 minutes)
```
❓ SESSION DE QUESTIONS-RÉPONSES
============================================================
Question 1/4
============================================================
❓ Quel est l'objet principal de cette présentation ?

🔍 Mode de recherche : hybrid
⏳ Recherche en cours...

💬 Réponse :
------------------------------------------------------------
[La réponse générée par l'IA]
------------------------------------------------------------
```

Le programme va poser 4 questions automatiques sur votre document.

### Phase 5 : Mode interactif 🎯
```
🎯 MODE INTERACTIF
============================================================
Vous pouvez maintenant poser vos propres questions !
(Tapez 'quit' ou 'q' pour quitter)

❓ Votre question : _
```

**C'est ici que vous tapez vos questions !**

#### Exemples de questions à poser :

```
❓ Votre question : Quels sont les objectifs de l'association ?
❓ Votre question : Y a-t-il un budget mentionné ?
❓ Votre question : Quelles sont les dates importantes ?
❓ Votre question : Résume-moi le document en 5 points
❓ Votre question : Qui sont les interlocuteurs principaux ?
```

#### Pour quitter :
```
❓ Votre question : quit
```
ou
```
❓ Votre question : q
```
ou appuyez sur `Ctrl + C`

---

## 4. Schéma de lancement (résumé visuel)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Ouvrir un terminal (cmd)                                 │
│    Windows + R  →  cmd  →  Entrée                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Aller dans le dossier                                    │
│    cd C:\Users\kosmo\pycode\LightRAG                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Vérifier l'installation                                  │
│    python verifier_installation.py                          │
│                                                              │
│    → Tout [OK] ? → Continuez                               │
│    → [PROBLEME] ? → Corrigez puis recommencez              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Lancer le programme                                      │
│    python mon_premier_test.py                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Attendre l'analyse (1-3 min)                            │
│    ⏳ Patience...                                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Poser vos questions !                                    │
│    ❓ Votre question : [tapez ici]                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Commandes complètes (copier-coller)

Voici toutes les commandes à taper dans l'ordre :

```bash
# 1. Aller dans le dossier
cd C:\Users\kosmo\pycode\LightRAG

# 2. Vérifier l'installation
python verifier_installation.py

# 3. Si tout est OK, lancer le programme
python mon_premier_test.py
```

---

## 6. Problèmes fréquents et solutions

### "python n'est pas reconnu..."
**Cause** : Python n'est pas dans le PATH
**Solution** :
```bash
# Essayez avec python3
python3 mon_premier_test.py

# Ou avec le chemin complet
C:\Users\kosmo\AppData\Local\Programs\Python\Python312\python.exe mon_premier_test.py
```

### "Le fichier n'existe pas"
**Cause** : Vous n'êtes pas dans le bon dossier
**Solution** :
```bash
# Vérifiez où vous êtes
cd

# Si ce n'est pas C:\Users\kosmo\pycode\LightRAG, allez-y
cd C:\Users\kosmo\pycode\LightRAG

# Vérifiez que les fichiers sont là
dir
```

### Le programme ne démarre pas
**Solution** :
1. Relancez d'abord `python verifier_installation.py`
2. Corrigez tous les [PROBLEME]
3. Réessayez

### Le programme se bloque / ne répond plus
**C'est normal pendant l'analyse !**
- Première analyse : 1-3 minutes
- Ne fermez pas le terminal
- Attendez de voir "✅ Document analysé avec succès !"

---

## 7. Où sont sauvegardées les données ?

Après la première analyse, un nouveau dossier est créé :

```
C:\Users\kosmo\pycode\LightRAG\mes_donnees_rag\
```

Ce dossier contient :
- Le graphe de connaissances
- Les embeddings (vecteurs)
- Le cache des réponses
- Les chunks de texte

**Avantage** : La prochaine fois, ce sera beaucoup plus rapide !

**Pour recommencer à zéro** : Supprimez ce dossier

---

## 8. Après avoir terminé

Pour quitter proprement :
1. Dans le mode interactif, tapez : `quit`
2. Ou appuyez sur `Ctrl + C`
3. Vous verrez :
```
🔚 FERMETURE
✅ LightRAG fermé proprement
```

Le terminal peut être fermé.

---

## Récapitulatif ultra-rapide

```bash
# Terminal → cmd

cd C:\Users\kosmo\pycode\LightRAG
python verifier_installation.py
python mon_premier_test.py

# Attendre l'analyse
# Poser vos questions
# Taper 'quit' pour sortir
```

**Temps total** :
- Première fois : ~5 minutes
- Fois suivantes : ~30 secondes

---

## Besoin d'aide supplémentaire ?

- **DEMARRAGE_RAPIDE.txt** : Instructions ultra-courtes
- **GUIDE_RAPIDE.md** : Guide complet avec exemples
- **claude-debutant.md** : Explications détaillées pour débutants
- **README_KOSMO.md** : Vue d'ensemble complète

**Ou relancez** :
```bash
python verifier_installation.py
```

pour diagnostiquer les problèmes.
