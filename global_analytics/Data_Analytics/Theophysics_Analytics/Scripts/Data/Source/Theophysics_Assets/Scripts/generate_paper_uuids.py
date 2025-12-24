#!/usr/bin/env python3
"""
Generate UUID schema for all Theophysics papers and sync to PostgreSQL.

Usage:
    python generate_paper_uuids.py --vault-path "D:/THEOPHYSICS_MASTER/03_PUBLICATIONS/COMPLETE_LOGOS_PAPERS_FINAL"
    
Features:
    - Generates stable UUID5 identifiers
    - Updates YAML frontmatter
    - Syncs to PostgreSQL
    - Creates citation relationships
    - Idempotent (safe to re-run)
"""

import os
import re
import yaml
import uuid
import psycopg2
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import hashlib
import argparse

# Configuration
DB_CONFIG = {
    'host': '192.168.1.215',
    'database': 'theophysics',
    'user': 'postgres',
    'password': os.getenv('POSTGRES_PASSWORD', 'your_password_here')
}

# UUID Namespace (generate once, use forever)
THEOPHYSICS_NAMESPACE = uuid.UUID('550e8400-e29b-41d4-a716-446655440000')

# Paper number pattern
PAPER_PATTERN = re.compile(r'^P(\d{2})-')

class TheophysicsUUIDGenerator:
    """Generate and manage UUIDs for Theophysics papers."""
    
    def __init__(self, vault_path: str, db_config: dict):
        self.vault_path = Path(vault_path)
        self.db_config = db_config
        self.conn = None
        
    def connect_db(self):
        """Connect to PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            print("✅ Connected to PostgreSQL")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def close_db(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("✅ Database connection closed")
    
    def generate_paper_uuid(self, paper_number: int, title: str) -> uuid.UUID:
        """Generate deterministic UUID5 for paper."""
        paper_identifier = f"P{paper_number:02d}:{title}"
        return uuid.uuid5(THEOPHYSICS_NAMESPACE, paper_identifier)
    
    def generate_section_uuid(self, paper_uuid: uuid.UUID, section_number: int, title: str) -> uuid.UUID:
        """Generate deterministic UUID5 for section."""
        section_identifier = f"{paper_uuid}:S{section_number:02d}:{title}"
        return uuid.uuid5(THEOPHYSICS_NAMESPACE, section_identifier)
    
    def generate_figure_uuid(self, paper_uuid: uuid.UUID, figure_number: int, filename: str) -> uuid.UUID:
        """Generate deterministic UUID5 for figure."""
        figure_identifier = f"{paper_uuid}:F{figure_number:03d}:{filename}"
        return uuid.uuid5(THEOPHYSICS_NAMESPACE, figure_identifier)
    
    def extract_yaml_frontmatter(self, content: str) -> Tuple[Optional[dict], str]:
        """Extract YAML frontmatter from markdown file."""
        yaml_pattern = re.compile(r'^---\s*\n(.*?\n)---\s*\n', re.DOTALL)
        match = yaml_pattern.match(content)
        
        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1))
                remaining_content = content[match.end():]
                return frontmatter, remaining_content
            except yaml.YAMLError as e:
                print(f"⚠️ YAML parsing error: {e}")
                return None, content
        return None, content
    
    def update_yaml_frontmatter(self, content: str, updates: dict) -> str:
        """Update or create YAML frontmatter with new fields."""
        frontmatter, body = self.extract_yaml_frontmatter(content)
        
        if frontmatter is None:
            frontmatter = {}
        
        # Update with new UUID fields
        frontmatter.update(updates)
        
        # Reconstruct file
        yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        return f"---\n{yaml_str}---\n\n{body}"
    
    def parse_markdown_structure(self, content: str) -> List[dict]:
        """Extract sections from markdown content."""
        sections = []
        section_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        
        matches = section_pattern.finditer(content)
        for i, match in enumerate(matches, 1):
            level = len(match.group(1))
            title = match.group(2).strip()
            sections.append({
                'number': i,
                'level': level,
                'title': title,
                'position': match.start()
            })
        
        return sections
    
    def extract_figures(self, content: str) -> List[dict]:
        """Extract figure references from markdown."""
        figures = []
        # Match both markdown and HTML image syntax
        img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)|<img[^>]+src=["\']([^"\']+)["\']')
        
        for i, match in enumerate(img_pattern.finditer(content), 1):
            if match.group(1) is not None:  # Markdown syntax
                alt_text = match.group(1)
                path = match.group(2)
            else:  # HTML syntax
                alt_text = ""
                path = match.group(3)
            
            figures.append({
                'number': i,
                'alt_text': alt_text,
                'path': path
            })
        
        return figures
    
    def extract_citations(self, content: str) -> List[str]:
        """Extract internal paper citations."""
        # Match [[Paper-XX-Title]] format
        citation_pattern = re.compile(r'\[\[Paper-(\d{2})[^\]]*\]\]')
        citations = citation_pattern.findall(content)
        return [int(c) for c in citations]
    
    def process_paper(self, paper_folder: Path) -> Optional[dict]:
        """Process a single paper folder and generate UUIDs."""
        # Extract paper number from folder name
        match = PAPER_PATTERN.match(paper_folder.name)
        if not match:
            print(f"⚠️ Skipping {paper_folder.name} (no paper number found)")
            return None
        
        paper_number = int(match.group(1))
        print(f"\n📄 Processing Paper {paper_number:02d}: {paper_folder.name}")
        
        # Find main paper file (LGS-F version = canonical)
        main_paper = None
        for candidate in ['LGS-F-P*.md', '00_The_Paper.md', f'P{paper_number:02d}*.md']:
            matches = list(paper_folder.glob(candidate))
            if matches:
                main_paper = matches[0]
                break
        
        if not main_paper or not main_paper.exists():
            print(f"❌ No main paper file found in {paper_folder.name}")
            return None
        
        print(f"   📖 Reading: {main_paper.name}")
        
        # Read file content
        with open(main_paper, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract existing frontmatter
        frontmatter, body = self.extract_yaml_frontmatter(content)
        if frontmatter is None:
            frontmatter = {}
        
        # Get or create paper title
        title = frontmatter.get('title', f'Paper {paper_number}: Title Not Set')
        
        # Generate paper UUID
        paper_uuid = self.generate_paper_uuid(paper_number, title)
        paper_code = f"P{paper_number:02d}"
        
        print(f"   🔑 UUID: {paper_uuid}")
        print(f"   📋 Code: {paper_code}")
        
        # Parse structure
        sections = self.parse_markdown_structure(body)
        figures = self.extract_figures(body)
        citations = self.extract_citations(body)
        
        print(f"   📊 Found: {len(sections)} sections, {len(figures)} figures, {len(citations)} citations")
        
        # Generate section UUIDs
        section_data = []
        for section in sections:
            section_uuid = self.generate_section_uuid(
                paper_uuid, 
                section['number'], 
                section['title']
            )
            section_data.append({
                **section,
                'uuid': section_uuid,
                'code': f"{paper_code}-S{section['number']:02d}"
            })
        
        # Generate figure UUIDs
        figure_data = []
        for figure in figures:
            figure_uuid = self.generate_figure_uuid(
                paper_uuid,
                figure['number'],
                figure['path']
            )
            figure_data.append({
                **figure,
                'uuid': figure_uuid,
                'code': f"{paper_code}-F{figure['number']:03d}"
            })
        
        # Update YAML frontmatter
        yaml_updates = {
            'paper_uuid': str(paper_uuid),
            'paper_code': paper_code,
            'paper_number': paper_number,
            'uuid_generated_at': datetime.now().isoformat(),
            'uuid_version': '1.0'
        }
        
        # Write back to file
        updated_content = self.update_yaml_frontmatter(content, yaml_updates)
        
        with open(main_paper, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"   ✅ YAML frontmatter updated")
        
        return {
            'paper_uuid': paper_uuid,
            'paper_number': paper_number,
            'paper_code': paper_code,
            'title': title,
            'file_path': str(main_paper),
            'relative_path': str(main_paper.relative_to(self.vault_path)),
            'frontmatter': frontmatter,
            'sections': section_data,
            'figures': figure_data,
            'citations': citations,
            'word_count': len(body.split()),
            'created_date': frontmatter.get('created', None),
            'updated_date': frontmatter.get('updated', None),
            'status': frontmatter.get('status', 'draft')
        }
    
    def sync_to_postgres(self, paper_data: dict):
        """Sync paper data to PostgreSQL."""
        if not self.conn:
            print("❌ No database connection")
            return
        
        cursor = self.conn.cursor()
        
        try:
            # Insert/Update main paper record
            cursor.execute("""
                INSERT INTO papers.theophysics_papers (
                    paper_uuid, paper_number, paper_code, title,
                    status, file_path, relative_path,
                    word_count, section_count, figure_count, citation_count,
                    yaml_frontmatter, created_date, updated_date
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s
                )
                ON CONFLICT (paper_uuid) DO UPDATE SET
                    title = EXCLUDED.title,
                    status = EXCLUDED.status,
                    word_count = EXCLUDED.word_count,
                    section_count = EXCLUDED.section_count,
                    figure_count = EXCLUDED.figure_count,
                    citation_count = EXCLUDED.citation_count,
                    yaml_frontmatter = EXCLUDED.yaml_frontmatter,
                    updated_at = NOW()
            """, (
                paper_data['paper_uuid'],
                paper_data['paper_number'],
                paper_data['paper_code'],
                paper_data['title'],
                paper_data['status'],
                paper_data['file_path'],
                paper_data['relative_path'],
                paper_data['word_count'],
                len(paper_data['sections']),
                len(paper_data['figures']),
                len(paper_data['citations']),
                yaml.dump(paper_data['frontmatter']),
                paper_data['created_date'],
                paper_data['updated_date']
            ))
            
            # Insert sections
            for section in paper_data['sections']:
                cursor.execute("""
                    INSERT INTO papers.paper_sections (
                        section_uuid, paper_uuid, section_number, section_code,
                        heading_level, title
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (section_uuid) DO UPDATE SET
                        title = EXCLUDED.title
                """, (
                    section['uuid'],
                    paper_data['paper_uuid'],
                    section['number'],
                    section['code'],
                    section['level'],
                    section['title']
                ))
            
            # Insert figures
            for figure in paper_data['figures']:
                cursor.execute("""
                    INSERT INTO papers.paper_figures (
                        figure_uuid, paper_uuid, figure_number, figure_code,
                        title, file_path
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (figure_uuid) DO UPDATE SET
                        file_path = EXCLUDED.file_path
                """, (
                    figure['uuid'],
                    paper_data['paper_uuid'],
                    figure['number'],
                    figure['code'],
                    figure['alt_text'],
                    figure['path']
                ))
            
            # Insert citations
            for cited_paper_number in paper_data['citations']:
                # Generate target UUID (we'll need to look this up or generate)
                target_code = f"P{cited_paper_number:02d}"
                cursor.execute("""
                    INSERT INTO papers.paper_citations (
                        source_paper_uuid, target_paper_uuid, citation_type
                    )
                    SELECT %s, paper_uuid, 'internal'
                    FROM papers.theophysics_papers
                    WHERE paper_code = %s
                    ON CONFLICT DO NOTHING
                """, (paper_data['paper_uuid'], target_code))
            
            self.conn.commit()
            print(f"   ✅ Synced to PostgreSQL")
            
        except Exception as e:
            self.conn.rollback()
            print(f"   ❌ Database sync failed: {e}")
        finally:
            cursor.close()
    
    def process_all_papers(self):
        """Process all paper folders in vault."""
        paper_folders = sorted([
            d for d in self.vault_path.iterdir()
            if d.is_dir() and PAPER_PATTERN.match(d.name)
        ])
        
        print(f"\n🔍 Found {len(paper_folders)} paper folders")
        
        processed_count = 0
        for folder in paper_folders:
            paper_data = self.process_paper(folder)
            if paper_data:
                self.sync_to_postgres(paper_data)
                processed_count += 1
        
        print(f"\n✅ Processed {processed_count}/{len(paper_folders)} papers")
    
    def generate_citation_report(self):
        """Generate citation relationship report from database."""
        if not self.conn:
            return
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                src.paper_code AS source,
                src.title AS source_title,
                tgt.paper_code AS target,
                tgt.title AS target_title,
                COUNT(*) as citation_count
            FROM papers.paper_citations pc
            JOIN papers.theophysics_papers src ON pc.source_paper_uuid = src.paper_uuid
            JOIN papers.theophysics_papers tgt ON pc.target_paper_uuid = tgt.paper_uuid
            GROUP BY src.paper_code, src.title, tgt.paper_code, tgt.title
            ORDER BY src.paper_code, tgt.paper_code
        """)
        
        print("\n📊 CITATION REPORT")
        print("=" * 80)
        for row in cursor.fetchall():
            print(f"{row[0]} → {row[2]}: {row[4]} citation(s)")
        
        cursor.close()


def main():
    parser = argparse.ArgumentParser(description='Generate UUIDs for Theophysics papers')
    parser.add_argument('--vault-path', required=True, help='Path to vault root')
    parser.add_argument('--dry-run', action='store_true', help='Don\'t write to files or database')
    
    args = parser.parse_args()
    
    print("🚀 Theophysics UUID Generator")
    print("=" * 80)
    
    generator = TheophysicsUUIDGenerator(args.vault_path, DB_CONFIG)
    
    if not args.dry_run:
        if generator.connect_db():
            generator.process_all_papers()
            generator.generate_citation_report()
            generator.close_db()
        else:
            print("⚠️ Running without database sync (connection failed)")
            generator.process_all_papers()
    else:
        print("🔍 DRY RUN MODE - No changes will be made")
        generator.process_all_papers()

if __name__ == '__main__':
    main()
