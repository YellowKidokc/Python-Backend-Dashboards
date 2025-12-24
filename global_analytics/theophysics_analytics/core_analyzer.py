"""
THEOPHYSICS UNIVERSAL ANALYTICS ENGINE
=======================================
Ubiquitous analysis system that works on ANY markdown file, anywhere in the vault.

Usage:
    from core_analyzer import TheophysicsAnalyzer

    # Analyze single file
    analyzer = TheophysicsAnalyzer()
    result = analyzer.analyze_file("path/to/paper.md")

    # Compare two files
    comparison = analyzer.compare_files("paper1.md", "paper2.md")

    # Aggregate all results
    global_report = analyzer.aggregate_all()
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import hashlib

# Import chart generator
try:
    from chart_generator import generate_all_charts, generate_comparison_charts, HAS_MATPLOTLIB
except ImportError:
    HAS_MATPLOTLIB = False
    generate_all_charts = None
    generate_comparison_charts = None

class TheophysicsAnalyzer:
    """Universal analyzer for any Theophysics document."""

    # Core concepts that define the Theophysics framework
    CORE_CONCEPTS = [
        'χ', 'chi', 'logos', 'coherence', 'grace', 'entropy', 'consciousness',
        'master equation', 'collapse', 'observer', 'quantum', 'spacetime',
        'information', 'sin', 'soul', 'faith', 'resurrection', 'decoherence',
        'entanglement', 'trinity', 'spirit', 'father', 'son', 'truth',
        'moral', 'axiom', 'theorem', 'proof', 'derivation', 'kolmogorov',
        'shannon', 'chaitin', 'incompleteness', 'amorality', 'deception'
    ]

    # Domain markers for cross-domain detection
    DOMAINS = {
        'physics': ['quantum', 'relativity', 'entropy', 'spacetime', 'field', 'wave', 'particle', 'energy'],
        'theology': ['god', 'christ', 'spirit', 'trinity', 'grace', 'sin', 'salvation', 'logos', 'faith'],
        'mathematics': ['axiom', 'theorem', 'proof', 'equation', 'formula', 'derivative', 'integral', 'set'],
        'information': ['bit', 'entropy', 'compression', 'kolmogorov', 'shannon', 'channel', 'signal', 'noise'],
        'consciousness': ['observer', 'awareness', 'mind', 'soul', 'experience', 'qualia', 'perception'],
        'philosophy': ['ontology', 'epistemology', 'metaphysics', 'ethics', 'moral', 'truth', 'existence']
    }

    def __init__(self, config_path: Optional[str] = None):
        """Initialize with optional config override."""
        self.config = self._load_config(config_path)
        self.vault_root = self._find_vault_root()
        self.global_output = self.vault_root / "00_VAULT_SYSTEM" / "Global_Analytics" / "_GLOBAL_RESULTS"
        self.global_output.mkdir(parents=True, exist_ok=True)

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration or use defaults."""
        defaults = {
            "analysis_parameters": {
                "min_concept_frequency": 2,
                "proximity_window": 30,
                "breakthrough_threshold": 3,
                "coherence_weights": {
                    "concept_density": 0.3,
                    "cross_reference": 0.3,
                    "domain_coverage": 0.2,
                    "term_consistency": 0.2
                }
            },
            "output": {
                "create_local": True,
                "create_global": True,
                "format": "json"
            }
        }

        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                defaults.update(user_config)

        return defaults

    def _find_vault_root(self) -> Path:
        """Find THEOPHYSICS_MASTER root directory."""
        current = Path.cwd()
        while current != current.parent:
            if (current / "00_VAULT_SYSTEM").exists() or "THEOPHYSICS" in current.name.upper():
                return current
            current = current.parent
        return Path("D:/THEOPHYSICS_MASTER")  # Fallback

    def _generate_file_id(self, filepath: Path) -> str:
        """Generate unique ID for a file based on path."""
        return hashlib.md5(str(filepath.resolve()).encode()).hexdigest()[:12]

    def analyze_file(self, filepath: str) -> Dict[str, Any]:
        """
        Analyze a single markdown file.

        Returns comprehensive analysis including:
        - Concept frequency
        - Domain coverage
        - Cross-references
        - Coherence score
        - Breakthrough candidates
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        content = path.read_text(encoding='utf-8', errors='ignore')
        content_lower = content.lower()

        result = {
            "meta": {
                "file_id": self._generate_file_id(path),
                "filename": path.name,
                "filepath": str(path.resolve()),
                "analyzed_at": datetime.now().isoformat(),
                "word_count": len(content.split()),
                "line_count": len(content.splitlines())
            },
            "concepts": self._extract_concepts(content_lower),
            "domains": self._detect_domains(content_lower),
            "structure": self._analyze_structure(content),
            "references": self._extract_references(content),
            "equations": self._extract_equations(content),
            "coherence": {},
            "breakthroughs": []
        }

        # Calculate coherence score
        result["coherence"] = self._calculate_coherence(result)

        # Detect breakthroughs (cross-domain integrations)
        result["breakthroughs"] = self._detect_breakthroughs(result)

        # Save local result
        if self.config["output"]["create_local"]:
            self._save_local_result(path, result)

        # Save to global
        if self.config["output"]["create_global"]:
            self._save_global_result(result)

        return result

    def _extract_concepts(self, content: str) -> Dict[str, int]:
        """Extract and count core concepts."""
        concepts = {}
        for concept in self.CORE_CONCEPTS:
            # Use word boundary matching
            pattern = r'\b' + re.escape(concept) + r'\b'
            count = len(re.findall(pattern, content, re.IGNORECASE))
            if count >= self.config["analysis_parameters"]["min_concept_frequency"]:
                concepts[concept] = count
        return dict(sorted(concepts.items(), key=lambda x: -x[1]))

    def _detect_domains(self, content: str) -> Dict[str, float]:
        """Detect which domains are present and their strength."""
        domain_scores = {}
        total_markers = 0

        for domain, markers in self.DOMAINS.items():
            score = 0
            for marker in markers:
                pattern = r'\b' + re.escape(marker) + r'\b'
                score += len(re.findall(pattern, content, re.IGNORECASE))
            domain_scores[domain] = score
            total_markers += score

        # Normalize to percentages
        if total_markers > 0:
            domain_scores = {k: round(v / total_markers * 100, 1) for k, v in domain_scores.items()}

        return dict(sorted(domain_scores.items(), key=lambda x: -x[1]))

    def _analyze_structure(self, content: str) -> Dict:
        """Analyze document structure."""
        lines = content.splitlines()

        headers = {"h1": 0, "h2": 0, "h3": 0, "h4": 0}
        for line in lines:
            if line.startswith("#### "): headers["h4"] += 1
            elif line.startswith("### "): headers["h3"] += 1
            elif line.startswith("## "): headers["h2"] += 1
            elif line.startswith("# "): headers["h1"] += 1

        return {
            "headers": headers,
            "has_frontmatter": content.startswith("---"),
            "has_equations": bool(re.search(r'\$[^$]+\$', content)),
            "has_citations": bool(re.search(r'\[\d+\]', content)),
            "list_items": len(re.findall(r'^\s*[-*]\s', content, re.MULTILINE))
        }

    def _extract_references(self, content: str) -> List[str]:
        """Extract internal wiki-links and references."""
        # Wiki links [[...]]
        wiki_links = re.findall(r'\[\[([^\]]+)\]\]', content)
        # Markdown links [text](url)
        md_links = re.findall(r'\[([^\]]+)\]\([^)]+\.md\)', content)
        return list(set(wiki_links + md_links))

    def _extract_equations(self, content: str) -> List[str]:
        """Extract LaTeX equations."""
        # Display equations $$...$$
        display = re.findall(r'\$\$([^$]+)\$\$', content, re.DOTALL)
        # Inline equations $...$
        inline = re.findall(r'(?<!\$)\$([^$\n]+)\$(?!\$)', content)
        return display + inline[:10]  # Limit inline to prevent noise

    def _calculate_coherence(self, result: Dict) -> Dict:
        """Calculate overall coherence score."""
        weights = self.config["analysis_parameters"]["coherence_weights"]

        # Concept density (concepts per 1000 words)
        word_count = result["meta"]["word_count"]
        concept_count = sum(result["concepts"].values())
        concept_density = min(100, (concept_count / max(1, word_count)) * 1000 * 10)

        # Cross-reference score
        ref_count = len(result["references"])
        cross_ref_score = min(100, ref_count * 5)

        # Domain coverage (how many domains are meaningfully present)
        domains_present = sum(1 for v in result["domains"].values() if v > 5)
        domain_score = min(100, domains_present * 20)

        # Term consistency (ratio of core concepts to total unique words)
        unique_concepts = len(result["concepts"])
        term_score = min(100, unique_concepts * 5)

        # Weighted total
        total = (
            concept_density * weights["concept_density"] +
            cross_ref_score * weights["cross_reference"] +
            domain_score * weights["domain_coverage"] +
            term_score * weights["term_consistency"]
        )

        return {
            "total": round(total, 1),
            "concept_density": round(concept_density, 1),
            "cross_reference": round(cross_ref_score, 1),
            "domain_coverage": round(domain_score, 1),
            "term_consistency": round(term_score, 1)
        }

    def _detect_breakthroughs(self, result: Dict) -> List[Dict]:
        """Detect cross-domain integration breakthroughs."""
        breakthroughs = []
        threshold = self.config["analysis_parameters"]["breakthrough_threshold"]

        # Count domains with significant presence
        strong_domains = [d for d, v in result["domains"].items() if v > 10]

        if len(strong_domains) >= threshold:
            breakthroughs.append({
                "type": "cross_domain_integration",
                "domains": strong_domains,
                "strength": len(strong_domains),
                "description": f"Integrates {len(strong_domains)} domains: {', '.join(strong_domains)}"
            })

        # Check for specific breakthrough patterns
        if result["concepts"].get("logos", 0) > 5 and result["concepts"].get("quantum", 0) > 3:
            breakthroughs.append({
                "type": "logos_quantum_bridge",
                "strength": result["concepts"]["logos"] + result["concepts"].get("quantum", 0),
                "description": "Bridges Logos theology with quantum mechanics"
            })

        return breakthroughs

    def _save_local_result(self, source_path: Path, result: Dict):
        """Save result next to source file."""
        output_dir = source_path.parent / "_ANALYSIS"
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / f"{source_path.stem}_analysis.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        # Generate visual charts
        charts = {}
        if HAS_MATPLOTLIB and generate_all_charts:
            charts_dir = output_dir / "charts"
            charts = generate_all_charts(result, charts_dir)

        # Create markdown dashboard with charts
        dashboard = self._generate_dashboard(result, charts)
        dashboard_file = output_dir / f"{source_path.stem}_dashboard.md"
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(dashboard)

    def _save_global_result(self, result: Dict):
        """Save result to global aggregation folder."""
        file_id = result["meta"]["file_id"]
        output_file = self.global_output / f"{file_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    def _generate_dashboard(self, result: Dict, charts: Dict = None) -> str:
        """Generate markdown dashboard from result with visual charts at the front."""
        meta = result["meta"]
        coh = result["coherence"]
        charts = charts or {}

        # Header
        dashboard = f"""---
