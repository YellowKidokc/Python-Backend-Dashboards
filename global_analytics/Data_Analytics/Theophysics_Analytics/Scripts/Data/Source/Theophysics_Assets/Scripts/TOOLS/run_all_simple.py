"""
Simple batch runner for all 12 papers
"""

import subprocess
import os
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
print("RUNNING ANALYSIS ON ALL 12 PAPERS")
print("=" * 60)
print()

success_count = 0
error_count = 0

for paper_name in PAPERS:
    paper_path = PAPERS_ROOT / paper_name
    local_path = paper_path / "_LOCAL"
    script = local_path / "analyze_paper.py"
    
    print(f"\n[{success_count + error_count + 1}/12] {paper_name}...")
    
    if not script.exists():
        print(f"   [ERROR] No analyzer script found")
        error_count += 1
        continue
    
    try:
        result = subprocess.run(
            ["python", str(script)],
            cwd=str(local_path),
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print(f"   [OK] Analysis complete")
            success_count += 1
        else:
            print(f"   [ERROR] Analysis failed")
            error_count += 1
    except Exception as e:
        print(f"   [ERROR] {str(e)[:50]}")
        error_count += 1

print()
print("=" * 60)
print(f"COMPLETE: {success_count} successful, {error_count} errors")
print("=" * 60)
