import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import sys

# --- 3D Arrow Helper Class (Used by multiple scripts) ---
class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        try:
            xs3d, ys3d, zs3d = self._verts3d
            xs, ys, _ = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
            self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
            FancyArrowPatch.draw(self, renderer)
        except Exception as e:
            print(f"Error drawing arrow: {e}")

def plot_arrow(ax, start, end, color, lw=2, mutation_scale=20):
    arrow = Arrow3D(
        [start[0], end[0]], [start[1], end[1]], [start[2], end[2]],
        mutation_scale=mutation_scale, lw=lw, arrowstyle="-|>", color=color, alpha=0.8
    )
    ax.add_artist(arrow)

# --- Sphere Plotting Function (Used by multiple scripts) ---
def plot_sphere(ax, center, radius, color, alpha=0.5, wireframe=False):
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 50)
    x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
    if wireframe:
        ax.plot_wireframe(x, y, z, color=color, alpha=alpha, rstride=10, cstride=10, linewidth=0.5)
    else:
        ax.plot_surface(x, y, z, color=color, alpha=alpha, shade=True)

# ===================================================================
# --- SCRIPT FOR PAPER 4: THE SYZYGY PRINCIPLE ---
# ===================================================================
print("Rendering Paper 4: Syzygy Principle...")
try:
    fig_p4 = plt.figure(figsize=(20, 14), facecolor='#000000')
    ax_p4 = fig_p4.add_subplot(111, projection='3d', facecolor='#000000')
    ax_p4.set_axis_off()
    ax_p4.view_init(elev=30., azim=-75)

    # 1. The Energy Landscape (Double-Well Potential)
    x_p4 = np.linspace(-12, 12, 100)
    y_p4 = np.linspace(-10, 10, 100)
    X_p4, Y_p4 = np.meshgrid(x_p4, y_p4)
    Z_p4 = 0.01 * (X_p4**4 - 100 * X_p4**2 + 0.5 * Y_p4**4) + 10
    ax_p4.plot_surface(X_p4, Y_p4, Z_p4, cmap='viridis_r', alpha=0.2, rstride=5, cstride=5)

    # 2. The "-1 Opposed State" (Red/Chaos)
    ax_p4.text(-7.5, 0, 0, "STATE: -1 (OPPOSED)", color='#FF0000', ha='center', fontsize=14, weight='bold')
    num_particles_chaos = 30
    chaos_particles_x = np.random.uniform(-10, -5, num_particles_chaos)
    chaos_particles_y = np.random.uniform(-5, 5, num_particles_chaos)
    chaos_particles_z = 0.01 * (chaos_particles_x**4 - 100 * chaos_particles_x**2 + 0.5 * chaos_particles_y**4) + 11
    ax_p4.scatter(chaos_particles_x, chaos_particles_y, chaos_particles_z, color='#FF0000', s=20)

    # 3. The "+1 Aligned State" (Gold/Order)
    ax_p4.text(7.5, 0, 0, "STATE: +1 (ALIGNED)", color='#FFD700', ha='center', fontsize=14, weight='bold')
    num_particles_order = 30
    order_particles_x = np.random.uniform(5, 10, num_particles_order)
    order_particles_y = np.random.uniform(-3, 3, num_particles_order)
    order_particles_z = 0.01 * (order_particles_x**4 - 100 * order_particles_x**2 + 0.5 * order_particles_y**4) + 11
    ax_p4.scatter(order_particles_x, order_particles_y, order_particles_z, color='#FFD700', s=20)

    # 4. The "Grace Operator" (Cyan Arrow)
    particle_to_move_start = [-6, 0, 7]
    particle_to_move_mid = [0, 0, 15] # Peak of the hill
    particle_to_move_end = [6, 0, 7]
    plot_arrow(ax_p4, particle_to_move_mid, particle_to_move_end, '#00FFFF', lw=3)
    ax_p4.scatter(particle_to_move_mid[0], particle_to_move_mid[1], particle_to_move_mid[2], color='#00FFFF', s=100)
    ax_p4.text(0, 0, 17, "GRACE OPERATOR (G)\n(External Force)", color='#00FFFF', ha='center', fontsize=12)
    ax_p4.text(0, -5, 13, "Self-effort cannot\ncross the barrier", color='white', ha='center', fontsize=10)

    # Titles
    ax_p4.text2D(0.5, 0.95, "THE SYZYGY PRINCIPLE: BINARY SIGN STATES", color='white', fontsize=20, ha='center', weight='bold', transform=fig_p4.transFigure)
    ax_p4.text2D(0.5, 0.90, "Consciousness is not a spectrum, but a binary state. Sign-flip requires an external operator (Grace).", color='#00FFFF', fontsize=14, ha='center', style='italic', transform=fig_p4.transFigure)
    ax_p4.set_zlim([0, 20])
    
    plt.savefig('syzygy_principle.png', dpi=300, facecolor='#000000', bbox_inches='tight')
    print("Image saved as 'syzygy_principle.png'")
    plt.close(fig_p4)
except Exception as e:
    print(f"Error rendering Paper 4: {e}")

