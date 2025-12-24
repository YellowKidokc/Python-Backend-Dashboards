#!/usr/bin/env python3
"""
Comprehensive audit of Logos Papers images before adding more.
Checks for:
1. Existing image references in papers
2. Correct/incorrect paths
3. Duplicates within papers
4. Proposes systematic renaming: P1-01, P1-02, etc.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Paths
PAPERS_DIR = Path(r"D:\THEOPHYSICS_MASTER\06_Publication\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL")
IMAGES_DIR = Path(r"D:\THEOPHYSICS_MASTER\Assets\Images\logos papers")

def scan_paper_for_images(paper_path):
    """Extract all image references from a paper."""
    content = paper_path.read_text(encoding='utf-8')
    # Match markdown image syntax: ![caption](path)
    pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
    matches = re.findall(pattern, content)
    return [(caption, path) for caption, path in matches]

def check_image_path_validity(image_path, paper_path):
    """Check if an image path from a paper actually exists."""
    # Convert relative path to absolute
    if image_path.startswith('http'):
        return "EXTERNAL_URL", None
    
    # Try to resolve relative to paper location
    absolute_path = (paper_path.parent / image_path).resolve()
    
    if absolute_path.exists():
        return "VALID", absolute_path
    else:
        return "BROKEN", absolute_path

def get_paper_number(paper_name):
    """Extract paper number from filename."""
    match = re.search(r'Paper-(\d+)', paper_name)
    if match:
        return int(match.group(1))
    return None

def audit_all_papers():
    """Main audit function."""
    print("="*80)
    print("LOGOS PAPERS IMAGE AUDIT")
    print("="*80)
    
    all_findings = {}
    
    # Scan each paper
    papers = sorted(PAPERS_DIR.glob("Paper-*.md"))
    
    for paper in papers:
        paper_num = get_paper_number(paper.name)
        if not paper_num:
            continue
            
        print(f"\n{'='*80}")
        print(f"PAPER {paper_num:02d}: {paper.name}")
        print(f"{'='*80}")
        
        images = scan_paper_for_images(paper)
        
        if not images:
            print("  ⚠️  NO IMAGES FOUND")
            all_findings[paper_num] = {
                'paper': paper.name,
                'images_count': 0,
                'images': [],
                'broken': [],
                'duplicates': []
            }
            continue
        
        print(f"  Found {len(images)} image reference(s)")
        
        valid_count = 0
        broken_count = 0
        seen_paths = defaultdict(int)
        broken_images = []
        
        for i, (caption, img_path) in enumerate(images, 1):
            status, abs_path = check_image_path_validity(img_path, paper)
            seen_paths[img_path] += 1
            
            if status == "VALID":
                valid_count += 1
                print(f"  ✓ Image {i:02d}: {Path(img_path).name[:50]}")
            elif status == "BROKEN":
                broken_count += 1
                broken_images.append((img_path, caption))
                print(f"  ✗ BROKEN {i:02d}: {img_path}")
            elif status == "EXTERNAL_URL":
                print(f"  🌐 External {i:02d}: {img_path[:60]}...")
        
        # Check for duplicates
        duplicates = [path for path, count in seen_paths.items() if count > 1]
        if duplicates:
            print(f"\n  ⚠️  DUPLICATES FOUND:")
            for dup in duplicates:
                print(f"     - {dup} (used {seen_paths[dup]} times)")
        
        all_findings[paper_num] = {
            'paper': paper.name,
            'images_count': len(images),
            'valid_count': valid_count,
            'broken_count': broken_count,
            'images': images,
            'broken': broken_images,
            'duplicates': duplicates
        }
        
        print(f"\n  Summary: {valid_count} valid, {broken_count} broken")
    
    return all_findings

def propose_image_renaming():
    """Propose systematic renaming of all images: P1-01.png, P1-02.png, etc."""
    print("\n" + "="*80)
    print("PROPOSED IMAGE RENAMING SCHEME")
    print("="*80)
    print("\nCurrent naming is inconsistent. Proposing systematic naming:\n")
    
    folder_map = {
        "P1_Logos_Principle": 1,
        "P2_Quantum_Bridge": 2,
        "P3_Algorithm_Reality": 3,
        "P4_Hard_Problem": 4,
        "P5_Soul_Observer": 5,
        "P6_Physics_Principalities": 6,
        "P7_Grace_Function": 7,
        "P8_Stretched_Heavens": 8,
        "P9_Moral_Universe": 9,
        "P10_Creatio_ex_Silico": 10,
        "P11_Validation_Protocols": 11,
        "P12_Decalogue": 12,
    }
    
    rename_plan = {}
    
    for folder_name, paper_num in folder_map.items():
        folder_path = IMAGES_DIR / folder_name
        if not folder_path.exists():
            continue
        
        images = sorted(folder_path.glob("*.png"))
        if not images:
            continue
        
        print(f"\nPaper {paper_num:02d} ({folder_name}): {len(images)} images")
        
        for i, img in enumerate(images, 1):
            new_name = f"P{paper_num:02d}-{i:02d}.png"
            if img.name != new_name:
                print(f"  {img.name:50s} → {new_name}")
                rename_plan[str(img)] = new_name
            else:
                print(f"  ✓ {img.name} (already correct)")
    
    return rename_plan

def check_available_images():
    """List all available images that are NOT yet in papers."""
    print("\n" + "="*80)
    print("AVAILABLE IMAGES NOT YET IN PAPERS")
    print("="*80)
    
    folder_map = {
        "P1_Logos_Principle": 1,
        "P2_Quantum_Bridge": 2,
        "P3_Algorithm_Reality": 3,
        "P4_Hard_Problem": 4,
        "P5_Soul_Observer": 5,
        "P6_Physics_Principalities": 6,
        "P7_Grace_Function": 7,
        "P8_Stretched_Heavens": 8,
        "P9_Moral_Universe": 9,
        "P10_Creatio_ex_Silico": 10,
        "P11_Validation_Protocols": 11,
        "P12_Decalogue": 12,
    }
    
    for folder_name, paper_num in folder_map.items():
        folder_path = IMAGES_DIR / folder_name
        if not folder_path.exists():
            continue
        
        images = list(folder_path.glob("*.png"))
        print(f"\nPaper {paper_num:02d}: {len(images)} images available in {folder_name}/")
        for img in sorted(images):
            print(f"  - {img.name}")

def main():
    print("\n" + "🔍 " * 40)
    print("STARTING COMPREHENSIVE LOGOS PAPERS IMAGE AUDIT")
    print("🔍 " * 40 + "\n")
    
    # Step 1: Audit papers
    findings = audit_all_papers()
    
    # Step 2: Check available images
    check_available_images()
    
    # Step 3: Propose renaming
    rename_plan = propose_image_renaming()
    
    # Summary
    print("\n" + "="*80)
    print("AUDIT SUMMARY")
    print("="*80)
    
    total_images = sum(f['images_count'] for f in findings.values())
    total_broken = sum(f['broken_count'] for f in findings.values())
    papers_with_images = len([f for f in findings.values() if f['images_count'] > 0])
    papers_without_images = len([f for f in findings.values() if f['images_count'] == 0])
    
    print(f"\n📊 Papers scanned: {len(findings)}")
    print(f"📸 Papers with images: {papers_with_images}")
    print(f"📭 Papers without images: {papers_without_images}")
    print(f"🖼️  Total image references: {total_images}")
    print(f"✓  Valid images: {total_images - total_broken}")
    print(f"✗  Broken links: {total_broken}")
    print(f"🔄 Images needing rename: {len(rename_plan)}")
    
    if total_broken > 0:
        print(f"\n⚠️  WARNING: {total_broken} broken image links need fixing!")
    
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Review broken image links above")
    print("2. Decide if you want to rename images to P01-01, P01-02 format")
    print("3. Then we can add remaining images to papers systematically")
    print("="*80)

if __name__ == "__main__":
    main()

