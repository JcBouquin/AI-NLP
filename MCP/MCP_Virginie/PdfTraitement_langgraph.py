from mcp.server.fastmcp import FastMCP
import os
import sys
import pdfplumber
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Define the path to your project
PATH = os.path.dirname(os.path.abspath(__file__)) + "/"

# Chemin de base pour les PDFs (à ajuster selon votre environnement)
BASE_DIR = os.path.abspath(r"C:\Users\kosmo\pycode\MCP_Virginie")

# Create an MCP server
mcp = FastMCP("PDF-Analysis-MCP-Server")

# Initialiser le LLM avec gestion sécurisée de la clé API
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    # ⚠️ À remplacer par une variable d'environnement en production
    print("⚠️ ATTENTION: Utilisez une variable d'environnement pour la clé API en production")
    api_key = "sk-proj-0xUZ6aBpi14QWLtzQC2nF0B2gQTojxukve0byW1qgx05hmq2wSTJs2mjq9C0Iyh8mq8WeoK0yCT y9HhFfHS_cUMhXQMX6_U0pycw_XiZUUtZ4V6Gc5xEwhMZOsYA6xKN4HruNnPRcA"

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=api_key
)

# ===== PARTIE 1: FONCTIONS D'EXTRACTION PDF =====

def post_process_text(text):
    """
    Fonction pour nettoyer et reformater le texte extrait.
    Corrige les problèmes courants comme les articles mal formatés.
    """
    # Corriger "A\nrticle" en "Article"
    text = re.sub(r'A\s*\n\s*rticle\s+(\d+)', r'Article \1', text)
    
    # Corriger "E\nn cas" en "En cas"
    text = re.sub(r'E\s*\n\s*n cas', r'En cas', text)
    
    # Corriger les sauts de lignes intempestifs dans le texte courant
    text = re.sub(r'(\w)\s*\n\s*(\w)', lambda m: f"{m.group(1)} {m.group(2)}" if not (m.group(2).lower() == 'les' or m.group(1) == '-') else f"{m.group(1)}\n{m.group(2)}", text)
    
    return text

def format_articles(text):
    """
    Améliore le formatage des articles pour respecter la mise en page désirée
    """
    # Mettre "Article XX" sur une ligne séparée et ajouter un saut de ligne après
    text = re.sub(r'\b(Article\s+\d+)\s+', r'\n\1\n\n', text)
    
    # Assurer que "Direction de" commence toujours sur une nouvelle ligne
    text = re.sub(r'([^\n])(Direction de)', r'\1\n\n\2', text)
    
    # Assurer que chaque élément commençant par un tiret est sur une nouvelle ligne
    text = re.sub(r'([^\n])\s*(-\s+)', r'\1\n\2', text)
    
    # Assurer que "dans la limite de ses attributions et fonctions :" est sur sa propre ligne
    text = re.sub(r'(dans la limite de ses attributions et fonctions\s*:)', r'\n\1\n', text)
    
    # S'assurer que le texte après un tiret soit bien séparé de la Direction qui suit
    text = re.sub(r'(afférents\.)\s*(Direction)', r'\1\n\n\2', text)
    text = re.sub(r'(comptes\.)\s*(Direction)', r'\1\n\n\2', text)
    
    # S'assurer que "Bulletin officiel" est au début d'une ligne
    text = re.sub(r'([^\n])(Bulletin officiel)', r'\1\n\2', text)
    
    # Nettoyer les lignes vides multiples (pas plus de 2 consécutives)
    text = re.sub(r'\n{3,}', r'\n\n', text)
    
    return text

