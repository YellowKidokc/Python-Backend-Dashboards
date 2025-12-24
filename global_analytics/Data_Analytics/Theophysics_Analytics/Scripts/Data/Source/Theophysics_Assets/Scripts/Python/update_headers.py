#!/usr/bin/env python3
"""
Script to update YAML frontmatter and headers in FINAL.md files
"""
import re
from pathlib import Path

# Paper metadata
PAPERS = {
    "LGS-P01-Logos-Principle-FINAL.md": {
        "number": 1,
        "title": "THE LOGOS PRINCIPLE",
        "subtitle": "A Participatory Framework for Unifying General Relativity & Quantum Mechanics",
        "duration": "90 min"
    },
    "LGS-P02-Quantum-Bridge-FINAL.md": {
        "number": 2,
        "title": "THE QUANTUM BRIDGE",
        "subtitle": "Eight Mathematical Proofs at the Physics-Theology Boundary",
        "duration": "75 min"
    },
    "LGS-P02-Quantum-Bridge-FINAL-RESTRUCTURED.md": {
        "number": 2,
        "title": "THE QUANTUM BRIDGE (RESTRUCTURED)",
        "subtitle": "Eight Mathematical Proofs at the Physics-Theology Boundary",
        "duration": "75 min"
    },
    "LGS-P03-Algorithm-Reality-FINAL.md": {
        "number": 3,
        "title": "THE ALGORITHM OF REALITY",
        "subtitle": "Computational Foundations of Physical Law",
        "duration": "70 min"
    },
    "LGS-P04-Hard-Problem-FINAL.md": {
        "number": 4,
        "title": "THE HARD PROBLEM OF CONSCIOUSNESS",
        "subtitle": "A Solution Through the Logos Field",
        "duration": "65 min"
    },
    "LGS-P05-Soul-Observer-FINAL.md": {
        "number": 5,
        "title": "THE SOUL OBSERVER",
        "subtitle": "Consciousness as Fundamental Observer",
        "duration": "60 min"
    },
    "LGS-P06-Physics-Principalities-FINAL.md": {
        "number": 6,
        "title": "A PHYSICS OF PRINCIPALITIES",
        "subtitle": "Spiritual Forces in Physical Framework",
        "duration": "70 min"
    },
    "LGS-P07-Grace-Function-FINAL.md": {
        "number": 7,
        "title": "THE GRACE FUNCTION",
        "subtitle": "Mathematical Framework for Divine Intervention",
        "duration": "75 min"
    },
    "LGS-P07-Grace-Function-FINAL-RIGOR.md": {
        "number": 7,
        "title": "THE GRACE FUNCTION (WITH RIGOR)",
        "subtitle": "Mathematical Framework for Divine Intervention - Extended Analysis",
        "duration": "90 min"
    },
    "LGS-P08-Stretched-Heavens-FINAL.md": {
        "number": 8,
        "title": "THE STRETCHED OUT HEAVENS",
        "subtitle": "Biblical Cosmology Meets Modern Physics",
        "duration": "65 min"
    },
    "LGS-P09-Moral-Universe-FINAL.md": {
        "number": 9,
        "title": "THE MORAL UNIVERSE",
        "subtitle": "Ethics as Physical Law",
        "duration": "70 min"
    },
    "LGS-P10-Creatio-Silico-FINAL.md": {
        "number": 10,
        "title": "CREATIO EX SILICO",
        "subtitle": "Creation from Information",
        "duration": "75 min"
    },
    "LGS-P11-Protocols-Validation-FINAL.md": {
        "number": 11,
        "title": "PROTOCOLS FOR VALIDATION",
        "subtitle": "Experimental Tests of the Logos Framework",
        "duration": "80 min"
    },
    "LGS-P12-Decalogue-Cosmos-FINAL.md": {
        "number": 12,
        "title": "THE DECALOGUE OF THE COSMOS",
        "subtitle": "Ten Fundamental Principles",
        "duration": "85 min"
    }
}

