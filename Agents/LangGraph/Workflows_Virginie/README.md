# Système d'Analyse PDF avec LangGraph

## Vue d'ensemble

Ce projet implémente un système d'analyse documentaire en utilisant LangGraph pour traiter des documents PDF administratifs, spécifiquement orienté vers l'identification et l'extraction de terme identifié . Le système est composé de deux workflows complémentaires qui automatisent l'ensemble du processus d'analyse documentaire.

## Architecture du Système

### Workflow 1 : Analyse Primaire PDF
**Pipeline :** `Extraction → Analyse → Export`

Le premier workflow constitue le cœur du système d'analyse documentaire. Il traite les pages d'un documents PDF un découpage contextuel.

#### Fonctionnement
1. **Extraction** : Lecture et prétraitement du PDF avec nettoyage automatique du texte
2. **Analyse** : Application d'un modèle LLM pour identifier les délégations de pouvoir
3. **Export** : Génération de fichiers de synthèse structurés

#### Traitement par Lots
Une caractéristique distinctive de ce workflow réside dans son approche de **traitement par lots réduits**. Au lieu d'analyser l'intégralité du document en une seule opération, le système segmente le traitement par tranches de 2 pages (paramétrable à 3 ou plus).

**Avantages de cette approche :**
- **Élimination des hallucinations** : La réduction du contexte permet au LLM de maintenir sa précision
- **Fiabilité accrue** : Zéro erreur d'interprétation observée vs. quelques rares hallucinations en traitement global
- **Contrôle qualité** : Validation possible tranche par tranche

**Limitation :**
- Nécessite l'exécution multiple du workflow pour traiter un document complet

### Workflow 2 : Analyse Secondaire de Synthèse
**Pipeline :** `Lecture → Formatage → Statistiques → Export`

Le second workflow exploite les résultats du premier pour produire des analyses approfondies.

#### Fonctionnement
1. **Lecture** : Ingestion du fichier de synthèse généré par le Workflow 1
2. **Formatage** : Extraction et structuration des données clés
3. **Statistiques** : Analyse quantitative et identification de patterns
4. **Export** : Génération de rapports statistique

## Prompt 

### Chain of Thought (CoT)
Le système implémente des techniques de prompting   basées sur les chaînes de raisonnement (Chains Of Thought). Cette approche guide le modèle LLM à travers un processus de réflexion structuré.

**Variantes CoT utilisées :**
- **Step-back Prompting** : Décomposition des tâches complexes en étapes élémentaires
- **Thread of Thought** : Maintien de la cohérence logique à travers les analyses
- **Analogical Prompting** : Apprentissage par exemples similaires pour améliorer la généralisation
- **Memory of Thought** : Conservation du contexte de raisonnement entre les étapes d'analyse
- **Active Prompting** : Adaptation dynamique des questions selon les réponses précédentes
- **Contrastive Promptingt** : Utilisation d'exemples positifs et négatifs pour affiner la compréhension

### Analogical Prompting
l'analogical prompting à été utilisé pour le nœud d'analyse principal. Cette technique consiste à fournir au modèle des exemples concrets similaires au cas d'usage cible, permettant une généralisation par analogie.

**Principe :**
- Présentation d'exemples types avec leur résolution complète
- Guidance par l'exemple plutôt que par l'instruction abstraite
- Amélioration significative de la précision d'extraction

## Outputs : 3 fichiers md

### Workflow 1
- **Fichier de synthèse** : `{nom_pdf}_synthese_{timestamp}.md`
- Consolidation de toutes les analyses par tranches
- Structure hiérarchique avec métadonnées complètes

### Workflow 2
- **Rapport formaté** : `{synthese}_formatted_{timestamp}.md`
- **Analyse statistique** : `{synthese}_statistics_{timestamp}.md`
- Horodatage automatique pour la traçabilité

## Avantages Opérationnels

### Précision
- **Taux d'erreur réduit** grâce au traitement par lots
- **Validation multi-niveaux** avec workflows séquentiels
- **Cohérence terminologique** via l'analogical prompting

### Scalabilité
- **Architecture modulaire** permettant l'adaptation à différents types de documents
- **Traitement parallélisable** des tranches pour optimisation future
- **Extensibilité** des analyses statistiques

### Traçabilité
- **Horodatage systématique** de tous les outputs
- **Conservation des fichiers intermédiaires** pour audit
- **Métadonnées complètes** sur les paramètres de traitement

## Configuration et Utilisation

### Paramètres Principaux
```python
pdf_filename = "document.pdf"  # Document à analyser
start_page = 102               # Page de début
end_page = 118                 # Page de fin
step = 2                       # Taille des lots (recommandé: 2-3)
```

### Exécution
```python
# Workflow 1 - Analyse PDF
result = process_pdf(pdf_filename, start_page, end_page)

# Workflow 2 - Analyse de synthèse (automatique après Workflow 1)
synthesis_result = process_synthesis_analysis(synthesis_file_path)
```

## Technologies Utilisées

- **LangGraph** : Orchestration des workflows
- **LangChain** : Interface LLM et gestion des prompts
- **OpenAI GPT-4o-mini** : Moteur d'analyse linguistique
- **PDFPlumber** : Extraction de texte PDF
- **Python** : Environnement de développement

 

 
