#!/usr/bin/env python3
"""
Update all FINAL papers to use correct organized image paths
"""
import re
from pathlib import Path

# Location to update
BASE_PATH = Path("D:/THEOPHYSICS_MASTER/03_PUBLICATIONS/Logos_Papers/COMPLETE_LOGOS_PAPERS_FINAL")

# Complete image mappings
IMAGE_MAPPINGS = {
    1: {
        "P1_02_great_schism.png": "P1-02-great-schism-O-1-of-17.png",
        "P1_12_participatory_universe_3d.png": "P1-12-participatory-universe-3d-O-2-of-17.png",
        "P1_03_information_substrate.png": "P1-03-information-substrate-O-3-of-17.png",
        "P1-01_information_substrate.png": "P1-01-information-substrate-O-4-of-17.png",
        "P1observer_creates_reality_3d.png": "P1-P1observer-creates-reality-3d-O-5-of-17.png",
        "P1-02_self_referential.png": "P1-02-self-referential-O-6-of-17.png",
        "P1-03_zero_divergence.png": "P1-03-zero-divergence-O-7-of-17.png",
        "P1_04_vapor_ice_analogy.png": "P1-04-vapor-ice-analogy-O-8-of-17.png",
        "P1_05_spacetime_curvature.png": "P1-05-spacetime-curvature-O-9-of-17.png",
        "P1_06_superposition_truth.png": "P1-06-superposition-truth-O-10-of-17.png",
        "P1_04_wave_collapse_mechanism.png": "P1-04-wave-collapse-mechanism-O-11-of-17.png",
        "P1_07_three_stage_collapse.png": "P1-07-three-stage-collapse-O-12-of-17.png",
        "P1_08_shared_reality.png": "P1-08-shared-reality-O-13-of-17.png",
        "P1_09_entanglement_correlation.png": "P1-09-entanglement-correlation-O-14-of-17.png",
        "P1_10_full_spectrum.png": "P1-10-full-spectrum-O-15-of-17.png",
        "P1_05_coherence_functional.png": "P1-05-coherence-functional-O-16-of-17.png",
        "P1_13_universe_compressed_code_3d.png": "P1-13-universe-compressed-code-3d-O-17-of-17.png",
    },
    2: {
        "P2_A_consciousness_collapse_event_3d.png": "P2-A-consciousness-collapse-event-3d-O-1-of-2.png",
        "P2_07_consciousness_information.png": "P2-07-consciousness-information-O-2-of-2.png",
    },
    3: {
        "P3_02_changing_ruler.png": "P3-02-changing-ruler-O-1-of-1.png",
    },
    4: {
        "P4_01_binary_states.png": "P4-01-binary-states-O-1-of-5.png",
        "P4_02_impossibility_of_works.png": "P4-02-impossibility-of-works-O-2-of-5.png",
        "P4_03_grace_operator.png": "P4-03-grace-operator-O-3-of-5.png",
        "P4_04_magnitude_vs_sign.png": "P4-04-magnitude-vs-sign-O-4-of-5.png",
        "P4_05_null_state.png": "P4-05-null-state-O-5-of-5.png",
    },
    5: {
        "P5_13soul_quantum_field_3d.png": "P5-13soul-quantum-field-3d-O-1-of-2.png",
        "P5_P11ai_consciousness_3d.png": "P5-P11ai-consciousness-3d-O-2-of-2.png",
    },
    6: {
        "P6_07_consciousness_information.png": "P6-07-consciousness-information-O-1-of-1.png",
    },
    10: {
        "P10_P11ai_consciousness_3d.png": "P10-P11ai-consciousness-3d-O-2-of-2.png",
    },
    11: {
        "P11_P11B_validation_protocols_3d.png": "P11-P11B-validation-protocols-3d-O-2-of-2.png",
    },
    12: {
        "P12_P12decalogue_cosmos_3d.png": "P12-P12decalogue-cosmos-3d-O-1-of-1.png",
    },
}

# Chart mappings (in charts folder)
CHART_MAPPINGS = {
    3: {
        "P3_01_hubble_tension.png": "P3-01-hubble-tension-O-1-of-6.png",
        "P3_05_information_density_timeline.png": "P3-05-information-density-timeline-O-5-of-6.png",
        "P3_07_epoch_1_recombination_era.png": "P3-07-epoch-1-recombination-era-O-2-of-6.png",
        "P3_08_epoch_2_first_stars_ignite.png": "P3-08-epoch-2-first-stars-ignite-O-3-of-6.png",
        "P3_09_epoch_3_galaxy_formation.png": "P3-09-epoch-3-galaxy-formation-O-4-of-6.png",
        "P3_12_epoch_6_life_and_consciousness.png": "P3-12-epoch-6-life-and-consciousness-O-6-of-6.png",
    },
    4: {
        "P4_08_prediction_timeline.png": "P4-08-prediction-timeline-O-2-of-4.png",
        "P4_12_epoch_6_life_and_consciousness.png": "P4-12-epoch-6-life-and-consciousness-O-1-of-4.png",
        "P4_13_complete_timeline.png": "P4-13-complete-timeline-O-3-of-4.png",
        "P4_14_information_density_quantified.png": "P4-14-information-density-quantified-O-4-of-4.png",
    },
    6: {
        "P6_11_epoch_5_complex_chemistry.png": "P6-11-epoch-5-complex-chemistry-O-1-of-1.png",
    },
    7: {
        "P7_01_hubble_tension.png": "P7-01-hubble-tension-O-1-of-1.png",
    },
}

def update_paper_images(paper_path, paper_num):
    """Update image paths in a paper"""
    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    mappings = IMAGE_MAPPINGS.get(paper_num, {})
    chart_mappings = CHART_MAPPINGS.get(paper_num, {})
    
    # Update regular images
    for old_name, new_name in mappings.items():
        # Pattern 1: ../assets/P1/old_name.png
        pattern1 = f'../assets/P{paper_num}/{old_name}'
        replacement1 = f'../assets/P{paper_num}/{new_name}'
        content = content.replace(pattern1, replacement1)
        
        # Pattern 2: ../../../../Assets/Images/logos papers/P1_Logos_Principle/old_name.png
        pattern2 = f'../../../../Assets/Images/logos papers/P{paper_num}_[^/]+/{re.escape(old_name)}'
        content = re.sub(pattern2, replacement1, content)
    
    # Update charts
    for old_name, new_name in chart_mappings.items():
        # Pattern: ../assets/charts/old_name.png or ../../../../Assets/.../charts/...
        pattern1 = f'../assets/charts/{old_name}'
        replacement1 = f'../assets/charts/{new_name}'
        content = content.replace(pattern1, replacement1)
        
        pattern2 = f'../../../../Assets/Images/logos papers/[^/]+/charts/{re.escape(old_name)}'
        content = re.sub(pattern2, replacement1, content)
    
    if content != original:
        with open(paper_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

if __name__ == "__main__":
    if not BASE_PATH.exists():
        print(f"Path {BASE_PATH} doesn't exist")
        exit(1)
    
    print(f"Processing papers in: {BASE_PATH}\n")
    papers_updated = []
    
    for paper_file in sorted(BASE_PATH.glob("Paper-*-FINAL.md")):
        match = re.search(r'Paper-(\d+)-', paper_file.name)
        if not match:
            continue
        
        paper_num = int(match.group(1))
        if update_paper_images(paper_file, paper_num):
            papers_updated.append(paper_file.name)
            print(f"  ✓ Updated: {paper_file.name}")
    
    print(f"\n{'='*60}")
    print(f"Updated {len(papers_updated)} papers")
    print(f"{'='*60}")

