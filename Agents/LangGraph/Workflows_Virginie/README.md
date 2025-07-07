# 📄 Analyseur de Délégations PDF avec LangGraph

## 🎯 Vue d'ensemble

Ce projet utilise **LangGraph** et **GPT-4o-mini** pour analyser automatiquement les documents PDF de délégations de pouvoir. Il extrait, analyse et produit des statistiques sur les délégations administratives avec export multi-format.

### 🔄 Architecture du Workflow

Le système fonctionne avec **4 nœuds séquentiels** :

```
📖 EXTRACTION → 🔬 ANALYSE → 📊 STATISTIQUES → 📤 EXPORT → ✅ FIN
```

---

## 🏗️ Installation

### Prérequis
- Python 3.8+
- Jupyter Notebook
- Clé API OpenAI

### Dépendances
```bash
pip install langchain-openai
pip install langgraph
pip install pdfplumber
pip install reportlab
pip install pygraphviz  # Pour l'affichage des graphiques
```

### Configuration
1. Définir votre clé API OpenAI :
```bash
export OPENAI_API_KEY="votre-clé-api"
```

2. Ajuster le chemin de base dans le code :
```python
BASE_DIR = os.path.abspath(r"C:\Votre\Chemin\Vers\LangGraph")
```

---

## 🔍 Détail des Nœuds

### 1️⃣ Nœud EXTRACTION (`extraction_node`)

**Objectif :** Extraire le texte des pages PDF spécifiées

**Processus :**
- 🔍 Localise le fichier PDF dans plusieurs emplacements possibles
- 📄 Extrait le texte des pages demandées avec `pdfplumber`
- 🧹 Nettoie et formate le texte (correction des sauts de ligne, articles)
- 💾 Sauvegarde le texte extrait dans `textes_extraits/`

**Entrées :**
- `pdf_filename` : Nom du fichier PDF
- `start_page`, `end_page` : Plage de pages (optionnel)

**Sorties :**
- `extracted_text` : Texte complet extrait
- `extracted_file_path` : Chemin du fichier texte sauvé

**Exemple de fichier généré :**
```
==================== PAGE 117 ====================

Article 25

Délégation est donnée à M. Jean MARTIN, directeur des ressources humaines...
```

### 2️⃣ Nœud ANALYSE (`analysis_node`)

**Objectif :** Analyser le texte pour identifier les délégations de pouvoir

**Processus Chain of Thought :**

1. **Lecture du document** : Compréhension du contexte
2. **Recherche "délégation est donnée"** : Identification des bénéficiaires
3. **Recherche "en cas d'absence"** : Identification des suppléants
4. **Formatage structuré** : Organisation des résultats

**Méthode d'analyse :**
- 🔍 Recherche systématique des expressions clés
- 👥 Extraction des noms et fonctions
- 📝 Gestion des cas particuliers (délégations multiples)
- ❌ Indication "Non mentionné" si absence d'information

**Sortie type :**
```
Article 25
[En cas d'absence ou d'empêchement de] : M. Pierre DUPONT, fonction : directeur général
[Délégation est donnée à] : M. Jean MARTIN, fonction : directeur des ressources humaines

Article 26
[En cas d'absence ou d'empêchement de] : Non mentionné
[Délégation est donnée à] : Mme Sophie BERNARD, Mme Claire ROUSSEAU, fonction : gestionnaires de l'unité budget
```

### 3️⃣ Nœud STATISTIQUES (`statistics_node`)

**Objectif :** Analyser les patterns et produire des insights statistiques

**Méthode Chain of Thought en 5 étapes :**

#### Étape 1: Inventaire des données
- 📊 Comptage total d'articles analysés
- ✅ Articles avec délégations vs sans délégations
- 👥 Recensement de toutes les personnes mentionnées

#### Étape 2: Analyse des patterns de délégation
- 🏢 Types de fonctions qui reçoivent des délégations
- 📈 Directions/services les plus représentés
- 👤 Analyse des noms (répartition hommes/femmes)

#### Étape 3: Mécanismes de substitution
- 🔄 Articles avec mécanismes de suppléance
- 🔗 Relations hiérarchiques identifiées
- ⚠️ Postes clés sans suppléants

#### Étape 4: Détection d'anomalies
- 🚫 Articles sans délégation explicite
- 👥 Délégations multiples (plusieurs personnes)
- 🔍 Fonctions atypiques ou uniques

#### Étape 5: Synthèse et recommandations
- 📊 Calcul de pourcentages et ratios
- 📈 Identification des tendances
- 💡 Recommandations d'amélioration

**Exemple de sortie statistique :**
```
=== ANALYSE STATISTIQUE ===

Étape 1 - Inventaire:
- Nombre d'articles analysés: 15
- Articles avec délégation: 12 (80%)
- Articles sans délégation: 3 (20%)
- Total personnes identifiées: 28

Étape 2 - Patterns de délégation:
- Délégations individuelles: 8 articles (53%)
- Délégations multiples: 4 articles (27%)
- Directions les plus représentées: Finances (40%), RH (25%)

Étape 3 - Mécanismes de substitution:
- Articles avec suppléant: 9/15 (60%)
- Relations hiérarchiques identifiées: 12
- Couverture de suppléance: Bonne (60%)

Étape 4 - Anomalies détectées:
- Articles 7, 12, 18: Absence de délégation (nécessitent vérification)
- Article 11: Délégation multiple sans suppléant désigné

Étape 5 - Recommandations:
- Définir des suppléants pour 6 postes clés
- Clarifier les délégations manquantes
- Standardiser les intitulés de fonctions
```

### 4️⃣ Nœud EXPORT (`export_node`)

**Objectif :** Exporter les résultats dans plusieurs formats consultables

