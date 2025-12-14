"""
Script pour analyser le document "Présentation association mairie.docx" avec LightRAG
et poser des questions dessus
"""

import os
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from lightrag.utils import setup_logger
from docx import Document

# Active les messages d'information pour voir ce qui se passe
setup_logger("lightrag", level="INFO")

# Dossier où seront stockées les données analysées
WORKING_DIR = "./mes_donnees_rag"
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

# Chemin vers votre document
DOCUMENT_PATH = "Présentation association mairie.docx"


def lire_fichier_word(chemin_fichier):
    """
    Lit un fichier Word (.docx) et retourne son contenu en texte
    """
    print(f"📄 Lecture du fichier : {chemin_fichier}")
    try:
        doc = Document(chemin_fichier)
        # Récupère tout le texte de tous les paragraphes
        texte_complet = "\n".join([paragraphe.text for paragraphe in doc.paragraphs])
        print(f"✅ Document lu avec succès ! ({len(texte_complet)} caractères)")
        return texte_complet
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier : {e}")
        return None


async def analyser_document():
    """
    Fonction principale qui analyse le document et répond aux questions
    """
    print("=" * 60)
    print("🚀 DÉMARRAGE DE LIGHTRAG")
    print("=" * 60)

    # Étape 1 : Créer le système LightRAG
    print("\n1️⃣ Création du système LightRAG...")
    rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func=openai_embed,
        llm_model_func=gpt_4o_mini_complete,
    )

    # Étape 2 : Initialiser les storages (OBLIGATOIRE !)
    print("2️⃣ Initialisation des storages...")
    await rag.initialize_storages()
    print("✅ LightRAG est prêt !")

    # Étape 3 : Lire le document Word
    print("\n" + "=" * 60)
    print("📖 LECTURE DU DOCUMENT")
    print("=" * 60)
    contenu = lire_fichier_word(DOCUMENT_PATH)

    if contenu is None or len(contenu.strip()) == 0:
        print("❌ Le document est vide ou n'a pas pu être lu. Abandon.")
        await rag.finalize_storages()
        return

    # Afficher un aperçu du contenu
    print("\n📝 Aperçu du contenu (200 premiers caractères) :")
    print("-" * 60)
    print(contenu[:200] + "..." if len(contenu) > 200 else contenu)
    print("-" * 60)

    # Étape 4 : Analyser le document avec LightRAG
    print("\n" + "=" * 60)
    print("🧠 ANALYSE DU DOCUMENT PAR LIGHTRAG")
    print("=" * 60)
    print("⏳ Analyse en cours... (cela peut prendre 1-2 minutes)")
    print("   LightRAG est en train de :")
    print("   - Découper le texte en morceaux")
    print("   - Identifier les entités (personnes, organisations, concepts)")
    print("   - Créer des relations entre les entités")
    print("   - Construire un graphe de connaissances")

    await rag.ainsert(contenu)
    print("✅ Document analysé et indexé avec succès !")

    # Étape 5 : Poser des questions
    print("\n" + "=" * 60)
    print("❓ SESSION DE QUESTIONS-RÉPONSES")
    print("=" * 60)

    # Liste de questions à poser sur le document
    questions = [
        "Quel est l'objet principal de cette présentation ?",
        "Quelles sont les informations clés mentionnées dans ce document ?",
        "Y a-t-il des dates ou des événements importants mentionnés ?",
        "Quels sont les acteurs ou personnes mentionnés dans le document ?",
    ]

    # Tester différents modes de recherche
    modes = ["hybrid", "global", "local"]

    for i, question in enumerate(questions, 1):
        print(f"\n{'=' * 60}")
        print(f"Question {i}/{len(questions)}")
        print(f"{'=' * 60}")
        print(f"❓ {question}")
        print()

        # Utiliser le mode hybrid (recommandé pour débuter)
        mode = "hybrid"
        print(f"🔍 Mode de recherche : {mode}")
        print("⏳ Recherche en cours...")

        try:
            reponse = await rag.aquery(
                question,
                param=QueryParam(mode=mode)
            )

            print(f"\n💬 Réponse :")
            print("-" * 60)
            print(reponse)
            print("-" * 60)

        except Exception as e:
            print(f"❌ Erreur lors de la question : {e}")

    # Étape 6 : Mode interactif - poser vos propres questions
    print("\n" + "=" * 60)
    print("🎯 MODE INTERACTIF")
    print("=" * 60)
    print("Vous pouvez maintenant poser vos propres questions !")
    print("(Tapez 'quit' ou 'q' pour quitter)")
    print()

    while True:
        try:
            # Demander une question à l'utilisateur
            question_utilisateur = input("\n❓ Votre question : ").strip()

            # Vérifier si l'utilisateur veut quitter
            if question_utilisateur.lower() in ['quit', 'q', 'quitter', 'exit']:
                print("👋 Au revoir !")
                break

            # Ignorer les questions vides
            if not question_utilisateur:
                continue

            # Chercher la réponse
            print("🔍 Recherche en cours...")
            reponse = await rag.aquery(
                question_utilisateur,
                param=QueryParam(mode="hybrid")
            )

            print(f"\n💬 Réponse :")
            print("-" * 60)
            print(reponse)
            print("-" * 60)

        except KeyboardInterrupt:
            print("\n\n👋 Programme interrompu par l'utilisateur. Au revoir !")
            break
        except Exception as e:
            print(f"❌ Erreur : {e}")

    # Étape 7 : Fermer proprement LightRAG
    print("\n" + "=" * 60)
    print("🔚 FERMETURE")
    print("=" * 60)
    await rag.finalize_storages()
    print("✅ LightRAG fermé proprement")
    print("\n💡 Note : Les données analysées sont sauvegardées dans le dossier")
    print(f"   '{WORKING_DIR}/' et seront réutilisées la prochaine fois !")


async def main():
    """
    Point d'entrée principal du programme
    """
    try:
        await analyser_document()
    except Exception as e:
        print(f"\n❌ Erreur fatale : {e}")
        print("\n🔧 Vérifiez que :")
        print("   1. Vous avez créé un fichier .env avec votre OPENAI_API_KEY")
        print("   2. Le fichier 'Présentation association mairie.docx' existe")
        print("   3. Vous avez installé toutes les dépendances (pip install python-docx)")


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║          🤖 LIGHTRAG - ANALYSEUR DE DOCUMENTS 🤖              ║
    ║                                                              ║
    ║  Ce programme va analyser votre document avec LightRAG      ║
    ║  et vous permettre de poser des questions dessus            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    # Vérifier que le fichier .env existe
    if not os.path.exists(".env"):
        print("⚠️  ATTENTION : Le fichier .env n'existe pas !")
        print("\n📝 Créez un fichier .env avec votre clé API OpenAI :")
        print("   OPENAI_API_KEY=sk-votre-cle-ici")
        print("\n💡 Ou utilisez cette commande :")
        print('   echo OPENAI_API_KEY=sk-votre-cle > .env')
        print()
        reponse = input("❓ Voulez-vous continuer quand même ? (o/n) : ")
        if reponse.lower() != 'o':
            print("👋 Au revoir !")
            exit()

    # Vérifier que le document existe
    if not os.path.exists(DOCUMENT_PATH):
        print(f"❌ Le fichier '{DOCUMENT_PATH}' n'existe pas !")
        print(f"📁 Assurez-vous qu'il est dans le dossier : {os.getcwd()}")
        exit()

    # Lancer le programme
    asyncio.run(main())