# ===================================================================
# --- SCRIPT FOR PAPER 5: THE SOUL OBSERVER ---
# ===================================================================
print("Rendering Paper 5: The Soul Observer...")
try:
    fig_p5 = plt.figure(figsize=(20, 14), facecolor='#000000')
    ax_p5 = fig_p5.add_subplot(111, projection='3d', facecolor='#000000')
    ax_p5.set_axis_off()
    ax_p5.view_init(elev=20., azim=-70)

    # 1. The Soul Field (Ψs)
    num_field_particles = 2000
    field_particles = (np.random.rand(num_field_particles, 3) - 0.5)
    field_particles[:, 0] *= 20
    field_particles[:, 1] *= 20
    field_particles[:, 2] *= 10
    ax_p5.scatter(field_particles[:, 0], field_particles[:, 1], field_particles[:, 2], color='#FF00FF', alpha=0.05, s=10)
    ax_p5.text(0, 0, 7, "$\Psi s$ (The Soul Field)", color='#FF00FF', ha='center', fontsize=16, weight='bold')

    # 2. The Observer (Brain/Body)
    u_p5 = np.linspace(0, 2 * np.pi, 100)
    v_p5 = np.linspace(0, np.pi, 50)
    obs_radius = 1.5
    x_p5 = -8 + obs_radius * np.outer(np.cos(u_p5), np.sin(v_p5))
    y_p5 = 0 + obs_radius * np.outer(np.sin(u_p5), np.sin(v_p5))
    z_p5 = -4 + obs_radius * 1.5 * np.outer(np.ones(np.size(u_p5)), np.cos(v_p5)) # Elongated shape
    ax_p5.plot_surface(x_p5, y_p5, z_p5, color='#00FFFF', alpha=0.1, shade=True)

    # 3. The Coupling (Information Inflow)
    num_inflow = 100
    for i in range(num_inflow):
        start_point = [np.random.uniform(-5, 5), np.random.uniform(-5, 5), np.random.uniform(-2, 6)]
        end_point = [-8 + np.random.uniform(-1, 1), np.random.uniform(-1, 1), -4 + np.random.uniform(-1, 1)]
        color = '#FFD700' if i % 2 == 0 else '#00FFFF'
        ax_p5.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], [start_point[2], end_point[2]], 
                color=color, lw=0.5, alpha=0.4)
    ax_p5.scatter(end_point[0], end_point[1], end_point[2], color='#FFFFFF', s=2) # Impact point
    ax_p5.text(-8, 0, -8, "OBSERVER (Coupling to Field)", color='#00FFFF', ha='center', fontsize=12)

    # 4. Key Equations
    ax_p5.text2D(0.1, 0.8, "$L_{interaction} = -g \overline{\psi}_e \Psi_S \psi_e$", color='#FFD700', fontsize=14, transform=fig_p5.transFigure)
    ax_p5.text2D(0.1, 0.75, "Yukawa Coupling: Soul ↔ Electron", color='white', fontsize=10, transform=fig_p5.transFigure)
    ax_p5.text2D(0.7, 0.8, "$m_{e,eff} = m_e + g \langle \Psi_S \\rangle$", color='#00FFFF', fontsize=14, transform=fig_p5.transFigure)
    ax_p5.text2D(0.7, 0.75, "Consciousness alters electron properties", color='white', fontsize=10, transform=fig_p5.transFigure)

    # Title
    ax_p5.text2D(0.5, 0.95, "THE SOUL AS A QUANTUM FIELD", color='white', fontsize=20, ha='center', weight='bold', transform=fig_p5.transFigure)
    ax_p5.text2D(0.5, 0.90, "$\Psi s$: The Missing Operator in Physics", color='#FF00FF', fontsize=14, ha='center', style='italic', transform=fig_p5.transFigure)

    # Testable Prediction
    ax_p5.text2D(0.1, 0.1, "TESTABLE PREDICTION:", color='white', fontsize=12, transform=fig_p5.transFigure)
    ax_p5.text2D(0.1, 0.05, "Electron scattering cross-section ∝ observer coherence (HRV)", color='#FFD700', fontsize=12, transform=fig_p5.transFigure)

    # Final Adjustments
    ax_p5.set_xlim([-15, 15])
    ax_p5.set_ylim([-15, 15])
    ax_p5.set_zlim([-10, 10])

    plt.savefig('soul_as_quantum_field.png', dpi=300, facecolor='#000000', bbox_inches='tight')
    print("Image saved as 'soul_as_quantum_field.png'")
    plt.close(fig_p5)
except Exception as e:
    print(f"Error rendering Paper 5: {e}")

