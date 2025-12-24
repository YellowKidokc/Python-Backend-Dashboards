"""
Generate Master Dashboard from all paper analyses
"""

import re
from pathlib import Path
from datetime import datetime

ANALYSIS_ROOT = Path(r"D:\THEOPHYSICS_MASTER\_ANALYSIS")
LOCAL_PAPERS = ANALYSIS_ROOT / "LOCAL_PAPERS"
CURRENT = ANALYSIS_ROOT / "00_CURRENT"

def extract_metrics(dashboard_path):
    """Extract key metrics from a LOCAL_DASHBOARD.md"""
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    metrics = {}
    
    # Extract coherence score
    match = re.search(r'\*\*Overall Coherence:\*\* ([\d.]+)/100', content)
    metrics['coherence'] = float(match.group(1)) if match else 0.0
    
    # Extract breakthroughs
    match = re.search(r'\*\*Found:\*\* (\d+) breakthroughs', content)
    metrics['breakthroughs'] = int(match.group(1)) if match else 0
    
    # Extract top concepts
    concepts = []
    lines = content.split('\n')
    in_concepts = False
    for line in lines:
        if '## 💡 TOP CONCEPTS' in line or '## TOP CONCEPTS' in line:
            in_concepts = True
            continue
        if in_concepts and '|' in line and not 'Concept' in line and not '---' in line:
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 2 and parts[0] and parts[1].isdigit():
                concepts.append((parts[0], int(parts[1])))
            if len(concepts) >= 5:
                break
    
    metrics['top_concepts'] = concepts[:5]
    
    return metrics

# Collect all paper data
papers_data = []

for paper_folder in sorted(LOCAL_PAPERS.iterdir()):
    if not paper_folder.is_dir():
        continue
    
    dashboard = paper_folder / "LOCAL_DASHBOARD.md"
    if not dashboard.exists():
        continue
    
    try:
        metrics = extract_metrics(dashboard)
        papers_data.append({
            'name': paper_folder.name,
            'coherence': metrics['coherence'],
            'breakthroughs': metrics['breakthroughs'],
            'top_concepts': metrics['top_concepts']
        })
    except Exception as e:
        print(f"Error processing {paper_folder.name}: {e}")

# Generate master dashboard
CURRENT.mkdir(parents=True, exist_ok=True)
dashboard_path = CURRENT / "MASTER_DASHBOARD.md"

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(f"# THEOPHYSICS MASTER ANALYSIS DASHBOARD\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"**Papers Analyzed:** {len(papers_data)}/12\n\n")
    f.write(f"---\n\n")
    
    # Summary statistics
    avg_coherence = sum(p['coherence'] for p in papers_data) / len(papers_data) if papers_data else 0
    total_breakthroughs = sum(p['breakthroughs'] for p in papers_data)
    
    f.write(f"## FRAMEWORK OVERVIEW\n\n")
    f.write(f"- **Average Coherence:** {avg_coherence:.1f}/100\n")
    f.write(f"- **Total Breakthroughs:** {total_breakthroughs}\n")
    f.write(f"- **Coherence Range:** {min(p['coherence'] for p in papers_data):.1f} - {max(p['coherence'] for p in papers_data):.1f}\n\n")
    f.write(f"---\n\n")
    
    # Paper summaries table
    f.write(f"## PAPER SUMMARIES\n\n")
    f.write(f"| Paper | Coherence | Breakthroughs | Top Concept |\n")
    f.write(f"|-------|-----------|---------------|-------------|\n")
    
    for paper in papers_data:
        top_concept = paper['top_concepts'][0][0] if paper['top_concepts'] else "N/A"
        top_count = paper['top_concepts'][0][1] if paper['top_concepts'] else 0
        f.write(f"| {paper['name'][:30]} | {paper['coherence']:.1f}/100 | {paper['breakthroughs']} | {top_concept} ({top_count}) |\n")
    
    f.write(f"\n---\n\n")
    
    # Detailed concept analysis
    f.write(f"## TOP CONCEPTS BY PAPER\n\n")
    for paper in papers_data:
        f.write(f"### {paper['name']}\n")
        f.write(f"**Coherence:** {paper['coherence']:.1f}/100\n\n")
        if paper['top_concepts']:
            for concept, count in paper['top_concepts']:
                f.write(f"- {concept}: {count}\n")
        f.write(f"\n")
    
    f.write(f"---\n\n")
    
    # Links to individual reports
    f.write(f"## DETAILED REPORTS\n\n")
    for paper in papers_data:
        f.write(f"- [{paper['name']}](../LOCAL_PAPERS/{paper['name']}/LOCAL_DASHBOARD.md)\n")

print(f"Master dashboard created: {dashboard_path}")
