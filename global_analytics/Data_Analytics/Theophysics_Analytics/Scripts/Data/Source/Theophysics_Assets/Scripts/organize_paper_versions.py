#!/usr/bin/env python3
"""
Find and organize different versions of Logos Papers from Documents folder.
Compares files to identify significantly different versions.
"""

import os
import shutil
import hashlib
from pathlib import Path
from collections import defaultdict
import difflib

documents_dir = r'C:\Users\Yellowkid\Documents'
output_base = r'C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers\VERSION_REPOSITORY'

# Paper patterns to search for
paper_patterns = [
    r'Paper\s*1.*[Ll]ogos.*[Pp]rinciple',
    r'Paper\s*2.*[Qq]uantum.*[Bb]ridge',
    r'Paper\s*3.*[Aa]lgorithm.*[Rr]eality',
    r'Paper\s*4.*[Hh]ard.*[Pp]roblem|Paper\s*4.*[Ss]yzygy',
    r'Paper\s*5.*[Ss]oul.*[Oo]bserver',
    r'Paper\s*6.*[Pp]rincipalities',
    r'Paper\s*7.*[Gg]race.*[Ff]unction',
    r'Paper\s*8.*[Ss]tretched.*[Hh]eavens',
    r'Paper\s*9.*[Mm]oral.*[Uu]niverse',
    r'Paper\s*10.*[Cc]reatio.*[Ss]ilico|Paper\s*10.*[Aa][Ii]',
    r'Paper\s*11.*[Vv]alidation|Paper\s*11.*[Pp]rotocols',
    r'Paper\s*12.*[Dd]ecalogue|Paper\s*12.*[Mm]aster.*[Ee]quation'
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

def find_paper_files(root_dir):
    """Find all potential Logos Papers files."""
    paper_files = defaultdict(list)
    
    for root, dirs, files in os.walk(root_dir):
        # Skip certain directories
        skip_dirs = ['node_modules', '.git', '__pycache__', '.obsidian']
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if not file.endswith('.md'):
                continue
            
            filepath = os.path.join(root, file)
            filename_lower = file.lower()
            
            # Check if it matches any paper pattern
            for i, pattern in enumerate(paper_patterns, 1):
                import re
                if re.search(pattern, filename_lower) or re.search(pattern, file):
                    paper_files[i].append(filepath)
                    break
    
    return paper_files

def organize_versions(paper_files):
    """Organize files by paper number and identify unique versions."""
    organized = {}
    
    for paper_num, files in paper_files.items():
        print(f"\n{'='*60}")
        print(f"PAPER {paper_num:02d}: Found {len(files)} potential files")
        print(f"{'='*60}")
        
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
        
        print(f"  Unique versions: {len(unique_versions)}")
        for i, version in enumerate(unique_versions, 1):
            print(f"    Version {i}: {os.path.basename(version['representative'])}")
            print(f"      Size: {version['size']:,} bytes")
            print(f"      Path: {version['representative']}")
            print(f"      Duplicates: {version['count'] - 1}")
        
        organized[paper_num] = unique_versions
    
    return organized

def copy_to_repository(organized):
    """Copy unique versions to organized repository structure."""
    os.makedirs(output_base, exist_ok=True)
    
    for paper_num, versions in organized.items():
        paper_dir = os.path.join(output_base, f"Paper-{paper_num:02d}")
        os.makedirs(paper_dir, exist_ok=True)
        
        for i, version in enumerate(versions, 1):
            source = version['representative']
            filename = os.path.basename(source)
            
            # Create unique filename
            version_dir = os.path.join(paper_dir, f"Version-{i:02d}")
            os.makedirs(version_dir, exist_ok=True)
            
            dest = os.path.join(version_dir, filename)
            
            # Add metadata file
            metadata = f"""# Version {i} Metadata

**Source:** {source}
**Size:** {version['size']:,} bytes
**Hash:** {version['hash']}
**Duplicate Count:** {version['count']}

## All Source Paths:
"""
            for path in version['all_paths']:
                metadata += f"- {path}\n"
            
            with open(os.path.join(version_dir, "VERSION_METADATA.md"), 'w', encoding='utf-8') as f:
                f.write(metadata)
            
            try:
                shutil.copy2(source, dest)
                print(f"  Copied: {filename} -> {version_dir}")
            except Exception as e:
                print(f"  ERROR copying {filename}: {e}")

def compare_versions(organized):
    """Compare versions to identify significantly different ones."""
    print(f"\n{'='*60}")
    print("VERSION COMPARISON ANALYSIS")
    print(f"{'='*60}")
    
    for paper_num, versions in organized.items():
        if len(versions) < 2:
            continue
        
        print(f"\nPaper {paper_num:02d}: Comparing {len(versions)} versions...")
        
        # Read all versions
        version_contents = []
        for version in versions:
            try:
                with open(version['representative'], 'r', encoding='utf-8', errors='ignore') as f:
                    version_contents.append(f.read())
            except:
                version_contents.append("")
        
        # Compare each pair
        for i in range(len(versions)):
            for j in range(i+1, len(versions)):
                similarity = calculate_similarity(version_contents[i], version_contents[j])
                print(f"  Version {i+1} vs Version {j+1}: {similarity:.1%} similar")
                
                if similarity < 0.8:  # Less than 80% similar
                    print(f"    *** SIGNIFICANTLY DIFFERENT - Worth comparing! ***")

def main():
    print("Searching for Logos Papers files in Documents folder...")
    print(f"Search directory: {documents_dir}")
    
    paper_files = find_paper_files(documents_dir)
    
    print(f"\nFound files for {len(paper_files)} papers")
    for paper_num, files in sorted(paper_files.items()):
        print(f"  Paper {paper_num:02d}: {len(files)} files")
    
    print("\nAnalyzing and organizing versions...")
    organized = organize_versions(paper_files)
    
    print("\nComparing versions for significant differences...")
    compare_versions(organized)
    
    print(f"\nCopying unique versions to repository...")
    print(f"Repository location: {output_base}")
    copy_to_repository(organized)
    
    print(f"\n{'='*60}")
    print("COMPLETE!")
    print(f"{'='*60}")
    print(f"\nRepository created at: {output_base}")
    print("\nNext steps:")
    print("1. Review VERSION_METADATA.md files in each version folder")
    print("2. Compare significantly different versions (similarity < 80%)")
    print("3. Identify any content that should be merged into final versions")

if __name__ == '__main__':
    main()

