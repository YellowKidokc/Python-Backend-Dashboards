#!/usr/bin/env python3
"""
extract_all.py - Master extraction script for local analytics
Extracts equations, definitions, axioms, tags, and links from markdown files.

Usage:
    python extract_all.py [--path PATH] [--output OUTPUT]

Defaults:
    --path: Parent folder of Scripts/
    --output: Master_Sheet/ folder
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime


def get_parent_folder():
    """Get the parent folder (where _Data_Analytics lives)."""
    script_dir = Path(__file__).parent
    return script_dir.parent.parent  # Go up from Scripts/ to _Data_Analytics/ to parent


def find_markdown_files(folder):
    """Find all markdown files in folder, excluding _Data_Analytics."""
    md_files = []
    for root, dirs, files in os.walk(folder):
        # Skip _Data_Analytics folder
        if '_Data_Analytics' in root:
            continue
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)
    return md_files


def extract_equations(content):
    """Extract LaTeX equations from markdown."""
    equations = []

    # Display math: $$...$$
    display_pattern = r'\$\$(.*?)\$\$'
    for match in re.finditer(display_pattern, content, re.DOTALL):
        equations.append({
            'type': 'display',
            'latex': match.group(1).strip(),
            'position': match.start()
        })

    # Inline math: $...$
    inline_pattern = r'(?<!\$)\$([^\$]+?)\$(?!\$)'
    for match in re.finditer(inline_pattern, content):
        equations.append({
            'type': 'inline',
            'latex': match.group(1).strip(),
            'position': match.start()
        })

    return equations


def extract_axioms(content):
    """Extract axioms (A1, A2, etc.) from markdown."""
    axioms = []

    # Pattern: **A1 (Name):** or A1: or **A1:**
    pattern = r'\*?\*?A(\d+)\s*(?:\([^)]+\))?\s*:?\*?\*?\s*([^\n]+)'
    for match in re.finditer(pattern, content):
        axioms.append({
            'id': f'A{match.group(1)}',
            'number': int(match.group(1)),
            'statement': match.group(2).strip(),
            'position': match.start()
        })

    return axioms


def extract_definitions(content):
    """Extract definitions from markdown."""
    definitions = []

    # Pattern: **Term**: Definition or **Term:** Definition
    pattern = r'\*\*([^*]+)\*\*\s*:\s*([^\n]+)'
    for match in re.finditer(pattern, content):
        term = match.group(1).strip()
        definition = match.group(2).strip()
        # Skip if it looks like an axiom
        if re.match(r'A\d+', term):
            continue
        definitions.append({
            'term': term,
            'definition': definition,
            'position': match.start()
        })

    return definitions


def extract_tags(content):
    """Extract tags from frontmatter and content."""
    tags = set()

    # Frontmatter tags
    frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        tags_match = re.search(r'tags:\s*\[(.*?)\]', frontmatter)
        if tags_match:
            for tag in tags_match.group(1).split(','):
                tags.add(tag.strip().strip('"\''))

    # Inline tags: #tag
    inline_pattern = r'#([a-zA-Z][a-zA-Z0-9_-]*)'
    for match in re.finditer(inline_pattern, content):
        tags.add(match.group(1))

    return list(tags)


def extract_links(content):
    """Extract internal and external links."""
    links = {
        'internal': [],
        'external': []
    }

    # Wikilinks: [[link]] or [[link|text]]
    wikilink_pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
    for match in re.finditer(wikilink_pattern, content):
        links['internal'].append(match.group(1).strip())

    # Markdown links: [text](url)
    md_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    for match in re.finditer(md_link_pattern, content):
        url = match.group(2)
        if url.startswith('http'):
            links['external'].append(url)
        else:
            links['internal'].append(url)

    return links


def process_file(filepath):
    """Process a single markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    return {
        'file': str(filepath.name),
        'path': str(filepath),
        'equations': extract_equations(content),
        'axioms': extract_axioms(content),
        'definitions': extract_definitions(content),
        'tags': extract_tags(content),
        'links': extract_links(content),
        'word_count': len(content.split())
    }