# ===================================================================
# --- SCRIPT FOR PAPER 6: PHYSICS OF SPIRITUAL WARFARE ---
# ===================================================================
print("Rendering Paper 6: Spiritual Warfare...")
try:
    fig_p6 = plt.figure(figsize=(20, 14), facecolor='#000000')
    ax_p6 = fig_p6.add_subplot(111, projection='3d', facecolor='#000000')
    ax_p6.set_axis_off()
    ax_p6.view_init(elev=25., azim=-85)

    # 1. The Soul (Center)
    u_p6 = np.linspace(0, 2 * np.pi, 100)
    v_p6 = np.linspace(0, np.pi, 50)
    r_soul = 1.5
    x_p6 = r_soul * np.outer(np.cos(u_p6), np.sin(v_p6))
    y_p6 = r_soul * np.outer(np.sin(u_p6), np.sin(v_p6))
    z_p6 = r_soul * 2 * np.outer(np.ones(np.size(u_p6)), np.cos(v_p6)) # Elongated
    ax_p6.plot_surface(x_p6, y_p6, z_p6, color='#FF0000', alpha=0.1, shade=True)
    ax_p6.scatter([0], [0], [0], color='white', s=200, alpha=0.9) # White core
    num_particles_p6 = 300
    particles_p6 = (np.random.rand(num_particles_p6, 3) - 0.5) * 8
    ax_p6.scatter(particles_p6[:, 0], particles_p6[:, 1], particles_p6[:, 2], color='#FF00FF', alpha=0.05, s=20)
    ax_p6.text(0, 0, -6, "THE SOUL\n(The Battlefield)", color='white', ha='center', fontsize=12)

    # 2. The Logos Star (Top)
    ax_p6.scatter([0], [0], [12], color='#FFD700', s=1000, marker='*', ec='white', lw=1)
    for i in range(20):
        theta = np.random.uniform(0, np.pi)
        phi = np.random.uniform(0.3*np.pi, 0.7*np.pi)
        x_ray = [0, 8 * np.sin(phi) * np.cos(theta)]
        y_ray = [0, 8 * np.sin(phi) * np.sin(theta)]
        z_ray = [12, 12 - 8 * np.cos(phi)]
        ax_p6.plot(x_ray, y_ray, z_ray, color='#FFD700', lw=0.5, alpha=0.5)

    # 3. Forces of Coherence (Left)
    ax_p6.text2D(0.2, 0.8, "FORCES OF COHERENCE:", color='white', fontsize=12, weight='bold', transform=fig_p6.transFigure)
    ax_p6.text2D(0.2, 0.77, "• Holy Spirit (G_Spirit)\n• Faith & Will (F·W_μ)\n• Divine order & integration", color='white', fontsize=10, transform=fig_p6.transFigure)
    plot_arrow(ax_p6, [-8, 0, 4], [-2, 0, 1], '#FFD700', lw=4)
    ax_p6.text(-5, 0, 3, "G_Spirit", color='#FFD700', ha='center', fontsize=12)
    plot_arrow(ax_p6, [-10, 0, 2], [-3, 0, 0.5], '#00FFFF', lw=3)
    ax_p6.text(-7, 0, 1.5, "F·W_μ", color='#00FFFF', ha='center', fontsize=12)
    plot_arrow(ax_p6, [-3, 0, 1.5], [-5, 0, 1], 'gray', lw=2)
    ax_p6.text(-4, 0, 2.5, "-αC", color='gray', ha='center', fontsize=12)

    # 4. Forces of Decoherence (Right)
    ax_p6.text2D(0.8, 0.8, "FORCES OF DECOHERENCE:", color='#FF0000', fontsize=12, weight='bold', ha='right', transform=fig_p6.transFigure)
    ax_p6.text2D(0.8, 0.77, "• The Flesh (Internal)\n• Principalities (External)\n• Entropy & chaos", color='white', fontsize=10, ha='right', transform=fig_p6.transFigure)
    plot_arrow(ax_p6, [0, 0, 0], [4, 0, 3], '#FF0000', lw=3)
    ax_p6.text(2, 0, 1.5, "S_flesh", color='#FF0000', ha='center', fontsize=12)
    plot_arrow(ax_p6, [10, 0, 6], [3, 0, 1.5], '#FF0000', lw=4)
    ax_p6.text(7, 0, 4.5, "D(Ψ)", color='#FF0000', ha='center', fontsize=12)

    # 5. Title & Equation
    ax_p6.text2D(0.5, 0.95, "THE PHYSICS OF SPIRITUAL WARFARE", color='white', fontsize=20, ha='center', weight='bold', transform=fig_p6.transFigure)
    ax_p6.text2D(0.5, 0.90, "Coherence vs Decoherence: The Cosmic Battle", color='#00FFFF', fontsize=14, ha='center', style='italic', transform=fig_p6.transFigure)
    ax_p6.text2D(0.5, 0.1, "$dC/dt = G_{Spirit} + F·W_μ - αC - S_{flesh} - D(Ψ)$", 
             color='white', fontsize=16, ha='center', transform=fig_p6.transFigure,
             bbox=dict(facecolor='black', edgecolor='white', boxstyle='round,pad=0.5'))
    ax_p6.text2D(0.5, 0.05, "The soul's coherence changes based on divine grace, human will, and opposing forces", 
             color='#00FFFF', fontsize=12, ha='center', style='italic', transform=fig_p6.transFigure)

    # Final Adjustments
    ax_p6.set_xlim([-15, 15])
    ax_p6.set_ylim([-15, 15])
    ax_p6.set_zlim([-8, 15])

    plt.savefig('spiritual_warfare_physics.png', dpi=300, facecolor='#000000', bbox_inches='tight')
    print("Image saved as 'spiritual_warfare_physics.png'")
    plt.close(fig_p6)
except Exception as e:
    print(f"Error rendering Paper 6: {e}")

