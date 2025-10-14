# 📋 Schémas de Base de Données

Ce dossier contient les descriptions des tables de la base de données médicale.

## 📚 Tables Disponibles

### 🏥 patients_table.md
Informations sur les patients du cabinet

**Colonnes principales :**
- `id`, `first_name`, `last_name`
- `date_of_birth`, `email`, `phone`
- `address`, `created_at`

**Cas d'usage :**
- Recherche de patients par nom
- Liste des nouveaux patients
- Statistiques démographiques

---

### 📅 appointments_table.md
Rendez-vous médicaux (passés, présents, futurs)

**Colonnes principales :**
- `id`, `patient_id`, `doctor_id`
- `appointment_date`, `duration_minutes`
- `reason`, `status`, `notes`

**Cas d'usage :**
- Rendez-vous du jour
- Historique patient
- Statistiques de fréquentation

---

### 👨‍⚕️ doctors_table.md
Médecins et spécialistes du cabinet

**Colonnes principales :**
- `id`, `first_name`, `last_name`
- `specialty`, `office_number`
- `available_days`, `is_active`

**Cas d'usage :**
- Liste des médecins actifs
- Recherche par spécialité
- Disponibilités

---

### 💊 prescriptions_table.md
Ordonnances et prescriptions médicales

**Colonnes principales :**
- `id`, `patient_id`, `doctor_id`
- `medication_name`, `dosage`
- `duration_days`, `created_at`

**Cas d'usage :**
- Historique des prescriptions
- Médicaments les plus prescrits
- Suivi des traitements

---

## 🔄 Format des Fichiers

Chaque fichier `.md` suit cette structure :

```markdown
# Table: nom_table

## Description
Description de ce que contient la table

## Colonnes
- `colonne1` (TYPE) - Description
- `colonne2` (TYPE) - Description

## Exemples de Requêtes

### Cas d'usage 1
\```sql
SELECT ... FROM table WHERE ...
\```

## Règles de Sécurité
- Règle 1
- Règle 2
```

---

## 🚀 Utilisation

### Charger tous les schémas

```bash
# Windows
load_schemas.bat

# Linux/Mac
./load_schemas.sh
```

### Ajouter un nouveau schéma manuellement

```bash
parlant-sql add-schema \
  --name "ma_nouvelle_table" \
  --description "Description de la table" \
  --columns "id:INTEGER PRIMARY KEY" \
  --columns "name:TEXT" \
  --example "SELECT * FROM ma_nouvelle_table;" \
  --rule "Règle de sécurité importante"
```

---

## 📝 Bonnes Pratiques

### ✅ DO

- **Descriptions claires** : Expliquer ce que contient chaque table
- **Exemples variés** : Montrer différents cas d'usage
- **Règles de sécurité** : Spécifier les champs sensibles
- **Types précis** : Indiquer TEXT, INTEGER, DATE, etc.

### ❌ DON'T

- **Schémas incomplets** : Toujours documenter toutes les colonnes importantes
- **Exemples complexes** : Les exemples doivent être didactiques
- **Oublier les règles** : Les règles de sécurité sont critiques

---

## 🔐 Règles de Sécurité Communes

Ces règles s'appliquent à TOUTES les tables :

1. **SELECT uniquement** - Pas de DELETE, UPDATE, DROP
2. **LIMIT obligatoire** - Maximum 100 résultats
3. **Données sensibles** - Masquer numéros sécu, mots de passe
4. **Jointures préférées** - Toujours joindre pour avoir les noms
5. **Filtres temporels** - Éviter de charger toutes les données historiques

---

## 📊 Diagramme des Relations

```
┌─────────────┐
│  patients   │
│             │
│  id  ←──────┼──────┐
└─────────────┘      │
                     │
┌─────────────┐      │      ┌──────────────┐
│   doctors   │      │      │ appointments │
│             │      │      │              │
│  id  ←──────┼──────┼──────┤ patient_id   │
└─────────────┘      │      │ doctor_id    │
                     │      │ id  ←────────┼──────┐
                     │      └──────────────┘      │
                     │                            │
                     │      ┌──────────────────┐  │
                     │      │  prescriptions   │  │
                     │      │                  │  │
                     └──────┤ patient_id       │  │
                            │ doctor_id        │  │
                            │ appointment_id ──┘  │
                            └──────────────────┘
```

---

## 🎯 Extension

Pour ajouter une nouvelle table à votre base :

1. **Créer le fichier `.md`** dans ce dossier
2. **Suivre le format** standard (voir ci-dessus)
3. **Ajouter des exemples** représentatifs
4. **Définir les règles** de sécurité
5. **Mettre à jour** `load_schemas.bat`
6. **Tester** avec `parlant-sql query`

---

**Questions ?** Consultez le [README principal](../README.md)

