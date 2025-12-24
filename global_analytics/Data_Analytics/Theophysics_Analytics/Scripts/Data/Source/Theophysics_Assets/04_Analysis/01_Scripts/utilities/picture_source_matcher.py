"""
Picture Source Matcher
Cross-references the Sonnet_4.5_Pictures folder (source of truth) with paper asset folders
to find the best picture matches for concepts and ideas.

This ensures we're using the most representative images from the source of truth.
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from difflib import SequenceMatcher


class PictureSourceMatcher:
    def __init__(self, source_folder: Path, papers_base: Path):
        """
        Initialize matcher.
        
        Args:
            source_folder: Path to Sonnet_4.5_Pictures (source of truth)
            papers_base: Path to COMPLETE_LOGOS_PAPERS_FINAL folder
        """
        self.source_folder = Path(source_folder)
        self.papers_base = Path(papers_base)
        self.source_images = self._load_source_images()
    
    def _load_source_images(self) -> Dict[str, List[Path]]:
        """Load all images from source folder, organized by paper/concept."""
        images = {}
        
        # Scan all image files
        for img_path in self.source_folder.rglob("*.png"):
            if img_path.is_file():
                # Extract paper/concept identifiers
                name = img_path.stem.lower()
                
                # Check for paper identifiers (P01, P02, etc.)
                paper_match = re.search(r'p(\d{2})', name)
                if paper_match:
                    paper_id = f"P{paper_match.group(1).zfill(2)}"
                    if paper_id not in images:
                        images[paper_id] = []
                    images[paper_id].append(img_path)
                
                # Also index by concept keywords
                keywords = self._extract_keywords(name)
                for keyword in keywords:
                    if keyword not in images:
                        images[keyword] = []
                    images[keyword].append(img_path)
        
        return images
    
    def _extract_keywords(self, name: str) -> List[str]:
        """Extract concept keywords from image name."""
        keywords = []
        
        # Common concept patterns
        concepts = [
            'observer', 'reality', 'collapse', 'wave', 'quantum', 'coherence',
            'information', 'substrate', 'self-referential', 'divergence',
            'spacetime', 'curvature', 'superposition', 'entanglement',
            'participatory', 'universe', 'compressed', 'code', 'gravity',
            'grace', 'sin', 'entropy', 'consciousness', 'trinity', 'logos',
            'master', 'equation', 'field', 'schism', 'vapor', 'ice',
            'shared', 'spectrum', 'validation', 'protocol', 'moral', 'ethics',
            'hubble', 'tension', 'ruler', 'clock', 'timeline', 'epoch',
            'decay', 'restoration', 'light', 'truth', 'revelation'
        ]
        
        name_lower = name.lower()
        for concept in concepts:
            if concept in name_lower:
                keywords.append(concept)
        
        return keywords
    
    def find_best_match(self, concept: str, paper_id: str, current_image: Optional[Path] = None) -> Optional[Path]:
        """
        Find the best matching image from source folder for a given concept.
        
        Args:
            concept: Description of what the image should show
            paper_id: Paper identifier (e.g., "P01")
            current_image: Currently used image path (for comparison)
        
        Returns:
            Best matching image path from source folder, or None
        """
        concept_lower = concept.lower()
        
        # Search in paper-specific images first
        candidates = []
        if paper_id in self.source_images:
            candidates.extend(self.source_images[paper_id])
        
        # Search by keywords
        for keyword in self._extract_keywords(concept):
            if keyword in self.source_images:
                candidates.extend(self.source_images[keyword])
        
        if not candidates:
            return None
        
        # Score candidates by similarity to concept
        scored = []
        for candidate in set(candidates):  # Remove duplicates
            name = candidate.stem.lower()
            score = SequenceMatcher(None, concept_lower, name).ratio()
            
            # Boost score for LGS-PC-* files (canonical versions)
            if 'lgs-pc' in name or 'lgs-pc01' in name:
                score += 0.2
            
            # Boost score for paper-specific files
            if paper_id.lower() in name:
                score += 0.1
            
            scored.append((score, candidate))
        
        # Return best match
        scored.sort(reverse=True, key=lambda x: x[0])
        if scored and scored[0][0] > 0.3:  # Minimum similarity threshold
            return scored[0][1]
        
        return None
    
    def scan_paper(self, paper_id: str) -> Dict[str, Dict]:
        """
        Scan a paper and suggest better images from source folder.
        
        Args:
            paper_id: Paper identifier (e.g., "P01")
        
        Returns:
            Dictionary mapping figure numbers to suggestions
        """
        paper_folder = self.papers_base / f"{paper_id}-*"
        paper_folders = list(self.papers_base.glob(f"{paper_id}-*"))
        
        if not paper_folders:
            return {}
        
        paper_folder = paper_folders[0]
        paper_md = paper_folder / f"Paper-*-CANONICAL.md"
        paper_mds = list(paper_folder.glob("*CANONICAL.md"))
        
        if not paper_mds:
            return {}
        
        paper_md = paper_mds[0]
        
        # Parse paper for image references
        suggestions = {}
        
        with open(paper_md, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find all image references
            image_pattern = r'!\[([^\]]+)\]\(([^\)]+)\)'
            matches = re.finditer(image_pattern, content)
            
            for match in matches:
                alt_text = match.group(1)
                image_path = match.group(2)
                
                # Find better match from source
                better_match = self.find_best_match(alt_text, paper_id)
                
                if better_match:
                    suggestions[alt_text] = {
                        'current': image_path,
                        'suggested': better_match,
                        'suggested_relative': self._make_relative_path(better_match, paper_folder)
                    }
        
        return suggestions
    
    def _make_relative_path(self, source_path: Path, paper_folder: Path) -> str:
        """Convert absolute source path to relative path for paper folder."""
        # For now, return the filename - we'll copy the file
        return f"_Assets/Images/{source_path.name}"
    
    def copy_suggested_image(self, source_path: Path, paper_folder: Path) -> Path:
        """
        Copy suggested image to paper's asset folder.
        
        Args:
            source_path: Path to image in source folder
            paper_folder: Path to paper folder
        
        Returns:
            Path to copied image
        """
        assets_folder = paper_folder / "_Assets" / "Images"
        assets_folder.mkdir(parents=True, exist_ok=True)
        
        dest_path = assets_folder / source_path.name
        
        # Copy file
        import shutil
        shutil.copy2(source_path, dest_path)
        
        return dest_path


def main():
    """CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Match pictures from source folder to papers')
    parser.add_argument('--paper', help='Paper ID (e.g., P01) or "all"')
    parser.add_argument('--source', default=r'C:\Users\Yellowkid\Desktop\Sonnet_4.5_Pictures',
                       help='Path to source pictures folder')
    parser.add_argument('--papers', default=r'D:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL',
                       help='Path to papers folder')
    parser.add_argument('--copy', action='store_true', help='Copy suggested images to paper folders')
    
    args = parser.parse_args()
    
    matcher = PictureSourceMatcher(args.source, args.papers)
    
    if args.paper == "all":
        papers = [f"P{i:02d}" for i in range(1, 13)]
    elif args.paper:
        papers = [args.paper]
    else:
        papers = ["P01"]  # Default
    
    for paper_id in papers:
        print(f"\n📊 Scanning {paper_id}...")
        suggestions = matcher.scan_paper(paper_id)
        
        if suggestions:
            print(f"  Found {len(suggestions)} potential improvements:")
            for alt_text, data in suggestions.items():
                print(f"\n  Figure: {alt_text}")
                print(f"    Current: {data['current']}")
                print(f"    Suggested: {data['suggested'].name}")
                
                if args.copy:
                    paper_folders = list(Path(args.papers).glob(f"{paper_id}-*"))
                    if paper_folders:
                        copied = matcher.copy_suggested_image(data['suggested'], paper_folders[0])
                        print(f"    ✅ Copied to: {copied}")
        else:
            print(f"  ℹ️  No suggestions found")


if __name__ == '__main__':
    main()