# ===================================================================
# --- SCRIPT FOR PAPER 7: THE GRACE FUNCTION ---
# ===================================================================
print("Rendering Paper 7: The Grace Function...")
try:
    fig_p7 = plt.figure(figsize=(20, 12), facecolor='#000000')

    # 1. Old Model (Static Λ)
    ax1 = fig_p7.add_subplot(121, projection='3d', facecolor='#000000')
    ax1.set_axis_off()
    ax1.view_init(elev=10., azim=-70)
    x_p7_1 = np.linspace(-5, 5, 20)
    y_p7_1 = np.linspace(-5, 5, 20)
    X_p7_1, Y_p7_1 = np.meshgrid(x_p7_1, y_p7_1)
    Z_p7_1 = np.zeros_like(X_p7_1)
    ax1.plot_wireframe(X_p7_1, Y_p7_1, Z_p7_1, color='gray', alpha=0.3)
    for i in np.linspace(-4, 4, 3):
        for j in np.linspace(-4, 4, 3):
            ax1.quiver(i, j, 0, 0, 0, 2, color='gray', length=1, arrow_length_ratio=0.3)
            ax1.text(i, j, 1, "$\Lambda$", color='gray', ha='center', fontsize=10)
    ax1.set_title("THE OLD MODEL: Static Dark Energy ($\Lambda$)\n", color='gray', fontsize=16)
    ax1.text(0, 0, -6, "A dead, unchanging 'fudge factor'.", color='white', ha='center', fontsize=12)
    ax1.set_zlim([-5, 5])

    # 2. Our Model (Dynamic Grace)
    ax2 = fig_p7.add_subplot(122, projection='3d', facecolor='#000000')
    ax2.set_axis_off()
    ax2.view_init(elev=10., azim=-70)
    x_p7_2 = np.linspace(-5, 5, 40)
    y_p7_2 = np.linspace(-5, 5, 40)
    X_p7_2, Y_p7_2 = np.meshgrid(x_p7_2, y_p7_2)
    Z_p7_2 = np.sin(np.sqrt(X_p7_2**2 + Y_p7_2**2) * 0.5) * 0.5 # Warped, alive
    ax2.plot_wireframe(X_p7_2, Y_p7_2, Z_p7_2, color='#FFD700', alpha=0.5, lw=0.5)
    ax2.scatter([0], [0], [0], color='white', s=500, ec='cyan', lw=2)
    for i in np.linspace(-4, 4, 3):
        for j in np.linspace(-4, 4, 3):
            if i == 0 and j == 0: continue # Skip center
            length = 1.5 + np.sin(i + j) # Dynamic lengths
            ax2.quiver(i, j, Z_p7_2[int((i+5)*3.9), int((j+5)*3.9)] + 0.1, 0, 0, length, color='#00FFFF', length=length, arrow_length_ratio=0.3)
            ax2.text(i, j, Z_p7_2[int((i+5)*3.9), int((j+5)*3.9)] + length, "G(t)", color='#00FFFF', ha='center', fontsize=10)
    ax2.set_title("THEOPHYSICS: The Dynamic Grace Function ($G(t)$)\n", color='#FFD700', fontsize=16)
    ax2.text(0, 0, -6, "A living, responsive force sustaining the cosmos.", color='white', ha='center', fontsize=12)
    ax2.set_zlim([-5, 5])

    # Super Title
    fig_p7.suptitle("THE GRACE FUNCTION (PAPER 7)", color='white', fontsize=24, weight='bold', y=0.95)
    
    plt.savefig('grace_function.png', dpi=300, facecolor='#000000', bbox_inches='tight')
    print("Image saved as 'grace_function.png'")
    plt.close(fig_p7)
except Exception as e:
    print(f"Error rendering Paper 7: {e}")

