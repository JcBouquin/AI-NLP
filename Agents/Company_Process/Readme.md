## 📝 **README.md - Classificateur Médical avec LLM**

```markdown
# �� Classificateur Médical - Analyse Sémantique

## �� Description

Classificateur automatique de documents médicaux utilisant l'analyse sémantique avec GPT-4o-mini pour organiser intelligemment des fichiers pharmaceutiques et médicaux.

## �� Objectifs

- **Automatiser** la classification de documents médicaux (PDF, PPT, PPTX)
- **Identifier** automatiquement les clients, bases de données et domaines médicaux
- **Organiser** les fichiers en 4 catégories : CLIENTS, BASES_DONNEES, MALADIES, AUTRES
- **Générer** des rapports détaillés avec justifications sémantiques
- **Consolider** tous les fichiers dans un dossier global

## 🔄 Workflow

### Phase 1-2 : Extraction et Copie
- Recherche et filtrage des fichiers par extension, date, taille
- Copie vers le dossier de travail

### Phase 3 : Analyse Sémantique
- Classification automatique avec GPT-4o-mini
- Analyse des titres de documents (pas du contenu)

### Phase 4-5 : Organisation
- Création des dossiers de classification
- Déplacement des fichiers dans les catégories appropriées
- Consolidation dans `results_global`

### Phase 6 : Rapports
- Génération des rapports JSON et TXT
- Statistiques détaillées de classification

### Phase 7 : Dépôt SharePoint (Optionnel)
- Upload du dossier `results_global` vers SharePoint
- Gestion des erreurs et rapport d'upload

## 🧠 Intelligence Artificielle

- **Modèle** : GPT-4o-mini
- **Température** : 0 (cohérence maximale)
- **Analyse** : Titres de documents uniquement
- **Classification** : Basée sur le contexte sémantique

## 🚀 Utilisation

### Prérequis
```bash
pip install langchain-openai langchain-core
```

### Variables d'Environnement
```bash
OPENAI_API_KEY=votre_clé_api_openai
SHAREPOINT_URL=https://votreentreprise.sharepoint.com
SHAREPOINT_SITE=votre-site
SHAREPOINT_LIBRARY=Documents Partagés/Classification_Medicale
SHAREPOINT_USERNAME=votre.email@entreprise.com
SHAREPOINT_PASSWORD=votre_mot_de_passe
```

### Exécution
```python
# Exécution complète du workflow
fichiers_info = rechercher_fichiers_filtres()
copied = copier_fichiers(fichiers_info)
analyses = analyser_et_classer_semantique()
stats_deplacement = creer_dossiers_et_deplacer(analyses)
fichiers_consolides = consolider_resultats_globaux()
rapport = generer_rapport_final(analyses, stats_deplacement)

# Dépôt SharePoint (optionnel)
# success_sharepoint = deposer_vers_sharepoint()
```

## �� Structure des Dossiers

```
Depots/
├── CLIENTS/           # Documents liés aux clients
├── BASES_DONNEES/     # Documents liés aux bases de données
├── MALADIES/          # Documents médicaux par domaine
├── AUTRES/            # Documents non classifiables
├── results_global/    # Consolidation de tous les fichiers
└── rapports/          # Rapports de classification
```

## �� Rapports Générés

- **rapport_classification.json** : Données structurées
- **rapport_classification.txt** : Rapport lisible

## ⚠️ Limitations

- **Analyse des titres uniquement** (pas du contenu des documents)
- **Dépendant de la qualité** des conventions de nommage
- **Coût API OpenAI** pour l'analyse sémantique

## 🔧 Configuration

- **Seuil de classification** : 20 KB (configurable)
- **Extensions supportées** : PDF, PPT, PPTX
- **Filtre de date** : Fichiers de moins d'un an
- **Mode LLM** : Automatique si clé API disponible

## 📈 Avantages

- **Flexibilité** : S'adapte aux nouveaux termes
- **Contexte** : Comprend l'intention derrière les titres
- **Traçabilité** : Justification de chaque décision
- **Précision** : Classification multi-critères intelligente

## 🎯 Cas d'Usage

- **Organisation** de documents pharmaceutiques
- **Classification** automatique de bases documentaires
- **Démonstration** de la valeur des LLM vs mots-clés
- **Workflow** de gestion documentaire automatisé
```

**Ce README donne une vue d'ensemble claire sans entrer dans les détails techniques** 📚
