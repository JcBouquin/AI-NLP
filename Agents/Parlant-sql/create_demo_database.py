"""
Script pour créer une base de données de démonstration SQLite
"""

import sqlite3
from datetime import datetime, timedelta
import random

def create_demo_database(db_path="medical_database.db"):
    """Créer une base de données de démonstration avec des données fictives"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Créer les tables
    print("Création des tables...")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        date_of_birth DATE NOT NULL,
        email TEXT,
        phone TEXT,
        address TEXT,
        insurance_number TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        office_number TEXT,
        available_days TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        appointment_date DATETIME NOT NULL,
        duration_minutes INTEGER DEFAULT 30,
        reason TEXT,
        status TEXT DEFAULT 'scheduled',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prescriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        appointment_id INTEGER,
        medication_name TEXT NOT NULL,
        dosage TEXT NOT NULL,
        duration_days INTEGER,
        instructions TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(id),
        FOREIGN KEY (appointment_id) REFERENCES appointments(id)
    )
    """)
    
    # Insérer des données de démonstration
    print("Insertion des médecins...")
    doctors = [
        ('Sophie', 'Martin', 'Médecine Générale', 'sophie.martin@cabinet.fr', '01-23-45-67-01', 'Bureau 101', 'Lun,Mer,Ven', 1),
        ('Thomas', 'Dupont', 'Cardiologie', 'thomas.dupont@cabinet.fr', '01-23-45-67-02', 'Bureau 102', 'Mar,Jeu', 1),
        ('Claire', 'Leblanc', 'Pédiatrie', 'claire.leblanc@cabinet.fr', '01-23-45-67-03', 'Bureau 103', 'Lun,Mar,Mer,Jeu,Ven', 1),
        ('Marc', 'Rousseau', 'Dermatologie', 'marc.rousseau@cabinet.fr', '01-23-45-67-04', 'Bureau 104', 'Mer,Jeu', 1),
    ]
    
    cursor.executemany("""
    INSERT INTO doctors (first_name, last_name, specialty, email, phone, office_number, available_days, is_active)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, doctors)
    
    print("Insertion des patients...")
    patients = [
        ('Jean', 'Durand', '1980-05-15', 'jean.durand@email.fr', '06-12-34-56-01', '12 Rue de Paris, 75001 Paris', '1800512345678'),
        ('Marie', 'Bernard', '1992-08-22', 'marie.bernard@email.fr', '06-12-34-56-02', '24 Avenue Foch, 75008 Paris', '2920822345679'),
        ('Pierre', 'Moreau', '1975-03-10', 'pierre.moreau@email.fr', '06-12-34-56-03', '8 Boulevard Haussmann, 75009 Paris', '1750310345680'),
        ('Anne', 'Petit', '2010-11-30', 'anne.petit@email.fr', '06-12-34-56-04', '15 Rue Lafayette, 75010 Paris', '2101130345681'),
        ('Lucas', 'Robert', '1988-07-18', 'lucas.robert@email.fr', '06-12-34-56-05', '32 Avenue Montaigne, 75008 Paris', '1880718345682'),
        ('Emma', 'Richard', '2005-02-14', 'emma.richard@email.fr', '06-12-34-56-06', '9 Rue de Rivoli, 75004 Paris', '2050214345683'),
        ('Paul', 'Simon', '1965-12-25', 'paul.simon@email.fr', '06-12-34-56-07', '18 Quai Voltaire, 75007 Paris', '1651225345684'),
        ('Julie', 'Laurent', '1995-09-08', 'julie.laurent@email.fr', '06-12-34-56-08', '27 Rue Saint-Honoré, 75001 Paris', '2950908345685'),
    ]
    
    cursor.executemany("""
    INSERT INTO patients (first_name, last_name, date_of_birth, email, phone, address, insurance_number)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, patients)
    
    print("Insertion des rendez-vous...")
    # Générer des rendez-vous sur les 30 derniers jours et 30 prochains jours
    base_date = datetime.now()
    statuses = ['scheduled', 'completed', 'cancelled', 'no-show']
    reasons = ['Consultation générale', 'Suivi', 'Contrôle', 'Urgence', 'Vaccination', 'Certificat médical']
    
    appointments = []
    for i in range(50):
        patient_id = random.randint(1, 8)
        doctor_id = random.randint(1, 4)
        days_offset = random.randint(-30, 30)
        hour = random.randint(9, 17)
        minute = random.choice([0, 15, 30, 45])
        appt_date = base_date + timedelta(days=days_offset)
        appt_date = appt_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Les rendez-vous passés sont plus probablement "completed"
        if days_offset < 0:
            status = random.choice(['completed', 'completed', 'completed', 'cancelled', 'no-show'])
        else:
            status = 'scheduled'
        
        reason = random.choice(reasons)
        duration = random.choice([15, 30, 45, 60])
        
        appointments.append((patient_id, doctor_id, appt_date, duration, reason, status))
    
    cursor.executemany("""
    INSERT INTO appointments (patient_id, doctor_id, appointment_date, duration_minutes, reason, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, appointments)
    
    print("Insertion des prescriptions...")
    medications = [
        ('Paracétamol', '1g 3 fois par jour', 7),
        ('Ibuprofène', '400mg 2 fois par jour', 5),
        ('Amoxicilline', '1g 2 fois par jour', 10),
        ('Doliprane', '500mg au besoin', 3),
        ('Ventoline', '2 bouffées si besoin', 30),
    ]
    
    prescriptions = []
    for i in range(20):
        patient_id = random.randint(1, 8)
        doctor_id = random.randint(1, 4)
        med_name, dosage, duration = random.choice(medications)
        prescriptions.append((patient_id, doctor_id, med_name, dosage, duration))
    
    cursor.executemany("""
    INSERT INTO prescriptions (patient_id, doctor_id, medication_name, dosage, duration_days)
    VALUES (?, ?, ?, ?, ?)
    """, prescriptions)
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Base de données créée avec succès: {db_path}")
    print(f"   - {len(doctors)} médecins")
    print(f"   - {len(patients)} patients")
    print(f"   - {len(appointments)} rendez-vous")
    print(f"   - {len(prescriptions)} prescriptions")

if __name__ == "__main__":
    create_demo_database()

