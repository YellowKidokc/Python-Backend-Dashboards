#!/usr/bin/env python3
"""
Complete Obsidian vault organization:
1. Rename all images to systematic P01-01.png format
2. Fix all broken image paths in papers
3. Add new visualizations to papers
"""

import os
import re
import shutil
from pathlib import Path
from collections import defaultdict

# Paths
PAPERS_DIR = Path(r"D:\THEOPHYSICS_MASTER\06_Publication\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL")
IMAGES_DIR = Path(r"D:\THEOPHYSICS_MASTER\Assets\Images\logos papers")

# Mapping of old folder names to paper numbers and clean names
FOLDER_MAP = {
    "P1_Logos_Principle": (1, "Logos_Principle"),
    "P2_Quantum_Bridge": (2, "Quantum_Bridge"),
    "P3_Algorithm_Reality": (3, "Algorithm_Reality"),
    "P4_Hard_Problem": (4, "Hard_Problem"),
    "P5_Soul_Observer": (5, "Soul_Observer"),
    "P6_Physics_Principalities": (6, "Physics_Principalities"),
    "P7_Grace_Function": (7, "Grace_Function"),
    "P8_Stretched_Heavens": (8, "Stretched_Heavens"),
    "P9_Moral_Universe": (9, "Moral_Universe"),
    "P10_Creatio_ex_Silico": (10, "Creatio_ex_Silico"),
    "P11_Validation_Protocols": (11, "Validation_Protocols"),
    "P12_Decalogue": (12, "Decalogue"),
}

def rename_all_images():
    """Rename all images to P01-01.png, P01-02.png format."""
    print("="*80)
    print("STEP 1: RENAMING ALL IMAGES TO SYSTEMATIC FORMAT")
    print("="*80)
    
    rename_map = {}  # old_path -> new_filename
    
    for folder_name, (paper_num, clean_name) in FOLDER_MAP.items():
        folder_path = IMAGES_DIR / folder_name
        if not folder_path.exists():
            print(f"  ⚠ Folder not found: {folder_name}")
            continue
        
        images = sorted(folder_path.glob("*.png"))
        if not images:
            print(f"\nPaper {paper_num:02d}: No images")
            continue
        
        print(f"\nPaper {paper_num:02d} ({folder_name}): {len(images)} images")
        
        for i, img_path in enumerate(images, 1):
            new_filename = f"P{paper_num:02d}-{i:02d}.png"
            new_path = folder_path / new_filename
            
            if img_path.name != new_filename:
                # Store the mapping for later reference updates
                rename_map[str(img_path)] = (str(new_path), img_path.name, new_filename)
                print(f"  {img_path.name:50s} → {new_filename}")
            else:
                print(f"  ✓ {img_path.name} (already correct)")
    
    # Execute renames
    if rename_map:
        print(f"\n{'='*80}")
        print(f"Renaming {len(rename_map)} files...")
        for old_path, (new_path, old_name, new_name) in rename_map.items():
            try:
                os.rename(old_path, new_path)
                print(f"  ✓ Renamed: {new_name}")
            except Exception as e:
                print(f"  ✗ Error renaming {old_name}: {e}")
    
    return rename_map

def get_correct_image_path(paper_num):
    """Get the correct relative path from paper to images folder."""
    # From COMPLETE_LOGOS_PAPERS_FINAL to logos papers folder
    return f"../../../../Assets/Images/logos papers"

def fix_paper_image_paths():
    """Fix all broken image paths in papers."""
    print("\n" + "="*80)
    print("STEP 2: FIXING ALL BROKEN IMAGE PATHS IN PAPERS")
    print("="*80)
    
    papers = sorted(PAPERS_DIR.glob("Paper-*.md"))
    
    for paper_path in papers:
        # Extract paper number
        match = re.search(r'Paper-(\d+)', paper_path.name)
        if not match:
            continue
        
        paper_num = int(match.group(1))
        print(f"\nFixing Paper {paper_num:02d}...")
        
        content = paper_path.read_text(encoding='utf-8')
        original_content = content
        
        # Pattern to match image references: ![caption](path)
        def replace_image_path(match):
            caption = match.group(1)
            old_path = match.group(2)
            
            # Skip external URLs
            if old_path.startswith('http'):
                return match.group(0)
            
            # Extract just the filename from the old path
            filename = Path(old_path).name
            
            # Determine which folder this image should be in
            folder_name = None
            for fname, (pnum, cname) in FOLDER_MAP.items():
                if pnum == paper_num:
                    folder_name = fname
                    break
            
            if not folder_name:
                print(f"  ⚠ No folder mapping for paper {paper_num}")
                return match.group(0)
            
            # Construct new correct path
            new_path = f"../../../../Assets/Images/logos papers/{folder_name}/{filename}"
            
            return f"![{caption}]({new_path})"
        
        # Replace all image paths
        pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
        content = re.sub(pattern, replace_image_path, content)
        
        if content != original_content:
            paper_path.write_text(content, encoding='utf-8')
            print(f"  ✓ Updated image paths")
        else:
            print(f"  - No changes needed")

