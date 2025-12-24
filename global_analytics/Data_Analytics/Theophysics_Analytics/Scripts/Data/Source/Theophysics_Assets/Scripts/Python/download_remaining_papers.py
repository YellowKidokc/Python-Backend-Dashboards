#!/usr/bin/env python3
"""
Alternative download methods for the 4 remaining critical papers
"""

import requests
from pathlib import Path
import time

def try_stromme_alternatives():
    """Try alternative URLs for Strømme paper"""
    base_dir = Path(r"d:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL")
    folder = base_dir / "P01-Logos-Principle" / "References" / "Critical_Papers"
    folder.mkdir(parents=True, exist_ok=True)
    
    output_file = folder / "Stromme_2025_Universal_Consciousness_Field.pdf"
    
    # Try different URL patterns
    urls = [
        # Direct DOI
        "https://doi.org/10.1063/5.0247814",
        # Alternative AIP URL
        "https://pubs.aip.org/aip/adv/article-pdf/15/11/115319/20337642/115319_1_online.pdf",
        # Another pattern
        "https://aip.scitation.org/doi/pdf/10.1063/5.0247814",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/pdf,*/*',
    }
    
    print("\n" + "="*70)
    print("Trying Alternative URLs for Strømme Paper")
    print("="*70)
    
    for i, url in enumerate(urls, 1):
        print(f"\nAttempt {i}: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
            print(f"  Status: {response.status_code}")
            print(f"  Content-Type: {response.headers.get('content-type', 'unknown')}")
            
            if response.status_code == 200 and (
                'pdf' in response.headers.get('content-type', '').lower() or
                response.content[:4] == b'%PDF'
            ):
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                print(f"  ✓ SUCCESS! Downloaded {len(response.content)} bytes")
                return True
            else:
                print(f"  ✗ Not a valid PDF")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        time.sleep(2)
    
    return False

def try_koelman_alternatives():
    """Try alternative URLs for Koelman paper"""
    base_dir = Path(r"d:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL")
    folder = base_dir / "P03-Algorithm-Reality" / "References" / "Critical_Papers"
    folder.mkdir(parents=True, exist_ok=True)
    
    output_file = folder / "Koelman_2024_Arrow_of_Time_Algorithmic_Meaning.pdf"
    
    # Try different URL patterns
    urls = [
        # Original
        "https://www.phenomenon.site/media/uploads/arrow-of-time-koelman.pdf",
        # Try without www
        "http://phenomenon.site/media/uploads/arrow-of-time-koelman.pdf",
        # Try direct IP if DNS issue
        "https://phenomenon.site/media/uploads/arrow-of-time-koelman.pdf",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/pdf,*/*',
        'Referer': 'https://www.phenomenon.site/',
    }
    
    print("\n" + "="*70)
    print("Trying Alternative URLs for Koelman Paper")
    print("="*70)
    
    for i, url in enumerate(urls, 1):
        print(f"\nAttempt {i}: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
            print(f"  Status: {response.status_code}")
            print(f"  Content-Type: {response.headers.get('content-type', 'unknown')}")
            print(f"  Content-Length: {len(response.content)}")
            
            if response.status_code == 200:
                # Check if PDF
                if response.content[:4] == b'%PDF':
                    with open(output_file, 'wb') as f:
                        f.write(response.content)
                    print(f"  ✓ SUCCESS! Downloaded {len(response.content)} bytes")
                    return True
                else:
                    print(f"  ✗ Not a PDF (first 20 bytes: {response.content[:20]})")
            else:
                print(f"  ✗ Failed with status {response.status_code}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        time.sleep(2)
    
    return False

def create_placeholder_files():
    """Create placeholder files with download instructions"""
    base_dir = Path(r"d:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL")
    
    placeholders = [
        {
            'folder': 'P01-Logos-Principle',
            'filename': 'DOWNLOAD_Vedral.txt',
            'content': '''MANUAL DOWNLOAD REQUIRED: Vedral - Living in a Quantum World

This paper requires manual download.

BEST OPTION:
1. Go to: https://www.scientificamerican.com/article/living-in-a-quantum-world/
2. Or search Google Scholar: "Vedral Living in a Quantum World"
3. Or use the book "Decoding Reality" by Vlatko Vedral (2010)

SAVE AS: Vedral_2011_Living_in_Quantum_World.pdf

KEY QUOTES TO EXTRACT:
- "Information is physical. Every atom, every particle, every force field — ultimately, these are carriers of information."
- "The entire universe can be seen as a quantum computer — processing itself into being."

CITATION:
Vedral, V. (2011). Living in a quantum world. Scientific American, 304(6), 38-43.
'''
        },
        {
            'folder': 'P01-Logos-Principle',
            'filename': 'DOWNLOAD_Abigail_Jude.txt',
            'content': '''MANUAL DOWNLOAD REQUIRED: Abigail & Jude - Meta-Vacuum Theory

This paper requires ResearchGate account (free).

STEPS:
1. Go to: https://www.researchgate.net/publication/391653710
2. Create free account or log in
3. Click "Request full-text" or "Download"
4. Authors usually respond within 24 hours

SAVE AS: Abigail_Jude_2025_Meta_Vacuum_Theory.pdf

KEY CONCEPT:
"A recursive event horizon within the meta-vacuum initiates dimensional expression."

CITATION:
Abigail, E., & Jude, L. (2025). Meta-Vacuum Theory and Its Implications for Modern Physics. 
ResearchGate Preprint. https://www.researchgate.net/publication/391653710
'''
        }
    ]
    
    for placeholder in placeholders:
        folder = base_dir / placeholder['folder'] / 'References' / 'Critical_Papers'
        folder.mkdir(parents=True, exist_ok=True)
        file_path = folder / placeholder['filename']
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(placeholder['content'])
        
        print(f"✓ Created placeholder: {placeholder['filename']}")

def main():
    """Try alternative download methods"""
    print("="*70)
    print("Attempting Alternative Downloads for Remaining 4 Papers")
    print("="*70)
    
    success_count = 0
    
    # Try Strømme
    if try_stromme_alternatives():
        success_count += 1
    
    # Try Koelman
    if try_koelman_alternatives():
        success_count += 1
    
    # Create placeholders for the other 2
    print("\n" + "="*70)
    print("Creating Placeholder Files for Manual Download")
    print("="*70 + "\n")
    create_placeholder_files()
    
    print("\n" + "="*70)
    print("Summary")
    print("="*70)
    print(f"✓ Successfully downloaded: {success_count}/2 attempted")
    print(f"⚠ Still need manual download: {4 - success_count}")
    print("\nSee MANUAL_DOWNLOAD_GUIDE.md for detailed instructions")
    print("="*70)

if __name__ == "__main__":
    main()
