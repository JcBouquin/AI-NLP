# Table: patients

## Description
Contient les informations sur tous les patients du cabinet médical.

## Colonnes
- `id` (INTEGER PRIMARY KEY) - Identifiant unique du patient
- `first_name` (TEXT) - Prénom du patient
- `last_name` (TEXT) - Nom de famille du patient
- `date_of_birth` (DATE) - Date de naissance
- `email` (TEXT) - Adresse email
- `phone` (TEXT) - Numéro de téléphone
- `address` (TEXT) - Adresse postale
- `insurance_number` (TEXT) - Numéro de sécurité sociale
- `created_at` (TIMESTAMP) - Date d'inscription
- `updated_at` (TIMESTAMP) - Dernière mise à jour

## Exemples de Requêtes

### Compter tous les patients
```sql
SELECT COUNT(*) as total_patients FROM patients;
```

### Lister les patients récents (30 derniers jours)
```sql
SELECT first_name, last_name, email, phone 
FROM patients 
WHERE created_at > DATE('now', '-30 days')
ORDER BY created_at DESC;
```

### Chercher un patient par nom
```sql
SELECT id, first_name, last_name, email, phone 
FROM patients 
WHERE last_name LIKE '%Martin%' 
OR first_name LIKE '%Martin%'
LIMIT 100;
```

### Patients nés dans une certaine période
```sql
SELECT first_name, last_name, date_of_birth
FROM patients
WHERE date_of_birth BETWEEN '1980-01-01' AND '1990-12-31'
ORDER BY date_of_birth;
```

## Règles de Sécurité
- ⚠️ Ne JAMAIS exposer `insurance_number` dans les résultats
- Toujours utiliser LIMIT pour éviter trop de résultats
- Les recherches par nom doivent être partielles (LIKE avec %)
- Ne pas permettre de modifications (UPDATE/DELETE)

