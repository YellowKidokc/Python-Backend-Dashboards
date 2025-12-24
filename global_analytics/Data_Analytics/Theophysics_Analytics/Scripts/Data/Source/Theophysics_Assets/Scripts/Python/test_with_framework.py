#!/usr/bin/env python3
"""
Test External Papers + Your Theophysics Framework
Compares coherence with and without your framework
"""

import os
import sys
import json
from pathlib import Path

# Import from coherence_analyzer
sys.path.insert(0, str(Path(__file__).parent))
from coherence_analyzer import (
    calculate_law_coverage,
    calculate_trinity_balance,
    calculate_grace_entropy_ratio,
    calculate_overall_coherence
)

def collect_external_papers(base_dir):
    """Collect all external papers from References/Markdown"""
    combined_text = ""
    papers = []
    
    paper_folders = sorted([d for d in base_dir.glob("P*-*") if d.is_dir()])
    
    for paper_folder in paper_folders:
        markdown_dir = paper_folder / "References" / "Markdown"
        
        if markdown_dir.exists():
            md_files = list(markdown_dir.glob("*.md"))
            
            for md_file in md_files:
                with open(md_file, 'r', encoding='utf-8') as f:
                    text = f.read()
                    combined_text += text + "\n\n"
                    papers.append({
                        'type': 'external',
                        'folder': paper_folder.name,
                        'file': md_file.name
                    })
    
    return combined_text, papers

def collect_framework_papers(base_dir):
    """Collect YOUR Theophysics framework papers"""
    combined_text = ""
    papers = []
    
    paper_folders = sorted([d for d in base_dir.glob("P*-*") if d.is_dir()])
    
    for paper_folder in paper_folders:
        # Look for your main papers (LGS-*.md files)
        md_files = list(paper_folder.glob("LGS-*.md"))
        md_files += list(paper_folder.glob("P*.md"))
        
        for md_file in md_files:
            print(f"Loading framework: {paper_folder.name}/{md_file.name}")
            with open(md_file, 'r', encoding='utf-8') as f:
                text = f.read()
                combined_text += text + "\n\n"
                papers.append({
                    'type': 'framework',
                    'folder': paper_folder.name,
                    'file': md_file.name
                })
    
    return combined_text, papers

