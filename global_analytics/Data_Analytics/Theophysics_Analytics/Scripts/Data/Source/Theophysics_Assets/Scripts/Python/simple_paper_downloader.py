#!/usr/bin/env python3
"""
Simple Paper Downloader - No browser automation needed
Uses arxiv API and direct downloads where possible
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
        os.system(f"{sys.executable} -m pip install {package}")

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
        print(f"    Error searching arXiv: {e}")
        return []

def download_pdf(url, output_path):
    """Download PDF from URL"""
    try:
        print(f"    Downloading from: {url}")
        urllib.request.urlretrieve(url, output_path)
        return True
    except Exception as e:
        print(f"    Download failed: {e}")
        return False

def sanitize_filename(filename):
    """Clean filename for saving"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename[:100]  # Limit length

def download_papers_from_csv(csv_path, base_dir):
    """Download papers from CSV using arXiv"""
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found")
        return
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        papers = list(reader)
    
    print(f"\nFound {len(papers)} papers in list")
    print("Searching arXiv for available papers...\n")
    
    # Group by paper number
    papers_by_folder = {}
    for paper in papers:
        paper_num = paper['Paper']
        if paper_num not in papers_by_folder:
            papers_by_folder[paper_num] = []
        papers_by_folder[paper_num].append(paper)
    
    stats = {'downloaded': 0, 'not_found': 0, 'failed': 0}
    
    # Process each paper folder
    for paper_num, paper_list in sorted(papers_by_folder.items()):
        print(f"\n{'='*70}")
        print(f"{paper_num} - Processing {len(paper_list)} papers")
        print(f"{'='*70}\n")
        
        # Find paper folder
        paper_folders = list(Path(base_dir).glob(f"{paper_num}-*"))
        if not paper_folders:
            print(f"Warning: No folder found for {paper_num}")
            continue
        
        paper_folder = paper_folders[0]
        pdf_dir = paper_folder / "References" / "PDFs"
        pdf_dir.mkdir(parents=True, exist_ok=True)
        
        # Download each paper
        for i, paper in enumerate(paper_list, 1):
            author = paper['Author']
            theory = paper['Theory']
            query = f"{author} {theory}"
            
            print(f"[{i}/{len(paper_list)}] Searching: {theory}")
            print(f"    Author: {author}")
            
            # Search arXiv
            results = search_arxiv(query, max_results=1)
            
            if results:
                result = results[0]
                print(f"    ✓ Found: {result['title'][:60]}...")
                
                # Create filename
                safe_author = sanitize_filename(author.split()[-1] if author else 'Unknown')
                safe_theory = sanitize_filename(theory)
                filename = f"{safe_author}_{safe_theory}.pdf"
                output_path = pdf_dir / filename
                
                # Download if not exists
                if output_path.exists():
                    print(f"    ⊘ Already exists: {filename}")
                    stats['downloaded'] += 1
                else:
                    if download_pdf(result['pdf_url'], output_path):
                        print(f"    ✓ Downloaded: {filename}")
                        stats['downloaded'] += 1
                    else:
                        print(f"    ✗ Download failed")
                        stats['failed'] += 1
                
                time.sleep(1)  # Be nice to arXiv
            else:
                print(f"    ⚠ Not found on arXiv (may need manual download)")
                stats['not_found'] += 1
            
            print()
    
    # Summary
    print(f"\n{'='*70}")
    print("Download Summary")
    print(f"{'='*70}")
    print(f"✓ Downloaded/Existing: {stats['downloaded']}")
    print(f"⚠ Not found on arXiv:  {stats['not_found']}")
    print(f"✗ Failed downloads:    {stats['failed']}")
    print(f"\nTotal papers:          {len(papers)}")
    print(f"{'='*70}\n")

def create_manual_download_list(csv_path, base_dir):
    """Create a list of papers not found for manual download"""
    # This would track which papers weren't found
    # and create a separate CSV for manual downloading
    pass

def main():
    """Main execution"""
    print("\n" + "="*70)
    print("Simple Academic Paper Downloader")
    print("Searches arXiv for physics/quantum papers")
    print("="*70 + "\n")
    
    base_dir = r"d:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL"
    csv_path = os.path.join(base_dir, "PAPERS_TO_DOWNLOAD.csv")
    
    print("Note:")
    print("- This searches arXiv (free physics/CS papers)")
    print("- Not all papers will be on arXiv")
    print("- You'll need to manually download paywalled papers")
    print("- Rate limited to be respectful to arXiv servers\n")
    
    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    download_papers_from_csv(csv_path, base_dir)
    
    print("\nNext steps:")
    print("1. Check P##-Paper-Name/References/PDFs/ for downloaded papers")
    print("2. For papers not found, use Google Scholar manually:")
    print("   - Open PAPERS_TO_DOWNLOAD.csv")
    print("   - Search Google Scholar for missing papers")
    print("   - Look for [PDF] links")
    print("3. Run: python convert_papers_to_markdown.py")
    print()

if __name__ == "__main__":
    main()
