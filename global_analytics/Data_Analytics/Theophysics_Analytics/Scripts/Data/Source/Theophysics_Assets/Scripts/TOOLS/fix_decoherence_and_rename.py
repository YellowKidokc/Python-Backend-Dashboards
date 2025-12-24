#!/usr/bin/env python3
"""
1. Fix Decoherence viz - move observer further right
2. Rename all Paper 2 images with descriptive names
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path
import shutil

# Output
OUTPUT_DIR = Path(r"D:\THEOPHYSICS_MASTER\Assets\Images\logos papers\P2_Quantum_Bridge")

# TVE Colors
DARK_BG = '#0a0a0a'
CYAN_OBSERVER = '#00FFFF'
PURPLE_FIELD = '#9933FF'
GREEN_ACTUAL = '#00FF00'
WHITE_SOURCE = '#FFFFFF'

def fix_decoherence_viz():
    """Fix Decoherence - move observer further right"""
    print("  Fixing Decoherence visualization...")
    
    fig = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
    ax = fig.add_subplot(111, projection='3d', facecolor=DARK_BG)
    ax.set_axis_off()
    
    def create_sphere(x_center, y_center, z_center, radius, color, alpha):
        theta = np.linspace(0, 2 * np.pi, 60)
        phi = np.linspace(0, np.pi, 60)
        THETA, PHI = np.meshgrid(theta, phi)
        x = radius * np.sin(PHI) * np.cos(THETA) + x_center
        y = radius * np.sin(PHI) * np.sin(THETA) + y_center
        z = radius * np.cos(PHI) + z_center
        ax.plot_surface(x, y, z, color=color, alpha=alpha, 
                        rstride=1, cstride=1, linewidth=0, antialiased=True)
    
    def plot_glowing_line(x_data, y_data, z_data, core_color, glow_color, core_linewidth, glow_linewidth, alpha):
        ax.plot(x_data, y_data, z_data, color=glow_color, linewidth=glow_linewidth, alpha=alpha/2)
        ax.plot(x_data, y_data, z_data, color=core_color, linewidth=core_linewidth, alpha=alpha)
    
    # Stage 1: Superposition
    np.random.seed(42)
    x_super = np.random.normal(-10, 2, 800)
    y_super = np.random.normal(0, 2, 800)
    z_super = np.random.normal(0, 2, 800)
    ax.scatter(x_super, y_super, z_super, c=PURPLE_FIELD, s=70, alpha=0.15)
    ax.text(-10, 0, 5, '1. Superposition |ψ⟩', color=PURPLE_FIELD, 
            ha='center', fontsize=24, weight='bold')
    
    # Stage 2: Decoherence (Menu of 3 Paths)
    ax.text(0, 0, 8, '2. Decoherence (The "Menu")', color=WHITE_SOURCE, 
            ha='center', fontsize=24, weight='bold')
    
    x_a = np.linspace(-5, 5, 50)
    y_a = np.full_like(x_a, 5)
    z_a = np.sin(x_a / 1.5) * 2
    ax.plot(x_a, y_a, z_a, color=CYAN_OBSERVER, alpha=0.4, linewidth=2)
    ax.text(5, 5, 3, 'Potential State A', color=CYAN_OBSERVER, ha='center', fontsize=18)
    
    x_b = np.linspace(-5, 5, 50)
    y_b = np.full_like(x_b, 0)
    z_b = np.sin(x_b / 1.5) * 2
    ax.plot(x_b, y_b, z_b, color=CYAN_OBSERVER, alpha=0.4, linewidth=2)
    ax.text(5, 0, 3, 'Potential State B', color=CYAN_OBSERVER, ha='center', fontsize=18)
    
    x_c = np.linspace(-5, 5, 50)
    y_c = np.full_like(x_c, -5)
    z_c = np.sin(x_c / 1.5) * 2
    ax.plot(x_c, y_c, z_c, color=CYAN_OBSERVER, alpha=0.4, linewidth=2)
    ax.text(5, -5, 3, 'Potential State C', color=CYAN_OBSERVER, ha='center', fontsize=18)
    
    # Stage 3: Collapse (Observer MOVED FURTHER RIGHT - from 10 to 14)
    create_sphere(14, 0, 8, 1.5, CYAN_OBSERVER, 0.9)
    ax.text(14, 0, 11, 'Observer Selects', color=CYAN_OBSERVER, ha='center', fontsize=24, weight='bold')
    
    plot_glowing_line(x_b, y_b, z_b, GREEN_ACTUAL, GREEN_ACTUAL, 5, 15, 1.0)
    ax.text(14, 0, 0, '3. Collapse → Actualized', color=GREEN_ACTUAL, ha='center', fontsize=24, weight='bold')
    
    fig.text(0.5, 0.95, 'Paper 2: Decoherence vs. Collapse',
             ha='center', fontsize=60, color='white', weight='bold')
    fig.text(0.5, 0.90, 'The 3-Stage Process of Actualization',
             ha='center', fontsize=24, color=PURPLE_FIELD, style='italic')
    fig.text(0.5, 0.05, 'Decoherence creates the "menu" of possibilities; Conscious collapse selects one to become real.',
             ha='center', fontsize=20, color='gray', style='italic')
    
    ax.view_init(elev=20, azim=-75)
    ax.set_xlim([-15, 18])  # Extended right
    ax.set_ylim([-8, 8])
    ax.set_zlim([-5, 12])
    
    plt.savefig(OUTPUT_DIR / 'P02-12-Decoherence-Collapse-V3-FIXED.png',
                dpi=300, facecolor=DARK_BG, bbox_inches='tight')
    plt.close()
    print("    ✓ Saved P02-12-Decoherence-Collapse-V3-FIXED.png")

def rename_all_files():
    """Rename all Paper 2 images with descriptive names"""
    print("\n  Renaming files with descriptive names...")
    
    # Mapping: old_name -> new_descriptive_name
    rename_map = {
        # Trinity visualizations
        'P02-02.png': 'P02-Proof8-Trinity-Triangulation.png',
        'P02-05-Trinity-Triangulation-Proof8.png': 'P02-Proof8-Trinity-Triangulation-V2.png',
        'P02-TRINITY-100PERCENT-TEST.png': 'P02-Proof8-Trinity-100Percent-Test.png',
        'P02-TRINITY-CYCLE-MASTER.png': 'P02-Trinity-Wave-Collapse-Cycle-MASTER.png',
        
        # Proofs
        'P02-06-Binary-Moral-States-Proof1.png': 'P02-Proof1-Binary-Moral-States-OLD.png',
        'P02-11-Binary-States-Proof1-V3.png': 'P02-Proof1-Binary-Moral-States-Terminator.png',
        
        'P02-08-Works-Orthogonality-Proof3.png': 'P02-Proof3-Works-Orthogonality-OLD.png',
        'P02-13-Works-Orthogonality-V3.png': 'P02-Proof3-Works-Orthogonality-Independence.png',
        
        'P02-09-Spiritual-Warfare-Proof5.png': 'P02-Proof5-Spiritual-Warfare-OLD.png',
        'P02-14-Spiritual-Warfare-V3.png': 'P02-Proof5-Quantum-Superposition-Vulnerability.png',
        
        'P02-10-Religious-Falsification-Proof7.png': 'P02-Proof7-Religious-Falsification-OLD.png',
        'P02-15-Religious-Falsification-V3.png': 'P02-Proof7-Religious-Falsification-UniqueFor more information, see: https://en.wikipedia.org/wiki/ASCII

Let me continue with a simpler approach:

<function_calls>
<invoke name="run_terminal_cmd">
<parameter name="command">cd "D:\THEOPHYSICS_MASTER\Assets\Images"; python fix_decoherence_and_rename.py
