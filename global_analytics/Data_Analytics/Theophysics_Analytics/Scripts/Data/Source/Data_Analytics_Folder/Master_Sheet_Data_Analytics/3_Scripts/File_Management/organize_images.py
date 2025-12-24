#!/usr/bin/env python3
"""
Script to organize images for FINAL papers with proper naming convention:
P1-[proper-name]-O-X.png where X is the number out of total images
Charts go in a charts folder
"""

import os
import re
import shutil
from pathlib import Path
from collections import defaultdict

# Base paths
BASE_DIR = Path(".")
ASSETS_SRC = BASE_DIR / "assets"
ASSETS_DST = BASE_DIR / "COMPLETE_LOGOS_PAPERS_FINAL" / "assets"
FINAL_PAPERS = BASE_DIR / "COMPLETE_LOGOS_PAPERS_FINAL"

# Paper mapping
PAPER_MAPPING = {
    1: "P1_Logos_Principle",
    2: "P2_Quantum_Bridge",
    3: "P3_Syzygy_Principle",
    4: "P4_Hard_Problem",
    5: "P5_Soul_Observer",  # May need to check actual folder
    6: "P6_Physics_Principalities",
    7: "P7_Grace_Function",
    8: "P8_Stretched_Heavens",
    9: "P9_Moral_Universe",
    10: "P10_Creatio_Silico",
    11: "P11_Protocols_Validation",
    12: "P12_Decalogue_Cosmos",
}

# Chart keywords - images with these in name go to charts folder
CHART_KEYWORDS = [
    "timeline", "tension", "clock", "measurement_methods", 
    "what_is_a_meter", "what_is_a_second", "prediction",
    "epoch", "complete_story", "information_density"
]

def is_chart(filename):
    """Check if image should go in charts folder"""
    filename_lower = filename.lower()
    return any(keyword in filename_lower for keyword in CHART_KEYWORDS)

def extract_image_refs_from_paper(paper_path):
    """Extract all image references from a paper"""
    images = []
    if not paper_path.exists():
        return images
    
    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Find all image references: ![alt](../assets/.../image.png)
        pattern = r'!\[.*?\]\(\.\./assets/([^/]+)/([^)]+\.png)\)'
        matches = re.findall(pattern, content)
        for folder, img in matches:
            images.append((folder, img))
    return images

def get_paper_number_from_filename(filename):
    """Extract paper number from filename like Paper-01-The-Logos-Principle-FINAL.md"""
    match = re.search(r'Paper-(\d+)-', filename)
    if match:
        return int(match.group(1))
    return None

def clean_name(name):
    """Clean image name for use in new filename"""
    # Remove common prefixes and clean up
    name = name.replace('.png', '')
    # Remove P1_, P2_ etc if present
    name = re.sub(r'^P\d+[-_\s]+', '', name)
    # Replace underscores and spaces with hyphens
    name = name.replace('_', '-').replace(' ', '-')
    # Remove multiple hyphens
    name = re.sub(r'-+', '-', name)
    # Remove leading/trailing hyphens
    name = name.strip('-')
    return name

def organize_images():
    """Main function to organize all images"""
    
    # Create destination structure
    ASSETS_DST.mkdir(parents=True, exist_ok=True)
    charts_dir = ASSETS_DST / "charts"
    charts_dir.mkdir(exist_ok=True)
    
    # Collect all images by paper
    paper_images = defaultdict(list)
    
    # Process each FINAL paper
    for paper_file in FINAL_PAPERS.glob("Paper-*-FINAL.md"):
        paper_num = get_paper_number_from_filename(paper_file.name)
        if not paper_num:
            continue
        
        print(f"\nProcessing Paper {paper_num}: {paper_file.name}")
        images = extract_image_refs_from_paper(paper_file)
        
        for folder, img in images:
            paper_images[paper_num].append((folder, img))
            print(f"  Found: {folder}/{img}")
    
    # Organize images
    for paper_num, images in sorted(paper_images.items()):
        print(f"\n{'='*60}")
        print(f"Organizing Paper {paper_num} ({len(images)} images)")
        print(f"{'='*60}")
        
        # Create paper folder
        paper_folder = ASSETS_DST / f"P{paper_num}"
        paper_folder.mkdir(exist_ok=True)
        
        # Separate charts from regular images
        regular_images = []
        chart_images = []
        
        for folder, img in images:
            if is_chart(img):
                chart_images.append((folder, img))
            else:
                regular_images.append((folder, img))
        
        # Copy regular images
        for idx, (folder, img) in enumerate(regular_images, 1):
            src_path = ASSETS_SRC / folder / img
            if not src_path.exists():
                # Try alternative locations and name variations
                alt_paths = [
                    ASSETS_SRC / PAPER_MAPPING.get(paper_num, folder) / img,
                    ASSETS_SRC / "P7_ Images" / img,  # Some images might be here
                ]
                # Try name variations (with/without underscores, hyphens, etc.)
                base_name = img.replace('_', '-').replace(' ', '-')
                alt_names = [
                    img.replace('P1observer', 'P1-11_observer').replace('P1_12', 'P1-12'),
                    img.replace('P1_13', 'P1-13'),
                    base_name,
                    img.replace('-', '_'),
                    img.replace('_', '-'),
                ]
                for alt_name in alt_names:
                    alt_paths.extend([
                        ASSETS_SRC / folder / alt_name,
                        ASSETS_SRC / PAPER_MAPPING.get(paper_num, folder) / alt_name,
                        ASSETS_SRC / "P7_ Images" / alt_name,
                    ])
                
                found = False
                for alt in alt_paths:
                    if alt.exists():
                        src_path = alt
                        found = True
                        break
                if not found:
                    print(f"  WARNING: {img} not found in {folder} (tried variations)")
                    continue
            
            clean_img_name = clean_name(img)
            total = len(regular_images)
            new_name = f"P{paper_num}-{clean_img_name}-O-{idx}-of-{total}.png"
            dst_path = paper_folder / new_name
            
            shutil.copy2(src_path, dst_path)
            print(f"  Copied: {img} -> {new_name}")
        
        # Copy chart images
        for idx, (folder, img) in enumerate(chart_images, 1):
            src_path = ASSETS_SRC / folder / img
            if not src_path.exists():
                # Try alternative locations and name variations
                alt_paths = [
                    ASSETS_SRC / PAPER_MAPPING.get(paper_num, folder) / img,
                    ASSETS_SRC / "P7_ Images" / img,
                ]
                # Try name variations
                base_name = img.replace('_', '-').replace(' ', '-')
                alt_names = [
                    base_name,
                    img.replace('-', '_'),
                    img.replace('_', '-'),
                ]
                for alt_name in alt_names:
                    alt_paths.extend([
                        ASSETS_SRC / folder / alt_name,
                        ASSETS_SRC / PAPER_MAPPING.get(paper_num, folder) / alt_name,
                        ASSETS_SRC / "P7_ Images" / alt_name,
                    ])
                
                found = False
                for alt in alt_paths:
                    if alt.exists():
                        src_path = alt
                        found = True
                        break
                if not found:
                    print(f"  WARNING: Chart {img} not found in {folder} (tried variations)")
                    continue
            
            clean_img_name = clean_name(img)
            total = len(chart_images)
            new_name = f"P{paper_num}-{clean_img_name}-O-{idx}-of-{total}.png"
            dst_path = charts_dir / new_name
            
            shutil.copy2(src_path, dst_path)
            print(f"  Copied chart: {img} -> charts/{new_name}")
    
    print(f"\n{'='*60}")
    print("Organization complete!")
    print(f"{'='*60}")

if __name__ == "__main__":
    organize_images()

