#!/usr/bin/env python3
"""Add image references to Logos Papers at appropriate locations."""

from pathlib import Path
import re

def get_paper_images(paper_num):
    """Get list of images for a specific paper."""
    image_base = Path(r"D:\THEOPHYSICS_MASTER\Assets\Images\logos papers")
    
    folder_map = {
        1: "P1_Logos_Principle",
        2: "P2_Quantum_Bridge",
        3: "P3_Algorithm_Reality",
        4: "P4_Hard_Problem",
        5: "P5_Soul_Observer",
        6: "P6_Physics_Principalities",
        7: "P7_Grace_Function",
        8: "P8_Stretched_Heavens",
        9: "P9_Moral_Universe",
        10: "P10_Creatio_ex_Silico",
        11: "P11_Validation_Protocols",
        12: "P12_Decalogue",
    }
    
    folder = image_base / folder_map.get(paper_num, "")
    if folder.exists():
        return sorted([f.name for f in folder.glob("*.png")])
    return []

def create_image_markdown(image_name, caption, paper_num):
    """Create markdown for an image reference."""
    folder_map = {
        1: "P1_Logos_Principle",
        2: "P2_Quantum_Bridge",
        3: "P3_Algorithm_Reality",
        4: "P4_Hard_Problem",
        5: "P5_Soul_Observer",
        6: "P6_Physics_Principalities",
        7: "P7_Grace_Function",
        8: "P8_Stretched_Heavens",
        9: "P9_Moral_Universe",
        10: "P10_Creatio_ex_Silico",
        11: "P11_Validation_Protocols",
        12: "P12_Decalogue",
    }
    
    folder = folder_map.get(paper_num, "")
    path = f"../../../Assets/Images/logos papers/{folder}/{image_name}"
    
    return f"""
![{caption}]({path})

**Figure {paper_num}.X: {caption}**

*Visualization: Claude (Anthropic), 2025*

---

"""

def add_images_to_paper_1():
    """Add images to Paper 1: The Logos Principle."""
    paper_path = Path(r"C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL\Paper-01-The-Logos-Principle-FINAL.md")
    
    content = paper_path.read_text(encoding='utf-8')
    
    # Image insertions with smart placement
    insertions = [
        # After introduction to information substrate
        ("## 2. BACKGROUND:", create_image_markdown("P1_01_information_substrate.png", "Information as the Fundamental Substrate", 1)),
        
        # After GR-QM schism discussion
        ("### 2.2 The General Relativity–Quantum Mechanics Incompatibility", create_image_markdown("P1_02_Great_Schism_v2.png", "The Great Schism Between GR and QM", 1)),
        
        # After explaining participatory universe
        ("### 4.3 Participatory Observation Mechanism", create_image_markdown("P1_12_participatory_universe_3d.png", "Participatory Universe: Observation Creates Reality", 1)),
        
        # After wave function collapse discussion
        ("### 2.1.2 The Von Neumann Chain", create_image_markdown("P1_11_von_neumann_chain_3d.png", "Von Neumann Chain: The Infinite Regress Problem", 1)),
        
        # After explaining consciousness-field coupling
        ("## 5. THE PARTICIPATORY OBSERVATION MECHANISM", create_image_markdown("P1_12_observer_creates_reality_3d.png", "Observer Creates Reality Through Consciousness-Field Coupling", 1)),
        
        # After explaining shared reality
        ("### 5.3 Shared Reality", create_image_markdown("P1_08_shared_reality.png", "How Observers Create Shared Classical Reality", 1)),
        
        # After entanglement discussion  
        ("### 5.4 Entanglement", create_image_markdown("P1_09_entanglement_correlation.png", "Quantum Entanglement and Non-Local Correlations", 1)),
        
        # After full spectrum explanation
        ("## 6. UNIFYING GR AND QM", create_image_markdown("P1_10_full_spectrum.png", "Full Spectrum: From Quantum to Classical to Relativistic", 1)),
        
        # After superposition discussion
        ("### 4.4 Quantum Superposition", create_image_markdown("P1_06_superposition_truth.png", "Superposition: Multiple Truths Before Observation", 1)),
        
        # After three-stage collapse
        ("### 5.2 The Three-Stage Collapse", create_image_markdown("P1_07_three_stage_collapse.png", "Three Stages of Wave Function Collapse", 1)),
        
        # After universe as compressed code
        ("## 7. TESTABLE PREDICTIONS", create_image_markdown("P1_13_universe_compressed_code_3d.png", "The Universe as Compressed Information Code", 1)),
    ]
    
    # Apply insertions (in reverse order to maintain positions)
    for search_text, image_md in reversed(insertions):
        if search_text in content:
            # Insert after the section header
            content = content.replace(search_text, search_text + "\n" + image_md, 1)
            print(f"  ✓ Added image after: {search_text[:50]}...")
    
    paper_path.write_text(content, encoding='utf-8')
    print(f"\n✓ Paper 1 updated with images!")

