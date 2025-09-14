import os
import shutil
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("extract-ppt")

@dataclass
class ExtractConfig:
    """Configuration pour l'extraction de fichiers"""
    base_dir: str = os.path.abspath(r"C:\Users\kosmo\Documents\ProcessEx")
    source_path: str = ""
    depot_path: str = ""
    days_limit: int = 365  # Fichiers de moins d'un an
    size_threshold_kb: int = 500  # Taille minimum en KB
    extensions: List[str] = None
    
    def __post_init__(self):
        if not self.source_path:
            self.source_path = os.path.join(self.base_dir, "ProcessEx")
        if not self.depot_path:
            self.depot_path = os.path.join(self.base_dir, "Depots")
        if self.extensions is None:
            self.extensions = [".ppt", ".pptx"]

# Configuration globale par défaut
default_config = ExtractConfig()

@mcp.tool()
def configure_extraction(
    base_dir: str = None,
    source_path: str = None,
    depot_path: str = None,
    days_limit: int = None,
    size_threshold_kb: int = None,
    extensions: List[str] = None
) -> str:
    """
    Configure les parametres d'extraction des fichiers PowerPoint.
    
    Args:
        base_dir: Repertoire de base (defaut: C:/Users/kosmo/Documents/ProcessEx)
        source_path: Chemin source des fichiers (defaut: base_dir/ProcessEx)
        depot_path: Chemin destination (defaut: base_dir/Depots)
        days_limit: Limite d'age en jours (defaut: 365)
        size_threshold_kb: Taille minimum en KB (defaut: 500)
        extensions: Extensions de fichiers a traiter (defaut: [".ppt", ".pptx"])
        
    Returns:
        Configuration mise a jour au format JSON
    """
    global default_config
    
    # Mettre a jour la configuration avec les parametres fournis
    if base_dir is not None:
        default_config.base_dir = os.path.abspath(base_dir)
    if source_path is not None:
        default_config.source_path = os.path.abspath(source_path)
    if depot_path is not None:
        default_config.depot_path = os.path.abspath(depot_path)
    if days_limit is not None:
        default_config.days_limit = days_limit
    if size_threshold_kb is not None:
        default_config.size_threshold_kb = size_threshold_kb
    if extensions is not None:
        default_config.extensions = extensions
    
    # Recalculer les chemins par defaut si necessaire
    if not default_config.source_path or source_path is None:
        default_config.source_path = os.path.join(default_config.base_dir, "ProcessEx")
    if not default_config.depot_path or depot_path is None:
        default_config.depot_path = os.path.join(default_config.base_dir, "Depots")
    
    config_dict = asdict(default_config)
    return json.dumps(config_dict, indent=2, ensure_ascii=False)

