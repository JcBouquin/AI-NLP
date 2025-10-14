# 🗄️ Parlant SQL - Text-to-SQL Tool Service

<div align="center">

**Un service d'agent SQL qui convertit le langage naturel en requêtes SQL sécurisées pour les agents Parlant**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

</div>

---

## 📖 Table des Matières

- [Vue d'ensemble](#-vue-densemble)
- [Caractéristiques](#-caractéristiques)
- [Installation](#-installation)
- [Démarrage Rapide](#-démarrage-rapide)
- [Utilisation](#-utilisation)
- [Intégration Parlant](#-intégration-parlant)
- [Architecture](#-architecture)
- [Sécurité](#-sécurité)
- [Exemples](#-exemples)

---

## 🎯 Vue d'ensemble

**Parlant SQL** est un outil spécialisé qui permet à vos agents Parlant d'interroger des bases de données SQL en langage naturel. Inspiré de `parlant-qna`, il applique le même principe de **traçabilité** et **anti-hallucination** aux requêtes de bases de données.

### Cas d'usage

- 🏥 **Systèmes médicaux** : "Combien de rendez-vous ai-je avec le Dr. Martin ?"
- 📊 **Analytics business** : "Quel est notre produit le plus vendu ce mois ?"
- 👥 **Support client** : "Affiche mes dernières commandes"
- 📈 **Reporting** : "Quelle est notre croissance ce trimestre ?"

---

## ✨ Caractéristiques

### 🛡️ Sécurité Avancée
- ✅ **Requêtes SELECT uniquement** (pas de DELETE/UPDATE/DROP)
- ✅ **Validation SQL stricte** avant exécution
- ✅ **Détection de SQL injection**
- ✅ **Approbation humaine** pour requêtes sensibles
- ✅ **Masquage de données** sensibles (numéros sécu, mots de passe)

### 🧠 Intelligence LLM
- ✅ **Chain-of-Thought** pour génération SQL
- ✅ **Draft → Critique → Révision** (comme QNA)
- ✅ **Explication en français** de chaque requête
- ✅ **Détection de confiance** (high/medium/low)
- ✅ **Gestion d'erreurs** intelligente

### 📝 Traçabilité Complète
- ✅ **Logging détaillé** de toutes les requêtes
- ✅ **SQL généré** visible et auditable
- ✅ **Métadonnées** (confiance, nombre de résultats, temps d'exécution)

### 🔌 Intégration Parlant
- ✅ **Module Parlant** prêt à l'emploi
- ✅ **Outil `sql_query`** utilisable dans les guidelines
- ✅ **Compatible** avec QNA et autres tools

---

## 📦 Installation

### Prérequis
- Python 3.10+
- Parlant framework installé
- OpenAI API key configurée

### Installation via pip (quand publié)
```bash
pip install parlant-sql
```

### Installation en développement
```bash
cd parlant-sql
pip install -e .
```

---

## 🚀 Démarrage Rapide

### 1. Créer une base de données de démonstration

```bash
python create_demo_database.py
```

Cela crée `medical_database.db` avec :
- 4 médecins
- 8 patients  
- 50 rendez-vous
- 20 prescriptions

### 2. Charger les schémas de tables

```bash
# Windows
load_schemas.bat

# Linux/Mac
chmod +x load_schemas.sh
./load_schemas.sh
```

### 3. Tester une requête

```bash
parlant-sql query -q "Combien de rendez-vous avons-nous aujourd'hui ?"
```

**Résultat :**
```
📊 Question: Combien de rendez-vous avons-nous aujourd'hui ?

🔍 SQL Generated:
SELECT COUNT(*) as total FROM appointments WHERE DATE(appointment_date) = DATE('now');

💡 Explanation:
Je compte tous les rendez-vous dont la date est aujourd'hui.

✅ Results (1 row(s)):
  1. {'total': 5}

🎯 Confidence: high
```

### 4. Mode interactif

```bash
parlant-sql interactive
```

---

## 💻 Utilisation

### CLI - Ajouter un schéma de table

```bash
parlant-sql add-schema \
  --name "products" \
  --description "Table des produits" \
  --columns "id:INTEGER PRIMARY KEY" \
  --columns "name:TEXT" \
  --columns "price:DECIMAL" \
  --example "SELECT * FROM products WHERE price < 100;" \
  --rule "Prices are in euros"
```

### CLI - Lister les schémas

```bash
parlant-sql list-schemas
```

### CLI - Exécuter une requête

```bash
parlant-sql query -q "Qui sont nos médecins actifs ?" --format json
```

### Mode Interactif

```bash
parlant-sql interactive --db-path medical_database.db
```

---

## 🔗 Intégration Parlant

### Démarrer Parlant avec le module SQL

```bash
parlant-server --module parlant_sql.module
```

### Utiliser dans un Agent

```python
import parlant.sdk as p

async def main():
    async with p.Server() as server:
        agent = await server.create_agent(
            name="Assistant Médical avec SQL",
            description="Agent avec accès base de données"
        )
        
        # Guideline pour utiliser SQL
        await agent.create_guideline(
            condition="Le patient demande des informations sur ses rendez-vous, prescriptions ou statistiques",
            action="Query the medical database to retrieve the information",
            tools=["sql_query"]  # ← Utilise parlant-sql
        )
        
        # Journey normal
        journey = await agent.create_journey(
            title="Prendre Rendez-vous",
            conditions=["Le patient veut prendre rendez-vous"]
        )
        # ...
```

### Exemple de Conversation

```
User: "Combien de rendez-vous ai-je eus avec le Dr. Martin cette année ?"
    ↓
Parlant évalue → Guideline SQL match ✅
    ↓
Appelle tool sql_query
    ↓
SQL Agent génère:
    SELECT COUNT(*) 
    FROM appointments 
    WHERE patient_id = ? 
    AND doctor_id = (SELECT id FROM doctors WHERE last_name='Martin')
    AND appointment_date >= DATE('now', 'start of year')
    ↓
Exécute → Résultat: 3
    ↓
Agent: "Vous avez eu 3 rendez-vous avec le Dr. Martin cette année."
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ AGENT PARLANT                                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Guideline 1: "Questions sur cabinet" → Tool: qna           │
│  Guideline 2: "Questions sur données" → Tool: sql_query    │
│                                                              │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ PARLANT SQL (app.py)                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Question en langage naturel                             │
│  2. Charge les schémas de tables                            │
│  3. LLM génère SQL structuré (Draft → Critique → Final)    │
│  4. Validation de sécurité                                  │
│  5. Exécution SQLite                                        │
│  6. Formatage des résultats                                 │
│                                                              │
└────────────────────┬────────────────────────────────────────┘
                     ↓
             ┌───────────────┐
             │  SQLite DB    │
             │  (medical_    │
             │   database.db)│
             └───────────────┘
```

---

## 🔐 Sécurité

### Couches de Protection

1. **Whitelist SQL** : Seul SELECT autorisé
2. **Blacklist Keywords** : DELETE, DROP, UPDATE bloqués
3. **Validation LLM** : Le LLM détecte les requêtes dangereuses
4. **LIMIT automatique** : Maximum 100 résultats
5. **Approbation humaine** : Flag pour requêtes complexes
6. **Masquage données** : Champs sensibles exclus

### Configuration Sécurité

Dans les schémas de tables (`database_schema/*.md`) :

```markdown
## Règles de Sécurité
- ⚠️ Ne JAMAIS exposer `insurance_number`
- Toujours utiliser LIMIT
- Les `notes` médicales sont confidentielles
```

Ces règles sont injectées dans le prompt LLM.

---

## 📚 Exemples

### Exemple 1 : Statistiques

**Question :** "Quel est notre taux d'annulation ce mois ?"

**SQL Généré :**
```sql
SELECT 
    COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as cancelled,
    COUNT(*) as total,
    ROUND(COUNT(CASE WHEN status = 'cancelled' THEN 1 END) * 100.0 / COUNT(*), 2) as rate
FROM appointments
WHERE appointment_date >= DATE('now', 'start of month');
```

**Résultat :** `{"cancelled": 3, "total": 42, "rate": 7.14}`

### Exemple 2 : Jointure Complexe

**Question :** "Qui sont les patients du Dr. Dupont ?"

**SQL Généré :**
```sql
SELECT DISTINCT
    p.first_name,
    p.last_name,
    p.phone,
    COUNT(a.id) as appointment_count
FROM patients p
JOIN appointments a ON p.id = a.patient_id
JOIN doctors d ON a.doctor_id = d.id
WHERE d.last_name = 'Dupont'
GROUP BY p.id
ORDER BY appointment_count DESC
LIMIT 100;
```

### Exemple 3 : Agrégation

**Question :** "Quel médecin est le plus sollicité ?"

**SQL Généré :**
```sql
SELECT 
    d.first_name,
    d.last_name,
    COUNT(a.id) as appointment_count
FROM doctors d
LEFT JOIN appointments a ON d.id = a.doctor_id
WHERE a.appointment_date >= DATE('now', '-30 days')
GROUP BY d.id
ORDER BY appointment_count DESC
LIMIT 1;
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📄 Licence

Distribué sous la licence Apache 2.0. Voir `LICENSE` pour plus d'informations.

---

## 🙏 Remerciements

- Inspiré par [parlant-qna](https://github.com/emcie-co/parlant-qna)
- Propulsé par [Parlant Framework](https://parlant.io)
- OpenAI pour les modèles LLM

---

## 📞 Support

- 📧 Email: support@example.com
- 💬 Discord: [Rejoindre](https://discord.gg/example)
- 📖 Documentation: [parlant.io/docs](https://parlant.io/docs)

---

<div align="center">
Made with ❤️ for the Parlant community
</div>

