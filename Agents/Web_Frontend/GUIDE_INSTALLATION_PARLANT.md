# 📚 Guide d'Installation et d'Exécution du Web Frontend Parlant

## 🎯 Comprendre le processus

### 1. **Installation de Parlant** (package Python)

Le dossier `parlant` contient le code source du framework Parlant. Pour l'utiliser, il faut l'installer comme package Python :

```bash
# Depuis la racine du projet (GenAI)
py -m pip install -e parlant/
```

**Résultat** : Python peut maintenant importer `parlant` partout sur votre système.

**Qu'est-ce que `-e` ?** = mode "éditable" (developement mode) 
- Vous pouvez modifier le code dans `parlant/` et les changements sont immédiats
- Pas besoin de réinstaller après chaque modification

---

### 2. **Exécution de setup_agent.py**

Quand vous exécutez `setup_agent.py` :

```bash
py setup_agent.py
```

**Ce que fait le script** :

1. ✅ Importe `parlant.sdk` (depuis le package installé)
2. ✅ Crée un agent Parlant via l'API
3. ✅ Configure les guidelines (QNA, SQL, Urgence)
4. ✅ Ajoute un journey (prise de RDV)
5. ✅ **Sauvegarde l'Agent ID** dans `agent_config.txt`

**IMPORTANT** : Ce script **démarre son propre serveur Parlant temporairement** !

```python
async with p.Server() as server:  # ← Démarre un serveur Parlant temporaire
    agent = await server.create_agent(...)  # ← Crée l'agent
    # Configuration...
```

**Ce qui se passe** :
- Un serveur Parlant démarre en arrière-plan (port interne)
- L'agent est créé via l'API
- Le serveur s'arrête à la fin du script
- **L'agent est SAUVEGARDÉ dans la base de données Parlant**

---

### 3. **Dossier parlant-data**

Le dossier `parlant-data` est créé par **parlant-server** lorsqu'il démarre pour la première fois :

```
parlant-data/
├── database.db      # Base de données SQLite
├── agents/          # Agents créés
│   └── abc123...    # Votre agent
├── glossary/        # Termes du glossaire
├── guidelines/      # Guidelines configurées
└── sessions/        # Sessions de chat
```

**Quand est-il créé ?**

1. ✅ **Premier lancement** de `parlant-server`
   ```bash
   parlant-server --module parlant_qna.module --module parlant_sql.module
   ```

2. ✅ **OU lors de l'exécution** de `setup_agent.py`
   - Le `Server()` temporaire crée aussi le dossier

---

### 4. **Démarrage du Frontend**

Une fois l'agent créé :

#### Terminal 1 : Démarrage de Parlant Server
```bash
# Avant de démarrer, assurez-vous d'avoir installé les modules
py -m pip install -e ..\parlant-qna\
py -m pip install -e ..\parlant-sql\

# Puis démarrer le serveur
parlant-server --module parlant_qna.module --module parlant_sql.module --host 0.0.0.0 --port 8000
```

#### Terminal 2 : Démarrage du Frontend
```bash
cd web_frontend
py -m http.server 8080
```

#### Terminal 3 : Charger les données
```bash
# Charger les données QNA (FAQ)
cd ../mon_agent_medical
load_medical_faq.bat

# Charger les données SQL
cd ../parlant-sql
load_schemas.bat
py create_demo_database.py
```

---

## 🔄 Flux Complet

