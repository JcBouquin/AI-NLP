# Table: prescriptions

## Description
Contient les ordonnances et prescriptions médicales.

## Colonnes
- `id` (INTEGER PRIMARY KEY) - Identifiant unique de l'ordonnance
- `patient_id` (INTEGER) - Référence au patient (FK vers patients.id)
- `doctor_id` (INTEGER) - Référence au médecin (FK vers doctors.id)
- `appointment_id` (INTEGER) - Référence au RDV (FK vers appointments.id)
- `medication_name` (TEXT) - Nom du médicament
- `dosage` (TEXT) - Posologie (ex: "1 comprimé 3 fois par jour")
- `duration_days` (INTEGER) - Durée du traitement en jours
- `instructions` (TEXT) - Instructions spéciales
- `created_at` (TIMESTAMP) - Date de prescription

## Exemples de Requêtes

### Prescriptions récentes d'un patient
```sql
SELECT p.medication_name, p.dosage, p.duration_days, p.created_at, d.last_name as doctor
FROM prescriptions p
JOIN doctors d ON p.doctor_id = d.id
WHERE p.patient_id = ?
ORDER BY p.created_at DESC
LIMIT 10;
```

### Médicaments les plus prescrits
```sql
SELECT medication_name, COUNT(*) as prescription_count
FROM prescriptions
WHERE created_at >= DATE('now', '-90 days')
GROUP BY medication_name
ORDER BY prescription_count DESC
LIMIT 10;
```

### Prescriptions par médecin
```sql
SELECT d.first_name, d.last_name, COUNT(p.id) as prescription_count
FROM doctors d
LEFT JOIN prescriptions p ON d.id = p.doctor_id
WHERE p.created_at >= DATE('now', 'start of month')
GROUP BY d.id
ORDER BY prescription_count DESC;
```

## Règles de Sécurité
- Les prescriptions sont des données médicales sensibles
- Toujours associer avec patient et médecin pour contexte
- Ne jamais modifier ou supprimer une prescription (traçabilité légale)
- Les instructions peuvent contenir des informations confidentielles

