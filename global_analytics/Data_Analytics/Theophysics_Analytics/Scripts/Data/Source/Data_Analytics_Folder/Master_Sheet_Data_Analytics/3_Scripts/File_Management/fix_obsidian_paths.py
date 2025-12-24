#!/usr/bin/env python3
"""
Fix image paths for Obsidian - use vault-relative paths instead of file-relative
"""
import re
from pathlib import Path

PAPER_PATH = Path("COMPLETE_LOGOS_PAPERS_FINAL/Paper-01-The-Logos-Principle-FINAL.md")

# Read the paper
with open(PAPER_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace ../assets/ with COMPLETE_LOGOS_PAPERS_FINAL/assets/
# This makes paths relative to vault root instead of file location
content = re.sub(
    r'!\[([^\]]*)\]\(\.\./assets/([^)]+)\)',
    r'![\1](COMPLETE_LOGOS_PAPERS_FINAL/assets/\2)',
    content
)

# Also fix the clickable links
content = re.sub(
    r'\[📎 ([^\]]+)\]\(\.\./assets/([^)]+)\)',
    r'[📎 \1](COMPLETE_LOGOS_PAPERS_FINAL/assets/\2)',
    content
)

# Write back
with open(PAPER_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed all image paths to be vault-relative")
print("Changed: ../assets/ → COMPLETE_LOGOS_PAPERS_FINAL/assets/")

