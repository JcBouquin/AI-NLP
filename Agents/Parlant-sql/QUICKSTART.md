# 🚀 Quickstart Guide - Parlant SQL

Guide de démarrage rapide en 5 minutes.

---

## ⚡ Installation Express

```bash
# 1. Cloner ou naviguer vers le projet
cd parlant-sql

# 2. Installer les dépendances
pip install -e .

# 3. Vérifier l'installation
parlant-sql --help
```

---

## 🎯 Premier Test (Standalone)

### 1. Créer une base de données de démo

```bash
python create_demo_database.py
```

✅ **Résultat :** `medical_database.db` créée avec des données de test

### 2. Charger les schémas de tables

```bash
load_schemas.bat  # Windows
# ou
./load_schemas.sh  # Linux/Mac
```

✅ **Résultat :** Schémas enregistrés dans `parlant-sql-db.json`

### 3. Tester une requête

```bash
parlant-sql query -q "Combien de patients avons-nous ?"
```

✅ **Résultat :**
```
📊 Question: Combien de patients avons-nous ?
🔍 SQL Generated: SELECT COUNT(*) FROM patients;
💡 Explanation: Je compte tous les patients dans la base.
✅ Results (1 row(s)): 1. {'COUNT(*)': 8}
🎯 Confidence: high
```

### 4. Mode interactif

```bash
parlant-sql interactive
```

Testez différentes questions :
- "Qui sont nos médecins ?"
- "Rendez-vous d'aujourd'hui ?"
- "Quel médecin est le plus sollicité ?"

---

## 🔗 Intégration avec Parlant

### 1. Démarrer Parlant avec le module SQL

```bash
parlant-server --module parlant_sql.module
```

### 2. Utiliser dans votre agent

```python
import parlant.sdk as p

async with p.Server() as server:
    agent = await server.create_agent(
        name="Mon Agent SQL",
        description="Agent avec accès base de données"
    )
    
    # Guideline pour utiliser SQL
    await agent.create_guideline(
        condition="Questions sur données dynamiques",
        tools=["sql_query"]
    )
```

### 3. Tester via l'interface Parlant

```
User: "Combien de rendez-vous ai-je ce mois ?"
Agent: [Utilise sql_query] "Vous avez 3 rendez-vous ce mois."
```

---

## 🏥 Exemple Médical Complet (QNA + SQL)

Combiner FAQ statiques et base de données dynamique :

```bash
# Terminal 1 : Démarrer avec QNA et SQL
parlant-server \
  --module parlant_qna.module \
  --module parlant_sql.module

# Terminal 2 : Charger les FAQs
cd ../mon_agent_medical
load_medical_faq.bat

# Terminal 3 : Charger les schémas SQL
cd ../parlant-sql
load_schemas.bat

# Terminal 4 : Lancer l'agent
python example_integration.py
```

**Résultat :**
- "Quels sont vos horaires ?" → QNA (FAQ statique)
- "Combien de rendez-vous ai-je ?" → SQL (base dynamique)
- "Je veux prendre RDV" → Journey (parcours guidé)

---

## 📊 Commandes Utiles

```bash
# Lister les schémas enregistrés
parlant-sql list-schemas

# Ajouter un nouveau schéma
parlant-sql add-schema \
  --name "ma_table" \
  --description "Description" \
  --columns "id:INTEGER" \
  --columns "name:TEXT"

# Supprimer un schéma
parlant-sql delete-schema <schema_id>

# Query avec format JSON
parlant-sql query -q "Question" --format json

# Query avec base custom
parlant-sql query -q "Question" --db-path custom.db
```

---

## 🐛 Troubleshooting

### Erreur : "Module not found: parlant_sql"

```bash
pip install -e .
```

### Erreur : "Database file not found"

```bash
python create_demo_database.py
```

### Erreur : "No schemas registered"

```bash
load_schemas.bat
```

### Requête bloquée pour sécurité

✅ **Normal** ! Seules les requêtes SELECT sont autorisées.

---

## 📚 Prochaines Étapes

1. ✅ Lire le [README complet](README.md)
2. ✅ Explorer les [exemples text-to-sql](text_to_sql_examples/)
3. ✅ Personnaliser les [schémas de tables](database_schema/)
4. ✅ Intégrer dans votre [agent Parlant](example_integration.py)

---

**Besoin d'aide ?** Consultez la documentation complète dans [README.md](README.md)

