"""
Picture Master Manager
Manages a master sheet of all pictures across the 12 Logos Papers.

Features:
- Tracks all pictures with descriptions, links, and metadata
- Generates clickable links for papers
- Maintains picture inventory per paper
- Tracks unused pictures
- Exports to YAML/JSON for vault integration
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class PictureEntry:
    """Represents a single picture entry in the master sheet."""
    paper_id: str  # P01, P02, etc.
    paper_name: str  # Full paper name
    figure_number: str  # Figure 1, Figure 2, etc.
    filename: str  # Current filename
    new_filename: str  # Proposed standardized filename
    path: str  # Relative path from paper root
    description: str  # Detailed description
    context: str  # Context/paragraph explaining the picture
    used: bool  # Whether currently used in paper
    chart_script: Optional[str] = None  # If rendered from chart script
    alt_text: str = ""  # Alt text for accessibility


class PictureMasterManager:
    """Manages the master picture registry."""
    
    def __init__(self, vault_root: Path):
        self.vault_root = Path(vault_root)
        self.papers_root = self.vault_root / "03_PUBLICATIONS" / "COMPLETE_LOGOS_PAPERS_FINAL"
        self.master_sheet_path = self.vault_root / "00_VAULT_SYSTEM" / "04_Analysis" / "07_Data" / "picture_master_sheet.yaml"
        self.pictures: Dict[str, List[PictureEntry]] = {}  # paper_id -> list of pictures
        
    def load_master_sheet(self) -> Dict:
        """Load existing master sheet if it exists."""
        if self.master_sheet_path.exists():
            with open(self.master_sheet_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def save_master_sheet(self):
        """Save master sheet to YAML."""
        self.master_sheet_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'last_updated': datetime.now().isoformat(),
            'papers': {}
        }
        
        for paper_id, pictures in self.pictures.items():
            data['papers'][paper_id] = [asdict(pic) for pic in pictures]
        
        with open(self.master_sheet_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"✅ Master sheet saved to: {self.master_sheet_path}")
    
    def scan_paper(self, paper_id: str) -> List[PictureEntry]:
        """Scan a paper folder for all pictures."""
        paper_folder = self.papers_root / f"P{paper_id.zfill(2)}-*"
        paper_folders = list(self.papers_root.glob(f"P{paper_id.zfill(2)}-*"))
        
        if not paper_folders:
            print(f"⚠️  No folder found for {paper_id}")
            return []
        
        paper_folder = paper_folders[0]
        paper_name = paper_folder.name.replace(f"P{paper_id.zfill(2)}-", "")
        
        # Find CANONICAL markdown file
        canonical_files = list(paper_folder.glob("*CANONICAL.md"))
        if not canonical_files:
            print(f"⚠️  No CANONICAL.md found in {paper_folder.name}")
            return []
        
        canonical_file = canonical_files[0]
        
        # Scan for images in markdown
        pictures = []
        assets_folder = paper_folder / "_Assets" / "Images"
        
        if not assets_folder.exists():
            print(f"⚠️  No _Assets/Images folder in {paper_folder.name}")
            return []
        
        # Read markdown and extract image references
        with open(canonical_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        import re
        # Pattern: ![alt text](path)
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        matches = re.finditer(image_pattern, content)
        
        figure_num = 1
        for match in matches:
            alt_text = match.group(1)
            img_path = match.group(2)
            
            # Resolve path
            if img_path.startswith('_Assets'):
                full_path = paper_folder / img_path
            elif img_path.startswith('/'):
                full_path = self.vault_root / img_path.lstrip('/')
            else:
                full_path = paper_folder / img_path
            
            if full_path.exists():
                filename = full_path.name
                # Generate standardized filename
                new_filename = f"P{paper_id.zfill(2)}-{paper_name}-Fig{figure_num:02d}-{self._sanitize_filename(alt_text)}.png"
                
                entry = PictureEntry(
                    paper_id=f"P{paper_id.zfill(2)}",
                    paper_name=paper_name,
                    figure_number=f"Figure {figure_num}",
                    filename=filename,
                    new_filename=new_filename,
                    path=str(img_path),
                    description="",  # To be filled manually
                    context="",  # To be filled manually
                    used=True,
                    alt_text=alt_text
                )
                pictures.append(entry)
                figure_num += 1
        
        # Also scan for unused images in assets folder
        all_images = list(assets_folder.glob("*.png")) + list(assets_folder.glob("*.jpg")) + list(assets_folder.glob("*.svg"))
        used_filenames = {pic.filename for pic in pictures}
        
        for img_file in all_images:
            if img_file.name not in used_filenames:
                entry = PictureEntry(
                    paper_id=f"P{paper_id.zfill(2)}",
                    paper_name=paper_name,
                    figure_number="Unused",
                    filename=img_file.name,
                    new_filename="",  # Will be determined later
                    path=f"_Assets/Images/{img_file.name}",
                    description="Unused image",
                    context="",
                    used=False,
                    alt_text=""
                )
                pictures.append(entry)
        
        return pictures
    
    def _sanitize_filename(self, text: str) -> str:
        """Sanitize text for use in filename."""
        import re
        # Remove special chars, replace spaces with hyphens
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text[:50]  # Limit length
    
    def generate_picture_links_markdown(self, paper_id: str) -> str:
        """Generate markdown with clickable picture links and descriptions."""
        if paper_id not in self.pictures:
            return ""
        
        pictures = [p for p in self.pictures[paper_id] if p.used]
        if not pictures:
            return ""
        
        markdown = f"## Picture Registry - {paper_id}\n\n"
        
        for pic in pictures:
            markdown += f"### {pic.figure_number}: {pic.alt_text or pic.filename}\n\n"
            markdown += f"**File:** `{pic.filename}`\n\n"
            if pic.new_filename:
                markdown += f"**Standardized:** `{pic.new_filename}`\n\n"
            markdown += f"**Path:** `{pic.path}`\n\n"
            if pic.description:
                markdown += f"**Description:** {pic.description}\n\n"
            if pic.context:
                markdown += f"**Context:** {pic.context}\n\n"
            markdown += f"![{pic.alt_text or pic.filename}]({pic.path})\n\n"
            markdown += "---\n\n"
        
        return markdown
    
    def add_picture(self, paper_id: str, picture: PictureEntry):
        """Add a picture to the registry."""
        if paper_id not in self.pictures:
            self.pictures[paper_id] = []
        self.pictures[paper_id].append(picture)
    
    def update_picture(self, paper_id: str, filename: str, **updates):
        """Update picture metadata."""
        if paper_id not in self.pictures:
            return False
        
        for pic in self.pictures[paper_id]:
            if pic.filename == filename:
                for key, value in updates.items():
                    if hasattr(pic, key):
                        setattr(pic, key, value)
                return True
        return False


def main():
    """CLI interface for picture management."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Manage picture master sheet')
    parser.add_argument('--scan', help='Scan a paper (e.g., P01)')
    parser.add_argument('--paper', help='Paper ID to work with')
    parser.add_argument('--save', action='store_true', help='Save master sheet')
    parser.add_argument('--export', help='Export format (markdown, json, yaml)')
    
    args = parser.parse_args()
    
    vault_root = Path(r"D:\THEOPHYSICS_MASTER")
    manager = PictureMasterManager(vault_root)
    
    # Load existing data
    existing = manager.load_master_sheet()
    if existing and 'papers' in existing:
        for paper_id, pics_data in existing['papers'].items():
            manager.pictures[paper_id] = [PictureEntry(**pic) for pic in pics_data]
    
    if args.scan:
        paper_id = args.scan.replace('P', '').zfill(2)
        print(f"Scanning {args.scan}...")
        pictures = manager.scan_paper(paper_id)
        manager.pictures[f"P{paper_id}"] = pictures
        print(f"Found {len(pictures)} pictures ({sum(1 for p in pictures if p.used)} used, {sum(1 for p in pictures if not p.used)} unused)")
        
        if args.save:
            manager.save_master_sheet()
    
    if args.export and args.paper:
        paper_id = args.paper.replace('P', '').zfill(2)
        if args.export == 'markdown':
            md = manager.generate_picture_links_markdown(f"P{paper_id}")
            output_path = vault_root / "00_VAULT_SYSTEM" / "04_Analysis" / "07_Data" / f"P{paper_id}_pictures.md"
            output_path.write_text(md, encoding='utf-8')
            print(f"✅ Exported to {output_path}")
        elif args.export == 'json':
            # Export JSON
            pass
        elif args.export == 'yaml':
            manager.save_master_sheet()


if __name__ == '__main__':
    main()