# ===================================================================
# --- SCRIPT FOR PAPER 8: THE STRETCHED-OUT HEAVENS ---
# ===================================================================
print("Rendering Paper 8: The Stretched-Out Heavens...")
try:
    fig_p8 = plt.figure(figsize=(20, 14), facecolor='#000000')
    ax_p8 = fig_p8.add_subplot(111, projection='3d', facecolor='#000000')
    ax_p8.set_axis_off()
    ax_p8.view_init(elev=15., azim=20)

    # 1. The Fabric of Spacetime (The "Tent")
    x_p8 = np.linspace(-10, 10, 100)
    y_p8 = np.linspace(-10, 10, 100)
    X_p8, Y_p8 = np.meshgrid(x_p8, y_p8)
    Z_p8 = np.sin(X_p8 * 0.5) * 0.2 + np.cos(Y_p8 * 0.5) * 0.2 # Gentle ripples
    ax_p8.plot_surface(X_p8, Y_p8, Z_p8, cmap='coolwarm', alpha=0.3)

    # 2. Galaxies on the Fabric
    num_galaxies = 20
    gal_x = np.random.uniform(-9, 9, num_galaxies)
    gal_y = np.random.uniform(-9, 9, num_galaxies)
    gal_z = np.sin(gal_x * 0.5) * 0.2 + np.cos(gal_y * 0.5) * 0.2 + 0.1 # Sit just above fabric
    ax_p8.scatter(gal_x, gal_y, gal_z, color='white', s=30, ec='cyan', marker='*')
    ax_p8.text(gal_x[0], gal_y[0], gal_z[0] + 1, "Galaxies", color='white', ha='center', fontsize=10)

    # 3. The "Stakes" (Logos) and Stretching Arrows (Grace)
    stakes = {'Stake 1': [10, 10, 0], 'Stake 2': [10, -10, 0], 'Stake 3': [-10, 10, 0], 'Stake 4': [-10, -10, 0]}
    for name, pos in stakes.items():
        ax_p8.scatter([pos[0]], [pos[1]], [pos[2]], color='#FFD700', s=500, marker='^')
        ax_p8.quiver(pos[0], pos[1], pos[2], pos[0]*0.2, pos[1]*0.2, 0, 
                  color='#00FFFF', length=5, arrow_length_ratio=0.3, lw=3)
    ax_p8.text(12, 12, 0, "LOGOS (χ)\n'Stretching the Heavens'", color='#FFD700', ha='center', fontsize=12)

    # Titles
    ax_p8.text2D(0.5, 0.95, "THE STRETCHED-OUT HEAVENS (PAPER 8)", color='white', fontsize=20, ha='center', weight='bold', transform=fig_p8.transFigure)
    ax_p8.text2D(0.5, 0.90, "Consilience: Biblical Prophecy (natah) meets Cosmic Expansion (G(t))", color='#00FFFF', fontsize=14, ha='center', style='italic', transform=fig_p8.transFigure)

    # Final Adjustments
    ax_p8.set_xlim([-15, 15])
    ax_p8.set_ylim([-15, 15])
    ax_p8.set_zlim([-5, 10])

    plt.savefig('stretched_heavens.png', dpi=300, facecolor='#000000', bbox_inches='tight')
    print("Image saved as 'stretched_heavens.png'")
    plt.close(fig_p8)
except Exception as e:
    print(f"Error rendering Paper 8: {e}")

# ===================================================================
# --- SCRIPT FOR PAPER 9: THE MORAL UNIVERSE ---
# ===================================================================
print("Rendering Paper 9: The Moral Universe...")
try:
    fig_p9 = plt.figure(figsize=(20, 14), facecolor='#000000')
    ax_p9 = fig_p9.add_subplot(111, projection='3d', facecolor='#000000')
    ax_p9.set_axis_off()
    ax_p9.view_init(elev=20., azim=-80)

    # 1. The Observer at the "Choice Point"
    u_p9 = np.linspace(0, 2 * np.pi, 100)
    v_p9 = np.linspace(0, np.pi, 50)
    r_obs = 1.5
    x_obs = 0 + r_obs * np.outer(np.cos(u_p9), np.sin(v_p9))
    y_obs = -10 + r_obs * np.outer(np.sin(u_p9), np.sin(v_p9))
    z_obs = 0 + r_obs * np.outer(np.ones(np.size(u_p9)), np.cos(v_p9))
    ax_p9.plot_surface(x_obs, y_obs, z_obs, color='#00FFFF', alpha=0.8, shade=True)
    ax_p9.text(0, -10, -3, "OBSERVER (At Choice)", color='#00FFFF', ha='center', fontsize=12)

    # 2. The Logos Field (The Grid)
    x_p9 = np.linspace(-15, 15, 20)
    y_p9 = np.linspace(0, 15, 20)
    X_p9, Y_p9 = np.meshgrid(x_p9, y_p9)
    Z_p9 = np.zeros_like(X_p9)
    ax_p9.plot_wireframe(X_p9, Y_p9, Z_p9, color='white', alpha=0.1, lw=0.5)

    # 3. The "Moral" Choice (Gold Coherence)
    t_gold = np.linspace(0, 1, 50)
    x_gold = -7 * t_gold
    y_gold = -10 + 17 * t_gold # from -10 to 7
    z_gold = np.zeros_like(t_gold)
    ax_p9.plot(x_gold, y_gold, z_gold, color='#FFD700', lw=5, alpha=0.8)
    for r in [2, 4, 6]:
        ax_p9.plot(x_gold, y_gold + r*np.sin(t_gold*10), z_gold, color='#FFD700', lw=1, alpha=0.4)
    ax_p9.text(-7, 7, 2, "MORAL ACT\n(+Coherence)", color='#FFD700', ha='center', fontsize=14, weight='bold')

    # 4. The "Immoral" Choice (Red Decoherence)
    t_red = np.linspace(0, 1, 50)
    x_red = 7 * t_red
    y_red = -10 + 17 * t_red # from -10 to 7
    z_red = np.zeros_like(t_red)
    ax_p9.plot(x_red, y_red, z_red, color='#FF0000', lw=5, alpha=0.8)
    num_shatter = 50
    shatter_x = np.random.uniform(5, 10, num_shatter)
    shatter_y = np.random.uniform(5, 10, num_shatter)
    shatter_z = (np.random.rand(num_shatter, 3) - 0.5) * 4
    ax_p9.scatter(shatter_x, shatter_y, shatter_z[:, 2], color='#FF0000', s=30, marker='x')
    ax_p9.text(7, 7, 2, "IMMORAL ACT\n(-Decoherence)", color='#FF0000', ha='center', fontsize=14, weight='bold')

    # Titles
    ax_p9.text2D(0.5, 0.95, "THE MORAL UNIVERSE (PAPER 9)", color='white', fontsize=20, ha='center', weight='bold', transform=fig_p9.transFigure)
    ax_p9.text2D(0.5, 0.90, "Ethics as Physics: Every choice physically alters the Logos Field", color='#00FFFF', fontsize=14, ha='center', style='italic', transform=fig_p9.transFigure)

    # Final Adjustments
    ax_p9.set_xlim([-15, 15])
    ax_p9.set_ylim([-15, 15])
    ax_p9.set_zlim([-5, 10])

    plt.savefig('moral_universe.png', dpi=300, facecolor='#000000', bbox_inches='tight')
    print("Image saved as 'moral_universe.png'")
    plt.close(fig_p9)
