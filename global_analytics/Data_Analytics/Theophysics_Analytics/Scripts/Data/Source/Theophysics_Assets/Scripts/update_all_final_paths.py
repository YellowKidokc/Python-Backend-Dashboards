#!/usr/bin/env python3
"""
Update all FINAL papers to use correct organized image paths
Maps old image names to new organized structure
"""
import re
from pathlib import Path

# Location to update
BASE_PATH = Path("D:/THEOPHYSICS_MASTER/03_PUBLICATIONS/Logos_Papers/COMPLETE_LOGOS_PAPERS_FINAL")
ASSETS_BASE = Path("COMPLETE_LOGOS_PAPERS_FINAL/assets")

# Image name mappings - map old names to new organized names
IMAGE_MAPPINGS = {
    # Paper 1 mappings
    1: {
        "P1_02_great_schism.png": "P1-02-great-schism-O-1-of-17.png",
        "P1_12_participatory_universe_3d.png": "P1-12-participatory-universe-3d-O-2-of-17.png",
        "P1_03_information_substrate.png": "P1-03-information-substrate-O-3-of-17.png",
        "P1-01_information_substrate.png": "P1-01-information-substrate-O-4-of-17.png",
        "P1observer_creates_reality_3d.png": "P1-P1observer-creates-reality-3d-O-5-of-17.png",
        "P1-02_self_referential.png": "P1-02-self-referential-O-6-of-17.png",
        "P1-03_zero_divergence.png": "P1-03-zero-divergence-O-7-of-17.png",
        "P1-04_vapor_ice_analogy.png": "P1-04-vapor-ice-analogy-O-8-of-17.png",
        "P1_05_spacetime_curvature.png": "P1-05-spacetime-curvature-O-9-of-17.png",
        "P1_06_superposition_truth.png": "P1-06-superposition-truth-O-10-of-17.png",
        "P1_04_wave_collapse_mechanism.png": "P1-04-wave-collapse-mechanism-O-11-of-17.png",
        "P1_07_three_stage_collapse.png": "P1-07-three-stage-collapse-O-12-of-17.png",
        "P1_08_shared_reality.png": "P1-08-shared-reality-O-13-of-17.png",
        "P1_09_entanglement_correlation.png": "P1-09-entanglement-correlation-O-14-of-17.png",
        "P1_10_full_spectrum.png": "P1-10-full-spectrum-O-15-of-17.png",
        "P1_05_coherence_functional.png": "P1-05-coherence-functional-O-16-of-17.png",
        "P1_13_universe_compressed_code_3d.png": "P1-13-universe-compressed-code-3d-O-17-of-17.png",
    },
    # Add other papers as needed
}

def update_paper_images(paper_path, paper_num):
    """Update image paths in a paper"""
    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    mappings = IMAGE_MAPPINGS.get(paper_num, {})
    
    # Pattern: ![alt](../assets/P1/old_name.png) or ![alt](../../../../Assets/...)
    # Replace with new organized names
    for old_name, new_name in mappings.items():
        # Pattern 1: ../assets/P1/old_name.png
        pattern1 = f'../assets/P{paper_num}/{old_name}'
        replacement1 = f'../assets/P{paper_num}/{new_name}'
        content = content.replace(pattern1, replacement1)
        
        # Pattern 2: ../../../../Assets/Images/logos papers/P1_Logos_Principle/old_name.png
        pattern2 = f'../../../../Assets/Images/logos papers/P{paper_num}_[^/]+/{old_name}'
        content = re.sub(pattern2, replacement1, content)
    
    if content != original:
        with open(paper_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

if __name__ == "__main__":
    if not BASE_PATH.exists():
        print(f"Path {BASE_PATH} doesn't exist")
        exit(1)
    
    print(f"Processing papers in: {BASE_PATH}\n")
    papers_updated = []
    
    for paper_file in sorted(BASE_PATH.glob("Paper-*-FINAL.md")):
        match = re.search(r'Paper-(\d+)-', paper_file.name)
        if not match:
            continue
        
        paper_num = int(match.group(1))
        if update_paper_images(paper_file, paper_num):
            papers_updated.append(paper_file.name)
            print(f"  ✓ Updated: {paper_file.name}")
    
    print(f"\n{'='*60}")
    print(f"Updated {len(papers_updated)} papers")
    print(f"{'='*60}")