def analyze_and_compare(external_text, framework_text, combined_text, 
                        external_papers, framework_papers):
    """Analyze all three scenarios"""
    
    print("\n" + "="*70)
    print("SCENARIO 1: External Papers Only (Baseline)")
    print("="*70)
    
    ext_law = calculate_law_coverage(external_text)
    ext_trinity, ext_trin_bal = calculate_trinity_balance(external_text)
    ext_ge = calculate_grace_entropy_ratio(external_text)
    ext_overall = calculate_overall_coherence(ext_law, ext_trin_bal, ext_ge)
    
    print(f"Papers: {len(external_papers)}")
    print(f"Words: {len(external_text.split()):,}")
    print(f"Overall Score: {ext_overall['overall_score']:.3f} ({ext_overall['grade']})")
    print(f"  Law Coverage:    {ext_overall['law_coverage']:.3f}")
    print(f"  Trinity Balance: {ext_overall['trinity_balance']:.3f}")
    print(f"  Grace/Entropy:   {ext_overall['grace_entropy_balance']:.3f}")
    
    print("\n" + "="*70)
    print("SCENARIO 2: Your Framework Only")
    print("="*70)
    
    fw_law = calculate_law_coverage(framework_text)
    fw_trinity, fw_trin_bal = calculate_trinity_balance(framework_text)
    fw_ge = calculate_grace_entropy_ratio(framework_text)
    fw_overall = calculate_overall_coherence(fw_law, fw_trin_bal, fw_ge)
    
    print(f"Papers: {len(framework_papers)}")
    print(f"Words: {len(framework_text.split()):,}")
    print(f"Overall Score: {fw_overall['overall_score']:.3f} ({fw_overall['grade']})")
    print(f"  Law Coverage:    {fw_overall['law_coverage']:.3f}")
    print(f"  Trinity Balance: {fw_overall['trinity_balance']:.3f}")
    print(f"  Grace/Entropy:   {fw_overall['grace_entropy_balance']:.3f}")
    
    print("\n" + "="*70)
    print("SCENARIO 3: External Papers + Your Framework (Combined)")
    print("="*70)
    
    comb_law = calculate_law_coverage(combined_text)
    comb_trinity, comb_trin_bal = calculate_trinity_balance(combined_text)
    comb_ge = calculate_grace_entropy_ratio(combined_text)
    comb_overall = calculate_overall_coherence(comb_law, comb_trin_bal, comb_ge)
    
    print(f"Papers: {len(external_papers) + len(framework_papers)}")
    print(f"Words: {len(combined_text.split()):,}")
    print(f"Overall Score: {comb_overall['overall_score']:.3f} ({comb_overall['grade']})")
    print(f"  Law Coverage:    {comb_overall['law_coverage']:.3f}")
    print(f"  Trinity Balance: {comb_overall['trinity_balance']:.3f}")
    print(f"  Grace/Entropy:   {comb_overall['grace_entropy_balance']:.3f}")
    
    print("\n" + "="*70)
    print("IMPACT ANALYSIS: Does Your Framework Improve Coherence?")
    print("="*70)
    
    overall_delta = comb_overall['overall_score'] - ext_overall['overall_score']
    law_delta = comb_overall['law_coverage'] - ext_overall['law_coverage']
    trinity_delta = comb_overall['trinity_balance'] - ext_overall['trinity_balance']
    ge_delta = comb_overall['grace_entropy_balance'] - ext_overall['grace_entropy_balance']
    
    def print_delta(name, delta, current):
        arrow = "↑" if delta > 0 else "↓" if delta < 0 else "→"
        color = "+" if delta > 0 else ""
        print(f"{name:<20} {arrow} {color}{delta:+.3f}  (now {current:.3f})")
    
    print_delta("Overall Score", overall_delta, comb_overall['overall_score'])
    print_delta("Law Coverage", law_delta, comb_overall['law_coverage'])
    print_delta("Trinity Balance", trinity_delta, comb_overall['trinity_balance'])
    print_delta("Grace/Entropy", ge_delta, comb_overall['grace_entropy_balance'])
    
    print("\n" + "="*70)
    print("VERDICT")
    print("="*70)
    
    if overall_delta > 0.05:
        print("\n✅ SIGNIFICANT IMPROVEMENT!")
        print(f"   Your framework INCREASES overall coherence by {overall_delta:.3f}")
        print("   This suggests your Theophysics framework successfully unifies")
        print("   the external theories into a more coherent whole.")
    elif overall_delta > 0:
        print("\n✓ MODEST IMPROVEMENT")
        print(f"   Your framework slightly increases coherence by {overall_delta:.3f}")
    elif overall_delta > -0.05:
        print("\n→ NEUTRAL IMPACT")
        print(f"   Your framework maintains coherence (delta: {overall_delta:.3f})")
    else:
        print("\n⚠️  COHERENCE DECREASED")
        print(f"   Adding framework reduced coherence by {overall_delta:.3f}")
    
    if ge_delta > 0.1:
        print(f"\n🌟 GRACE BOOST: +{ge_delta:.3f}")
        print("   Your framework significantly increases grace over entropy!")
    
    # Save results
    results = {
        'external_only': {
            'papers': len(external_papers),
            'words': len(external_text.split()),
            'overall': ext_overall,
            'law_coverage': {k: v['score'] for k, v in ext_law.items()},
            'trinity_balance': ext_trin_bal,
            'grace_entropy': ext_ge
        },
        'framework_only': {
            'papers': len(framework_papers),
            'words': len(framework_text.split()),
            'overall': fw_overall,
            'law_coverage': {k: v['score'] for k, v in fw_law.items()},
            'trinity_balance': fw_trin_bal,
            'grace_entropy': fw_ge
        },
        'combined': {
            'papers': len(external_papers) + len(framework_papers),
            'words': len(combined_text.split()),
            'overall': comb_overall,
            'law_coverage': {k: v['score'] for k, v in comb_law.items()},
            'trinity_balance': comb_trin_bal,
            'grace_entropy': comb_ge
        },
        'impact': {
            'overall_delta': overall_delta,
            'law_delta': law_delta,
            'trinity_delta': trinity_delta,
            'grace_entropy_delta': ge_delta
        }
    }
    
    return results

def main():
    """Main execution"""
    print("\n" + "="*70)
    print("THEOPHYSICS FRAMEWORK COHERENCE TEST")
    print("Comparing External Papers vs External + Your Framework")
    print("="*70 + "\n")
    
    base_dir = Path(r"d:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL")
    
    print("Collecting external papers...")
    external_text, external_papers = collect_external_papers(base_dir)
    print(f"✓ Loaded {len(external_papers)} external papers\n")
    
    print("Collecting your framework papers...")
    framework_text, framework_papers = collect_framework_papers(base_dir)
    print(f"✓ Loaded {len(framework_papers)} framework papers\n")
    
    combined_text = external_text + "\n\n" + framework_text
    
    results = analyze_and_compare(
        external_text, framework_text, combined_text,
        external_papers, framework_papers
    )
    
    # Save results
    output_path = base_dir / "FRAMEWORK_IMPACT_ANALYSIS.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✓ Results saved to: {output_path}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
