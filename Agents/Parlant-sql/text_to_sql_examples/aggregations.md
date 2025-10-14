# Exemples Text-to-SQL : Agrégations et Statistiques

## Statistiques par Statut

**Question:** "Donne-moi les statistiques des rendez-vous par statut ce mois"
```sql
SELECT 
    status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM appointments WHERE appointment_date >= DATE('now', 'start of month')), 2) as percentage
FROM appointments
WHERE appointment_date >= DATE('now', 'start of month')
GROUP BY status
ORDER BY count DESC;
```

## Médecin le Plus Sollicité

**Question:** "Quel est le médecin avec le plus de rendez-vous ?"
```sql
SELECT 
    d.first_name,
    d.last_name,
    d.specialty,
    COUNT(a.id) as appointment_count
FROM doctors d
LEFT JOIN appointments a ON d.id = a.doctor_id
WHERE a.appointment_date >= DATE('now', '-30 days')
GROUP BY d.id
ORDER BY appointment_count DESC
LIMIT 1;
```

## Moyenne d'Âge des Patients

**Question:** "Quelle est l'âge moyen de nos patients ?"
```sql
SELECT 
    AVG((julianday('now') - julianday(date_of_birth)) / 365.25) as average_age,
    MIN((julianday('now') - julianday(date_of_birth)) / 365.25) as youngest_age,
    MAX((julianday('now') - julianday(date_of_birth)) / 365.25) as oldest_age
FROM patients;
```

## Taux d'Annulation

**Question:** "Quel est notre taux d'annulation ce mois ?"
```sql
SELECT 
    COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as cancelled,
    COUNT(*) as total,
    ROUND(COUNT(CASE WHEN status = 'cancelled' THEN 1 END) * 100.0 / COUNT(*), 2) as cancellation_rate
FROM appointments
WHERE appointment_date >= DATE('now', 'start of month');
```

## Top 5 Médicaments Prescrits

**Question:** "Quels sont les médicaments les plus prescrits ?"
```sql
SELECT 
    medication_name,
    COUNT(*) as prescription_count,
    COUNT(DISTINCT patient_id) as unique_patients
FROM prescriptions
WHERE created_at >= DATE('now', '-90 days')
GROUP BY medication_name
ORDER BY prescription_count DESC
LIMIT 5;
```

## Rendez-vous par Jour de la Semaine

**Question:** "Quel jour de la semaine est le plus chargé ?"
```sql
SELECT 
    CASE CAST(strftime('%w', appointment_date) AS INTEGER)
        WHEN 0 THEN 'Dimanche'
        WHEN 1 THEN 'Lundi'
        WHEN 2 THEN 'Mardi'
        WHEN 3 THEN 'Mercredi'
        WHEN 4 THEN 'Jeudi'
        WHEN 5 THEN 'Vendredi'
        WHEN 6 THEN 'Samedi'
    END as day_name,
    COUNT(*) as appointment_count
FROM appointments
WHERE appointment_date >= DATE('now', '-30 days')
AND status = 'completed'
GROUP BY strftime('%w', appointment_date)
ORDER BY appointment_count DESC;
```

## Durée Moyenne des Consultations

**Question:** "Quelle est la durée moyenne des consultations ?"
```sql
SELECT 
    AVG(duration_minutes) as avg_duration,
    MIN(duration_minutes) as min_duration,
    MAX(duration_minutes) as max_duration
FROM appointments
WHERE status = 'completed'
AND appointment_date >= DATE('now', '-30 days');
```

