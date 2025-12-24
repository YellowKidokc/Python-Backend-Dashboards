#!/usr/bin/env python3
"""
Add missing sections (Hypotheses, Lexicon, Evidence, Enigmas, References, What We Got Wrong)
from individual FINAL papers to the assembled master paper
"""
import re
from pathlib import Path

ASSEMBLED = Path("COMPLETE_LOGOS_PAPERS_FINAL/THEOPHYSICS_MASTER_PAPER_ASSEMBLED.md")
PAPERS_DIR = Path("COMPLETE_LOGOS_PAPERS_FINAL")

def extract_section(content, section_pattern, next_section_pattern=None):
    """Extract a section from content"""
    match = re.search(section_pattern, content, re.MULTILINE)
    if not match:
        return None
    
    start = match.start()
    
    # Find end - either next major section or end of file
    if next_section_pattern:
        end_match = re.search(next_section_pattern, content[start + 1:], re.MULTILINE)
        if end_match:
            end = start + end_match.start()
        else:
            end = len(content)
    else:
        # Look for next ## section
        next_match = re.search(r'^## [^#]', content[start + 1:], re.MULTILINE)
        if next_match:
            end = start + next_match.start()
        else:
            end = len(content)
    
    return content[start:end].strip()

def get_all_sections(paper_path):
    """Extract all sections from a paper"""
    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = {}
    
    # Define section patterns in order
    section_patterns = [
        ('hypotheses', r'^## 🎯 Hypotheses'),
        ('lexicon', r'^## 📖 Lexicon'),
        ('evidence', r'^## ✅ How Right We Are|^## ✅ Evidence'),
        ('what_wrong', r'^### E\. What We Got Wrong|^### C\. What We Got Wrong'),
        ('enigmas', r'^## ❓ Enigmas'),
        ('references', r'^## 📚 References'),
    ]
    
    for name, pattern in section_patterns:
        section = extract_section(content, pattern)
        if section:
            sections[name] = section
    
    return sections

# Read assembled file
with open(ASSEMBLED, 'r', encoding='utf-8') as f:
    assembled_content = f.read()

# Process each paper
for paper_num in range(1, 13):
    paper_file = PAPERS_DIR / f"Paper-{paper_num:02d}-*-FINAL.md"
    paper_files = list(PAPERS_DIR.glob(f"Paper-{paper_num:02d}-*-FINAL.md"))
    
    if not paper_files:
        print(f"Paper {paper_num}: File not found")
        continue
    
    paper_path = paper_files[0]
    print(f"\nProcessing Paper {paper_num}: {paper_path.name}")
    
    # Get sections from individual paper
    sections = get_all_sections(paper_path)
    print(f"  Found sections: {list(sections.keys())}")
    
    # Find paper section in assembled file
    paper_pattern = rf'^# \*\*Paper {paper_num}:'
    paper_match = re.search(paper_pattern, assembled_content, re.MULTILINE)
    
    if not paper_match:
        print(f"  Paper {paper_num} not found in assembled file")
        continue
    
    # Find where this paper ends (next paper or end)
    paper_start = paper_match.start()
    next_paper_match = re.search(rf'^# \*\*Paper {paper_num + 1}:', assembled_content[paper_start + 1:], re.MULTILINE)
    
    if next_paper_match:
        paper_end = paper_start + next_paper_match.start()
    else:
        # Check for Paper 11/12 which might have different format
        next_match = re.search(rf'^### \*\*Paper {paper_num + 1}:', assembled_content[paper_start + 1:], re.MULTILINE)
        if next_match:
            paper_end = paper_start + next_match.start()
        else:
            paper_end = len(assembled_content)
    
    paper_section = assembled_content[paper_start:paper_end]
    
    # Check what's missing
    missing = []
    for name in ['hypotheses', 'lexicon', 'evidence', 'what_wrong', 'enigmas', 'references']:
        pattern_map = {
            'hypotheses': r'^## 🎯 Hypotheses',
            'lexicon': r'^## 📖 Lexicon',
            'evidence': r'^## ✅ How Right We Are|^## ✅ Evidence',
            'what_wrong': r'^### E\. What We Got Wrong|^### C\. What We Got Wrong',
            'enigmas': r'^## ❓ Enigmas',
            'references': r'^## 📚 References',
        }
        if not re.search(pattern_map[name], paper_section, re.MULTILINE):
            if name in sections:
                missing.append(name)
    
    if missing:
        print(f"  Missing sections: {missing}")
        
        # Find insertion point (before navigation/acknowledgments, or at end)
        # Look for Series Navigation or Acknowledgments or next paper
        insert_pattern = r'(^## 📖 Series Navigation|^## 🙏 Acknowledgments|^---\s*$)'
        insert_match = re.search(insert_pattern, paper_section, re.MULTILINE)
        
        if insert_match:
            insert_pos = paper_start + insert_match.start()
        else:
            insert_pos = paper_end
        
        # Build text to insert
        insert_text = "\n\n---\n\n"
        for name in missing:
            if name in sections:
                insert_text += sections[name] + "\n\n---\n\n"
        
        # Insert
        assembled_content = assembled_content[:insert_pos] + insert_text + assembled_content[insert_pos:]
        print(f"  ✓ Added {len(missing)} missing sections")
    else:
        print(f"  ✓ All sections present")

# Write updated assembled file
with open(ASSEMBLED, 'w', encoding='utf-8') as f:
    f.write(assembled_content)

print("\n✓ Done! Updated assembled master paper with missing sections.")