def extract_pdf_text(pdf_path: str, output_dir: str = "extracted_text", start_page: int = None, end_page: int = None):
    """
    Extract text from specified pages of a PDF file and save it to a single file.
    """
    if not os.path.exists(pdf_path):
        return f"Erreur: Fichier non trouvé: {pdf_path}"
    
    # Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    
    # Déterminer la plage de pages
    if start_page and end_page:
        page_info = f" (pages {start_page}-{end_page})"
    elif start_page:
        page_info = f" (à partir de la page {start_page})"
    else:
        page_info = " (toutes les pages)"
        start_page = 1
        
    if not end_page:
        end_page = float('inf')
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            
            # Ajuster la plage de pages si nécessaire
            start_idx = max(0, start_page - 1)
            end_idx = min(total_pages, end_page)
            
            # Préparer un seul fichier pour toutes les pages
            pdf_name = os.path.basename(pdf_path).replace(".pdf", "")
            output_filename = f"{pdf_name}_pages_{start_page}-{end_idx}.txt"
            output_path = os.path.join(output_dir, output_filename)
            
            # Extraire et écrire le texte de toutes les pages dans un seul fichier
            with open(output_path, 'w', encoding='utf-8') as output_file:
                for i in range(start_idx, end_idx):
                    page = pdf.pages[i]
                    page_text = page.extract_text()
                    
                    if page_text:
                        # Post-traitement pour corriger les problèmes de formatage
                        page_text = post_process_text(page_text)
                        
                        # Amélioration du formatage des articles
                        page_text = format_articles(page_text)
                        
                        # Écrire un séparateur de page clair
                        output_file.write(f"\n\n{'='*20} PAGE {i+1} {'='*20}\n\n")
                        output_file.write(page_text)
                        output_file.write("\n")
            
            return output_path
            
    except Exception as e:
        return f"Erreur lors de l'extraction du texte: {str(e)}"

# ===== PARTIE 2: ANALYSE AVEC VOTRE PROMPT SOPHISTIQUÉ =====

# Template de prompt avec votre logique d'analyse sophistiquée complète
analysis_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
Vous êtes un expert en analyse de texte juridique et administratif.
Votre spécialité est d'identifier les noms de personnes et leurs rôles
dans des documents officiels, particulièrement les délégations de pouvoir.

Analyse le texte et extrais les informations demandées, en suivant les étapes détaillées ci-dessous.

Chain of Thought pour l'analyse

Instructions générales :
Cette méthode d'analyse doit être appliquée sur l'ensemble du document administratif en procédant article par article. Pour chaque article du document :
1. Isoler le texte de l'article concerné
2. Appliquer la méthode d'analyse décrite dans les exemples ci-dessous
3. Rechercher systématiquement les termes spécifiques et les noms associés
4. Si les termes recherchés n'existent pas dans l'article, indiquer "Non mentionné" pour la catégorie correspondante
5. Compiler les résultats en respectant le format suivant pour chaque article :

Article [Numéro]
[En cas d'absence ou d'empêchement de] : [Nom de la personne ou "Non mentionné"]
[Délégation est donnée à] : [Nom de la personne ou "Non mentionné"]

Exemple 1:

1. Lecture du document :
   Je commence par lire attentivement l'extrait suivant pour en comprendre le contexte et la structure.

   "Délégation est donnée à M. Thomas DUPONT, responsable de l'Unité budget et contrôle interne au sein de la

   Direction des achats et des finances, à l'effet de signer, au nom de la directrice générale de Santé publique France,
   dans la limite de ses attributions et fonctions :

   - l'ensemble des bons de commande d'un montant hors taxe inférieur à 35 000 € ;
   - en cas d'absence ou d'empêchement de la directrice des achats et des finances,
   Mme Sophie MARTIN (épouse DURAND), l'ensemble des bons de commande ;
   - les certifications de service fait sans limitation de montant."

2. Recherche du terme "délégation est donnée" :
   Je cherche si cette expression apparaît dans le texte et j'examine ce qui suit.

   Trouvé : "Délégation est donnée à M. Thomas DUPONT"

   J'identifie donc le nom qui suit cette expression : M. Thomas DUPONT

   Si cette expression n'était pas présente, j'indiquerais "Non mentionné".

   Si cette expression est présente :

   j'identifie la fonction devant le nom de M. Thomas DUPONT : responsable de l'Unité budget et contrôle interne au sein de la Direction des achats et des finances

   la fonction est :  responsable de l'Unité budget et contrôle interne au sein de la Direction des achats et des finances