@mcp.tool()
def search_and_filter_files(
    source_path: str = None,
    size_threshold_kb: int = None,
    days_limit: int = None,
    extensions: List[str] = None,
    show_rejected: bool = False
) -> str:
    """
    Recherche et filtre les fichiers selon les critères spécifiés.
    
    Args:
        source_path: Chemin source à analyser (utilise la config par défaut si non fourni)
        size_threshold_kb: Taille minimum en KB (utilise la config par défaut si non fourni)
        days_limit: Âge maximum en jours (utilise la config par défaut si non fourni)
        extensions: Extensions à traiter (utilise la config par défaut si non fourni)
        show_rejected: Afficher le détail des fichiers rejetés
        
    Returns:
        Résultats de la recherche et du filtrage au format JSON
    """
    
    # Utiliser la config par défaut si paramètres non fournis
    source_path = source_path if source_path is not None else default_config.source_path
    size_threshold_kb = size_threshold_kb if size_threshold_kb is not None else default_config.size_threshold_kb
    days_limit = days_limit if days_limit is not None else default_config.days_limit
    extensions = extensions if extensions is not None else default_config.extensions
    
    # Conversion des paramètres
    size_threshold_bytes = size_threshold_kb * 1024
    date_limit = datetime.now() - timedelta(days=days_limit)
    
    if not os.path.exists(source_path):
        return json.dumps({
            'success': False,
            'error': f"Chemin source introuvable: {source_path}",
            'acceptes': [],
            'rejetes': [],
            'stats': {}
        }, indent=2, ensure_ascii=False)
    
    fichiers_acceptes = []
    fichiers_rejetes = []
    stats = {
        "total_examines": 0,
        "rejetes_extension": 0,
        "rejetes_taille": 0,
        "rejetes_date": 0,
        "rejetes_acces": 0,
        "acceptes": 0,
    }
    dossiers_stats = {}
    
    # Parcours des dossiers
    for item in os.listdir(source_path):
        item_path = os.path.join(source_path, item)
        if not os.path.isdir(item_path):
            continue
            
        count_dossier = 0
        
        for root, dirs, files in os.walk(item_path):
            for file in files:
                file_path = os.path.join(root, file)
                stats["total_examines"] += 1
                
                # Vérification extension
                if not any(file.lower().endswith(ext) for ext in extensions):
                    stats["rejetes_extension"] += 1
                    fichiers_rejetes.append({
                        "chemin": file_path,
                        "nom": file,
                        "raison": "Extension non supportée",
                        "dossier": item
                    })
                    continue
                
                try:
                    # Métadonnées fichier
                    taille = os.path.getsize(file_path)
                    date_mod = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    # Filtrage par taille
                    if taille < size_threshold_bytes:
                        stats["rejetes_taille"] += 1
                        fichiers_rejetes.append({
                            "chemin": file_path,
                            "nom": file,
                            "raison": f"Taille insuffisante ({round(taille/1024, 1)} KB < {size_threshold_kb} KB)",
                            "taille": taille,
                            "date_modification": date_mod.isoformat(),
                            "dossier": item
                        })
                        continue
                    
                    # Filtrage par date
                    if date_mod < date_limit:
                        stats["rejetes_date"] += 1
                        fichiers_rejetes.append({
                            "chemin": file_path,
                            "nom": file,
                            "raison": f"Fichier trop ancien ({(datetime.now() - date_mod).days} jours > {days_limit} jours)",
                            "taille": taille,
                            "date_modification": date_mod.isoformat(),
                            "dossier": item
                        })
                        continue
                    
                    # Fichier accepté
                    fichier_info = {
                        "chemin": file_path,
                        "nom": file,
                        "taille": taille,
                        "date_modification": date_mod.isoformat(),
                        "taille_mb": round(taille / (1024 * 1024), 2),
                        "taille_kb": round(taille / 1024, 1),
                        "age_jours": (datetime.now() - date_mod).days,
                        "dossier": item,
                        "classification_ok": True
                    }
                    
                    fichiers_acceptes.append(fichier_info)
                    count_dossier += 1
                    stats["acceptes"] += 1
                    
                except (OSError, PermissionError) as e:
                    stats["rejetes_acces"] += 1
                    fichiers_rejetes.append({
                        "chemin": file_path,
                        "nom": file,
                        "raison": f"Erreur d'accès: {str(e)}",
                        "dossier": item
                    })
        
        dossiers_stats[item] = count_dossier
    
    # Préparer les résultats
    results = {
        'success': True,
        'acceptes': fichiers_acceptes,
        'rejetes': fichiers_rejetes if show_rejected else [],
        'stats': {
            'filtrage': stats,
            'dossiers': dossiers_stats,
            'total_rejetes': len(fichiers_rejetes),
            'total_acceptes': len(fichiers_acceptes)
        },
        'parametres_utilises': {
            'source_path': source_path,
            'size_threshold_kb': size_threshold_kb,
            'days_limit': days_limit,
            'extensions': extensions
        }
    }
    
    return json.dumps(results, indent=2, ensure_ascii=False)

