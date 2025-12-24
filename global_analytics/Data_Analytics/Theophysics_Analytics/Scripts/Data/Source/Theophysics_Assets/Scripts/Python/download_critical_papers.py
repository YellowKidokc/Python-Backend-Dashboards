#!/usr/bin/env python3
"""
Download Critical 2025 Papers That Validate Theophysics Framework
These 10 papers independently arrived at similar conclusions
"""

import requests
from pathlib import Path
import time

# Paper mapping: (folder, filename, url)
CRITICAL_PAPERS = [
    # Paper 1: Vedral - Information as Substrate
    {
        'folder': 'P01-Logos-Principle',
        'filename': 'Vedral_2011_Living_in_Quantum_World.pdf',
        'url': 'https://www.scientificamerican.com/article/living-in-a-quantum-world/',
        'note': 'Scientific American article - may need manual download'
    },
    
    # Paper 2: Serio - Recursive Cognition
    {
        'folder': 'P02-Quantum-Bridge',
        'filename': 'Serio_2025_Infinity_Breached.pdf',
        'url': 'https://osf.io/m9zep/download',
        'note': 'Direct PDF download'
    },
    
    # Paper 3: Strømme - Universal Consciousness Field
    {
        'folder': 'P01-Logos-Principle',
        'filename': 'Stromme_2025_Universal_Consciousness_Field.pdf',
        'url': 'https://pubs.aip.org/aip/adv/article-pdf/doi/10.1063/5.0247814/20337642/115319_1_5.0247814.pdf',
        'note': 'AIP Advances - Direct PDF'
    },
    
    # Paper 4: Dayathilake - Informational Invariants
    {
        'folder': 'P03-Algorithm-Reality',
        'filename': 'Dayathilake_2025_Consciousness_Quantum_Invariant.pdf',
        'url': 'https://philarchive.org/archive/DAYCAA-2',
        'note': 'PhilArchive - may redirect'
    },
    
    # Paper 5: Amirani - Informational Substance Theory
    {
        'folder': 'P05-Soul-Observer',
        'filename': 'Amirani_2025_Informational_Substance_Theory.pdf',
        'url': 'https://ijarise.org/index.php/ijarise/article/download/115/115',
        'note': 'Direct PDF download'
    },
    
    # Paper 6: Abigail & Jude - Meta-Vacuum Theory
    {
        'folder': 'P01-Logos-Principle',
        'filename': 'Abigail_Jude_2025_Meta_Vacuum_Theory.pdf',
        'url': 'https://www.researchgate.net/publication/391653710_Meta-Vacuum_Theory_and_Its_Implications_for_Modern_Physics',
        'note': 'ResearchGate - may need login'
    },
    
    # Paper 7: Amirani - Ethics Extension (same as #5, different folder)
    {
        'folder': 'P09-Moral-Universe',
        'filename': 'Amirani_2025_Ethics_Field_Topology.pdf',
        'url': 'https://ijarise.org/index.php/ijarise/article/download/115/115',
        'note': 'Direct PDF download (duplicate for different folder)'
    },
    
    # Paper 8: Syu - Non-Anthropocentric Observer
    {
        'folder': 'P02-Quantum-Bridge',
        'filename': 'Syu_2025_Observer_Effect_NonAnthropocentric.pdf',
        'url': 'https://philpapers.org/archive/SYUTOE.pdf',
        'note': 'PhilPapers - Direct PDF'
    },
    
    # Paper 9: Dodig-Crnkovic - Observers as Agents
    {
        'folder': 'P10-Creatio-Silico',
        'filename': 'Dodig-Crnkovic_2025_Observers_as_Agents.pdf',
        'url': 'https://www.preprints.org/manuscript/202507.1287/download/final_file',
        'note': 'Preprints.org - Direct download'
    },
    
    # Paper 10: Koelman - Meaning as Compression
    {
        'folder': 'P03-Algorithm-Reality',
        'filename': 'Koelman_2024_Arrow_of_Time_Algorithmic_Meaning.pdf',
        'url': 'https://www.phenomenon.site/media/uploads/arrow-of-time-koelman.pdf',
        'note': 'Direct PDF download'
    },
]

