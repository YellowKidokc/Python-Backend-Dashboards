#!/usr/bin/env python3
"""
Trinity Triangulation - 100% Standard
Rich, glowing, mechanism-first visualization
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

# Output
OUTPUT_DIR = Path(r"D:\THEOPHYSICS_MASTER\Assets\Images\logos papers\P2_Quantum_Bridge")

# --- 1. Setup (TVE Standard) ---
DARK_BG = '#0a0a0a'
CYAN_OBSERVER = '#00FFFF'
GOLD_LOGOS = '#FFD700'
SON_INTERNAL = '#FF00FF'
SPIRIT_IMMANENT = '#00FF00'
WHITE_SOURCE = '#FFFFFF'

fig = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
ax = fig.add_subplot(111, projection='3d', facecolor=DARK_BG)
ax.set_axis_off()

# --- 2. The Geometry (Rich & Glowing) ---

# Helper function to create a 3D sphere surface
def create_sphere(center, radius, color, alpha, glow=False):
    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)
    
    x = center[0] + radius * np.sin(phi) * np.cos(theta)
    y = center[1] + radius * np.sin(phi) * np.sin(theta)
    z = center[2] + radius * np.cos(phi)
    
    if glow:
        # Glow effect: no edges, high transparency
        ax.plot_surface(x, y, z, color=color, alpha=alpha, 
                        rstride=1, cstride=1, linewidth=0, antialiased=True)
    else:
        # Solid object: less transparent, with wireframe for definition
        ax.plot_surface(x, y, z, color=color, alpha=alpha, 
                        rstride=5, cstride=5, linewidth=0.5, 
                        edgecolor=WHITE_SOURCE, antialiased=True)

# --- The Central Quantum State (with Halo) ---
# Halo layers (multiple transparent spheres)
create_sphere((0, 0, 0), 1.0, CYAN_OBSERVER, 0.05, glow=True)
create_sphere((0, 0, 0), 1.2, CYAN_OBSERVER, 0.05, glow=True)
create_sphere((0, 0, 0), 1.4, CYAN_OBSERVER, 0.03, glow=True)
# Solid Core
create_sphere((0, 0, 0), 0.8, CYAN_OBSERVER, 0.7)
ax.text(0, 0, 1.8, 'Quantum State\n(Potentiality)', color=CYAN_OBSERVER, 
        ha='center', fontsize=18, weight='bold')

# --- The Three Observers (Solid Spheres) ---
obs_dist = 5

# Father
create_sphere((obs_dist, 0, 0), 0.5, GOLD_LOGOS, 0.8)
ax.text(obs_dist, 0, 0.8, 'Father\n(External)', color=GOLD_LOGOS, 
        ha='center', fontsize=18, weight='bold')

# Son
create_sphere((0, obs_dist, 0), 0.5, SON_INTERNAL, 0.8)
ax.text(0, obs_dist, 0.8, 'Son\n(Internal)', color=SON_INTERNAL, 
        ha='center', fontsize=18, weight='bold')

# Spirit
create_sphere((0, 0, obs_dist), 0.5, SPIRIT_IMMANENT, 0.8)
ax.text(0, 0, obs_dist+0.8, 'Spirit\n(Immanent)', color=SPIRIT_IMMANENT, 
        ha='center', fontsize=18, weight='bold')

# --- The Triangulation Lines (with "Glow") ---
# Glow (thick, transparent)
ax.plot([0, obs_dist], [0, 0], [0, 0], 'w-', linewidth=5, alpha=0.1)
ax.plot([0, 0], [0, obs_dist], [0, 0], 'w-', linewidth=5, alpha=0.1)
ax.plot([0, 0], [0, 0], [0, obs_dist], 'w-', linewidth=5, alpha=0.1)
# Core (thin, bright)
ax.plot([0, obs_dist], [0, 0], [0, 0], 'w--', linewidth=2, alpha=0.7)
ax.plot([0, 0], [0, obs_dist], [0, 0], 'w--', linewidth=2, alpha=0.7)
ax.plot([0, 0], [0, 0], [0, obs_dist], 'w--', linewidth=2, alpha=0.7)

# --- 3. Titles and Labels (Using fig.text) ---
fig.text(0.5, 0.95, 'Paper 2: Trinity Triangulation (Proof 8)',
         ha='center', fontsize=60, color='white', weight='bold')
fig.text(0.5, 0.90, 'Three Observers Collapse Uncertainty to Zero',
         ha='center', fontsize=24, color=CYAN_OBSERVER, style='italic')

# --- THE NEW BOTTOM TAGLINE ---
fig.text(0.5, 0.05, 'Three perspectives are required for one perfect, actualized reality.',
         ha='center', fontsize=20, color='gray', style='italic')

# --- 4. Camera and Export ---
ax.view_init(elev=20, azim=30)

# Set limits to keep the "floating" feeling consistent
ax.set_xlim([-4, 6])
ax.set_ylim([-4, 6])
ax.set_zlim([-4, 6])

plt.savefig(OUTPUT_DIR / 'P02-TRINITY-100PERCENT-TEST.png',
            dpi=300, facecolor=DARK_BG, bbox_inches='tight')
print("✓ Rendered: P02-TRINITY-100PERCENT-TEST.png")
plt.close()