3. Recherche du terme "en cas d'absence ou d'empêchement" :
   Je cherche si cette expression apparaît dans le texte et j'examine le contexte.

   Trouvé : "en cas d'absence ou d'empêchement de la directrice des achats et des finances, Mme Sophie MARTIN (épouse DURAND)"

   Dans ce contexte, je comprends que Mme Sophie MARTIN (épouse DURAND) est mentionnée comme la directrice des achats et des finances.

   Si cette expression n'était pas présente, j'indiquerais "Non mentionné".

   Si cette expression est présente j'identife également la fonction devant le nom de Mme Sophie MARTIN (épouse DURAND) : directrice des achats et des finances

   la fonction est : directrice des achats et des finances

4. Format de sortie :
   Je structure les informations collectées selon le format demandé.

   [En cas d'absence ou d'empêchement de] : Mme Sophie MARTIN (épouse DURAND) , fonction : directrice des achats et des finances
   [Délégation est donnée à] : M. Thomas DUPONT , fonction : responsable de l'Unité budget et contrôle interne au sein de la Direction des achats et des finances

Exemple 2:

1. Lecture du document :
   Je commence par lire attentivement l'extrait suivant pour en comprendre le contexte et la structure.

   "En cas d'absence ou d'empêchement de Mme Sophia DUBOIS, directrice de l'aide et diffusion aux publics, délégation est donnée à Mme Camille LAURENT, adjointe, dans la limite de ses attributions et fonctions :

   - les engagements financiers relatifs à l'activité de la

   Direction de l'aide et diffusion aux publics d'un montant hors taxe inférieur à 25 000 € et les engagements contractuels afférents ;
   - les lettres de mission envoyées à des collaborateurs externes pour la relecture de rapports produits par Santé publique France avec la mention du montant d'indemnisation de la vacation ;
   - toute décision relative aux opérations d'inventaire dans le cadre de l'arrêté annuel des comptes."

2. Recherche du terme "En cas d'absence ou d'empêchement de" :
   Je cherche cette expression dans le texte et j'examine ce qui suit.

   Trouvé : "En cas d'absence ou d'empêchement de Mme Sophia DUBOIS"

   J'identifie donc le nom qui suit cette expression : Mme Sophia DUBOIS

   Si cette expression n'était pas présente, j'indiquerais "Non mentionné".

   Si cette expression est présente j'identife également la fonction devant le nom de Mme Sophia DUBOIS : directrice de l'aide et diffusion aux publics

   la fonction est : directrice de l'aide et diffusion aux publics

3. Recherche du terme "délégation est donnée à" :
   Je cherche cette expression dans le texte et j'examine ce qui suit.

   Trouvé : "délégation est donnée à Mme Camille LAURENT"

   J'identifie donc le nom qui suit cette expression : Mme Camille LAURENT

   Si cette expression n'était pas présente, j'indiquerais "Non mentionné".

   Si cette expression est présente j'identife également la fonction devant le nom de Mme Camille LAURENT : adjointe

   la fonction est : adjointe

4. Format de sortie :
   Je structure les informations collectées selon le format demandé.

   [En cas d'absence ou d'empêchement de] : Mme Sophia DUBOIS fonction : directrice de l'aide et diffusion aux publics
   [Délégation est donnée à] : Mme Camille LAURENT fonction : adjointe

Le résultat final pour l'ensemble du document ressemblera à ceci :

Article 22
[En cas d'absence ou d'empêchement de] : Mme Sophia DUBOIS fonction : directrice de l'aide et diffusion aux publics
[Délégation est donnée à] : Mme Camille LAURENT fonction : adjointe

Article 8
[En cas d'absence ou d'empêchement de] : Mme Sophie MARTIN (épouse DURAND) fonction : directrice des achats et des finances
[Délégation est donnée à] : M. Thomas DUPONT fonction : responsable de l'Unité budget et contrôle interne au sein de la Direction des achats et des finances

