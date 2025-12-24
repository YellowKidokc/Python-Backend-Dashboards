#!/usr/bin/env python3
"""
Verify that all papers in the assembled master paper have their complete sections
(Hypotheses, Lexicon, Evidence, Enigmas, References, What We Got Wrong, etc.)
"""
import re
from pathlib import Path

ASSEMBLED = Path("COMPLETE_LOGOS_PAPERS_FINAL/THEOPHYSICS_MASTER_PAPER_ASSEMBLED.md")
PAPERS_DIR = Path("COMPLETE_LOGOS_PAPERS_FINAL")

# Expected sections that should appear after each paper
EXPECTED_SECTIONS = [
    r'## 🎯 Hypotheses',
    r'## 📖 Lexicon',
    r'## ✅ How Right We Are',
    r'### E\. What We Got Wrong',
    r'## ❓ Enigmas',
    r'## 📚 References',
]

# Find all paper sections in assembled file
with open(ASSEMBLED, 'r', encoding='utf-8') as f:
    content = f.read()

# Find paper headers
paper_pattern = r'^# \*\*Paper (\d+):'
papers = {}
for match in re.finditer(paper_pattern, content, re.MULTILINE):
    paper_num = int(match.group(1))
    start_pos = match.start()
    # Find next paper or end of file
    next_match = re.search(rf'^# \*\*Paper {paper_num + 1}:', content[start_pos + 1:], re.MULTILINE)
    if next_match:
        end_pos = start_pos + next_match.start()
    else:
        end_pos = len(content)
    
    papers[paper_num] = {
        'start': start_pos,
        'end': end_pos,
        'content': content[start_pos:end_pos]
    }

print(f"Found {len(papers)} papers in assembled file")
print("\nChecking sections for each paper:\n")

for paper_num in sorted(papers.keys()):
    paper_content = papers[paper_num]['content']
    print(f"Paper {paper_num}:")
    
    found_sections = []
    for section_pattern in EXPECTED_SECTIONS:
        if re.search(section_pattern, paper_content, re.MULTILINE):
            found_sections.append(section_pattern)
            print(f"  ✓ {section_pattern}")
        else:
            print(f"  ✗ MISSING: {section_pattern}")
    
    print()

