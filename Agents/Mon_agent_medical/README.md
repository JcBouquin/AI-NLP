# Agent Médical Simple

Un agent conversationnel basé sur Parlant qui aide avec :
- 🗓️ Prise de rendez-vous
- 💊 Questions médicales (via parlant-qna)
- 📞 Informations du cabinet

## 🚀 Installation

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Configurer OpenAI
```bash
# Copier le fichier .env et ajouter votre clé API
# Éditez .env et remplacez "sk-votre-clé-ici" par votre vraie clé OpenAI
```

Obtenez votre clé API sur : https://platform.openai.com/api-keys

## ▶️ Lancement

### Étape 1 : Lancer parlant-qna (Terminal 1)

```bash
# Démarrer le service RAG
parlant-qna serve
```

### Étape 2 : Charger les FAQ médicales (Terminal 1)

**Option A : Script automatique (recommandé)**
```bash
# Windows
load_medical_faq.bat

# Linux/Mac
bash load_medical_faq.sh
```

**Option B : Manuellement**
```bash
parlant-qna add -q "Qu'est-ce qu'une IRM ?" -a "..."
parlant-qna add -q "C'est quoi un scanner ?" -a "..."
# etc.
```

**Note :** Les FAQ sont stockées dans `medical_faq/*.md` pour référence, mais doivent être chargées via `parlant-qna add`

### Étape 3 : Lancer l'agent (Terminal 2)

```bash
# Démarrer l'agent médical
python my_healthcare_agent.py --module parlant_qna.module
```

## 💬 Exemples d'utilisation

Une fois lancé, vous pouvez interagir :

### 🗓️ Prise de rendez-vous :
- "Je voudrais prendre rendez-vous"
- "J'ai besoin de consulter un cardiologue"

### ℹ️ Informations spécifiques au cabinet (via RAG) :
- "Quels sont vos horaires ?"
- "Qui sont les médecins disponibles ?"
- "Combien coûte une consultation ?"
- "Comment annuler mon rendez-vous ?"
- "Où êtes-vous situés ?"

### 🏥 Questions médicales générales (LLM direct) :
- "C'est quoi une IRM ?"
- "Quels sont les symptômes d'une grippe ?"
- "Comment prévenir l'hypertension ?"

### 🚨 Urgence :
- "C'est urgent, j'ai très mal !"

**Note :** Le RAG est utilisé UNIQUEMENT pour les informations spécifiques au cabinet. Pour les connaissances médicales générales, le LLM répond directement (plus rapide et tout aussi précis).

## 🏗️ Structure

```
mon_agent_medical/
├── my_healthcare_agent.py         # Code de l'agent
├── requirements.txt               # Dépendances
├── .env                           # Configuration API (à créer)
├── load_medical_faq.bat           # Script chargement FAQ (Windows)
├── load_medical_faq.sh            # Script chargement FAQ (Linux/Mac)
├── CONFIGURATION.md               # Guide configuration OpenAI
├── README.md                      # Ce fichier
└── medical_faq/                   # FAQ spécifiques au cabinet
    ├── README.md                  # Explication RAG vs LLM
    ├── horaires_cabinet.md        # Horaires d'ouverture
    ├── medecins_equipe.md         # Équipe médicale
    ├── politique_annulation.md    # Règles annulation
    ├── tarifs_remboursements.md   # Prix et remboursements
    └── contact_acces.md           # Coordonnées et accès
```

## 🔧 Personnalisation

### Modifier les FAQ du cabinet
Éditez les fichiers dans `medical_faq/` avec VOS vraies informations :
- Vos horaires réels
- Votre équipe médicale
- Vos tarifs
- Votre adresse

### Modifier l'agent
Éditez `my_healthcare_agent.py` pour :
- Ajouter d'autres journeys (examens, prescriptions, etc.)
- Créer de nouvelles guidelines
- Définir vos propres tools
- Adapter le glossaire médical

### Comprendre RAG vs LLM
Lisez `GUIDE_RAG.md` pour savoir quelles informations mettre dans le RAG

## 📚 Documentation

- [Parlant Docs](https://www.parlant.io/docs)
- [Parlant-QNA](https://pypi.org/project/parlant-qna/)

