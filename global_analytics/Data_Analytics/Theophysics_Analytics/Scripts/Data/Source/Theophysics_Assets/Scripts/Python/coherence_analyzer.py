#!/usr/bin/env python3
"""
Lowe Coherence Lagrangian Analyzer
Tests academic papers against the Theophysics framework
Based on the Lowe Coherence Lagrangian principles
"""

import os
import sys
import json
import re
from pathlib import Path
from collections import defaultdict
import csv

def install_if_needed(package):
    """Install package if not available"""
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        os.system(f"{sys.executable} -m pip install {package} -q")

# Install required packages
install_if_needed('numpy')

import numpy as np

# ============================================================================
# TEN LAWS FRAMEWORK - Physical ↔ Spiritual Isomorphisms
# ============================================================================

TEN_LAWS = {
    'LAW_01_GRAVITY_BELONGING': {
        'physical': ['gravity', 'gravitational', 'curvature', 'spacetime', 'mass', 'attraction'],
        'spiritual': ['belonging', 'unity', 'connection', 'relationship', 'communion', 'love'],
        'symbol': 'G',
        'description': 'Gravity ↔ Belonging'
    },
    'LAW_02_STRONG_COVENANT': {
        'physical': ['strong force', 'nuclear', 'binding', 'quark', 'gluon', 'confinement'],
        'spiritual': ['covenant', 'commitment', 'promise', 'bond', 'oath', 'fidelity'],
        'symbol': 'M',
        'description': 'Strong Force ↔ Covenant'
    },
    'LAW_03_EM_TRUTH': {
        'physical': ['electromagnetic', 'light', 'photon', 'wave', 'radiation', 'field'],
        'spiritual': ['truth', 'revelation', 'knowledge', 'information', 'communication', 'word'],
        'symbol': 'E',
        'description': 'Electromagnetism ↔ Truth'
    },
    'LAW_04_THERMO_ENTROPY': {
        'physical': ['entropy', 'thermodynamics', 'disorder', 'heat', 'irreversible', 'decay'],
        'spiritual': ['sin', 'corruption', 'fall', 'death', 'chaos', 'separation'],
        'symbol': 'S',
        'description': 'Thermodynamics ↔ Entropy/Sin'
    },
    'LAW_05_QUANTUM_FAITH': {
        'physical': ['quantum', 'superposition', 'probability', 'wave function', 'uncertainty', 'potential'],
        'spiritual': ['faith', 'hope', 'possibility', 'trust', 'belief', 'unseen'],
        'symbol': 'T',
        'description': 'Quantum Mechanics ↔ Faith'
    },
    'LAW_06_MEASUREMENT_INCARNATION': {
        'physical': ['measurement', 'observation', 'collapse', 'observer', 'actualization', 'concrete'],
        'spiritual': ['incarnation', 'manifestation', 'embodiment', 'presence', 'actualization', 'christ'],
        'symbol': 'K',
        'description': 'Measurement ↔ Incarnation'
    },
    'LAW_07_NEGENTROPY_FORGIVENESS': {
        'physical': ['negentropy', 'order', 'organization', 'life', 'complexity', 'information'],
        'spiritual': ['grace', 'forgiveness', 'redemption', 'restoration', 'healing', 'salvation'],
        'symbol': 'R',
        'description': 'Negentropy ↔ Forgiveness/Grace'
    },
    'LAW_08_RELATIVITY_COMPASSION': {
        'physical': ['relativity', 'frame', 'perspective', 'transformation', 'invariance', 'equivalence'],
        'spiritual': ['compassion', 'empathy', 'understanding', 'perspective', 'mercy', 'love'],
        'symbol': 'Q',
        'description': 'Relativity ↔ Compassion'
    },
    'LAW_09_RESONANCE_COMMUNION': {
        'physical': ['resonance', 'synchronization', 'coherence', 'harmony', 'oscillation', 'coupling'],
        'spiritual': ['communion', 'fellowship', 'unity', 'worship', 'prayer', 'spirit'],
        'symbol': 'F',
        'description': 'Resonance ↔ Communion'
    },
    'LAW_10_CPT_RESURRECTION': {
        'physical': ['symmetry', 'conservation', 'reversibility', 'CPT', 'invariance', 'restoration'],
        'spiritual': ['resurrection', 'eternal life', 'restoration', 'renewal', 'transformation', 'glory'],
        'symbol': 'C',
        'description': 'CPT Symmetry ↔ Resurrection'
    }
}

# ============================================================================
# TRINITY FRAMEWORK
# ============================================================================

