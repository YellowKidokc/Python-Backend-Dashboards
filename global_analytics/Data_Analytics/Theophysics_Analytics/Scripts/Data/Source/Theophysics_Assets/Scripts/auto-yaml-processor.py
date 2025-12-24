#!/usr/bin/env python3
"""
THEOPHYSICS AUTO-YAML PROCESSOR
Automatically adds comprehensive YAML frontmatter to all notes with AI-powered tagging

Features:
- Scans entire vault
- Adds YAML to notes without frontmatter
- Uses OpenAI to analyze content and auto-tag
- 4-domain publishing system (Private, Public, Research, Academia)
- Respects existing YAML
- Batch processing for efficiency
- Hidden YAML option (HTML comments)

Author: David Lowe + Claude
Version: 2.0
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import re
import yaml
import json
from typing import Dict, List, Optional, Tuple
import time

# Try to import OpenAI (will fall back to manual if not available)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI not installed. Run: pip install openai")
    print("   AI tagging will be skipped. Install to enable.")

class TheophysicsYAMLProcessor:
    def __init__(self, vault_path: str, openai_api_key: Optional[str] = None):
        self.vault_path = Path(vault_path)
        self.openai_api_key = openai_api_key
        self.client = None
        
        if OPENAI_AVAILABLE and openai_api_key:
            self.client = OpenAI(api_key=openai_api_key)
        
        # Statistics
        self.stats = {
            'processed': 0,
            'skipped': 0,
            'errors': 0,
            'ai_tagged': 0
        }
        
        # Theophysics tag ontology
        self.tag_ontology = {
            'pillars': ['physics', 'theology', 'math', 'consciousness'],
            'logos': ['master', 'force', 'decay', 'restore', 'state'],
            'theos': ['D_LOGOS', 'D_FATHER', 'D_SPIRIT', 'D_ADVERSARY'],
            'chi_vars': ['Negentropy', 'Entropy', 'Time', 'Knowledge', 
                        'Relationality', 'Quantum', 'Faith', 'Coherence']
        }
    
    def has_yaml_frontmatter(self, content: str) -> bool:
        """Check if file already has YAML frontmatter"""
        return content.strip().startswith('---') and '\n---' in content[3:]
    
    def extract_existing_yaml(self, content: str) -> Tuple[Optional[Dict], str]:
        """Extract existing YAML and body content"""
        if not self.has_yaml_frontmatter(content):
            return None, content
        
        match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if not match:
            return None, content
        
        yaml_str = match.group(1)
        body = match.group(2)
        
        try:
            yaml_data = yaml.safe_load(yaml_str)
            return yaml_data, body
        except yaml.YAMLError as e:
            print(f"  ⚠️  Invalid YAML, will regenerate: {e}")
            return None, content
    
    def analyze_content_with_ai(self, title: str, content: str) -> Dict:
        """Use OpenAI to analyze content and suggest tags"""
        if not self.client:
            return self._fallback_analysis(content)
        
        try:
            prompt = f"""Analyze this Theophysics document and provide classification.

TITLE: {title}

CONTENT PREVIEW (first 2000 chars):
{content[:2000]}

Provide JSON with this structure:
{{
  "summary": "2-3 sentence summary",
  "key_points": ["point 1", "point 2", "point 3"],
  "main_concepts": ["concept 1", "concept 2"],
  "pillars": ["physics|theology|math|consciousness"],
  "logos": ["master|force|decay|restore|state"],
  "theos": ["D_LOGOS|D_FATHER|D_SPIRIT|D_ADVERSARY"],
  "chi_vars": ["Negentropy|Entropy|Time|Knowledge|etc"],
  "general_tags": ["tag1", "tag2"],
  "confidence": 0.85
}}