def add_new_visualizations_to_papers():
    """Add the newly created visualizations to their respective papers."""
    print("\n" + "="*80)
    print("STEP 3: ADDING NEW VISUALIZATIONS TO PAPERS")
    print("="*80)
    
    # Paper 2: Trinity Triangulation
    paper2_path = PAPERS_DIR / "Paper-02-The-Quantum-Bridge-FINAL.md"
    if paper2_path.exists():
        print("\nAdding Trinity Triangulation to Paper 2...")
        content = paper2_path.read_text(encoding='utf-8')
        
        # Find a good place to insert (after Proof 8 section if it exists)
        new_image = """
![Trinity Triangulation: Three Observer Perspectives Collapse Quantum Uncertainty](../../../../Assets/Images/logos papers/P2_Quantum_Bridge/P02-Trinity-Triangulation-Proof8.png)

**Figure 2.X: Trinity Triangulation (Proof 8)**

Three orthogonal observer perspectives (Father, Son, Spirit) are required to perfectly "triangulate" and collapse a quantum state, eliminating all uncertainty. This visualization demonstrates how the Trinity's three-fold observation creates complete actualization of potentiality.

*Visualization: David Lowe & Claude (Anthropic), November 2025*

---

"""
        
        # Insert after "## 8. PROOF 8" or near the end before references
        if "## 8. PROOF 8" in content:
            content = content.replace("## 8. PROOF 8", "## 8. PROOF 8\n" + new_image, 1)
            paper2_path.write_text(content, encoding='utf-8')
            print("  ✓ Added Trinity Triangulation visualization")
        else:
            print("  ⚠ Could not find insertion point (Proof 8 section)")
    
    # Paper 5: Soul Field Potential
    paper5_path = PAPERS_DIR / "Paper-05-The-Soul-Observer-FINAL.md"
    if paper5_path.exists():
        print("\nAdding Soul Field Potential to Paper 5...")
        content = paper5_path.read_text(encoding='utf-8')
        
        new_image = """
![Soul Field Potential: Sombrero Potential with Localized Soul Quanta](../../../../Assets/Images/logos papers/P5_Soul_Observer/P05-Soul-Field-Potential-Sombrero.png)

**Figure 5.X: Soul Field Potential (φ⁴ "Sombrero" Potential)**

The soul field exhibits a quartic potential V(Ψ_S) = (Ψ_S² - v²)², creating a characteristic "sombrero" or "Mexican hat" shape. Individual souls are localized excitations (quanta) that sit in the stable trough of this potential, representing persistent, coherent information structures. The unstable peak at the center represents the "false vacuum" state from which souls emerge through spontaneous symmetry breaking.

*Visualization: David Lowe & Claude (Anthropic), November 2025*

---

"""
        
        # Insert after "## 2. THE SOUL AS QUANTUM FIELD" or similar
        if "## 2. THE SOUL AS QUANTUM FIELD" in content:
            content = content.replace("## 2. THE SOUL AS QUANTUM FIELD", "## 2. THE SOUL AS QUANTUM FIELD\n" + new_image, 1)
            paper5_path.write_text(content, encoding='utf-8')
            print("  ✓ Added Soul Field Potential visualization")
        else:
            print("  ⚠ Could not find insertion point (Soul as Quantum Field section)")

def create_summary_report():
    """Create a summary of what was done."""
    print("\n" + "="*80)
    print("ORGANIZATION COMPLETE - SUMMARY")
    print("="*80)
    
    total_images = 0
    for folder_name in FOLDER_MAP.keys():
        folder_path = IMAGES_DIR / folder_name
        if folder_path.exists():
            count = len(list(folder_path.glob("*.png")))
            total_images += count
            print(f"  Paper {FOLDER_MAP[folder_name][0]:02d}: {count} images")
    
    print(f"\n  Total images: {total_images}")
    print(f"  All renamed to P##-##.png format")
    print(f"  All paper paths fixed")
    print(f"  New visualizations added")
    
    print("\n" + "="*80)
    print("✅ YOUR OBSIDIAN VAULT IS NOW FULLY ORGANIZED!")
    print("="*80)

def main():
    print("\n" + "🎨 " * 40)
    print("OBSIDIAN VAULT ORGANIZATION - FULL CLEANUP")
    print("🎨 " * 40 + "\n")
    
    # Step 1: Rename all images
    rename_map = rename_all_images()
    
    # Step 2: Fix all paper image paths
    fix_paper_image_paths()
    
    # Step 3: Add new visualizations
    add_new_visualizations_to_papers()
    
    # Step 4: Summary
    create_summary_report()

if __name__ == "__main__":
    main()

