"""
THEOPHYSICS MASTER ANALYSIS ORCHESTRATOR
Coordinates all analysis operations across papers and system
"""

import os
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# ============================================================================
# PATHS
# ============================================================================

BASE = Path(r"D:\THEOPHYSICS_MASTER")
ANALYSIS_ROOT = BASE / "_ANALYSIS"
PAPERS_ROOT = BASE / "06_Publication" / "Logos_Papers"

CURRENT = ANALYSIS_ROOT / "00_CURRENT"
LOCAL = ANALYSIS_ROOT / "LOCAL_PAPERS"
GLOBAL_DIR = ANALYSIS_ROOT / "GLOBAL"
ARCHIVE = ANALYSIS_ROOT / "ARCHIVE"
TOOLS = ANALYSIS_ROOT / "TOOLS"

# ============================================================================
# PAPER REGISTRY
# ============================================================================

PAPERS = {
    "P01": "Logos_Principle",
    "P02": "Quantum_Bridge",
    "P03": "Algorithm_Reality",
    "P04": "Hard_Problem",
    "P05": "Soul_Physics",
    "P06": "Principalities",
    "P07": "Grace_Function",
    "P08": "Stretched_Heavens",
    "P09": "Moral_Universe",
    "P10": "AI_Consciousness",
    "P11": "Protocols",
    "P12": "Decalogue"
}

# ============================================================================
# ORCHESTRATOR CLASS
# ============================================================================

