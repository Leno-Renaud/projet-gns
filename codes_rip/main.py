from cfg_generation import cfg_generation
from get_topology import extract_topology


def main():
    BASE_DIR = Path(__file__).parent.absolute()
    GNS3_PROJECT_FILE = r"C:\Users\Hector\Desktop\INSA Lyon\3A-TC\S1\GNS Projet\blank_project\blank_project.gns3"
    IP_BASE = "10.0.0.0/30"
    extract_topology(GNS3_PROJECT_FILE, IP_BASE, BASE_DIR)
    cfg_generation("topologie.json")