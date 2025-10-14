# Table: doctors

## Description
Contient les informations sur tous les médecins et spécialistes du cabinet.

## Colonnes
- `id` (INTEGER PRIMARY KEY) - Identifiant unique du médecin
- `first_name` (TEXT) - Prénom
- `last_name` (TEXT) - Nom de famille
- `specialty` (TEXT) - Spécialité médicale
- `email` (TEXT) - Email professionnel
- `phone` (TEXT) - Téléphone direct
- `office_number` (TEXT) - Numéro de bureau
- `available_days` (TEXT) - Jours de disponibilité (ex: "Lun,Mer,Ven")
- `is_active` (BOOLEAN) - Médecin actif ou non
- `created_at` (TIMESTAMP) - Date d'ajout

## Exemples de Requêtes

### Lister tous les médecins actifs
```sql
SELECT first_name, last_name, specialty, office_number
FROM doctors
WHERE is_active = 1
ORDER BY last_name;
```

### Médecins par spécialité
```sql
SELECT specialty, COUNT(*) as doctor_count
FROM doctors
WHERE is_active = 1
GROUP BY specialty
ORDER BY doctor_count DESC;
```

### Trouver un médecin par nom
```sql
SELECT id, first_name, last_name, specialty, phone, office_number
FROM doctors
WHERE last_name LIKE '%Martin%'
AND is_active = 1;
```

### Médecin le plus sollicité (avec rendez-vous)
```sql
SELECT d.first_name, d.last_name, d.specialty, COUNT(a.id) as appointment_count
FROM doctors d
LEFT JOIN appointments a ON d.id = a.doctor_id
WHERE d.is_active = 1
AND a.appointment_date >= DATE('now', '-30 days')
GROUP BY d.id
ORDER BY appointment_count DESC
LIMIT 1;
```

## Règles de Sécurité
- Seuls les médecins `is_active = 1` doivent être affichés normalement
- Email et phone sont des données sensibles, à utiliser avec précaution
- La spécialité doit être standard: 'Médecine Générale', 'Cardiologie', 'Pédiatrie', etc.

