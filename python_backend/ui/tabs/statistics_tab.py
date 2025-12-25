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
        self.mode_combo.currentIndexChanged.connect(self._on_mode_changed)
        mode_layout.addWidget(self.mode_combo)

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
