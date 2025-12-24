"""
Paper Exporter - Exports papers with only referenced images
Creates self-contained vault slices for monthly releases
"""

import re
import shutil
from pathlib import Path
from typing import List, Set
import uuid as uuid_lib


class PaperExporter:
    """Exports papers with only referenced assets."""
    
    def __init__(self, vault_root: Path, canonical_images: Path):
        """
        Initialize exporter.
        
        Args:
            vault_root: Root of your private vault
            canonical_images: Path to 00_CANONICAL/Images/
        """
        self.vault_root = Path(vault_root)
        self.canonical_images = Path(canonical_images)
        self.export_root = self.vault_root / "EXPORTS"
        self.export_root.mkdir(exist_ok=True)
    
    def find_image_references(self, paper_content: str) -> Set[str]:
        """
        Find all image UUIDs referenced in paper.
        
        Returns:
            Set of UUIDs (without IMG- prefix or extension)
        """
        # Pattern: ![[00_CANONICAL/Images/IMG-uuid.png]]
        pattern = r'!\[\[.*?/IMG-([a-f0-9-]+)\.(png|jpg|jpeg|svg|gif)\]\]'
        matches = re.findall(pattern, paper_content, re.IGNORECASE)
        
        uuids = set()
        for uuid_match, ext in matches:
            uuids.add(uuid_match.lower())
        
        return uuids
    
    def find_explanation_references(self, paper_content: str) -> Set[str]:
        """Find all explanation file UUIDs referenced."""
        pattern = r'\[.*?\]\(.*?/IMG-([a-f0-9-]+)-explanation\.md\)'
        matches = re.findall(pattern, paper_content, re.IGNORECASE)
        return {m.lower() for m in matches}
    
    def copy_image(self, image_uuid: str, output_images_folder: Path) -> bool:
        """Copy image file to export folder."""
        # Try different extensions
        for ext in ['png', 'jpg', 'jpeg', 'svg', 'gif']:
            source = self.canonical_images / f"IMG-{image_uuid}.{ext}"
            if source.exists():
                dest = output_images_folder / f"IMG-{image_uuid}.{ext}"
                shutil.copy2(source, dest)
                return True
        return False
    
    def copy_explanation(self, image_uuid: str, output_images_folder: Path) -> bool:
        """Copy explanation file if it exists."""
        source = self.canonical_images / f"IMG-{image_uuid}-explanation.md"
        if source.exists():
            dest = output_images_folder / f"IMG-{image_uuid}-explanation.md"
            shutil.copy2(source, dest)
            return True
        return False
    
    def rewrite_links(self, content: str) -> str:
        """Rewrite canonical paths to relative paths."""
        # Rewrite image links
        content = re.sub(
            r'!\[\[.*?/IMG-([a-f0-9-]+)\.(png|jpg|jpeg|svg|gif)\]\]',
            r'![[Images/IMG-\1.\2]]',
            content,
            flags=re.IGNORECASE
        )
        
        # Rewrite explanation links
        content = re.sub(
            r'\[([^\]]+)\]\(.*?/IMG-([a-f0-9-]+)-explanation\.md\)',
            r'[\1](Images/IMG-\2-explanation.md)',
            content,
            flags=re.IGNORECASE
        )
        
        return content
    
    def clean_metadata(self, content: str) -> str:
        """Remove internal-only metadata."""
        # Remove concept_uuid if present
        content = re.sub(r'concept_uuid:\s*[^\n]+\n', '', content)
        
        # Remove logic_layer if present
        if 'logic_layer:' in content:
            # Remove entire logic_layer block (simplified)
            content = re.sub(r'logic_layer:.*?(?=\n\w+:|$)', '', content, flags=re.DOTALL)
        
        # Remove internal-only tags
        content = re.sub(r'tags:\s*\[.*?internal.*?\]', '', content, flags=re.IGNORECASE)
        
        return content
    
    def export_paper(
        self,
        paper_path: Path,
        paper_name: str,
        clean_metadata: bool = True
    ) -> Path:
        """
        Export a paper with only referenced images.
        
        Args:
            paper_path: Path to paper markdown file
            paper_name: Name for export folder (e.g., "Paper-01")
            clean_metadata: Whether to remove internal metadata
        
        Returns:
            Path to export folder
        """
        # Read paper
        paper_content = paper_path.read_text(encoding='utf-8')
        
        # Find referenced images
        image_uuids = self.find_image_references(paper_content)
        explanation_uuids = self.find_explanation_references(paper_content)
        
        # Create export folder
        export_folder = self.export_root / paper_name
        export_folder.mkdir(exist_ok=True)
        
        # Create Images subfolder
        images_folder = export_folder / "Images"
        images_folder.mkdir(exist_ok=True)
        
        # Copy images
        copied_images = []
        for img_uuid in image_uuids:
            if self.copy_image(img_uuid, images_folder):
                copied_images.append(img_uuid)
                # Also copy explanation if referenced
                if img_uuid in explanation_uuids:
                    self.copy_explanation(img_uuid, images_folder)
        
        # Rewrite links
        exported_content = self.rewrite_links(paper_content)
        
        # Clean metadata if requested
        if clean_metadata:
            exported_content = self.clean_metadata(exported_content)
        
        # Write exported paper
        exported_paper = export_folder / f"{paper_name}.md"
        exported_paper.write_text(exported_content, encoding='utf-8')
        
        # Create README
        readme = export_folder / "README.md"
        readme.write_text(f"""# {paper_name}

This is a self-contained Obsidian vault slice containing:
- {paper_name}.md (the paper)
- Images/ (only images used in this paper)

## Usage

1. Open this folder in Obsidian
2. All images and links are self-contained
3. No external dependencies

## Images Included

{len(copied_images)} images:
{chr(10).join(f'- IMG-{uuid}' for uuid in sorted(copied_images))}
""")
        
        print(f"✅ Exported {paper_name}")
        print(f"   Images copied: {len(copied_images)}")
        print(f"   Export folder: {export_folder}")
        
        return export_folder
    
    def create_incremental_update(
        self,
        paper_path: Path,
        paper_name: str,
        existing_vault: Path
    ) -> Path:
        """
        Create incremental update for existing vault.
        Only adds new images, doesn't duplicate existing ones.
        
        Args:
            paper_path: Path to new paper
            paper_name: Name of new paper
            existing_vault: Path to reader's existing vault
        
        Returns:
            Path to update package
        """
        # Find what images already exist
        existing_images_folder = existing_vault / "Images"
        existing_uuids = set()
        if existing_images_folder.exists():
            for img_file in existing_images_folder.glob("IMG-*.png"):
                # Extract UUID from filename
                match = re.search(r'IMG-([a-f0-9-]+)\.', img_file.name)
                if match:
                    existing_uuids.add(match.group(1).lower())
        
        # Read new paper
        paper_content = paper_path.read_text(encoding='utf-8')
        needed_uuids = self.find_image_references(paper_content)
        
        # Only copy NEW images
        new_uuids = needed_uuids - existing_uuids
        
        # Create update package
        update_folder = self.export_root / f"{paper_name}-UPDATE"
        update_folder.mkdir(exist_ok=True)
        
        images_folder = update_folder / "Images"
        images_folder.mkdir(exist_ok=True)
        
        # Copy only new images
        for img_uuid in new_uuids:
            self.copy_image(img_uuid, images_folder)
            self.copy_explanation(img_uuid, images_folder)
        
        # Export paper
        exported_content = self.rewrite_links(paper_content)
        exported_content = self.clean_metadata(exported_content)
        
        papers_folder = update_folder / "Papers"
        papers_folder.mkdir(exist_ok=True)
        (papers_folder / f"{paper_name}.md").write_text(exported_content, encoding='utf-8')
        
        # Create update instructions
        instructions = update_folder / "UPDATE_INSTRUCTIONS.md"
        instructions.write_text(f"""# Update Instructions for {paper_name}

## What's New

- New paper: {paper_name}.md
- New images: {len(new_uuids)} images added to your Images/ folder

## How to Update

1. Copy {paper_name}.md to your Papers/ folder
2. Copy all files from Images/ to your Images/ folder
3. Done! Your vault now includes this paper.

## Images Added

{chr(10).join(f'- IMG-{uuid}' for uuid in sorted(new_uuids))}
""")
        
        print(f"✅ Created incremental update for {paper_name}")
        print(f"   New images: {len(new_uuids)}")
        print(f"   Update package: {update_folder}")
        
        return update_folder


# Example usage
if __name__ == "__main__":
    # Configure paths
    VAULT_ROOT = Path("D:/THEOPHYSICS_MASTER")
    CANONICAL_IMAGES = VAULT_ROOT / "00_CANONICAL" / "Images"
    
    exporter = PaperExporter(VAULT_ROOT, CANONICAL_IMAGES)
    
    # Export Paper 01
    paper_01 = VAULT_ROOT / "03_PUBLICATIONS" / "COMPLETE_LOGOS_PAPERS_FINAL" / "P01-Logos-Principle" / "Paper-1-The-Logos-Principle-CANONICAL-CURSOR.md"
    
    if paper_01.exists():
        export_folder = exporter.export_paper(paper_01, "Paper-01")
        print(f"\n📦 Export ready: {export_folder}")
        print("   Give this folder to your readers!")
    else:
        print(f"Paper not found: {paper_01}")

