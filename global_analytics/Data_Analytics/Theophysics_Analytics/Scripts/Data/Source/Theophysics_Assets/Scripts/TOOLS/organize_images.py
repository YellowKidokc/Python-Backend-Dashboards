#!/usr/bin/env python3
"""Organize Logos Papers images into correct folder structure."""

import shutil
from pathlib import Path

def organize_images():
    """Organize all images according to YAML asset_folder specifications."""
    
    base_dir = Path(r"D:\THEOPHYSICS_MASTER\Assets\Images\logos papers")
    
    # Define correct folder structure (from YAML)
    correct_folders = {
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
    
    # Old folder names to rename
    old_folders = {
        "LGP_01_The_Logos_Principle": 1,
        "LGP_02_The_Quantum_Bridge": 2,
        "LGP_03_The_Algorithm_of_Reality": 3,
        "LGP_04_The_Hard_Problem_of_Consciousness": 4,
        "LGP_05_The_Soul_as_Quantum_Observer": 5,
        "LGP_06_A_Physics_of_Principalities": 6,
        "LGP_07_The_Grace_Function": 7,
        "LGP_08_The_Stretched_Out_Heavens": 8,
        "LGP_09_The_Moral_Universe": 9,
        "LGP_10_Creatio_ex_Silico": 10,
    }
    
    print("=" * 80)
    print("ORGANIZING LOGOS PAPERS IMAGES")
    print("=" * 80)
    
    # Step 1: Create correct folder structure
    print("\nStep 1: Creating correct folder structure...")
    for num, folder_name in correct_folders.items():
        folder_path = base_dir / folder_name
        folder_path.mkdir(exist_ok=True)
        print(f"  ✓ {folder_name}")
    
    # Step 2: Move files from old folders to new folders
    print("\nStep 2: Moving files from old folders...")
    for old_folder, paper_num in old_folders.items():
        old_path = base_dir / old_folder
        if old_path.exists():
            new_folder = correct_folders[paper_num]
            new_path = base_dir / new_folder
            
            print(f"\n  Moving: {old_folder} → {new_folder}")
            
            # Move all files
            for file in old_path.iterdir():
                if file.is_file():
                    dest = new_path / file.name
                    if not dest.exists():
                        shutil.move(str(file), str(dest))
                        print(f"    → {file.name}")
            
            # Remove old folder if empty
            if not any(old_path.iterdir()):
                old_path.rmdir()
                print(f"  ✓ Removed empty folder: {old_folder}")
    
    # Step 3: Move loose files in root to correct folders
    print("\nStep 3: Moving loose files to correct folders...")
    
    # Files to move
    moves = {
        "creatio_ex_silico.png": "P10_Creatio_ex_Silico",
        "moral_universe.png": "P9_Moral_Universe",
        "stretched_heavens.png": "P8_Stretched_Heavens",
        "P04-01-Binary-Consciousness.png": "P4_Hard_Problem",
        "P4B_soul_quantum_field_3d.png": "P5_Soul_Observer",
        "P4soul_quantum_field_3d.png": "P5_Soul_Observer",
    }
    
    for filename, target_folder in moves.items():
        source = base_dir / filename
        if source.exists():
            dest = base_dir / target_folder / filename
            if not dest.exists():
                shutil.move(str(source), str(dest))
                print(f"  ✓ {filename} → {target_folder}")
    
    # Step 4: Move main Images folder files
    print("\nStep 4: Checking parent Images folder...")
    parent_dir = base_dir.parent
    
    parent_moves = {
        "grace_function.png": "P7_Grace_Function",
        "decalogue_of_the_cosmos.png": "P12_Decalogue",
        "protocols_for_validation.png": "P11_Validation_Protocols",
        "soul_as_quantum_field.png": "P5_Soul_Observer",
    }
    
    for filename, target_folder in parent_moves.items():
        source = parent_dir / filename
        if source.exists():
            dest = base_dir / target_folder / filename
            if not dest.exists():
                shutil.move(str(source), str(dest))
                print(f"  ✓ {filename} → {target_folder}")
    
    # Step 5: Summary
    print("\n" + "=" * 80)
    print("ORGANIZATION COMPLETE")
    print("=" * 80)
    
    for num, folder_name in correct_folders.items():
        folder_path = base_dir / folder_name
        file_count = len(list(folder_path.glob("*.png")))
        print(f"  Paper {num:02d}: {file_count} images in {folder_name}")
    
    print("\n✓ All images organized!")

if __name__ == "__main__":
    organize_images()

