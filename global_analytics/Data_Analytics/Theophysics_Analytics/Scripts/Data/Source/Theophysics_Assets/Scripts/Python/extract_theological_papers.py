#!/usr/bin/env python3
"""
Extract Theological Companion Papers from Theological.md
and place them in their respective P## folders
"""

import re
from pathlib import Path

def extract_theological_papers():
    """Extract T-P01 through T-P12 from Theological.md"""
    
    base_dir = Path(r"d:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL")
    theological_file = base_dir / "Theological.md"
    
    # Read the entire file
    with open(theological_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find theological papers
    # Looking for "# T-P##:" headers
    pattern = r'(# T-P(\d+):.*?)(?=# T-P\d+:|$)'
    
    matches = re.findall(pattern, content, re.DOTALL)
    
    print(f"Found {len(matches)} theological papers\n")
    
    for match in matches:
        paper_content = match[0].strip()
        paper_num = match[1].zfill(2)  # Pad with zero (01, 02, etc.)
        
        # Find the paper title
        title_match = re.search(r'# T-P\d+: (.+)', paper_content)
        if title_match:
            title = title_match.group(1).strip()
            # Clean title for filename
            clean_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '-')
            
            # Find corresponding P## folder
            paper_folders = list(base_dir.glob(f"P{paper_num}-*"))
            
            if paper_folders:
                paper_folder = paper_folders[0]
                output_file = paper_folder / f"T-P{paper_num}-{clean_title}.md"
                
                # Write the theological paper
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(paper_content)
                
                print(f"✓ Created: {output_file.name}")
                print(f"  in {paper_folder.name}")
            else:
                print(f"⚠ No folder found for P{paper_num}")
        
        print()
    
    print("="*70)
    print("Extraction Complete!")
    print("="*70)

if __name__ == "__main__":
    extract_theological_papers()