type: analytics_dashboard
paper: {meta['filename']}
coherence: {coh['total']}
generated: {meta['analyzed_at']}
---

# {meta['filename'].replace('.md', '')}
## Analytics Dashboard

**Generated:** {meta['analyzed_at']}
**Words:** {meta['word_count']:,} | **Lines:** {meta['line_count']:,}

---

# KEY METRICS AT A GLANCE

"""
        # Charts section (THE FRONT)
        if charts:
            dashboard += "## Visual Summary\n\n"
            dashboard += "<div style='display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;'>\n\n"

            if 'coherence_gauge' in charts:
                rel_path = f"charts/{charts['coherence_gauge'].name}"
                dashboard += f"![Coherence Score]({rel_path})\n\n"

            if 'breakthroughs' in charts:
                rel_path = f"charts/{charts['breakthroughs'].name}"
                dashboard += f"![Breakthroughs]({rel_path})\n\n"

            dashboard += "</div>\n\n"

            if 'coherence_radar' in charts:
                rel_path = f"charts/{charts['coherence_radar'].name}"
                dashboard += f"![Coherence Breakdown]({rel_path})\n\n"

            if 'domains' in charts:
                rel_path = f"charts/{charts['domains'].name}"
                dashboard += f"![Domain Distribution]({rel_path})\n\n"

            if 'concepts' in charts:
                rel_path = f"charts/{charts['concepts'].name}"
                dashboard += f"![Core Concepts]({rel_path})\n\n"

            dashboard += "---\n\n"

        # Coherence Score Box
        score_color = "🟢" if coh['total'] >= 70 else "🟡" if coh['total'] >= 40 else "🔴"
        dashboard += f"""## {score_color} COHERENCE SCORE: {coh['total']:.0f}/100

