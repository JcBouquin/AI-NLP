# Table: appointments

## Description
Contient tous les rendez-vous médicaux passés, présents et futurs.

## Colonnes
- `id` (INTEGER PRIMARY KEY) - Identifiant unique du rendez-vous
- `patient_id` (INTEGER) - Référence au patient (FK vers patients.id)
- `doctor_id` (INTEGER) - Référence au médecin (FK vers doctors.id)
- `appointment_date` (DATETIME) - Date et heure du rendez-vous
- `duration_minutes` (INTEGER) - Durée prévue en minutes
- `reason` (TEXT) - Motif de la consultation
- `status` (TEXT) - Statut: 'scheduled', 'completed', 'cancelled', 'no-show'
- `notes` (TEXT) - Notes du médecin (après consultation)
- `created_at` (TIMESTAMP) - Date de création du RDV
- `updated_at` (TIMESTAMP) - Dernière modification

## Exemples de Requêtes

### Rendez-vous d'aujourd'hui
```sql
SELECT a.id, p.first_name, p.last_name, d.first_name as doctor_first, d.last_name as doctor_last, a.appointment_date, a.reason
FROM appointments a
JOIN patients p ON a.patient_id = p.id
JOIN doctors d ON a.doctor_id = d.id
WHERE DATE(a.appointment_date) = DATE('now')
AND a.status = 'scheduled'
ORDER BY a.appointment_date;
```

### Rendez-vous à venir pour un patient
```sql
SELECT a.appointment_date, d.first_name, d.last_name, a.reason, a.status
FROM appointments a
JOIN doctors d ON a.doctor_id = d.id
WHERE a.patient_id = ?
AND a.appointment_date > datetime('now')
ORDER BY a.appointment_date
LIMIT 10;
```

### Statistiques par statut
```sql
SELECT status, COUNT(*) as count
FROM appointments
WHERE appointment_date >= DATE('now', 'start of month')
GROUP BY status;
```

### Rendez-vous annulés ce mois-ci
```sql
SELECT COUNT(*) as cancelled_count
FROM appointments
WHERE status = 'cancelled'
AND appointment_date >= DATE('now', 'start of month')
AND appointment_date < DATE('now', 'start of month', '+1 month');
```

### Rendez-vous par médecin
```sql
SELECT d.first_name, d.last_name, COUNT(a.id) as appointment_count
FROM doctors d
LEFT JOIN appointments a ON d.id = a.doctor_id
WHERE a.appointment_date >= DATE('now', '-30 days')
GROUP BY d.id
ORDER BY appointment_count DESC;
```

## Règles de Sécurité
- Les `notes` médicales sont confidentielles, ne pas les exposer sans raison
- Toujours joindre avec `patients` et `doctors` pour avoir des noms lisibles
- Filtrer par date pour éviter de charger tous les rendez-vous historiques
- Status valides: 'scheduled', 'completed', 'cancelled', 'no-show'