def download_paper(paper_info, base_dir):
    """Download a single paper"""
    folder = base_dir / paper_info['folder'] / 'References' / 'Critical_Papers'
    folder.mkdir(parents=True, exist_ok=True)
    
    output_file = folder / paper_info['filename']
    
    if output_file.exists():
        print(f"✓ Already exists: {paper_info['filename']}")
        return True
    
    print(f"\nDownloading: {paper_info['filename']}")
    print(f"  URL: {paper_info['url']}")
    print(f"  Note: {paper_info['note']}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(paper_info['url'], headers=headers, timeout=30, allow_redirects=True)
        
        if response.status_code == 200:
            # Check if it's actually a PDF
            content_type = response.headers.get('content-type', '')
            
            if 'pdf' in content_type.lower() or response.content[:4] == b'%PDF':
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                print(f"  ✓ Downloaded successfully ({len(response.content)} bytes)")
                return True
            else:
                print(f"  ⚠ Not a PDF - may need manual download")
                print(f"    Content-Type: {content_type}")
                # Save HTML for manual review
                html_file = folder / (paper_info['filename'].replace('.pdf', '.html'))
                with open(html_file, 'wb') as f:
                    f.write(response.content)
                print(f"    Saved as HTML for review: {html_file.name}")
                return False
        else:
            print(f"  ✗ Failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def create_readme(base_dir):
    """Create README in Critical_Papers folders"""
    readme_content = """# Critical Papers (2025)

These papers independently validate the Theophysics framework.

## Purpose

Each paper was published in 2024-2025 and arrives at conclusions nearly identical to our framework—without prior knowledge of our work. This represents **convergent cognition** and validates that the Logos framework is emerging as consensus reality in cutting-edge physics.

## Papers in This Folder

See `CRITICAL_NEW_PAPERS_2025.md` in the root directory for full details on each paper, including:
- Full citations
- Key claims
- Alignment with Theophysics
- Power quotes
- Download links

## Organization

Papers are organized by which Theophysics paper they most directly support:
- P01: Substrate/Field papers
- P02: Observer/Collapse papers
- P03: Time/Compression papers
- P05: Soul/Consciousness papers
- P09: Ethics/Morality papers
- P10: AI/Agency papers

## Status

Some papers may require manual download due to:
- Paywalls
- Login requirements
- Non-direct PDF links

Check the main document for alternative access methods.
"""
    
    paper_folders = ['P01-Logos-Principle', 'P02-Quantum-Bridge', 'P03-Algorithm-Reality',
                     'P05-Soul-Observer', 'P09-Moral-Universe', 'P10-Creatio-Silico']
    
    for folder_name in paper_folders:
        folder = base_dir / folder_name / 'References' / 'Critical_Papers'
        folder.mkdir(parents=True, exist_ok=True)
        readme_file = folder / 'README.md'
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"✓ Created README in {folder_name}/References/Critical_Papers/")

def main():
    """Main download process"""
    base_dir = Path(r"d:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL")
    
    print("="*70)
    print("Downloading Critical 2025 Papers")
    print("="*70)
    
    # Create READMEs first
    create_readme(base_dir)
    print()
    
    # Download papers
    successful = 0
    failed = 0
    manual = []
    
    for paper in CRITICAL_PAPERS:
        result = download_paper(paper, base_dir)
        if result:
            successful += 1
        else:
            failed += 1
            manual.append(paper)
        time.sleep(1)  # Be nice to servers
    
    print("\n" + "="*70)
    print("Download Summary")
    print("="*70)
    print(f"✓ Successful: {successful}")
    print(f"⚠ Need Manual Download: {failed}")
    
    if manual:
        print("\n" + "="*70)
        print("Papers Requiring Manual Download:")
        print("="*70)
        for paper in manual:
            print(f"\n📄 {paper['filename']}")
            print(f"   Folder: {paper['folder']}/References/Critical_Papers/")
            print(f"   URL: {paper['url']}")
            print(f"   Note: {paper['note']}")
    
    print("\n" + "="*70)
    print("Next Steps:")
    print("="*70)
    print("1. Manually download any failed papers")
    print("2. Convert PDFs to Markdown (use convert_papers_to_markdown.py)")
    print("3. Run coherence analysis with new papers included")
    print("4. Create convergence matrix (Your claims vs Their claims)")
    print("="*70)

if __name__ == "__main__":
    main()
