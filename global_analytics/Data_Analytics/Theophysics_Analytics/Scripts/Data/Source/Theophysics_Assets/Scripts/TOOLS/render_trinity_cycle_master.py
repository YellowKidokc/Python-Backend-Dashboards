#!/usr/bin/env python3
"""
The Trinity-Wave Collapse Cycle - MASTER DIAGRAM
The complete mechanism showing Father → Son → Spirit actualization
100% Standard with rich spheres, glowing effects, and mechanism-first approach
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

# Output
OUTPUT_DIR = Path(r"D:\THEOPHYSICS_MASTER\Assets\Images\logos papers\P2_Quantum_Bridge")

# --- 1. Setup (TVE Standard) ---
DARK_BG = '#0a0a0a'
GOLD_LOGOS = '#FFD700'    # Father (Source)
SON_INTERNAL = '#FF00FF'  # Son (Structure)
CYAN_OBSERVER = '#00FFFF' # Spirit (Actualizer)
GREEN_ACTUAL = '#00FF00'  # The Collapsed "Now"
WHITE_SOURCE = '#FFFFFF'

fig = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
ax = fig.add_subplot(111, projection='3d', facecolor=DARK_BG)
ax.set_axis_off()

# Helper function to create a 3D sphere surface with glow
def create_sphere_with_glow(x_center, y_center, z_center, radius, core_color, glow_color, core_alpha, label_text=None, text_offset=0):
    theta = np.linspace(0, 2 * np.pi, 60)
    phi = np.linspace(0, np.pi, 60)
    THETA, PHI = np.meshgrid(theta, phi)

    # Core sphere
    x_core = radius * np.sin(PHI) * np.cos(THETA) + x_center
    y_core = radius * np.sin(PHI) * np.sin(THETA) + y_center
    z_core = radius * np.cos(PHI) + z_center
    ax.plot_surface(x_core, y_core, z_core, color=core_color, alpha=core_alpha, 
                    rstride=1, cstride=1, linewidth=0, antialiased=True)
    
    # Glow layers
    for r_glow_mult in [1.2, 1.5, 1.8]:
        r_glow = radius * r_glow_mult
        x_glow = r_glow * np.sin(PHI) * np.cos(THETA) + x_center
        y_glow = r_glow * np.sin(PHI) * np.sin(THETA) + y_center
        z_glow = r_glow * np.cos(PHI) + z_center
        ax.plot_surface(x_glow, y_glow, z_glow, color=glow_color, alpha=0.08 / r_glow_mult, 
                        rstride=1, cstride=1, linewidth=0, antialiased=True)

    if label_text:
        ax.text(x_center, y_center, z_center + radius + text_offset, label_text, 
                color=WHITE_SOURCE, ha='center', fontsize=20, weight='bold')

# Helper function for glowing lines
def plot_glowing_line(x_data, y_data, z_data, core_color, glow_color, core_linewidth, glow_linewidth, alpha):
    ax.plot(x_data, y_data, z_data, color=glow_color, linewidth=glow_linewidth, alpha=alpha/2)
    ax.plot(x_data, y_data, z_data, color=core_color, linewidth=core_linewidth, alpha=alpha)

# --- 2. The Geometry (Mechanism-First) ---

# --- Component 1: FATHER (The Source) ---
# "Yellow stars radiating outward on beams"
create_sphere_with_glow(0, 0, 15, 2.5, GOLD_LOGOS, GOLD_LOGOS, 0.9)
ax.text(0, 0, 19, '1. FATHER: Infinite Possibility Generator |ψ⟩', 
        color=GOLD_LOGOS, ha='center', fontsize=24, weight='bold')

# Radiating beams of possibility
num_beams = 10
for i in range(num_beams):
    angle = (2 * np.pi / num_beams) * i
    x_end = 8 * np.cos(angle)
    y_end = 8 * np.sin(angle)
    z_end = 5 # Pointing down towards the Son's level
    plot_glowing_line([0, x_end], [0, y_end], [15, z_end], 
                      GOLD_LOGOS, GOLD_LOGOS, 1, 6, 0.4)
    # Add "stars" (possibilities) along the beams
    ax.scatter(x_end, y_end, z_end, s=100, c=GOLD_LOGOS, marker='*', alpha=0.8)

# --- Component 2: SON (The Structurer) ---
# "Magenta helix... ordered spiral through time"
ax.text(0, 0, -1, '2. SON: Temporal Coherence Structurer |a⟩', 
        color=SON_INTERNAL, ha='center', fontsize=24, weight='bold')

# Create the Magenta Helix
t_helix = np.linspace(5, -8, 100) # Flowing downwards
x_helix = 6 * np.cos(t_helix * 1.5)
y_helix = 6 * np.sin(t_helix * 1.5)
z_helix = t_helix
plot_glowing_line(x_helix, y_helix, z_helix, 
                  SON_INTERNAL, SON_INTERNAL, 4, 12, 0.9)

# --- Component 3: SPIRIT (The Actualizer) ---
# "Cyan clouds collapsing to white stars"
ax.text(0, 0, -14, '3. SPIRIT: Temporal Actualizer P(a)', 
        color=CYAN_OBSERVER, ha='center', fontsize=24, weight='bold')

# The "Pre-Collapse Cloud" (Cyan)
# The helix aims at z=-8, so the cloud is centered there
np.random.seed(42)
x_cloud = np.random.normal(0, 2, 500)
y_cloud = np.random.normal(0, 2, 500)
z_cloud = np.random.normal(-9, 1, 500) # Centered at the end of the helix
ax.scatter(x_cloud, y_cloud, z_cloud, c=CYAN_OBSERVER, s=60, alpha=0.1, 
           label="Pre-Collapse 'Now' (Cyan Cloud)")

# The "Actualized Now" (Green Star/Sphere)
# This is the "white star" (using GREEN_ACTUAL for semantic color)
create_sphere_with_glow(0, 0, -10, 1.5, GREEN_ACTUAL, GREEN_ACTUAL, 0.9)
ax.text(0, 0, -10, 'NOW', color=WHITE_SOURCE, ha='center', 
        va='center', fontsize=20, weight='bold')

# --- 4. Titles and Labels (Using fig.text) ---
fig.text(0.5, 0.95, 'The Trinity-Wave Collapse Cycle',
         ha='center', fontsize=60, color='white', weight='bold')
fig.text(0.5, 0.90, 'The Complete Mechanism of Actualization (Section 4.4)',
         ha='center', fontsize=24, color=WHITE_SOURCE, style='italic')

# --- BOTTOM TAGLINE ---
fig.text(0.5, 0.05, 'Father generates possibility, Son structures coherence, Spirit actualizes reality. [CYCLE REPEATS]',
         ha='center', fontsize=20, color='gray', style='italic')

# --- 5. Camera and Export ---
ax.view_init(elev=20, azim=20)

ax.set_xlim([-12, 12])
ax.set_ylim([-12, 12])
ax.set_zlim([-18, 22])

plt.savefig(OUTPUT_DIR / 'P02-TRINITY-CYCLE-MASTER.png',
            dpi=300, facecolor=DARK_BG, bbox_inches='tight')
print("✓ Rendered: P02-TRINITY-CYCLE-MASTER.png")
print("\nThis is THE master diagram - the complete mechanism!")
plt.close()

