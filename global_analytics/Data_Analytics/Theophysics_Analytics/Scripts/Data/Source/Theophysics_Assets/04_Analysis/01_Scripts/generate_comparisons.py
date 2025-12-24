"""
Comparison Stats Generator - Compare multiple papers
Part of the Unified Research Analytics System
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import numpy as np


class ComparisonStatsGenerator:
    """Generate comparative statistics for multiple papers."""
    
    def __init__(self, vault_root: Path):
        """
        Initialize comparison generator.
        
        Args:
            vault_root: Root of the Obsidian vault
        """
        self.vault_root = Path(vault_root)
        self.local_stats_folder = self.vault_root / "Stats" / "Local"
        self.comparison_folder = self.vault_root / "Stats" / "Comparisons"
        self.comparison_folder.mkdir(parents=True, exist_ok=True)
    
    def load_paper_stats(self, paper_id: str) -> Dict[str, Any]:
        """Load local stats for a paper."""
        stats_file = self.local_stats_folder / f"{paper_id}.stats.json"
        if not stats_file.exists():
            raise FileNotFoundError(f"Stats not found: {stats_file}")
        
        with open(stats_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate(self, paper_ids: List[str]) -> Dict[str, Any]:
        """
        Generate comparison statistics for multiple papers.
        
        Args:
            paper_ids: List of paper IDs (filenames without extension)
        
        Returns:
            Comparison statistics dictionary
        """
        if len(paper_ids) < 2:
            raise ValueError("Need at least 2 papers to compare")
        
        # Load all stats
        all_stats = {}
        for paper_id in paper_ids:
            all_stats[paper_id] = self.load_paper_stats(paper_id)
        
        # Generate comparison
        comparison = {
            "metadata": self._generate_metadata(paper_ids),
            "papers": paper_ids,
            "per_paper_stats": all_stats,
            "comparative_metrics": self._generate_comparative_metrics(all_stats),
            "similarity_matrix": self._generate_similarity_matrix(all_stats),
            "rankings": self._generate_rankings(all_stats)
        }
        
        return comparison
    
    def _generate_metadata(self, paper_ids: List[str]) -> Dict[str, Any]:
        """Generate comparison metadata."""
        return {
            "comparison_id": "-".join(paper_ids),
            "paper_count": len(paper_ids),
            "generated_at": datetime.now().isoformat()
        }
    
    def _generate_comparative_metrics(self, all_stats: Dict[str, Dict]) -> Dict[str, Any]:
        """Generate comparative metrics across papers."""
        metrics = {}
        
        # Text metrics comparison
        metrics["text_comparison"] = {
            paper_id: {
                "word_count": stats["text"]["total_word_count"],
                "unique_words": stats["text"]["unique_word_count"],
                "reading_time": stats["text"]["reading_time_minutes"],
                "lexical_density": stats["text"]["lexical_density_percent"]
            }
            for paper_id, stats in all_stats.items()
        }
        
        # Math density comparison
        metrics["math_comparison"] = {
            paper_id: {
                "total_math": stats["math"]["total_math_elements"],
                "blocks": stats["math"]["math_block_count"],
                "inline": stats["math"]["inline_math_count"]
            }
            for paper_id, stats in all_stats.items()
        }
        
        # Theology comparison
        metrics["theology_comparison"] = {
            paper_id: {
                "trinity_total": stats["theology"]["trinity_total"],
                "trinity_symmetry": stats["theology"]["trinity_symmetry_score"],
                "logos_mentions": stats["theology"]["logos_mentions"]
            }
            for paper_id, stats in all_stats.items()
        }
        
        # Link density comparison
        metrics["link_comparison"] = {
            paper_id: {
                "internal_links": stats["links"]["internal_link_count"],
                "external_links": stats["links"]["external_url_count"]
            }
            for paper_id, stats in all_stats.items()
        }
        
        # Image usage comparison
        metrics["image_comparison"] = {
            paper_id: {
                "image_count": stats["images"]["embedded_image_count"],
                "unique_images": stats["images"]["unique_image_uuids"]
            }
            for paper_id, stats in all_stats.items()
        }
        
        return metrics
    
    def _generate_similarity_matrix(self, all_stats: Dict[str, Dict]) -> Dict[str, Any]:
        """Generate similarity matrix between papers."""
        paper_ids = list(all_stats.keys())
        n = len(paper_ids)
        
        # Create matrix
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        
        for i, paper1 in enumerate(paper_ids):
            for j, paper2 in enumerate(paper_ids):
                if i == j:
                    matrix[i][j] = 1.0
                elif i < j:
                    # Calculate similarity
                    similarity = self._calculate_similarity(
                        all_stats[paper1],
                        all_stats[paper2]
                    )
                    matrix[i][j] = similarity
                    matrix[j][i] = similarity  # Symmetric
        
        return {
            "papers": paper_ids,
            "matrix": matrix
        }
    
    def _calculate_similarity(self, stats1: Dict, stats2: Dict) -> float:
        """Calculate similarity score between two papers."""
        scores = []
        
        # Tag overlap
        tags1 = set(stats1["entities"].get("tags", []))
        tags2 = set(stats2["entities"].get("tags", []))
        if tags1 or tags2:
            jaccard = len(tags1 & tags2) / len(tags1 | tags2) if (tags1 | tags2) else 0
            scores.append(jaccard)
        
        # Word count similarity (normalized)
        wc1 = stats1["text"]["total_word_count"]
        wc2 = stats2["text"]["total_word_count"]
        wc_sim = 1 - abs(wc1 - wc2) / max(wc1, wc2) if max(wc1, wc2) > 0 else 0
        scores.append(wc_sim)
        
        # Math density similarity
        math1 = stats1["math"]["total_math_elements"]
        math2 = stats2["math"]["total_math_elements"]
        math_sim = 1 - abs(math1 - math2) / max(math1, math2, 1)
        scores.append(math_sim)
        
        # Average similarity
        return sum(scores) / len(scores) if scores else 0.0
    
    def _generate_rankings(self, all_stats: Dict[str, Dict]) -> Dict[str, List]:
        """Generate rankings across different metrics."""
        rankings = {}
        
        # Sort by word count
        rankings["by_word_count"] = sorted(
            all_stats.items(),
            key=lambda x: x[1]["text"]["total_word_count"],
            reverse=True
        )
        rankings["by_word_count"] = [
            {"paper_id": p[0], "value": p[1]["text"]["total_word_count"]}
            for p in rankings["by_word_count"]
        ]
        
        # Sort by math density
        rankings["by_math_density"] = sorted(
            all_stats.items(),
            key=lambda x: x[1]["math"]["total_math_elements"],
            reverse=True
        )
        rankings["by_math_density"] = [
            {"paper_id": p[0], "value": p[1]["math"]["total_math_elements"]}
            for p in rankings["by_math_density"]
        ]
        
        # Sort by trinity symmetry
        rankings["by_trinity_symmetry"] = sorted(
            all_stats.items(),
            key=lambda x: x[1]["theology"]["trinity_symmetry_score"],
            reverse=True
        )
        rankings["by_trinity_symmetry"] = [
            {"paper_id": p[0], "value": p[1]["theology"]["trinity_symmetry_score"]}
            for p in rankings["by_trinity_symmetry"]
        ]
        
        # Sort by image count
        rankings["by_image_count"] = sorted(
            all_stats.items(),
            key=lambda x: x[1]["images"]["embedded_image_count"],
            reverse=True
        )
        rankings["by_image_count"] = [
            {"paper_id": p[0], "value": p[1]["images"]["embedded_image_count"]}
            for p in rankings["by_image_count"]
        ]
        
        return rankings
    
    def save(self, paper_ids: List[str], comparison: Dict[str, Any]) -> Path:
        """
        Save comparison statistics to JSON file.
        
        Args:
            paper_ids: List of paper IDs
            comparison: Comparison dictionary
        
        Returns:
            Path to saved comparison file
        """
        comparison_id = "-".join(paper_ids[:3])  # Use first 3 for filename
        if len(paper_ids) > 3:
            comparison_id += f"-plus{len(paper_ids)-3}"
        
        comparison_file = self.comparison_folder / f"{comparison_id}.comparison.json"
        
        with open(comparison_file, 'w', encoding='utf-8') as f:
            json.dump(comparison, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Comparison saved: {comparison_file}")
        return comparison_file
    
    def generate_and_save(self, paper_ids: List[str]) -> Path:
        """Generate and save comparison in one step."""
        comparison = self.generate(paper_ids)
        return self.save(paper_ids, comparison)


# CLI Interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python generate_comparisons.py <paper1> <paper2> [paper3 ...]")
        print("Example: python generate_comparisons.py Paper-01 Paper-02 Paper-03")
        sys.exit(1)
    
    vault_root = Path("D:/THEOPHYSICS_MASTER")
    generator = ComparisonStatsGenerator(vault_root)
    
    paper_ids = sys.argv[1:]
    print(f"Comparing {len(paper_ids)} papers: {', '.join(paper_ids)}")
    
    try:
        generator.generate_and_save(paper_ids)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

