import sys
from pathlib import Path
from get_topology import extract_topology

# --- CONFIGURATION CENTRALISÉE ---
BASE_DIR = Path(__file__).parent.absolute()

# Chemins
GNS3_PROJECT_FILE = r"C:\Users\Hector\Desktop\INSA Lyon\3A-TC\S1\GNS Projet\blank_project\blank_project.gns3"
OUTPUT_DIR = BASE_DIR / "configs"
TEMPLATE_FILE = BASE_DIR / "router_rip.j2"
TOPOLOGY_FILE = BASE_DIR / "topology.json"

# Configuration réseau
IP_BASE = "10.0.0.0/30"

# --- IMPORTS DYNAMIQUES ---
try:
    from jinja2 import Template
except ImportError:
    print("Erreur : Jinja2 n'est pas installé. Installez-le avec : pip install jinja2")
    sys.exit(1)

import json
from collections import defaultdict


def generate_configs():
    """
    Génère les fichiers de configuration à partir du topology.json
    """
    # Vérifier que topology.json existe
    if not TOPOLOGY_FILE.exists():
        print(f"Erreur : {TOPOLOGY_FILE} n'existe pas.")
        print("Exécutez d'abord extract_topology().")
        return False
    
    # Vérifier que le template existe
    if not TEMPLATE_FILE.exists():
        print(f"Erreur : Le template {TEMPLATE_FILE} n'existe pas.")
        return False
    
    # Créer le répertoire de sortie
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Charger la topologie
    with open(TOPOLOGY_FILE, "r", encoding="utf-8") as f:
        topology_data = json.load(f)
    
    # Charger le template Jinja2
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = Template(f.read())
    
    # Générer les configs
    print(f"\n--- GÉNÉRATION DES CONFIGURATIONS ---")
    for router in topology_data["routers"]:
        config = template.render(
            name=router["name"],
            interfaces=router["interfaces"],
            rip_networks=router["rip_networks"]
        )
        
        output_file = OUTPUT_DIR / f"{router['name']}.cfg"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(config)
        print(f" -> Configuration générée : {output_file}")
    
    print(f"\nTerminé ! Les fichiers .cfg sont dans : {OUTPUT_DIR}")
    return True


def main():
    """
    Fonction principale : exécute l'extraction de topologie et la génération de configs
    """
    print("=" * 60)
    print("EXTRACTION DE TOPOLOGIE GNS3 ET GÉNÉRATION DE CONFIGURATIONS")
    print("=" * 60)
    
    # Étape 1 : Extraire la topologie
    print(f"\nÉtape 1 : Extraction de la topologie depuis {GNS3_PROJECT_FILE}")
    print("-" * 60)
    try:
        extract_topology(GNS3_PROJECT_FILE, IP_BASE, BASE_DIR)
    except Exception as e:
        print(f"Erreur lors de l'extraction : {e}")
        sys.exit(1)
    
    # Étape 2 : Générer les configurations
    print(f"\nÉtape 2 : Génération des fichiers de configuration")
    print("-" * 60)
    try:
        success = generate_configs()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"Erreur lors de la génération : {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("SUCCÈS : Processus complété !")
    print("=" * 60)


if __name__ == "__main__":
    main()