#!/usr/bin/env python3
"""
Find all paper versions in Documents vault, keep top 5, and create comparison document.
"""

import os
import shutil
import hashlib
from pathlib import Path
from collections import defaultdict
import difflib
import re

documents_dir = r'C:\Users\Yellowkid\Documents'
output_dir = r'C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers\TOP5_COMPARISON'

# Paper patterns - expanded to catch all variations
paper_patterns = [
    (1, r'[Pp]aper\s*1|P01|Logos\s*[Pp]rinciple'),
    (2, r'[Pp]aper\s*2|P02|[Qq]uantum\s*[Bb]ridge'),
    (3, r'[Pp]aper\s*3|P03|[Aa]lgorithm\s*[Oo]f\s*[Rr]eality'),
    (4, r'[Pp]aper\s*4|P04|[Hh]ard\s*[Pp]roblem|[Ss]yzygy'),
    (5, r'[Pp]aper\s*5|P05|[Ss]oul\s*[Oo]bserver'),
    (6, r'[Pp]aper\s*6|P06|[Pp]rincipalities'),
    (7, r'[Pp]aper\s*7|P07|[Gg]race\s*[Ff]unction'),
    (8, r'[Pp]aper\s*8|P08|[Ss]tretched\s*[Hh]eavens'),
    (9, r'[Pp]aper\s*9|P09|[Mm]oral\s*[Uu]niverse'),
    (10, r'[Pp]aper\s*10|P10|[Cc]reatio|AI\s*[Cc]onsciousness'),
    (11, r'[Pp]aper\s*11|P11|[Vv]alidation|[Pp]rotocols'),
    (12, r'[Pp]aper\s*12|P12|[Dd]ecalogue|[Mm]aster\s*[Ee]quation'),
]