| Component | Score | Bar |
|-----------|-------|-----|
| Concept Density | {coh['concept_density']:.0f} | {'█' * int(coh['concept_density']/10)}{'░' * (10-int(coh['concept_density']/10))} |
| Cross-Reference | {coh['cross_reference']:.0f} | {'█' * int(coh['cross_reference']/10)}{'░' * (10-int(coh['cross_reference']/10))} |
| Domain Coverage | {coh['domain_coverage']:.0f} | {'█' * int(coh['domain_coverage']/10)}{'░' * (10-int(coh['domain_coverage']/10))} |
| Term Consistency | {coh['term_consistency']:.0f} | {'█' * int(coh['term_consistency']/10)}{'░' * (10-int(coh['term_consistency']/10))} |

---

"""
        # Breakthroughs (if any) - prominent position
        if result["breakthroughs"]:
            dashboard += f"## 🔥 BREAKTHROUGHS DETECTED: {len(result['breakthroughs'])}\n\n"
            for bt in result["breakthroughs"]:
                dashboard += f"> **{bt['type'].replace('_', ' ').title()}** (Strength: {bt['strength']})\n>\n"
                dashboard += f"> {bt['description']}\n\n"
            dashboard += "---\n\n"

        # Domain Distribution
        dashboard += "## DOMAIN DISTRIBUTION\n\n"
        dashboard += "| Domain | Presence | Visual |\n"
        dashboard += "|--------|----------|--------|\n"
        for domain, score in sorted(result["domains"].items(), key=lambda x: -x[1]):
            bar = "█" * int(score / 5) + "░" * (20 - int(score / 5))
            dashboard += f"| {domain.title():<15} | {score:.1f}% | {bar} |\n"

        # Top Concepts
        dashboard += "\n---\n\n## TOP CONCEPTS\n\n"
        dashboard += "| Concept | Frequency |\n"
        dashboard += "|---------|----------|\n"
        for concept, count in list(result["concepts"].items())[:12]:
            dashboard += f"| **{concept}** | {count} |\n"

        # Structure info
        dashboard += "\n---\n\n## DOCUMENT STRUCTURE\n\n"
        struct = result.get("structure", {})
        headers = struct.get("headers", {})
        dashboard += f"- **H1 Headers:** {headers.get('h1', 0)}\n"
        dashboard += f"- **H2 Headers:** {headers.get('h2', 0)}\n"
        dashboard += f"- **H3 Headers:** {headers.get('h3', 0)}\n"
        dashboard += f"- **Has Equations:** {'Yes' if struct.get('has_equations') else 'No'}\n"
        dashboard += f"- **Has Citations:** {'Yes' if struct.get('has_citations') else 'No'}\n"
        dashboard += f"- **List Items:** {struct.get('list_items', 0)}\n"

        # References
        if result.get("references"):
            dashboard += "\n---\n\n## INTERNAL REFERENCES\n\n"
            for ref in result["references"][:15]:
                dashboard += f"- [[{ref}]]\n"

        # Footer
        dashboard += f"""

