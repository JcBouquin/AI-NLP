# 📁 Structure du Projet Parlant SQL

Vue d'ensemble complète de l'organisation du projet.

---

## 🌳 Arborescence

```
parlant-sql/
│
├── parlant_sql/                    # 📦 Package principal
│   ├── __init__.py                # Initialisation du package
│   ├── app.py                     # ⚙️ Logique principale SQL Agent
│   ├── module.py                  # 🔌 Module d'intégration Parlant
│   └── cli.py                     # 💻 Interface en ligne de commande
│
├── database_schema/                # 📋 Schémas des tables
│   ├── README.md                  # Documentation des schémas
│   ├── patients_table.md          # Table patients
│   ├── appointments_table.md      # Table rendez-vous
│   ├── doctors_table.md           # Table médecins
│   └── prescriptions_table.md     # Table prescriptions
│
├── text_to_sql_examples/          # 📚 Exemples Text-to-SQL
│   ├── basic_queries.md           # Requêtes simples
│   ├── join_queries.md            # Jointures
│   └── aggregations.md            # Agrégations et stats
│
├── create_demo_database.py        # 🗄️ Créateur de DB de démo
├── load_schemas.bat               # 📥 Script de chargement Windows
├── example_integration.py         # 🎯 Exemple d'intégration
│
├── README.md                      # 📖 Documentation principale
├── QUICKSTART.md                  # 🚀 Guide de démarrage rapide
├── PROJECT_STRUCTURE.md           # 📁 Ce fichier
│
├── pyproject.toml                 # 📦 Configuration Poetry
├── LICENSE                        # ⚖️ Licence Apache 2.0
└── .gitignore                     # 🚫 Fichiers à ignorer

Fichiers générés (gitignored):
├── parlant-sql-db.json           # 💾 Base des schémas
├── parlant-sql.log               # 📝 Logs
├── medical_database.db           # 🏥 Base de démo SQLite
└── __pycache__/                  # Python cache
```

---

## 📦 Composants Principaux

### 1. `parlant_sql/app.py` (485 lignes)

**Responsabilités :**
- Gestion des schémas de tables
- Génération SQL avec LLM (Chain-of-Thought)
- Validation de sécurité SQL
- Exécution des requêtes SQLite
- Formatage des résultats

**Classes principales :**
```python
class App:
    - execute_natural_language_query()  # Convertir langage naturel → SQL
    - create_schema()                    # Ajouter un schéma de table
    - list_schemas()                     # Lister les schémas
    - delete_schema()                    # Supprimer un schéma

class TableSchema:                       # Représente un schéma de table
class _SQLQuerySchema:                   # Schéma pour génération structurée
class SQLQueryResult:                    # Résultat d'une requête
```

**Flux d'exécution :**
```
Question NL → Charge schémas → LLM génère SQL → Validation sécu 
→ Exécution SQLite → Format résultats → Retour
```

---

### 2. `parlant_sql/module.py` (165 lignes)

**Responsabilités :**
- Intégration avec Parlant
- Enregistrement du tool `sql_query`
- Gestion du cycle de vie du plugin

**Classes principales :**
```python
class SqlQueryPlugin(ServicePlugin):
    - initialize()                      # Init du plugin
    - get_tool_schemas()               # Définition du tool
    - execute_tool()                   # Exécution du tool
    - cleanup()                        # Nettoyage
```

**Utilisation :**
```bash
parlant-server --module parlant_sql.module
```

---

### 3. `parlant_sql/cli.py` (220 lignes)

**Responsabilités :**
- Interface en ligne de commande
- Gestion des schémas (CRUD)
- Exécution de requêtes
- Mode interactif

**Commandes disponibles :**
```bash
parlant-sql add-schema     # Ajouter un schéma
parlant-sql list-schemas   # Lister les schémas
parlant-sql delete-schema  # Supprimer un schéma
parlant-sql query          # Exécuter une requête
parlant-sql interactive    # Mode interactif
```

---

## 📋 Fichiers de Documentation

### 1. `database_schema/*.md`

Format standard pour définir les tables :
```markdown
# Table: nom

## Description
Ce que contient la table

## Colonnes
- colonne (TYPE) - Description

## Exemples de Requêtes
SELECT ... FROM ...

## Règles de Sécurité
- Règle 1
- Règle 2
```

### 2. `text_to_sql_examples/*.md`

Exemples d'apprentissage pour le LLM :
- **basic_queries.md** : Comptages, listes, recherches
- **join_queries.md** : Jointures multi-tables
- **aggregations.md** : Statistiques et groupements

---

## 🔧 Fichiers de Configuration

### `pyproject.toml`

Configuration Poetry avec :
- Dépendances (parlant, click, aiofiles)
- Scripts CLI (entry point `parlant-sql`)
- Configuration Black, MyPy

### `.gitignore`

