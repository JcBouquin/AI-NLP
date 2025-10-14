# Exemples Text-to-SQL : Jointures

## Rendez-vous avec Détails Patient et Médecin

**Question:** "Montre-moi les rendez-vous d'aujourd'hui avec tous les détails"
```sql
SELECT 
    a.id,
    a.appointment_date,
    a.reason,
    a.status,
    p.first_name as patient_first,
    p.last_name as patient_last,
    p.phone as patient_phone,
    d.first_name as doctor_first,
    d.last_name as doctor_last,
    d.specialty
FROM appointments a
JOIN patients p ON a.patient_id = p.id
JOIN doctors d ON a.doctor_id = d.id
WHERE DATE(a.appointment_date) = DATE('now')
ORDER BY a.appointment_date;
```

## Patients d'un Médecin Spécifique

**Question:** "Quels sont les patients du Dr. Martin ?"
```sql
SELECT DISTINCT
    p.id,
    p.first_name,
    p.last_name,
    p.phone,
    COUNT(a.id) as appointment_count
FROM patients p
JOIN appointments a ON p.id = a.patient_id
JOIN doctors d ON a.doctor_id = d.id
WHERE d.last_name = 'Martin'
GROUP BY p.id
ORDER BY appointment_count DESC
LIMIT 100;
```

## Prescriptions avec Patient et Médecin

**Question:** "Quelles ordonnances ont été faites cette semaine ?"
```sql
SELECT 
    pr.medication_name,
    pr.dosage,
    pr.created_at,
    p.first_name as patient_first,
    p.last_name as patient_last,
    d.first_name as doctor_first,
    d.last_name as doctor_last
FROM prescriptions pr
JOIN patients p ON pr.patient_id = p.id
JOIN doctors d ON pr.doctor_id = d.id
WHERE pr.created_at >= DATE('now', 'weekday 0', '-7 days')
ORDER BY pr.created_at DESC
LIMIT 50;
```

## Rendez-vous sans No-Show par Médecin

**Question:** "Combien de rendez-vous complétés par médecin ce mois ?"
```sql
SELECT 
    d.first_name,
    d.last_name,
    d.specialty,
    COUNT(a.id) as completed_appointments
FROM doctors d
JOIN appointments a ON d.id = a.doctor_id
WHERE a.status = 'completed'
AND a.appointment_date >= DATE('now', 'start of month')
GROUP BY d.id
ORDER BY completed_appointments DESC;
```

