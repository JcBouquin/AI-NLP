# Processus Détaillé - Du Question à la Réponse

## 📋 Vue d'Ensemble

Ce document explique **étape par étape** ce qui se passe quand vous posez une question au serveur MCP CrewAI.

## 🔄 Schéma du Flux Complet

```
┌─────────────────┐
│ Claude Desktop  │
│  (Utilisateur)  │
└────────┬────────┘
         │ 1. Question posée
         ↓
┌─────────────────────────────────────────────────┐
│         PROTOCOLE MCP (JSON-RPC)                │
│  Communication standardisée entre applications  │
└────────┬────────────────────────────────────────┘
         │ 2. Appel JSON au serveur
         ↓
┌─────────────────────────────────────────────────┐
│              SERVER.PY                          │
│  • Réception de l'appel MCP                     │
│  • Routage vers le bon outil                    │
│  • Gestion des erreurs                          │
└────────┬────────────────────────────────────────┘
         │ 3. Délégation à PharmacyResearchCrew
         ↓
┌─────────────────────────────────────────────────┐
│         PHARMACY_CREW.PY                        │
│  • Orchestration des 3 agents CrewAI           │
│  • Accès aux documents                          │
│  • Coordination du travail d'équipe             │
└────────┬────────────────────────────────────────┘
         │ 4. Exécution séquentielle
         ↓
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   AGENT 1:       │→ │   AGENT 2:       │→ │   AGENT 3:       │
│   Chercheur      │  │   Analyste       │  │   Expert         │
│                  │  │                  │  │                  │
│ • Lit les docs   │  │ • Synthétise     │  │ • Formule la     │
│ • Extrait infos  │  │ • Structure      │  │   réponse finale │
│ • Transmet       │  │ • Transmet       │  │ • Valide         │
└──────────────────┘  └──────────────────┘  └──────────────────┘
         │                      │                      │
         └──────────────────────┴──────────────────────┘
                                │ 5. Résultat final
                                ↓
┌─────────────────────────────────────────────────┐
│              SERVER.PY                          │
│  • Réception du résultat                       │
│  • Formatage en réponse MCP                     │
│  • Envoi JSON-RPC                               │
└────────┬────────────────────────────────────────┘
         │ 6. Réponse MCP
         ↓
┌─────────────────────────────────────────────────┐
│         PROTOCOLE MCP (JSON-RPC)                │
└────────┬────────────────────────────────────────┘
         │ 7. Affichage
         ↓
┌─────────────────┐
│ Claude Desktop  │
│  (Utilisateur)  │
│  RÉPONSE ! ✅   │
└─────────────────┘
```

## 📝 Exemple Concret

### Question de l'Utilisateur
> "Quels sont les programmes de fidélité mentionnés dans les documents?"

---

## 🔍 Étape par Étape

### ÉTAPE 1: Claude Desktop (Client MCP)

**Ce qui se passe:**
- L'utilisateur pose la question dans Claude Desktop
- Claude Desktop identifie qu'il faut utiliser le serveur `crewai-mcp-ex1`
- L'outil `analyze_pharmacy_question` est sélectionné

**Message JSON envoyé:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "analyze_pharmacy_question",
    "arguments": {
      "question": "Quels sont les programmes de fidélité mentionnés dans les documents?"
    }
  }
}
```

**Fichier concerné:** Aucun (client externe)

---

### ÉTAPE 2: server.py - Réception de l'Appel

**Fichier:** `server.py`

**Fonction appelée:** `handle_call_tool()` (ligne 138)

**Ce qui se passe:**
```python
@server.call_tool()
async def handle_call_tool(
    name: str,                    # "analyze_pharmacy_question"
    arguments: dict[str, Any]     # {"question": "Quels sont..."}
) -> list[TextContent]:
```

**Actions:**
1. Vérification: Est-ce que `pharmacy_crew` existe?
   - Si non, initialisation avec le chemin absolu vers `pharmacy_docs/`

```python
if pharmacy_crew is None:
    docs_dir = Path(__file__).parent / "pharmacy_docs"
    pharmacy_crew = PharmacyResearchCrew(docs_directory=str(docs_dir))
```

2. Routage vers le bon handler selon le nom de l'outil
3. Extraction de la question depuis les arguments

```python
if name == "analyze_pharmacy_question":
    question = arguments.get("question")