Ignore :
- Fichiers Python (`__pycache__`, `*.pyc`)
- Bases de données (`*.db`, `*.sqlite`)
- Fichiers générés (`parlant-sql-db.json`, `*.log`)
- Environnements virtuels (`venv/`, `.venv/`)

---

## 🚀 Scripts Utilitaires

### `create_demo_database.py`

Crée `medical_database.db` avec :
- 4 tables (patients, doctors, appointments, prescriptions)
- Données de démonstration fictives
- Utilisable immédiatement pour tests

### `load_schemas.bat`

Charge les 4 schémas de tables via CLI :
```batch
parlant-sql add-schema --name "patients" --columns ...
parlant-sql add-schema --name "appointments" --columns ...
...
```

### `example_integration.py`

Exemple complet d'agent Parlant avec :
- QNA pour FAQ statiques
- SQL pour données dynamiques
- Journey pour prise de RDV
- Guidelines pour routage intelligent

---

## 📊 Flux de Données

```
┌────────────────────────────────────────────────────────────┐
│ USER QUESTION                                               │
│ "Combien de rendez-vous ai-je ce mois ?"                  │
└──────────────────────┬─────────────────────────────────────┘
                       ↓
┌────────────────────────────────────────────────────────────┐
│ PARLANT AGENT                                              │
│ Guideline: "données dynamiques" → tool: sql_query         │
└──────────────────────┬─────────────────────────────────────┘
                       ↓
┌────────────────────────────────────────────────────────────┐
│ PARLANT SQL MODULE (module.py)                            │
│ execute_tool("sql_query", question=...)                   │
└──────────────────────┬─────────────────────────────────────┘
                       ↓
┌────────────────────────────────────────────────────────────┐
│ APP (app.py)                                               │
│ execute_natural_language_query(question)                   │
│                                                            │
│  1. _format_schema_context()                              │
│     → Charge schemas de parlant-sql-db.json              │
│                                                            │
│  2. Génère prompt avec schémas + examples                │
│                                                            │
│  3. LLM génère _SQLQuerySchema structuré:                │
│     - Analyse question                                     │
│     - Identifie tables/colonnes                           │
│     - Draft SQL → Critique → Final SQL                   │
│                                                            │
│  4. Validation sécurité:                                  │
│     - Vérifie SELECT only                                │
│     - Check dangerous keywords                            │
│     - Vérifie LIMIT                                       │
│                                                            │
│  5. Exécution SQLite:                                     │
│     - conn = sqlite3.connect(db_path)                    │
│     - cursor.execute(sql)                                │
│     - rows = cursor.fetchall()                           │
│                                                            │
│  6. Retourne SQLQueryResult                               │
└──────────────────────┬─────────────────────────────────────┘
                       ↓
┌────────────────────────────────────────────────────────────┐
│ MODULE (module.py)                                         │
│ _format_results(result) → Markdown formaté               │
└──────────────────────┬─────────────────────────────────────┘
                       ↓
┌────────────────────────────────────────────────────────────┐
│ PARLANT AGENT                                              │
│ Reçoit résultat formaté, répond au user                  │
└──────────────────────┬─────────────────────────────────────┘
                       ↓
┌────────────────────────────────────────────────────────────┐
│ USER                                                        │
│ "Vous avez 3 rendez-vous ce mois."                        │
└────────────────────────────────────────────────────────────┘
```

---

## 🎯 Points d'Entrée

### 1. CLI Standalone

```bash
parlant-sql query -q "Question"
```
→ `cli.py` → `app.py` → SQLite

### 2. Module Parlant

```bash
parlant-server --module parlant_sql.module
```
→ `module.py` → `app.py` → SQLite

### 3. Code Python

```python
from parlant_sql.app import create_persistent_app

async with create_persistent_app() as app:
    result = await app.execute_natural_language_query("Question")
```

---

## 🔒 Sécurité Multi-Couches

1. **app.py (ligne 268-286)** : Validation des keywords dangereux
2. **app.py (ligne 241-267)** : Schéma LLM avec `security_check_passed`
3. **database_schema/*.md** : Règles de sécurité par table
4. **Prompt système** : Instructions strictes SELECT-only

---

## 🧪 Tests Recommandés

```bash
# 1. Test standalone
parlant-sql query -q "Liste les patients"

# 2. Test interactif
parlant-sql interactive

# 3. Test intégration Parlant
python example_integration.py

# 4. Test avec base custom
parlant-sql query -q "Question" --db-path autre.db
```

---

## 📈 Extension Future

Ajouts possibles :
- Support PostgreSQL/MySQL (pas seulement SQLite)
- Embedding-based schema selection (pour grosses DBs)
- Cache des requêtes fréquentes
- Dashboard web de monitoring
- Tests unitaires automatisés
- CI/CD pipeline

---

**Questions ?** Consultez [README.md](README.md) ou [QUICKSTART.md](QUICKSTART.md)