@mcp.tool()
def copy_files_to_depot(
    search_results: str,
    depot_path: str = None,
    copy_rejected: bool = True,
    create_sel_files: bool = True
) -> str:
    """
    Copie les fichiers vers le dossier Depots avec organisation.
    
    Args:
        search_results: Résultats JSON de la recherche (obtenu via search_and_filter_files)
        depot_path: Chemin de destination (utilise la config par défaut si non fourni)
        copy_rejected: Copier aussi les fichiers rejetés
        create_sel_files: Créer le dossier Sel_Files pour les fichiers acceptés
        
    Returns:
        Résultats de la copie au format JSON
    """
    
    depot_path = depot_path or default_config.depot_path
    
    try:
        # Parser les résultats de recherche
        search_data = json.loads(search_results)
        if not search_data.get('success', False):
            return json.dumps({
                'success': False,
                'error': 'Données de recherche invalides ou échec de la recherche'
            }, indent=2, ensure_ascii=False)
        
        fichiers_acceptes = search_data.get('acceptes', [])
        fichiers_rejetes = search_data.get('rejetes', [])
        
    except json.JSONDecodeError:
        return json.dumps({
            'success': False,
            'error': 'Format JSON invalide pour les résultats de recherche'
        }, indent=2, ensure_ascii=False)
    
    # Créer dossier principal
    os.makedirs(depot_path, exist_ok=True)
    
    # Créer Sel_Files si demandé
    sel_files_path = None
    if create_sel_files:
        sel_files_path = os.path.join(depot_path, "Sel_Files")
        os.makedirs(sel_files_path, exist_ok=True)
    
    # Copie des fichiers acceptés
    copied_acceptes = 0
    taille_acceptes = 0
    errors_acceptes = []
    
    for fichier in fichiers_acceptes:
        try:
            file_path = fichier["chemin"]
            file_name = fichier["nom"]
            
            # Destination selon configuration
            if create_sel_files:
                destination = os.path.join(sel_files_path, file_name)
            else:
                destination = os.path.join(depot_path, file_name)
            
            # Éviter les doublons
            if os.path.exists(destination):
                base, ext = os.path.splitext(file_name)
                counter = 1
                while os.path.exists(destination):
                    new_name = f"{base}_{counter}{ext}"
                    destination = os.path.join(os.path.dirname(destination), new_name)
                    counter += 1
            
            shutil.copy(file_path, destination)
            copied_acceptes += 1
            taille_acceptes += fichier["taille"]
            
        except Exception as e:
            error_msg = f"Erreur copie {file_name}: {e}"
            errors_acceptes.append(error_msg)
    
    # Copie des fichiers rejetés
    copied_rejetes = 0
    taille_rejetes = 0
    errors_rejetes = []
    
    if copy_rejected and fichiers_rejetes:
        autre_path = os.path.join(depot_path, "Autre")
        os.makedirs(autre_path, exist_ok=True)
        
        # Grouper par raison
        rejetes_par_raison = {}
        for fichier in fichiers_rejetes:
            raison = fichier['raison'].split(':')[0].split('(')[0].strip()
            raison_clean = raison.replace(' ', '_').replace('é', 'e').lower()
            
            if raison_clean not in rejetes_par_raison:
                rejetes_par_raison[raison_clean] = []
            rejetes_par_raison[raison_clean].append(fichier)
        
        for raison, fichiers in rejetes_par_raison.items():
            sous_dossier = os.path.join(autre_path, raison)
            os.makedirs(sous_dossier, exist_ok=True)
            
            for fichier in fichiers:
                try:
                    file_path = fichier["chemin"]
                    file_name = fichier["nom"]
                    destination = os.path.join(sous_dossier, file_name)
                    
                    # Éviter doublons
                    if os.path.exists(destination):
                        base, ext = os.path.splitext(file_name)
                        counter = 1
                        while os.path.exists(destination):
                            new_name = f"{base}_{counter}{ext}"
                            destination = os.path.join(sous_dossier, new_name)
                            counter += 1
                    
                    shutil.copy(file_path, destination)
                    copied_rejetes += 1
                    if 'taille' in fichier:
                        taille_rejetes += fichier['taille']
                        
                except Exception as e:
                    error_msg = f"Erreur copie rejeté {fichier['nom']}: {e}"
                    errors_rejetes.append(error_msg)
    
    results = {
        'success': True,
        'copied_acceptes': copied_acceptes,
        'copied_rejetes': copied_rejetes,
        'taille_acceptes': taille_acceptes,
        'taille_rejetes': taille_rejetes,
        'taille_total_mb': round((taille_acceptes + taille_rejetes) / (1024 * 1024), 1),
        'errors': errors_acceptes + errors_rejetes,
        'sel_files_created': create_sel_files,
        'depot_path': depot_path,
        'structure_creee': {
            'depot_principal': depot_path,
            'sel_files': os.path.join(depot_path, "Sel_Files") if create_sel_files else None,
            'autre': os.path.join(depot_path, "Autre") if copy_rejected and fichiers_rejetes else None
        }
    }
    
    return json.dumps(results, indent=2, ensure_ascii=False)