```

**État actuel:**
- Question extraite: ✅
- PharmacyResearchCrew initialisé: ✅
- Prêt à déléguer: ✅

---

### ÉTAPE 3: server.py - Délégation à CrewAI

**Fichier:** `server.py` (ligne 154-156)

**Code:**
```python
# Analyser la question avec CrewAI
result = pharmacy_crew.answer_question(question)
```

**Ce qui se passe:**
- Le serveur MCP appelle la méthode `answer_question()` de la classe `PharmacyResearchCrew`
- Passage de la question en paramètre
- **Attente de la réponse** (30-90 secondes)

---

### ÉTAPE 4: pharmacy_crew.py - Initialisation

**Fichier:** `pharmacy_crew.py`

**Classe:** `PharmacyResearchCrew`

**Ce qui a été fait à l'initialisation:**

```python
def __init__(self, docs_directory="./pharmacy_docs"):
    self.docs_directory = docs_directory

    # 1. Charger TOUS les documents en mémoire
    self.documents = self._load_all_documents()

    # 2. Créer les 3 agents
    self.researcher = self._create_researcher()
    self.analyst = self._create_analyst()
    self.expert = self._create_expert()
```

**État de la mémoire:**
```python
self.documents = {
    "complements_alimentaires.txt": "contenu complet...",
    "cosmetiques.txt": "contenu complet...",
    "dermatologie.txt": "contenu complet...",
    "fidelisation_client.txt": "contenu complet...",  # 👈 Celui-ci nous intéresse!
    "medicaments_otc.txt": "contenu complet..."
}
```

---

### ÉTAPE 5: pharmacy_crew.py - Création des Tâches

**Fichier:** `pharmacy_crew.py` (ligne 128)

**Méthode appelée:** `answer_question(question)`

**Code:**
```python
def answer_question(self, question: str) -> str:
    # 1. Créer les tâches spécifiques à cette question
    tasks = self.create_task_for_question(question)
```

**Méthode:** `create_task_for_question()` (ligne 94)

**3 tâches créées:**

#### Tâche 1: Recherche
```python
research_task = Task(
    description=f"""Rechercher des informations sur: '{question}'

    Analyse tous les documents disponibles dans ton backstory
    et extrais les informations pertinentes.""",

    expected_output="Liste des informations pertinentes trouvées",
    agent=self.researcher
)
```

#### Tâche 2: Analyse
```python
analysis_task = Task(
    description=f"Analyser les informations trouvées pour: '{question}'",
    expected_output="Synthèse structurée des informations pertinentes",
    agent=self.analyst,
    context=[research_task]  # 👈 Dépend de la tâche précédente
)
```

#### Tâche 3: Expertise
```python
expert_task = Task(
    description=f"Répondre à la question: '{question}'",
    expected_output="Réponse complète et précise à la question",
    agent=self.expert,
    context=[analysis_task]  # 👈 Dépend de la tâche précédente
)
```

---

### ÉTAPE 6: pharmacy_crew.py - Création du Crew

**Fichier:** `pharmacy_crew.py` (ligne 140)

**Code:**
```python
crew = Crew(
    agents=[self.researcher, self.analyst, self.expert],
    tasks=[research_task, analysis_task, expert_task],
    verbose=False,           # Pas de logs parasites
    process=Process.sequential  # Les tâches s'exécutent dans l'ordre
)
```

**Schéma d'exécution:**
```
Task 1 (Recherche) → Task 2 (Analyse) → Task 3 (Expertise)
     ↓                    ↓                    ↓
  Chercheur            Analyste             Expert
```

---

### ÉTAPE 7: Agent 1 - Le Chercheur

**Fichier:** `pharmacy_crew.py` (ligne 48)

**Agent:** `Chercheur Pharmaceutique`

**Rôle:** Trouver les informations pertinentes

**Backstory (important!):**
```python
backstory=f"""Tu es un chercheur pharmaceutique expérimenté...

Tu as accès aux documents suivants:
{docs_context}  # 👈 TOUS les documents sont dans le contexte!

Utilise ces documents pour répondre aux questions."""
```

**Ce qu'il voit:**
```
=== DOCUMENTS DISPONIBLES ===

--- complements_alimentaires.txt ---
[contenu complet]

--- cosmetiques.txt ---
[contenu complet]

--- dermatologie.txt ---
[contenu complet]

--- fidelisation_client.txt ---
[contenu complet du fichier]
Programmes de fidélité:
1. Carte de fidélité avec système de points...
2. Programme de parrainage...
3. Événements exclusifs...
[etc.]

