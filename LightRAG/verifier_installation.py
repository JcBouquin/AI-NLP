# -*- coding: utf-8 -*-
"""
Script de vérification pour s'assurer que tout est prêt avant de lancer mon_premier_test.py
"""

import os
import sys

def verifier_python():
    """Vérifie la version de Python"""
    version = sys.version_info
    print(f"[Python] Version : {version.major}.{version.minor}.{version.micro}")
    if version.major == 3 and version.minor >= 10:
        print("   [OK] Version compatible (>= 3.10)")
        return True
    else:
        print("   [ERREUR] Version incompatible (necessaire Python 3.10+)")
        return False

def verifier_modules():
    """Vérifie que les modules nécessaires sont installés"""
    modules_requis = {
        'lightrag': 'LightRAG',
        'docx': 'python-docx (pour lire les fichiers Word)',
        'dotenv': 'python-dotenv (pour lire le fichier .env)',
        'openai': 'openai (pour communiquer avec OpenAI)',
    }

    tout_ok = True
    print("\n[Modules] Verification des modules Python :")

    for module, description in modules_requis.items():
        try:
            __import__(module)
            print(f"   [OK] {description}")
        except ImportError:
            print(f"   [MANQUANT] {description}")
            tout_ok = False
            if module == 'docx':
                print(f"      --> Installez avec : pip install python-docx")
            elif module == 'lightrag':
                print(f"      --> Installez avec : pip install -e .")
            else:
                print(f"      --> Installez avec : pip install {module}")

    return tout_ok

def verifier_env():
    """Vérifie que le fichier .env existe et contient une clé API"""
    print("\n[Config] Verification du fichier .env :")

    if not os.path.exists('.env'):
        print("   [MANQUANT] Le fichier .env n'existe pas")
        print("      --> Creez un fichier .env avec votre OPENAI_API_KEY")
        print("      --> Exemple : OPENAI_API_KEY=sk-votre-cle")
        return False

    print("   [OK] Le fichier .env existe")

    # Vérifier le contenu
    with open('.env', 'r', encoding='utf-8') as f:
        contenu = f.read()

    if 'OPENAI_API_KEY' not in contenu:
        print("   [ATTENTION] Le fichier .env ne contient pas OPENAI_API_KEY")
        return False

    if 'sk-votre-cle' in contenu or 'sk-votre-api' in contenu:
        print("   [ATTENTION] Vous devez remplacer la cle par votre vraie cle API")
        print("      --> Obtenez une cle sur : https://platform.openai.com/api-keys")
        return False

    # Extraire la clé pour voir si elle a l'air valide
    for ligne in contenu.split('\n'):
        if ligne.startswith('OPENAI_API_KEY='):
            cle = ligne.split('=', 1)[1].strip()
            if cle.startswith('sk-') and len(cle) > 20:
                print(f"   [OK] Cle API configuree (commence par {cle[:8]}...)")
                return True
            else:
                print(f"   [ATTENTION] La cle API ne semble pas valide")
                print(f"      --> Elle devrait commencer par 'sk-'")
                return False

    return False

def verifier_document():
    """Vérifie que le document à analyser existe"""
    print("\n[Document] Verification du document :")

    doc_path = "Présentation association mairie.docx"

    if os.path.exists(doc_path):
        taille = os.path.getsize(doc_path)
        print(f"   [OK] '{doc_path}' existe ({taille:,} octets)")
        return True
    else:
        print(f"   [MANQUANT] '{doc_path}' n'existe pas")
        print(f"      --> Placez votre document dans le dossier : {os.getcwd()}")
        return False

def verifier_lightrag():
    """Vérifie que LightRAG fonctionne"""
    print("\n[LightRAG] Verification de LightRAG :")

    try:
        import lightrag
        version = getattr(lightrag, '__version__', 'inconnue')
        print(f"   [OK] LightRAG version {version} installe")
        return True
    except Exception as e:
        print(f"   [ERREUR] Erreur lors de l'import de LightRAG : {e}")
        return False

def main():
    print("=" * 64)
    print("       VERIFICATION DE L'INSTALLATION LIGHTRAG")
    print("=" * 64)
    print()

    resultats = {
        'Python': verifier_python(),
        'Modules': verifier_modules(),
        'Fichier .env': verifier_env(),
        'Document': verifier_document(),
        'LightRAG': verifier_lightrag(),
    }

    print("\n" + "=" * 60)
    print("RESUME")
    print("=" * 60)

    for nom, ok in resultats.items():
        statut = "[OK]" if ok else "[PROBLEME]"
        print(f"{statut} {nom}")

    print()

    if all(resultats.values()):
        print("==> TOUT EST PRET !")
        print()
        print("Vous pouvez maintenant lancer le programme principal :")
        print("   python mon_premier_test.py")
        print()
    else:
        print("==> IL Y A DES PROBLEMES A CORRIGER")
        print()
        print("Corrigez les problemes mentionnes ci-dessus avant de continuer.")
        print()
        print("Besoin d'aide ?")
        print("   - Lisez le fichier GUIDE_RAPIDE.md")
        print("   - Consultez claude-debutant.md pour les debutants")
        print("   - Lisez claude.md pour la documentation complete")
        print()

if __name__ == "__main__":
    main()
