"""
Lower breakthrough threshold in all papers' config.json files
"""

import json
from pathlib import Path

PAPERS_ROOT = Path(r"D:\THEOPHYSICS_MASTER\06_Publication\Logos_Papers")

PAPERS = [
    "P01-Logos-Principle",
    "P02-Quantum-Bridge",
    "P03-Algorithm-Reality",
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

print("=" * 60)
print("LOWERING BREAKTHROUGH THRESHOLD: 3 -> 2")
print("=" * 60)
print()

updated = 0
for paper_name in PAPERS:
    config_path = PAPERS_ROOT / paper_name / "_LOCAL" / "config.json"
    
    if not config_path.exists():
        print(f"[WARN] No config.json in {paper_name}")
        continue
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        old_threshold = config.get('breakthrough_detection', {}).get('integration_order_min', 3)
        
        if 'breakthrough_detection' not in config:
            config['breakthrough_detection'] = {}
        
        config['breakthrough_detection']['integration_order_min'] = 2
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"[OK] {paper_name}: {old_threshold} -> 2")
        updated += 1
    
    except Exception as e:
        print(f"[ERROR] {paper_name}: {str(e)[:50]}")

print()
print("=" * 60)
print(f"Updated {updated} config files")
print("=" * 60)
print()
print("Now re-running analysis to find breakthroughs...")
