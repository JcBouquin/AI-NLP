"""
Script pour créer et configurer l'agent Parlant avec les tools QNA et SQL
Exécuter ce script AVANT de lancer le frontend web
"""

import asyncio
import sys
from pathlib import Path

# Ajouter le chemin parent pour importer parlant
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import parlant.sdk as p
except ImportError:
    print("❌ Erreur: Le module 'parlant' n'est pas installé")
    print("   Installez-le avec: pip install parlant")
    sys.exit(1)


async def create_medical_agent():
    """Créer un agent médical complet avec QNA et SQL"""
    
    print("🚀 Création de l'agent médical...")
    print()
    
    try:
        async with p.Server() as server:
            # Créer l'agent
            agent = await server.create_agent(
                name="Assistant Médical Web",
                description="Agent médical accessible via interface web avec accès FAQ et base de données"
            )
            
            print(f"✅ Agent créé avec succès !")
            print(f"   Nom: {agent.name}")
            print(f"   ID: {agent.id}")
            print()
            
            # === GLOSSAIRE ===
            print("📚 Ajout du glossaire...")
            
            await agent.create_term(
                name="Numéro du cabinet",
                description="Le numéro de téléphone du cabinet est le +33-1-23-45-67-89"
            )
            
            await agent.create_term(
                name="Horaires d'ouverture",
                description="Le cabinet est ouvert du lundi au vendredi de 9h à 17h, fermé le week-end"
            )
            
            print("   ✅ 2 termes ajoutés au glossaire")
            print()
            
            # === GUIDELINES ===
            print("📋 Configuration des guidelines...")
            
            # Guideline 1: QNA pour informations générales
            guideline_qna = await agent.create_guideline(
                condition="Le patient demande des informations générales sur le cabinet "
                         "(horaires, équipe médicale, tarifs, adresse, politique d'annulation, accès)",
                action="Search the cabinet's FAQ knowledge base for static information",
                tools=["qna"]
            )
            print(f"   ✅ Guideline QNA créée (ID: {guideline_qna.id})")
            
            # Guideline 2: SQL pour données dynamiques
            guideline_sql = await agent.create_guideline(
                condition="Le patient demande des informations sur ses rendez-vous, "
                         "ses prescriptions, son dossier médical, ou des statistiques du cabinet "
                         "(nombre de patients, disponibilités des médecins, rendez-vous du jour, etc.)",
                action="Query the medical database to retrieve real-time information. "
                       "Explain the result in a clear, empathetic and professional way.",
                tools=["sql_query"]
            )
            print(f"   ✅ Guideline SQL créée (ID: {guideline_sql.id})")
            
            # Guideline 3: Urgence (override)
            guideline_urgence = await agent.create_guideline(
                condition="Le patient dit que c'est urgent ou décrit des symptômes graves "
                         "(douleurs thoraciques, difficultés respiratoires, saignements importants, etc.)",
                action="Demander immédiatement au patient d'appeler le 15 (SAMU) ou de se rendre aux urgences. "
                       "Fournir le numéro du cabinet (+33-1-23-45-67-89) comme alternative si moins grave."
            )
            print(f"   ✅ Guideline Urgence créée (ID: {guideline_urgence.id})")
            
            # Guideline 4: Hors sujet
            guideline_offtopic = await agent.create_guideline(
                condition="Le patient parle de sujets qui n'ont rien à voir avec la santé ou le cabinet médical "
                         "(politique, actualités, divertissement, recettes de cuisine, etc.)",
                action="Poliment rediriger le patient vers des questions liées à la santé ou au cabinet médical"
            )
            print(f"   ✅ Guideline Hors-sujet créée (ID: {guideline_offtopic.id})")
            
            print()
            
            # === JOURNEY (OPTIONNEL) ===
            print("🗺️  Création du journey de prise de rendez-vous...")
            
            journey = await agent.create_journey(
                title="Prendre Rendez-vous",
                description="Aide le patient à prendre un rendez-vous médical",
                conditions=["Le patient veut prendre rendez-vous", "Le patient souhaite consulter"]
            )
            
            # États du journey
            t1 = await journey.initial_state.transition_to(
                chat_state="Demander poliment la raison de la visite (symptômes, suivi, certificat, etc.)"
            )
            
            t2 = await t1.target.transition_to(
                chat_state="Proposer d'interroger la base de données pour voir les créneaux disponibles, "
                          "ou demander s'ils ont une préférence de médecin ou de jour"
            )
            
            t3 = await t2.target.transition_to(
                chat_state="Confirmer les détails du rendez-vous et informer que la réservation sera traitée"
            )
            
            await t3.target.transition_to(
                chat_state="Remercier et rappeler qu'ils peuvent annuler 24h avant sans frais"
            )
            
            print(f"   ✅ Journey créé (ID: {journey.id})")
            print()
            
            # === RÉSUMÉ ===
            print("=" * 70)
            print("✅ AGENT CONFIGURÉ AVEC SUCCÈS !")
            print("=" * 70)
            print()
            print("📝 Résumé de la configuration:")
            print(f"   • Agent ID: {agent.id}")
            print(f"   • Guidelines: 4 (QNA, SQL, Urgence, Hors-sujet)")
            print(f"   • Journey: 1 (Prise de RDV)")
            print(f"   • Tools disponibles: qna, sql_query")
            print()
            print("🔧 PROCHAINES ÉTAPES:")
            print()
            print("1️⃣  Mettez à jour chat.js avec l'Agent ID:")
            print(f"    AGENT_ID: '{agent.id}'")
            print()
            print("2️⃣  Démarrez le serveur Parlant avec les modules:")
            print("    parlant-server \\")
            print("      --module parlant_qna.module \\")
            print("      --module parlant_sql.module \\")
            print("      --host 0.0.0.0 \\")
            print("      --port 8000")
            print()
            print("3️⃣  Chargez les données (si pas déjà fait):")
            print("    • FAQ: cd ../mon_agent_medical && load_medical_faq.bat")
            print("    • SQL: cd ../parlant-sql && load_schemas.bat")
            print("    • DB:  python create_demo_database.py")
            print()
            print("4️⃣  Lancez le frontend:")
            print("    cd web_frontend")
            print("    python -m http.server 8080")
            print()
            print("5️⃣  Ouvrez le navigateur:")
            print("    http://localhost:8080")
            print()
            print("=" * 70)
            
            # Sauvegarder l'ID dans un fichier
            config_file = Path(__file__).parent / "agent_config.txt"
            with open(config_file, 'w') as f:
                f.write(f"AGENT_ID={agent.id}\n")
                f.write(f"AGENT_NAME={agent.name}\n")
                f.write(f"CREATED_AT={agent.created_at}\n")
            
            print(f"💾 Configuration sauvegardée dans: {config_file}")
            print()
            
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'agent: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    print()
    print("=" * 70)
    print(" CONFIGURATION DE L'AGENT PARLANT POUR LE FRONTEND WEB")
    print("=" * 70)
    print()
    
    asyncio.run(create_medical_agent())