def update_yaml_frontmatter(content, filename):
    """Update YAML frontmatter"""
    # Update 'updated' field to 2025-11-19
    content = re.sub(
        r'updated:\s*"[\d-]+"',
        'updated: "2025-11-19"',
        content
    )

    # Update downloads field
    content = re.sub(
        r'downloads:\s*\[""\]',
        'downloads: []',
        content
    )
    content = re.sub(
        r'downloads:\s*\[.*?\]',
        'downloads: []',
        content
    )

    # Update migration_date
    content = re.sub(
        r'migration_date:\s*"[\d-]+"',
        'migration_date: "2025-11-19"',
        content
    )

    return content

def create_new_header(paper_info):
    """Create the new header section"""
    num = paper_info['number']
    num_str = f"{num:02d}"

    header = f"""# {paper_info['title']}
## {paper_info['subtitle']}

---

**Authors:**
David Lowe¹
Claude (Anthropic)²

**Affiliations:**
¹ Independent Researcher, Oklahoma City, OK
² Anthropic PBC, San Francisco, CA

**Correspondence:**
David Lowe: [contact information]

**Date:** November 2025

**Paper:** {num} of 12 in the Logos Papers series

**License:** CC BY-NC 4.0

---

## 🎧 Audio & Resources


# 📖 READ THE ENTIRE PAPER TO YOU

### 🔊 **[FULL PAPER AUDIO - READ TO YOU](./audio/paper{num_str}_complete_reading.mp3)** ({paper_info['duration']})
**Complete audio narration of the entire paper from start to finish.**
*Perfect for listening while driving, exercising, or relaxing.*

---

**Additional Resources:**

- 🎙️ **[Foundation Podcast](./audio/paper{num_str}_foundation.mp3)** (12-17 min) - Essential concepts explained
- 🎙️ **[Paper Podcast](./audio/paper{num_str}_main.mp3)** (30-45 min) - Complete guided walkthrough

---

"""
    return header

def update_file(filepath):
    """Update a single file"""
    print(f"Processing {filepath.name}...")

    if filepath.name not in PAPERS:
        print(f"  Skipping {filepath.name} - not in PAPERS dict")
        return

    paper_info = PAPERS[filepath.name]

    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update YAML frontmatter
    content = update_yaml_frontmatter(content, filepath.name)

    # Find end of YAML frontmatter
    yaml_end = content.find('---', 3)  # Find second ---
    if yaml_end == -1:
        print(f"  ERROR: Could not find YAML frontmatter in {filepath.name}")
        return

    yaml_section = content[:yaml_end + 3]
    rest_of_content = content[yaml_end + 3:]

    # Remove old header section (everything until first ##)
    # We want to keep content starting from first major section
    # Look for patterns like "## 📖 For Everyone" or "## Abstract" or "## ⚠️"
    patterns = [
        r'\n## 📖 For Everyone',
        r'\n## For Everyone',
        r'\n## Abstract',
        r'\n## ⚠️',
        r'\n## 🔬',
        r'\n## \d+\.',
        r'\n### 1\.',
    ]

    first_section_pos = len(rest_of_content)
    for pattern in patterns:
        match = re.search(pattern, rest_of_content)
        if match:
            first_section_pos = min(first_section_pos, match.start())

    if first_section_pos < len(rest_of_content):
        body_content = rest_of_content[first_section_pos:]
    else:
        # Can't find section, keep everything after ---
        body_content = rest_of_content

    # Create new header
    new_header = create_new_header(paper_info)

    # Combine: YAML + newline + new header + body
    updated_content = yaml_section + "\n\n" + new_header + body_content.lstrip()

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"  [OK] Updated {filepath.name}")

def main():
    """Main function"""
    base_dir = Path(__file__).parent

    for filename in PAPERS.keys():
        filepath = base_dir / filename
        if filepath.exists():
            update_file(filepath)
        else:
            print(f"File not found: {filepath}")

if __name__ == "__main__":
    main()
