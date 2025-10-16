# 📥 Guide d'Installation de Poppler

## 🎯 Pourquoi Poppler ?

Poppler est nécessaire pour **convertir les PDFs en images** avant l'analyse OCR avec Tesseract.

```
Flux de travail OCR :
PDF → [Poppler] → Image → [Tesseract] → Texte
```

---

## 📦 Installation de Poppler (Windows)

### **Étape 1 : Télécharger Poppler**

1. **Ouvrir le lien** :
   ```
   https://github.com/oschwartz10612/poppler-windows/releases/
   ```

2. **Télécharger la dernière version** :
   - Chercher la dernière **Release** (ex: `Release-24.08.0-0`)
   - Télécharger : **`poppler-24.08.0_x64.7z`** (ou `.zip`)
   - Taille : ~25 MB

---

### **Étape 2 : Extraire l'Archive**

1. **Localiser le fichier téléchargé** (dossier `Téléchargements`)

2. **Extraire l'archive** :
   - Si `.7z` : Utiliser **7-Zip** (télécharger depuis https://www.7-zip.org/ si nécessaire)
   - Si `.zip` : Clic droit → **Extraire tout**

3. **Vous obtiendrez un dossier** :
   ```
   poppler-24.08.0/
     ├── Library/
     │   └── bin/
     │       ├── pdfinfo.exe
     │       ├── pdftoppm.exe
     │       ├── pdfimages.exe
     │       └── ... (environ 50 fichiers .exe et .dll)
     └── ...
   ```

---

### **Étape 3 : Installer Poppler**

**Copier le dossier** `poppler-24.08.0` dans un emplacement permanent :

#### **Option A : Installation Système (Recommandé)**
```
Copier vers : C:\Program Files\poppler\
```
- Renommer `poppler-24.08.0` → `poppler`
- Chemin final : `C:\Program Files\poppler\Library\bin\`

#### **Option B : Installation Utilisateur**
```
Copier vers : C:\poppler\
```
- Chemin final : `C:\poppler\Library\bin\`

---

### **Étape 4 : Vérification**

#### **Test 1 : Vérifier que les fichiers sont bien là**

Ouvrir l'Explorateur Windows et naviguer vers :
```
C:\Program Files\poppler\Library\bin\
```

Vous devez voir environ 50 fichiers `.exe` et `.dll`, dont :
- ✅ `pdfinfo.exe`
- ✅ `pdftoppm.exe`
- ✅ `pdfimages.exe`

---

#### **Test 2 : Lancer le Script Python**

```powershell
py "C:\Users\jcbouquin\AI\GenAI\Prompt Engineering\extract_pdf_content_arbo.py"
```

**Si Poppler est bien installé**, vous verrez :
```
[OK] Poppler trouve : C:\Program Files\poppler\Library\bin
[CONVERSION] Conversion du PDF en images...
[OK] 1 page(s) convertie(s)
```

 ** 📦


