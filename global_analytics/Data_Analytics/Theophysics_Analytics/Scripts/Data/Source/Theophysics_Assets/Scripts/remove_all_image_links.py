#!/usr/bin/env python3
"""
Remove all image references from all FINAL papers
"""
import re
from pathlib import Path

FINAL_PAPERS = Path("COMPLETE_LOGOS_PAPERS_FINAL")

# Pattern to match image references and their figure captions
# Matches: ![alt](../assets/.../image.png) followed by optional figure caption
image_pattern = re.compile(
    r'!\[[^\]]*\]\([^)]+assets[^)]+\.png\)\s*\n\s*\n\*\*Figure[^\n]*\n\s*\n[^\n]*\n\s*\n\*[^\n]*\n',
    re.MULTILINE | re.DOTALL
)

# Also match standalone image references without captions
simple_image_pattern = re.compile(
    r'!\[[^\]]*\]\([^)]+assets[^)]+\.png\)\s*\n',
    re.MULTILINE
)

def remove_images_from_file(file_path):
    """Remove all image references from a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remove image references with captions
    content = image_pattern.sub('', content)
    
    # Remove standalone image references
    content = simple_image_pattern.sub('', content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Process all FINAL papers
papers_updated = []
for paper_file in FINAL_PAPERS.glob("Paper-*-FINAL.md"):
    if remove_images_from_file(paper_file):
        papers_updated.append(paper_file.name)
        print(f"✓ Cleaned: {paper_file.name}")

print(f"\n{'='*60}")
print(f"Cleaned {len(papers_updated)} papers")
print(f"{'='*60}")

