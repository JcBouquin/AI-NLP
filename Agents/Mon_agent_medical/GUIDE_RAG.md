# 🎯 Guide : Quand utiliser le RAG vs le LLM direct

## 💡 Principe fondamental

**Le LLM (GPT-4) connaît DÉJÀ :**
- Toutes les connaissances générales du monde
- Médecine générale, anatomie, maladies
- Sciences, histoire, culture, etc.

**Le RAG sert UNIQUEMENT pour :**
- VOS données spécifiques
- Informations privées/internes
- Données changeantes (horaires, prix)
- Procédures locales

---

## ❌ N'utilisez PAS le RAG pour :

### Définitions médicales
```
❌ "Qu'est-ce qu'une IRM ?"
❌ "C'est quoi un scanner ?"
❌ "Symptômes de la grippe ?"
```
→ **Le LLM sait déjà !** Pas besoin de stocker

### Conseils médicaux généraux
```
❌ "Comment prévenir l'hypertension ?"
❌ "Quelle alimentation pour le diabète ?"
❌ "Exercices pour le dos ?"
```
→ **Connaissances universelles** déjà dans le LLM

### Anatomie / Physiologie
```
❌ "Rôle du foie ?"
❌ "Comment fonctionne le cœur ?"
```
→ **Connaissance scientifique générale**

---

## ✅ Utilisez le RAG pour :

### 1. Informations spécifiques à VOTRE cabinet
```
✅ "Quels sont VOS horaires ?"
✅ "Qui sont VOS médecins ?"
✅ "Où êtes-vous situés ?"
```
→ **Le LLM ne peut pas savoir !**

### 2. Politiques et procédures internes
```
✅ "VOTRE politique d'annulation ?"
✅ "Comment prendre RDV chez VOUS ?"
✅ "VOS tarifs ?"
```
→ **Spécifique à votre organisation**

### 3. Informations changeantes
```
✅ "Horaires pendant les fêtes ?"
✅ "Nouveaux services disponibles ?"
✅ "Médecin de garde ce week-end ?"
```
→ **Données évolutives que vous contrôlez**

### 4. Données privées/confidentielles
```
✅ "Protocole interne pour urgences ?"
✅ "Procédure de triage spécifique ?"
```
→ **Informations non publiques**

---

## 🔄 Exemple concret

### Question : "J'ai mal au dos, que faire ?"

**Sans RAG (LLM direct) :**
```
Agent: "Pour un mal de dos, je vous recommande :
- Repos relatif (éviter immobilité totale)
- Application de chaleur ou froid
- Étirements doux
- Consultation si douleur persiste > 48h

Souhaitez-vous prendre rendez-vous avec un de nos médecins ?"
```
✅ **Connaissance générale + guideline pour proposer RDV**

---

### Question : "Quels sont vos horaires ?"

**Avec RAG :**
```
Agent appelle tool 'qna'
→ Cherche dans horaires_cabinet.md
→ Retourne : "Lundi-Vendredi 8h30-19h, Samedi 9h-13h"

Agent: "Notre cabinet est ouvert du lundi au vendredi 
de 8h30 à 19h, et le samedi de 9h à 13h. Nous sommes 
fermés le dimanche et jours fériés."
```
✅ **Information spécifique récupérée du RAG**

---

## 📊 Matrice de décision

| Type d'info | Exemple | LLM direct | RAG |
|-------------|---------|------------|-----|
| **Connaissance médicale générale** | "C'est quoi l'asthme ?" | ✅ | ❌ |
| **Horaires de VOTRE cabinet** | "Vous ouvrez quand ?" | ❌ | ✅ |
| **Symptômes maladie** | "Symptômes COVID ?" | ✅ | ❌ |
| **VOS tarifs** | "Prix consultation ?" | ❌ | ✅ |
| **Anatomie humaine** | "Rôle du pancréas ?" | ✅ | ❌ |
| **VOTRE équipe médicale** | "Qui est Dr. Martin ?" | ❌ | ✅ |
| **Premiers secours** | "Que faire si brûlure ?" | ✅ | ❌ |
| **VOS procédures** | "Comment annuler RDV ?" | ❌ | ✅ |

---

## 💰 Impact coût/performance

### LLM direct :
- ⚡ **Plus rapide** (1 appel LLM)
- 💰 **Moins cher** (pas de RAG)
- ✅ **Tout aussi précis** pour connaissance générale

### RAG :
- 🐌 **Plus lent** (recherche + LLM)
- 💸 **Plus cher** (tokens + embedding)
- ✅ **Indispensable** pour info spécifique
- 🎯 **Traçable** (sources citées)

---

## 🎯 Règle d'or

> **Si Google peut répondre → LLM suffit**
> 
> **Si seul VOUS pouvez répondre → RAG nécessaire**

---

## 🔧 Dans votre agent

Les **guidelines** décident automatiquement :

```python
await agent.create_guideline(
    condition="patient asks about medical procedures or terminology",
    action="use tool 'qna' to search medical documentation",
    tools=["qna"]  # ← Appelle RAG
)
```

Mais pour les **connaissances générales**, l'agent répond directement sans RAG !

