"""
Global Stats Generator - Vault-wide analytics
Part of the Unified Research Analytics System
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from collections import Counter


class GlobalStatsGenerator:
    """Generate vault-wide statistics and analytics."""
    
    def __init__(self, vault_root: Path):
        """
        Initialize global stats generator.
        
        Args:
            vault_root: Root of the Obsidian vault
        """
        self.vault_root = Path(vault_root)
        self.local_stats_folder = self.vault_root / "Stats" / "Local"
        self.global_folder = self.vault_root / "Stats" / "Global"
        self.global_folder.mkdir(parents=True, exist_ok=True)
    
    def load_all_paper_stats(self) -> Dict[str, Dict[str, Any]]:
        """Load all available paper statistics."""
        all_stats = {}
        
        for stats_file in self.local_stats_folder.glob("*.stats.json"):
            paper_id = stats_file.stem.replace('.stats', '')
            with open(stats_file, 'r', encoding='utf-8') as f:
                all_stats[paper_id] = json.load(f)
        
        return all_stats
    
    def generate(self) -> Dict[str, Any]:
        """
        Generate global vault statistics.
        
        Returns:
            Global statistics dictionary
        """
        # Load all paper stats
        all_stats = self.load_all_paper_stats()
        
        if not all_stats:
            raise ValueError("No paper statistics found. Run generate_stats.py first.")
        
        # Generate global stats
        global_stats = {
            "metadata": self._generate_metadata(all_stats),
            "per_paper": all_stats,
            "aggregates": self._generate_aggregates(all_stats),
            "distributions": self._generate_distributions(all_stats),
            "tag_analysis": self._generate_tag_analysis(all_stats),
            "math_analysis": self._generate_math_analysis(all_stats),
            "theology_analysis": self._generate_theology_analysis(all_stats),
            "network_analysis": self._generate_network_analysis(all_stats)
        }
        
        return global_stats
    
    def _generate_metadata(self, all_stats: Dict) -> Dict[str, Any]:
        """Generate global metadata."""
        return {
            "total_papers": len(all_stats),
            "generated_at": datetime.now().isoformat(),
            "papers": list(all_stats.keys())
        }
    
    def _generate_aggregates(self, all_stats: Dict) -> Dict[str, Any]:
        """Generate aggregate statistics across all papers."""
        total_words = sum(s["text"]["total_word_count"] for s in all_stats.values())
        total_unique_words = sum(s["text"]["unique_word_count"] for s in all_stats.values())
        total_images = sum(s["images"]["embedded_image_count"] for s in all_stats.values())
        total_math = sum(s["math"]["total_math_elements"] for s in all_stats.values())
        total_links = sum(s["links"]["internal_link_count"] for s in all_stats.values())
        
        # Average reading time
        avg_reading_time = sum(s["text"]["reading_time_minutes"] for s in all_stats.values()) / len(all_stats)
        
        # Total trinity mentions
        total_trinity = sum(s["theology"]["trinity_total"] for s in all_stats.values())
        
        return {
            "total_word_count": total_words,
            "total_unique_words": total_unique_words,
            "total_images": total_images,
            "total_math_elements": total_math,
            "total_internal_links": total_links,
            "average_reading_time_minutes": round(avg_reading_time, 2),
            "total_trinity_mentions": total_trinity,
            "average_words_per_paper": round(total_words / len(all_stats), 2)
        }
    
    def _generate_distributions(self, all_stats: Dict) -> Dict[str, Any]:
        """Generate distribution statistics."""
        word_counts = [s["text"]["total_word_count"] for s in all_stats.values()]
        math_counts = [s["math"]["total_math_elements"] for s in all_stats.values()]
        image_counts = [s["images"]["embedded_image_count"] for s in all_stats.values()]
        
        return {
            "word_count_distribution": {
                "min": min(word_counts),
                "max": max(word_counts),
                "mean": sum(word_counts) / len(word_counts),
                "values": dict(zip(all_stats.keys(), word_counts))
            },
            "math_distribution": {
                "min": min(math_counts),
                "max": max(math_counts),
                "mean": sum(math_counts) / len(math_counts),
                "values": dict(zip(all_stats.keys(), math_counts))
            },
            "image_distribution": {
                "min": min(image_counts),
                "max": max(image_counts),
                "mean": sum(image_counts) / len(image_counts),
                "values": dict(zip(all_stats.keys(), image_counts))
            }
        }
    
    def _generate_tag_analysis(self, all_stats: Dict) -> Dict[str, Any]:
        """Analyze tag usage across vault."""
        # Collect all tags
        all_tags = []
        tag_by_paper = {}
        
        for paper_id, stats in all_stats.items():
            tags = stats["entities"].get("tags", [])
            all_tags.extend(tags)
            tag_by_paper[paper_id] = tags
        
        # Count tag frequency
        tag_frequency = Counter(all_tags)
        
        # Most common tags
        most_common = tag_frequency.most_common(20)
        
        return {
            "unique_tags": len(set(all_tags)),
            "total_tag_instances": len(all_tags),
            "most_common_tags": [{"tag": tag, "count": count} for tag, count in most_common],
            "tags_per_paper": {
                paper_id: len(tags)
                for paper_id, tags in tag_by_paper.items()
            }
        }
    
    def _generate_math_analysis(self, all_stats: Dict) -> Dict[str, Any]:
        """Analyze math usage across vault."""
        math_papers = {
            paper_id: stats["math"]
            for paper_id, stats in all_stats.items()
            if stats["math"]["total_math_elements"] > 0
        }
        
        total_math = sum(s["total_math_elements"] for s in math_papers.values())
        
        # Papers ranked by math density
        math_ranking = sorted(
            math_papers.items(),
            key=lambda x: x[1]["total_math_elements"],
            reverse=True
        )
        
        return {
            "papers_with_math": len(math_papers),
            "total_math_elements": total_math,
            "average_math_per_paper": round(total_math / len(all_stats), 2),
            "most_mathematical_papers": [
                {"paper_id": p[0], "math_count": p[1]["total_math_elements"]}
                for p in math_ranking[:10]
            ]
        }
    
    def _generate_theology_analysis(self, all_stats: Dict) -> Dict[str, Any]:
        """Analyze theology content across vault."""
        total_father = sum(s["theology"]["trinity_father_count"] for s in all_stats.values())
        total_son = sum(s["theology"]["trinity_son_count"] for s in all_stats.values())
        total_spirit = sum(s["theology"]["trinity_spirit_count"] for s in all_stats.values())
        total_logos = sum(s["theology"]["logos_mentions"] for s in all_stats.values())
        
        # Trinity symmetry by paper
        symmetry_scores = {
            paper_id: stats["theology"]["trinity_symmetry_score"]
            for paper_id, stats in all_stats.items()
        }
        
        return {
            "total_trinity_mentions": {
                "father": total_father,
                "son": total_son,
                "spirit": total_spirit,
                "total": total_father + total_son + total_spirit
            },
            "total_logos_mentions": total_logos,
            "trinity_symmetry_by_paper": symmetry_scores,
            "most_balanced_trinity_papers": sorted(
                symmetry_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }
    
    def _generate_network_analysis(self, all_stats: Dict) -> Dict[str, Any]:
        """Analyze link network across vault."""
        # Collect all internal links
        total_internal_links = sum(s["links"]["internal_link_count"] for s in all_stats.values())
        total_external_links = sum(s["links"]["external_url_count"] for s in all_stats.values())
        
        # Papers by link density
        link_density = {
            paper_id: stats["links"]["internal_link_count"]
            for paper_id, stats in all_stats.items()
        }
        
        return {
            "total_internal_links": total_internal_links,
            "total_external_links": total_external_links,
            "average_links_per_paper": round(total_internal_links / len(all_stats), 2),
            "most_connected_papers": sorted(
                link_density.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }
    
    def save(self, global_stats: Dict[str, Any]) -> Path:
        """
        Save global statistics to JSON file.
        
        Args:
            global_stats: Global statistics dictionary
        
        Returns:
            Path to saved global stats file
        """
        global_file = self.global_folder / "vault.stats.json"
        
        with open(global_file, 'w', encoding='utf-8') as f:
            json.dump(global_stats, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Global stats saved: {global_file}")
        
        # Also save individual analysis files
        self._save_tag_analysis(global_stats["tag_analysis"])
        self._save_math_analysis(global_stats["math_analysis"])
        self._save_theology_analysis(global_stats["theology_analysis"])
        
        return global_file
    
    def _save_tag_analysis(self, tag_analysis: Dict) -> None:
        """Save tag analysis to separate file."""
        tag_file = self.global_folder / "tag.stats.json"
        with open(tag_file, 'w', encoding='utf-8') as f:
            json.dump(tag_analysis, f, indent=2, ensure_ascii=False)
        print(f"✅ Tag analysis saved: {tag_file}")
    
    def _save_math_analysis(self, math_analysis: Dict) -> None:
        """Save math analysis to separate file."""
        math_file = self.global_folder / "math.stats.json"
        with open(math_file, 'w', encoding='utf-8') as f:
            json.dump(math_analysis, f, indent=2, ensure_ascii=False)
        print(f"✅ Math analysis saved: {math_file}")
    
    def _save_theology_analysis(self, theology_analysis: Dict) -> None:
        """Save theology analysis to separate file."""
        theology_file = self.global_folder / "theology.stats.json"
        with open(theology_file, 'w', encoding='utf-8') as f:
            json.dump(theology_analysis, f, indent=2, ensure_ascii=False)
        print(f"✅ Theology analysis saved: {theology_file}")
    
    def generate_and_save(self) -> Path:
        """Generate and save global stats in one step."""
        global_stats = self.generate()
        return self.save(global_stats)


# CLI Interface
if __name__ == "__main__":
    vault_root = Path("D:/THEOPHYSICS_MASTER")
    generator = GlobalStatsGenerator(vault_root)
    
    print("Generating global vault statistics...")
    try:
        generator.generate_and_save()
        print("\n✅ Global statistics generated successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import sys
        sys.exit(1)

