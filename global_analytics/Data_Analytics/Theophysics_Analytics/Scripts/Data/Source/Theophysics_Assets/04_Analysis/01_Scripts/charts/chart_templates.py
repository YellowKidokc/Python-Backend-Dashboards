"""
Highcharts Template Generator
Generates HTML files with Highcharts visualizations from JSON data.

Requires: Highcharts subscription (user has one)

Usage:
    python chart_templates.py --all
    python chart_templates.py --chart word_counts
"""

import json
from pathlib import Path
from typing import Dict, List
import argparse


# Configuration
DATA_PATH = Path(r"D:\THEOPHYSICS_MASTER\00_VAULT_SYSTEM\04_Analysis\07_Data\metrics")
OUTPUT_PATH = Path(r"D:\THEOPHYSICS_MASTER\00_VAULT_SYSTEM\04_Analysis\10_Dashboards\Charts")


# Base HTML template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/highcharts-more.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
    <script src="https://code.highcharts.com/modules/export-data.js"></script>
    <script src="https://code.highcharts.com/modules/accessibility.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 20px;
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 20px;
        }}
        #chart-container {{
            min-height: 400px;
        }}
        .data-selector {{
            margin-bottom: 20px;
            padding: 10px;
            background: #f9f9f9;
            border-radius: 4px;
        }}
        .data-selector label {{
            margin-right: 10px;
            font-weight: 500;
        }}
        .data-selector select {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        .stat-card {{
            background: #f0f7ff;
            padding: 15px 20px;
            border-radius: 8px;
            min-width: 150px;
        }}
        .stat-card .value {{
            font-size: 24px;
            font-weight: bold;
            color: #2563eb;
        }}
        .stat-card .label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <p class="subtitle">{subtitle}</p>

        <div class="data-selector">
            <label for="data-source">Data Source:</label>
            <select id="data-source" onchange="updateChart(this.value)">
                {selector_options}
            </select>
        </div>

        <div id="chart-container"></div>

        <div class="stats" id="stats-container">
            {stats_html}
        </div>
    </div>

    <script>
        // Chart data loaded from JSON
        const chartData = {chart_data};

        // Current chart instance
        let chart;

        // Initialize chart
        function initChart() {{
            {chart_init_code}
        }}

        // Update chart with new data
        function updateChart(source) {{
            {chart_update_code}
        }}

        // Initialize on load
        document.addEventListener('DOMContentLoaded', initChart);
    </script>
</body>
</html>
"""


class HighchartsGenerator:
    """Generates Highcharts HTML files from JSON data."""

    def __init__(self):
        self.data_path = DATA_PATH
        self.output_path = OUTPUT_PATH
        self.output_path.mkdir(parents=True, exist_ok=True)

        # Load data
        self.chart_data = self._load_data('chart_data.json')
        self.paper_metrics = self._load_data('paper_metrics.json')
        self.global_metrics = self._load_data('global_metrics.json')

    def _load_data(self, filename: str) -> Dict:
        """Load JSON data file."""
        filepath = self.data_path / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def generate_word_counts_chart(self) -> str:
        """Generate word counts column chart."""
        data = self.chart_data.get('word_counts', {})

        chart_init = """
            chart = Highcharts.chart('chart-container', {
                chart: { type: 'column' },
                title: { text: 'Word Count by Paper' },
                xAxis: {
                    categories: %s,
                    title: { text: 'Paper' }
                },
                yAxis: {
                    title: { text: 'Word Count' },
                    labels: {
                        formatter: function() {
                            return this.value.toLocaleString();
                        }
                    }
                },
                tooltip: {
                    pointFormat: '<b>{point.y:,.0f}</b> words'
                },
                plotOptions: {
                    column: {
                        colorByPoint: true,
                        dataLabels: {
                            enabled: true,
                            formatter: function() {
                                return this.y.toLocaleString();
                            }
                        }
                    }
                },
                series: [{
                    name: 'Words',
                    data: %s
                }],
                credits: { enabled: false }
            });
        """ % (json.dumps(data.get('categories', [])), json.dumps(data.get('series', [{}])[0].get('data', [])))

        chart_update = """
            // Update logic for different data sources
            console.log('Selected:', source);
        """

        selector_options = '<option value="all">All Papers</option>'

        stats_html = """
            <div class="stat-card">
                <div class="value">%s</div>
                <div class="label">Total Words</div>
            </div>
            <div class="stat-card">
                <div class="value">%s</div>
                <div class="label">Total Pages</div>
            </div>
            <div class="stat-card">
                <div class="value">%s</div>
                <div class="label">Avg Words/Paper</div>
            </div>
        """ % (
            f"{self.global_metrics.get('totals', {}).get('total_words', 0):,}",
            f"{self.global_metrics.get('totals', {}).get('total_pages', 0):,}",
            f"{self.global_metrics.get('averages', {}).get('avg_words_per_paper', 0):,.0f}"
        )

        return HTML_TEMPLATE.format(
            title="Word Counts Analysis",
            subtitle="Total word count across all 12 Logos Papers",
            selector_options=selector_options,
            stats_html=stats_html,
            chart_data=json.dumps(self.chart_data),
            chart_init_code=chart_init,
            chart_update_code=chart_update
        )

    def generate_content_comparison_chart(self) -> str:
        """Generate stacked bar chart for content metrics."""
        data = self.chart_data.get('content_comparison', {})

        chart_init = """
            chart = Highcharts.chart('chart-container', {
                chart: { type: 'bar' },
                title: { text: 'Content Breakdown by Paper' },
                xAxis: {
                    categories: %s,
                    title: { text: 'Paper' }
                },
                yAxis: {
                    min: 0,
                    title: { text: 'Count' },
                    stackLabels: { enabled: true }
                },
                legend: {
                    reversed: true
                },
                plotOptions: {
                    series: {
                        stacking: 'normal',
                        dataLabels: {
                            enabled: true
                        }
                    }
                },
                series: %s,
                credits: { enabled: false }
            });
        """ % (json.dumps(data.get('categories', [])), json.dumps(data.get('series', [])))

        chart_update = "console.log('Selected:', source);"
        selector_options = '<option value="all">All Papers</option>'

        totals = self.global_metrics.get('totals', {})
        stats_html = """
            <div class="stat-card">
                <div class="value">%s</div>
                <div class="label">Definitions</div>
            </div>
            <div class="stat-card">
                <div class="value">%s</div>
                <div class="label">Axioms</div>
            </div>
            <div class="stat-card">
                <div class="value">%s</div>
                <div class="label">Claims</div>
            </div>
            <div class="stat-card">
                <div class="value">%s</div>
                <div class="label">Equations</div>
            </div>
        """ % (
            totals.get('total_definitions', 0),
            totals.get('total_axioms', 0),
            totals.get('total_claims', 0),
            totals.get('total_equations', 0)
        )

        return HTML_TEMPLATE.format(
            title="Content Breakdown",
            subtitle="Definitions, Axioms, Claims, and Equations across all papers",
            selector_options=selector_options,
            stats_html=stats_html,
            chart_data=json.dumps(self.chart_data),
            chart_init_code=chart_init,
            chart_update_code=chart_update
        )

    def generate_domain_radar_chart(self) -> str:
        """Generate radar chart for domain distribution."""
        data = self.chart_data.get('domain_distribution', {})

        # Convert to radar format
        domains = self.global_metrics.get('domain_averages', {})
        categories = list(domains.keys())
        values = list(domains.values())

        chart_init = """
            chart = Highcharts.chart('chart-container', {
                chart: {
                    polar: true,
                    type: 'area'
                },
                title: { text: 'Domain Distribution (Global Average)' },
                pane: {
                    size: '80%%',
                    startAngle: 0
                },
                xAxis: {
                    categories: %s,
                    tickmarkPlacement: 'on',
                    lineWidth: 0
                },
                yAxis: {
                    gridLineInterpolation: 'polygon',
                    lineWidth: 0,
                    min: 0,
                    max: 1
                },
                tooltip: {
                    shared: true,
                    pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:.2f}</b><br/>'
                },
                legend: {
                    align: 'right',
                    verticalAlign: 'middle',
                    layout: 'vertical'
                },
                series: [{
                    name: 'Global Average',
                    data: %s,
                    pointPlacement: 'on',
                    fillOpacity: 0.3
                }],
                credits: { enabled: false }
            });
        """ % (json.dumps(categories), json.dumps(values))

        chart_update = "console.log('Selected:', source);"

        # Add paper options to selector
        paper_options = '<option value="global">Global Average</option>'
        if self.paper_metrics:
            for paper in self.paper_metrics:
                paper_options += f'<option value="{paper["paper_id"]}">{paper["paper_id"]} - {paper["paper_name"]}</option>'

        stats_html = """
            <div class="stat-card">
                <div class="value">10</div>
                <div class="label">Domains Tracked</div>
            </div>
            <div class="stat-card">
                <div class="value">G-M-E-S-T</div>
                <div class="label">Physics Bridge</div>
            </div>
            <div class="stat-card">
                <div class="value">K-R-Q-F-C</div>
                <div class="label">Theology Bridge</div>
            </div>
        """

        return HTML_TEMPLATE.format(
            title="Domain Analysis",
            subtitle="10-domain coverage profile (G=Grace, M=Mass, E=Energy, S=Entropy, T=Time, K=Knowledge, R=Revelation, Q=Quantum, F=Faith, C=Coherence)",
            selector_options=paper_options,
            stats_html=stats_html,
            chart_data=json.dumps(self.chart_data),
            chart_init_code=chart_init,
            chart_update_code=chart_update
        )

    def generate_complexity_chart(self) -> str:
        """Generate line chart for complexity metrics."""
        data = self.chart_data.get('complexity_trend', {})

        chart_init = """
            chart = Highcharts.chart('chart-container', {
                chart: { type: 'line' },
                title: { text: 'Reading Complexity Across Papers' },
                xAxis: {
                    categories: %s,
                    title: { text: 'Paper' }
                },
                yAxis: [{
                    title: { text: 'Reading Ease (0-100)' },
                    min: 0,
                    max: 100
                }, {
                    title: { text: 'Grade Level' },
                    opposite: true
                }],
                tooltip: {
                    shared: true
                },
                plotOptions: {
                    line: {
                        dataLabels: { enabled: true },
                        marker: { enabled: true }
                    }
                },
                series: [{
                    name: 'Flesch Reading Ease',
                    data: %s,
                    yAxis: 0
                }, {
                    name: 'Grade Level',
                    data: %s,
                    yAxis: 1
                }],
                credits: { enabled: false }
            });
        """ % (
            json.dumps(data.get('categories', [])),
            json.dumps(data.get('series', [{}])[0].get('data', []) if data.get('series') else []),
            json.dumps(data.get('series', [{}, {}])[1].get('data', []) if len(data.get('series', [])) > 1 else [])
        )

        chart_update = "console.log('Selected:', source);"
        selector_options = '<option value="all">All Papers</option>'

        avgs = self.global_metrics.get('averages', {})
        stats_html = """
            <div class="stat-card">
                <div class="value">%s</div>
                <div class="label">Avg Reading Ease</div>
            </div>
            <div class="stat-card">
                <div class="value">Grade %s</div>
                <div class="label">Avg Grade Level</div>
            </div>
        """ % (
            avgs.get('avg_reading_ease', '-'),
            avgs.get('avg_grade_level', '-')
        )

        return HTML_TEMPLATE.format(
            title="Complexity Analysis",
            subtitle="Flesch Reading Ease and Grade Level across all papers",
            selector_options=selector_options,
            stats_html=stats_html,
            chart_data=json.dumps(self.chart_data),
            chart_init_code=chart_init,
            chart_update_code=chart_update
        )

    def generate_all_charts(self):
        """Generate all chart HTML files."""
        charts = [
            ('chart_word_counts.html', self.generate_word_counts_chart),
            ('chart_content_comparison.html', self.generate_content_comparison_chart),
            ('chart_domain_radar.html', self.generate_domain_radar_chart),
            ('chart_complexity.html', self.generate_complexity_chart),
        ]

        for filename, generator in charts:
            try:
                html = generator()
                output_file = self.output_path / filename
                output_file.write_text(html, encoding='utf-8')
                print(f"Generated: {filename}")
            except Exception as e:
                print(f"Error generating {filename}: {e}")

        # Generate index
        self._generate_index(charts)

    def _generate_index(self, charts: List):
        """Generate index file for all charts."""
        index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Theophysics Charts Gallery</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        h1 { color: #333; }
        .chart-list {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-top: 30px;
        }
        .chart-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            transition: box-shadow 0.2s;
        }
        .chart-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .chart-card h3 {
            margin: 0 0 10px 0;
            color: #2563eb;
        }
        .chart-card p {
            color: #666;
            font-size: 14px;
            margin: 0;
        }
        .chart-card a {
            text-decoration: none;
            color: inherit;
        }
    </style>
</head>
<body>
    <h1>Theophysics Charts Gallery</h1>
    <p>Highcharts visualizations generated from Logos Papers metrics.</p>

    <div class="chart-list">
        <div class="chart-card">
            <a href="chart_word_counts.html">
                <h3>Word Counts</h3>
                <p>Column chart showing word count per paper</p>
            </a>
        </div>
        <div class="chart-card">
            <a href="chart_content_comparison.html">
                <h3>Content Breakdown</h3>
                <p>Stacked bar chart of definitions, axioms, claims, equations</p>
            </a>
        </div>
        <div class="chart-card">
            <a href="chart_domain_radar.html">
                <h3>Domain Distribution</h3>
                <p>Radar chart showing 10-domain coverage</p>
            </a>
        </div>
        <div class="chart-card">
            <a href="chart_complexity.html">
                <h3>Complexity Analysis</h3>
                <p>Line chart of reading ease and grade level</p>
            </a>
        </div>
    </div>

    <hr style="margin: 40px 0;">
    <p style="color: #999; font-size: 12px;">
        Generated from: 07_Data/metrics/chart_data.json<br>
        Requires: Highcharts subscription
    </p>
</body>
</html>
"""

        index_file = self.output_path / '_Charts_Index.html'
        index_file.write_text(index_html, encoding='utf-8')
        print(f"Generated: _Charts_Index.html")


def main():
    parser = argparse.ArgumentParser(description='Generate Highcharts HTML files')
    parser.add_argument('--all', action='store_true', help='Generate all charts')
    parser.add_argument('--chart', help='Generate specific chart (word_counts, content, domain, complexity)')

    args = parser.parse_args()

    generator = HighchartsGenerator()

    if args.all or not args.chart:
        print("Generating all Highcharts files...")
        generator.generate_all_charts()
        print(f"\nCharts saved to: {OUTPUT_PATH}")
    elif args.chart:
        chart_map = {
            'word_counts': ('chart_word_counts.html', generator.generate_word_counts_chart),
            'content': ('chart_content_comparison.html', generator.generate_content_comparison_chart),
            'domain': ('chart_domain_radar.html', generator.generate_domain_radar_chart),
            'complexity': ('chart_complexity.html', generator.generate_complexity_chart),
        }

        if args.chart in chart_map:
            filename, func = chart_map[args.chart]
            html = func()
            output_file = OUTPUT_PATH / filename
            output_file.write_text(html, encoding='utf-8')
            print(f"Generated: {filename}")
        else:
            print(f"Unknown chart: {args.chart}")
            print(f"Available: {', '.join(chart_map.keys())}")


if __name__ == '__main__':
    main()
