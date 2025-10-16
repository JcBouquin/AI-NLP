"""
Script d'extraction pour PDF contenant des organigrammes/arborescences
Utilise OCR (Tesseract) pour extraire le texte des structures visuelles complexes
"""

import os
import sys
from pathlib import Path
from datetime import datetime

try:
    import fitz  # PyMuPDF
    print("[OK] PyMuPDF charge")
except ImportError:
    print("[INSTALL] Installation de PyMuPDF...")
    os.system("pip install PyMuPDF")
    import fitz

try:
    from pdf2image import convert_from_path
    print("[OK] pdf2image charge")
except ImportError:
    print("[INSTALL] Installation de pdf2image...")
    os.system("pip install pdf2image")
    from pdf2image import convert_from_path

# Configuration automatique du chemin Poppler (Windows)
poppler_paths = [
    r"C:\Program Files\poppler\Library\bin",
    r"C:\Program Files\poppler-25.07.0\Library\bin",
    r"C:\Program Files\Release-25.07.0-0\poppler-25.07.0\Library\bin",
    r"C:\Users\jcbouquin\Downloads\Release-25.07.0-0\poppler-25.07.0\Library\bin",  # Temporaire
    r"C:\Program Files\poppler-24.08.0\Library\bin",
    r"C:\Program Files\poppler-24.02.0\Library\bin",
    r"C:\poppler\Library\bin",
    r"C:\Users\jcbouquin\AppData\Local\Programs\poppler\Library\bin",
]

poppler_path = None
for path in poppler_paths:
    if os.path.exists(path):
        poppler_path = path
        print(f"[OK] Poppler trouve : {path}")
        break

if not poppler_path:
    print("[WARNING] Poppler non trouve aux emplacements standards")
    print("[INFO] Apres installation, le script detectera automatiquement Poppler")

try:
    from PIL import Image, ImageEnhance
    print("[OK] Pillow charge")
except ImportError:
    print("[INSTALL] Installation de Pillow...")
    os.system("pip install Pillow")
    from PIL import Image, ImageEnhance

try:
    import pytesseract
    print("[OK] pytesseract charge")
except ImportError:
    print("[INSTALL] Installation de pytesseract...")
    os.system("pip install pytesseract")
    import pytesseract

# Configuration automatique du chemin Tesseract (Windows)
tesseract_paths = [
    r"C:\Users\jcbouquin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",  # Emplacement trouve
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Tesseract-OCR\tesseract.exe"
]

tesseract_found = False
for path in tesseract_paths:
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        tesseract_found = True
        print(f"[OK] Tesseract trouve : {path}")
        break

if not tesseract_found:
    print("[WARNING] Tesseract-OCR non trouve aux emplacements standards")
    print("[INFO] Si Tesseract est installe ailleurs, configurez :")
    print("  pytesseract.pytesseract.tesseract_cmd = r'CHEMIN_VERS_TESSERACT'")

try:
    import cv2
    import numpy as np
    print("[OK] OpenCV charge")
except ImportError:
    print("[INSTALL] Installation d'OpenCV...")
    os.system("pip install opencv-python")
    import cv2
    import numpy as np


def preprocess_image_for_ocr(image):
    """
    Pretraitement de l'image pour ameliorer la qualite de l'OCR
    """
    # Convertir PIL Image en array numpy pour OpenCV
    img_array = np.array(image)
    
    # Convertir en niveaux de gris
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    # Augmenter le contraste
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Debruitage
    denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
    
    # Binarisation adaptative
    binary = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    # Reconvertir en PIL Image
    return Image.fromarray(binary)


def detect_text_boxes(image):
    """
    Detecte les zones de texte (boites) dans l'organigramme
    """
    img_array = np.array(image)
    
    # Convertir en niveaux de gris
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    # Binarisation
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Detecter les contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtrer les contours (garder seulement les boites significatives)
    boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        # Garder seulement les grandes zones (boites de l'organigramme)
        if area > 5000 and w > 100 and h > 50:
            boxes.append((x, y, w, h))
    
    # Trier les boites de haut en bas, puis de gauche a droite
    boxes = sorted(boxes, key=lambda b: (b[1], b[0]))
    
    return boxes