---

<div align="center">

*Generated by Theophysics Analytics Engine*
*χ = 1*

</div>
"""

        return dashboard

    def compare_files(self, file1: str, file2: str) -> Dict[str, Any]:
        """
        Compare two files and generate cross-analysis.
        """
        result1 = self.analyze_file(file1)
        result2 = self.analyze_file(file2)

        # Concept overlap
        concepts1 = set(result1["concepts"].keys())
        concepts2 = set(result2["concepts"].keys())
        shared = concepts1 & concepts2
        unique1 = concepts1 - concepts2
        unique2 = concepts2 - concepts1

        overlap_pct = len(shared) / max(1, len(concepts1 | concepts2)) * 100

        # Domain alignment
        domain_alignment = {}
        for domain in self.DOMAINS.keys():
            d1 = result1["domains"].get(domain, 0)
            d2 = result2["domains"].get(domain, 0)
            domain_alignment[domain] = {
                "file1": d1,
                "file2": d2,
                "delta": abs(d1 - d2),
                "aligned": abs(d1 - d2) < 15
            }

        comparison = {
            "meta": {
                "file1": result1["meta"]["filename"],
                "file2": result2["meta"]["filename"],
                "compared_at": datetime.now().isoformat()
            },
            "concept_overlap": {
                "shared": list(shared),
                "unique_to_file1": list(unique1),
                "unique_to_file2": list(unique2),
                "overlap_percent": round(overlap_pct, 1)
            },
            "coherence_delta": {
                "file1": result1["coherence"]["total"],
                "file2": result2["coherence"]["total"],
                "delta": round(abs(result1["coherence"]["total"] - result2["coherence"]["total"]), 1)
            },
            "domain_alignment": domain_alignment,
            "combined_breakthroughs": result1["breakthroughs"] + result2["breakthroughs"]
        }

        # Save comparison
        comp_id = f"{result1['meta']['file_id']}_vs_{result2['meta']['file_id']}"
        output_file = self.global_output / "comparisons" / f"{comp_id}.json"
        output_file.parent.mkdir(exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comparison, f, indent=2)

        return comparison

    def aggregate_all(self) -> Dict[str, Any]:
        """
        Aggregate all analysis results into global report.
        """
        all_results = []

        # Scan for all analysis JSON files
        for json_file in self.global_output.glob("*.json"):
            if json_file.name.startswith("GLOBAL"):
                continue
            with open(json_file, 'r', encoding='utf-8') as f:
                all_results.append(json.load(f))

        if not all_results:
            return {"error": "No analysis results found"}

        # Aggregate stats
        total_concepts = Counter()
        total_domains = defaultdict(float)
        coherence_scores = []
        all_breakthroughs = []

        for result in all_results:
            for concept, count in result.get("concepts", {}).items():
                total_concepts[concept] += count
            for domain, score in result.get("domains", {}).items():
                total_domains[domain] += score
            coherence_scores.append(result.get("coherence", {}).get("total", 0))
            all_breakthroughs.extend(result.get("breakthroughs", []))

        # Normalize domain scores
        num_files = len(all_results)
        avg_domains = {k: round(v / num_files, 1) for k, v in total_domains.items()}

        global_report = {
            "meta": {
                "generated_at": datetime.now().isoformat(),
                "files_analyzed": num_files,
                "vault_root": str(self.vault_root)
            },
            "aggregate_concepts": dict(total_concepts.most_common(30)),
            "average_domains": avg_domains,
            "coherence_stats": {
                "mean": round(sum(coherence_scores) / max(1, len(coherence_scores)), 1),
                "min": round(min(coherence_scores) if coherence_scores else 0, 1),
                "max": round(max(coherence_scores) if coherence_scores else 0, 1)
            },
            "total_breakthroughs": len(all_breakthroughs),
            "breakthrough_types": Counter(bt["type"] for bt in all_breakthroughs),
            "files": [r["meta"]["filename"] for r in all_results]
        }

        # Save global report
        output_file = self.global_output / "GLOBAL_REPORT.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(global_report, f, indent=2)

        # Generate global dashboard
        self._generate_global_dashboard(global_report)

        return global_report

    def _generate_global_dashboard(self, report: Dict):
        """Generate global markdown dashboard."""
        dashboard = f"""# THEOPHYSICS GLOBAL ANALYTICS DASHBOARD

