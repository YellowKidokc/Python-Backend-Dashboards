#!/usr/bin/env python3
"""
Fix all image paths in FINAL papers to use the organized structure
Updates paths from old format to new organized format
"""
import re
from pathlib import Path

# Check both locations
LOCATIONS = [
    Path("COMPLETE_LOGOS_PAPERS_FINAL"),
    Path("D:/THEOPHYSICS_MASTER/03_PUBLICATIONS/Logos_Papers/COMPLETE_LOGOS_PAPERS_FINAL"),
]

# Mapping of old paths to new paths
def fix_image_paths(content, paper_num):
    """Fix image paths in content"""
    # Pattern 1: Old format ../../../../Assets/Images/logos papers/P1_Logos_Principle/image.png
    pattern1 = re.compile(
        r'!\[([^\]]*)\]\(\.\./\.\./\.\./\.\./Assets/Images/logos papers/P(\d+)_[^/]+/([^)]+\.png)\)',
        re.IGNORECASE
    )
    
    def replace1(match):
        alt = match.group(1)
        pnum = match.group(2)
        img = match.group(3)
        # Convert old image name to new format
        # Remove P1_, P2_ prefixes, clean up name
        clean_name = img.replace(f'P{pnum}_', '').replace('P{pnum}', '').replace('_', '-').lower()
        # Try to match with organized names
        new_path = f"../assets/P{pnum}/{img}"
        # Actually, we need to use the organized naming
        # For now, use the paper folder structure
        return f"![{alt}](../assets/P{pnum}/{img})"
    
    content = pattern1.sub(replace1, content)
    
    # Pattern 2: Any path with Assets/Images/logos papers
    pattern2 = re.compile(
        r'!\[([^\]]*)\]\([^)]*Assets/Images/logos papers/P(\d+)_[^/]+/([^)]+\.png)\)',
        re.IGNORECASE
    )
    
    def replace2(match):
        alt = match.group(1)
        pnum = match.group(2)
        img = match.group(3)
        return f"![{alt}](../assets/P{pnum}/{img})"
    
    content = pattern2.sub(replace2, content)
    
    return content

# Process all FINAL papers
for base_path in LOCATIONS:
    if not base_path.exists():
        print(f"Skipping {base_path} - doesn't exist")
        continue
    
    print(f"\nProcessing: {base_path}")
    papers_updated = []
    
    for paper_file in base_path.glob("Paper-*-FINAL.md"):
        paper_num = None
        match = re.search(r'Paper-(\d+)-', paper_file.name)
        if match:
            paper_num = int(match.group(1))
        
        with open(paper_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        content = fix_image_paths(content, paper_num)
        
        if content != original:
            with open(paper_file, 'w', encoding='utf-8') as f:
                f.write(content)
            papers_updated.append(paper_file.name)
            print(f"  ✓ Updated: {paper_file.name}")
    
    print(f"Updated {len(papers_updated)} papers in {base_path}")

print("\n" + "="*60)
print("Path fixing complete!")

