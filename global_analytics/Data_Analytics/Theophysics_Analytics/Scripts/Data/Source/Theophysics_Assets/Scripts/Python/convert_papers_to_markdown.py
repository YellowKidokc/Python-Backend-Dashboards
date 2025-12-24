#!/usr/bin/env python3
"""
PDF to Markdown Converter for Academic Papers
Converts downloaded PDFs to markdown format for coherence analysis
"""

import os
import sys
from pathlib import Path
import csv

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Installing required package: PyMuPDF...")
    os.system(f"{sys.executable} -m pip install PyMuPDF")
    import fitz

def convert_pdf_to_markdown(pdf_path, output_path):
    """Convert a single PDF to markdown format"""
    try:
        doc = fitz.open(pdf_path)
        markdown_content = []
        
        # Extract metadata
        metadata = doc.metadata
        if metadata:
            markdown_content.append("---")
            markdown_content.append(f"title: {metadata.get('title', 'Unknown')}")
            markdown_content.append(f"author: {metadata.get('author', 'Unknown')}")
            markdown_content.append(f"source_pdf: {pdf_path.name}")
            markdown_content.append(f"pages: {len(doc)}")
            markdown_content.append("---\n")
        
        # Extract text from each page
        for page_num, page in enumerate(doc, 1):
            text = page.get_text()
            if text.strip():
                markdown_content.append(f"\n## Page {page_num}\n")
                markdown_content.append(text)
        
        # Write to markdown file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_content))
        
        doc.close()
        return True, f"Converted {pdf_path.name}"
        
    except Exception as e:
        return False, f"Error converting {pdf_path.name}: {str(e)}"

def process_paper_folders(base_dir):
    """Process all paper folders and convert PDFs"""
    base_path = Path(base_dir)
    results = []
    
    # Paper folders P01-P12
    paper_folders = [f"P{i:02d}-*" for i in range(1, 13)]
    
    for pattern in paper_folders:
        for paper_dir in base_path.glob(pattern):
            pdf_dir = paper_dir / "References" / "PDFs"
            md_dir = paper_dir / "References" / "Markdown"
            
            # Create markdown directory if it doesn't exist
            md_dir.mkdir(parents=True, exist_ok=True)
            
            if pdf_dir.exists():
                # Convert all PDFs in the folder
                for pdf_file in pdf_dir.glob("*.pdf"):
                    md_file = md_dir / f"{pdf_file.stem}.md"
                    
                    # Skip if already converted
                    if md_file.exists():
                        results.append((paper_dir.name, pdf_file.name, "Already exists", "SKIP"))
                        continue
                    
                    success, message = convert_pdf_to_markdown(pdf_file, md_file)
                    status = "SUCCESS" if success else "FAILED"
                    results.append((paper_dir.name, pdf_file.name, message, status))
    
    return results

def create_citation_index(base_dir):
    """Create an index of all converted papers"""
    base_path = Path(base_dir)
    citations = []
    
    for pattern in [f"P{i:02d}-*" for i in range(1, 13)]:
        for paper_dir in base_path.glob(pattern):
            md_dir = paper_dir / "References" / "Markdown"
            
            if md_dir.exists():
                for md_file in md_dir.glob("*.md"):
                    # Read first few lines to get metadata
                    with open(md_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()[:10]
                        title = "Unknown"
                        author = "Unknown"
                        
                        for line in lines:
                            if line.startswith("title:"):
                                title = line.split(":", 1)[1].strip()
                            elif line.startswith("author:"):
                                author = line.split(":", 1)[1].strip()
                    
                    citations.append({
                        'Paper': paper_dir.name,
                        'Filename': md_file.name,
                        'Title': title,
                        'Author': author,
                        'Path': str(md_file.relative_to(base_path))
                    })
    
    # Write citation index
    if citations:
        index_path = base_path / "CONVERTED_PAPERS_INDEX.csv"
        with open(index_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Paper', 'Filename', 'Title', 'Author', 'Path'])
            writer.writeheader()
            writer.writerows(citations)
        
        print(f"\n✓ Created citation index: {index_path}")
        print(f"  Total papers converted: {len(citations)}")

def main():
    """Main execution"""
    print("\n=== PDF to Markdown Converter ===\n")
    
    # Get base directory
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        base_dir = r"d:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL"
    
    print(f"Processing papers in: {base_dir}\n")
    
    # Convert PDFs
    results = process_paper_folders(base_dir)
    
    # Print results
    if results:
        print("\n=== Conversion Results ===\n")
        success_count = 0
        skip_count = 0
        fail_count = 0
        
        for paper, filename, message, status in results:
            if status == "SUCCESS":
                print(f"✓ {paper}: {filename}")
                success_count += 1
            elif status == "SKIP":
                print(f"⊘ {paper}: {filename} (already converted)")
                skip_count += 1
            else:
                print(f"✗ {paper}: {message}")
                fail_count += 1
        
        print(f"\n=== Summary ===")
        print(f"Success: {success_count}")
        print(f"Skipped: {skip_count}")
        print(f"Failed: {fail_count}")
        
        # Create citation index
        create_citation_index(base_dir)
    else:
        print("No PDFs found to convert.")
        print("\nMake sure PDFs are placed in:")
        print("  P##-Paper-Name/References/PDFs/")
    
    print("\n=== Complete ===\n")

if __name__ == "__main__":
    main()
