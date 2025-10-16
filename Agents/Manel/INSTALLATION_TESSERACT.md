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

pip install PyMuPDF pdf2image pytesseract opencv-python Pillow
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

* 🛠️




