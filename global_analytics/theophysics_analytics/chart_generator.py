"""
THEOPHYSICS CHART GENERATOR
===========================
Auto-generates visual charts for analytics dashboards.

Outputs PNG charts that embed directly in markdown dashboards.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
import math

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import Circle, FancyBboxPatch
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("WARNING: matplotlib not installed. Run: pip install matplotlib numpy")


# Theophysics color palette
COLORS = {
    'primary': '#1a237e',      # Deep blue (Logos)
    'secondary': '#b71c1c',    # Deep red (Blood)
    'accent': '#ffd700',       # Gold (Glory)
    'light': '#e8eaf6',        # Light blue
    'dark': '#0d1137',         # Near black
    'success': '#2e7d32',      # Green
    'warning': '#f57c00',      # Orange
    'physics': '#1565c0',
    'theology': '#7b1fa2',
    'mathematics': '#00838f',
    'information': '#558b2f',
    'consciousness': '#d84315',
    'philosophy': '#6a1b9a',
    'grid': '#e0e0e0',
    'text': '#212121'
}


def setup_style():
    """Configure matplotlib style for Theophysics aesthetic."""
    if not HAS_MATPLOTLIB:
        return

    plt.rcParams.update({
        'figure.facecolor': '#fafafa',
        'axes.facecolor': '#ffffff',
        'axes.edgecolor': COLORS['grid'],
        'axes.labelcolor': COLORS['text'],
        'axes.titlecolor': COLORS['primary'],
        'xtick.color': COLORS['text'],
        'ytick.color': COLORS['text'],
        'grid.color': COLORS['grid'],
        'grid.alpha': 0.5,
        'font.family': 'sans-serif',
        'font.size': 10,
        'axes.titlesize': 14,
        'axes.labelsize': 11,
        'figure.titlesize': 16
    })


def generate_coherence_gauge(score: float, output_path: Path, title: str = "Coherence Score"):
    """
    Generate a gauge/meter chart for coherence score.

    Args:
        score: Value 0-100
        output_path: Where to save PNG
        title: Chart title
    """
    if not HAS_MATPLOTLIB:
        return None

    setup_style()
    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={'aspect': 'equal'})

    # Draw gauge background
    theta_start = 180
    theta_end = 0
    theta_range = theta_start - theta_end

    # Background arc (gray)
    bg_theta = np.linspace(np.radians(theta_start), np.radians(theta_end), 100)
    bg_r = 0.8
    ax.plot(bg_r * np.cos(bg_theta), bg_r * np.sin(bg_theta),
            color=COLORS['grid'], linewidth=20, solid_capstyle='round')

    # Score arc (colored based on value)
    if score >= 70:
        color = COLORS['success']
    elif score >= 40:
        color = COLORS['warning']
    else:
        color = COLORS['secondary']

    score_angle = theta_start - (score / 100) * theta_range
    score_theta = np.linspace(np.radians(theta_start), np.radians(score_angle), 50)
    ax.plot(bg_r * np.cos(score_theta), bg_r * np.sin(score_theta),
            color=color, linewidth=20, solid_capstyle='round')

    # Needle
    needle_angle = np.radians(score_angle)
    ax.annotate('', xy=(0.6 * np.cos(needle_angle), 0.6 * np.sin(needle_angle)),
                xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=COLORS['dark'], lw=2))

    # Center circle
    center = Circle((0, 0), 0.1, color=COLORS['dark'], zorder=10)
    ax.add_patch(center)

    # Score text
    ax.text(0, -0.2, f"{score:.0f}", fontsize=36, fontweight='bold',
            ha='center', va='center', color=COLORS['primary'])
    ax.text(0, -0.4, "/ 100", fontsize=14, ha='center', va='center', color=COLORS['text'])

    # Labels
    ax.text(-0.85, 0, "0", fontsize=10, ha='center', color=COLORS['text'])
    ax.text(0.85, 0, "100", fontsize=10, ha='center', color=COLORS['text'])
    ax.text(0, 0.85, "50", fontsize=10, ha='center', color=COLORS['text'])

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.6, 1.2)
    ax.axis('off')
    ax.set_title(title, fontsize=16, fontweight='bold', color=COLORS['primary'], pad=10)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#fafafa')
    plt.close()

    return output_path


def generate_domain_chart(domains: Dict[str, float], output_path: Path, title: str = "Domain Distribution"):
    """
    Generate horizontal bar chart for domain distribution.

    Args:
        domains: Dict of domain -> percentage
        output_path: Where to save PNG
        title: Chart title
    """
    if not HAS_MATPLOTLIB:
        return None

    setup_style()

    # Sort by value
    sorted_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)
    names = [d[0].title() for d in sorted_domains]
    values = [d[1] for d in sorted_domains]

    # Colors for each domain
    domain_colors = [COLORS.get(d[0].lower(), COLORS['primary']) for d in sorted_domains]

    fig, ax = plt.subplots(figsize=(8, 5))

    y_pos = np.arange(len(names))
    bars = ax.barh(y_pos, values, color=domain_colors, edgecolor='white', linewidth=1)

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax.text(val + 1, bar.get_y() + bar.get_height()/2, f'{val:.1f}%',
                va='center', fontsize=10, color=COLORS['text'])

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    ax.set_xlabel('Presence (%)')
    ax.set_xlim(0, max(values) * 1.2 if values else 100)
    ax.set_title(title, fontsize=14, fontweight='bold', color=COLORS['primary'])
    ax.invert_yaxis()  # Top to bottom
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#fafafa')
    plt.close()

    return output_path


def generate_concept_cloud(concepts: Dict[str, int], output_path: Path, title: str = "Core Concepts"):
    """
    Generate a bubble chart for concept frequency.

    Args:
        concepts: Dict of concept -> count
        output_path: Where to save PNG
        title: Chart title
    """
    if not HAS_MATPLOTLIB:
        return None

    setup_style()

    # Take top 12 concepts
    sorted_concepts = sorted(concepts.items(), key=lambda x: x[1], reverse=True)[:12]
    if not sorted_concepts:
        return None

    names = [c[0] for c in sorted_concepts]
    counts = [c[1] for c in sorted_concepts]

    # Normalize sizes
    max_count = max(counts)
    sizes = [(c / max_count) * 2000 + 200 for c in counts]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Position bubbles in a cloud-like arrangement
    np.random.seed(42)  # Reproducible
    x = np.random.uniform(0.1, 0.9, len(names))
    y = np.random.uniform(0.2, 0.8, len(names))

    # Adjust positions based on size (bigger = more central)
    for i, size in enumerate(sizes):
        factor = size / max(sizes)
        x[i] = 0.5 + (x[i] - 0.5) * (1 - factor * 0.5)
        y[i] = 0.5 + (y[i] - 0.5) * (1 - factor * 0.5)

    scatter = ax.scatter(x, y, s=sizes, c=range(len(names)),
                         cmap='Blues', alpha=0.7, edgecolors=COLORS['primary'], linewidth=2)

    # Add labels
    for i, (xi, yi, name, count) in enumerate(zip(x, y, names, counts)):
        ax.annotate(f'{name}\n({count})', (xi, yi), ha='center', va='center',
                    fontsize=9, fontweight='bold', color=COLORS['dark'])

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title(title, fontsize=14, fontweight='bold', color=COLORS['primary'])

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#fafafa')
    plt.close()

    return output_path


def generate_coherence_breakdown(coherence: Dict[str, float], output_path: Path, title: str = "Coherence Breakdown"):
    """
    Generate radar/spider chart for coherence components.

    Args:
        coherence: Dict with concept_density, cross_reference, domain_coverage, term_consistency
        output_path: Where to save PNG
        title: Chart title
    """
    if not HAS_MATPLOTLIB:
        return None

    setup_style()

    categories = ['Concept\nDensity', 'Cross\nReference', 'Domain\nCoverage', 'Term\nConsistency']
    values = [
        coherence.get('concept_density', 0),
        coherence.get('cross_reference', 0),
        coherence.get('domain_coverage', 0),
        coherence.get('term_consistency', 0)
    ]

    # Close the radar
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Plot
    ax.plot(angles, values, 'o-', linewidth=2, color=COLORS['primary'])
    ax.fill(angles, values, alpha=0.25, color=COLORS['primary'])

    # Set the labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=10)

    # Set y-axis
    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(['25', '50', '75', '100'], size=8, color=COLORS['text'])

    ax.set_title(title, fontsize=14, fontweight='bold', color=COLORS['primary'], pad=20)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#fafafa')
    plt.close()

    return output_path


def generate_breakthrough_badge(breakthroughs: List[Dict], output_path: Path):
    """
    Generate a visual badge showing breakthrough status.

    Args:
        breakthroughs: List of breakthrough dicts
        output_path: Where to save PNG
    """
    if not HAS_MATPLOTLIB:
        return None

    setup_style()

    fig, ax = plt.subplots(figsize=(4, 2))

    count = len(breakthroughs)

    if count == 0:
        color = COLORS['grid']
        text = "No Breakthroughs"
        icon = "○"
    elif count == 1:
        color = COLORS['warning']
        text = "1 Breakthrough"
        icon = "★"
    else:
        color = COLORS['accent']
        text = f"{count} Breakthroughs"
        icon = "★" * min(count, 3)

    # Draw badge
    badge = FancyBboxPatch((0.1, 0.2), 0.8, 0.6, boxstyle="round,pad=0.05",
                            facecolor=color, edgecolor=COLORS['dark'], linewidth=2)
    ax.add_patch(badge)

    ax.text(0.5, 0.55, icon, fontsize=24, ha='center', va='center', color=COLORS['dark'])
    ax.text(0.5, 0.35, text, fontsize=12, ha='center', va='center',
            color=COLORS['dark'], fontweight='bold')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#fafafa')
    plt.close()

    return output_path


def generate_all_charts(analysis_result: Dict, output_dir: Path) -> Dict[str, Path]:
    """
    Generate all charts for an analysis result.

    Args:
        analysis_result: Full analysis dict from core_analyzer
        output_dir: Directory to save charts

    Returns:
        Dict mapping chart type to file path
    """
    if not HAS_MATPLOTLIB:
        print("Charts skipped - matplotlib not installed")
        return {}

    output_dir.mkdir(parents=True, exist_ok=True)
    charts = {}

    filename_base = Path(analysis_result['meta']['filename']).stem

    # Coherence gauge
    coherence_path = output_dir / f"{filename_base}_coherence_gauge.png"
    generate_coherence_gauge(
        analysis_result['coherence']['total'],
        coherence_path,
        "Overall Coherence"
    )
    charts['coherence_gauge'] = coherence_path

    # Coherence breakdown radar
    breakdown_path = output_dir / f"{filename_base}_coherence_radar.png"
    generate_coherence_breakdown(
        analysis_result['coherence'],
        breakdown_path,
        "Coherence Components"
    )
    charts['coherence_radar'] = breakdown_path

    # Domain distribution
    if analysis_result.get('domains'):
        domain_path = output_dir / f"{filename_base}_domains.png"
        generate_domain_chart(
            analysis_result['domains'],
            domain_path,
            "Domain Distribution"
        )
        charts['domains'] = domain_path

    # Concept cloud
    if analysis_result.get('concepts'):
        concept_path = output_dir / f"{filename_base}_concepts.png"
        generate_concept_cloud(
            analysis_result['concepts'],
            concept_path,
            "Core Concepts"
        )
        charts['concepts'] = concept_path

    # Breakthrough badge
    breakthrough_path = output_dir / f"{filename_base}_breakthroughs.png"
    generate_breakthrough_badge(
        analysis_result.get('breakthroughs', []),
        breakthrough_path
    )
    charts['breakthroughs'] = breakthrough_path

    return charts


def generate_comparison_charts(comparison: Dict, output_dir: Path) -> Dict[str, Path]:
    """Generate charts for paper comparison."""
    if not HAS_MATPLOTLIB:
        return {}

    output_dir.mkdir(parents=True, exist_ok=True)
    charts = {}

    # Coherence comparison bar chart
    fig, ax = plt.subplots(figsize=(6, 4))

    files = [comparison['meta']['file1'][:20], comparison['meta']['file2'][:20]]
    scores = [comparison['coherence_delta']['file1'], comparison['coherence_delta']['file2']]

    bars = ax.bar(files, scores, color=[COLORS['primary'], COLORS['secondary']], edgecolor='white')

    for bar, score in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{score:.0f}', ha='center', fontsize=12, fontweight='bold')

    ax.set_ylabel('Coherence Score')
    ax.set_ylim(0, 100)
    ax.set_title('Coherence Comparison', fontsize=14, fontweight='bold', color=COLORS['primary'])

    plt.tight_layout()
    comp_path = output_dir / "comparison_coherence.png"
    plt.savefig(comp_path, dpi=150, bbox_inches='tight', facecolor='#fafafa')
    plt.close()

    charts['coherence_comparison'] = comp_path

    return charts


if __name__ == "__main__":
    # Test with sample data
    sample_result = {
        "meta": {"filename": "Test_Paper.md"},
        "coherence": {
            "total": 72.5,
            "concept_density": 65,
            "cross_reference": 80,
            "domain_coverage": 75,
            "term_consistency": 70
        },
        "domains": {
            "physics": 35.2,
            "theology": 28.1,
            "mathematics": 18.5,
            "information": 10.2,
            "consciousness": 5.0,
            "philosophy": 3.0
        },
        "concepts": {
            "logos": 15,
            "coherence": 12,
            "quantum": 10,
            "grace": 8,
            "entropy": 7,
            "consciousness": 5,
            "trinity": 4
        },
        "breakthroughs": [
            {"type": "cross_domain", "strength": 4, "description": "Test breakthrough"}
        ]
    }

    output = Path("_test_charts")
    charts = generate_all_charts(sample_result, output)
    print(f"Generated {len(charts)} charts in {output}")