@mcp.tool()
def extract_workflow(
    source_path: str = None,
    depot_path: str = None,
    size_threshold_kb: int = None,
    extensions: List[str] = None,
    copy_rejected: bool = True,
    show_rejected_details: bool = False
) -> str:
    """
    Workflow complet d'extraction : recherche, filtrage et copie en une seule opération.
    
    Args:
        source_path: Chemin source à analyser
        depot_path: Chemin de destination
        size_threshold_kb: Taille minimum en KB
        extensions: Extensions à traiter (ex: [".ppt", ".pptx", ".pdf"])
        copy_rejected: Copier aussi les fichiers rejetés
        show_rejected_details: Inclure les détails des fichiers rejetés
        
    Returns:
        Résultats complets du workflow au format JSON
    """
    
    try:
        # Phase 1: Recherche et filtrage
        search_results = search_and_filter_files(
            source_path=source_path,
            size_threshold_kb=size_threshold_kb,
            extensions=extensions,
            show_rejected=show_rejected_details
        )
        
        search_data = json.loads(search_results)
        if not search_data.get('success', False):
            return search_results
        
        # Vérifier s'il y a des fichiers acceptés
        if search_data['stats']['total_acceptes'] == 0:
            return json.dumps({
                'success': True,
                'phase_1_recherche': search_data,
                'phase_2_copie': None,
                'message': 'Aucun fichier accepté trouvé. Workflow terminé après la phase de recherche.',
                'workflow_complete': False
            }, indent=2, ensure_ascii=False)
        
        # Phase 2: Copie
        copy_results = copy_files_to_depot(
            search_results=search_results,
            depot_path=depot_path,
            copy_rejected=copy_rejected,
            create_sel_files=True
        )
        
        copy_data = json.loads(copy_results)
        
        # Résultats combinés
        workflow_results = {
            'success': copy_data.get('success', False),
            'workflow_complete': True,
            'phase_1_recherche': search_data,
            'phase_2_copie': copy_data,
            'resume_final': {
                'fichiers_examines': search_data['stats']['filtrage']['total_examines'],
                'fichiers_acceptes': search_data['stats']['total_acceptes'],
                'fichiers_rejetes': search_data['stats']['total_rejetes'],
                'taux_acceptation_pct': round(search_data['stats']['total_acceptes'] / max(1, search_data['stats']['filtrage']['total_examines']) * 100, 1),
                'files_copies_acceptes': copy_data['copied_acceptes'],
                'files_copies_rejetes': copy_data['copied_rejetes'],
                'taille_total_mb': copy_data['taille_total_mb'],
                'depot_cree': copy_data['depot_path']
            }
        }
        
        return json.dumps(workflow_results, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            'success': False,
            'error': f'Erreur dans le workflow: {str(e)}',
            'workflow_complete': False
        }, indent=2, ensure_ascii=False)

@mcp.tool()
def get_current_config() -> str:
    """
    Retourne la configuration actuelle du serveur.
    
    Returns:
        Configuration actuelle au format JSON
    """
    config_dict = asdict(default_config)
    return json.dumps(config_dict, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')