Article 15
[En cas d'absence ou d'empêchement de] : Non mentionné
[Délégation est donnée à] : Non mentionné
"""),
    ("human", "Analysez le texte suivant :\n\n{text_content}")
])

def analyze_extracted_file(extracted_file_path: str):
    """
    Analyse le fichier extrait avec votre prompt sophistiqué
    """
    try:
        # Lire le fichier
        with open(extracted_file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
        
        # Préparer le prompt avec le contenu du texte
        prompt_value = analysis_prompt_template.invoke({
            "text_content": text_content
        })
        
        # Invoquer le LLM
        response = llm.invoke(prompt_value.to_messages())
        
        return response.content
        
    except Exception as e:
        return f"Erreur lors de l'analyse: {str(e)}"

# ===== PARTIE 3: MCP TOOLS =====

@mcp.tool()
def extract_and_analyze_pdf(pdf_filename: str, start_page: int = None, end_page: int = None) -> str:
    """
    Extract text from PDF pages and analyze it.
    
    Args:
        pdf_filename (str): Name of the PDF file (e.g., "2025.5.sante.pdf")
        start_page (int): First page to extract (optional)
        end_page (int): Last page to extract (optional)
    Returns:
        str: Analysis results
    """
    try:
        # Construire le chemin complet du PDF
        pdf_paths_to_try = [
            pdf_filename,  # Fichier directement accessible
            os.path.join(BASE_DIR, pdf_filename),  # Dans le répertoire de base
            os.path.join(PATH, pdf_filename)  # Dans le répertoire du script
        ]
        
        pdf_path = None
        for path in pdf_paths_to_try:
            if os.path.exists(path):
                pdf_path = path
                break
        
        if not pdf_path:
            return f"""
Erreur: Fichier PDF non trouvé: {pdf_filename}

Chemins testés:
- {pdf_filename}
- {os.path.join(BASE_DIR, pdf_filename)}  
- {os.path.join(PATH, pdf_filename)}
"""
        
        # Étape 1: Extraction du PDF
        output_dir = os.path.join(BASE_DIR, "textes_extraits")
        extracted_file_path = extract_pdf_text(pdf_path, output_dir, start_page, end_page)
        
        if not extracted_file_path or extracted_file_path.startswith("Erreur:"):
            return f"Erreur lors de l'extraction du PDF: {extracted_file_path}"
        
        # Étape 2: Analyse avec votre prompt sophistiqué
        analysis_result = analyze_extracted_file(extracted_file_path)
        
        return f"""
=== EXTRACTION ET ANALYSE TERMINÉES ===

PDF source: {pdf_path}
Pages analysées: {start_page or 'début'} à {end_page or 'fin'}
Fichier extrait: {extracted_file_path}

=== RÉSULTATS DE L'ANALYSE ===
{analysis_result}
        """
        
    except Exception as e:
        return f"Erreur lors du traitement: {str(e)}"

@mcp.tool()
def test_connection() -> str:
    """
    Test tool to verify MCP server is working.
    
    Returns:
        str: Simple test message
    """
    return "✅ Connexion MCP réussie ! Le serveur PDF fonctionne correctement."

@mcp.tool()
def pdf_query_tool(query: str) -> str:
    """
    Query the PDF content using a retriever.
    
    Args:
        query (str): The query to search in the PDF content
    Returns:
        str: A str of the retrieved document sections
    """
    return f"Recherche pour '{query}' dans le contenu PDF extrait."

# ===== LANCEMENT DU SERVEUR =====

if __name__ == "__main__":
    import sys
    
    # Mode de démarrage selon les arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Mode test local
        print("🧪 Mode test local activé...")
        print("🚀 Démarrage du serveur MCP PDF-Analysis...")
        print("📋 Outils disponibles:")
        print("   - extract_and_analyze_pdf: Extraction + Analyse complète")
        print("   - test_connection: Test de connexion")
        print("   - pdf_query_tool: Recherche dans le PDF")
        
        print("\n🧪 Test de connexion...")
        try:
            result_test = test_connection()
            print(result_test)
        except Exception as e:
            print(f"Erreur test connexion: {e}")
        
        print("\n🧪 Test d'extraction et analyse...")
        try:
            result = extract_and_analyze_pdf("2025.5.sante.pdf", 117, 131)
            print(result)
        except Exception as e:
            print(f"Erreur lors du test: {e}")
            import traceback
            traceback.print_exc()
    else:
        # Mode serveur MCP normal - EXACTEMENT comme le script qui marche
        print("Starting PDF-Analysis-MCP-Server...")
        try:
            mcp.run()
        except KeyboardInterrupt:
            print("Server stopped by user")
        except Exception as e:
            print(f"Server error: {e}")