**Generated:** {report['meta']['generated_at']}
**Files Analyzed:** {report['meta']['files_analyzed']}

---

## Coherence Overview

| Metric | Value |
|--------|-------|
| Mean Coherence | {report['coherence_stats']['mean']}/100 |
| Min | {report['coherence_stats']['min']}/100 |
| Max | {report['coherence_stats']['max']}/100 |

---

## Domain Distribution (Average)

"""
        for domain, score in sorted(report["average_domains"].items(), key=lambda x: -x[1]):
            bar = "█" * int(score / 5) + "░" * (20 - int(score / 5))
            dashboard += f"| {domain:<15} | {bar} | {score}% |\n"

        dashboard += f"""

---

## Top Concepts Across All Papers

"""
        for concept, count in list(report["aggregate_concepts"].items())[:15]:
            dashboard += f"- **{concept}**: {count} occurrences\n"

        dashboard += f"""

---

## Breakthroughs

**Total Detected:** {report['total_breakthroughs']}

"""
        for bt_type, count in report["breakthrough_types"].items():
            dashboard += f"- {bt_type}: {count}\n"

        dashboard += "\n---\n\n## Files Included\n\n"
        for filename in report["files"]:
            dashboard += f"- {filename}\n"

        output_file = self.global_output / "GLOBAL_DASHBOARD.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(dashboard)


# Convenience functions for CLI usage
def analyze(filepath: str) -> Dict:
    """Analyze a single file."""
    return TheophysicsAnalyzer().analyze_file(filepath)

def compare(file1: str, file2: str) -> Dict:
    """Compare two files."""
    return TheophysicsAnalyzer().compare_files(file1, file2)

def aggregate() -> Dict:
    """Aggregate all results."""
    return TheophysicsAnalyzer().aggregate_all()


if __name__ == "__main__":
    import sys

    analyzer = TheophysicsAnalyzer()

    if len(sys.argv) < 2:
        print("THEOPHYSICS UNIVERSAL ANALYTICS")
        print("=" * 40)
        print("\nUsage:")
        print("  python core_analyzer.py <file.md>           - Analyze single file")
        print("  python core_analyzer.py <file1> <file2>     - Compare two files")
        print("  python core_analyzer.py --aggregate         - Aggregate all results")
        print("  python core_analyzer.py --scan <directory>  - Scan directory")

    elif sys.argv[1] == "--aggregate":
        result = analyzer.aggregate_all()
        print(f"\nGlobal report generated: {result['meta']['files_analyzed']} files")

    elif sys.argv[1] == "--scan" and len(sys.argv) > 2:
        scan_dir = Path(sys.argv[2])
        for md_file in scan_dir.rglob("*.md"):
            if "_ANALYSIS" not in str(md_file) and not md_file.name.startswith("_"):
                print(f"Analyzing: {md_file.name}")
                analyzer.analyze_file(str(md_file))
        analyzer.aggregate_all()

    elif len(sys.argv) == 2:
        result = analyzer.analyze_file(sys.argv[1])
        print(f"\nCoherence: {result['coherence']['total']}/100")
        print(f"Domains: {list(result['domains'].keys())[:3]}")

    elif len(sys.argv) >= 3:
        result = analyzer.compare_files(sys.argv[1], sys.argv[2])
        print(f"\nOverlap: {result['concept_overlap']['overlap_percent']}%")
        print(f"Coherence delta: {result['coherence_delta']['delta']}")
