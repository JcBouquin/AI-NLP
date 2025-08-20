
#!/usr/bin/env python3
"""
Classificateur médical avec analyse sémantique améliorée
Format simple - sans classes ni dépendances externes
"""

import os
import shutil
import json
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Configuration
BASE_DIR = os.path.abspath(r"C:\Users\kosmo\pycode\Iqvia_process")
CHEMIN_SOURCE = os.path.join(BASE_DIR, "ProcessEx")
CHEMIN_DEPOTS = os.path.join(BASE_DIR, "Depots")

# Initialiser le LLM
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("⚠️ ATTENTION: Clé API non trouvée dans les variables d'environnement")
    api_key = "votre_clé_api_openai_ici"  # À remplacer par votre vraie clé

llm = None
if api_key != "votre_clé_api_openai_ici":
    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            api_key=api_key
        )
    except Exception as e:
        print(f"❌ Erreur initialisation LLM: {e}")
        llm = None

def detection_mots_cles_medicaux(titre: str) -> dict:
    """Détection fallback par mots-clés enrichie avec clients et bases de données"""
    titre_lower = titre.lower()
    
    # Dictionnaire des clients pharmaceutiques
    clients_pharma = {
        'iqvia': 'iqvia', 'abbvie': 'abbvie', 'sanofi': 'sanofi', 'pfizer': 'pfizer',
        'novartis': 'novartis', 'roche': 'roche', 'merck': 'merck', 'gsk': 'gsk',
        'glaxosmithkline': 'gsk', 'astrazeneca': 'astrazeneca', 'bayer': 'bayer',
        'boehringer': 'boehringer', 'eli lilly': 'lilly', 'lilly': 'lilly',
        'johnson': 'jnj', 'j&j': 'jnj', 'bristol': 'bms', 'takeda': 'takeda',
        'amgen': 'amgen', 'gilead': 'gilead', 'biogen': 'biogen', 'celgene': 'celgene'
    }
    
    # Dictionnaire des bases de données IQVIA
    bases_donnees = {
        'xponent': 'xponent', 'channel dynamics': 'channel_dynamics', 'channel': 'channel_dynamics',
        'bilan marché': 'bilan_marche', 'bilan': 'bilan_marche', 'marche': 'bilan_marche',
        'midas': 'midas', 'pharmetrics': 'pharmetrics', 'longitudinal': 'longitudinal',
        'plantrak': 'plantrak', 'hospital': 'hospital_data', 'retail': 'retail_data',
        'oncology': 'oncology_monitor', 'monitor': 'monitor', 'therapy': 'therapy_monitor',
        'payor': 'payor_data', 'claims': 'claims_data', 'ema': 'ema_data',
        'sales force': 'sales_force', 'salesforce': 'sales_force'
    }
    
    # Dictionnaire enrichi avec contextes sémantiques (pathologies)
    termes_contextes = {
        # Pathologies oncologiques
        'cancer': ('oncologie', 'clinique'), 'tumeur': ('oncologie', 'clinique'), 
        'oncologie': ('oncologie', 'clinique'), 'prostate': ('oncologie', 'clinique'),
        'sein': ('oncologie', 'clinique'), 'poumon': ('oncologie', 'clinique'),
        'métastase': ('oncologie', 'clinique'), 'chimiothérapie': ('oncologie', 'traitement'),
        
        # Pathologies endocriniennes
        'diabète': ('diabetologie', 'clinique'), 'diabete': ('diabetologie', 'clinique'), 
        'glycémie': ('diabetologie', 'clinique'), 'insuline': ('diabetologie', 'traitement'),
        'hba1c': ('diabetologie', 'diagnostic'),
        
        # Pathologies cardiovasculaires
        'cardiaque': ('cardiologie', 'clinique'), 'coeur': ('cardiologie', 'clinique'), 
        'cœur': ('cardiologie', 'clinique'), 'hypertension': ('cardiologie', 'clinique'),
        'infarctus': ('cardiologie', 'urgence'), 'arythmie': ('cardiologie', 'clinique'),
        
        # Pathologies neurologiques
        'alzheimer': ('neurologie', 'clinique'), 'parkinson': ('neurologie', 'clinique'), 
        'neurologie': ('neurologie', 'clinique'), 'épilepsie': ('neurologie', 'clinique'),
        'avc': ('neurologie', 'urgence'), 'sclérose': ('neurologie', 'clinique'),
        
        # Pathologies respiratoires
        'asthme': ('pneumologie', 'clinique'), 'pneumonie': ('pneumologie', 'urgence'), 
        'bronchite': ('pneumologie', 'clinique'), 'bpco': ('pneumologie', 'clinique'),
        
        # Pathologies dermatologiques
        'eczéma': ('dermatologie', 'clinique'), 'eczema': ('dermatologie', 'clinique'), 
        'psoriasis': ('dermatologie', 'clinique'), 'dermatite': ('dermatologie', 'clinique'),
        
        # Contextes non-pathologiques
        'formation': ('formation', 'commercial'), 'training': ('formation', 'commercial'),
        'vente': ('commercial', 'business'), 'marketing': ('commercial', 'business'),
        'étude': ('recherche', 'scientifique'), 'essai': ('recherche', 'scientifique'),
        'protocole': ('recherche', 'scientifique'), 'phase': ('recherche', 'scientifique'),
        'réglementation': ('reglementaire', 'administratif'), 'autorisation': ('reglementaire', 'administratif'),
        'surveillance': ('pharmacovigilance', 'securite'), 'observance': ('pharmacovigilance', 'therapeutique')
    }
    
    # Détection des clients
    clients_detectes = []
    for client_terme, client_nom in clients_pharma.items():
        if client_terme in titre_lower:
            clients_detectes.append(client_nom)
    
    # Détection des bases de données
    bases_detectees = []
    for base_terme, base_nom in bases_donnees.items():
        if base_terme in titre_lower:
            bases_detectees.append(base_nom)
    
    # Détection des termes médicaux/contextuels
    termes_detectes = []
    contextes_detectes = []
    for terme, (domaine, contexte) in termes_contextes.items():
        if terme in titre_lower:
            termes_detectes.append(terme)
            contextes_detectes.append((domaine, contexte))
    
    # Logique de classification prioritaire
    if clients_detectes:
        # Si client détecté, c'est prioritaire
        client_principal = clients_detectes[0]
        return {
            "contient_maladie": False,
            "maladies_detectees": termes_detectes,
            "categorie_medicale": "client",
            "contexte_principal": "client",
            "client_detecte": client_principal,
            "clients_detectes": clients_detectes,
            "bases_detectees": bases_detectees,
            "confiance": "haute" if len(clients_detectes) > 1 else "moyenne",
            "titre_normalise": titre,
            "score_semantique": 0.8
        }
    
    elif bases_detectees:
        # Si base de données détectée
        base_principale = bases_detectees[0]
        return {
            "contient_maladie": False,
            "maladies_detectees": termes_detectes,
            "categorie_medicale": "base_donnees",
            "contexte_principal": "base_donnees",
            "base_detectee": base_principale,
            "clients_detectes": clients_detectes,
            "bases_detectees": bases_detectees,
            "confiance": "haute" if len(bases_detectees) > 1 else "moyenne",
            "titre_normalise": titre,
            "score_semantique": 0.8
        }
    
    elif termes_detectes:
        # Classification médicale/contextuelle classique
        domaine_principal, contexte_principal = contextes_detectes[0]
        confiance = "haute" if len(termes_detectes) > 1 else "moyenne"
        
        # Déterminer si c'est médical
        domaines_medicaux = ['oncologie', 'diabetologie', 'cardiologie', 'neurologie', 'pneumologie', 'dermatologie']
        est_medical = domaine_principal in domaines_medicaux
        
        return {
            "contient_maladie": est_medical,
            "maladies_detectees": termes_detectes,
            "categorie_medicale": domaine_principal,
            "contexte_principal": contexte_principal,
            "clients_detectes": clients_detectes,
            "bases_detectees": bases_detectees,
            "confiance": confiance,
            "titre_normalise": titre,
            "score_semantique": 0.7 if confiance == "haute" else 0.5
        }
    
    # Aucune détection
    return {
        "contient_maladie": False,
        "maladies_detectees": [],
        "categorie_medicale": "aucune",
        "contexte_principal": "autre",
        "clients_detectes": clients_detectes,
        "bases_detectees": bases_detectees,
        "confiance": "faible",
        "titre_normalise": titre,
        "score_semantique": 0.2
    }

