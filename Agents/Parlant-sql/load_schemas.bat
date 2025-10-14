@echo off
echo ============================================
echo   Chargement des Schemas de Base de Donnees
echo ============================================
echo.
echo Ces schemas permettent au SQL Agent de comprendre
echo la structure de la base de donnees medicale.
echo.

echo Ajout de la table patients...
parlant-sql add-schema ^
  --name "patients" ^
  --description "Table contenant les informations sur tous les patients du cabinet medical" ^
  --columns "id:INTEGER PRIMARY KEY" ^
  --columns "first_name:TEXT" ^
  --columns "last_name:TEXT" ^
  --columns "date_of_birth:DATE" ^
  --columns "email:TEXT" ^
  --columns "phone:TEXT" ^
  --columns "address:TEXT" ^
  --columns "created_at:TIMESTAMP" ^
  --example "SELECT COUNT(*) FROM patients;" ^
  --example "SELECT first_name, last_name FROM patients WHERE last_name LIKE '%%Smith%%' LIMIT 10;" ^
  --rule "Never expose insurance_number" ^
  --rule "Always use LIMIT to prevent too many results"

echo.
echo Ajout de la table appointments...
parlant-sql add-schema ^
  --name "appointments" ^
  --description "Table contenant tous les rendez-vous medicaux passes, presents et futurs" ^
  --columns "id:INTEGER PRIMARY KEY" ^
  --columns "patient_id:INTEGER" ^
  --columns "doctor_id:INTEGER" ^
  --columns "appointment_date:DATETIME" ^
  --columns "duration_minutes:INTEGER" ^
  --columns "reason:TEXT" ^
  --columns "status:TEXT" ^
  --example "SELECT COUNT(*) FROM appointments WHERE DATE(appointment_date) = DATE('now');" ^
  --example "SELECT * FROM appointments a JOIN patients p ON a.patient_id = p.id WHERE DATE(a.appointment_date) = DATE('now');" ^
  --rule "Always join with patients and doctors for readable names" ^
  --rule "Status must be one of: scheduled, completed, cancelled, no-show"

echo.
echo Ajout de la table doctors...
parlant-sql add-schema ^
  --name "doctors" ^
  --description "Table contenant les informations sur tous les medecins et specialistes du cabinet" ^
  --columns "id:INTEGER PRIMARY KEY" ^
  --columns "first_name:TEXT" ^
  --columns "last_name:TEXT" ^
  --columns "specialty:TEXT" ^
  --columns "email:TEXT" ^
  --columns "phone:TEXT" ^
  --columns "is_active:BOOLEAN" ^
  --example "SELECT * FROM doctors WHERE is_active = 1;" ^
  --example "SELECT d.*, COUNT(a.id) as appt_count FROM doctors d LEFT JOIN appointments a ON d.id = a.doctor_id GROUP BY d.id;" ^
  --rule "Only show doctors where is_active = 1" ^
  --rule "Email and phone are sensitive data"

echo.
echo Ajout de la table prescriptions...
parlant-sql add-schema ^
  --name "prescriptions" ^
  --description "Table contenant les ordonnances et prescriptions medicales" ^
  --columns "id:INTEGER PRIMARY KEY" ^
  --columns "patient_id:INTEGER" ^
  --columns "doctor_id:INTEGER" ^
  --columns "medication_name:TEXT" ^
  --columns "dosage:TEXT" ^
  --columns "duration_days:INTEGER" ^
  --columns "created_at:TIMESTAMP" ^
  --example "SELECT medication_name, COUNT(*) FROM prescriptions GROUP BY medication_name ORDER BY COUNT(*) DESC LIMIT 10;" ^
  --rule "Prescriptions are sensitive medical data" ^
  --rule "Never allow DELETE or UPDATE operations"

echo.
echo ============================================
echo   Schemas charges avec succes !
echo ============================================
echo.
echo Verifiez avec: parlant-sql list-schemas
pause