TRINITY_ASPECTS = {
    'FATHER': {
        'keywords': ['source', 'origin', 'creator', 'foundation', 'axiom', 'principle', 'law', 'authority'],
        'symbol': 'Θ',
        'role': 'Source/Lawgiver'
    },
    'SON': {
        'keywords': ['manifestation', 'form', 'embodiment', 'incarnation', 'christ', 'logos', 'word', 'mediator'],
        'symbol': 'Λ',
        'role': 'Manifestation/Form'
    },
    'SPIRIT': {
        'keywords': ['coherence', 'relation', 'connection', 'field', 'interaction', 'communion', 'unity', 'bond'],
        'symbol': 'Ψ',
        'role': 'Coherence/Relation'
    }
}

# ============================================================================
# COHERENCE METRICS
# ============================================================================

def calculate_law_coverage(text):
    """Calculate how many of the Ten Laws are represented in the text"""
    text_lower = text.lower()
    law_scores = {}
    
    for law_name, law_data in TEN_LAWS.items():
        # Count physical keywords
        physical_count = sum(1 for kw in law_data['physical'] if kw in text_lower)
        # Count spiritual keywords
        spiritual_count = sum(1 for kw in law_data['spiritual'] if kw in text_lower)
        
        # Score: both physical and spiritual present = high coherence
        if physical_count > 0 and spiritual_count > 0:
            score = min(physical_count + spiritual_count, 10) / 10.0
        elif physical_count > 0 or spiritual_count > 0:
            score = min(physical_count + spiritual_count, 5) / 10.0
        else:
            score = 0.0
        
        law_scores[law_name] = {
            'score': score,
            'physical_count': physical_count,
            'spiritual_count': spiritual_count,
            'description': law_data['description']
        }
    
    return law_scores

def calculate_trinity_balance(text):
    """Calculate Trinity balance (Father-Son-Spirit)"""
    text_lower = text.lower()
    trinity_scores = {}
    
    for aspect_name, aspect_data in TRINITY_ASPECTS.items():
        count = sum(1 for kw in aspect_data['keywords'] if kw in text_lower)
        trinity_scores[aspect_name] = {
            'count': count,
            'role': aspect_data['role']
        }
    
    total = sum(t['count'] for t in trinity_scores.values())
    if total > 0:
        for aspect in trinity_scores.values():
            aspect['percentage'] = (aspect['count'] / total) * 100
    else:
        for aspect in trinity_scores.values():
            aspect['percentage'] = 0
    
    # Calculate balance score (ideal is 33.33% each)
    balance_score = 1.0 - (np.std([t['percentage'] for t in trinity_scores.values()]) / 33.33)
    balance_score = max(0, min(1, balance_score))
    
    return trinity_scores, balance_score

def calculate_grace_entropy_ratio(text):
    """Calculate Grace vs Entropy balance (G - S metric)"""
    text_lower = text.lower()
    
    # Grace keywords (Law 7 + positive terms)
    grace_keywords = TEN_LAWS['LAW_07_NEGENTROPY_FORGIVENESS']['spiritual'] + \
                     ['order', 'organization', 'life', 'healing', 'restoration']
    
    # Entropy keywords (Law 4 + negative terms)
    entropy_keywords = TEN_LAWS['LAW_04_THERMO_ENTROPY']['spiritual'] + \
                       ['disorder', 'chaos', 'death', 'decay', 'corruption']
    
    grace_count = sum(1 for kw in grace_keywords if kw in text_lower)
    entropy_count = sum(1 for kw in entropy_keywords if kw in text_lower)
    
    total = grace_count + entropy_count
    if total > 0:
        grace_ratio = grace_count / total
    else:
        grace_ratio = 0.5  # Neutral if neither present
    
    return {
        'grace_count': grace_count,
        'entropy_count': entropy_count,
        'grace_ratio': grace_ratio,
        'balance': grace_ratio  # 1.0 = all grace, 0.0 = all entropy, 0.5 = balanced
    }

def calculate_overall_coherence(law_scores, trinity_balance, grace_entropy):
    """Calculate overall Logos coherence score"""
    
    # Law coverage score (average of all laws)
    law_coverage = np.mean([law['score'] for law in law_scores.values()])
    
    # Trinity balance score
    trinity_score = trinity_balance
    
    # Grace-Entropy score (prefer grace > entropy)
    ge_score = grace_entropy['balance']
    
    # Overall coherence (weighted average)
    overall = (law_coverage * 0.5) + (trinity_score * 0.25) + (ge_score * 0.25)
    
    return {
        'overall_score': overall,
        'law_coverage': law_coverage,
        'trinity_balance': trinity_score,
        'grace_entropy_balance': ge_score,
        'grade': get_coherence_grade(overall)
    }

def get_coherence_grade(score):
    """Convert score to letter grade"""
    if score >= 0.9: return 'A+'
    elif score >= 0.85: return 'A'
    elif score >= 0.8: return 'A-'
    elif score >= 0.75: return 'B+'
    elif score >= 0.7: return 'B'
    elif score >= 0.65: return 'B-'
    elif score >= 0.6: return 'C+'
    elif score >= 0.55: return 'C'
    elif score >= 0.5: return 'C-'
    else: return 'D'

# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def analyze_single_paper(markdown_path):
    """Analyze a single paper's coherence"""
    with open(markdown_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    law_scores = calculate_law_coverage(text)
    trinity_scores, trinity_balance = calculate_trinity_balance(text)
    grace_entropy = calculate_grace_entropy_ratio(text)
    overall = calculate_overall_coherence(law_scores, trinity_balance, grace_entropy)
    
    return {
        'file': markdown_path.name,
        'law_scores': law_scores,
        'trinity': trinity_scores,
        'trinity_balance': trinity_balance,
        'grace_entropy': grace_entropy,
        'overall': overall,
        'word_count': len(text.split())
    }

def analyze_paper_folder(paper_folder):
    """Analyze all papers in a P## folder"""
    markdown_dir = paper_folder / "References" / "Markdown"
    
    if not markdown_dir.exists():
        return None
    
    md_files = list(markdown_dir.glob("*.md"))
    if not md_files:
        return None
    
    # Analyze each paper individually
    individual_results = []
    for md_file in md_files:
        result = analyze_single_paper(md_file)
        individual_results.append(result)
    
    # Combine all papers in folder
    combined_text = ""
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            combined_text += f.read() + "\n\n"
    
    # Analyze combined
    law_scores = calculate_law_coverage(combined_text)
    trinity_scores, trinity_balance = calculate_trinity_balance(combined_text)
    grace_entropy = calculate_grace_entropy_ratio(combined_text)
    overall = calculate_overall_coherence(law_scores, trinity_balance, grace_entropy)
    
    return {
        'paper_folder': paper_folder.name,
        'individual_papers': individual_results,
        'combined_analysis': {
            'law_scores': law_scores,
            'trinity': trinity_scores,
            'trinity_balance': trinity_balance,
            'grace_entropy': grace_entropy,
            'overall': overall,
            'total_papers': len(md_files),
            'total_words': len(combined_text.split())
        }
    }

def save_results(results, output_dir):
    """Save analysis results to Data_Analytics folder"""
    analytics_dir = output_dir / "Data_Analytics"
    analytics_dir.mkdir(exist_ok=True)
    
    # Save JSON
    json_path = analytics_dir / "coherence_analysis.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    # Save CSV summary
    csv_path = analytics_dir / "coherence_summary.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Paper', 'Overall_Score', 'Grade', 'Law_Coverage', 'Trinity_Balance', 'Grace_Entropy', 'Word_Count'])
        
        if 'individual_papers' in results:
            for paper in results['individual_papers']:
                writer.writerow([
                    paper['file'],
                    f"{paper['overall']['overall_score']:.3f}",
                    paper['overall']['grade'],
                    f"{paper['overall']['law_coverage']:.3f}",
                    f"{paper['overall']['trinity_balance']:.3f}",
                    f"{paper['overall']['grace_entropy_balance']:.3f}",
                    paper['word_count']
                ])
    
    print(f"  ✓ Saved to {analytics_dir}")

def main():
    """Main execution"""
    print("\n" + "="*70)
    print("Lowe Coherence Lagrangian Analyzer")
    print("Testing papers against Theophysics framework")
    print("="*70 + "\n")
    
    base_dir = Path(r"d:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL")
    
    # Find all P## folders
    paper_folders = sorted([d for d in base_dir.glob("P*-*") if d.is_dir()])
    
    print(f"Found {len(paper_folders)} paper folders\n")
    
    all_results = {}
    
    # Analyze each folder
    for paper_folder in paper_folders:
        print(f"Analyzing {paper_folder.name}...")
        result = analyze_paper_folder(paper_folder)
        
        if result:
            all_results[paper_folder.name] = result
            save_results(result, paper_folder)
            
            # Print summary
            combined = result['combined_analysis']
            print(f"  Papers: {combined['total_papers']}")
            print(f"  Overall Score: {combined['overall']['overall_score']:.3f} ({combined['overall']['grade']})")
            print(f"  Law Coverage: {combined['overall']['law_coverage']:.3f}")
            print(f"  Trinity Balance: {combined['overall']['trinity_balance']:.3f}")
            print(f"  Grace/Entropy: {combined['overall']['grace_entropy_balance']:.3f}")
        else:
            print(f"  ⚠ No markdown files found")
        print()
    
    # Save master results
    master_path = base_dir / "MASTER_COHERENCE_ANALYSIS.json"
    with open(master_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print("="*70)
    print("Analysis Complete!")
    print(f"✓ Master results: {master_path}")
    print("✓ Individual results in each P##/Data_Analytics/")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
