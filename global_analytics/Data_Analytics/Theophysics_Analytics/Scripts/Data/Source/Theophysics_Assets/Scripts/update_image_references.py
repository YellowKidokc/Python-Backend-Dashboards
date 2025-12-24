#!/usr/bin/env python3
"""
Script to update image references in FINAL papers to point to new organized structure
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Base paths
FINAL_PAPERS = Path("COMPLETE_LOGOS_PAPERS_FINAL")
ASSETS_DST = FINAL_PAPERS / "assets"

# Mapping of old image paths to new organized structure
# This will be built dynamically based on what was organized

def get_paper_number_from_filename(filename):
    """Extract paper number from filename"""
    match = re.search(r'Paper-(\d+)-', filename)
    if match:
        return int(match.group(1))
    return None

def clean_name(name):
    """Clean image name for matching"""
    name = name.replace('.png', '')
    name = re.sub(r'^P\d+[-_\s]+', '', name)
    name = name.replace('_', '-').replace(' ', '-')
    name = re.sub(r'-+', '-', name)
    name = name.strip('-')
    return name.lower()

def build_image_mapping():
    """Build mapping from old paths to new paths"""
    mapping = {}
    
    # Scan organized assets
    for paper_dir in ASSETS_DST.iterdir():
        if not paper_dir.is_dir() or paper_dir.name == "charts":
            continue
        
        paper_num = None
        match = re.match(r'P(\d+)', paper_dir.name)
        if match:
            paper_num = int(match.group(1))
        
        for img_file in paper_dir.glob("*.png"):
            # Extract original name from new filename
            # Format: P1-[name]-O-X-of-Y.png
            new_name = img_file.name
            # Try to extract the original name part
            parts = new_name.replace('.png', '').split('-O-')
            if len(parts) > 0:
                name_part = parts[0].replace(f'P{paper_num}-', '')
                # Map various old formats to new format
                old_variants = [
                    f"P{paper_num}_{name_part.replace('-', '_')}.png",
                    f"P{paper_num}-{name_part}.png",
                    f"{name_part.replace('-', '_')}.png",
                    f"{name_part}.png",
                ]
                new_path = f"../assets/{paper_dir.name}/{new_name}"
                for old_var in old_variants:
                    mapping[(paper_num, old_var)] = new_path
    
    # Also handle charts
    charts_dir = ASSETS_DST / "charts"
    if charts_dir.exists():
        for img_file in charts_dir.glob("*.png"):
            new_name = img_file.name
            parts = new_name.replace('.png', '').split('-O-')
            if len(parts) > 0:
                # Extract paper number from filename like P3-01-hubble-tension-O-1-of-6.png
                match = re.match(r'P(\d+)-', new_name)
                if match:
                    paper_num = int(match.group(1))
                    name_part = parts[0].replace(f'P{paper_num}-', '')
                    old_variants = [
                        f"{name_part.replace('-', '_')}.png",
                        f"{name_part}.png",
                    ]
                    new_path = f"../assets/charts/{new_name}"
                    for old_var in old_variants:
                        mapping[(paper_num, old_var)] = new_path
    
    return mapping

def update_paper_references(paper_path, paper_num, image_mapping):
    """Update image references in a paper"""
    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    updated = False
    
    # Find all image references: ![alt](../assets/folder/image.png)
    pattern = r'!\[([^\]]*)\]\(\.\./assets/([^/]+)/([^)]+\.png)\)'
    
    def replace_match(match):
        nonlocal updated
        alt_text = match.group(1)
        folder = match.group(2)
        img = match.group(3)
        
        # Try to find new path
        # Check direct mapping
        key = (paper_num, img)
        if key in image_mapping:
            new_path = image_mapping[key]
            updated = True
            return f"![{alt_text}]({new_path})"
        
        # Try with cleaned name
        clean_img = clean_name(img)
        for (pnum, old_img), new_path in image_mapping.items():
            if pnum == paper_num and clean_name(old_img) == clean_img:
                updated = True
                return f"![{alt_text}]({new_path})"
        
        # If not found, keep original but update path structure if folder matches paper
        if folder.startswith(f"P{paper_num}"):
            # Try to find in organized structure
            paper_folder = ASSETS_DST / f"P{paper_num}"
            charts_folder = ASSETS_DST / "charts"
            
            # Check if image exists in new structure
            for org_img in paper_folder.glob("*.png"):
                if clean_name(org_img.name) == clean_img or img in org_img.name:
                    new_path = f"../assets/P{paper_num}/{org_img.name}"
                    updated = True
                    return f"![{alt_text}]({new_path})"
            
            for org_img in charts_folder.glob(f"P{paper_num}-*.png"):
                if clean_name(org_img.name) == clean_img or img in org_img.name:
                    new_path = f"../assets/charts/{org_img.name}"
                    updated = True
                    return f"![{alt_text}]({new_path})"
        
        # Keep original if no match found
        return match.group(0)
    
    new_content = re.sub(pattern, replace_match, content)
    
    if updated:
        with open(paper_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    """Main function"""
    print("Building image mapping...")
    image_mapping = build_image_mapping()
    print(f"Found {len(image_mapping)} image mappings")
    
    print("\nUpdating paper references...")
    updated_count = 0
    
    for paper_file in FINAL_PAPERS.glob("Paper-*-FINAL.md"):
        paper_num = get_paper_number_from_filename(paper_file.name)
        if not paper_num:
            continue
        
        print(f"Processing Paper {paper_num}: {paper_file.name}")
        if update_paper_references(paper_file, paper_num, image_mapping):
            updated_count += 1
            print(f"  ✓ Updated")
        else:
            print(f"  - No changes needed")
    
    print(f"\n{'='*60}")
    print(f"Updated {updated_count} papers")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

