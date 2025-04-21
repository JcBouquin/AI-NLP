from typing import Any, Dict, List
import httpx
from bs4 import BeautifulSoup
import re
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("meteo-paris-scraper")

# Constants
BASE_URL = "https://www.meteo-paris.com/ile-de-france/previsions"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

async def fetch_webpage(url: str) -> str:
    """Fetch the webpage content."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html",
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching webpage: {e}")
            return ""

async def extract_weather_data_targeted(html_content: str) -> List[Dict[str, Any]]:
    """
    Extraction ciblée basée sur l'inspection HTML fournie.
    Cette méthode s'appuie sur les classes CSS spécifiques vues dans l'inspection.
    """
    if not html_content:
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    weather_data = []
    
    print("=== Extraction ciblée basée sur l'inspection HTML ===")
    
    # 1. Chercher les jours de la semaine avec leur numéro
    day_pattern = re.compile(r'(Lun\.|Mar\.|Mer\.|Jeu\.|Ven\.|Sam\.|Dim\.)\s*(\d+)')
    
    # Chercher les éléments qui contiennent le jour et le numéro
    day_containers = []
    
    # Méthode 1: Chercher les éléments qui contiennent directement le texte du jour
    for text in soup.find_all(string=day_pattern):
        parent = text.parent
        # Remonter jusqu'à trouver un conteneur qui semble être une ligne de prévision
        container = parent
        while container and container.name != 'div' and not container.get('class'):
            container = container.parent
        
        if container and container not in day_containers:
            day_containers.append(container)
    
    # Méthode 2: Chercher par structure de classes vue dans l'inspection
    row_selectors = [
        'div.flex-1',
        'div[class*="flex-1"]',
        'div.relative.flex',
        'div[class*="relative"]',
        'div.bg-secondary-darken'
    ]
    
    for selector in row_selectors:
        elements = soup.select(selector)
        for elem in elements:
            text = elem.get_text()
            if day_pattern.search(text) and elem not in day_containers:
                day_containers.append(elem)
    
    print(f"Trouvé {len(day_containers)} conteneurs potentiels de jours")
    
    # Pour chaque conteneur de jour, chercher les températures associées
    for i, container in enumerate(day_containers):
        container_text = container.get_text().strip()
        day_match = day_pattern.search(container_text)
        
        if day_match:
            full_day = day_match.group(0)
            full_day = full_day.split('.')[0] + '.' + full_day.split('.')[1][:2]
             
            print(f"\nAnalyse du conteneur #{i+1} pour {full_day}")
            
            # D'après l'inspection, les températures sont dans des éléments circulaires
            # avec des classes comme "rounded-full" ou des couleurs de fond spécifiques
            
            # Méthode 1: Chercher des éléments avec la classe rounded-full
            temp_elements = container.select('.rounded-full') or container.select('[class*="rounded"]')
            
            # Méthode 2: Chercher des éléments avec les couleurs de fond vues dans l'inspection
            if not temp_elements:
                temp_elements = []
                
                # Chercher par la structure de classe vue dans l'inspection
                for elem in container.find_all():
                    elem_classes = elem.get('class', [])
                    elem_class_str = ' '.join(elem_classes) if elem_classes else ''
                    
                    # Ces éléments correspondent souvent aux températures
                    if (('flex' in elem_class_str and 'items-center' in elem_class_str) or
                        ('bg-' in elem_class_str) or
                        ('rounded' in elem_class_str)):
                        
                        elem_text = elem.get_text().strip()
                        # Vérifier que c'est un nombre simple
                        if re.match(r'^\d+$', elem_text):
                            temp_elements.append(elem)
            
            # Si nous avons trouvé des éléments de température
            if temp_elements and len(temp_elements) >= 2:
                temp_texts = [elem.get_text().strip() for elem in temp_elements]
                print(f"  Textes des éléments de température: {temp_texts}")
                
                # Filtrer pour ne garder que les éléments qui contiennent des nombres
                temp_elements = [elem for elem in temp_elements if re.match(r'^\d+$', elem.get_text().strip())]
                
                if len(temp_elements) >= 2:
                    # Les deux premiers éléments sont probablement min et max
                    temp_min = temp_elements[0].get_text().strip()
                    temp_max = temp_elements[1].get_text().strip()
                    
                    print(f"  Températures trouvées: min={temp_min}, max={temp_max}")
                    
                    weather_data.append({
                        "date": full_day,
                        "temperature_min": temp_min,
                        "temperature_max": temp_max,
                        "source": "Ciblage précis"
                    })
                else:
                    print(f"  Pas assez d'éléments de température trouvés après filtrage")
            else:
                print(f"  Pas assez d'éléments de température trouvés")
                
                # Dernière tentative: chercher des nombres simples dans le conteneur
                numbers = re.findall(r'\b\d{1,2}\b', container_text)
                
                if len(numbers) >= 3:  # Jour + min + max
                    # Le premier nombre est souvent le jour
                    if numbers[0] in full_day:
                        temp_min, temp_max = numbers[1], numbers[2]
                    else:
                        temp_min, temp_max = numbers[0], numbers[1]
                    
                    print(f"  Températures extraites du texte: min={temp_min}, max={temp_max}")
                    
                    weather_data.append({
                        "date": full_day,
                        "temperature_min": temp_min,
                        "temperature_max": temp_max,
                        "source": "Extraction de texte"
                    })
    
    
    
    return weather_data





@mcp.tool()
async def get_meteo_paris() -> dict:
    """
    Récupère les prévisions météorologiques de Paris depuis meteo-paris.com.
    Retourne les températures minimales et maximales pour tous les jours disponibles.
    """
    print("=== Scraper Météo Paris - Version Ciblage Précis ===")
    html_content = await fetch_webpage(BASE_URL)
    
    if not html_content:
        print("Échec de la récupération de la page web")
        return {"error": "Impossible de récupérer les données météorologiques. Le site est peut-être indisponible."}
    
    print(f"Page web récupérée ({len(html_content)} caractères)")
    
    # Essayer d'abord l'extraction ciblée basée sur l'inspection HTML
    weather_data = await extract_weather_data_targeted(html_content)
    
        
    # Si aucune donnée n'a été trouvée
    if not weather_data:
        return {"error": "Aucune donnée météorologique trouvée sur la page."}
    
    # Retourner directement la structure de données pour qu'elle soit sérialisée en JSON proprement
    return {"previsions": weather_data}

if __name__ == "__main__":
    print("Starting Meteo Paris scraper MCP server...")
    # Initialize and run the server
    mcp.run(transport='stdio')