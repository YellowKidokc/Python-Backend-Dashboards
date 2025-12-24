#!/usr/bin/env python3
"""
Generate UUID schema for ALL Theophysics vault content.

Usage:
    python generate_vault_uuids.py --vault-path "D:/THEOPHYSICS_MASTER"
    
Features:
    - Generates stable UUID5 identifiers for ALL markdown files
    - Updates/creates YAML frontmatter
    - Syncs papers to PostgreSQL (optional)
    - Idempotent (safe to re-run)
    - Processes papers, notes, templates, and all other markdown files
"""

import os
import re
import yaml
import uuid
import psycopg2
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
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

# Files to skip
SKIP_FILES = {'.obsidian', '.git', '.claude', 'node_modules', '__pycache__', '.stfolder'}

class TheophysicsVaultUUIDGenerator:
    """Generate and manage UUIDs for all Theophysics vault content."""
    
    def __init__(self, vault_path: str, db_config: dict, db_sync: bool = False):
        self.vault_path = Path(vault_path)
        self.db_config = db_config
        self.db_sync = db_sync
        self.conn = None
        self.stats = {
            'papers_processed': 0,
            'notes_processed': 0,
            'yaml_created': 0,
            'yaml_updated': 0,
            'uuids_generated': 0,
            'errors': 0
        }
        
    def connect_db(self):
        """Connect to PostgreSQL database."""
        if not self.db_sync:
            return False
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
    
    def generate_file_uuid(self, file_path: Path, title: str = None) -> uuid.UUID:
        """Generate deterministic UUID5 for any file."""
        # Use relative path from vault root for consistency
        try:
            rel_path = file_path.relative_to(self.vault_path)
        except ValueError:
            rel_path = file_path
        
        # Create identifier from path and optional title
        if title:
            identifier = f"{rel_path}:{title}"
        else:
            identifier = str(rel_path)
        
        return uuid.uuid5(THEOPHYSICS_NAMESPACE, identifier)
    
    def generate_paper_uuid(self, paper_number: int, title: str) -> uuid.UUID:
        """Generate deterministic UUID5 for paper."""
        paper_identifier = f"P{paper_number:02d}:{title}"
        return uuid.uuid5(THEOPHYSICS_NAMESPACE, paper_identifier)
    
    def extract_yaml_frontmatter(self, content: str) -> Tuple[Optional[dict], str]:
        """Extract YAML frontmatter from markdown file."""
        yaml_pattern = re.compile(r'^---\s*\n(.*?\n)---\s*\n', re.DOTALL)
        match = yaml_pattern.match(content)
        
        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1))
                if frontmatter is None:
                    frontmatter = {}
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
            self.stats['yaml_created'] += 1
        else:
            self.stats['yaml_updated'] += 1
        
        # Update with new UUID fields (don't overwrite existing)
        for key, value in updates.items():
            if key not in frontmatter or frontmatter[key] is None:
                frontmatter[key] = value
        
        # Reconstruct file
        yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False, allow_unicode=True)
        return f"---\n{yaml_str}---\n\n{body}"
    
    def extract_title_from_content(self, content: str, filename: str) -> str:
        """Extract title from content or filename."""
        # Try to find first H1 heading
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
        
        # Fall back to filename without extension
        return filename.replace('.md', '').replace('_', ' ').replace('-', ' ')
    
    def determine_file_type(self, file_path: Path) -> str:
        """Determine the type of file based on path and name."""
        path_str = str(file_path).lower()
        name = file_path.name.lower()
        
        # Check for papers
        if 'paper' in path_str or re.match(r'p\d{2}', name) or 'lgs-' in name:
            return 'paper'
        
        # Check for templates
        if 'template' in path_str or 'template' in name:
            return 'template'
        
        # Check for documentation
        if 'readme' in name or 'docs' in path_str or 'documentation' in path_str:
            return 'documentation'
        
        # Check for analysis
        if 'analysis' in path_str or 'critique' in path_str:
            return 'analysis'
        
        # Check for concepts
        if 'concept' in name or 'atom' in name:
            return 'concept'
        
        # Check for workflow/admin
        if 'workflow' in path_str or 'admin' in path_str:
            return 'workflow'
        
        # Default
        return 'note'
    
    def process_markdown_file(self, file_path: Path) -> bool:
        """Process a single markdown file and add/update UUID."""
        try:
            # Skip empty files
            if file_path.stat().st_size == 0:
                print(f"⏭️  Skipping empty file: {file_path.name}")
                return False
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract existing frontmatter
            frontmatter, body = self.extract_yaml_frontmatter(content)
            
            # Check if UUID already exists
            if frontmatter and 'uuid' in frontmatter and frontmatter['uuid']:
                print(f"✓ Already has UUID: {file_path.name}")
                return True
            
            # Extract or generate title
            if frontmatter and 'title' in frontmatter:
                title = frontmatter['title']
            else:
                title = self.extract_title_from_content(body, file_path.name)
            
            # Generate UUID
            file_uuid = self.generate_file_uuid(file_path, title)
            self.stats['uuids_generated'] += 1
            
            # Determine file type
            file_type = self.determine_file_type(file_path)
            
            # Get relative path
            try:
                rel_path = file_path.relative_to(self.vault_path)
            except ValueError:
                rel_path = file_path
            
            # Prepare YAML updates (comprehensive Theophysics standard)
            yaml_updates = {
                # Core metadata
                'uuid': str(file_uuid),
                'title': title,
                'author': frontmatter.get('author', 'David Lowe') if frontmatter else 'David Lowe',
                'type': file_type,
                'created': frontmatter.get('created') if frontmatter else datetime.now().strftime('%Y-%m-%d'),
                'updated': datetime.now().strftime('%Y-%m-%d'),
                'status': frontmatter.get('status', 'draft') if frontmatter else 'draft',
                
                # UUID metadata
                'file_path': str(rel_path),
                'uuid_generated_at': datetime.now().isoformat(),
                'uuid_version': '1.0',
                
                # Classification (only if not already present)
                'tags': frontmatter.get('tags', []) if frontmatter else [],
                'pillars': frontmatter.get('pillars', []) if frontmatter else [],
                'category': frontmatter.get('category', 'theophysics-general') if frontmatter else 'theophysics-general',
            }
            
            # Write back to file
            updated_content = self.update_yaml_frontmatter(content, yaml_updates)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ {file_path.name}")
            print(f"   UUID: {file_uuid}")
            print(f"   Type: {file_type}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")
            self.stats['errors'] += 1
            return False
    
    def process_paper_folder(self, paper_folder: Path) -> Optional[dict]:
        """Process a paper folder (for database sync)."""
        # Extract paper number from folder name
        match = PAPER_PATTERN.match(paper_folder.name)
        if not match:
            return None
        
        paper_number = int(match.group(1))
        print(f"\n📄 Processing Paper {paper_number:02d}: {paper_folder.name}")
        
        # Find main paper file (LGS-F version = canonical)
        main_paper = None
        for pattern in ['LGS-F-P*.md', 'LGS-P*.md', f'P{paper_number:02d}*.md']:
            matches = list(paper_folder.glob(pattern))
            if matches:
                main_paper = matches[0]
                break
        
        if not main_paper or not main_paper.exists():
            print(f"⚠️ No main paper file found in {paper_folder.name}")
            return None
        
        # Process the main paper file
        self.process_markdown_file(main_paper)
        self.stats['papers_processed'] += 1
        
        # Read updated content
        with open(main_paper, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter, body = self.extract_yaml_frontmatter(content)
        
        if frontmatter:
            return {
                'paper_uuid': frontmatter.get('uuid'),
                'paper_number': paper_number,
                'paper_code': f"P{paper_number:02d}",
                'title': frontmatter.get('title', 'Untitled'),
                'file_path': str(main_paper),
                'frontmatter': frontmatter
            }
        
        return None
    
    def should_skip_path(self, path: Path) -> bool:
        """Check if path should be skipped."""
        path_parts = path.parts
        return any(skip in path_parts for skip in SKIP_FILES)
    
    def process_all_markdown_files(self):
        """Process all markdown files in the vault."""
        print(f"\n🔍 Scanning vault: {self.vault_path}")
        
        # Find all markdown files
        all_md_files = []
        for md_file in self.vault_path.rglob('*.md'):
            if not self.should_skip_path(md_file):
                all_md_files.append(md_file)
        
        print(f"📊 Found {len(all_md_files)} markdown files")
        print("=" * 80)
        
        # Process each file
        for md_file in sorted(all_md_files):
            self.process_markdown_file(md_file)
            self.stats['notes_processed'] += 1
        
        print("\n" + "=" * 80)
        print("📊 PROCESSING COMPLETE")
        print("=" * 80)
        print(f"Total files processed: {self.stats['notes_processed']}")
        print(f"UUIDs generated: {self.stats['uuids_generated']}")
        print(f"YAML created: {self.stats['yaml_created']}")
        print(f"YAML updated: {self.stats['yaml_updated']}")
        print(f"Errors: {self.stats['errors']}")
    
    def process_papers_for_db(self):
        """Process paper folders for database sync."""
        if not self.db_sync or not self.conn:
            return
        
        papers_path = self.vault_path / '03_PUBLICATIONS' / 'COMPLETE_LOGOS_PAPERS_FINAL'
        
        if not papers_path.exists():
            print(f"⚠️ Papers path not found: {papers_path}")
            return
        
        paper_folders = sorted([
            d for d in papers_path.iterdir()
            if d.is_dir() and PAPER_PATTERN.match(d.name)
        ])
        
        print(f"\n📚 Found {len(paper_folders)} paper folders for DB sync")
        
        for folder in paper_folders:
            paper_data = self.process_paper_folder(folder)
            if paper_data and self.conn:
                self.sync_paper_to_db(paper_data)
    
    def sync_paper_to_db(self, paper_data: dict):
        """Sync paper metadata to PostgreSQL."""
        if not self.conn:
            return
        
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO papers.theophysics_papers (
                    paper_uuid, paper_number, paper_code, title,
                    status, file_path, yaml_frontmatter, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s::jsonb, NOW()
                )
                ON CONFLICT (paper_uuid) DO UPDATE SET
                    title = EXCLUDED.title,
                    status = EXCLUDED.status,
                    yaml_frontmatter = EXCLUDED.yaml_frontmatter,
                    updated_at = NOW()
            """, (
                paper_data['paper_uuid'],
                paper_data['paper_number'],
                paper_data['paper_code'],
                paper_data['title'],
                paper_data['frontmatter'].get('status', 'draft'),
                paper_data['file_path'],
                yaml.dump(paper_data['frontmatter'])
            ))
            
            self.conn.commit()
            print(f"   ✅ Synced to database")
            
        except Exception as e:
            self.conn.rollback()
            print(f"   ❌ Database sync failed: {e}")
        finally:
            cursor.close()


def main():
    parser = argparse.ArgumentParser(description='Generate UUIDs for all Theophysics vault content')
    parser.add_argument('--vault-path', required=True, help='Path to vault root')
    parser.add_argument('--dry-run', action='store_true', help='Don\'t write to files or database')
    parser.add_argument('--db-sync', action='store_true', help='Sync papers to PostgreSQL database')
    
    args = parser.parse_args()
    
    print("🚀 Theophysics Vault UUID Generator")
    print("=" * 80)
    print(f"Vault: {args.vault_path}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"Database Sync: {'ENABLED' if args.db_sync else 'DISABLED'}")
    print("=" * 80)
    
    if args.dry_run:
        print("\n⚠️ DRY RUN MODE - No changes will be made\n")
        return
    
    generator = TheophysicsVaultUUIDGenerator(args.vault_path, DB_CONFIG, args.db_sync)
    
    # Process all markdown files
    generator.process_all_markdown_files()
    
    # Optionally sync papers to database
    if args.db_sync:
        if generator.connect_db():
            generator.process_papers_for_db()
            generator.close_db()

if __name__ == '__main__':
    main()
