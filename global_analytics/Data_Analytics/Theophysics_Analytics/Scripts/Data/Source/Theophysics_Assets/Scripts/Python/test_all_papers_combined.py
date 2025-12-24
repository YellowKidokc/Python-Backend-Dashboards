#!/usr/bin/env python3
"""
Test All External Papers Combined
Measures baseline coherence of all downloaded papers together
WITHOUT the Theophysics framework
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

def main():
    """Test all external papers combined"""
    print("\n" + "="*70)
    print("Testing All External Papers Combined")
    print("Baseline coherence WITHOUT Theophysics framework")
    print("="*70 + "\n")
    
    base_dir = Path(r"d:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL")
    
    # Collect all markdown files from all P## folders
    all_papers = []
    combined_text = ""
    
    paper_folders = sorted([d for d in base_dir.glob("P*-*") if d.is_dir()])
    
    for paper_folder in paper_folders:
        markdown_dir = paper_folder / "References" / "Markdown"
        
        if markdown_dir.exists():
            md_files = list(markdown_dir.glob("*.md"))
            
            for md_file in md_files:
                print(f"Loading: {paper_folder.name}/{md_file.name}")
                with open(md_file, 'r', encoding='utf-8') as f:
                    text = f.read()
                    combined_text += text + "\n\n"
                    all_papers.append({
                        'folder': paper_folder.name,
                        'file': md_file.name,
                        'word_count': len(text.split())
                    })
    
    print(f"\n{'='*70}")
    print(f"Loaded {len(all_papers)} papers")
    print(f"Total words: {len(combined_text.split()):,}")
    print(f"{'='*70}\n")
    
    # Analyze combined text
    print("Analyzing combined coherence...\n")
    
    law_scores = calculate_law_coverage(combined_text)
    trinity_scores, trinity_balance = calculate_trinity_balance(combined_text)
    grace_entropy = calculate_grace_entropy_ratio(combined_text)
    overall = calculate_overall_coherence(law_scores, trinity_balance, grace_entropy)
    
    # Print results
    print("="*70)
    print("COMBINED COHERENCE RESULTS")
    print("="*70)
    print(f"\n📊 OVERALL SCORE: {overall['overall_score']:.3f} ({overall['grade']})")
    print(f"   Law Coverage:        {overall['law_coverage']:.3f}")
    print(f"   Trinity Balance:     {overall['trinity_balance']:.3f}")
    print(f"   Grace/Entropy:       {overall['grace_entropy_balance']:.3f}")
    
    print(f"\n{'='*70}")
    print("TEN LAWS COVERAGE")
    print(f"{'='*70}")
    
    for law_name, law_data in law_scores.items():
        score_bar = "█" * int(law_data['score'] * 20)
        print(f"{law_data['description']:<40} {law_data['score']:.3f} {score_bar}")
        print(f"  Physical: {law_data['physical_count']:3d} | Spiritual: {law_data['spiritual_count']:3d}")
    
    print(f"\n{'='*70}")
    print("TRINITY BALANCE")
    print(f"{'='*70}")
    
    for aspect_name, aspect_data in trinity_scores.items():
        bar = "█" * int(aspect_data['percentage'] / 5)
        print(f"{aspect_name:<10} {aspect_data['percentage']:5.1f}% {bar}")
        print(f"  {aspect_data['role']}: {aspect_data['count']} mentions")
    
    print(f"\nBalance Score: {trinity_balance:.3f}")
    print(f"(1.0 = perfect balance, 0.0 = completely imbalanced)")
    
    print(f"\n{'='*70}")
    print("GRACE vs ENTROPY")
    print(f"{'='*70}")
    
    grace_bar = "█" * int(grace_entropy['grace_ratio'] * 40)
    entropy_bar = "█" * int((1 - grace_entropy['grace_ratio']) * 40)
    
    print(f"Grace:   {grace_entropy['grace_count']:4d} mentions {grace_bar}")
    print(f"Entropy: {grace_entropy['entropy_count']:4d} mentions {entropy_bar}")
    print(f"\nGrace Ratio: {grace_entropy['grace_ratio']:.3f}")
    print(f"(1.0 = all grace, 0.0 = all entropy, 0.5 = balanced)")
    
    # Save results
    results = {
        'total_papers': len(all_papers),
        'total_words': len(combined_text.split()),
        'papers': all_papers,
        'law_scores': {k: {
            'score': v['score'],
            'physical_count': v['physical_count'],
            'spiritual_count': v['spiritual_count'],
            'description': v['description']
        } for k, v in law_scores.items()},
        'trinity': {k: {
            'count': v['count'],
            'percentage': v['percentage'],
            'role': v['role']
        } for k, v in trinity_scores.items()},
        'trinity_balance': trinity_balance,
        'grace_entropy': grace_entropy,
        'overall': overall
    }
    
    output_path = base_dir / "ALL_PAPERS_COMBINED_COHERENCE.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✓ Results saved to: {output_path}")
    print(f"{'='*70}\n")
    
    # Summary interpretation
    print("="*70)
    print("INTERPRETATION")
    print("="*70)
    print(f"\nThis is the BASELINE coherence of all external papers")
    print(f"(Wheeler, Chalmers, Einstein, etc.) WITHOUT your framework.")
    print(f"\nOverall Score: {overall['overall_score']:.3f} ({overall['grade']})")
    
    if overall['overall_score'] < 0.5:
        print("\n⚠️  LOW COHERENCE - These papers don't naturally align well")
        print("   This suggests they need a unifying framework!")
    elif overall['overall_score'] < 0.7:
        print("\n⚡ MODERATE COHERENCE - Some natural alignment exists")
        print("   But there's room for a unifying framework to improve it")
    else:
        print("\n✓ HIGH COHERENCE - These papers already align well")
        print("  Your framework would need to maintain or improve this")
    
    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    main()
