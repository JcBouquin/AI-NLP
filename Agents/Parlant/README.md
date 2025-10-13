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

### Étape 2 : Ajouter des FAQ médicales (Terminal 1)

```bash
parlant-qna add -q "Qu'est-ce qu'une IRM ?" -a "Une IRM (Imagerie par Résonance Magnétique) est un examen d'imagerie médicale qui utilise un champ magnétique puissant pour créer des images détaillées des organes et tissus internes."

parlant-qna add -q "C'est quoi un scanner ?" -a "Un scanner (tomodensitométrie) est un examen qui utilise des rayons X pour créer des images en coupes du corps. Il permet de visualiser les structures internes avec précision."

parlant-qna add -q "Qu'est-ce qu'une prise de sang ?" -a "Une prise de sang est un prélèvement de sang veineux utilisé pour analyser divers paramètres biologiques (glycémie, cholestérol, etc.)."
```

### Étape 3 : Lancer l'agent (Terminal 2)

```bash
# Démarrer l'agent médical
python my_healthcare_agent.py --module parlant_qna.module
```

## 💬 Exemples d'utilisation

Une fois lancé, vous pouvez interagir :

- **Prendre rendez-vous :**
  - "Je voudrais prendre rendez-vous"
  - "J'ai besoin de consulter"

- **Questions médicales :**
  - "C'est quoi une IRM ?"
  - "Qu'est-ce qu'un scanner ?"

- **Urgence :**
  - "C'est urgent, j'ai très mal !"

- **Informations :**
  - "Quels sont vos horaires ?"
  - "Quel est votre numéro ?"

## 🏗️ Structure

```
mon_agent_medical/
├── requirements.txt           # Dépendances
├── my_healthcare_agent.py     # Code de l'agent
└── README.md                  # Ce fichier
```

## 🔧 Personnalisation

Modifiez `my_healthcare_agent.py` pour :
- Ajouter d'autres journeys
- Créer de nouvelles guidelines
- Définir vos propres tools
- Adapter le glossaire médical

## 📚 Documentation

- [Parlant Docs](https://www.parlant.io/docs)
- [Parlant-QNA](https://pypi.org/project/parlant-qna/)

