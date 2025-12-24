#!/usr/bin/env python3
"""
THEOPHYSICS ANALYTICS RUNNER
============================
Simple CLI for running analytics anywhere in the vault.

Examples:
    # Analyze a single paper
    python run_analytics.py "D:/THEOPHYSICS_MASTER/03_PUBLICATIONS/.../Paper.md"

    # Compare two papers
    python run_analytics.py compare Paper1.md Paper2.md

    # Scan entire folder and aggregate
    python run_analytics.py scan "D:/THEOPHYSICS_MASTER/03_PUBLICATIONS/COMPLETE_LOGOS_PAPERS_FINAL"

    # Just aggregate existing results
    python run_analytics.py aggregate

    # Analyze the Principia Moralia folder
    python run_analytics.py scan "D:/THEOPHYSICS_MASTER/03_PUBLICATIONS/COMPLETE_LOGOS_PAPERS_FINAL/P00 Logos Paper Intro"
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core_analyzer import TheophysicsAnalyzer

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║          THEOPHYSICS UNIVERSAL ANALYTICS ENGINE              ║
║                        χ = 1                                 ║
╚══════════════════════════════════════════════════════════════╝
""")

def print_result_summary(result: dict, mode: str = "single"):
    """Pretty print analysis results."""
    if mode == "single":
        meta = result["meta"]
        coh = result["coherence"]
        print(f"\n📄 {meta['filename']}")
        print(f"   Words: {meta['word_count']:,} | Lines: {meta['line_count']:,}")
        print(f"\n   COHERENCE: {coh['total']}/100")
        print(f"   ├─ Concept Density:  {coh['concept_density']}")
        print(f"   ├─ Cross-Reference:  {coh['cross_reference']}")
        print(f"   ├─ Domain Coverage:  {coh['domain_coverage']}")
        print(f"   └─ Term Consistency: {coh['term_consistency']}")

        if result["breakthroughs"]:
            print(f"\n   🔥 BREAKTHROUGHS: {len(result['breakthroughs'])}")
            for bt in result["breakthroughs"]:
                print(f"      └─ {bt['description']}")

        print(f"\n   Top Domains: {', '.join(list(result['domains'].keys())[:3])}")
        print(f"   Top Concepts: {', '.join(list(result['concepts'].keys())[:5])}")

    elif mode == "compare":
        print(f"\n📊 COMPARISON: {result['meta']['file1']} vs {result['meta']['file2']}")
        print(f"\n   Concept Overlap: {result['concept_overlap']['overlap_percent']}%")
        print(f"   Shared concepts: {len(result['concept_overlap']['shared'])}")
        print(f"   Coherence Delta: {result['coherence_delta']['delta']}")

        aligned = sum(1 for d in result['domain_alignment'].values() if d['aligned'])
        print(f"   Domain Alignment: {aligned}/{len(result['domain_alignment'])} domains aligned")

    elif mode == "aggregate":
        print(f"\n📈 GLOBAL AGGREGATION")
        print(f"   Files analyzed: {result['meta']['files_analyzed']}")
        print(f"\n   COHERENCE (across vault):")
        print(f"   ├─ Mean:  {result['coherence_stats']['mean']}")
        print(f"   ├─ Min:   {result['coherence_stats']['min']}")
        print(f"   └─ Max:   {result['coherence_stats']['max']}")
        print(f"\n   Total Breakthroughs: {result['total_breakthroughs']}")


def main():
    print_banner()
    analyzer = TheophysicsAnalyzer()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python run_analytics.py <file.md>              - Analyze single file")
        print("  python run_analytics.py compare <f1> <f2>      - Compare two files")
        print("  python run_analytics.py scan <directory>       - Scan all .md files")
        print("  python run_analytics.py aggregate              - Aggregate all results")
        print("\nOutput locations:")
        print(f"  LOCAL:  <paper_folder>/_ANALYSIS/")
        print(f"  GLOBAL: {analyzer.global_output}")
        return

    command = sys.argv[1].lower()

    if command == "aggregate":
        print("Aggregating all results...")
        result = analyzer.aggregate_all()
        print_result_summary(result, "aggregate")
        print(f"\n✅ Global dashboard saved to: {analyzer.global_output / 'GLOBAL_DASHBOARD.md'}")

    elif command == "compare" and len(sys.argv) >= 4:
        file1, file2 = sys.argv[2], sys.argv[3]
        print(f"Comparing: {Path(file1).name} vs {Path(file2).name}")
        result = analyzer.compare_files(file1, file2)
        print_result_summary(result, "compare")

    elif command == "scan" and len(sys.argv) >= 3:
        scan_dir = Path(sys.argv[2])
        if not scan_dir.exists():
            print(f"❌ Directory not found: {scan_dir}")
            return

        md_files = [f for f in scan_dir.rglob("*.md")
                    if "_ANALYSIS" not in str(f)
                    and "_GLOBAL" not in str(f)
                    and not f.name.startswith("_")]

        print(f"Found {len(md_files)} markdown files to analyze...\n")

        for i, md_file in enumerate(md_files, 1):
            print(f"[{i}/{len(md_files)}] {md_file.name}...", end=" ")
            try:
                result = analyzer.analyze_file(str(md_file))
                print(f"✓ Coherence: {result['coherence']['total']}")
            except Exception as e:
                print(f"✗ Error: {e}")

        print("\nAggregating results...")
        result = analyzer.aggregate_all()
        print_result_summary(result, "aggregate")
        print(f"\n✅ Complete! Dashboard: {analyzer.global_output / 'GLOBAL_DASHBOARD.md'}")

    else:
        # Single file analysis
        filepath = sys.argv[1]
        if not Path(filepath).exists():
            print(f"❌ File not found: {filepath}")
            return

        print(f"Analyzing: {Path(filepath).name}")
        result = analyzer.analyze_file(filepath)
        print_result_summary(result, "single")
        print(f"\n✅ Local dashboard: {Path(filepath).parent / '_ANALYSIS'}")


if __name__ == "__main__":
    main()