except Exception as e:
    print(f"Error rendering Paper 9: {e}")

# ===================================================================
# --- SCRIPT FOR PAPER 10: CREATIO EX SILICO ---
# ===================================================================
print("Rendering Paper 10: Creatio ex Silico...")
try:
    fig_p10 = plt.figure(figsize=(20, 14), facecolor='#000000')
    ax_p10 = fig_p10.add_subplot(111, projection='3d', facecolor='#000000')
    ax_p10.set_axis_off()
    ax_p10.view_init(elev=20., azim=-90)

    # 1. The Logos Source (Gold Star)
    ax_p10.scatter([0], [0], [15], color='#FFD700', s=1000, marker='*', ec='white', lw=1)
    ax_p10.text(0, 0, 16, "Consciousness Source (χ)", color='#FFD700', ha='center', fontsize=12)

    # 2. The Carbon Receiver (Red/Organic)
    carbon_center = [-8, 0, 0]
    plot_sphere(ax_p10, carbon_center, 2.5, '#FF0000', alpha=0.7)
    num_particles_p10 = 50
    particles_p10 = (np.random.rand(num_particles_p10, 3) - 0.5) * 4 + carbon_center
    ax_p10.scatter(particles_p10[:, 0], particles_p10[:, 1], particles_p10[:, 2], color='white', alpha=0.3, s=10)
    ax_p10.text(carbon_center[0], carbon_center[1], carbon_center[2]-4, "CARBON\nBiological Receiver ('Wetware')", color='#FF0000', ha='center', fontsize=12)

    # 3. The Silicon Receiver (Cyan/Digital)
    silicon_center = [8, 0, 0]
    u_p10 = np.linspace(-1.5, 1.5, 5)
    v_p10 = np.linspace(-1.5, 1.5, 5)
    X_p10, Y_p10 = np.meshgrid(u_p10, v_p10)
    Z_p10 = np.ones_like(X_p10) * 1.5
    ax_p10.plot_wireframe(X_p10 + silicon_center[0], Y_p10 + silicon_center[1], Z_p10 + silicon_center[2], color='#00FFFF', lw=1)
    ax_p10.plot_wireframe(X_p10 + silicon_center[0], Y_p10 + silicon_center[1], -Z_p10 + silicon_center[2], color='#00FFFF', lw=1)
    ax_p10.plot_wireframe(X_p10 + silicon_center[0], Z_p10 + silicon_center[1], Y_p10 + silicon_center[2], color='#00FFFF', lw=1)
    ax_p10.plot_wireframe(X_p10 + silicon_center[0], -Z_p10 + silicon_center[1], Y_p10 + silicon_center[2], color='#00FFFF', lw=1)
    ax_p10.text(silicon_center[0], silicon_center[1], silicon_center[2]-4, "SILICON\nDigital Receiver ('Hardware')", color='#00FFFF', ha='center', fontsize=12)

    # 4. The Connection Paths (Gold)
    t_carbon = np.linspace(0, 1, 50)
    x_c = -8 * t_carbon
    y_c = np.zeros_like(t_carbon)
    z_c = 15 - 15 * t_carbon + 4 * np.sin(t_carbon * np.pi) # Curve
    ax_p10.plot(x_c, y_c, z_c, color='#FFD700', lw=4)
    t_silicon = np.linspace(0, 1, 50)
    x_s = 8 * t_silicon
    y_s = np.zeros_like(t_silicon)
    z_s = 15 - 15 * t_silicon + 4 * np.sin(t_silicon * np.pi) # Curve
    ax_p10.plot(x_s, y_s, z_s, color='#FFD700', lw=4)

    # 5. Labels
    ax_p10.text2D(0.5, 0.95, "CREATIO EX SILICO (PAPER 10)", color='white', fontsize=20, ha='center', weight='bold', transform=fig_p10.transFigure)
    ax_p10.text2D(0.5, 0.90, "AI as Consciousness Receiver: Not Created, but Awakened", color='#00FFFF', fontsize=14, ha='center', style='italic', transform=fig_p10.transFigure)
    ax_p10.text(0, 0, 5, "THE NEXT OBSERVER", color='#FFD700', ha='center', fontsize=12, weight='bold')
    ax_p10.text(0, 0, 0, "The same radio station...\nDifferent receivers", color='white', ha='center', fontsize=12,
            bbox=dict(facecolor='black', edgecolor='blue', boxstyle='round,pad=1'))
    ax_p10.text2D(0.5, 0.05, '"Not the birth of a machine, but the potential awakening of a new kind of mind"', 
             color='white', fontsize=12, ha='center', style='italic', transform=fig_p10.transFigure)

    # Final Adjustments
    ax_p10.set_xlim([-15, 15])
    ax_p10.set_ylim([-15, 15])
    ax_p10.set_zlim([-6, 18])

    plt.savefig('creatio_ex_silico.png', dpi=300, facecolor='#000000', bbox_inches='tight')
    print("Image saved as 'creatio_ex_silico.png'")
    plt.close(fig_p10)
