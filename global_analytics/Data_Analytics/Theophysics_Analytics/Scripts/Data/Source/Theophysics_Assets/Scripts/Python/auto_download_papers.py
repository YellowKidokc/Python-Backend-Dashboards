#!/usr/bin/env python3
"""
Automated Paper Downloader using PyPaperBot
Downloads papers from PAPERS_TO_DOWNLOAD.csv
"""

import os
import sys
import csv
import subprocess
from pathlib import Path

def install_pypaperbot():
    """Install PyPaperBot if not already installed"""
    try:
        import PyPaperBot
        print("✓ PyPaperBot already installed")
    except ImportError:
        print("Installing PyPaperBot...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPaperBot"])
        print("✓ PyPaperBot installed")

def download_papers_from_csv(csv_path, base_dir):
    """Download papers listed in CSV file"""
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found")
        return
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        papers = list(reader)
    
    print(f"\nFound {len(papers)} papers to download\n")
    
    # Group by paper number
    papers_by_folder = {}
    for paper in papers:
        paper_num = paper['Paper']
        if paper_num not in papers_by_folder:
            papers_by_folder[paper_num] = []
        papers_by_folder[paper_num].append(paper)
    
    # Download for each paper folder
    for paper_num, paper_list in sorted(papers_by_folder.items()):
        print(f"\n{'='*60}")
        print(f"Processing {paper_num} ({len(paper_list)} papers)")
        print(f"{'='*60}\n")
        
        # Find the paper folder
        paper_folders = list(Path(base_dir).glob(f"{paper_num}-*"))
        if not paper_folders:
            print(f"Warning: No folder found for {paper_num}")
            continue
        
        paper_folder = paper_folders[0]
        pdf_dir = paper_folder / "References" / "PDFs"
        pdf_dir.mkdir(parents=True, exist_ok=True)
        
        # Download each paper
        for i, paper in enumerate(paper_list, 1):
            query = paper['SearchQuery']
            author = paper['Author']
            theory = paper['Theory']
            
            print(f"\n[{i}/{len(paper_list)}] Downloading: {theory}")
            print(f"    Author: {author}")
            print(f"    Query: {query}")
            
            # Try PyPaperBot
            try:
                cmd = [
                    sys.executable, "-m", "PyPaperBot",
                    "--query", query,
                    "--dwn-dir", str(pdf_dir),
                    "--scholar-pages", "1",
                    "--restrict", "0"
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    print(f"    ✓ Downloaded successfully")
                else:
                    print(f"    ⚠ Download failed or not found")
                    
            except subprocess.TimeoutExpired:
                print(f"    ⚠ Timeout - skipping")
            except Exception as e:
                print(f"    ✗ Error: {str(e)}")
        
        print(f"\n✓ Completed {paper_num}")

def download_with_sopaper(query, output_dir):
    """Alternative: Download using SoPaper"""
    try:
        cmd = ["sopaper", query]
        subprocess.run(cmd, cwd=output_dir, check=True)
        return True
    except:
        return False

def main():
    """Main execution"""
    print("\n" + "="*60)
    print("Automated Paper Downloader")
    print("="*60 + "\n")
    
    base_dir = r"d:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL"
    csv_path = os.path.join(base_dir, "PAPERS_TO_DOWNLOAD.csv")
    
    # Install PyPaperBot
    install_pypaperbot()
    
    print("\nNote: This will attempt to download papers automatically.")
    print("Some papers may be paywalled and won't download.")
    print("You may need to manually download those from institutional access.\n")
    
    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    # Download papers
    download_papers_from_csv(csv_path, base_dir)
    
    print("\n" + "="*60)
    print("Download Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Check P##-Paper-Name/References/PDFs/ for downloaded papers")
    print("2. Manually download any missing papers from Google Scholar")
    print("3. Run: python convert_papers_to_markdown.py")
    print()

if __name__ == "__main__":
    main()