def extract_text_from_box(image, box):
    """
    Extrait le texte d'une zone specifique de l'image
    """
    x, y, w, h = box
    # Crop l'image a la zone de la boite
    cropped = image.crop((x, y, x + w, y + h))
    
    # Pretraiter l'image
    preprocessed = preprocess_image_for_ocr(cropped)
    
    # OCR avec configuration optimisee (francais si disponible, sinon anglais)
    try:
        custom_config = r'--oem 3 --psm 6 -l fra'
        text = pytesseract.image_to_string(preprocessed, config=custom_config)
    except Exception:
        # Fallback vers l'anglais si le francais n'est pas installe
        custom_config = r'--oem 3 --psm 6 -l eng'
        text = pytesseract.image_to_string(preprocessed, config=custom_config)
    
    return text.strip()


def extract_organigramme_simple(image):
    """
    Extraction simple : OCR sur toute l'image
    """
    # Pretraiter l'image
    preprocessed = preprocess_image_for_ocr(image)
    
    # OCR avec configuration optimisee (francais si disponible, sinon anglais)
    try:
        custom_config = r'--oem 3 --psm 3 -l fra'
        text = pytesseract.image_to_string(preprocessed, config=custom_config)
    except Exception:
        # Fallback vers l'anglais si le francais n'est pas installe
        custom_config = r'--oem 3 --psm 3 -l eng'
        text = pytesseract.image_to_string(preprocessed, config=custom_config)
    
    return text.strip()


def extract_organigramme_structure(image):
    """
    Extraction structuree : detecte les boites et extrait le texte de chacune
    """
    boxes = detect_text_boxes(image)
    
    content = []
    content.append(f"[INFO] {len(boxes)} zones detectees\n")
    
    for i, box in enumerate(boxes, 1):
        text = extract_text_from_box(image, box)
        if text:
            content.append(f"\n### Zone {i} (x={box[0]}, y={box[1]})\n")
            content.append(text)
            content.append("\n---\n")
    
    return "\n".join(content)