--- medicaments_otc.txt ---
[contenu complet]
```

**Action du chercheur:**
1. Lit **TOUS** les documents dans son contexte
2. Identifie que `fidelisation_client.txt` contient la réponse
3. Extrait les informations sur les programmes de fidélité
4. **Produit:** Liste des programmes trouvés

**Output de l'Agent 1:**
```
Informations trouvées sur les programmes de fidélité:

1. Carte de fidélité avec système de points ou remises
   - Accumulation de points à chaque achat
   - Conversion en réductions

2. Programme de parrainage
   - Récompenses pour recommandation de clients
   - Avantages pour le parrain et le filleul

3. Événements exclusifs
   - Ateliers santé/beauté
   - Consultations personnalisées

[etc.]

Source: fidelisation_client.txt
```

**Modèle utilisé:** GPT-4o-mini (via OpenAI API)

---

### ÉTAPE 8: Agent 2 - L'Analyste

**Fichier:** `pharmacy_crew.py` (ligne 69)

**Agent:** `Analyste de Données Pharmaceutiques`

**Rôle:** Synthétiser et structurer les informations

**Input:** Reçoit l'output de l'Agent 1 via le contexte

**Action de l'analyste:**
1. Lit la liste brute du chercheur
2. Organise les informations de manière structurée
3. Identifie les catégories et hiérarchies
4. Prépare une synthèse claire

**Output de l'Agent 2:**
```
SYNTHÈSE STRUCTURÉE:

Les programmes de fidélité identifiés se classent en 3 catégories:

A. Programmes transactionnels
   - Carte de fidélité (points/remises)
   - Objectif: Récompenser les achats réguliers

B. Programmes relationnels
   - Parrainage client
   - Objectif: Développer le réseau de clients

C. Programmes expérientiels
   - Événements exclusifs
   - Objectif: Créer un lien émotionnel

Chaque programme vise à fidéliser mais avec des mécaniques différentes.
```

**Modèle utilisé:** GPT-4o-mini (via OpenAI API)

---

### ÉTAPE 9: Agent 3 - L'Expert

**Fichier:** `pharmacy_crew.py` (ligne 81)

**Agent:** `Expert en Pharmacie`

**Rôle:** Formuler la réponse finale pour l'utilisateur

**Configuration spéciale:**
```python
llm=ChatOpenAI(temperature=0.2, model="gpt-4o-mini")
# Temperature basse = réponses plus précises et moins créatives
```

**Input:** Reçoit la synthèse de l'Agent 2 via le contexte

**Action de l'expert:**
1. Lit la synthèse structurée
2. Adapte le langage pour l'utilisateur final
3. S'assure que la réponse est complète et précise
4. Ajoute des explications si nécessaire
5. **Produit la réponse finale**

**Output de l'Agent 3 (RÉPONSE FINALE):**
```
D'après les documents analysés, voici les principaux programmes
de fidélité mentionnés pour les pharmacies:

1. **Carte de fidélité avec système de points**
   Les clients accumulent des points à chaque achat qui peuvent
   être convertis en réductions sur leurs futurs achats. Ce système
   récompense la régularité et encourage les clients à revenir.

2. **Programme de parrainage**
   Les clients actuels peuvent recommander la pharmacie à leur
   entourage. Le parrain et le nouveau client bénéficient tous
   deux d'avantages (réductions ou cadeaux).

3. **Événements exclusifs pour membres**
   Organisation d'ateliers santé/beauté et consultations
   personnalisées réservés aux membres du programme de fidélité.
   Cela crée une relation privilégiée avec les clients fidèles.

Ces programmes visent à créer une relation durable avec les
clients en combinant récompenses matérielles et expériences
personnalisées.
```

**Modèle utilisé:** GPT-4o-mini avec temperature=0.2

---

### ÉTAPE 10: pharmacy_crew.py - Retour du Résultat

**Fichier:** `pharmacy_crew.py` (ligne 147)

**Code:**
```python
result = crew.kickoff()  # Lance l'exécution des 3 agents
return str(result)       # Convertit en string et retourne
```

**Ce qui se passe:**
- Le Crew exécute les 3 tâches séquentiellement
- Chaque agent passe son output au suivant
- Le résultat final (output de l'Expert) est retourné
- Format: String (texte simple)

---

### ÉTAPE 11: server.py - Formatage de la Réponse

**Fichier:** `server.py` (ligne 157)

**Code:**
```python
return [TextContent(type="text", text=f"✅ Analyse complète:\n\n{result}")]
```

**Ce qui se passe:**
- Le serveur reçoit la string de CrewAI
- Formate en objet `TextContent` (format MCP)
- Ajoute un préfixe "✅ Analyse complète:"
- Retourne au protocole MCP

**Format MCP:**
```python
[
    TextContent(
        type="text",
        text="✅ Analyse complète:\n\n[La réponse de l'expert]"
    )
]
```

---

### ÉTAPE 12: Protocole MCP - Envoi au Client

**Format JSON-RPC envoyé:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "✅ Analyse complète:\n\nD'après les documents analysés..."
      }
    ]
  }
}
```

