"""
Agent médical simplifié basé sur healthcare.py
Utilise le tool parlant-qna pour répondre aux questions médicales
"""

import parlant.sdk as p
import asyncio
import os
from dotenv import load_dotenv

# Charger les variables d'environnement (dont OPENAI_API_KEY)
load_dotenv()


@p.tool
async def get_upcoming_slots(context: p.ToolContext) -> p.ToolResult:
    """Simule des créneaux disponibles"""
    return p.ToolResult(data=["Lundi 10h", "Mardi 14h", "Mercredi 16h"])


@p.tool
async def schedule_appointment(context: p.ToolContext, slot: str) -> p.ToolResult:
    """Simule la prise de rendez-vous"""
    return p.ToolResult(data=f"Rendez-vous confirmé pour {slot}")


async def main():
    async with p.Server() as server:
        # Créer l'agent
        agent = await server.create_agent(
            name="Assistant Médical Simple",
            description="Agent empathique qui aide avec les rendez-vous et questions médicales"
        )
        
        # Glossaire médical
        await agent.create_term(
            name="Numéro du cabinet",
            description="Le numéro est le +33-1-23-45-67-89"
        )
        
        await agent.create_term(
            name="Horaires",
            description="Ouvert du lundi au vendredi, 9h-17h"
        )
        
        # Journey : Prise de rendez-vous
        journey = await agent.create_journey(
            title="Prendre Rendez-vous",
            description="Aide le patient à trouver un créneau",
            conditions=["Le patient veut prendre rendez-vous"]
        )
        
        t1 = await journey.initial_state.transition_to(
            chat_state="Demander la raison de la visite"
        )
        
        t2 = await t1.target.transition_to(
            tool_state=get_upcoming_slots
        )
        
        t3 = await t2.target.transition_to(
            chat_state="Proposer les créneaux disponibles"
        )
        
        t4 = await t3.target.transition_to(
            tool_state=schedule_appointment,
            condition="Le patient choisit un créneau"
        )
        
        await t4.target.transition_to(
            chat_state="Confirmer le rendez-vous"
        )
        
        # Guidelines
        
        # 1. Utiliser QNA pour questions médicales
        # Note: Le tool 'qna' est automatiquement disponible via --module parlant_qna.module
        await agent.create_guideline(
            condition="Le patient pose une question sur un terme médical ou procédure",
            action="Search the medical documentation knowledge base for an answer",
            tools=["qna"]  # ← LIEN EXPLICITE vers le tool qna
        )
        
        # 2. Urgence
        await agent.create_guideline(
            condition="Le patient dit que c'est urgent",
            action="Lui dire d'appeler immédiatement le cabinet"
        )
        
        # 3. Hors sujet
        await agent.create_guideline(
            condition="Le patient parle de sujets non médicaux",
            action="Poliment rediriger vers les questions médicales"
        )
        
        print("✅ Agent médical démarré !")
        print("🔗 Accédez à l'interface web pour chatter")
        
        # Garder le serveur actif
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())

