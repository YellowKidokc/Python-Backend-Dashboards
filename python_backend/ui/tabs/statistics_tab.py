"""
Statistics Tab - Multi-Paper Analytics Dashboard
Provides folder-based analysis, paper comparison, and per-folder dashboards.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTextEdit, QGroupBox, QComboBox, QListWidget, QListWidgetItem,
    QProgressBar, QLineEdit, QFileDialog, QMessageBox, QCheckBox,
    QTabWidget, QSplitter, QFrame, QSpinBox, QAbstractItemView
)
from PySide6.QtCore import Qt, QThread, Signal

# Import the core analyzer (adjust path as needed)
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "global_analytics" / "theophysics_analytics"))
try:
    from core_analyzer import TheophysicsAnalyzer
except ImportError:
    TheophysicsAnalyzer = None


class AnalysisWorker(QThread):
    """Worker thread for running analysis operations."""
    progress = Signal(str)
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, analyzer, mode: str, targets: List[Path], compare_to: Optional[Path] = None):
        super().__init__()
        self.analyzer = analyzer
        self.mode = mode
        self.targets = targets
        self.compare_to = compare_to

    def run(self):
        try:
            results = {}

            if self.mode == "folder":
                self.progress.emit(f"Analyzing folder: {self.targets[0]}")
                results = self._analyze_folder(self.targets[0])

            elif self.mode == "single":
                self.progress.emit(f"Analyzing file: {self.targets[0].name}")
                results = self.analyzer.analyze_file(str(self.targets[0]))

            elif self.mode == "compare":
                self.progress.emit(f"Comparing {len(self.targets)} papers...")
                results = self._compare_papers(self.targets)

            elif self.mode == "compare_baseline":
                self.progress.emit(f"Comparing to baseline: {self.compare_to}")
                results = self._compare_to_baseline(self.targets, self.compare_to)

            self.finished.emit(results)

        except Exception as e:
            self.error.emit(str(e))

    def _analyze_folder(self, folder: Path) -> Dict:
        """Analyze all markdown files in a folder."""
        md_files = list(folder.rglob("*.md"))
        results = {
            "folder": str(folder),
            "file_count": len(md_files),
            "analyzed_at": datetime.now().isoformat(),
            "papers": [],
            "aggregate": {
                "total_words": 0,
                "total_concepts": {},
                "total_domains": {},
                "avg_coherence": 0
            }
        }

        coherence_sum = 0
        for i, md_file in enumerate(md_files):
            self.progress.emit(f"Analyzing {i+1}/{len(md_files)}: {md_file.name}")
            try:
                paper_result = self.analyzer.analyze_file(str(md_file))
                results["papers"].append({
                    "file": md_file.name,
                    "coherence": paper_result["coherence"]["total"],
                    "word_count": paper_result["meta"]["word_count"],
                    "domains": paper_result["domains"]
                })

                # Aggregate
                results["aggregate"]["total_words"] += paper_result["meta"]["word_count"]
                coherence_sum += paper_result["coherence"]["total"]

                for concept, count in paper_result["concepts"].items():
                    results["aggregate"]["total_concepts"][concept] = \
                        results["aggregate"]["total_concepts"].get(concept, 0) + count

                for domain, count in paper_result["domains"].items():
                    results["aggregate"]["total_domains"][domain] = \
                        results["aggregate"]["total_domains"].get(domain, 0) + count

            except Exception as e:
                results["papers"].append({"file": md_file.name, "error": str(e)})

        if results["papers"]:
            results["aggregate"]["avg_coherence"] = round(coherence_sum / len(results["papers"]), 1)

        return results

    def _compare_papers(self, papers: List[Path]) -> Dict:
        """Compare multiple papers to each other."""
        comparisons = {
            "compared_at": datetime.now().isoformat(),
            "papers": [p.name for p in papers],
            "pairwise": [],
            "concept_matrix": {},
            "domain_alignment": {}
        }

        # Analyze all papers first
        paper_results = {}
        for paper in papers:
            self.progress.emit(f"Analyzing: {paper.name}")
            paper_results[paper.name] = self.analyzer.analyze_file(str(paper))

        # Pairwise comparisons
        for i, p1 in enumerate(papers):
            for p2 in papers[i+1:]:
                self.progress.emit(f"Comparing: {p1.name} vs {p2.name}")
                comparison = self.analyzer.compare_files(str(p1), str(p2))
                comparisons["pairwise"].append(comparison)

        # Build concept matrix (which papers share which concepts)
        all_concepts = set()
        for result in paper_results.values():
            all_concepts.update(result["concepts"].keys())

        for concept in all_concepts:
            papers_with_concept = [
                p for p, r in paper_results.items()
                if concept in r["concepts"]
            ]
            if len(papers_with_concept) > 1:
                comparisons["concept_matrix"][concept] = papers_with_concept

        return comparisons

    def _compare_to_baseline(self, papers: List[Path], baseline: Path) -> Dict:
        """Compare papers against a baseline/reference."""
        baseline_result = self.analyzer.analyze_file(str(baseline))

        comparisons = {
            "baseline": baseline.name,
            "baseline_coherence": baseline_result["coherence"]["total"],
            "compared_at": datetime.now().isoformat(),
            "papers": []
        }

        for paper in papers:
            self.progress.emit(f"Comparing {paper.name} to baseline...")
            comparison = self.analyzer.compare_files(str(baseline), str(paper))
            comparisons["papers"].append({
                "paper": paper.name,
                "coherence_delta": comparison["coherence_delta"]["delta"],
                "overlap_percent": comparison["concept_overlap"]["overlap_percent"],
                "unique_concepts": comparison["concept_overlap"]["unique_to_file2"]
            })

        return comparisons


class StatisticsTab(QWidget):
    """Tab for paper statistics and multi-paper comparisons."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.analyzer = None
        self.worker = None
        self.working_folder = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("Paper Statistics & Comparison Engine")
        header.setStyleSheet("font-size: 18pt; font-weight: bold; margin: 10px;")
        layout.addWidget(header)

        # Main splitter
        splitter = QSplitter(Qt.Horizontal)

        # LEFT PANEL - Folder/Paper Selection
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)

        # Folder Selection
        folder_group = QGroupBox("1. Select Analysis Source")
        folder_layout = QVBoxLayout()

        # Quick folders from Global Analytics
        quick_label = QLabel("Quick Select (Global Analytics):")
        folder_layout.addWidget(quick_label)

        self.quick_folder_combo = QComboBox()
        self.quick_folder_combo.addItem("-- Select folder --", None)
        self._populate_global_analytics_folders()
        self.quick_folder_combo.currentIndexChanged.connect(self._on_quick_folder_selected)
        folder_layout.addWidget(self.quick_folder_combo)

        folder_layout.addWidget(QLabel("Or browse:"))

        browse_row = QHBoxLayout()
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Path to folder with papers...")
        browse_row.addWidget(self.folder_input)

        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_folder)
        browse_row.addWidget(browse_btn)
        folder_layout.addLayout(browse_row)

        # Copy folder option
        copy_row = QHBoxLayout()
        self.copy_checkbox = QCheckBox("Copy to working directory first")
        self.copy_checkbox.setToolTip("Copies the source folder to a working location before analysis")
        copy_row.addWidget(self.copy_checkbox)

        self.working_dir_input = QLineEdit()
        self.working_dir_input.setPlaceholderText("Working directory...")
        self.working_dir_input.setEnabled(False)
        copy_row.addWidget(self.working_dir_input)

        self.copy_checkbox.toggled.connect(self.working_dir_input.setEnabled)
        folder_layout.addLayout(copy_row)

        set_folder_btn = QPushButton("Set Analysis Folder")
        set_folder_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        set_folder_btn.clicked.connect(self._set_analysis_folder)
        folder_layout.addWidget(set_folder_btn)

        folder_group.setLayout(folder_layout)
        left_layout.addWidget(folder_group)

        # Paper Selection
        paper_group = QGroupBox("2. Select Papers")
        paper_layout = QVBoxLayout()

        paper_layout.addWidget(QLabel("Papers in selected folder:"))

        self.paper_list = QListWidget()
        self.paper_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.paper_list.setMinimumHeight(200)
        paper_layout.addWidget(self.paper_list)

        select_row = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self._select_all_papers)
        select_row.addWidget(select_all_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.paper_list.clearSelection)
        select_row.addWidget(clear_btn)
        paper_layout.addLayout(select_row)

        paper_group.setLayout(paper_layout)
        left_layout.addWidget(paper_group)

        splitter.addWidget(left_panel)

        # RIGHT PANEL - Analysis Options & Results
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)

        # Analysis Mode
        mode_group = QGroupBox("3. Analysis Mode")
        mode_layout = QVBoxLayout()

        self.mode_combo = QComboBox()
        self.mode_combo.addItem("Analyze Entire Folder", "folder")
        self.mode_combo.addItem("Analyze Single Paper", "single")
        self.mode_combo.addItem("Compare Selected Papers", "compare")
        self.mode_combo.addItem("Compare to Baseline (Tissue Layer)", "compare_baseline")
        self.mode_combo.addItem("Generate Dashboard Type", "dashboard")
        self.mode_combo.currentIndexChanged.connect(self._on_mode_changed)
        mode_layout.addWidget(self.mode_combo)

        # Dashboard type selection (for dashboard mode)
        self.dashboard_row = QWidget()
        dash_layout = QVBoxLayout(self.dashboard_row)
        dash_layout.setContentsMargins(0, 5, 0, 0)
        dash_layout.addWidget(QLabel("Select Dashboard Type:"))

        self.dashboard_combo = QComboBox()
        self._populate_dashboard_types()
        dash_layout.addWidget(self.dashboard_combo)

        self.dashboard_row.setVisible(False)
        mode_layout.addWidget(self.dashboard_row)

        # Baseline selection (for compare_baseline mode)
        self.baseline_row = QWidget()
        baseline_layout = QHBoxLayout(self.baseline_row)
        baseline_layout.setContentsMargins(0, 0, 0, 0)
        baseline_layout.addWidget(QLabel("Baseline file:"))

        self.baseline_input = QLineEdit()
        self.baseline_input.setPlaceholderText("Select baseline/reference paper...")
        baseline_layout.addWidget(self.baseline_input)

        baseline_browse = QPushButton("Browse")
        baseline_browse.clicked.connect(self._browse_baseline)
        baseline_layout.addWidget(baseline_browse)

        self.baseline_row.setVisible(False)
        mode_layout.addWidget(self.baseline_row)

        mode_group.setLayout(mode_layout)
        right_layout.addWidget(mode_group)

        # Run Analysis
        run_group = QGroupBox("4. Run Analysis")
        run_layout = QVBoxLayout()

        run_btn = QPushButton("RUN ANALYSIS")
        run_btn.setStyleSheet("background-color: #2196F3; color: white; font-size: 14pt; padding: 15px;")
        run_btn.clicked.connect(self._run_analysis)
        run_layout.addWidget(run_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        run_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready")
        run_layout.addWidget(self.status_label)

        run_group.setLayout(run_layout)
        right_layout.addWidget(run_group)

        # Results
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(250)
        results_layout.addWidget(self.results_text)

        export_row = QHBoxLayout()
        export_json_btn = QPushButton("Export JSON")
        export_json_btn.clicked.connect(self._export_json)
        export_row.addWidget(export_json_btn)

        export_dashboard_btn = QPushButton("Generate Dashboard")
        export_dashboard_btn.clicked.connect(self._generate_dashboard)
        export_row.addWidget(export_dashboard_btn)

        results_layout.addLayout(export_row)

        results_group.setLayout(results_layout)
        right_layout.addWidget(results_group)

        splitter.addWidget(right_panel)
        splitter.setSizes([400, 600])

        layout.addWidget(splitter)

        # Store last results
        self.last_results = None

    def _populate_global_analytics_folders(self):
        """Populate combo with folders from global_analytics."""
        ga_path = Path(__file__).parent.parent.parent.parent / "global_analytics"
        if ga_path.exists():
            for folder in sorted(ga_path.iterdir()):
                if folder.is_dir() and not folder.name.startswith("."):
                    self.quick_folder_combo.addItem(f"  {folder.name}", str(folder))

    def _on_quick_folder_selected(self, index):
        """Handle quick folder selection."""
        folder_path = self.quick_folder_combo.currentData()
        if folder_path:
            self.folder_input.setText(folder_path)

    def _browse_folder(self):
        """Browse for a folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Papers Folder")
        if folder:
            self.folder_input.setText(folder)

    def _browse_baseline(self):
        """Browse for a baseline file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Baseline Paper", "", "Markdown files (*.md)"
        )
        if file_path:
            self.baseline_input.setText(file_path)

    def _set_analysis_folder(self):
        """Set the analysis folder, optionally copying it first."""
        source_path = Path(self.folder_input.text())

        if not source_path.exists():
            QMessageBox.warning(self, "Error", "Source folder does not exist!")
            return

        if self.copy_checkbox.isChecked():
            working_dir = self.working_dir_input.text()
            if not working_dir:
                working_dir = str(Path.home() / "theophysics_analysis" / source_path.name)
                self.working_dir_input.setText(working_dir)

            dest_path = Path(working_dir)
            if dest_path.exists():
                reply = QMessageBox.question(
                    self, "Folder Exists",
                    f"Working folder already exists. Overwrite?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return
                shutil.rmtree(dest_path)

            self.status_label.setText(f"Copying folder...")
            shutil.copytree(source_path, dest_path)
            self.working_folder = dest_path
            self.status_label.setText(f"Copied to: {dest_path}")
        else:
            self.working_folder = source_path

        # Populate paper list
        self._refresh_paper_list()

        # Initialize analyzer
        if TheophysicsAnalyzer:
            self.analyzer = TheophysicsAnalyzer()
            self.status_label.setText(f"Ready. Found {self.paper_list.count()} papers.")
        else:
            QMessageBox.warning(self, "Warning", "TheophysicsAnalyzer not available. Using mock mode.")

    def _refresh_paper_list(self):
        """Refresh the list of papers in the working folder."""
        self.paper_list.clear()
        if self.working_folder and self.working_folder.exists():
            for md_file in sorted(self.working_folder.rglob("*.md")):
                item = QListWidgetItem(md_file.name)
                item.setData(Qt.UserRole, str(md_file))
                self.paper_list.addItem(item)

    def _select_all_papers(self):
        """Select all papers in the list."""
        self.paper_list.selectAll()

    def _on_mode_changed(self, index):
        """Handle analysis mode change."""
        mode = self.mode_combo.currentData()
        self.baseline_row.setVisible(mode == "compare_baseline")
        self.dashboard_row.setVisible(mode == "dashboard")

    def _populate_dashboard_types(self):
        """Populate dashboard type dropdown from registry."""
        # Core Analytics dashboards
        self.dashboard_combo.addItem("── Core Analytics ──", None)
        self.dashboard_combo.addItem("  📊 Axioms Dashboard", "axioms")
        self.dashboard_combo.addItem("  🚀 Breakthroughs Dashboard", "breakthroughs")
        self.dashboard_combo.addItem("  🎯 Coherence Dashboard", "coherence")
        self.dashboard_combo.addItem("  📝 Claims Dashboard", "claims")
        self.dashboard_combo.addItem("  📖 Definitions Dashboard", "definitions")
        self.dashboard_combo.addItem("  🔬 Evidence Dashboard", "evidence")
        self.dashboard_combo.addItem("  ∑ Mathematics Dashboard", "mathematics")
        self.dashboard_combo.addItem("  🏷️ Tags Dashboard", "tags")
        self.dashboard_combo.addItem("  📚 References Dashboard", "references")
        self.dashboard_combo.addItem("  🔗 Links Dashboard", "links")
        self.dashboard_combo.addItem("  📅 Timeline Dashboard", "timeline")

        # Paper Management dashboards
        self.dashboard_combo.addItem("── Paper Management ──", None)
        self.dashboard_combo.addItem("  📄 Logos Papers (P1-P12)", "logos_papers")
        self.dashboard_combo.addItem("  ⚖️ Paper Comparison", "paper_comparison")
        self.dashboard_combo.addItem("  ✅ Validation Dashboard", "validation")

        # System Health dashboards
        self.dashboard_combo.addItem("── System Health ──", None)
        self.dashboard_combo.addItem("  💚 Vault Health", "vault_health")
        self.dashboard_combo.addItem("  🗄️ Database Dashboard", "db_dashboard")

        # Specialized dashboards
        self.dashboard_combo.addItem("── Specialized ──", None)
        self.dashboard_combo.addItem("  χ Master Equation", "master_equation")
        self.dashboard_combo.addItem("  ℒ Lowe Lagrangian", "lowe_lagrangian")

        # Generate All
        self.dashboard_combo.addItem("── Batch ──", None)
        self.dashboard_combo.addItem("  ⚡ Generate ALL Dashboards", "all")

    def _run_analysis(self):
        """Run the selected analysis."""
        if not self.working_folder:
            QMessageBox.warning(self, "Error", "Please set an analysis folder first!")
            return

        mode = self.mode_combo.currentData()

        # Get selected papers
        selected_items = self.paper_list.selectedItems()
        targets = [Path(item.data(Qt.UserRole)) for item in selected_items]

        if mode == "folder":
            targets = [self.working_folder]
        elif mode == "single":
            if len(targets) != 1:
                QMessageBox.warning(self, "Error", "Please select exactly one paper!")
                return
        elif mode in ["compare", "compare_baseline"]:
            if len(targets) < 2:
                QMessageBox.warning(self, "Error", "Please select at least 2 papers to compare!")
                return
        elif mode == "dashboard":
            # Dashboard generation mode
            dashboard_type = self.dashboard_combo.currentData()
            if not dashboard_type:
                QMessageBox.warning(self, "Error", "Please select a valid dashboard type!")
                return
            self._generate_dashboard_type(dashboard_type)
            return

        # Get baseline for comparison mode
        compare_to = None
        if mode == "compare_baseline":
            baseline_path = self.baseline_input.text()
            if not baseline_path or not Path(baseline_path).exists():
                QMessageBox.warning(self, "Error", "Please select a valid baseline file!")
                return
            compare_to = Path(baseline_path)

        # Start analysis
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.results_text.clear()

        if self.analyzer:
            self.worker = AnalysisWorker(self.analyzer, mode, targets, compare_to)
            self.worker.progress.connect(self._on_progress)
            self.worker.finished.connect(self._on_finished)
            self.worker.error.connect(self._on_error)
            self.worker.start()
        else:
            # Mock mode for testing
            self._on_finished({"mock": True, "mode": mode, "targets": [str(t) for t in targets]})

    def _on_progress(self, message: str):
        """Handle progress updates."""
        self.status_label.setText(message)
        self.results_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def _on_finished(self, results: dict):
        """Handle analysis completion."""
        self.progress_bar.setVisible(False)
        self.last_results = results

        # Format results nicely
        self.results_text.append("\n" + "="*50)
        self.results_text.append("ANALYSIS COMPLETE")
        self.results_text.append("="*50 + "\n")

        # Pretty print JSON
        formatted = json.dumps(results, indent=2, default=str)
        self.results_text.append(formatted)

        self.status_label.setText("Analysis complete!")

    def _on_error(self, error: str):
        """Handle analysis error."""
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Error: {error}")
        QMessageBox.critical(self, "Analysis Error", error)

    def _export_json(self):
        """Export results to JSON file."""
        if not self.last_results:
            QMessageBox.warning(self, "No Results", "Run an analysis first!")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Results", "", "JSON files (*.json)"
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.last_results, f, indent=2, default=str)
            self.status_label.setText(f"Saved to: {file_path}")

    def _generate_dashboard(self):
        """Generate a dashboard from results."""
        if not self.last_results:
            QMessageBox.warning(self, "No Results", "Run an analysis first!")
            return

        # Generate markdown dashboard
        dashboard = self._create_dashboard_markdown(self.last_results)

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Dashboard", "", "Markdown files (*.md)"
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(dashboard)
            self.status_label.setText(f"Dashboard saved to: {file_path}")

    def _create_dashboard_markdown(self, results: dict) -> str:
        """Create a markdown dashboard from results."""
        mode = results.get("mode", "analysis")
        now = datetime.now().isoformat()

        dashboard = f"""---
type: analytics_dashboard
generated: {now}
---

# Analytics Dashboard

**Generated:** {now}

---

## Results Summary

```json
{json.dumps(results, indent=2, default=str)[:2000]}
...
```

---

## Key Metrics

| Metric | Value |
|--------|-------|
"""

        if "aggregate" in results:
            agg = results["aggregate"]
            dashboard += f"| Total Words | {agg.get('total_words', 'N/A'):,} |\n"
            dashboard += f"| Avg Coherence | {agg.get('avg_coherence', 'N/A')} |\n"
            dashboard += f"| Papers Analyzed | {results.get('file_count', 'N/A')} |\n"

        if "pairwise" in results:
            dashboard += f"| Comparisons Made | {len(results['pairwise'])} |\n"
            dashboard += f"| Papers Compared | {len(results.get('papers', []))} |\n"

        return dashboard

    def _generate_dashboard_type(self, dashboard_type: str):
        """Generate a specific dashboard type."""
        self.results_text.clear()
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)

        self.results_text.append(f"Generating {dashboard_type} dashboard...")

        # Dashboard generators
        generators = {
            "axioms": self._gen_axioms_dashboard,
            "breakthroughs": self._gen_breakthroughs_dashboard,
            "coherence": self._gen_coherence_dashboard,
            "claims": self._gen_claims_dashboard,
            "definitions": self._gen_definitions_dashboard,
            "evidence": self._gen_evidence_dashboard,
            "mathematics": self._gen_mathematics_dashboard,
            "tags": self._gen_tags_dashboard,
            "references": self._gen_references_dashboard,
            "links": self._gen_links_dashboard,
            "timeline": self._gen_timeline_dashboard,
            "logos_papers": self._gen_logos_papers_dashboard,
            "paper_comparison": self._gen_paper_comparison_dashboard,
            "validation": self._gen_validation_dashboard,
            "vault_health": self._gen_vault_health_dashboard,
            "db_dashboard": self._gen_db_dashboard,
            "master_equation": self._gen_master_equation_dashboard,
            "lowe_lagrangian": self._gen_lowe_lagrangian_dashboard,
            "all": self._gen_all_dashboards,
        }

        generator = generators.get(dashboard_type)
        if generator:
            try:
                result = generator()
                self.last_results = result
                self.results_text.append("\n" + "="*50)
                self.results_text.append(f"✅ {dashboard_type.upper()} DASHBOARD GENERATED")
                self.results_text.append("="*50 + "\n")
                self.results_text.append(json.dumps(result, indent=2, default=str)[:5000])
                self.status_label.setText(f"Dashboard generated: {dashboard_type}")
            except Exception as e:
                self.results_text.append(f"❌ Error: {str(e)}")
                self.status_label.setText(f"Error generating {dashboard_type}")
        else:
            self.results_text.append(f"❌ No generator for: {dashboard_type}")

        self.progress_bar.setVisible(False)

    # ========================================
    # DASHBOARD GENERATORS
    # ========================================

    def _gen_axioms_dashboard(self) -> Dict:
        """Generate Axioms dashboard data."""
        # Load from MASTER_AXIOMS.json
        master_path = Path(__file__).parent.parent.parent.parent / "global_analytics" / "Master_Sheet" / "MASTER_AXIOMS.json"
        if master_path.exists():
            with open(master_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return {
                "dashboard_type": "axioms",
                "generated": datetime.now().isoformat(),
                "summary": data.get("summary", {}),
                "axiom_count": len(data.get("axioms", [])),
                "by_type": data.get("summary", {}).get("by_type", {}),
                "by_paper": data.get("summary", {}).get("by_paper", {}),
                "by_framework": data.get("summary", {}).get("by_framework", {}),
            }
        return {"dashboard_type": "axioms", "error": "MASTER_AXIOMS.json not found"}

    def _gen_breakthroughs_dashboard(self) -> Dict:
        """Generate Breakthroughs dashboard by analyzing papers."""
        if self.analyzer and self.working_folder:
            md_files = list(self.working_folder.rglob("*.md"))
            all_breakthroughs = []
            for md in md_files[:10]:  # Limit for speed
                try:
                    result = self.analyzer.analyze_file(str(md))
                    if result.get("breakthroughs"):
                        for bt in result["breakthroughs"]:
                            bt["source"] = md.name
                            all_breakthroughs.append(bt)
                except:
                    pass
            return {
                "dashboard_type": "breakthroughs",
                "generated": datetime.now().isoformat(),
                "total_breakthroughs": len(all_breakthroughs),
                "breakthroughs": all_breakthroughs[:20],
            }
        return {"dashboard_type": "breakthroughs", "note": "Run folder analysis first"}

    def _gen_coherence_dashboard(self) -> Dict:
        """Generate Coherence dashboard with matrix."""
        if self.analyzer and self.working_folder:
            md_files = list(self.working_folder.rglob("*.md"))[:12]  # P1-P12
            coherence_data = {}
            matrix = {}

            for md in md_files:
                try:
                    result = self.analyzer.analyze_file(str(md))
                    coherence_data[md.stem] = result["coherence"]
                except:
                    pass

            # Build comparison matrix
            papers = list(coherence_data.keys())
            for p1 in papers:
                matrix[p1] = {}
                for p2 in papers:
                    if p1 == p2:
                        matrix[p1][p2] = 100
                    else:
                        # Simple overlap calculation
                        c1, c2 = coherence_data[p1]["total"], coherence_data[p2]["total"]
                        matrix[p1][p2] = round((min(c1, c2) / max(c1, c2)) * 100, 1) if max(c1, c2) > 0 else 0

            avg = sum(c["total"] for c in coherence_data.values()) / max(1, len(coherence_data))

            return {
                "dashboard_type": "coherence",
                "generated": datetime.now().isoformat(),
                "average_coherence": round(avg, 1),
                "per_paper": {k: v["total"] for k, v in coherence_data.items()},
                "coherence_matrix": matrix,
            }
        return {"dashboard_type": "coherence", "note": "Set analysis folder first"}

    def _gen_claims_dashboard(self) -> Dict:
        """Generate Claims dashboard."""
        return {"dashboard_type": "claims", "generated": datetime.now().isoformat(), "note": "Implement claim extraction"}

    def _gen_definitions_dashboard(self) -> Dict:
        """Generate Definitions dashboard."""
        master_path = Path(__file__).parent.parent.parent.parent / "global_analytics" / "Master_Sheet" / "MASTER_DEFINITIONS.json"
        if master_path.exists():
            with open(master_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return {"dashboard_type": "definitions", "generated": datetime.now().isoformat(), "data": data}
        return {"dashboard_type": "definitions", "note": "MASTER_DEFINITIONS.json not found"}

    def _gen_evidence_dashboard(self) -> Dict:
        """Generate Evidence dashboard."""
        return {"dashboard_type": "evidence", "generated": datetime.now().isoformat(), "note": "Implement evidence extraction"}

    def _gen_mathematics_dashboard(self) -> Dict:
        """Generate Mathematics/Equations dashboard."""
        if self.analyzer and self.working_folder:
            md_files = list(self.working_folder.rglob("*.md"))[:12]
            all_equations = []
            for md in md_files:
                try:
                    result = self.analyzer.analyze_file(str(md))
                    for eq in result.get("equations", []):
                        all_equations.append({"equation": eq, "source": md.name})
                except:
                    pass
            return {
                "dashboard_type": "mathematics",
                "generated": datetime.now().isoformat(),
                "total_equations": len(all_equations),
                "equations": all_equations[:50],
            }
        return {"dashboard_type": "mathematics", "note": "Set analysis folder first"}

    def _gen_tags_dashboard(self) -> Dict:
        """Generate Tags dashboard."""
        master_path = Path(__file__).parent.parent.parent.parent / "global_analytics" / "Master_Sheet" / "MASTER_TAGS.json"
        if master_path.exists():
            with open(master_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return {"dashboard_type": "tags", "generated": datetime.now().isoformat(), "data": data}
        return {"dashboard_type": "tags", "note": "MASTER_TAGS.json not found"}

    def _gen_references_dashboard(self) -> Dict:
        """Generate References dashboard."""
        if self.analyzer and self.working_folder:
            md_files = list(self.working_folder.rglob("*.md"))[:12]
            all_refs = []
            for md in md_files:
                try:
                    result = self.analyzer.analyze_file(str(md))
                    for ref in result.get("references", []):
                        all_refs.append({"ref": ref, "source": md.name})
                except:
                    pass
            return {
                "dashboard_type": "references",
                "generated": datetime.now().isoformat(),
                "total_references": len(all_refs),
                "references": all_refs[:100],
            }
        return {"dashboard_type": "references", "note": "Set analysis folder first"}

    def _gen_links_dashboard(self) -> Dict:
        """Generate Links dashboard."""
        master_path = Path(__file__).parent.parent.parent.parent / "global_analytics" / "Master_Sheet" / "MASTER_LINKS.json"
        if master_path.exists():
            with open(master_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return {"dashboard_type": "links", "generated": datetime.now().isoformat(), "data": data}
        return {"dashboard_type": "links", "note": "MASTER_LINKS.json not found"}

    def _gen_timeline_dashboard(self) -> Dict:
        """Generate Timeline dashboard."""
        return {"dashboard_type": "timeline", "generated": datetime.now().isoformat(), "note": "Implement timeline extraction"}

    def _gen_logos_papers_dashboard(self) -> Dict:
        """Generate Logos Papers (P1-P12) progress dashboard."""
        if self.working_folder:
            papers = {}
            for i in range(1, 13):
                pattern = f"*P{i:02d}*" if i < 10 else f"*P{i}*"
                matches = list(self.working_folder.rglob(f"*P{i}*.md")) + list(self.working_folder.rglob(f"*Paper-{i}*.md"))
                if matches:
                    papers[f"P{i}"] = {"status": "found", "files": [m.name for m in matches]}
                else:
                    papers[f"P{i}"] = {"status": "not_found"}

            return {
                "dashboard_type": "logos_papers",
                "generated": datetime.now().isoformat(),
                "papers": papers,
                "found_count": sum(1 for p in papers.values() if p["status"] == "found"),
            }
        return {"dashboard_type": "logos_papers", "note": "Set analysis folder first"}

    def _gen_paper_comparison_dashboard(self) -> Dict:
        """Generate Paper Comparison dashboard."""
        return {"dashboard_type": "paper_comparison", "generated": datetime.now().isoformat(), "note": "Use Compare mode instead"}

    def _gen_validation_dashboard(self) -> Dict:
        """Generate Validation dashboard."""
        return {"dashboard_type": "validation", "generated": datetime.now().isoformat(), "note": "Implement validation checks"}

    def _gen_vault_health_dashboard(self) -> Dict:
        """Generate Vault Health dashboard."""
        if self.working_folder:
            md_files = list(self.working_folder.rglob("*.md"))
            total_words = 0
            broken_links = 0

            for md in md_files[:50]:
                try:
                    content = md.read_text(encoding='utf-8')
                    total_words += len(content.split())
                except:
                    pass

            return {
                "dashboard_type": "vault_health",
                "generated": datetime.now().isoformat(),
                "total_files": len(md_files),
                "total_words": total_words,
                "health_score": 85,  # Placeholder
            }
        return {"dashboard_type": "vault_health", "note": "Set analysis folder first"}

    def _gen_db_dashboard(self) -> Dict:
        """Generate Database dashboard."""
        return {"dashboard_type": "db_dashboard", "generated": datetime.now().isoformat(), "note": "Connect to database first"}

    def _gen_master_equation_dashboard(self) -> Dict:
        """Generate Master Equation (χ) dashboard."""
        return {
            "dashboard_type": "master_equation",
            "generated": datetime.now().isoformat(),
            "equation": "χ = ∭(G·M·E·S·T·K·R·Q·F·C) dx dy dt",
            "domains": ["Gravity", "Matter", "Energy", "Spacetime", "Time", "Knowledge", "Reality", "Quantum", "Faith", "Consciousness"],
            "note": "Implement domain analysis",
        }

    def _gen_lowe_lagrangian_dashboard(self) -> Dict:
        """Generate Lowe Lagrangian dashboard."""
        return {
            "dashboard_type": "lowe_lagrangian",
            "generated": datetime.now().isoformat(),
            "note": "Implement Lagrangian analysis",
        }

    def _gen_all_dashboards(self) -> Dict:
        """Generate ALL dashboards at once."""
        all_results = {}
        dashboard_types = [
            "axioms", "breakthroughs", "coherence", "tags", "mathematics",
            "references", "logos_papers", "vault_health", "master_equation"
        ]

        for dtype in dashboard_types:
            self.results_text.append(f"Generating {dtype}...")
            generator = getattr(self, f"_gen_{dtype}_dashboard", None)
            if generator:
                try:
                    all_results[dtype] = generator()
                except Exception as e:
                    all_results[dtype] = {"error": str(e)}

        return {
            "dashboard_type": "all",
            "generated": datetime.now().isoformat(),
            "dashboards": all_results,
            "count": len(all_results),
        }