def extract_pdf_organigramme(pdf_path, mode="simple"):
    """
    Extrait le contenu d'un PDF d'organigramme
    
    Args:
        pdf_path: Chemin vers le fichier PDF
        mode: "simple" pour OCR global, "structure" pour detection de zones
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        print(f"[ERROR] Fichier introuvable : {pdf_path}")
        return
    
    print(f"\n[PDF] Extraction du PDF : {pdf_path.name}")
    print(f"[MODE] Mode d'extraction : {mode}")
    
    # Preparer les chemins de sortie
    base_name = pdf_path.stem
    output_file = pdf_path.parent / f"{base_name}_extracted_arbo.md"
    images_dir = pdf_path.parent / f"{base_name}_arbo_images"
    images_dir.mkdir(exist_ok=True)
    
    print(f"[IMAGES] Dossier images : {images_dir.name}")
    print(f"[OUTPUT] Fichier sortie : {output_file.name}")
    
    # Convertir le PDF en images
    print(f"\n[CONVERSION] Conversion du PDF en images...")
    try:
        # Utiliser poppler_path si trouve, sinon essayer sans (si dans PATH)
        if poppler_path:
            images = convert_from_path(str(pdf_path), dpi=300, poppler_path=poppler_path)
        else:
            images = convert_from_path(str(pdf_path), dpi=300)
        print(f"[OK] {len(images)} page(s) convertie(s)")
    except Exception as e:
        print(f"[ERROR] Erreur de conversion : {e}")
        print("\n" + "=" * 60)
        print("[ERROR] POPPLER N'EST PAS INSTALLE !")
        print("=" * 60)
        print("\n[ETAPE 1] Telechargez Poppler :")
        print("  https://github.com/oschwartz10612/poppler-windows/releases/")
        print("\n[ETAPE 2] Extraire l'archive (.7z ou .zip)")
        print("\n[ETAPE 3] Copier le dossier dans :")
        print("  C:\\Program Files\\poppler\\")
        print("  OU")
        print("  C:\\poppler\\")
        print("\n[ETAPE 4] Relancer ce script")
        print("=" * 60)
        return
    
    # Preparer le contenu Markdown
    content_lines = []
    content_lines.append(f"# Extraction d'organigramme : {base_name}")
    content_lines.append(f"Source : `{pdf_path.name}`")
    content_lines.append(f"Date d'extraction : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    content_lines.append(f"Mode : {mode}")
    content_lines.append("---\n")
    content_lines.append(f"**Nombre de pages :** {len(images)}\n")
    
    # Traiter chaque page
    print(f"\n[EXTRACTION] Extraction du texte par OCR...")
    
    for page_num, image in enumerate(images, 1):
        print(f"  [PAGE] Page {page_num}/{len(images)}")
        
        content_lines.append(f"\n## Page {page_num}\n")
        
        # Sauvegarder l'image originale
        image_path = images_dir / f"page_{page_num}_original.png"
        image.save(image_path, "PNG")
        content_lines.append(f"![Organigramme Page {page_num}](./{images_dir.name}/page_{page_num}_original.png)\n")
        
        # Extraire le texte selon le mode choisi
        try:
            if mode == "structure":
                text = extract_organigramme_structure(image)
            else:  # mode == "simple"
                text = extract_organigramme_simple(image)
            
            if text:
                content_lines.append("### Texte extrait\n")
                content_lines.append("```")
                content_lines.append(text)
                content_lines.append("```\n")
            else:
                content_lines.append("*Aucun texte detecte*\n")
        
        except Exception as e:
            content_lines.append(f"*Erreur lors de l'extraction : {e}*\n")
            print(f"  [ERROR] Erreur OCR page {page_num} : {e}")
    
    # Sauvegarder le fichier Markdown
    print(f"\n[SAVE] Sauvegarde du fichier Markdown...")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(content_lines))
    
    print("\n" + "=" * 60)
    print("[SUCCESS] EXTRACTION TERMINEE !")
    print("=" * 60)
    print(f"[PAGES] Pages traitees : {len(images)}")
    print(f"[FILE] Fichier genere : {output_file.name}")
    print(f"[FOLDER] Images dans : {images_dir.name}")
    print("=" * 60)
    print(f"\n[DONE] Vous pouvez maintenant lire le fichier : {output_file.name}")


if __name__ == "__main__":
    # ============================================================
    # CONFIGURATION
    # ============================================================
    
    # Obtenir le repertoire du script
    script_dir = Path(__file__).parent
    
    # Chemin vers le fichier PDF d'organigramme (dans le meme dossier que le script)
    pdf_file = script_dir / "ORGA GENERAL Photos + adresses mail Octobre 2025.pdf"
    
    # Mode d'extraction :
    # - "simple" : OCR global sur toute la page (plus rapide, moins structure)
    # - "structure" : Detection des zones + OCR par zone (plus lent, plus structure)
    extraction_mode = "simple"
    
    # ============================================================
    
    # Verification de Tesseract
    print("\n[CHECK] Verification de Tesseract-OCR...")
    try:
        version = pytesseract.get_tesseract_version()
        print(f"[OK] Tesseract-OCR detecte : Version {version}")
    except Exception as e:
        print("\n" + "=" * 60)
        print("[ERROR] TESSERACT-OCR N'EST PAS INSTALLE !")
        print("=" * 60)
        print("\n[ETAPE 1] Telechargez Tesseract-OCR :")
        print("  https://github.com/UB-Mannheim/tesseract/wiki")
        print("\n[ETAPE 2] Installez-le avec ces options :")
        print("  - Cocher 'French (fra)' dans les langues")
        print("  - Installer dans : C:\\Program Files\\Tesseract-OCR\\")
        print("\n[ETAPE 3] Relancez ce script apres installation")
        print("=" * 60)
        print(f"\n[DEBUG] Erreur : {e}")
        sys.exit(1)
    
    # Lancer l'extraction
    print("\n[START] Lancement de l'extraction...\n")
    extract_pdf_organigramme(pdf_file, mode=extraction_mode)