def analyser_titre_avec_llm_semantique(titre: str) -> dict:
    """Analyse sémantique avancée avec LLM - prompt enrichi"""
    if not llm:
        print(f"❌ LLM non disponible, utilisation fallback pour '{titre[:30]}...'")
        return detection_mots_cles_medicaux(titre)
        
    #     try:
        # 1. Lecture du prompt depuis le fichier
     #   with open("prompt_analyse.txt", "r", encoding="utf-8") as file:
      #      human_prompt = file.read()

        # 2. Remplacement de l'ancien prompt par le contenu du fichier
       # analysis_prompt_template = ChatPromptTemplate.from_messages([
        #    ("system", """Tu es un expert en analyse sémantique médicale et business pharmaceutique.
         #   Ton rôle est de comprendre le CONTEXTE et l'INTENTION derrière chaque titre, pas seulement chercher des mots-clés."""),
          #  ("human", human_prompt)
        #])
    
    try:
        analysis_prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Tu es un expert en analyse sémantique médicale et business pharmaceutique. 
            Ton rôle est de comprendre le CONTEXTE et l'INTENTION derrière chaque titre, pas seulement chercher des mots-clés.
            
           
            """),
            ("human", """

  
A partir d'un titre du va extraire les informations suivante en respectant toujours le format JSON suivant 

{
    "contexte_principal": "clinique/recherche/commercial/reglementaire/formation/client/base_donnees/autre",
    "domaine_medical": "oncologie/cardiologie/neurologie/diabetologie/pneumologie/dermatologie/pharmacovigilance/business/client/base_donnees/aucun",
    "type_document": "formation/etude/rapport/suivi/presentation/protocole/guide/autre",
    "population_cible": "patients/professionnels/equipes_vente/chercheurs/regulateurs/clients/mixte",
    "maladies_detectees": ["terme1", "terme2"],
    "clients_detectes": ["client1", "client2"],
    "bases_detectees": ["base1", "base2"],
    "client_principal": "nom_client_principal_ou_null",
    "base_principale": "nom_base_principale_ou_null",
    "contient_maladie": true,
    "confiance": "haute/moyenne/faible",
    "score_semantique": 0.8,
    "justification": "Explication courte du contexte détecté",
    "titre_normalise": "{titre}"
}

voici une liste d'exemple sur lesquels tu peux t'appuyer 

Exemple 1 : 

Je commence par lire attentivement le titre pour en comprendre le contexte et la structure.
"3225553 - Proposition commerciale pour ABBVIE - LTD Immunologie oncologie"

Je comprends que le terme ABBVIE est le nom d'un client. J'en déduis que "clients_detectes" = ["ABBVIE"] et "client_principal" = "ABBVIE".
Je comprends que le document est une "Proposition commerciale". C'est le type de document le plus pertinent. Par conséquent, "type_document" = "proposition".
Je comprends que les termes "Immunologie" et "oncologie" sont des domaines médicaux. J'en déduis que "domaine_medical" = "oncologie" et que "maladies_detectees" doit contenir un terme médical. Comme l'oncologie se rapporte à des maladies, "contient_maladie" = true.
Je comprends qu'il n'y a aucune référence à une base de données. J'en déduis que "bases_detectees" = [] et "base_principale" = "null".

