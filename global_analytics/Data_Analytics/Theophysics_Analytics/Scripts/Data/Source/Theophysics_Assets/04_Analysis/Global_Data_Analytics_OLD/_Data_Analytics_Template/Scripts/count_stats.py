#!/usr/bin/env python3
"""
count_stats.py - Generate statistics dashboard from extracted data.

Usage:
    python count_stats.py [--input INPUT] [--output OUTPUT]
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import Counter


def load_json(filepath):
    """Load JSON file safely."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def categorize_tags(tags):
    """Categorize tags by domain."""
    categories = {
        'Physics': ['quantum', 'entropy', 'field', 'wave', 'particle', 'relativity', 'thermodynamics'],
        'Theology': ['grace', 'sin', 'logos', 'trinity', 'scripture', 'salvation', 'resurrection'],
        'Mathematics': ['axiom', 'theorem', 'equation', 'proof', 'algebra', 'geometry'],
        'Information': ['information', 'entropy', 'complexity', 'compression', 'data'],
        'Consciousness': ['consciousness', 'observer', 'mind', 'soul', 'awareness', 'qualia']
    }

    result = {cat: 0 for cat in categories}
    result['Other'] = 0

    for tag in tags:
        tag_lower = tag.lower()
        found = False
        for cat, keywords in categories.items():
            if any(kw in tag_lower for kw in keywords):
                result[cat] += 1
                found = True
                break
        if not found:
            result['Other'] += 1

    return result


def classify_equation_complexity(equations):
    """Classify equations by complexity."""
    complexity = {'Simple': 0, 'Medium': 0, 'Complex': 0}

    for eq in equations:
        latex = eq.get('latex', '')
        # Count significant symbols
        symbol_count = len(re.findall(r'[a-zA-Z\\]', latex))

        if symbol_count <= 5:
            complexity['Simple'] += 1
        elif symbol_count <= 15:
            complexity['Medium'] += 1
        else:
            complexity['Complex'] += 1

    return complexity


def generate_statistics(master_sheet_folder):
    """Generate comprehensive statistics."""
    folder = Path(master_sheet_folder)

    # Load extracted data
    equations = load_json(folder / 'Equations.json')
    axioms = load_json(folder / 'Axioms.json')
    definitions = load_json(folder / 'Definitions.json')
    tags = load_json(folder / 'Tags.json')
    links = load_json(folder / 'Links.json')
    stats = load_json(folder / 'stats.json')

    # Build comprehensive stats
    full_stats = {
        'generated_at': datetime.now().isoformat(),
        'content': {
            'equations': len(equations),
            'axioms': len(axioms),
            'definitions': len(definitions),
            'tags': len(tags),
            'internal_links': len(links.get('internal', [])),
            'external_links': len(links.get('external', [])),
            'total_words': stats.get('total_words', 0),
            'files_analyzed': stats.get('file_count', 0)
        },
        'tag_distribution': categorize_tags(tags),
        'equation_types': {
            'display': sum(1 for e in equations if e.get('type') == 'display'),
            'inline': sum(1 for e in equations if e.get('type') == 'inline')
        },
        'axiom_levels': {},
        'reading_time_minutes': stats.get('total_words', 0) // 200
    }

    # Axiom levels
    for ax in axioms:
        num = ax.get('number', 0)
        if num <= 3:
            level = 'Level 1: Existence'
        elif num <= 7:
            level = 'Level 2: Properties'
        elif num <= 11:
            level = 'Level 3: Origin'
        elif num <= 15:
            level = 'Level 4: Source'
        elif num <= 18:
            level = 'Level 5: Moral'
        elif num <= 20:
            level = 'Level 6: Identity'
        elif num <= 22:
            level = 'Level 7: Alternative'
        else:
            level = 'Level 8: Gap'

        full_stats['axiom_levels'][level] = full_stats['axiom_levels'].get(level, 0) + 1

    return full_stats


def update_dashboard(stats, dashboard_path):
    """Update the Statistics.md dashboard with current stats."""
    template = f"""---
uid: DA-stats-dashboard
type: dashboard
created: 2025-11-29
updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
purpose: Local statistics for current folder
---

# Statistics Dashboard

> Auto-generated statistics. Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## Content Metrics

| Category | Count |
|----------|-------|
| **Equations** | {stats['content']['equations']} |
| **Axioms** | {stats['content']['axioms']} |
| **Definitions** | {stats['content']['definitions']} |
| **Tags** | {stats['content']['tags']} |
| **Internal Links** | {stats['content']['internal_links']} |
| **External Links** | {stats['content']['external_links']} |
| **Total Words** | {stats['content']['total_words']:,} |
| **Reading Time** | ~{stats['reading_time_minutes']} min |

---

## Tag Distribution

| Category | Count |
|----------|-------|
| Physics | {stats['tag_distribution']['Physics']} |
| Theology | {stats['tag_distribution']['Theology']} |
| Mathematics | {stats['tag_distribution']['Mathematics']} |
| Information | {stats['tag_distribution']['Information']} |
| Consciousness | {stats['tag_distribution']['Consciousness']} |
| Other | {stats['tag_distribution']['Other']} |

---

## Equation Types

| Type | Count |
|------|-------|
| Display ($$...$$) | {stats['equation_types']['display']} |
| Inline ($...$) | {stats['equation_types']['inline']} |

---

## Axiom Levels

| Level | Count |
|-------|-------|
"""
    for level, count in sorted(stats['axiom_levels'].items()):
        template += f"| {level} | {count} |\n"

    template += """
---

*Auto-generated by `count_stats.py`*
"""

    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(template)


def main():
    import re  # Import here for classify_equation_complexity

    parser = argparse.ArgumentParser(description='Generate statistics from extracted data')
    parser.add_argument('--input', type=str, help='Master_Sheet folder path')
    parser.add_argument('--output', type=str, help='Dashboard output path')
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    master_sheet = Path(args.input) if args.input else script_dir.parent / 'Master_Sheet'
    dashboard = Path(args.output) if args.output else script_dir.parent / 'Dashboards' / 'Statistics.md'

    print(f"[count_stats] Reading from: {master_sheet}")

    stats = generate_statistics(master_sheet)

    # Save full stats
    with open(master_sheet / 'full_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)

    # Update dashboard
    update_dashboard(stats, dashboard)

    print(f"[count_stats] Statistics generated!")
    print(f"  Equations: {stats['content']['equations']}")
    print(f"  Axioms: {stats['content']['axioms']}")
    print(f"  Definitions: {stats['content']['definitions']}")
    print(f"  Words: {stats['content']['total_words']:,}")
    print(f"[count_stats] Dashboard updated: {dashboard}")


if __name__ == '__main__':
    main()
