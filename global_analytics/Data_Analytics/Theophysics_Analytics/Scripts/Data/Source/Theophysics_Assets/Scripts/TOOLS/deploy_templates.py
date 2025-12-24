"""
Deploy LOCAL analysis folders to all 12 Logos Papers
"""

import shutil
from pathlib import Path

BASE = Path(r"D:\THEOPHYSICS_MASTER\06_Publication\Logos_Papers")
TEMPLATE_SOURCE = BASE / "P03-Algorithm-Reality" / "_LOCAL"

PAPERS = [
    "P01-Logos-Principle",
    "P02-Quantum-Bridge",
    "P03-Algorithm-Reality",  # Already has it
    "P04-Hard-Problem",
    "P05-Soul-Observer",
    "P06-Physics-Principalities",
    "P07-Grace-Function",
    "P08-Stretched-Heavens",
    "P09-Moral-Universe",
    "P10-Creatio-Silico",
    "P11-Protocols-Validation",
    "P12-Decalogue-Cosmos"
]

def deploy_template(paper_folder):
    """Copy template to a paper folder"""
    dest = paper_folder / "_LOCAL"
    
    if dest.exists():
        print(f"[OK] {paper_folder.name} already has _LOCAL")
        return
    
    try:
        # Copy the entire _LOCAL folder
        shutil.copytree(TEMPLATE_SOURCE, dest)
        print(f"[OK] Deployed to {paper_folder.name}")
        
        # Update the paper name in config.json if needed
        config_file = dest / "config.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = f.read()
            
            # Replace paper name reference
            config = config.replace("Paper-03-Algorithm-Reality", f"Paper-{paper_folder.name}")
            
            with open(config_file, 'w') as f:
                f.write(config)
    
    except Exception as e:
        print(f"[ERROR] Error deploying to {paper_folder.name}: {e}")

if __name__ == "__main__":
    print("="*60)
    print("DEPLOYING LOCAL FOLDERS TO ALL PAPERS")
    print("="*60 + "\n")
    
    for paper_name in PAPERS:
        paper_folder = BASE / paper_name
        if paper_folder.exists():
            deploy_template(paper_folder)
        else:
            print(f"[WARN] {paper_name} folder not found")
    
    print("\n" + "="*60)
    print("[OK] DEPLOYMENT COMPLETE!")
    print("="*60)
    print("\nNext: Run master_orchestrator.py --all")