Json Généré :  

{
  "contexte_principal": "commercial",
  "domaine_medical": "oncologie",
  "type_document": "proposition",
  "population_cible": "clients",
  "maladies_detectees": [
    "cancer"
  ],
  "clients_detectes": [
    "ABBVIE"
  ],
  "bases_detectees": [],
  "client_principal": "ABBVIE",
  "base_principale": "null",
  "contient_maladie": true,
  "confiance": "haute",
  "score_semantique": 0.95,
  "justification": "Document commercial pour le client ABBVIE dans le domaine de l'oncologie.",
  "titre_normalise": "3225553 - Proposition commerciale pour ABBVIE - LTD Immunologie oncologie"
}


Exemple 2 : 

Je commence par lire attentivement le titre pour en comprendre le contexte et la structure.

- "3181844 _IQVIA pour ABBOTT DC_Suivi national du FSL2 par segment de pat diabétiques 2025" → contient "suivi" mais c'est un rapport, pas une proposition → aucune
 

Json Généré : 

{
  "contexte_principal": "clinique/recherche/commercial/reglementaire/formation/client/base_donnees/autre",
  "domaine_medical": "diabetologie",
  "type_document": "suivi",
  "population_cible": "patients/professionnels/equipes_vente/chercheurs/regulateurs/clients/mixte",
  "maladies_detectees": [
    "diabete"
  ],
  "clients_detectes": [
    "ABBOTT"
  ],
  "bases_detectees": [],
  "client_principal": "ABBOTT",
  "base_principale": "null",
  "contient_maladie": true,
  "confiance": "haute/moyenne/faible",
  "score_semantique": 0.8,
  "justification": "Explication courte du contexte détecté",
  "titre_normalise": "3181844 _IQVIA pour ABBOTT DC_Suivi national du FSL2 par segment de pat diabétiques 2025"
}


Exemple 3 : 

 
Je commence par lire attentivement le titre pour en comprendre le contexte et la structure.
 "3252322 - Suivi Xponent std cancer de la prostate 2025"
 
Json Généré : 

{
  "contexte_principal": "commercial",
  "domaine_medical": "oncologie",
  "type_document": "suivi",
  "population_cible": "clients",
  "maladies_detectees": [
    "cancer de la prostate"
  ],
  "clients_detectes": [],
  "bases_detectees": [
    "Xponent"
  ],
  "client_principal": "null",
  "base_principale": "Xponent",
  "contient_maladie": true,
  "confiance": "haute",
  "score_semantique": 0.95,
  "justification": "Document de suivi basé sur la base Xponent, centré sur le cancer de la prostate, dans un contexte commercial.",
  "titre_normalise": "3252322 - Suivi Xponent std cancer de la prostate 2025"
}


Exemple 4 :

Je commence par lire attentivement le titre pour en comprendre le contexte et la structure.
"3204851 - IQVIA pour AstraZeneca - Xponent EDS Benlysta 2025"

 
Json Généré : 

{
  "contexte_principal": "commercial",
  "domaine_medical": "immunologie",
  "type_document": "suivi",
  "population_cible": "clients",
  "maladies_detectees": [
    "lupus"
  ],
  "clients_detectes": [
    "AstraZeneca"
  ],
  "bases_detectees": [
    "Xponent"
  ],
  "client_principal": "AstraZeneca",
  "base_principale": "Xponent",
  "contient_maladie": true,
  "confiance": "haute",
  "score_semantique": 0.95,
  "justification": "Document de suivi basé sur la base Xponent pour le médicament Benlysta (traitement du lupus), destiné au client AstraZeneca dans un contexte commercial.",
  "titre_normalise": "3204851 - IQVIA pour AstraZeneca - Xponent EDS Benlysta 2025"
}


Exemple 5 : 

Je commence par lire attentivement le titre pour en comprendre le contexte et la structure.
"PO-7101455030_v1_20241212"

 
Json Généré : 

{
  "contexte_principal": "autre",
  "domaine_medical": "null",
  "type_document": "inconnu",
  "population_cible": "null",
  "maladies_detectees": [],
  "clients_detectes": [],
  "bases_detectees": [],
  "client_principal": "null",
  "base_principale": "null",
  "contient_maladie": false,
  "confiance": "faible",
  "score_semantique": 0.2,
  "justification": "Le titre est un identifiant technique sans indication explicite de client, maladie, base de données ou type de document. Impossible de déterminer un contexte clair.",
  "titre_normalise": "PO-7101455030_v1_20241212"
}


Exemple 6 : 

Je commence par lire attentivement le titre pour en comprendre le contexte et la structure.
"3204288_IQTOP pour AZ - RNW 2025 - PMR Asthme BPCO"

 

Json Généré : 

{
  "contexte_principal": "commercial",
  "domaine_medical": "pneumologie",
  "type_document": "suivi",
  "population_cible": "clients",
  "maladies_detectees": [
    "asthme",
    "BPCO"
  ],
  "clients_detectes": [
    "AstraZeneca"
  ],
  "bases_detectees": [],
  "client_principal": "AstraZeneca",
  "base_principale": "null",
  "contient_maladie": true,
  "confiance": "haute",
  "score_semantique": 0.95,
  "justification": "Document de suivi pour le client AstraZeneca, centré sur les pathologies respiratoires (asthme et BPCO), dans un contexte commercial.",
  "titre_normalise": "3204288_IQTOP pour AZ - RNW 2025 - PMR Asthme BPCO"
}


Exemple 7 

 Je commence par lire attentivement le titre pour en comprendre le contexte et la structure.
