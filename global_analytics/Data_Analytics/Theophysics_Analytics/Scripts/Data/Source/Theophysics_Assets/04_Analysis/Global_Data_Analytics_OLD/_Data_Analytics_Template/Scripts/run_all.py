#!/usr/bin/env python3
"""
run_all.py - Master script to run entire analytics pipeline.

Usage:
    python run_all.py [--path PATH]

This will:
1. Extract all data from markdown files
2. Generate statistics
3. Build Mermaid diagrams
4. Update all dashboards
"""

import subprocess
import sys
from pathlib import Path


def run_script(script_name, args=None):
    """Run a Python script and capture output."""
    script_path = Path(__file__).parent / script_name
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)

    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print('='*60)

    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Run full analytics pipeline')
    parser.add_argument('--path', type=str, help='Path to analyze')
    args = parser.parse_args()

    extra_args = ['--path', args.path] if args.path else []

    print("=" * 60)
    print("  THEOPHYSICS LOCAL ANALYTICS PIPELINE")
    print("=" * 60)

    # Step 1: Extract all
    success = run_script('extract_all.py', extra_args)
    if not success:
        print("[ERROR] extract_all.py failed")
        return

    # Step 2: Count stats
    success = run_script('count_stats.py')
    if not success:
        print("[ERROR] count_stats.py failed")
        return

    # Step 3: Build mermaid
    success = run_script('build_mermaid.py')
    if not success:
        print("[ERROR] build_mermaid.py failed")
        return

    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE")
    print("=" * 60)
    print("\nCheck:")
    print("  - Dashboards/Statistics.md")
    print("  - Dashboards/Mermaid_Maps.md")
    print("  - Master_Sheet/*.json")


if __name__ == '__main__':
    main()
