"""
Exemple d'intégration de parlant-sql dans un agent Parlant
"""

import parlant.sdk as p
import asyncio


async def main():
    """Créer un agent médical avec accès SQL"""
    
    async with p.Server() as server:
        # Créer l'agent
        agent = await server.create_agent(
            name="Assistant Médical Complet",
            description="Agent avec FAQ statiques ET accès base de données dynamique"
        )
        
        # === GLOSSAIRE ===
        await agent.create_term(
            name="Numéro du cabinet",
            description="Le numéro est le +33-1-23-45-67-89"
        )
        
        await agent.create_term(
            name="Horaires",
            description="Ouvert du lundi au vendredi, 9h-17h"
        )
        
        # === JOURNEY : Prise de Rendez-vous ===
        journey = await agent.create_journey(
            title="Prendre Rendez-vous",
            description="Aide le patient à prendre un rendez-vous",
            conditions=["Le patient veut prendre rendez-vous"]
        )
        
        # États du parcours
        t1 = await journey.initial_state.transition_to(
            chat_state="Demander la raison de la visite"
        )
        
        t2 = await t1.target.transition_to(
            chat_state="Proposer les créneaux disponibles (utiliser sql_query pour voir disponibilités)"
        )
        
        await t2.target.transition_to(
            chat_state="Confirmer le rendez-vous"
        )
        
        # === GUIDELINES ===
        
        # 1. FAQ Statiques (QNA) - Informations générales du cabinet
        await agent.create_guideline(
            condition="Le patient demande des informations générales sur le cabinet "
                     "(horaires, tarifs, adresse, politique d'annulation)",
            action="Search the cabinet's FAQ knowledge base for static information",
            tools=["qna"]  # ← Utilise parlant-qna
        )
        
        # 2. Base de Données Dynamique (SQL) - Données personnelles et statistiques
        await agent.create_guideline(
            condition="Le patient demande des informations sur ses rendez-vous personnels, "
                     "ses prescriptions, son dossier, ou des statistiques du cabinet "
                     "(nombre de patients, disponibilités des médecins, etc.)",
            action="Query the medical database to retrieve real-time information. "
                   "Explain the query result in a clear and empathetic way.",
            tools=["sql_query"]  # ← Utilise parlant-sql
        )
        
        # 3. Urgence (Override tout)
        await agent.create_guideline(
            condition="Le patient dit que c'est urgent ou décrit des symptômes graves",
            action="Lui dire d'appeler immédiatement le 15 (SAMU) ou le cabinet au +33-1-23-45-67-89"
        )
        
        # 4. Hors sujet
        await agent.create_guideline(
            condition="Le patient parle de sujets non médicaux (politique, actualités, divertissement)",
            action="Poliment rediriger vers les questions médicales ou administratives du cabinet"
        )
        
        print("✅ Agent médical complet créé avec succès !")
        print("\n🎯 Capabilities:")
        print("   1. 📚 FAQ statiques (via QNA)")
        print("   2. 🗄️ Requêtes base de données (via SQL)")
        print("   3. 🗺️ Journey de prise de RDV")
        print("   4. 🚨 Gestion des urgences")
        print("\n🔗 Pour démarrer:")
        print("   parlant-server --module parlant_qna.module --module parlant_sql.module")
        print("\n💬 Exemples de questions:")
        print("   - 'Quels sont vos horaires ?' → QNA")
        print("   - 'Combien de rendez-vous ai-je ce mois ?' → SQL")
        print("   - 'Je voudrais prendre rendez-vous' → Journey")
        print("   - 'J'ai des douleurs thoraciques intenses' → Urgence")
        
        # Garder le serveur actif
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())