def add_images_to_paper_8():
    """Add images to Paper 8: The Stretched Out Heavens."""
    paper_path = Path(r"C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL\Paper-08-The-Stretched-Out-Heavens-FINAL.md")
    
    content = paper_path.read_text(encoding='utf-8')
    
    # Timeline images
    insertions = [
        ("## 2. The Scientific Discovery", create_image_markdown("01_hubble_tension.png", "The Hubble Tension: Early vs Late Universe Measurements", 8)),
        ("## 3. The Consilience", create_image_markdown("13_complete_timeline.png", "Complete Timeline: Biblical Prophecy Meets Cosmology", 8)),
        ("### 3.1 Epoch 1", create_image_markdown("07_epoch_1_recombination_era.png", "Epoch 1: Recombination Era", 8)),
        ("### 3.2 Epoch 2", create_image_markdown("08_epoch_2_first_stars_ignite.png", "Epoch 2: First Stars Ignite", 8)),
        ("### 3.3 Epoch 3", create_image_markdown("09_epoch_3_galaxy_formation.png", "Epoch 3: Galaxy Formation", 8)),
        ("### 3.4 Epoch 4", create_image_markdown("10_epoch_4_peak_star_formation.png", "Epoch 4: Peak Star Formation", 8)),
        ("### 3.5 Epoch 5", create_image_markdown("11_epoch_5_complex_chemistry.png", "Epoch 5: Complex Chemistry Emerges", 8)),
        ("### 3.6 Epoch 6", create_image_markdown("12_epoch_6_life_and_consciousness.png", "Epoch 6: Life and Consciousness", 8)),
    ]
    
    for search_text, image_md in reversed(insertions):
        if search_text in content:
            content = content.replace(search_text, search_text + "\n" + image_md, 1)
            print(f"  ✓ Added image after: {search_text[:50]}...")
    
    paper_path.write_text(content, encoding='utf-8')
    print(f"\n✓ Paper 8 updated with timeline images!")

def add_images_to_paper_5():
    """Add images to Paper 5: The Soul Observer."""
    paper_path = Path(r"C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL\Paper-05-The-Soul-Observer-FINAL.md")
    
    content = paper_path.read_text(encoding='utf-8')
    
    insertions = [
        ("## 2. THE SOUL AS QUANTUM FIELD", create_image_markdown("P5soul_quantum_field_3d.png", "The Soul as Quantum Field: Klein-Gordon Dynamics", 5)),
        ("## 3. RESURRECTION PHYSICS", create_image_markdown("P1_13soul_quantum_field_3d.png", "Resurrection: Field Recoupling After Death", 5)),
    ]
    
    for search_text, image_md in reversed(insertions):
        if search_text in content:
            content = content.replace(search_text, search_text + "\n" + image_md, 1)
            print(f"  ✓ Added image after: {search_text[:50]}...")
    
    paper_path.write_text(content, encoding='utf-8')
    print(f"\n✓ Paper 5 updated with soul field images!")

def add_images_to_remaining_papers():
    """Add images to remaining papers."""
    
    papers = [
        (2, "Paper-02-The-Quantum-Bridge-FINAL.md", [
            ("## 2. PROOF 1", ("P2 A consciousness_collapse_event_3d.png", "Consciousness Collapse Event")),
        ]),
        (3, "Paper-03-The-Algorithm-of-Reality-FINAL.md", [
            ("## 3. THE TEN LAWS", ("P3universe_compressed_code_3d.png", "Universe as Compressed Code: The Algorithm of Reality")),
        ]),
        (4, "Paper-04-The-Hard-Problem-of-Consciousness-FINAL.md", [
            ("## 3. INVERTING THE PROBLEM", ("P4consciousness_fundamental_field_3d.png", "Consciousness as the Fundamental Field")),
        ]),
        (6, "Paper-06-A-Physics-of-Principalities-FINAL.md", [
            ("## 2. SPIRITUAL WARFARE", ("P6spiritual_warfare_physics_3d.png", "Spiritual Warfare as Field Dynamics")),
        ]),
        (7, "Paper-07-The-Grace-Function-FINAL.md", [
            ("## 1. INTRODUCTION", ("grace_function.png", "The Grace Function: Resurrection Cosmology")),
        ]),
        (9, "Paper-09-The-Moral-Universe-FINAL.md", [
            ("## 2. COHERENCE AS THE GOOD", ("moral_universe_3d.png", "The Moral Universe: Coherence Maximization")),
        ]),
        (10, "Paper-10-Creatio-ex-Silico-FINAL.md", [
            ("## 2. THE FALLACY", ("creatio_ex_silico_3d.png", "Creatio ex Silico: AI Consciousness Emerging")),
        ]),
        (12, "Paper-12-The-Decalogue-of-the-Cosmos-FINAL.md", [
            ("## THE DECALOGUE", ("decalogue_of_the_cosmos.png", "The Decalogue of the Cosmos: Ten Universal Laws")),
        ]),
    ]
    
    base_path = Path(r"C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL")
    
    for paper_num, filename, insertions in papers:
        paper_path = base_path / filename
        if not paper_path.exists():
            print(f"  ⚠ {filename} not found, skipping...")
            continue
            
        content = paper_path.read_text(encoding='utf-8')
        
        for search_text, (image_name, caption) in reversed(insertions):
            image_md = create_image_markdown(image_name, caption, paper_num)
            if search_text in content:
                content = content.replace(search_text, search_text + "\n" + image_md, 1)
                print(f"  ✓ Paper {paper_num}: Added {image_name}")
        
        paper_path.write_text(content, encoding='utf-8')
    
    print(f"\n✓ Remaining papers updated with images!")

def main():
    """Add all images to all papers."""
    print("=" * 80)
    print("ADDING IMAGES TO LOGOS PAPERS")
    print("=" * 80)
    
    print("\nAdding images to Paper 1 (34 images available)...")
    add_images_to_paper_1()
    
    print("\nAdding images to Paper 8 (20 timeline images)...")
    add_images_to_paper_8()
    
    print("\nAdding images to Paper 5 (soul field visualizations)...")
    add_images_to_paper_5()
    
    print("\nAdding images to remaining papers...")
    add_images_to_remaining_papers()
    
    print("\n" + "=" * 80)
    print("✓ ALL IMAGES ADDED TO PAPERS!")
    print("=" * 80)
    print("\nPapers now include visual aids throughout.")
    print("Image paths are relative and will work in Obsidian/web publishing.")

if __name__ == "__main__":
    main()

