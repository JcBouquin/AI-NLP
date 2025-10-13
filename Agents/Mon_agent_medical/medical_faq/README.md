# 📚 FAQ du Cabinet Médical

## 🎯 Pourquoi ces FAQ et pas des définitions médicales générales ?

**Distinction importante :**

### ❌ PAS besoin de RAG pour :
- "Qu'est-ce qu'une IRM ?" → Le LLM sait déjà
- "C'est quoi un scanner ?" → Connaissance générale
- "Définition d'une prise de sang" → Inutile de stocker

### ✅ RAG UTILE pour :
- "Quels sont VOS horaires ?" → Spécifique à votre cabinet
- "Qui sont VOS médecins ?" → Données privées
- "Quelle est VOTRE politique d'annulation ?" → Règles internes
- "VOTRE adresse ?" → Information locale

---

## 📁 Contenu des FAQ

### 1. `horaires_cabinet.md`
- Heures d'ouverture
- Jours fériés
- Urgences hors horaires

### 2. `medecins_equipe.md`
- Liste des praticiens
- Spécialités
- Disponibilités

### 3. `politique_annulation.md`
- Délais d'annulation
- Frais éventuels
- Modalités

### 4. `tarifs_remboursements.md`
- Prix des consultations
- Taux de remboursement
- Moyens de paiement

### 5. `contact_acces.md`
- Adresse du cabinet
- Téléphone, email
- Accès (métro, parking)
- Accessibilité PMR

---

## 🔄 Comment charger ces FAQ

```bash
# Windows
load_medical_faq.bat

# Linux/Mac
bash load_medical_faq.sh
```

---

## ✏️ Comment personnaliser

1. **Modifier les fichiers .md** avec VOS informations réelles
2. **Relancer le script** de chargement
3. **Ou ajouter manuellement** :
   ```bash
   parlant-qna add -q "Question ?" -a "Réponse spécifique"
   ```

---

## 💡 Bonnes pratiques

### ✅ À stocker dans le RAG :
- Informations changeantes (horaires, tarifs)
- Données privées (équipe, procédures internes)
- Informations locales (adresse, accès)
- Politiques spécifiques (annulation, remboursement)

### ❌ À NE PAS stocker (LLM connaît déjà) :
- Définitions médicales générales
- Anatomie humaine
- Maladies courantes
- Conseils médicaux généraux

**Le RAG sert à compléter les connaissances du LLM avec VOS données spécifiques !**

