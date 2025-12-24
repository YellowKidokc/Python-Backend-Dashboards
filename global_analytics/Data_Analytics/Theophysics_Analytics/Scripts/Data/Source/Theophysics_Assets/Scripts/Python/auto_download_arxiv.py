#!/usr/bin/env python3
"""
Automatic arXiv Paper Downloader - No prompts
Downloads papers automatically from PAPERS_TO_DOWNLOAD.csv
"""

import os
import sys
import csv
import urllib.request
import time
from pathlib import Path

def install_if_needed(package):
    """Install package if not available"""
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        os.system(f"{sys.executable} -m pip install {package} -q")

# Install required packages
install_if_needed('arxiv')

import arxiv

def search_arxiv(query, max_results=3):
    """Search arXiv for papers"""
    try:
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []
        for result in search.results():
            results.append({
                'title': result.title,
                'authors': [a.name for a in result.authors],
                'pdf_url': result.pdf_url,
                'summary': result.summary[:200] + '...'
            })
        return results
    except Exception as e:
        return []

def download_pdf(url, output_path):
    """Download PDF from URL"""
    try:
        urllib.request.urlretrieve(url, output_path)
        return True
    except Exception as e:
        return False

def sanitize_filename(filename):
    """Clean filename for saving"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename[:100]

def main():
    """Main execution"""
    print("\n" + "="*70)
    print("Automatic arXiv Paper Downloader")
    print("="*70 + "\n")
    
    base_dir = r"d:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL"
    csv_path = os.path.join(base_dir, "PAPERS_TO_DOWNLOAD.csv")
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found")
        return
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        papers = list(reader)
    
    print(f"Found {len(papers)} papers to search")
    print("Searching arXiv...\n")
    
    # Group by paper number
    papers_by_folder = {}
    for paper in papers:
        paper_num = paper['Paper']
        if paper_num not in papers_by_folder:
            papers_by_folder[paper_num] = []
        papers_by_folder[paper_num].append(paper)
    
    stats = {'downloaded': 0, 'existing': 0, 'not_found': 0, 'failed': 0}
    not_found_list = []
    
    # Process each paper folder
    for paper_num, paper_list in sorted(papers_by_folder.items()):
        print(f"\n{paper_num} - Processing {len(paper_list)} papers")
        print("-" * 70)
        
        # Find paper folder
        paper_folders = list(Path(base_dir).glob(f"{paper_num}-*"))
        if not paper_folders:
            continue
        
        paper_folder = paper_folders[0]
        pdf_dir = paper_folder / "References" / "PDFs"
        pdf_dir.mkdir(parents=True, exist_ok=True)
        
        # Download each paper
        for paper in paper_list:
            author = paper['Author']
            theory = paper['Theory']
            query = f"{author} {theory}"
            
            print(f"  {theory[:50]:<50} ", end='', flush=True)
            
            # Create filename
            safe_author = sanitize_filename(author.split()[-1] if author else 'Unknown')
            safe_theory = sanitize_filename(theory)
            filename = f"{safe_author}_{safe_theory}.pdf"
            output_path = pdf_dir / filename
            
            # Check if already exists
            if output_path.exists():
                print("✓ EXISTS")
                stats['existing'] += 1
                continue
            
            # Search arXiv
            results = search_arxiv(query, max_results=1)
            
            if results:
                result = results[0]
                if download_pdf(result['pdf_url'], output_path):
                    print("✓ DOWNLOADED")
                    stats['downloaded'] += 1
                else:
                    print("✗ FAILED")
                    stats['failed'] += 1
                    not_found_list.append((paper_num, author, theory))
                time.sleep(1)  # Rate limit
            else:
                print("⚠ NOT ON ARXIV")
                stats['not_found'] += 1
                not_found_list.append((paper_num, author, theory))
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"✓ Downloaded:       {stats['downloaded']}")
    print(f"✓ Already existed:  {stats['existing']}")
    print(f"⚠ Not on arXiv:     {stats['not_found']}")
    print(f"✗ Failed:           {stats['failed']}")
    print(f"{'='*70}")
    
    # Save not found list
    if not_found_list:
        not_found_path = os.path.join(base_dir, "MANUAL_DOWNLOAD_NEEDED.csv")
        with open(not_found_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Paper', 'Author', 'Theory', 'Search_Query'])
            for paper_num, author, theory in not_found_list:
                writer.writerow([paper_num, author, theory, f"{author} {theory}"])
        
        print(f"\n✓ Created MANUAL_DOWNLOAD_NEEDED.csv ({len(not_found_list)} papers)")
        print("  Use Google Scholar to find these papers manually")
    
    print("\n✓ Download complete!")
    print("\nNext step: python convert_papers_to_markdown.py\n")

if __name__ == "__main__":
    main()