Only include tags that strongly apply. Return valid JSON only."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Fast and cheap for batch processing
                messages=[
                    {"role": "system", "content": "You are a Theophysics classification expert. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"  ⚠️  AI analysis failed: {e}")
            return self._fallback_analysis(content)
    
    def _fallback_analysis(self, content: str) -> Dict:
        """Simple keyword-based analysis when AI not available"""
        content_lower = content.lower()
        
        result = {
            "summary": "",
            "key_points": [],
            "main_concepts": [],
            "pillars": [],
            "logos": [],
            "theos": [],
            "chi_vars": [],
            "general_tags": [],
            "confidence": 0.5
        }
        
        # Simple keyword detection
        if any(word in content_lower for word in ['equation', 'physics', 'quantum', 'entropy']):
            result['pillars'].append('physics')
        if any(word in content_lower for word in ['god', 'grace', 'spirit', 'faith', 'scripture']):
            result['pillars'].append('theology')
        if any(word in content_lower for word in ['entropy', 'decay', 'sin', 'corruption']):
            result['logos'].append('decay')
        if any(word in content_lower for word in ['grace', 'restore', 'redemption', 'negentropy']):
            result['logos'].append('restore')
        
        return result
    
    def generate_yaml_frontmatter(self, file_path: Path, content: str, 
                                  existing_yaml: Optional[Dict] = None) -> Dict:
        """Generate comprehensive YAML frontmatter"""
        
        # Extract title
        title = existing_yaml.get('title', '') if existing_yaml else ''
        if not title:
            # Try first heading
            heading_match = re.search(r'^#+\s*(.+)', content, re.MULTILINE)
            title = heading_match.group(1).strip() if heading_match else file_path.stem
        
        # Determine default domain (everything starts private)
        publish_to = {
            'private': True,
            'public': False,
            'research': False,
            'academia': False
        }
        
        # Preserve existing publish settings
        if existing_yaml and 'publish_to' in existing_yaml:
            publish_to.update(existing_yaml['publish_to'])
        
        # Base YAML structure
        yaml_data = {
            'publish_to': publish_to,
            'title': title,
            'author': 'David Lowe',
            'created': existing_yaml.get('created', datetime.now().strftime('%Y-%m-%d')) if existing_yaml else datetime.now().strftime('%Y-%m-%d'),
            'updated': datetime.now().strftime('%Y-%m-%d'),
            'status': existing_yaml.get('status', 'draft') if existing_yaml else 'draft',
            'type': existing_yaml.get('type', 'note') if existing_yaml else 'note',
            'tags': existing_yaml.get('tags', []) if existing_yaml else [],
            'pillars': existing_yaml.get('pillars', []) if existing_yaml else [],
            'logos': existing_yaml.get('logos', []) if existing_yaml else [],
            'theos': existing_yaml.get('theos', []) if existing_yaml else [],
            'chi_vars': existing_yaml.get('chi_vars', []) if existing_yaml else [],
            'related_notes': existing_yaml.get('related_notes', []) if existing_yaml else [],
            'series': existing_yaml.get('series', '') if existing_yaml else '',
            'paper_number': existing_yaml.get('paper_number', 0) if existing_yaml else 0,
            'summary': existing_yaml.get('summary', '') if existing_yaml else '',
            'key_points': existing_yaml.get('key_points', []) if existing_yaml else [],
            'main_concepts': existing_yaml.get('main_concepts', []) if existing_yaml else [],
            'ai_processed': existing_yaml.get('ai_processed', False) if existing_yaml else False,
            'ai_confidence': existing_yaml.get('ai_confidence', 0.0) if existing_yaml else 0.0,
            'needs_review': existing_yaml.get('needs_review', False) if existing_yaml else False
        }
        
        # AI analysis (if not already processed)
        if self.client and not yaml_data['ai_processed']:
            print(f"  🤖 Running AI analysis...")
            ai_result = self.analyze_content_with_ai(title, content)
            
            # Merge AI results
            if ai_result['summary']:
                yaml_data['summary'] = ai_result['summary']
            if ai_result['key_points']:
                yaml_data['key_points'] = ai_result['key_points']
            if ai_result['main_concepts']:
                yaml_data['main_concepts'] = ai_result['main_concepts']
            
            # Add AI-suggested tags
            yaml_data['pillars'].extend([p for p in ai_result['pillars'] if p not in yaml_data['pillars']])
            yaml_data['logos'].extend([l for l in ai_result['logos'] if l not in yaml_data['logos']])
            yaml_data['theos'].extend([t for t in ai_result['theos'] if t not in yaml_data['theos']])
            yaml_data['chi_vars'].extend([c for c in ai_result['chi_vars'] if c not in yaml_data['chi_vars']])
            yaml_data['tags'].extend([t for t in ai_result['general_tags'] if t not in yaml_data['tags']])
            
            yaml_data['ai_processed'] = True
            yaml_data['ai_confidence'] = ai_result['confidence']
            
            self.stats['ai_tagged'] += 1
            time.sleep(0.5)  # Rate limiting
        
        return yaml_data
    
    def format_yaml_header(self, yaml_data: Dict, hidden: bool = False) -> str:
        """Format YAML as frontmatter string"""
        
        # Convert to YAML string
        yaml_str = yaml.dump(yaml_data, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        if hidden:
            # Wrap in HTML comments (hidden from reading view)
            return f"<!--\n---\n{yaml_str}---\n-->\n\n"
        else:
            # Standard frontmatter
            return f"---\n{yaml_str}---\n\n"
    
    def process_file(self, file_path: Path, hidden_yaml: bool = False, 
                     skip_existing: bool = True, dry_run: bool = False) -> bool:
        """Process a single markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for existing YAML
            existing_yaml, body = self.extract_existing_yaml(content)
            
            if existing_yaml and skip_existing:
                print(f"⏭️  SKIP: {file_path.name} (already has YAML)")
                self.stats['skipped'] += 1
                return True
            
            # Generate YAML
            yaml_data = self.generate_yaml_frontmatter(file_path, body, existing_yaml)
            yaml_header = self.format_yaml_header(yaml_data, hidden_yaml)
            
            # Construct new content
            new_content = yaml_header + body.lstrip()
            
            # Write file (unless dry run)
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            
            # Display info
            domains = [k for k, v in yaml_data['publish_to'].items() if v]
            domains_str = ', '.join(domains)
            
            print(f"✅ PROCESSED: {file_path.name}")
            print(f"   Title: {yaml_data['title']}")
            print(f"   Domains: {domains_str}")
            if yaml_data['ai_processed']:
                print(f"   AI Tagged: {len(yaml_data['pillars'])} pillars, {len(yaml_data['logos'])} logos (confidence: {yaml_data['ai_confidence']:.2f})")
            print()
            
            self.stats['processed'] += 1
            return True
            
        except Exception as e:
            print(f"❌ ERROR: {file_path.name} - {e}")
            self.stats['errors'] += 1
            return False
    
    def process_vault(self, hidden_yaml: bool = False, skip_existing: bool = True, 
                     dry_run: bool = True, exclude_dirs: List[str] = None):
        """Process entire vault"""
        
        print("=" * 70)
        print("THEOPHYSICS AUTO-YAML PROCESSOR")
        print("=" * 70)
        print(f"Vault: {self.vault_path}")
        print(f"Mode: {'DRY RUN (preview)' if dry_run else 'LIVE (will modify files)'}")
        print(f"Hidden YAML: {hidden_yaml}")
        print(f"Skip existing: {skip_existing}")
        print(f"AI Tagging: {'ENABLED ✓' if self.client else 'DISABLED (install openai)'}")
        print("=" * 70)
        print()
        
        # Default exclusions
        if exclude_dirs is None:
            exclude_dirs = ['.git', '.obsidian', '.trash', 'node_modules', '_gsdata_']
        
        # Find all markdown files
        md_files = []
        for md_file in self.vault_path.rglob('*.md'):
            # Skip excluded directories
            if any(excluded in md_file.parts for excluded in exclude_dirs):
                continue
            md_files.append(md_file)
        
        print(f"Found {len(md_files)} markdown files\n")
        
        # Process each file
        for md_file in md_files:
            self.process_file(md_file, hidden_yaml, skip_existing, dry_run)
        
        # Summary
        print("=" * 70)
        print("SUMMARY:")
        print(f"  ✅ Processed: {self.stats['processed']}")
        print(f"  ⏭️  Skipped: {self.stats['skipped']}")
        print(f"  ❌ Errors: {self.stats['errors']}")
        if self.client:
            print(f"  🤖 AI Tagged: {self.stats['ai_tagged']}")
        print(f"  📊 Total: {len(md_files)}")
        print("=" * 70)
        
        if dry_run:
            print("\n🔍 DRY RUN - No files were modified")
            print("   Review output, then run with dry_run=False")

def main():
    """Main execution"""
    
    # ===== CONFIGURATION =====
    VAULT_PATH = r"D:\THEOPHYSICS"
    OPENAI_API_KEY = None  # Set to your key or use environment variable
    
    # Get API key from environment if not set
    if not OPENAI_API_KEY:
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Options
    HIDDEN_YAML = False  # True = wrap in HTML comments (hidden in reading view)
    SKIP_EXISTING = True  # True = skip files that already have YAML
    DRY_RUN = True  # True = preview only, False = actually modify files
    
    EXCLUDE_DIRS = [
        '.git', 
        '.obsidian', 
        '.trash',
        'node_modules',
        '_gsdata_',
        'cloudflare-workers'
    ]
    
    # Initialize processor
    processor = TheophysicsYAMLProcessor(VAULT_PATH, OPENAI_API_KEY)
    
    # Run dry run first
    print("\n🔍 RUNNING DRY RUN (preview mode)...\n")
    processor.process_vault(
        hidden_yaml=HIDDEN_YAML,
        skip_existing=SKIP_EXISTING,
        dry_run=True,
        exclude_dirs=EXCLUDE_DIRS
    )
    
    # Ask for confirmation
    print("\n" + "=" * 70)
    response = input("Proceed with ACTUAL processing? This will modify files. (y/N): ")
    
    if response.lower() == 'y':
        print("\n⚙️  PROCESSING VAULT...\n")
        
        # Re-initialize to reset stats
        processor = TheophysicsYAMLProcessor(VAULT_PATH, OPENAI_API_KEY)
        processor.process_vault(
            hidden_yaml=HIDDEN_YAML,
            skip_existing=SKIP_EXISTING,
            dry_run=False,
            exclude_dirs=EXCLUDE_DIRS
        )
        
        print("\n✅ COMPLETE!")
        print("\nNext steps:")
        print("1. Review files in Obsidian")
        print("2. For public/research/academia publishing:")
        print("   - Open note and change publish_to settings")
        print("   - Set 'public: true' to publish publicly")
        print("   - Set 'research: true' for research archive")
        print("   - Set 'academia: true' for academic papers")
        print("3. Deploy to Cloudflare Pages when ready")
    else:
        print("\n❌ CANCELLED")

if __name__ == "__main__":
    main()

