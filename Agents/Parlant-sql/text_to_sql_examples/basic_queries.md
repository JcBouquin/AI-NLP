# Exemples Text-to-SQL : Requêtes de Base

## Comptage Simple

**Question:** "Combien de patients avons-nous ?"
```sql
SELECT COUNT(*) as total_patients FROM patients;
```

**Question:** "Combien de rendez-vous aujourd'hui ?"
```sql
SELECT COUNT(*) as today_appointments 
FROM appointments 
WHERE DATE(appointment_date) = DATE('now');
```

**Question:** "Combien de médecins actifs ?"
```sql
SELECT COUNT(*) as active_doctors 
FROM doctors 
WHERE is_active = 1;
```

## Listes Simples

**Question:** "Liste tous les patients"
```sql
SELECT first_name, last_name, email, phone 
FROM patients 
ORDER BY last_name 
LIMIT 100;
```

**Question:** "Quels sont nos médecins ?"
```sql
SELECT first_name, last_name, specialty, office_number 
FROM doctors 
WHERE is_active = 1 
ORDER BY last_name;
```

## Recherches par Nom

**Question:** "Trouve le patient Martin"
```sql
SELECT id, first_name, last_name, email, phone 
FROM patients 
WHERE last_name LIKE '%Martin%' 
OR first_name LIKE '%Martin%'
LIMIT 10;
```

**Question:** "Qui est le Dr. Dupont ?"
```sql
SELECT first_name, last_name, specialty, phone, office_number 
FROM doctors 
WHERE last_name LIKE '%Dupont%' 
AND is_active = 1;
```

## Filtres par Date

**Question:** "Rendez-vous de la semaine prochaine"
```sql
SELECT a.appointment_date, p.first_name, p.last_name, d.last_name as doctor, a.reason
FROM appointments a
JOIN patients p ON a.patient_id = p.id
JOIN doctors d ON a.doctor_id = d.id
WHERE a.appointment_date >= DATE('now', 'weekday 0')
AND a.appointment_date < DATE('now', 'weekday 0', '+7 days')
AND a.status = 'scheduled'
ORDER BY a.appointment_date;
```

**Question:** "Patients inscrits ce mois-ci"
```sql
SELECT first_name, last_name, email, created_at
FROM patients
WHERE created_at >= DATE('now', 'start of month')
ORDER BY created_at DESC;
```