def get_file_hash(filepath):
    """Get MD5 hash of file content."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    except:
        return None

def get_file_size(filepath):
    """Get file size in bytes."""
    try:
        return os.path.getsize(filepath)
    except:
        return 0

def calculate_similarity(content1, content2):
    """Calculate similarity ratio between two file contents."""
    return difflib.SequenceMatcher(None, content1, content2).ratio()

def find_all_paper_files(root_dir):
    """Find all potential paper files."""
    paper_files = defaultdict(list)
    
    print(f"Searching in: {root_dir}")
    print("This may take a few minutes...\n")
    
    file_count = 0
    for root, dirs, files in os.walk(root_dir):
        # Skip certain directories
        skip_dirs = ['node_modules', '.git', '__pycache__', '.obsidian', 'VERSION_REPOSITORY', 'TOP5_COMPARISON']
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if not file.endswith('.md'):
                continue
            
            filepath = os.path.join(root, file)
            filename_lower = file.lower()
            file_content_lower = ""
            
            # Try to read first 500 chars for better matching
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content_lower = f.read(500).lower()
            except:
                pass
            
            # Check if it matches any paper pattern
            for paper_num, pattern in paper_patterns:
                if re.search(pattern, filename_lower) or re.search(pattern, file_content_lower):
                    paper_files[paper_num].append(filepath)
                    file_count += 1
                    if file_count % 100 == 0:
                        print(f"  Found {file_count} potential paper files...")
                    break
    
    return paper_files

def organize_and_select_top5(paper_files):
    """Organize files by paper and select top 5 versions."""
    organized = {}
    
    for paper_num, files in sorted(paper_files.items()):
        print(f"\n{'='*70}")
        print(f"PAPER {paper_num:02d}: Found {len(files)} potential files")
        print(f"{'='*70}")
        
        # Group by hash (exact duplicates)
        hash_groups = defaultdict(list)
        for filepath in files:
            file_hash = get_file_hash(filepath)
            if file_hash:
                hash_groups[file_hash].append(filepath)
        
        # Identify unique versions
        unique_versions = []
        seen_hashes = set()
        
        for file_hash, filepaths in hash_groups.items():
            if file_hash in seen_hashes:
                continue
            
            # Use the shortest path as representative
            representative = min(filepaths, key=len)
            size = get_file_size(representative)
            
            unique_versions.append({
                'hash': file_hash,
                'representative': representative,
                'all_paths': filepaths,
                'size': size,
                'count': len(filepaths)
            })
            
            seen_hashes.add(file_hash)
        
        # Sort by size (larger files might be more complete)
        unique_versions.sort(key=lambda x: x['size'], reverse=True)
        
        # Select top 5
        top5 = unique_versions[:5]
        
        print(f"  Unique versions: {len(unique_versions)}")
        print(f"  Selected TOP 5 for comparison:")
        for i, version in enumerate(top5, 1):
            print(f"    Version {i}: {os.path.basename(version['representative'])}")
            print(f"      Size: {version['size']:,} bytes")
            print(f"      Path: {version['representative']}")
            print(f"      Duplicates: {version['count'] - 1}")
        
        organized[paper_num] = top5
    
    return organized

def create_comparison_document(organized):
    """Create a single comparison document with all top 5 versions."""
    os.makedirs(output_dir, exist_ok=True)
    
    comparison_file = os.path.join(output_dir, "ALL_PAPERS_TOP5_COMPARISON.md")
    
    with open(comparison_file, 'w', encoding='utf-8') as f:
        f.write("# ALL LOGOS PAPERS - TOP 5 VERSIONS COMPARISON\n\n")
        f.write("This document contains the top 5 versions of each paper for easy comparison.\n")
        f.write("Versions are sorted by file size (largest first, likely most complete).\n\n")
        f.write("="*80 + "\n\n")
        
        for paper_num in sorted(organized.keys()):
            versions = organized[paper_num]
            
            f.write(f"\n{'='*80}\n")
            f.write(f"# PAPER {paper_num:02d} - TOP 5 VERSIONS\n")
            f.write(f"{'='*80}\n\n")
            
            for i, version in enumerate(versions, 1):
                f.write(f"\n## VERSION {i} (Size: {version['size']:,} bytes)\n\n")
                f.write(f"**Source:** `{version['representative']}`\n\n")
                f.write(f"**Hash:** {version['hash']}\n\n")
                f.write(f"**Duplicate Count:** {version['count'] - 1}\n\n")
                f.write(f"**All Source Paths:**\n")
                for path in version['all_paths']:
                    f.write(f"- `{path}`\n")
                f.write(f"\n")
                f.write(f"{'-'*80}\n\n")
                
                # Read and include file content
                try:
                    with open(version['representative'], 'r', encoding='utf-8', errors='ignore') as content_file:
                        content = content_file.read()
                        # Limit to first 50,000 chars to keep file manageable
                        if len(content) > 50000:
                            content = content[:50000] + "\n\n... [CONTENT TRUNCATED - See source file for full content] ...\n"
                        f.write("```markdown\n")
                        f.write(content)
                        f.write("\n```\n\n")
                except Exception as e:
                    f.write(f"**ERROR reading file:** {e}\n\n")
                
                f.write(f"\n{'='*80}\n\n")
            
            # Add similarity comparison
            if len(versions) > 1:
                f.write(f"\n### SIMILARITY COMPARISON\n\n")
                f.write("| Version 1 | Version 2 | Similarity |\n")
                f.write("|-----------|-----------|------------|\n")
                
                # Read all versions for comparison
                version_contents = []
                for version in versions:
                    try:
                        with open(version['representative'], 'r', encoding='utf-8', errors='ignore') as vf:
                            version_contents.append(vf.read())
                    except:
                        version_contents.append("")
                
                for i in range(len(versions)):
                    for j in range(i+1, len(versions)):
                        similarity = calculate_similarity(version_contents[i], version_contents[j])
                        f.write(f"| Version {i+1} | Version {j+1} | {similarity:.1%} |\n")
                        if similarity < 0.8:
                            f.write(f"  *** SIGNIFICANTLY DIFFERENT - Worth comparing! ***\n")
                
                f.write(f"\n")
    
    print(f"\n{'='*70}")
    print("COMPARISON DOCUMENT CREATED!")
    print(f"{'='*70}")
    print(f"\nLocation: {comparison_file}")
    print(f"\nThis document contains:")
    print(f"  - Top 5 versions of each paper")
    print(f"  - Full content of each version")
    print(f"  - Similarity comparisons")
    print(f"  - Source paths for all versions")
    print(f"\nYou can now review this document to:")
    print(f"  - Compare different versions")
    print(f"  - Identify missing content")
    print(f"  - See how papers evolved")
    print(f"  - Find content that should be merged")

def copy_top5_to_folder(organized):
    """Copy top 5 versions to organized folder structure."""
    top5_dir = os.path.join(output_dir, "TOP5_VERSIONS")
    os.makedirs(top5_dir, exist_ok=True)
    
    for paper_num, versions in organized.items():
        paper_dir = os.path.join(top5_dir, f"Paper-{paper_num:02d}")
        os.makedirs(paper_dir, exist_ok=True)
        
        for i, version in enumerate(versions, 1):
            source = version['representative']
            filename = os.path.basename(source)
            
            # Create unique filename
            version_dir = os.path.join(paper_dir, f"Version-{i:02d}")
            os.makedirs(version_dir, exist_ok=True)
            
            dest = os.path.join(version_dir, filename)
            
            try:
                shutil.copy2(source, dest)
                print(f"  Copied: {filename} -> {version_dir}")
            except Exception as e:
                print(f"  ERROR copying {filename}: {e}")

def main():
    print("="*70)
    print("FINDING ALL PAPER VERSIONS IN DOCUMENTS VAULT")
    print("="*70)
    print(f"\nSearch directory: {documents_dir}")
    
    paper_files = find_all_paper_files(documents_dir)
    
    print(f"\n{'='*70}")
    print(f"FOUND FILES FOR {len(paper_files)} PAPERS")
    print(f"{'='*70}")
    for paper_num, files in sorted(paper_files.items()):
        print(f"  Paper {paper_num:02d}: {len(files)} files")
    
    print("\n" + "="*70)
    print("ORGANIZING AND SELECTING TOP 5 VERSIONS...")
    print("="*70)
    organized = organize_and_select_top5(paper_files)
    
    print("\n" + "="*70)
    print("CREATING COMPARISON DOCUMENT...")
    print("="*70)
    create_comparison_document(organized)
    
    print("\n" + "="*70)
    print("COPYING TOP 5 VERSIONS TO FOLDER...")
    print("="*70)
    copy_top5_to_folder(organized)
    
    print("\n" + "="*70)
    print("COMPLETE!")
    print("="*70)
    print(f"\nOutput location: {output_dir}")
    print("\nFiles created:")
    print("  1. ALL_PAPERS_TOP5_COMPARISON.md - Single document with all versions")
    print("  2. TOP5_VERSIONS/ - Folder with organized top 5 versions")

if __name__ == '__main__':
    main()