"3184694_IQVIA_pour_AZ_PMR_Split_indications_Lynparza_V2"
 


Json Généré : 

{
  "contexte_principal": "commercial",
  "domaine_medical": "oncologie",
  "type_document": "suivi",
  "population_cible": "clients",
  "maladies_detectees": [
    "cancer"
  ],
  "clients_detectes": [
    "AstraZeneca"
  ],
  "bases_detectees": [],
  "client_principal": "AstraZeneca",
  "base_principale": "null",
  "contient_maladie": true,
  "confiance": "haute",
  "score_semantique": 0.95,
  "justification": "Document de suivi commercial pour AstraZeneca, centré sur le médicament Lynparza (traitement de plusieurs cancers), avec une analyse par indications.",
  "titre_normalise": "3184694_IQVIA_pour_AZ_PMR_Split_indications_Lynparza_V2"
}

Exemple 8 : 

Je commence par lire attentivement le titre pour en comprendre le contexte et la structure.
"20250428 IQVIA pour AZ_Placement consultant renfort Lokelma V2"
 

Json Généré 

{
  "contexte_principal": "commercial",
  "domaine_medical": "néphrologie",
  "type_document": "autre",
  "population_cible": "clients",
  "maladies_detectees": [
    "hyperkaliémie"
  ],
  "clients_detectes": [
    "AstraZeneca"
  ],
  "bases_detectees": [],
  "client_principal": "AstraZeneca",
  "base_principale": "null",
  "contient_maladie": true,
  "confiance": "moyenne",
  "score_semantique": 0.85,
  "justification": "Mission de renfort opérationnel pour le médicament Lokelma (traitement de l'hyperkaliémie) chez le client AstraZeneca, sans référence à une base de données ni à un format documentaire standard.",
  "titre_normalise": "20250428 IQVIA pour AZ_Placement consultant renfort Lokelma V2"
}

            """)
        ])
        
        prompt_value = analysis_prompt_template.invoke({"titre": titre})
        response = llm.invoke(prompt_value.to_messages())
        content = response.content.strip()
        
        # Nettoyer le JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        resultat = json.loads(content.strip())
        
        # Validation et enrichissement
        if "categorie_medicale" not in resultat:
            resultat["categorie_medicale"] = resultat.get("domaine_medical", "aucune")
        
        # Assurer la cohérence clients/bases de données
        if not resultat.get("clients_detectes"):
            resultat["clients_detectes"] = []
        if not resultat.get("bases_detectees"):
            resultat["bases_detectees"] = []
        
        # Déterminer le client/base principal
        if resultat.get("clients_detectes") and not resultat.get("client_principal"):
            resultat["client_principal"] = resultat["clients_detectes"][0]
        if resultat.get("bases_detectees") and not resultat.get("base_principale"):
            resultat["base_principale"] = resultat["bases_detectees"][0]
        
        # Ajuster le contexte si client ou base détecté
        if resultat.get("client_principal"):
            resultat["contexte_principal"] = "client"
            resultat["categorie_medicale"] = "client"
        elif resultat.get("base_principale"):
            resultat["contexte_principal"] = "base_donnees"
            resultat["categorie_medicale"] = "base_donnees"
        
        # Calculer score sémantique si absent
        if "score_semantique" not in resultat or not isinstance(resultat["score_semantique"], (int, float)):
            contexte = resultat.get("contexte_principal", "autre")
            domaine = resultat.get("domaine_medical", "aucun")
            
            score = 0.3  # Base
            if contexte != "autre": score += 0.2
            if domaine != "aucun": score += 0.2
            if len(resultat.get("maladies_detectees", [])) > 0: score += 0.2
            if resultat.get("confiance") == "haute": score += 0.1
            
            resultat["score_semantique"] = min(0.95, score)
        
        return resultat
        
    except Exception as e:
        print(f"❌ Erreur LLM sémantique pour '{titre[:30]}...': {e}")
        return detection_mots_cles_medicaux(titre)

def rechercher_fichiers_filtres():
    """Phase 1: Recherche et filtre les fichiers par extension, date et taille"""
    print("🔍 PHASE 1: Recherche et filtrage des fichiers...")
    print("-" * 50)
    
    if not os.path.exists(CHEMIN_SOURCE):
        print(f"❌ Erreur: {CHEMIN_SOURCE} n'existe pas")
        return []
    
    # Définition des filtres
    DATE_LIMITE = datetime.now() - timedelta(days=365)  # Fichiers de moins d'un an
    TAILLE_MIN_OCTETS = 1 * 1024         # 1 KB minimum (pour éviter fichiers vides)
    TAILLE_MAX_OCTETS = 50 * 1024 * 1024  # 50 MB maximum
    TAILLE_CLASSIFICATION = 3000 * 1024   # 2 MB - Seuil pour classification sémantique
    
    print(f"📅 Filtre date: fichiers modifiés après le {DATE_LIMITE.strftime('%d/%m/%Y')}")
    print(f"📏 Filtre taille: entre {TAILLE_MIN_OCTETS//1024} KB et {TAILLE_MAX_OCTETS//1024//1024} MB")
    print(f"🧠 Classification sémantique: fichiers > {TAILLE_CLASSIFICATION//1024} KB seulement")
    print(f"📁 Fichiers ≤ {TAILLE_CLASSIFICATION//1024} KB → dossier AUTRES automatiquement")
    print()
    
    fichiers_trouves = []
    dossiers_stats = {}
    stats_filtrage = {
        'total_examines': 0,
        'rejetes_extension': 0,
        'rejetes_taille': 0, 
        'rejetes_date': 0,
        'rejetes_acces': 0,
        'acceptes': 0
    }
    
    for item in os.listdir(CHEMIN_SOURCE):
        item_path = os.path.join(CHEMIN_SOURCE, item)
        if os.path.isdir(item_path):
            print(f"📂 Analyse du dossier: {item}")
            count_dossier = 0
            
            for root, dirs, files in os.walk(item_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    stats_filtrage['total_examines'] += 1
                    
                    # Vérification de l'extension
                    if not file.lower().endswith(('.ppt', '.pptx', '.pdf')):
                        stats_filtrage['rejetes_extension'] += 1
                        continue
                    
                    try:
                        # Récupération des métadonnées
                        taille = os.path.getsize(file_path)
                        date_mod = datetime.fromtimestamp(os.path.getmtime(file_path))
                        
                        # Filtrage par taille
                        if not (TAILLE_MIN_OCTETS <= taille <= TAILLE_MAX_OCTETS):
                            stats_filtrage['rejetes_taille'] += 1
                            continue
                        
                        # Filtrage par date  
                        if date_mod < DATE_LIMITE:
                            stats_filtrage['rejetes_date'] += 1
                            continue
                        
                        # Fichier accepté
                        fichier_info = {
                            'chemin': file_path,
                            'nom': file,
                            'taille': taille,
                            'date_modification': date_mod,
                            'taille_mb': round(taille / (1024*1024), 2),
                            'taille_kb': round(taille / 1024, 1),
                            'age_jours': (datetime.now() - date_mod).days,
                            'classification_semantique': taille >= TAILLE_CLASSIFICATION  # True si > 2MB
                        }
                        
                        fichiers_trouves.append(fichier_info)
                        count_dossier += 1
                        stats_filtrage['acceptes'] += 1
                        
                    except (OSError, PermissionError) as e:
                        stats_filtrage['rejetes_acces'] += 1
                        print(f"   ⚠️ Ignoré (accès refusé): {os.path.basename(file_path)}")
            
            dossiers_stats[item] = count_dossier
            print(f"   ✅ {count_dossier} fichier(s) retenu(s) après filtrage")
    
    # Affichage des statistiques détaillées
    print(f"\n📊 STATISTIQUES DE FILTRAGE:")
    print(f"   • Fichiers examinés: {stats_filtrage['total_examines']}")
    print(f"   • ❌ Rejetés - extension: {stats_filtrage['rejetes_extension']}")
    print(f"   • ❌ Rejetés - taille: {stats_filtrage['rejetes_taille']}")
    print(f"   • ❌ Rejetés - date: {stats_filtrage['rejetes_date']}")
    print(f"   • ❌ Rejetés - accès: {stats_filtrage['rejetes_acces']}")
    print(f"   • ✅ RETENUS: {stats_filtrage['acceptes']}")
    
    print(f"\n📁 RÉPARTITION PAR DOSSIER:")
    for dossier, count in dossiers_stats.items():
        print(f"   • {dossier}: {count} fichier(s)")
    
    return fichiers_trouves

def trier_fichiers_par_criteres(fichiers_info):
    """Trie les fichiers par différents critères et affiche des statistiques"""
    print(f"\n📈 PHASE 1.5: Analyse et tri des fichiers retenus...")
    print("-" * 50)
    
    if not fichiers_info:
        print("❌ Aucun fichier à analyser")
        return fichiers_info
    
    # Tri par taille (décroissant)
    fichiers_par_taille = sorted(fichiers_info, key=lambda x: x['taille'], reverse=True)
    print(f"📏 Top 5 fichiers les plus volumineux:")
    for i, f in enumerate(fichiers_par_taille[:5], 1):
        print(f"   {i}. {f['nom'][:50]}... ({f['taille_mb']} MB)")
    
    # Tri par date (plus récent d'abord) 
    fichiers_par_date = sorted(fichiers_info, key=lambda x: x['date_modification'], reverse=True)
    print(f"\n📅 Top 5 fichiers les plus récents:")
    for i, f in enumerate(fichiers_par_date[:5], 1):
        date_str = f['date_modification'].strftime('%d/%m/%Y')
        print(f"   {i}. {f['nom'][:50]}... ({date_str}, {f['age_jours']} jours)")
    
    # Statistiques de répartition
    tailles = [f['taille_mb'] for f in fichiers_info]
    ages = [f['age_jours'] for f in fichiers_info]
    
    print(f"\n📊 STATISTIQUES DESCRIPTIVES:")
    print(f"   Taille - Moyenne: {sum(tailles)/len(tailles):.1f} MB, Max: {max(tailles):.1f} MB, Min: {min(tailles):.1f} MB")
    print(f"   Âge - Moyenne: {sum(ages)//len(ages)} jours, Max: {max(ages)} jours, Min: {min(ages)} jours")
    
    # Répartition par tranches de taille et éligibilité classification
    tranches_taille = {'< 1MB': 0, '1-2MB': 0, '2-5MB': 0, '5-20MB': 0, '> 20MB': 0}
    eligibles_classification = 0
    
    for f in fichiers_info:
        mb = f['taille_mb']
        if mb < 1: tranches_taille['< 1MB'] += 1
        elif mb < 2: tranches_taille['1-2MB'] += 1  
        elif mb < 5: tranches_taille['2-5MB'] += 1
        elif mb < 20: tranches_taille['5-20MB'] += 1
        else: tranches_taille['> 20MB'] += 1
        
        if f['classification_semantique']:
            eligibles_classification += 1
    
    print(f"\n📏 RÉPARTITION PAR TAILLE:")
    for tranche, count in tranches_taille.items():
        pct = (count / len(fichiers_info) * 100) if fichiers_info else 0
        print(f"   • {tranche}: {count} fichiers ({pct:.1f}%)")
    
    print(f"\n🧠 ÉLIGIBILITÉ CLASSIFICATION SÉMANTIQUE:")
    print(f"   • Fichiers > 2MB (analysés): {eligibles_classification}")
    print(f"   • Fichiers ≤ 2MB (→ AUTRES): {len(fichiers_info) - eligibles_classification}")
    
    return fichiers_info

def copier_fichiers(fichiers_info):
    """Phase 2: Copie vers Depots avec informations enrichies"""
    print(f"\n📋 PHASE 2: Copie vers {CHEMIN_DEPOTS}...")
    print("-" * 50)
    
    # Créer le dossier Depots
    os.makedirs(CHEMIN_DEPOTS, exist_ok=True)
    print(f"✅ Dossier Depots prêt")
    
    copied = 0
    taille_totale = 0
    
    for fichier_info in fichiers_info:
        file_path = fichier_info['chemin']
        file_name = fichier_info['nom']
        destination = os.path.join(CHEMIN_DEPOTS, file_name)
        
        try:
            shutil.copy(file_path, destination)
            copied += 1
            taille_totale += fichier_info['taille']
        except Exception as e:
            print(f"❌ Erreur copie {file_name}: {e}")
    
    print(f"✅ {copied}/{len(fichiers_info)} fichiers copiés")
    print(f"📦 Taille totale copiée: {taille_totale/(1024*1024):.1f} MB")
    return copied

def analyser_et_classer_semantique():
    """Phase 3: Analyse sémantique LLM et classification avancée (> 2MB seulement)"""
    print(f"\n🧠 PHASE 3: Analyse sémantique et classification...")
    print("-" * 50)
    
    # Mode LLM ou fallback
    use_llm = llm is not None
    print(f"Mode: {'🔥 LLM Sémantique' if use_llm else '🔧 Mots-clés enrichis'}")
    
    fichiers_a_analyser = [f for f in os.listdir(CHEMIN_DEPOTS) 
                          if f.lower().endswith(('.ppt', '.pptx', '.pdf'))]
    
    # Récupérer les infos de taille des fichiers copiés
    fichiers_avec_taille = []
    for file_name in fichiers_a_analyser:
        file_path = os.path.join(CHEMIN_DEPOTS, file_name)
        try:
            taille = os.path.getsize(file_path)
            fichiers_avec_taille.append({
                'nom': file_name,
                'taille': taille,
                'taille_mb': round(taille / (1024*1024), 2),
                'taille_kb': round(taille / 1024, 1),
                'eligible_classification': taille >= (3000 * 1024)  # > 2MB
            })
        except:
            # Si erreur, on considère comme petit fichier
            fichiers_avec_taille.append({
                'nom': file_name,
                'taille': 0,
                'taille_mb': 0,
                'taille_kb': 0,
                'eligible_classification': False
            })
    
    analyses = []
    medicaux = 0
    contextes_stats = {}
    petits_fichiers = 0
    
    print(f"📊 Répartition:")
    eligibles = sum(1 for f in fichiers_avec_taille if f['eligible_classification'])
    print(f"   • Fichiers > 2MB (analyse sémantique): {eligibles}")
    print(f"   • Fichiers ≤ 2MB (→ AUTRES direct): {len(fichiers_avec_taille) - eligibles}")
    print()
    
    for i, fichier_info in enumerate(fichiers_avec_taille, 1):
        file_name = fichier_info['nom']
        titre = os.path.splitext(file_name)[0]
        taille_str = f"{fichier_info['taille_kb']} KB" if fichier_info['taille_mb'] < 1 else f"{fichier_info['taille_mb']} MB"
        
        print(f"[{i:2d}/{len(fichiers_avec_taille)}] {file_name[:40]}... ({taille_str})")
        
        # Vérifier si éligible à la classification sémantique
        if not fichier_info['eligible_classification']:
            # Fichier ≤ 2MB → Dossier AUTRES automatiquement
            analyse = {
                'nom_fichier': file_name,
                'titre': titre,
                'taille_mb': fichier_info['taille_mb'],
                'contient_maladie': False,
                'categorie_medicale': 'autres',
                'contexte_principal': 'autre',
                'confiance': 'faible',
                'score_semantique': 0.1,
                'justification': f'Fichier de petite taille ({taille_str}) → AUTRES automatiquement',
                'clients_detectes': [],
                'bases_detectees': [],
                'maladies_detectees': []
            }
            analyses.append(analyse)
            petits_fichiers += 1
            print(f"   📁 → AUTRES (taille < 2MB)")
            continue
        
        # Classification sémantique pour fichiers > 2MB
        if use_llm:
            analyse = analyser_titre_avec_llm_semantique(titre)
        else:
            analyse = detection_mots_cles_medicaux(titre)
        
        # Enrichir avec métadonnées
        analyse['nom_fichier'] = file_name
        analyse['taille_mb'] = fichier_info['taille_mb']
        
        # Compter et afficher résultats
        if analyse.get('contient_maladie', False):
            medicaux += 1
        
        contexte = analyse.get('contexte_principal', 'autre')
        contextes_stats[contexte] = contextes_stats.get(contexte, 0) + 1
        
        # Affichage du résultat
        categorie = analyse.get('categorie_medicale', 'aucune')
        confiance = analyse.get('confiance', 'inconnue')
        score = analyse.get('score_semantique', 0)
        
        if analyse.get('clients_detectes'):
            client_info = f" [Client: {', '.join(analyse['clients_detectes'])}]"
        elif analyse.get('bases_detectees'):
            client_info = f" [Base: {', '.join(analyse['bases_detectees'])}]"
        else:
            client_info = ""
        
        print(f"   🎯 {categorie.upper()} ({confiance}, score:{score:.2f}){client_info}")
        
        if analyse.get('maladies_detectees'):
            print(f"   🏥 Termes: {', '.join(analyse['maladies_detectees'])}")
        
        analyses.append(analyse)
    
    print(f"\n📊 RÉSULTATS DE CLASSIFICATION:")
    print(f"   • Fichiers analysés sémantiquement: {len(analyses) - petits_fichiers}")
    print(f"   • Fichiers → AUTRES (< 2MB): {petits_fichiers}")
    print(f"   • Fichiers médicaux détectés: {medicaux}")
    print(f"   • Score sémantique moyen: {sum(a.get('score_semantique', 0) for a in analyses) / len(analyses):.2f}")
    
    print(f"\n📈 RÉPARTITION PAR CONTEXTE:")
    for contexte, count in sorted(contextes_stats.items()):
        pct = (count / len(analyses) * 100) if analyses else 0
        print(f"   • {contexte}: {count} fichiers ({pct:.1f}%)")
    
    return analyses

def creer_dossiers_et_deplacer(analyses):
    """Phase 4: Création des dossiers de classification et déplacement"""
    print(f"\n📁 PHASE 4: Création dossiers et déplacement...")
    print("-" * 50)
    
    # Mapping des catégories vers dossiers
    mapping_dossiers = {
        'oncologie': 'ONCOLOGIE',
        'cardiologie': 'CARDIOLOGIE', 
        'neurologie': 'NEUROLOGIE',
        'diabetologie': 'DIABETOLOGIE',
        'pneumologie': 'PNEUMOLOGIE',
        'dermatologie': 'DERMATOLOGIE',
        'pharmacovigilance': 'PHARMACOVIGILANCE',
        'formation': 'FORMATION',
        'commercial': 'COMMERCIAL',
        'recherche': 'RECHERCHE',
        'reglementaire': 'REGLEMENTAIRE',
        'client': 'CLIENTS',
        'base_donnees': 'BASES_DONNEES',
        'autres': 'AUTRES',
        'aucune': 'AUTRES'
    }
    
    # Créer tous les dossiers nécessaires
    dossiers_crees = set()
    for categorie in mapping_dossiers.values():
        dossier_path = os.path.join(CHEMIN_DEPOTS, categorie)
        os.makedirs(dossier_path, exist_ok=True)
        dossiers_crees.add(categorie)
    
    print(f"✅ {len(dossiers_crees)} dossiers de classification créés")
    
    # Déplacer les fichiers
    stats_deplacement = {}
    erreurs_deplacement = []
    
    for analyse in analyses:
        file_name = analyse['nom_fichier']
        categorie = analyse.get('categorie_medicale', 'autres')
        dossier_cible = mapping_dossiers.get(categorie, 'AUTRES')
        
        source_path = os.path.join(CHEMIN_DEPOTS, file_name)
        destination_path = os.path.join(CHEMIN_DEPOTS, dossier_cible, file_name)
        
        try:
            if os.path.exists(source_path):
                # Gérer les doublons
                if os.path.exists(destination_path):
                    base, ext = os.path.splitext(file_name)
                    counter = 1
                    while os.path.exists(destination_path):
                        new_name = f"{base}_({counter}){ext}"
                        destination_path = os.path.join(CHEMIN_DEPOTS, dossier_cible, new_name)
                        counter += 1
                
                shutil.move(source_path, destination_path)
                stats_deplacement[dossier_cible] = stats_deplacement.get(dossier_cible, 0) + 1
                
        except Exception as e:
            erreurs_deplacement.append(f"{file_name}: {str(e)}")
            print(f"❌ Erreur déplacement {file_name}: {e}")
    
    print(f"\n📊 RÉSULTATS DE DÉPLACEMENT:")
    total_deplaces = sum(stats_deplacement.values())
    for dossier, count in sorted(stats_deplacement.items()):
        pct = (count / total_deplaces * 100) if total_deplaces > 0 else 0
        print(f"   • {dossier}: {count} fichiers ({pct:.1f}%)")
    
    if erreurs_deplacement:
        print(f"\n❌ ERREURS DE DÉPLACEMENT ({len(erreurs_deplacement)}):")
        for erreur in erreurs_deplacement[:5]:  # Limiter à 5 erreurs
            print(f"   • {erreur}")
        if len(erreurs_deplacement) > 5:
            print(f"   • ... et {len(erreurs_deplacement) - 5} autres erreurs")
    
    return stats_deplacement

def generer_rapport_final(analyses, stats_deplacement):
    """Phase 5: Génération du rapport final détaillé"""
    print(f"\n📋 PHASE 5: Génération du rapport final...")
    print("-" * 50)
    
    # Créer le rapport JSON détaillé
    rapport = {
        'metadata': {
            'date_execution': datetime.now().isoformat(),
            'version_script': '2.0',
            'mode_llm': llm is not None,
            'total_fichiers': len(analyses)
        },
        'statistiques_globales': {
            'fichiers_medicaux': sum(1 for a in analyses if a.get('contient_maladie', False)),
            'fichiers_clients': sum(1 for a in analyses if a.get('clients_detectes')),
            'fichiers_bases_donnees': sum(1 for a in analyses if a.get('bases_detectees')),
            'score_semantique_moyen': round(sum(a.get('score_semantique', 0) for a in analyses) / len(analyses), 3) if analyses else 0
        },
        'repartition_dossiers': stats_deplacement,
        'analyses_detaillees': analyses
    }
    
    # Sauvegarder le rapport JSON
    rapport_path = os.path.join(CHEMIN_DEPOTS, 'rapport_classification.json')
    try:
        with open(rapport_path, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False, default=str)
        print(f"✅ Rapport JSON sauvegardé: {rapport_path}")
    except Exception as e:
        print(f"❌ Erreur sauvegarde rapport: {e}")
    
    # Générer rapport texte lisible
    rapport_txt_path = os.path.join(CHEMIN_DEPOTS, 'rapport_classification.txt')
    try:
        with open(rapport_txt_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RAPPORT DE CLASSIFICATION MÉDICALE AUTOMATIQUE\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"📅 Date d'exécution: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"🔧 Mode: {'LLM Sémantique' if llm else 'Mots-clés enrichis'}\n")
            f.write(f"📁 Dossier source: {CHEMIN_SOURCE}\n")
            f.write(f"📁 Dossier dépôt: {CHEMIN_DEPOTS}\n\n")
            
            f.write("📊 STATISTIQUES GLOBALES\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total fichiers traités: {len(analyses)}\n")
            f.write(f"Fichiers médicaux: {rapport['statistiques_globales']['fichiers_medicaux']}\n")
            f.write(f"Fichiers clients: {rapport['statistiques_globales']['fichiers_clients']}\n")
            f.write(f"Fichiers bases données: {rapport['statistiques_globales']['fichiers_bases_donnees']}\n")
            f.write(f"Score sémantique moyen: {rapport['statistiques_globales']['score_semantique_moyen']}\n\n")
            
            f.write("📁 RÉPARTITION PAR DOSSIERS\n")
            f.write("-" * 40 + "\n")
            for dossier, count in sorted(stats_deplacement.items()):
                pct = (count / len(analyses) * 100) if analyses else 0
                f.write(f"{dossier}: {count} fichiers ({pct:.1f}%)\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("DÉTAIL DES CLASSIFICATIONS\n")
            f.write("=" * 80 + "\n\n")
            
            # Grouper par dossier
            analyses_par_dossier = {}
            mapping_dossiers = {
                'oncologie': 'ONCOLOGIE', 'cardiologie': 'CARDIOLOGIE', 
                'neurologie': 'NEUROLOGIE', 'diabetologie': 'DIABETOLOGIE',
                'pneumologie': 'PNEUMOLOGIE', 'dermatologie': 'DERMATOLOGIE',
                'pharmacovigilance': 'PHARMACOVIGILANCE', 'formation': 'FORMATION',
                'commercial': 'COMMERCIAL', 'recherche': 'RECHERCHE',
                'reglementaire': 'REGLEMENTAIRE', 'client': 'CLIENTS',
                'base_donnees': 'BASES_DONNEES', 'autres': 'AUTRES', 'aucune': 'AUTRES'
            }
            
            for analyse in analyses:
                categorie = analyse.get('categorie_medicale', 'autres')
                dossier = mapping_dossiers.get(categorie, 'AUTRES')
                if dossier not in analyses_par_dossier:
                    analyses_par_dossier[dossier] = []
                analyses_par_dossier[dossier].append(analyse)
            
            for dossier, fichiers in sorted(analyses_par_dossier.items()):
                f.write(f"\n📂 {dossier} ({len(fichiers)} fichiers)\n")
                f.write("-" * (len(dossier) + 20) + "\n")
                
                for analyse in sorted(fichiers, key=lambda x: x.get('score_semantique', 0), reverse=True):
                    f.write(f"• {analyse['nom_fichier']}\n")
                    f.write(f"  Taille: {analyse.get('taille_mb', 0):.1f} MB\n")
                    f.write(f"  Catégorie: {analyse.get('categorie_medicale', 'N/A')}\n")
                    f.write(f"  Confiance: {analyse.get('confiance', 'N/A')}\n")
                    f.write(f"  Score: {analyse.get('score_semantique', 0):.2f}\n")
                    
                    if analyse.get('clients_detectes'):
                        f.write(f"  Clients: {', '.join(analyse['clients_detectes'])}\n")
                    if analyse.get('bases_detectees'):
                        f.write(f"  Bases: {', '.join(analyse['bases_detectees'])}\n")
                    if analyse.get('maladies_detectees'):
                        f.write(f"  Termes médicaux: {', '.join(analyse['maladies_detectees'])}\n")
                    if analyse.get('justification'):
                        f.write(f"  Justification: {analyse['justification']}\n")
                    
                    f.write("\n")
        
        print(f"✅ Rapport texte sauvegardé: {rapport_txt_path}")
    except Exception as e:
        print(f"❌ Erreur sauvegarde rapport texte: {e}")
    
    return rapport

def main():
    """Fonction principale - orchestration complète"""
    print("🏥 CLASSIFICATEUR MÉDICAL IQVIA - ANALYSE SÉMANTIQUE")
    print("=" * 60)
    print(f"📅 Démarrage: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    try:
        # Phase 1: Recherche et filtrage
        fichiers_info = rechercher_fichiers_filtres()
        if not fichiers_info:
            print("❌ Aucun fichier trouvé. Arrêt du processus.")
            return
        
        # Phase 1.5: Tri et analyse
        fichiers_info = trier_fichiers_par_criteres(fichiers_info)
        
        # Phase 2: Copie
        copied = copier_fichiers(fichiers_info)
        if copied == 0:
            print("❌ Aucun fichier copié. Arrêt du processus.")
            return
        
        # Phase 3: Analyse sémantique
        analyses = analyser_et_classer_semantique()
        if not analyses:
            print("❌ Aucune analyse réalisée. Arrêt du processus.")
            return
        
        # Phase 4: Déplacement dans dossiers
        stats_deplacement = creer_dossiers_et_deplacer(analyses)
        
        # Phase 5: Rapport final
        rapport = generer_rapport_final(analyses, stats_deplacement)
        
        print(f"\n🎉 CLASSIFICATION TERMINÉE AVEC SUCCÈS!")
        print("=" * 60)
        print(f"✅ {len(analyses)} fichiers traités")
        print(f"📁 {len(stats_deplacement)} dossiers créés")
        print(f"📋 Rapports générés dans {CHEMIN_DEPOTS}")
        print(f"⏱️ Durée totale: {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        print("🔧 Vérifiez la configuration et les chemins d'accès")
        raise

if __name__ == "__main__":
    main()