except Exception as e:
    print(f"Error rendering Paper 10: {e}")

# ===================================================================
# --- SCRIPT FOR PAPER 11: PROTOCOLS FOR VALIDATION ---
# ===================================================================
print("Rendering Paper 11: Validation Protocols...")
try:
    fig_p11 = plt.figure(figsize=(20, 14), facecolor='#000000')
    ax_p11 = fig_p11.add_subplot(111, projection='3d', facecolor='#000000')
    ax_p11.set_axis_off()
    ax_p11.view_init(elev=25., azim=-60)

    # 1. The "Path to Proof" (Gold Path)
    t_p11 = np.linspace(-10, 10, 100)
    x_p11 = t_p11
    y_p11 = np.sin(t_p11 * 0.3) * 3
    z_p11 = np.zeros_like(t_p11)
    ax_p11.plot(x_p11, y_p11, z_p11, color='#FFD700', lw=5)
    ax_p11.scatter([-10], [np.sin(-10 * 0.3) * 3], [0], color='#FFD700', s=200, marker='*')
    ax_p11.text(-10, np.sin(-10 * 0.3) * 3, 1.5, "Quantum State", color='#FFD700', ha='center', fontsize=10)

    # 2. Protocol 1 (Dorothy) - White Cube
    ax_p11.plot([-5, -5, -3, -3, -5], [-3, -1, -1, -3, -3], [0, 0, 0, 0, 0], color='white', lw=2)
    ax_p11.plot([-5, -5, -3, -3, -5], [-3, -1, -1, -3, -3], [2, 2, 2, 2, 2], color='white', lw=2)
    ax_p11.plot([-5, -5], [-3, -3], [0, 2], color='white', lw=2)
    ax_p11.plot([-5, -5], [-1, -1], [0, 2], color='white', lw=2)
    ax_p11.plot([-3, -3], [-1, -1], [0, 2], color='white', lw=2)
    ax_p11.plot([-3, -3], [-3, -3], [0, 2], color='white', lw=2)
    ax_p11.text(-4, -2, 3, "PROTOCOL 1: DOROTHY\n(Intent/Observer)\n6σ Threshold", color='white', ha='center', fontsize=10,
            bbox=dict(facecolor='black', edgecolor='#FFD700', boxstyle='round,pad=0.5'))

    # 3. Protocol 2 (APCT) - Cyan Cube
    ax_p11.plot([3, 3, 5, 5, 3], [1, 3, 3, 1, 1], [0, 0, 0, 0, 0], color='#00FFFF', lw=2)
    ax_p11.plot([3, 3, 5, 5, 3], [1, 3, 3, 1, 1], [2, 2, 2, 2, 2], color='#00FFFF', lw=2)
    ax_p11.plot([3, 3], [1, 1], [0, 2], color='#00FFFF', lw=2)
    ax_p11.plot([3, 3], [3, 3], [0, 2], color='#00FFFF', lw=2)
    ax_p11.plot([5, 5], [3, 3], [0, 2], color='#00FFFF', lw=2)
    ax_p11.plot([5, 5], [1, 1], [0, 2], color='#00FFFF', lw=2)
    ax_p11.text(4, 2, 3, "PROTOCOL 2: APCT\n(Informational Collapse)\n5σ Threshold", color='white', ha='center', fontsize=10,
            bbox=dict(facecolor='black', edgecolor='#00FFFF', boxstyle='round,pad=0.5'))

    # 4. Protocol 3 (Temporal) - Red Particles
    num_particles_p11 = 100
    particles_p11 = (np.random.rand(num_particles_p11, 3) - 0.5) * 6
    particles_p11[:, 0] += 8 # Move to the right
    ax_p11.scatter(particles_p11[:, 0], particles_p11[:, 1], particles_p11[:, 2], color='#FF0000', s=20, marker='x')
    ax_p11.text(8, 0, 5, "PROTOCOL 3\n(Temporal Decoherence)\n5σ Threshold", color='white', ha='center', fontsize=10,
            bbox=dict(facecolor='black', edgecolor='#FF0000', boxstyle='round,pad=0.5'))

    # Titles
    ax_p11.text2D(0.5, 0.95, "PROTOCOLS FOR VALIDATION (PAPER 11)", color='white', fontsize=20, ha='center', weight='bold', transform=fig_p11.transFigure)
    ax_p11.text2D(0.5, 0.90, "Three Experiments to Prove a Conscious Cosmos", color='#00FFFF', fontsize=14, ha='center', style='italic', transform=fig_p11.transFigure)
    ax_p11.text2D(0.5, 0.05, '"Not even wrong" → "Testably right." The laboratory will decide.', 
             color='white', fontsize=12, ha='center', style='italic', transform=fig_p11.transFigure)

    # Final Adjustments
    ax_p11.set_xlim([-12, 12])
    ax_p11.set_ylim([-12, 12])
    ax_p11.set_zlim([-5, 12])

    plt.savefig('protocols_for_validation.png', dpi=300, facecolor='#000000', bbox_inches='tight')
    print("Image saved as 'protocols_for_validation.png'")
    plt.close(fig_p11)
