# 📥 Guide d'Installation de Tesseract-OCR

## 🎯 Vous Êtes Ici

Votre script `extract_pdf_content_arbo.py` nécessite **Tesseract-OCR** pour fonctionner.
pip install PyMuPDF pdf2image pytesseract opencv-python Pillow
```
Statut actuel :
✅ pytesseract (Python) : Installé
✅ OpenCV : Installé
✅ PyMuPDF : Installé
✅ pdf2image : Installé
❌ Tesseract-OCR (Moteur) : NON INSTALLÉ ← À installer
```

---

## 📦 Étapes d'Installation (Windows)

### **Étape 1 : Télécharger Tesseract-OCR**

1. **Ouvrir le lien** :
   ```
   https://github.com/UB-Mannheim/tesseract/wiki
   ```

2. **Télécharger la dernière version 64-bit** :
   - Chercher : `tesseract-ocr-w64-setup-x.x.x.exe`
   - Exemple : `tesseract-ocr-w64-setup-5.4.0.20240606.exe`
   - Cliquer pour télécharger (~60 MB)

---

### **Étape 2 : Installation**

1. **Lancer l'installeur** téléchargé

2. **Suivre l'assistant d'installation** :

   #### Écran 1 : Bienvenue
   - Cliquer sur **"Next"**

   #### Écran 2 : Licence
   - Accepter la licence → **"I Agree"**

   #### Écran 3 : Composants **[IMPORTANT]**
   ```
   ✅ Cocher "Tesseract"
   ✅ Cocher "Additional language data (download)"
       ↳ Dans la liste, cocher "French (fra)" ← IMPORTANT !
   ```

   #### Écran 4 : Destination
   ```
   📁 Installer dans : C:\Program Files\Tesseract-OCR\
   ```
   (Laisser le chemin par défaut)

   #### Écran 5 : Installation
   - Cliquer **"Install"**
   - Attendre 30-60 secondes

   #### Écran 6 : Fin
   - Cliquer **"Finish"**

---

### **Étape 3 : Vérification**

**Option A : Via Terminal**
```powershell
tesseract --version
```

Si ça affiche la version → ✅ Installation réussie !

Si erreur "commande non reconnue" → Continuer avec Option B

---

**Option B : Via le Script Python**
```powershell
py "C:\Users\jcbouquin\AI\GenAI\Prompt Engineering\extract_pdf_content_arbo.py"
```

Si ça affiche :
```
[OK] Tesseract trouve : C:\Program Files\Tesseract-OCR\tesseract.exe
[OK] Tesseract-OCR detecte : Version 5.x.x
```
→ ✅ **Installation réussie !**

Si ça affiche encore l'erreur → Continuer avec le dépannage ci-dessous

---

## 🔧 Dépannage

### **Problème 1 : Tesseract non détecté après installation**

**Cause :** Le script ne trouve pas Tesseract

**Solution 1 :** Vérifier que Tesseract est bien installé
```powershell
dir "C:\Program Files\Tesseract-OCR\"
```

Si vous voyez `tesseract.exe` → Tesseract est installé, mais le script ne le trouve pas.

**Solution 2 :** Ajouter le chemin manuellement dans le script

Ouvrir `extract_pdf_content_arbo.py` et modifier ligne ~44-48 :

```python
# Configuration automatique du chemin Tesseract (Windows)
tesseract_paths = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Tesseract-OCR\tesseract.exe",
    r"VOTRE_CHEMIN_ICI\tesseract.exe"  # ← Ajouter votre chemin si différent
]
```

---

### **Problème 2 : Langue française non installée**

**Symptôme :** OCR fonctionne mais reconnaît mal les textes français

**Solution :** Réinstaller Tesseract et cocher **"French (fra)"**

Ou télécharger manuellement le fichier de langue :
1. Télécharger `fra.traineddata` : https://github.com/tesseract-ocr/tessdata/raw/main/fra.traineddata
2. Copier dans : `C:\Program Files\Tesseract-OCR\tessdata\`

---

### **Problème 3 : "tesseract is not installed or it's not in your PATH"**

**Solution :** Ajouter Tesseract au PATH Windows

1. Ouvrir **Panneau de configuration** → **Système** → **Paramètres système avancés**
2. Cliquer **"Variables d'environnement"**
3. Dans **"Variables système"**, sélectionner **"Path"** → **"Modifier"**
4. Cliquer **"Nouveau"** et ajouter :
   ```
   C:\Program Files\Tesseract-OCR
   ```
5. **"OK"** → **Redémarrer le terminal**

---

## ⚡ Alternative Recommandée (Sans OCR)

### **Vous n'avez PAS BESOIN d'OCR pour votre PDF !**

Votre PDF `ORGA GENERAL Photos + adresses mail Octobre 2025.pdf` contient du **texte natif sélectionnable**.

**Solution 10x plus rapide** (pas d'installation requise) :

```powershell
py "C:\Users\jcbouquin\AI\GenAI\Prompt Engineering\extract_pdf_content_arbo2.py"
```

**Résultats :**
- ✅ 3 secondes (vs 20-30 secondes avec OCR)
- ✅ 55 cellules extraites
- ✅ 9 emails détectés
- ✅ Structure hiérarchique

---

## 📊 Comparaison

| Critère | extract_pdf_content_arbo.py (OCR) | extract_pdf_content_arbo2.py (Natif) |
|---------|-----------------------------------|---------------------------------------|
| **Installation** | Tesseract requis (~60 MB) | Rien de plus |
| **Temps** | 20-30 secondes/page | 3 secondes total |
| **Qualité** | 95% (erreurs OCR possibles) | 100% (texte natif) |
| **Utilité pour votre PDF** | ❌ Inutile (PDF natif) | ✅ Parfait |

---

## 🎯 Recommandation

```
┌──────────────────────────────────────────────────────────┐
│  POUR VOTRE CAS :                                         │
│                                                           │
│  ✅ Utilisez extract_pdf_content_arbo2.py                 │
│     (Pas d'installation, 10x plus rapide)                │
│                                                           │
│  ❌ N'installez Tesseract-OCR QUE SI :                    │
│     - Vous avez des PDFs scannés (images)                │
│     - Le texte n'est pas sélectionnable                  │
└──────────────────────────────────────────────────────────┘
```

---

## 📞 Support

Si vous avez des questions :
1. Vérifier que le PDF n'est pas déjà "natif" (texte sélectionnable)
2. Essayer `extract_pdf_content_arbo2.py` d'abord
3. Installer Tesseract seulement si vraiment nécessaire

---

**Créé pour faciliter l'installation de Tesseract-OCR** 🛠️


