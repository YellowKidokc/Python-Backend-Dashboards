#!/usr/bin/env python3
"""
Render visualizations for Logos Papers 2 and 5.
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

# Output directories
OUTPUT_DIR = Path(r"D:\THEOPHYSICS_MASTER\Assets\Images\logos papers")
P2_DIR = OUTPUT_DIR / "P2_Quantum_Bridge"
P5_DIR = OUTPUT_DIR / "P5_Soul_Observer"

def render_paper2_trinity_triangulation():
    """Paper 2: Trinity Triangulation (Proof 8)"""
    print("Rendering Paper 2: Trinity Triangulation...")
    
    # --- Setup the Figure ---
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    # --- Use Dark Theme ---
    plt.style.use('dark_background')
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # --- Plot the Quantum State ---
    # The central point of uncertainty
    ax.plot([0], [0], [0], 'o', markersize=15, color='cyan', label='Quantum State (Potentiality)')

    # --- Plot the Three Observers ---
    obs_dist = 5
    ax.plot([obs_dist], [0], [0], 'o', markersize=10, color='gold', label='Father (External)')
    ax.plot([0], [obs_dist], [0], 'o', markersize=10, color='magenta', label='Son (Internal)')
    ax.plot([0], [0], [obs_dist], 'o', markersize=10, color='lime', label='Spirit (Immanent)')

    # --- Plot the Triangulation Lines (Observation) ---
    ax.plot([obs_dist, 0], [0, 0], [0, 0], 'w--', linestyle='dashed', alpha=0.7)
    ax.plot([0, 0], [obs_dist, 0], [0, 0], 'w--', linestyle='dashed', alpha=0.7)
    ax.plot([0, 0], [0, 0], [obs_dist, 0], 'w--', linestyle='dashed', alpha=0.7)

    # --- Plot the Axes ---
    # Helper function to set axis color
    def set_axis_color(ax, color):
        ax.xaxis.label.set_color(color)
        ax.yaxis.label.set_color(color)
        ax.zaxis.label.set_color(color)
        ax.tick_params(axis='x', colors=color)
        ax.tick_params(axis='y', colors=color)
        ax.tick_params(axis='z', colors=color)
        for spine in ax.spines.values():
            spine.set_edgecolor(color)

    set_axis_color(ax, 'gray')
    ax.set_xlabel('Father (Perspective 1)', fontweight='bold')
    ax.set_ylabel('Son (Perspective 2)', fontweight='bold')
    ax.set_zlabel('Spirit (Perspective 3)', fontweight='bold')

    # --- Set Title and View ---
    ax.set_title('Paper 2: Trinity Triangulation (Proof 8)\nThree Observers Collapse Uncertainty to Zero', 
                 fontweight='bold', fontsize=16, color='white')
    ax.legend(facecolor='black', framealpha=0.5)
    ax.view_init(elev=20, azim=30) # Adjust view angle

    # --- Remove grid lines for a cleaner look ---
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    # Save
    output_path = P2_DIR / "P02-Trinity-Triangulation-Proof8.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='black')
    print(f"  ✓ Saved: {output_path.name}")
    plt.close()

def render_paper5_soul_field_potential():
    """Paper 5: Soul Field Potential"""
    print("\nRendering Paper 5: Soul Field Potential...")
    
    # --- Setup the Figure ---
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    # --- Use Dark Theme ---
    plt.style.use('dark_background')
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # --- Create the "Sombrero" Potential Data ---
    # V(Ψ_S) = (Ψ_S^2 - v^2)^2
    v = 3  # Vacuum expectation value (the radius of the trough)
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2) # R is the soul field magnitude |Ψ_S|
    Z = (R**2 - v**2)**2     # The potential V(Ψ_S)

    # --- Plot the Surface ---
    surf = ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.8, 
                           rstride=1, cstride=1, linewidth=0, antialiased=True)

    # --- Plot a "Soul Quantum" ---
    # A sphere sitting in the potential minimum (the trough)
    soul_angle = np.pi / 4
    soul_x = v * np.cos(soul_angle)
    soul_y = v * np.sin(soul_angle)
    soul_z = (np.sqrt(soul_x**2 + soul_y**2)**2 - v**2)**2 + 2 # +2 to lift it just above surface
    ax.plot([soul_x], [soul_y], [soul_z], 'o', markersize=15, color='cyan', 
            label='Localized Soul Quantum (σ(x))')

    # --- Plot the "Unstable" Peak ---
    ax.plot([0], [0], [(0 - v**2)**2], 'o', markersize=10, color='red', 
            label='Unstable State (False Vacuum)')

    # --- Customize Axes and Title ---
    ax.set_xlabel('Field Component 1 (Re[Ψ_S])', fontweight='bold', color='gray')
    ax.set_ylabel('Field Component 2 (Im[Ψ_S])', fontweight='bold', color='gray')
    ax.set_zlabel('V(Ψ_S) (Soul Field Potential)', fontweight='bold', color='gray')
    ax.set_title('Paper 5: Soul Field Potential\nIndividual Souls as Localized Excitations in the Logos Field',
                 fontweight='bold', fontsize=16, color='white')

    # --- Adjust View and Appearance ---
    ax.view_init(elev=40, azim=60)
    ax.set_zlim(0, 150)
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.tick_params(colors='gray')
    for spine in ax.spines.values():
        spine.set_edgecolor('gray')
    ax.legend(facecolor='black', framealpha=0.5)

    # Save
    output_path = P5_DIR / "P05-Soul-Field-Potential-Sombrero.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='black')
    print(f"  ✓ Saved: {output_path.name}")
    plt.close()

def main():
    print("="*80)
    print("RENDERING LOGOS PAPERS VISUALIZATIONS")
    print("="*80)
    
    # Ensure output directories exist
    P2_DIR.mkdir(parents=True, exist_ok=True)
    P5_DIR.mkdir(parents=True, exist_ok=True)
    
    # Render visualizations
    render_paper2_trinity_triangulation()
    render_paper5_soul_field_potential()
    
    print("\n" + "="*80)
    print("✓ RENDERING COMPLETE!")
    print("="*80)
    print(f"\nOutput locations:")
    print(f"  Paper 2: {P2_DIR}")
    print(f"  Paper 5: {P5_DIR}")

if __name__ == "__main__":
    main()