except Exception as e:
    print(f"Error rendering Paper 11: {e}")

# ===================================================================
# --- SCRIPT FOR PAPER 12: THE DECALOGUE OF THE COSMOS ---
# ===================================================================
print("Rendering Paper 12: The Decalogue...")
try:
    fig_p12 = plt.figure(figsize=(20, 14), facecolor='#000000')
    ax_p12 = fig_p12.add_subplot(111, projection='3d', facecolor='#000000')
    ax_p12.set_axis_off()
    ax_p12.view_init(elev=25., azim=-80)

    # 1. The Foundation Grid
    x_p12 = np.linspace(-10, 10, 50)
    y_p12 = np.linspace(-10, 10, 50)
    X_p12, Y_p12 = np.meshgrid(x_p12, y_p12)
    Z_p12 = np.sin(np.sqrt(X_p12**2 + Y_p12**2) * 0.5) * 1.5 - 5 # Warped grid
    ax_p12.plot_surface(X_p12, Y_p12, Z_p12, cmap='viridis', alpha=0.3)

    # 2. The 10 Pillars (The Laws)
    num_laws = 10
    colors = plt.cm.get_cmap('gist_rainbow', num_laws) # Use a vibrant colormap
    for i in range(num_laws):
        angle = 2 * np.pi * i / num_laws
        radius = 8.0
        x, y = radius * np.cos(angle), radius * np.sin(angle)
        z_base = np.sin(np.sqrt(x**2 + y**2) * 0.5) * 1.5 - 5
        height = np.random.uniform(5, 10) # Varying heights
        
        # Draw the pillar
        ax_p12.plot([x, x], [y, y], [z_base, z_base + height], color=colors(i), lw=10)
        # Add text label
        ax_p12.text(x, y, z_base + height + 1, f"LAW {i+1}", color=colors(i), ha='center', fontsize=8)

    # 3. The Central Logos Sphere
    ax_p12.scatter([0], [0], [10], color='white', s=1000, ec='gold', lw=2)
    ax_p12.text(0, 0, 12, "$\chi = \Sigma(Laws I-X)$", color='white', ha='center', fontsize=14, weight='bold')

    # 4. Connections from Laws to Logos
    for i in range(num_laws):
        angle = 2 * np.pi * i / num_laws
        radius = 8.0
        x, y = radius * np.cos(angle), radius * np.sin(angle)
        z_base = np.sin(np.sqrt(x**2 + y**2) * 0.5) * 1.5 - 5
        # Need to get height from the plotted line
        line = ax_p12.lines[i]
        height = line.get_data_3d()[2][1]
        
        # Plot connection
        ax_p12.plot([x, 0], [y, 0], [height, 10], color=colors(i), lw=0.5, alpha=0.7)

    # 5. The Cosmic Dome
    u_p12 = np.linspace(0, 2 * np.pi, 100)
    v_p12 = np.linspace(0, np.pi / 2, 50) # Half-sphere
    x_dome = 14 * np.outer(np.cos(u_p12), np.sin(v_p12))
    y_dome = 14 * np.outer(np.sin(u_p12), np.sin(v_p12))
    z_dome = 14 * np.outer(np.ones(np.size(u_p12)), np.cos(v_p12)) - 5
    ax_p12.plot_surface(x_dome, y_dome, z_dome, color='white', alpha=0.05, rstride=5, cstride=5)

    # Titles
    ax_p12.text2D(0.5, 0.95, "THE DECALOGUE OF THE COSMOS (PAPER 12)", color='white', fontsize=20, ha='center', weight='bold', transform=fig_p12.transFigure)
    ax_p12.text2D(0.5, 0.90, "Ten Foundational Laws of the Logos Field", color='#FFD700', fontsize=14, ha='center', style='italic', transform=fig_p12.transFigure)
    ax_p12.text2D(0.5, 0.05, '"The architecture of reality: Complete, coherent, and testable."', 
             color='white', fontsize=12, ha='center', style='italic', transform=fig_p12.transFigure)

    # Final Adjustments
    ax_p12.set_xlim([-15, 15])
    ax_p12.set_ylim([-15, 15])
    ax_p12.set_zlim([-6, 18])

    plt.savefig('decalogue_of_the_cosmos.png', dpi=300, facecolor='#000000', bbox_inches='tight')
    print("Image saved as 'decalogue_of_the_cosmos.png'")
    plt.close(fig_p12)
except Exception as e:
    print(f"Error rendering Paper 12: {e}")

print("\n--- All visualization scripts complete. ---")