# Serveur MCP d'Analyse de Documents PDF

## 🎯 Vue d'ensemble

Ce serveur MCP (Model Context Protocol) est spécialisé dans l'extraction et l'analyse intelligente de documents PDF, particulièrement optimisé pour les documents juridiques et administratifs contenant des délégations de pouvoir.

### 🔧 Architecture du serveur

**Nom du serveur :** `PDF-Analysis-MCP-Server`  
**Framework :** FastMCP  
**Modèle LLM :** GPT-4o-mini (OpenAI)

## 📋 Outils MCP disponibles

### 1. `extract_and_analyze_pdf`
**Fonction principale** - Extraction et analyse complète de documents PDF

**Paramètres :**
- `pdf_filename` (str) : Nom du fichier PDF (ex: "2025.5.sante.pdf")
- `start_page` (int, optionnel) : Première page à extraire
- `end_page` (int, optionnel) : Dernière page à extraire

**Exemple d'utilisation :**
```python
extract_and_analyze_pdf("2025.5.sante.pdf", 117, 131)
```

**Fonctionnalités :**
- Extraction de texte avec post-traitement intelligent
- Correction automatique des formatages PDF défaillants
- Analyse sophistiquée des délégations de pouvoir
- Sauvegarde automatique des extraits dans `textes_extraits/`

### 2. `test_connection`
**Test de connectivité** - Vérification du bon fonctionnement du serveur

**Retour :** Message de confirmation de connexion

### 3. `pdf_query_tool`
**Recherche dans le contenu** - Outil de requête sur le contenu PDF extrait

**Paramètres :**
- `query` (str) : Requête de recherche dans le contenu PDF

## 🧠 Prompt MCP spécialisé

### `analyze_legal_delegations`
Prompt sophistiqué d'analyse pour identifier les délégations de pouvoir dans les documents juridiques.

**Capacités d'analyse :**
- Identification automatique des articles
- Extraction des noms et fonctions
- Reconnaissance des patterns "En cas d'absence ou d'empêchement de"
- Détection des patterns "Délégation est donnée à"
- Formatage structuré des résultats

**Format de sortie :**
```
Article X
[En cas d'absence ou d'empêchement de] : Nom, fonction : description
[Délégation est donnée à] : Nom, fonction : description
```

## 🗂️ Structure des fichiers

```
MCP_Virginie/
├── README.md                          # Ce fichier
├── traitement_simple_prompt.py        # Serveur MCP avec prompts intégrés
├── PdfTraitement_langgraph.py         # Version avec template LangChain
├── requirements.txt                   # Dépendances de base
├── requirements_langgraph.txt         # Dépendances étendues
├── 2025.5.sante.pdf                  # Document PDF d'exemple
├── mcp_debug.log                     # Logs de débogage
└── textes_extraits/                  # Répertoire des extraits générés
    └── 2025.5.sante_pages_117-131.txt
```

## 🚀 Installation et configuration

