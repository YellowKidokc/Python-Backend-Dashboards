#!/usr/bin/env python3
"""Fix Decoherence viz - move observer sphere further right"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

OUTPUT_DIR = Path(r"D:\THEOPHYSICS_MASTER\Assets\Images\logos papers\P2_Quantum_Bridge")

DARK_BG = '#0a0a0a'
CYAN_OBSERVER = '#00FFFF'
PURPLE_FIELD = '#9933FF'
GREEN_ACTUAL = '#00FF00'
WHITE_SOURCE = '#FFFFFF'

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

# Stage 2: Decoherence
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

# Stage 3: Observer MOVED FROM 10 to 15 (further right)
create_sphere(15, 0, 8, 1.5, CYAN_OBSERVER, 0.9)
ax.text(15, 0, 11, 'Observer Selects', color=CYAN_OBSERVER, ha='center', fontsize=24, weight='bold')

plot_glowing_line(x_b, y_b, z_b, GREEN_ACTUAL, GREEN_ACTUAL, 5, 15, 1.0)
ax.text(15, 0, 0, '3. Collapse → Actualized', color=GREEN_ACTUAL, ha='center', fontsize=24, weight='bold')

fig.text(0.5, 0.95, 'Paper 2: Decoherence vs. Collapse',
         ha='center', fontsize=60, color='white', weight='bold')
fig.text(0.5, 0.90, 'The 3-Stage Process of Actualization',
         ha='center', fontsize=24, color=PURPLE_FIELD, style='italic')
fig.text(0.5, 0.05, 'Decoherence creates the "menu" of possibilities; Conscious collapse selects one to become real.',
         ha='center', fontsize=20, color='gray', style='italic')

ax.view_init(elev=20, azim=-75)
ax.set_xlim([-15, 19])  # Extended right
ax.set_ylim([-8, 8])
ax.set_zlim([-5, 12])

plt.savefig(OUTPUT_DIR / 'P02-Decoherence-Collapse-FIXED.png',
            dpi=300, facecolor=DARK_BG, bbox_inches='tight')
print("✓ Fixed: Observer moved from X=10 to X=15 (further right)")
print("✓ Saved: P02-Decoherence-Collapse-FIXED.png")
plt.close()

