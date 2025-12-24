#!/usr/bin/env python3
"""
Properly fix all image paths in FINAL papers to use organized structure
Maps old image names to new organized names
"""
import re
from pathlib import Path
import os

# Location to fix
BASE_PATH = Path("D:/THEOPHYSICS_MASTER/03_PUBLICATIONS/Logos_Papers/COMPLETE_LOGOS_PAPERS_FINAL")

# Get all organized images to create mapping
ASSETS_PATH = Path("COMPLETE_LOGOS_PAPERS_FINAL/assets")

def build_image_mapping():
    """Build mapping from old names to new organized names"""
    mapping = {}
    
    # Scan organized assets
    for paper_dir in ASSETS_PATH.iterdir():
        if not paper_dir.is_dir():
            continue
        
        match = re.match(r'P(\d+)', paper_dir.name)
        if not match:
            continue
        
        paper_num = int(match.group(1))
        
        for img_file in paper_dir.glob("*.png"):
            new_name = img_file.name
            # Extract descriptive part (before -O-)
            parts = new_name.split('-O-')
            if len(parts) > 0:
                desc_part = parts[0].replace(f'P{paper_num}-', '')
                # Create various old name patterns
                old_variants = [
                    new_name.replace(f'P{paper_num}-', '').replace('-O-', '_').replace('-', '_'),
                    new_name.replace(f'P{paper_num}-', 'P{paper_num}_').replace('-O-', '_').replace('-', '_'),
                    desc_part.replace('-', '_'),
                    img_file.stem.replace(f'P{paper_num}-', '').replace('-', '_'),
                ]
                
                new_path = f"../assets/{paper_dir.name}/{new_name}"
                for old_var in old_variants:
                    mapping[(paper_num, old_var)] = new_path
    
    # Also check charts
    charts_dir = ASSETS_PATH / "charts"
    if charts_dir.exists():
        for img_file in charts_dir.glob("*.png"):
            new_name = img_file.name
            match = re.match(r'P(\d+)-', new_name)
            if match:
                paper_num = int(match.group(1))
                desc_part = new_name.split('-O-')[0].replace(f'P{paper_num}-', '')
                old_variants = [
                    desc_part.replace('-', '_'),
                    new_name.replace(f'P{paper_num}-', '').replace('-', '_'),
                ]
                new_path = f"../assets/charts/{new_name}"
                for old_var in old_variants:
                    mapping[(paper_num, old_var)] = new_path
    
    return mapping

def fix_paper_paths(paper_path, paper_num, image_mapping):
    """Fix image paths in a paper"""
    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Pattern: ![alt](../../../../Assets/Images/logos papers/P1_Logos_Principle/image.png)
    pattern = re.compile(
        r'!\[([^\]]*)\]\(\.\./\.\./\.\./\.\./Assets/Images/logos papers/P(\d+)_[^/]+/([^)]+\.png)\)',
        re.IGNORECASE
    )
    
    def replace_match(match):
        alt = match.group(1)
        pnum = int(match.group(2))
        old_img = match.group(3)
        
        # Try to find in mapping
        img_base = old_img.replace('.png', '').replace('_', '-').lower()
        
        # Check direct match
        key = (pnum, old_img.replace('.png', ''))
        if key in image_mapping:
            return f"![{alt}]({image_mapping[key]})"
        
        # Try variations
        for (p, old), new_path in image_mapping.items():
            if p == pnum and (old.lower() in old_img.lower() or old_img.lower() in old.lower()):
                return f"![{alt}]({new_path})"
        
        # Fallback: use paper folder structure
        return f"![{alt}](../assets/P{pnum}/{old_img})"
    
    content = pattern.sub(replace_match, content)
    
    if content != original:
        with open(paper_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

if __name__ == "__main__":
    if not BASE_PATH.exists():
        print(f"Path {BASE_PATH} doesn't exist")
        exit(1)
    
    print("Building image mapping...")
    image_mapping = build_image_mapping()
    print(f"Found {len(image_mapping)} image mappings")
    
    print(f"\nProcessing papers in: {BASE_PATH}")
    papers_updated = []
    
    for paper_file in BASE_PATH.glob("Paper-*-FINAL.md"):
        match = re.search(r'Paper-(\d+)-', paper_file.name)
        if not match:
            continue
        
        paper_num = int(match.group(1))
        if fix_paper_paths(paper_file, paper_num, image_mapping):
            papers_updated.append(paper_file.name)
            print(f"  ✓ Updated: {paper_file.name}")
    
    print(f"\n{'='*60}")
    print(f"Updated {len(papers_updated)} papers")
    print(f"{'='*60}")