class AnalysisOrchestrator:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        self.results = {
            "timestamp": self.timestamp,
            "papers_analyzed": [],
            "global_analyses": [],
            "errors": []
        }
    
    def analyze_single_paper(self, paper_id):
        """Analyze a single paper"""
        print(f"\n{'='*60}")
        print(f"ANALYZING {paper_id} - {PAPERS[paper_id]}")
        print(f"{'='*60}")
        
        paper_name = f"{paper_id}-{PAPERS[paper_id]}"
        paper_path = PAPERS_ROOT / paper_name
        local_path = paper_path / "_LOCAL"
        
        # Check if _LOCAL exists
        if not local_path.exists():
            print(f"❌ No _LOCAL folder found at {local_path}")
            self.results["errors"].append(f"{paper_id}: No _LOCAL folder")
            return False
        
        # Check if analyze_paper.py exists
        script = local_path / "analyze_paper.py"
        if not script.exists():
            print(f"❌ No analyze_paper.py found")
            self.results["errors"].append(f"{paper_id}: No analyzer script")
            return False
        
        try:
            # Run the analysis
            print(f"Running analysis...")
            result = subprocess.run(
                ["python", str(script)],
                cwd=str(local_path),
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                print(f"✅ Analysis complete!")
                
                # Copy results to LOCAL_PAPERS
                dest = LOCAL / f"{paper_id}_{PAPERS[paper_id]}"
                dest.mkdir(parents=True, exist_ok=True)
                
                for item in local_path.iterdir():
                    if item.is_file():
                        shutil.copy2(item, dest)
                    elif item.is_dir() and item.name.startswith("_"):
                        shutil.copytree(item, dest / item.name, dirs_exist_ok=True)
                
                print(f"✅ Results copied to {dest}")
                self.results["papers_analyzed"].append(paper_id)
                return True
            else:
                print(f"❌ Analysis failed: {result.stderr}")
                self.results["errors"].append(f"{paper_id}: {result.stderr[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            self.results["errors"].append(f"{paper_id}: {str(e)}")
            return False
    
    def analyze_all_papers(self):
        """Analyze all 12 papers"""
        print(f"\n{'='*60}")
        print(f"BATCH ANALYSIS: ALL 12 PAPERS")
        print(f"{'='*60}\n")
        
        for paper_id in PAPERS.keys():
            self.analyze_single_paper(paper_id)
        
        self.generate_master_dashboard()
    
    def generate_master_dashboard(self):
        """Generate the master dashboard in 00_CURRENT"""
        print(f"\n{'='*60}")
        print(f"GENERATING MASTER DASHBOARD")
        print(f"{'='*60}")
        
        dashboard = CURRENT / "MASTER_DASHBOARD.md"
        
        # Collect stats from all analyzed papers
        papers_data = []
        for paper_id in self.results["papers_analyzed"]:
            paper_folder = LOCAL / f"{paper_id}_{PAPERS[paper_id]}"
            dashboard_file = paper_folder / "LOCAL_DASHBOARD.md"
            
            if dashboard_file.exists():
                with open(dashboard_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Extract key metrics (simple parsing)
                    coherence = "N/A"
                    breakthroughs = "N/A"
                    
                    if "Overall Coherence:" in content:
                        line = [l for l in content.split('\n') if 'Overall Coherence:' in l][0]
                        coherence = line.split(':')[1].strip()
                    
                    if "Found:" in content:
                        line = [l for l in content.split('\n') if 'Found:' in l][0]
                        breakthroughs = line.split(':')[1].strip()
                    
                    papers_data.append({
                        "id": paper_id,
                        "name": PAPERS[paper_id],
                        "coherence": coherence,
                        "breakthroughs": breakthroughs
                    })
        
        # Write master dashboard
        with open(dashboard, 'w', encoding='utf-8') as f:
            f.write(f"# 🎯 THEOPHYSICS MASTER ANALYSIS DASHBOARD\n\n")
            f.write(f"**Generated:** {self.timestamp}\n\n")
            f.write(f"---\n\n")
            
            f.write(f"## 📊 OVERVIEW\n\n")
            f.write(f"**Papers Analyzed:** {len(self.results['papers_analyzed'])}/12\n")
            f.write(f"**Global Analyses:** {len(self.results['global_analyses'])}\n")
            f.write(f"**Errors:** {len(self.results['errors'])}\n\n")
            
            f.write(f"---\n\n")
            f.write(f"## 📈 PAPER SUMMARIES\n\n")
            f.write(f"| Paper | Name | Coherence | Breakthroughs |\n")
            f.write(f"|-------|------|-----------|---------------|\n")
            
            for paper in papers_data:
                f.write(f"| {paper['id']} | {paper['name']} | {paper['coherence']} | {paper['breakthroughs']} |\n")
            
            f.write(f"\n---\n\n")
            f.write(f"## 🔗 DETAILED REPORTS\n\n")
            for paper in papers_data:
                f.write(f"- [{paper['id']} - {paper['name']}](../LOCAL_PAPERS/{paper['id']}_{paper['name']}/LOCAL_DASHBOARD.md)\n")
            
            if self.results['errors']:
                f.write(f"\n---\n\n")
                f.write(f"## ⚠️ ERRORS\n\n")
                for error in self.results['errors']:
                    f.write(f"- {error}\n")
        
        print(f"✅ Master dashboard created: {dashboard}")
    
    def create_archive_snapshot(self, description="snapshot"):
        """Create timestamped archive of current analyses"""
        archive_folder = ARCHIVE / f"{self.timestamp}_{description}"
        archive_folder.mkdir(parents=True, exist_ok=True)
        
        # Copy LOCAL_PAPERS
        if LOCAL.exists():
            shutil.copytree(LOCAL, archive_folder / "LOCAL_PAPERS", dirs_exist_ok=True)
        
        # Copy CURRENT dashboard
        if (CURRENT / "MASTER_DASHBOARD.md").exists():
            shutil.copy2(CURRENT / "MASTER_DASHBOARD.md", archive_folder)
        
        print(f"✅ Archive created: {archive_folder}")

# ============================================================================
# MAIN CLI
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Theophysics Analysis Orchestrator")
    parser.add_argument("--paper", help="Analyze single paper (e.g., P03)")
    parser.add_argument("--all", action="store_true", help="Analyze all papers")
    parser.add_argument("--dashboard", action="store_true", help="Regenerate master dashboard only")
    parser.add_argument("--archive", help="Create archive with description")
    
    args = parser.parse_args()
    
    orch = AnalysisOrchestrator()
    
    if args.paper:
        if args.paper in PAPERS:
            orch.analyze_single_paper(args.paper)
            orch.generate_master_dashboard()
        else:
            print(f"❌ Unknown paper: {args.paper}")
            print(f"Valid papers: {list(PAPERS.keys())}")
    
    elif args.all:
        orch.analyze_all_papers()
    
    elif args.dashboard:
        orch.generate_master_dashboard()
    
    elif args.archive:
        orch.create_archive_snapshot(args.archive)
    
    else:
        print("Usage:")
        print("  python master_orchestrator.py --paper P03")
        print("  python master_orchestrator.py --all")
        print("  python master_orchestrator.py --dashboard")
        print("  python master_orchestrator.py --archive 'post_refinement'")
