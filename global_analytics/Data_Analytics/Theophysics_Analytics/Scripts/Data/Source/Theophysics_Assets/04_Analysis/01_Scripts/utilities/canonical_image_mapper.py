"""
Canonical Image Mapper
Maps canonical LGS-PC-01-* images from source folder to paper concepts.
These are the source of truth images that should be used in papers.
"""

from pathlib import Path
from typing import Dict, Optional


# Mapping of P01 concepts to canonical LGS-PC-01-* image names
P01_CANONICAL_MAP = {
    "Observer Creates Reality": "LGS-PC-01-ObserverCreatesReality-O5.png",
    "Information Foundation": "LGS-PC-01-InformationFoundation-O4.png",
    "Information Substrate": "LGS-PC01-information-substrate-03-17.png",
    "Self Referential": "LGS-PC-01-SelfReferential-O6.png",
    "Zero Divergence": "LGS-PC-01-ZeroDivergence-O7.png",
    "Vapor Ice Analogy": "LGS-PC-01-VaporToIce-O8.png",
    "Spacetime Curvature": "LGS-PC-01-SpacetimeCurvature-O1.png",
    "Superposition": "LGS-PC-01-Superposition-O9.png",
    "Three Stage Collapse": "LGS-PC-01-ThreeStageCollapse-O10.png",
    "Shared Reality": "LGS-PC-01-SharedReality-O11.png",
    "Entanglement": "LGS-PC-01-Entanglement-O12.png",
    "Universe Compressed Code": "LGS-PC-01-UniverseCompressedCode-O13.png",
    "Participatory Universe": "LGS-PC-01-ParticipatoryUniverse-O3.png",
    "Full Spectrum": "LGS-PC-01-FullSpectrum-O2.png",
    "Great Schism": "LGS-PC01-great-schism-01-17.png",
    "GR vs QM Chart": "LGS-PC01-gr-vs-qm-chart-MATH.png",
    "Von Neumann Chain": "LGS-PC01-von-neumann-chain-21-33.png",
    "Wave Collapse Mechanism": "LGS-PC01-wave-collapse-mechanism-11-17.png",
    "Coherence Functional": "LGS-PC01-coherence-functional-16-17.png",
}


def find_canonical_image(concept: str, source_folder: Path) -> Optional[Path]:
    """
    Find canonical image for a concept.
    
    Args:
        concept: Concept name/description
        source_folder: Path to Sonnet_4.5_Pictures folder
    
    Returns:
        Path to canonical image, or None
    """
    # Try exact match first
    for key, filename in P01_CANONICAL_MAP.items():
        if key.lower() in concept.lower():
            img_path = source_folder / filename
            if img_path.exists():
                return img_path
    
    # Try LGS-PC-01-* pattern
    concept_clean = concept.lower().replace(" ", "").replace("-", "").replace("_", "")
    for img_path in source_folder.glob("LGS-PC-01-*.png"):
        name_clean = img_path.stem.lower().replace("-", "").replace("_", "")
        if concept_clean in name_clean or name_clean in concept_clean:
            return img_path
    
    # Try LGS-PC01-* pattern
    for img_path in source_folder.glob("LGS-PC01-*.png"):
        name_clean = img_path.stem.lower().replace("-", "").replace("_", "")
        if concept_clean in name_clean or name_clean in concept_clean:
            return img_path
    
    return None


def copy_canonical_to_paper(canonical_path: Path, paper_folder: Path, new_name: Optional[str] = None) -> Path:
    """
    Copy canonical image to paper's asset folder.
    
    Args:
        canonical_path: Path to canonical image in source folder
        paper_folder: Path to paper folder
        new_name: Optional new filename (if None, uses original name)
    
    Returns:
        Path to copied image
    """
    import shutil
    
    assets_folder = paper_folder / "_Assets" / "Images"
    assets_folder.mkdir(parents=True, exist_ok=True)
    
    if new_name:
        dest_path = assets_folder / new_name
    else:
        dest_path = assets_folder / canonical_path.name
    
    shutil.copy2(canonical_path, dest_path)
    return dest_path


def update_paper_images(paper_id: str, source_folder: Path, papers_base: Path, dry_run: bool = True):
    """
    Update paper with canonical images from source folder.
    
    Args:
        paper_id: Paper ID (e.g., "P01")
        source_folder: Path to Sonnet_4.5_Pictures
        papers_base: Path to COMPLETE_LOGOS_PAPERS_FINAL
        dry_run: If True, only show what would be done
    """
    # Find paper folder
    paper_folders = list(papers_base.glob(f"{paper_id}-*"))
    if not paper_folders:
        print(f"❌ Paper {paper_id} not found")
        return
    
    paper_folder = paper_folders[0]
    paper_mds = list(paper_folder.glob("*CANONICAL.md"))
    if not paper_mds:
        print(f"❌ CANONICAL.md not found for {paper_id}")
        return
    
    paper_md = paper_mds[0]
    
    # Read paper content
    with open(paper_md, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all image references
    import re
    image_pattern = r'!\[([^\]]+)\]\(([^\)]+)\)'
    matches = list(re.finditer(image_pattern, content))
    
    updates = []
    for match in matches:
        alt_text = match.group(1)
        current_path = match.group(2)
        
        # Find canonical version
        canonical = find_canonical_image(alt_text, source_folder)
        
        if canonical:
            # Generate standardized name
            new_name = f"{paper_id}-{alt_text.replace(' ', '-').replace(':', '').replace(',', '')}.png"
            new_name = re.sub(r'[^\w\-\.]', '', new_name)
            
            updates.append({
                'alt_text': alt_text,
                'current': current_path,
                'canonical': canonical,
                'new_name': new_name,
                'match': match
            })
    
    # Show updates
    print(f"\n📊 Found {len(updates)} canonical images for {paper_id}:")
    for update in updates:
        print(f"\n  {update['alt_text']}")
        print(f"    Current: {update['current']}")
        print(f"    Canonical: {update['canonical'].name}")
        print(f"    New name: {update['new_name']}")
        
        if not dry_run:
            # Copy canonical image
            copied = copy_canonical_to_paper(update['canonical'], paper_folder, update['new_name'])
            print(f"    ✅ Copied to: {copied}")
            
            # Update markdown (would need to be done manually or with careful regex)
            # For now, just copy the files


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Map canonical images to papers')
    parser.add_argument('--paper', default='P01', help='Paper ID')
    parser.add_argument('--source', default=r'C:\Users\Yellowkid\Desktop\Sonnet_4.5_Pictures',
                       help='Source folder')
    parser.add_argument('--papers', default=r'D:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL',
                       help='Papers folder')
    parser.add_argument('--apply', action='store_true', help='Actually copy files (default is dry-run)')
    
    args = parser.parse_args()
    
    update_paper_images(
        args.paper,
        Path(args.source),
        Path(args.papers),
        dry_run=not args.apply
    )