```
1. Installation de parlant
   py -m pip install -e parlant/
   │
   └─► parlant est maintenant importable partout
       
2. Exécution de setup_agent.py
   py setup_agent.py
   │
   └─► Démarre un serveur Parlant temporaire
   │   └─► Crée l'agent via API
   │       └─► Configure guidelines, journey
   │           └─► Sauvegarde dans parlant-data/database.db
   └─► Arrête le serveur temporaire
   
3. Mise à jour de chat.js
   MODIFIER: AGENT_ID = 'abc123-def456-...'
   
4. Démarrage de parlant-server (PERMANENT)
   parlant-server --module ...
   │
   └─► Lit parlant-data/database.db
   └─► Active les modules (QNA, SQL)
   └─► Attend les requêtes sur localhost:8000
   
5. Chargement des données
   load_medical_faq.bat  → Charge FAQ dans QNA module
   create_demo_database.py → Crée DB SQLite
   
6. Démarrage du frontend
   py -m http.server 8080
   │
   └─► Servit index.html sur localhost:8080
   
7. Chat dans le navigateur
   Navigateur → http://localhost:8080
   │
   └─► chat.js envoie POST à localhost:8000
       │
       └─► parlant-server traite avec l'agent
           │
           └─► Guidelines évaluent la question
               │
               ├─► Condition QNA ? → Tool: qna
               └─► Condition SQL ? → Tool: sql_query
```

---

## 📁 Structure des Dossiers

```
GenAI/
├── parlant/               # Code source du framework Parlant
│   ├── src/
│   │   └── parlant/
│   │       └── sdk.py    # API Parlant
│   └── pyproject.toml    # Config du package
│
├── parlant-qna/           # Module QNA (FAQ)
├── parlant-sql/           # Module SQL (requêtes DB)
│
├── parlant-data/          # ← CRÉÉ par parlant-server
│   ├── database.db        # SQLite avec agents, guidelines, etc.
│   ├── agents/
│   ├── glossary/
│   ├── guidelines/
│   └── sessions/
│
└── web_frontend/
    ├── setup_agent.py     # Script de configuration
    ├── chat.js            # Frontend JavaScript
    ├── index.html          # Interface HTML
    └── agent_config.txt   # ← Généré par setup_agent.py
```

---

## 🎯 Résumé

**Question** : "D'où vient parlant-data ?"
**Réponse** : Créé par `parlant-server` au premier démarrage (ou par le serveur temporaire dans `setup_agent.py`)

**Question** : "Comment setup_agent.py communique avec parlant ?"
**Réponse** : Via l'import Python `import parlant.sdk as p`. Le package doit être installé avec `pip install -e parlant/`

**Question** : "Où sont stockés les agents ?"
**Réponse** : Dans `parlant-data/database.db` (SQLite). Tous les agents sont persistés là.

**Question** : "Pourquoi deux serveurs ?"
**Réponse** :
- `Server()` dans setup_agent.py = TEMPORAIRE, juste pour créer l'agent
- `parlant-server` en ligne de commande = PERMANENT, pour servir les requêtes du frontend

---

## 🚀 Commandes Rapides

```bash
# 1. Installer parlant
py -m pip install -e parlant/

# 2. Créer l'agent
cd web_frontend
py setup_agent.py

# 3. Noter l'Agent ID affiché
# 4. Modifier chat.js (AGENT_ID)

# 5. Démarrer le serveur (Terminal 1)
parlant-server --module parlant_qna.module --module parlant_sql.module

# 6. Charger les données (Terminal 2)
cd ../mon_agent_medical && load_medical_faq.bat
cd ../parlant-sql && py create_demo_database.py

# 7. Démarrer le frontend (Terminal 3)
cd web_frontend
py -m http.server 8080

# 8. Ouvrir http://localhost:8080
```

---

## ⚠️ Problèmes Courants

**Erreur** : `ModuleNotFoundError: No module named 'parlant'`
**Solution** : `py -m pip install -e parlant/`

**Erreur** : `Agent non trouvé` dans le chat
**Solution** : Vérifier que l'Agent ID dans chat.js correspond à celui de setup_agent.py

**Erreur** : `Connection refused` dans le navigateur
**Solution** : Vérifier que parlant-server est démarré sur le port 8000

**Erreur** : `parlant-data not found`
**Solution** : Normal si jamais démarré parlant-server. Il sera créé automatiquement au premier démarrage.