---

### ÉTAPE 13: Claude Desktop - Affichage

**Ce qui se passe:**
- Claude Desktop reçoit la réponse JSON
- Parse le format MCP
- Extrait le texte
- **Affiche la réponse à l'utilisateur**

---

## ⏱️ Timing Détaillé

| Étape | Durée | Action |
|-------|-------|--------|
| 1-2 | ~50ms | Communication MCP + routage |
| 3-4 | ~100ms | Initialisation CrewAI (si première fois) |
| 5-6 | ~200ms | Création des tâches et du Crew |
| 7 | **10-20s** | Agent 1: Recherche dans les documents |
| 8 | **10-20s** | Agent 2: Analyse et synthèse |
| 9 | **10-30s** | Agent 3: Formulation finale |
| 10-13 | ~100ms | Retour et affichage |
| **TOTAL** | **30-90s** | Temps total de bout en bout |

## 🔑 Points Clés à Retenir

### 1. Tous les Documents Sont en Mémoire
```python
# Lors de l'initialisation
self.documents = self._load_all_documents()

# Les 5 fichiers .txt sont chargés ENTIÈREMENT en RAM
# Les agents y ont accès via leur backstory
```

### 2. Processus Séquentiel
```
Chercheur → Analyste → Expert
   (1)        (2)       (3)

Chaque agent reçoit l'output du précédent via "context"
```

### 3. Utilisation de l'API OpenAI
```python
# Chaque agent fait des appels à GPT-4o-mini
from langchain_openai import ChatOpenAI

# 3 agents × 1 appel API = 3 appels minimum par question
# Coût: ~$0.001-0.003 par question
```

### 4. Chemins Absolus
```python
# IMPORTANT: Utilisation de chemins absolus
docs_dir = Path(__file__).parent / "pharmacy_docs"

# Évite les problèmes de working directory
```

### 5. Mode Silencieux
```python
verbose=False                      # Pas de logs CrewAI
logging.getLogger().setLevel(CRITICAL)  # Pas de logs Python
os.environ["CREWAI_TELEMETRY_OPTOUT"] = "true"  # Pas de telemetry

# Résultat: Communication MCP propre
```

## 📊 Flux de Données

```
Question (string)
    ↓
JSON MCP
    ↓
server.py (handle_call_tool)
    ↓
pharmacy_crew.answer_question(string)
    ↓
create_task_for_question() → [Task1, Task2, Task3]
    ↓
Crew.kickoff()
    ↓
Agent 1: docs_context (5 fichiers) → output1 (string)
    ↓
Agent 2: input=output1 → output2 (string)
    ↓
Agent 3: input=output2 → output3 (string) = RÉPONSE FINALE
    ↓
return str(result) → server.py
    ↓
TextContent(text=result)
    ↓
JSON MCP
    ↓
Affichage Claude Desktop
```

## 🎯 Résumé Ultra-Simplifié

1. **Claude Desktop** envoie la question au **serveur MCP**
2. **server.py** route vers **pharmacy_crew**
3. **pharmacy_crew** crée 3 agents qui travaillent en équipe:
   - **Chercheur**: Fouille dans les 5 documents → trouve les infos
   - **Analyste**: Structure les infos → crée une synthèse
   - **Expert**: Formule la réponse finale → texte pour l'utilisateur
4. La réponse remonte via **server.py** puis **MCP**
5. **Claude Desktop** affiche la réponse

**Temps total:** 30-90 secondes
**Fichiers lus:** Les 5 documents .txt (automatiquement)
**Appels API:** 3 appels à GPT-4o-mini (un par agent)

---

**Fichiers impliqués:**
- `server.py` - Point d'entrée MCP et routage
- `pharmacy_crew.py` - Orchestration CrewAI et agents
- `pharmacy_docs/*.txt` - Documents source (5 fichiers)

**Dépendances externes:**
- OpenAI API (GPT-4o-mini)
- Protocol MCP (Claude Desktop)
- CrewAI framework
- LangChain

---

*Document créé le 2025-11-10*
*Version: 1.0.0*
