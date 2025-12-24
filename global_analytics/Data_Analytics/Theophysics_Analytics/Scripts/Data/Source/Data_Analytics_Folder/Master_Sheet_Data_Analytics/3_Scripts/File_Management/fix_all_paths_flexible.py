#!/usr/bin/env python3
"""
Flexibly fix all image paths in FINAL papers
Handles various old path formats and maps to organized structure
"""
import re
from pathlib import Path

BASE_PATH = Path("D:/THEOPHYSICS_MASTER/03_PUBLICATIONS/Logos_Papers/COMPLETE_LOGOS_PAPERS_FINAL")
ASSETS_BASE = Path("COMPLETE_LOGOS_PAPERS_FINAL/assets")

def get_organized_images():
    """Get all organized image names by paper"""
    images = {}
    charts = {}
    
    # Regular images
    for paper_dir in ASSETS_BASE.iterdir():
        if not paper_dir.is_dir() or paper_dir.name == "charts":
            continue
        match = re.match(r'P(\d+)', paper_dir.name)
        if match:
            paper_num = int(match.group(1))
            images[paper_num] = [f.name for f in paper_dir.glob("*.png")]
    
    # Charts
    charts_dir = ASSETS_BASE / "charts"
    if charts_dir.exists():
        for img_file in charts_dir.glob("*.png"):
            match = re.match(r'P(\d+)-', img_file.name)
            if match:
                paper_num = int(match.group(1))
                if paper_num not in charts:
                    charts[paper_num] = []
                charts[paper_num].append(img_file.name)
    
    return images, charts

def find_matching_image(old_name, paper_num, organized_images, is_chart=False):
    """Find matching organized image name"""
    old_clean = old_name.lower().replace('.png', '').replace('_', '-').replace(' ', '-')
    
    # Check if it's a chart
    if is_chart:
        for chart_name in organized_images.get(paper_num, []):
            chart_clean = chart_name.lower().replace('.png', '').replace('_', '-')
            if old_clean in chart_clean or chart_clean in old_clean:
                return f"../assets/charts/{chart_name}"
        return None
    
    # Check regular images
    for img_name in organized_images.get(paper_num, []):
        img_clean = img_name.lower().replace('.png', '').replace('_', '-')
        # Check if key parts match
        if old_clean in img_clean or img_clean in old_clean:
            return f"../assets/P{paper_num}/{img_name}"
    
    return None

def fix_paper(paper_path, paper_num, organized_images, organized_charts):
    """Fix all image paths in a paper"""
    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Pattern 1: Old format ../../../../Assets/Images/logos papers/P1_Logos_Principle/image.png
    def replace_old_path(match):
        alt = match.group(1)
        pnum = int(match.group(2))
        old_img = match.group(3)
        
        # Check if it's a chart (look for chart keywords)
        is_chart = any(kw in old_img.lower() for kw in ['chart', 'timeline', 'epoch', 'hubble'])
        
        if is_chart:
            new_path = find_matching_image(old_img, pnum, organized_charts, is_chart=True)
        else:
            new_path = find_matching_image(old_img, pnum, organized_images, is_chart=False)
        
        if new_path:
            return f"![{alt}]({new_path})"
        else:
            # Fallback
            folder = "charts" if is_chart else f"P{pnum}"
            return f"![{alt}](../assets/{folder}/{old_img})"
    
    pattern1 = re.compile(
        r'!\[([^\]]*)\]\(\.\./\.\./\.\./\.\./Assets/Images/logos papers/P(\d+)_[^/]+/([^)]+\.png)\)',
        re.IGNORECASE
    )
    content = pattern1.sub(replace_old_path, content)
    
    # Pattern 2: Already using ../assets but wrong name
    def replace_wrong_name(match):
        alt = match.group(1)
        folder = match.group(2)
        old_img = match.group(3)
        
        match_pnum = re.match(r'P(\d+)', folder)
        if not match_pnum:
            return match.group(0)
        
        pnum = int(match_pnum.group(1))
        is_chart = folder == "charts"
        
        if is_chart:
            new_path = find_matching_image(old_img, pnum, organized_charts, is_chart=True)
        else:
            new_path = find_matching_image(old_img, pnum, organized_images, is_chart=False)
        
        if new_path:
            return f"![{alt}]({new_path})"
        else:
            return match.group(0)  # Keep as is if no match
    
    pattern2 = re.compile(
        r'!\[([^\]]*)\]\(\.\./assets/(P\d+|charts)/([^)]+\.png)\)',
        re.IGNORECASE
    )
    content = pattern2.sub(replace_wrong_name, content)
    
    if content != original:
        with open(paper_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

if __name__ == "__main__":
    if not BASE_PATH.exists():
        print(f"Path {BASE_PATH} doesn't exist")
        exit(1)
    
    print("Loading organized images...")
    organized_images, organized_charts = get_organized_images()
    print(f"Found images for papers: {sorted(organized_images.keys())}")
    print(f"Found charts for papers: {sorted(organized_charts.keys())}")
    
    print(f"\nProcessing papers in: {BASE_PATH}\n")
    papers_updated = []
    
    for paper_file in sorted(BASE_PATH.glob("Paper-*-FINAL.md")):
        match = re.search(r'Paper-(\d+)-', paper_file.name)
        if not match:
            continue
        
        paper_num = int(match.group(1))
        if fix_paper(paper_file, paper_num, organized_images, organized_charts):
            papers_updated.append(paper_file.name)
            print(f"  ✓ Updated: {paper_file.name}")
    
    print(f"\n{'='*60}")
    print(f"Updated {len(papers_updated)} papers")
    print(f"{'='*60}")