**Formats générés :**

#### 📄 Export Markdown (`.md`)
- **Usage :** Documentation lisible et modifiable
- **Contenu :** Analyse complète + statistiques + métadonnées
- **Avantages :** Facile à consulter, modifier, partager

#### 📕 Export PDF (`.pdf`)
- **Usage :** Rapport professionnel pour présentation
- **Contenu :** Mise en page soignée avec styles
- **Avantages :** Format officiel, impression facile

#### 📋 Export JSON (`.json`)
- **Usage :** Traitement automatique et intégration
- **Contenu :** Données structurées + métriques calculées
- **Avantages :** Parsing facile, intégration système

**Structure des fichiers générés :**
```
2025.5.sante_analyse_20250107_143052.md
2025.5.sante_analyse_20250107_143052.pdf
2025.5.sante_analyse_20250107_143052.json
```

**Exemple de structure JSON :**
```json
{
  "metadata": {
    "source_file": "2025.5.sante.pdf",
    "pages_analyzed": "117 à 131",
    "analysis_date": "2025-01-07T14:30:52",
    "tool": "LangGraph + GPT-4o-mini"
  },
  "detailed_analysis": {
    "articles": [...],
    "raw_result": "Article 25\n[Délégation]..."
  },
  "statistical_analysis": {
    "raw_statistics": "=== ANALYSE STATISTIQUE ===...",
    "computed_metrics": {
      "total_articles": 15,
      "articles_with_delegation": 12,
      "delegation_rate": 80.0,
      "substitution_rate": 60.0
    }
  }
}
```

---

## 🚀 Utilisation

### Méthode 1: Analyse complète automatique
```python
# Tout en une fois avec affichage du graphique
result = run_complete_analysis("2025.5.sante.pdf", 117, 131)
```

### Méthode 2: Étape par étape
```python
# 1. Afficher le workflow
display_workflow_graph()

# 2. Lancer l'analyse
result = process_pdf("2025.5.sante.pdf", 117, 131)

# 3. Afficher les résultats complets
show_final_results(result)
```

### Méthode 3: Fonctions individuelles
```python
# Juste le graphique
show_graph()

# Juste l'analyse sans affichage
result = process_pdf("mon_document.pdf", 1, 50)
```

---

## 📁 Structure des Fichiers de Sortie

### Localisation
Tous les fichiers sont générés dans le **même répertoire que le PDF source**.

### Nomenclature
```
[nom_pdf]_analyse_[timestamp].[extension]
```

### Contenu des exports

#### 📄 Fichier Markdown
```markdown
# Analyse de délégations de pouvoir

## Informations du document
- **Fichier source :** 2025.5.sante.pdf
- **Pages analysées :** 117 à 131

## Résultats de l'analyse détaillée
[Résultats article par article]

## Analyse statistique et insights
[Statistiques et recommandations]
```

#### 📕 Fichier PDF
- Page de garde avec métadonnées
- Section analyse détaillée avec formatage
- Section statistiques avec mise en page soignée
- Styles professionnels (couleurs, typographie)

#### 📋 Fichier JSON
- Structure de données complète
- Métriques calculées automatiquement
- Facilite l'intégration avec d'autres outils

---

## 📊 Métriques Calculées Automatiquement

Le système calcule automatiquement :

- **Nombre total d'articles** analysés
- **Taux de délégation** (% d'articles avec délégation)
- **Taux de suppléance** (% d'articles avec mécanisme de substitution)
- **Répartition par types** de délégation (individuelle vs multiple)
- **Analyse des directions** les plus représentées
- **Détection d'anomalies** et articles problématiques

---

## 🛠️ Personnalisation

### Modifier les pages à analyser
```python
result = process_pdf("document.pdf", start_page=10, end_page=25)
```

### Analyser tout le document
```python
result = process_pdf("document.pdf")  # Analyse tout le PDF
```

### Changer le modèle LLM
```python
llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # Plus rapide
    # model="gpt-4o",       # Plus précis
    temperature=0,
    api_key=api_key
)
```

---

## 🔧 Dépannage

### Erreur "fichier non trouvé"
Le système recherche le PDF dans :
1. Répertoire courant du notebook
2. `BASE_DIR` défini dans le code
3. Chemin absolu spécifié

### Erreur d'affichage graphique
```bash
# Windows
pip install graphviz
# Télécharger depuis https://graphviz.org/download/

# Mac
brew install graphviz

# Linux
sudo apt-get install graphviz
```

### Performances lentes
- Réduire la plage de pages
- Utiliser `gpt-3.5-turbo` au lieu de `gpt-4o-mini`
- Vérifier la taille du prompt

---

## 📈 Cas d'Usage

### 1. Audit de gouvernance
- Identifier les délégations manquantes
- Vérifier la couverture de suppléance
- Analyser la répartition des pouvoirs

### 2. Conformité réglementaire
- Documenter les délégations existantes
- Générer des rapports officiels
- Tracer les responsabilités

### 3. Optimisation organisationnelle
- Identifier les goulots d'étranglement
- Proposer des améliorations
- Standardiser les processus

---

## 🔮 Extensions Possibles

- **Multi-langues :** Support d'autres langues
- **OCR :** Support des PDF scannés
- **Base de données :** Stockage des résultats
- **API REST :** Interface web
- **Comparaison :** Évolution entre versions
- **Alertes :** Détection automatique d'anomalies

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

---

## 📞 Support

Pour toute question ou problème :
- 📧 Email : [votre-email]
- 🐛 Issues : [lien-github-issues]
- 📖 Documentation : [lien-docs]

---

*Développé avec ❤️ en utilisant LangGraph et GPT-4o-mini*