### Prérequis
- Python 3.8+
- Clé API OpenAI (variable d'environnement `OPENAI_API_KEY`)

### Installation des dépendances

**Version de base :**
```bash
pip install -r requirements.txt
```

**Version avec LangGraph :**
```bash
pip install -r requirements_langgraph.txt
```

### Configuration de la clé API

**Méthode recommandée (variable d'environnement) :**
```bash
set OPENAI_API_KEY=votre_clé_api_ici
```

### Démarrage du serveur

**Mode serveur MCP :**
```bash
python traitement_simple_prompt.py
```

**Mode test local :**
```bash
python traitement_simple_prompt.py --test
```

## 🔍 Fonctionnalités techniques

### Traitement PDF avancé
- **Post-traitement intelligent** : Correction automatique des artifacts PDF
- **Formatage adaptatif** : Restructuration pour une meilleure lisibilité
- **Gestion des pages** : Extraction sélective par plage de pages
- **Encodage robuste** : Support UTF-8 pour les caractères spéciaux

### Analyse linguistique sophistiquée
- **Chain of Thought** : Raisonnement étape par étape
- **Pattern matching** : Reconnaissance de structures juridiques
- **Extraction d'entités** : Identification automatique des noms et fonctions
- **Gestion des cas limites** : Traitement des informations manquantes

### Ressources MCP
- **system://pdf-environment** : Informations sur l'environnement et les chemins

## 📊 Exemple de résultat d'analyse

```
=== EXTRACTION ET ANALYSE TERMINÉES ===

PDF source: C:\Users\kosmo\pycode\MCP_Virginie\2025.5.sante.pdf
Pages analysées: 117 à 131
Fichier extrait: C:\Users\kosmo\pycode\MCP_Virginie\textes_extraits\2025.5.sante_pages_117-131.txt

=== RÉSULTATS DE L'ANALYSE ===

Article 1
[En cas d'absence ou d'empêchement de] : Mme Caroline SEMAILLE, fonction : directrice générale
[Délégation est donnée à] : Mme Marie-Anne JACQUET, fonction : directrice générale adjointe

Article 2
[En cas d'absence ou d'empêchement de] : Mme Caroline SEMAILLE, fonction : directrice générale et Mme Marie-Anne JACQUET, fonction : directrice générale adjointe
[Délégation est donnée à] : M. Yann LE STRAT, fonction : directeur scientifique
```

## 🛠️ Développement et débogage

### Logs de débogage
Les logs sont automatiquement générés dans `mcp_debug.log` pour faciliter le diagnostic des problèmes.

### Mode test
Le mode `--test` permet de valider le fonctionnement sans démarrer le serveur MCP complet.

### Structure modulaire
- **Extraction PDF** : Module autonome pour le traitement des documents
- **Analyse LLM** : Composant d'analyse avec prompts spécialisés
- **Serveur MCP** : Interface standardisée pour l'intégration

## 🔒 Sécurité et bonnes pratiques

- ⚠️ **Clés API** : Utilisez toujours des variables d'environnement en production
- 📁 **Chemins** : Validation automatique des chemins de fichiers
- 🛡️ **Erreurs** : Gestion robuste des exceptions et erreurs de traitement
- 📝 **Logs** : Traçabilité complète des opérations

## 🎯 Cas d'usage

### Documents juridiques
- Analyse de délégations de pouvoir
- Extraction d'organigrammes administratifs
- Identification de responsabilités hiérarchiques

### Documents administratifs
- Traitement de bulletins officiels
- Analyse de structures organisationnelles
- Extraction d'informations réglementaires

## 📈 Performances

### Optimisations
- **Traitement par lot** : Extraction de plages de pages
- **Post-traitement intelligent** : Amélioration automatique du formatage
- **Gestion mémoire** : Traitement efficace des gros documents
- **Cache intelligent** : Réutilisation des extraits existants

### Limites
- Documents PDF avec OCR non optimisé
- Formats PDF très complexes ou endommagés
- Très gros documents (>1000 pages) peuvent nécessiter un traitement séquentiel

## 🤝 Contribution

Pour contribuer au développement :
1. Testez avec le mode `--test`
2. Vérifiez les logs dans `mcp_debug.log`
3. Respectez la structure modulaire existante
4. Documentez les nouvelles fonctionnalités

## 📞 Support

En cas de problème :
1. Vérifiez la configuration de la clé API OpenAI
2. Consultez les logs de débogage
3. Testez avec le mode `--test`
4. Vérifiez la présence du fichier PDF cible

---

Prompt uilisé 

As-tu accès au serveur MCP traitement_simple_prompt.py ? Si oui, peux-tu me lister les outils MCP que tu peux voir ? Cite-les-moi juste.
Maintenant, peux-tu exécuter l'outil extract_and_analyze_pdf pour les pages 117 à 131 du PDF que tu trouveras ici : C:\Users\kosmo\pycode\MCP_Virginie ? Tu écriras les résultats dans un fichier MD en respectant le format du prompt.
Peux-tu ajouter au fichier MD créé toutes les analyses et statistiques que tu pourrais trouver ?

**Version :** 1.0  
**Dernière mise à jour :** Juin 2025  
**Auteur :** Serveur MCP PDF-Analysis