def aggregate_results(results):
    """Aggregate results from all files."""
    aggregated = {
        'equations': [],
        'axioms': [],
        'definitions': [],
        'tags': set(),
        'links': {'internal': [], 'external': []},
        'total_words': 0,
        'file_count': len(results)
    }

    for result in results:
        for eq in result['equations']:
            eq['source_file'] = result['file']
            aggregated['equations'].append(eq)

        for ax in result['axioms']:
            ax['source_file'] = result['file']
            aggregated['axioms'].append(ax)

        for defn in result['definitions']:
            defn['source_file'] = result['file']
            aggregated['definitions'].append(defn)

        aggregated['tags'].update(result['tags'])
        aggregated['links']['internal'].extend(result['links']['internal'])
        aggregated['links']['external'].extend(result['links']['external'])
        aggregated['total_words'] += result['word_count']

    aggregated['tags'] = list(aggregated['tags'])
    aggregated['links']['internal'] = list(set(aggregated['links']['internal']))
    aggregated['links']['external'] = list(set(aggregated['links']['external']))

    return aggregated


def save_results(aggregated, output_folder):
    """Save results to Master_Sheet folder."""
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    # Save equations
    with open(output_folder / 'Equations.json', 'w', encoding='utf-8') as f:
        json.dump(aggregated['equations'], f, indent=2)

    # Save axioms
    with open(output_folder / 'Axioms.json', 'w', encoding='utf-8') as f:
        json.dump(aggregated['axioms'], f, indent=2)

    # Save definitions
    with open(output_folder / 'Definitions.json', 'w', encoding='utf-8') as f:
        json.dump(aggregated['definitions'], f, indent=2)

    # Save tags
    with open(output_folder / 'Tags.json', 'w', encoding='utf-8') as f:
        json.dump(aggregated['tags'], f, indent=2)

    # Save links
    with open(output_folder / 'Links.json', 'w', encoding='utf-8') as f:
        json.dump(aggregated['links'], f, indent=2)

    # Save summary stats
    stats = {
        'extracted_at': datetime.now().isoformat(),
        'file_count': aggregated['file_count'],
        'equation_count': len(aggregated['equations']),
        'axiom_count': len(aggregated['axioms']),
        'definition_count': len(aggregated['definitions']),
        'tag_count': len(aggregated['tags']),
        'internal_link_count': len(aggregated['links']['internal']),
        'external_link_count': len(aggregated['links']['external']),
        'total_words': aggregated['total_words']
    }
    with open(output_folder / 'stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)

    return stats


def main():
    parser = argparse.ArgumentParser(description='Extract analytics from markdown files')
    parser.add_argument('--path', type=str, help='Path to analyze')
    parser.add_argument('--output', type=str, help='Output folder for Master_Sheet')
    args = parser.parse_args()

    # Determine paths
    if args.path:
        target_folder = Path(args.path)
    else:
        target_folder = get_parent_folder()

    if args.output:
        output_folder = Path(args.output)
    else:
        script_dir = Path(__file__).parent
        output_folder = script_dir.parent / 'Master_Sheet'

    print(f"[extract_all] Analyzing: {target_folder}")
    print(f"[extract_all] Output to: {output_folder}")

    # Find and process files
    md_files = find_markdown_files(target_folder)
    print(f"[extract_all] Found {len(md_files)} markdown files")

    results = []
    for filepath in md_files:
        try:
            result = process_file(filepath)
            results.append(result)
            print(f"  - {filepath.name}: {len(result['equations'])} eq, {len(result['axioms'])} ax")
        except Exception as e:
            print(f"  ! Error processing {filepath}: {e}")

    # Aggregate and save
    aggregated = aggregate_results(results)
    stats = save_results(aggregated, output_folder)

    print(f"\n[extract_all] Complete!")
    print(f"  Files: {stats['file_count']}")
    print(f"  Equations: {stats['equation_count']}")
    print(f"  Axioms: {stats['axiom_count']}")
    print(f"  Definitions: {stats['definition_count']}")
    print(f"  Tags: {stats['tag_count']}")
    print(f"  Links: {stats['internal_link_count']} internal, {stats['external_link_count']} external")
    print(f"  Words: {stats['total_words']}")


if __name__ == '__main__':
    main()
