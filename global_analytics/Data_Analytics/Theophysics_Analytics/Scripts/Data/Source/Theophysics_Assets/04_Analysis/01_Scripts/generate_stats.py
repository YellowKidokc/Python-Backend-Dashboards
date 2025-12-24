"""
Local Stats Generator - Generate comprehensive statistics for a single paper
Part of the Unified Research Analytics System
"""

import re
import yaml
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import Counter
import math


class LocalStatsGenerator:
    """Generate comprehensive statistics for a single markdown paper."""
    
    def __init__(self, vault_root: Path, config_path: Optional[Path] = None):
        """
        Initialize stats generator.
        
        Args:
            vault_root: Root of the Obsidian vault
            config_path: Path to config.yaml (optional)
        """
        self.vault_root = Path(vault_root)
        
        # Load config
        if config_path and config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
        else:
            self.config = {}
        
        self.stats_folder = self.vault_root / "Stats" / "Local"
        self.stats_folder.mkdir(parents=True, exist_ok=True)
        
        # Exclude patterns
        self.exclude_patterns = self.config.get('scanning', {}).get('exclude_patterns', [])
    
    def generate(self, paper_path: Path) -> Dict[str, Any]:
        """
        Generate all statistics for a paper.
        
        Args:
            paper_path: Path to the markdown file
        
        Returns:
            Complete statistics dictionary
        """
        paper_path = Path(paper_path)
        if not paper_path.exists():
            raise FileNotFoundError(f"Paper not found: {paper_path}")
        
        # Read paper
        content = paper_path.read_text(encoding='utf-8')
        
        # Extract frontmatter
        frontmatter = self._extract_frontmatter(content)
        
        # Remove frontmatter from content for analysis
        content_no_fm = self._remove_frontmatter(content)
        
        # Generate all stat categories
        stats = {
            "metadata": self._generate_metadata(paper_path),
            "text": self._generate_text_stats(content_no_fm),
            "links": self._generate_link_stats(content_no_fm),
            "entities": self._generate_entity_stats(content_no_fm, frontmatter),
            "images": self._generate_image_stats(content_no_fm),
            "math": self._generate_math_stats(content_no_fm),
            "theology": self._generate_theology_stats(content_no_fm),
            "logic": self._generate_logic_stats(frontmatter),
            "history": self._generate_history_stats(paper_path)
        }
        
        return stats
    
    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extract YAML frontmatter."""
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1)) or {}
            except:
                return {}
        return {}
    
    def _remove_frontmatter(self, content: str) -> str:
        """Remove YAML frontmatter from content."""
        return re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    def _generate_metadata(self, paper_path: Path) -> Dict[str, Any]:
        """Generate basic metadata."""
        return {
            "filename": paper_path.name,
            "paper_id": paper_path.stem,
            "file_size": paper_path.stat().st_size,
            "generated_at": datetime.now().isoformat(),
            "relative_path": str(paper_path.relative_to(self.vault_root))
        }
    
    def _generate_text_stats(self, content: str) -> Dict[str, Any]:
        """Generate text statistics."""
        # Word count
        words = re.findall(r'\b\w+\b', content)
        word_count = len(words)
        unique_words = len(set(w.lower() for w in words))
        
        # Sentence count
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)
        
        # Paragraph count
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        paragraph_count = len(paragraphs)
        
        # Character count
        char_count = len(content)
        
        # Reading time (assume 200 words/min)
        reading_time_min = word_count / 200
        
        # Average sentence length
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Longest sentence
        longest_sentence = max([len(s.split()) for s in sentences]) if sentences else 0
        
        # Lexical density (unique / total)
        lexical_density = (unique_words / word_count * 100) if word_count > 0 else 0
        
        return {
            "total_word_count": word_count,
            "unique_word_count": unique_words,
            "character_count": char_count,
            "sentence_count": sentence_count,
            "paragraph_count": paragraph_count,
            "reading_time_minutes": round(reading_time_min, 2),
            "speaking_time_minutes": round(reading_time_min * 2, 2),
            "average_sentence_length": round(avg_sentence_length, 2),
            "longest_sentence_words": longest_sentence,
            "lexical_density_percent": round(lexical_density, 2),
            "compression_ratio": round(char_count / word_count, 2) if word_count > 0 else 0
        }
    
    def _generate_link_stats(self, content: str) -> Dict[str, Any]:
        """Generate link statistics."""
        # Wikilinks: [[link]]
        wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
        
        # External URLs
        urls = re.findall(r'https?://[^\s\)]+', content)
        
        # Block references: ^blockid
        block_refs = re.findall(r'\^([a-zA-Z0-9]+)', content)
        
        return {
            "internal_link_count": len(wikilinks),
            "unique_internal_links": len(set(wikilinks)),
            "external_url_count": len(urls),
            "block_reference_count": len(block_refs),
            "total_links": len(wikilinks) + len(urls)
        }
    
    def _generate_entity_stats(self, content: str, frontmatter: Dict) -> Dict[str, Any]:
        """Generate entity statistics."""
        # Tags from frontmatter
        tags = frontmatter.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        
        # Inline tags: #tag
        inline_tags = re.findall(r'#([a-zA-Z0-9_/-]+)', content)
        
        all_tags = list(set(tags + inline_tags))
        
        # UUID references
        uuids = re.findall(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', content)
        
        return {
            "tag_count": len(all_tags),
            "unique_tags": len(set(all_tags)),
            "tags": all_tags,
            "uuid_count": len(set(uuids)),
            "concept_mentions": len(re.findall(r'\b(Logos|Grace|Entropy|Coherence|Trinity)\b', content))
        }
    
    def _generate_image_stats(self, content: str) -> Dict[str, Any]:
        """Generate image statistics."""
        # Markdown images: ![alt](path)
        md_images = re.findall(r'!\[([^\]]*)\]\(([^\)]+)\)', content)
        
        # Wikilink images: ![[image.png]]
        wiki_images = re.findall(r'!\[\[([^\]]+)\]\]', content)
        
        total_images = len(md_images) + len(wiki_images)
        
        # Image UUIDs
        image_uuids = re.findall(r'IMG-([a-f0-9-]+)\.(png|jpg|jpeg|svg|gif)', content)
        
        return {
            "embedded_image_count": total_images,
            "markdown_images": len(md_images),
            "wikilink_images": len(wiki_images),
            "unique_image_uuids": len(set(u[0] for u in image_uuids))
        }
    
    def _generate_math_stats(self, content: str) -> Dict[str, Any]:
        """Generate math statistics."""
        # LaTeX math blocks: $$ ... $$
        math_blocks = re.findall(r'\$\$(.*?)\$\$', content, re.DOTALL)
        
        # Inline math: $ ... $
        inline_math = re.findall(r'\$([^\$]+)\$', content)
        
        # Common math symbols
        symbols = re.findall(r'[∫∑∏√∂∇∆Ψχλμνπσφω]', content)
        
        # Greek letters in LaTeX
        greek = re.findall(r'\\(alpha|beta|gamma|delta|epsilon|chi|psi|phi|theta)', content)
        
        return {
            "math_block_count": len(math_blocks),
            "inline_math_count": len(inline_math),
            "unique_symbols": len(set(symbols + greek)),
            "total_math_elements": len(math_blocks) + len(inline_math)
        }
    
    def _generate_theology_stats(self, content: str) -> Dict[str, Any]:
        """Generate theology-specific statistics."""
        # Trinity mentions
        father_count = len(re.findall(r'\bFather\b', content))
        son_count = len(re.findall(r'\bSon\b', content))
        spirit_count = len(re.findall(r'\b(Spirit|Holy Spirit)\b', content))
        
        # Theophysics terms
        logos_count = len(re.findall(r'\bLogos\b', content))
        grace_count = len(re.findall(r'\b(Grace|grace)\b', content))
        sin_count = len(re.findall(r'\b(sin|Sin|entropy)\b', content))
        
        # Trinity symmetry (how balanced is usage?)
        trinity_total = father_count + son_count + spirit_count
        trinity_balance = 0
        if trinity_total > 0:
            expected = trinity_total / 3
            variance = sum([(x - expected)**2 for x in [father_count, son_count, spirit_count]]) / 3
            trinity_balance = 1 - (math.sqrt(variance) / expected) if expected > 0 else 0
        
        return {
            "trinity_father_count": father_count,
            "trinity_son_count": son_count,
            "trinity_spirit_count": spirit_count,
            "trinity_total": trinity_total,
            "trinity_symmetry_score": round(trinity_balance, 3),
            "logos_mentions": logos_count,
            "grace_mentions": grace_count,
            "sin_entropy_mentions": sin_count
        }
    
    def _generate_logic_stats(self, frontmatter: Dict) -> Dict[str, Any]:
        """Generate logic progression statistics."""
        logic_layer = frontmatter.get('logic_layer', {})
        
        if not logic_layer:
            return {
                "has_logic_layer": False
            }
        
        branches = logic_layer.get('branches', [])
        bridges = logic_layer.get('bridges', [])
        skeleton = logic_layer.get('skeleton', {})
        statements = logic_layer.get('condensed_statements', [])
        
        return {
            "has_logic_layer": True,
            "branch_count": len(branches),
            "bridge_count": len(bridges),
            "skeleton_section_count": len(skeleton.get('sections', [])),
            "condensed_statement_count": len(statements),
            "seed_defined": bool(logic_layer.get('seed'))
        }
    
    def _generate_history_stats(self, paper_path: Path) -> Dict[str, Any]:
        """Generate file history statistics."""
        stat = paper_path.stat()
        
        return {
            "created_timestamp": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_timestamp": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "file_size_bytes": stat.st_size
        }
    
    def save(self, paper_path: Path, stats: Dict[str, Any]) -> Path:
        """
        Save statistics to JSON file.
        
        Args:
            paper_path: Path to the paper
            stats: Statistics dictionary
        
        Returns:
            Path to saved stats file
        """
        paper_name = paper_path.stem
        stats_file = self.stats_folder / f"{paper_name}.stats.json"
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Stats saved: {stats_file}")
        return stats_file
    
    def generate_and_save(self, paper_path: Path) -> Path:
        """Generate and save statistics in one step."""
        stats = self.generate(paper_path)
        return self.save(paper_path, stats)


# CLI Interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python generate_stats.py <paper.md>")
        print("   or: python generate_stats.py --all")
        sys.exit(1)
    
    vault_root = Path("D:/THEOPHYSICS_MASTER")
    generator = LocalStatsGenerator(vault_root)
    
    # Load config
    config_file = Path(__file__).parent / "config.yaml"
    generator = LocalStatsGenerator(vault_root, config_file)
    
    if sys.argv[1] == "--all":
        # Generate stats for all papers in included folders
        include_folders = generator.config.get('scanning', {}).get('include_folders', [])
        exclude_patterns = generator.exclude_patterns
        
        if not include_folders:
            include_folders = ["03_PUBLICATIONS/COMPLETE_LOGOS_PAPERS_FINAL"]
        
        paper_files = []
        for folder in include_folders:
            folder_path = vault_root / folder
            if folder_path.exists():
                papers = list(folder_path.rglob("Paper-*.md"))
                # Filter out excluded patterns
                for paper in papers:
                    excluded = False
                    for pattern in exclude_patterns:
                        if pattern.replace('**/', '') in str(paper):
                            excluded = True
                            break
                    if not excluded:
                        paper_files.append(paper)
        
        print(f"Found {len(paper_files)} papers (after exclusions)")
        for paper in paper_files:
            try:
                generator.generate_and_save(paper)
            except Exception as e:
                print(f"❌ Error processing {paper.name}: {e}")
    else:
        # Generate stats for specific paper
        paper_path = Path(sys.argv[1])
        generator.generate_and_save(paper_path)

