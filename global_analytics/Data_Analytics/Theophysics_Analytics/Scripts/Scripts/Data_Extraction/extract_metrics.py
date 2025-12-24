"""
Paper Metrics Extraction Script
Extracts core metrics from papers for Highcharts visualization.

Output: JSON files ready for Highcharts consumption.

Usage:
    python extract_metrics.py --paper P01
    python extract_metrics.py --all
    python extract_metrics.py --global
"""

import json
import re
import math
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from collections import Counter
import argparse


# Configuration
PAPERS_PATH = Path(r"D:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL")
OUTPUT_PATH = Path(r"D:\THEOPHYSICS_MASTER\00_VAULT_SYSTEM\04_Analysis\07_Data\metrics")


@dataclass
class BasicMetrics:
    """Core text metrics."""
    word_count: int = 0
    unique_words: int = 0
    character_count: int = 0
    paragraph_count: int = 0
    sentence_count: int = 0
    page_count_estimate: int = 0
    words_per_page: float = 0.0
    average_sentence_length: float = 0.0
    reading_time_minutes: int = 0


@dataclass
class ContentMetrics:
    """Content-specific metrics."""
    definitions_count: int = 0
    axioms_count: int = 0
    claims_count: int = 0
    equations_count: int = 0
    references_count: int = 0
    internal_links_count: int = 0
    external_links_count: int = 0
    headers_count: int = 0
    tables_count: int = 0
    code_blocks_count: int = 0


@dataclass
class ComplexityMetrics:
    """Text complexity metrics."""
    flesch_reading_ease: float = 0.0
    flesch_kincaid_grade: float = 0.0
    vocabulary_richness: float = 0.0
    technical_term_density: float = 0.0
    average_word_length: float = 0.0


@dataclass
class DomainMetrics:
    """Domain contribution scores."""
    G: float = 0.0  # Grace
    M: float = 0.0  # Mass/Moral
    E: float = 0.0  # Energy
    S: float = 0.0  # Entropy
    T: float = 0.0  # Time/Truth
    K: float = 0.0  # Knowledge
    R: float = 0.0  # Revelation
    Q: float = 0.0  # Quantum
    F: float = 0.0  # Faith
    C: float = 0.0  # Coherence


@dataclass
class PaperMetrics:
    """Complete metrics for a single paper."""
    paper_id: str
    paper_name: str
    file_path: str
    basic: BasicMetrics
    content: ContentMetrics
    complexity: ComplexityMetrics
    domains: DomainMetrics


# Domain keywords for detection
DOMAIN_KEYWORDS = {
    'G': ['grace', 'gift', 'unmerited', 'favor', 'divine love', 'blessing', 'mercy', 'forgiveness'],
    'M': ['mass', 'momentum', 'moral', 'weight', 'gravity', 'matter', 'inertia', 'substance'],
    'E': ['energy', 'electromagnetic', 'photon', 'light', 'radiation', 'field', 'force', 'power'],
    'S': ['entropy', 'sin', 'disorder', 'decay', 'death', 'chaos', 'thermodynamic', 'probability'],
    'T': ['time', 'truth', 'temporal', 'eternal', 'duration', 'moment', 'chronology', 'eschatology'],
    'K': ['knowledge', 'epistemology', 'knowing', 'understanding', 'cognition', 'information', 'data'],
    'R': ['revelation', 'disclosed', 'manifest', 'appear', 'unveil', 'prophecy', 'scripture', 'word'],
    'Q': ['quantum', 'wave function', 'superposition', 'entanglement', 'collapse', 'measurement', 'observer'],
    'F': ['faith', 'trust', 'belief', 'confidence', 'assurance', 'hope', 'fidelity'],
    'C': ['coherence', 'consciousness', 'awareness', 'mind', 'integration', 'unity', 'wholeness', 'order']
}

# Technical terms for density calculation
TECHNICAL_TERMS = [
    'lagrangian', 'hamiltonian', 'tensor', 'manifold', 'isomorphism', 'homomorphism',
    'eigenvalue', 'hermitian', 'unitary', 'hilbert', 'banach', 'topology',
    'logos', 'trinity', 'incarnation', 'resurrection', 'atonement', 'eschatology',
    'theophysics', 'panpsychism', 'dualism', 'monism', 'ontology', 'epistemology',
    'decoherence', 'superposition', 'entanglement', 'wavefunction', 'quantum',
    'negentropy', 'thermodynamics', 'relativity', 'spacetime', 'geodesic'
]


class MetricsExtractor:
    """Extracts metrics from paper markdown files."""

    def __init__(self):
        self.papers_path = PAPERS_PATH
        self.output_path = OUTPUT_PATH
        self.output_path.mkdir(parents=True, exist_ok=True)

    def extract_paper_metrics(self, paper_folder: Path) -> Optional[PaperMetrics]:
        """Extract metrics from a single paper folder."""
        # Find canonical file
        canonical_files = list(paper_folder.glob("*CANONICAL*.md"))
        if not canonical_files:
            print(f"No canonical file found in {paper_folder}")
            return None

        paper_file = canonical_files[0]

        # Read content
        try:
            content = paper_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading {paper_file}: {e}")
            return None

        # Extract paper ID from folder name
        folder_name = paper_folder.name
        paper_id_match = re.match(r'Paper\s*(\d+)', folder_name)
        paper_id = f"P{paper_id_match.group(1).zfill(2)}" if paper_id_match else folder_name

        # Extract paper name
        paper_name = folder_name.split(' - ')[-1] if ' - ' in folder_name else folder_name

        # Calculate metrics
        basic = self._calculate_basic_metrics(content)
        content_metrics = self._calculate_content_metrics(content)
        complexity = self._calculate_complexity_metrics(content)
        domains = self._calculate_domain_metrics(content)

        return PaperMetrics(
            paper_id=paper_id,
            paper_name=paper_name,
            file_path=str(paper_file),
            basic=basic,
            content=content_metrics,
            complexity=complexity,
            domains=domains
        )

    def _calculate_basic_metrics(self, content: str) -> BasicMetrics:
        """Calculate basic text metrics."""
        # Clean content (remove markdown formatting for accurate counts)
        clean_content = self._clean_markdown(content)

        # Word count
        words = clean_content.split()
        word_count = len(words)

        # Unique words
        unique_words = len(set(w.lower() for w in words))

        # Character count
        character_count = len(clean_content)

        # Paragraph count (double newlines)
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        paragraph_count = len(paragraphs)

        # Sentence count
        sentences = re.split(r'[.!?]+', clean_content)
        sentences = [s for s in sentences if s.strip()]
        sentence_count = len(sentences)

        # Page estimate (approx 300 words per page)
        page_count = max(1, word_count // 300)

        # Words per page
        words_per_page = word_count / page_count if page_count > 0 else 0

        # Average sentence length
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0

        # Reading time (200 words per minute average)
        reading_time = max(1, word_count // 200)

        return BasicMetrics(
            word_count=word_count,
            unique_words=unique_words,
            character_count=character_count,
            paragraph_count=paragraph_count,
            sentence_count=sentence_count,
            page_count_estimate=page_count,
            words_per_page=round(words_per_page, 1),
            average_sentence_length=round(avg_sentence_length, 1),
            reading_time_minutes=reading_time
        )

    def _calculate_content_metrics(self, content: str) -> ContentMetrics:
        """Calculate content-specific metrics."""
        # Definitions (patterns: "defined as", "Definition:", "**Term**")
        definitions = len(re.findall(
            r'(?:defined as|Definition:|is defined|we define|\*\*[A-Z][^*]+\*\*\s*[-:])',
            content, re.IGNORECASE
        ))

        # Axioms (patterns: "Axiom", "Law", "Principle")
        axioms = len(re.findall(
            r'(?:Axiom|Law|Principle|Postulate)\s*\d*\s*[:.]',
            content, re.IGNORECASE
        ))

        # Claims (patterns: "we claim", "we propose", "we argue")
        claims = len(re.findall(
            r'(?:we claim|we propose|we argue|we assert|we suggest|it follows that)',
            content, re.IGNORECASE
        ))

        # Equations (LaTeX patterns)
        equations = len(re.findall(r'\$[^$]+\$|\\\[.+?\\\]|\\\(.+?\\\)', content))

        # References (citation patterns)
        references = len(re.findall(r'\[\d+\]|\([A-Z][a-z]+,?\s*\d{4}\)', content))

        # Internal links (Obsidian [[links]])
        internal_links = len(re.findall(r'\[\[[^\]]+\]\]', content))

        # External links (URLs)
        external_links = len(re.findall(r'https?://[^\s\)]+', content))

        # Headers
        headers = len(re.findall(r'^#{1,6}\s+', content, re.MULTILINE))

        # Tables
        tables = len(re.findall(r'\|[^|]+\|', content)) // 3  # Rough estimate

        # Code blocks
        code_blocks = len(re.findall(r'```', content)) // 2

        return ContentMetrics(
            definitions_count=definitions,
            axioms_count=axioms,
            claims_count=claims,
            equations_count=equations,
            references_count=references,
            internal_links_count=internal_links,
            external_links_count=external_links,
            headers_count=headers,
            tables_count=tables,
            code_blocks_count=code_blocks
        )

    def _calculate_complexity_metrics(self, content: str) -> ComplexityMetrics:
        """Calculate text complexity metrics."""
        clean_content = self._clean_markdown(content)
        words = clean_content.split()

        if not words:
            return ComplexityMetrics()

        # Syllable counting (simplified)
        def count_syllables(word):
            word = word.lower()
            count = 0
            vowels = 'aeiouy'
            prev_char_was_vowel = False
            for char in word:
                is_vowel = char in vowels
                if is_vowel and not prev_char_was_vowel:
                    count += 1
                prev_char_was_vowel = is_vowel
            if word.endswith('e'):
                count -= 1
            return max(1, count)

        total_syllables = sum(count_syllables(w) for w in words)
        word_count = len(words)

        # Sentence count
        sentences = re.split(r'[.!?]+', clean_content)
        sentences = [s for s in sentences if s.strip()]
        sentence_count = max(1, len(sentences))

        # Flesch Reading Ease
        flesch_reading_ease = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (total_syllables / word_count)
        flesch_reading_ease = max(0, min(100, flesch_reading_ease))

        # Flesch-Kincaid Grade Level
        flesch_kincaid = 0.39 * (word_count / sentence_count) + 11.8 * (total_syllables / word_count) - 15.59
        flesch_kincaid = max(0, flesch_kincaid)

        # Vocabulary richness (type-token ratio)
        unique_words = len(set(w.lower() for w in words))
        vocabulary_richness = unique_words / word_count

        # Technical term density
        content_lower = clean_content.lower()
        tech_term_count = sum(1 for term in TECHNICAL_TERMS if term in content_lower)
        technical_density = tech_term_count / (word_count / 100)  # Per 100 words

        # Average word length
        avg_word_length = sum(len(w) for w in words) / word_count

        return ComplexityMetrics(
            flesch_reading_ease=round(flesch_reading_ease, 1),
            flesch_kincaid_grade=round(flesch_kincaid, 1),
            vocabulary_richness=round(vocabulary_richness, 3),
            technical_term_density=round(technical_density, 2),
            average_word_length=round(avg_word_length, 1)
        )

    def _calculate_domain_metrics(self, content: str) -> DomainMetrics:
        """Calculate domain contribution scores."""
        content_lower = content.lower()
        word_count = len(content_lower.split())

        domain_scores = {}

        for domain, keywords in DOMAIN_KEYWORDS.items():
            # Count keyword occurrences
            count = 0
            for keyword in keywords:
                count += len(re.findall(rf'\b{re.escape(keyword)}\b', content_lower))

            # Normalize to 0-1 scale (per 1000 words)
            normalized = min(1.0, (count / (word_count / 1000)) / 10)
            domain_scores[domain] = round(normalized, 2)

        return DomainMetrics(**domain_scores)

    def _clean_markdown(self, content: str) -> str:
        """Remove markdown formatting for accurate text analysis."""
        # Remove YAML frontmatter
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # Remove code blocks
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        content = re.sub(r'`[^`]+`', '', content)

        # Remove links but keep text
        content = re.sub(r'\[\[([^\]|]+)\|?[^\]]*\]\]', r'\1', content)
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)

        # Remove headers markers
        content = re.sub(r'^#+\s*', '', content, flags=re.MULTILINE)

        # Remove bold/italic
        content = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', content)
        content = re.sub(r'_{1,2}([^_]+)_{1,2}', r'\1', content)

        # Remove LaTeX
        content = re.sub(r'\$[^$]+\$', '', content)
        content = re.sub(r'\\\[.+?\\\]', '', content, flags=re.DOTALL)

        # Remove extra whitespace
        content = ' '.join(content.split())

        return content

    def extract_all_papers(self) -> List[PaperMetrics]:
        """Extract metrics from all papers."""
        all_metrics = []

        # Find all paper folders
        paper_folders = sorted([
            f for f in self.papers_path.iterdir()
            if f.is_dir() and f.name.startswith('Paper')
        ])

        print(f"Found {len(paper_folders)} paper folders")

        for folder in paper_folders:
            print(f"Processing: {folder.name}")
            metrics = self.extract_paper_metrics(folder)
            if metrics:
                all_metrics.append(metrics)

        return all_metrics

    def calculate_global_metrics(self, paper_metrics: List[PaperMetrics]) -> Dict:
        """Calculate aggregate metrics across all papers."""
        if not paper_metrics:
            return {}

        # Aggregate totals
        totals = {
            'total_words': sum(p.basic.word_count for p in paper_metrics),
            'total_unique_words': len(set(
                w for p in paper_metrics
                for w in Path(p.file_path).read_text(encoding='utf-8').lower().split()
            )) if paper_metrics else 0,
            'total_pages': sum(p.basic.page_count_estimate for p in paper_metrics),
            'total_definitions': sum(p.content.definitions_count for p in paper_metrics),
            'total_axioms': sum(p.content.axioms_count for p in paper_metrics),
            'total_claims': sum(p.content.claims_count for p in paper_metrics),
            'total_equations': sum(p.content.equations_count for p in paper_metrics),
            'total_references': sum(p.content.references_count for p in paper_metrics),
        }

        n = len(paper_metrics)

        # Aggregate averages
        averages = {
            'avg_words_per_paper': round(totals['total_words'] / n, 0),
            'avg_pages_per_paper': round(totals['total_pages'] / n, 1),
            'avg_definitions_per_paper': round(totals['total_definitions'] / n, 1),
            'avg_reading_ease': round(sum(p.complexity.flesch_reading_ease for p in paper_metrics) / n, 1),
            'avg_grade_level': round(sum(p.complexity.flesch_kincaid_grade for p in paper_metrics) / n, 1),
        }

        # Aggregate domain scores
        domain_averages = {}
        for domain in ['G', 'M', 'E', 'S', 'T', 'K', 'R', 'Q', 'F', 'C']:
            values = [getattr(p.domains, domain) for p in paper_metrics]
            domain_averages[domain] = round(sum(values) / n, 2)

        return {
            'scope': 'global',
            'papers_analyzed': n,
            'totals': totals,
            'averages': averages,
            'domain_averages': domain_averages
        }

    def save_metrics(self, paper_metrics: List[PaperMetrics], global_metrics: Dict):
        """Save metrics to JSON files."""
        # Save individual paper metrics
        paper_data = [asdict(p) for p in paper_metrics]

        with open(self.output_path / 'paper_metrics.json', 'w', encoding='utf-8') as f:
            json.dump(paper_data, f, indent=2)

        # Save global metrics
        with open(self.output_path / 'global_metrics.json', 'w', encoding='utf-8') as f:
            json.dump(global_metrics, f, indent=2)

        # Generate Highcharts-ready data
        chart_data = self._generate_chart_data(paper_metrics, global_metrics)
        with open(self.output_path / 'chart_data.json', 'w', encoding='utf-8') as f:
            json.dump(chart_data, f, indent=2)

        print(f"\nMetrics saved to: {self.output_path}")
        print(f"  - paper_metrics.json ({len(paper_metrics)} papers)")
        print(f"  - global_metrics.json")
        print(f"  - chart_data.json (Highcharts-ready)")

    def _generate_chart_data(self, paper_metrics: List[PaperMetrics], global_metrics: Dict) -> Dict:
        """Generate pre-formatted data for Highcharts."""
        papers = sorted(paper_metrics, key=lambda p: p.paper_id)

        return {
            # Bar chart: Word counts by paper
            'word_counts': {
                'categories': [p.paper_id for p in papers],
                'series': [{
                    'name': 'Word Count',
                    'data': [p.basic.word_count for p in papers]
                }]
            },

            # Bar chart: Content metrics comparison
            'content_comparison': {
                'categories': [p.paper_id for p in papers],
                'series': [
                    {'name': 'Definitions', 'data': [p.content.definitions_count for p in papers]},
                    {'name': 'Axioms', 'data': [p.content.axioms_count for p in papers]},
                    {'name': 'Claims', 'data': [p.content.claims_count for p in papers]},
                    {'name': 'Equations', 'data': [p.content.equations_count for p in papers]}
                ]
            },

            # Pie chart: Domain distribution (global average)
            'domain_distribution': {
                'data': [
                    {'name': 'Grace (G)', 'y': global_metrics['domain_averages']['G']},
                    {'name': 'Mass (M)', 'y': global_metrics['domain_averages']['M']},
                    {'name': 'Energy (E)', 'y': global_metrics['domain_averages']['E']},
                    {'name': 'Entropy (S)', 'y': global_metrics['domain_averages']['S']},
                    {'name': 'Time (T)', 'y': global_metrics['domain_averages']['T']},
                    {'name': 'Knowledge (K)', 'y': global_metrics['domain_averages']['K']},
                    {'name': 'Revelation (R)', 'y': global_metrics['domain_averages']['R']},
                    {'name': 'Quantum (Q)', 'y': global_metrics['domain_averages']['Q']},
                    {'name': 'Faith (F)', 'y': global_metrics['domain_averages']['F']},
                    {'name': 'Coherence (C)', 'y': global_metrics['domain_averages']['C']}
                ]
            },

            # Radar chart: Per-paper domain profiles
            'domain_profiles': {
                'categories': ['G', 'M', 'E', 'S', 'T', 'K', 'R', 'Q', 'F', 'C'],
                'series': [
                    {
                        'name': p.paper_id,
                        'data': [
                            p.domains.G, p.domains.M, p.domains.E, p.domains.S, p.domains.T,
                            p.domains.K, p.domains.R, p.domains.Q, p.domains.F, p.domains.C
                        ]
                    }
                    for p in papers
                ]
            },

            # Line chart: Complexity across papers
            'complexity_trend': {
                'categories': [p.paper_id for p in papers],
                'series': [
                    {'name': 'Reading Ease', 'data': [p.complexity.flesch_reading_ease for p in papers]},
                    {'name': 'Grade Level', 'data': [p.complexity.flesch_kincaid_grade for p in papers]}
                ]
            },

            # Bar chart: Page counts
            'page_counts': {
                'categories': [p.paper_id for p in papers],
                'series': [{
                    'name': 'Pages',
                    'data': [p.basic.page_count_estimate for p in papers]
                }]
            },

            # Summary stats for display
            'summary': {
                'total_words': global_metrics['totals']['total_words'],
                'total_pages': global_metrics['totals']['total_pages'],
                'total_definitions': global_metrics['totals']['total_definitions'],
                'total_axioms': global_metrics['totals']['total_axioms'],
                'papers_count': global_metrics['papers_analyzed'],
                'avg_reading_ease': global_metrics['averages']['avg_reading_ease'],
                'avg_grade_level': global_metrics['averages']['avg_grade_level']
            }
        }


def main():
    parser = argparse.ArgumentParser(description='Extract metrics from Theophysics papers')
    parser.add_argument('--paper', help='Extract metrics for specific paper (e.g., P01)')
    parser.add_argument('--all', action='store_true', help='Extract metrics for all papers')
    parser.add_argument('--global-only', action='store_true', help='Only calculate global metrics from existing data')

    args = parser.parse_args()

    extractor = MetricsExtractor()

    if args.paper:
        # Single paper
        paper_folder = PAPERS_PATH / f"Paper {args.paper[1:]} *"  # P01 -> "Paper 1 *"
        folders = list(PAPERS_PATH.glob(f"Paper {args.paper[1:].lstrip('0')} *"))
        if folders:
            metrics = extractor.extract_paper_metrics(folders[0])
            if metrics:
                print(f"\nMetrics for {metrics.paper_id}:")
                print(f"  Words: {metrics.basic.word_count}")
                print(f"  Pages: {metrics.basic.page_count_estimate}")
                print(f"  Definitions: {metrics.content.definitions_count}")
                print(f"  Reading Level: Grade {metrics.complexity.flesch_kincaid_grade}")
        else:
            print(f"Paper folder not found for {args.paper}")

    elif args.all or not (args.paper or args.global_only):
        # All papers
        print("Extracting metrics from all papers...")
        paper_metrics = extractor.extract_all_papers()

        print("\nCalculating global metrics...")
        global_metrics = extractor.calculate_global_metrics(paper_metrics)

        extractor.save_metrics(paper_metrics, global_metrics)

        # Print summary
        print("\n" + "="*50)
        print("EXTRACTION SUMMARY")
        print("="*50)
        print(f"Papers analyzed: {len(paper_metrics)}")
        print(f"Total words: {global_metrics['totals']['total_words']:,}")
        print(f"Total pages: {global_metrics['totals']['total_pages']:,}")
        print(f"Total definitions: {global_metrics['totals']['total_definitions']}")
        print(f"Total axioms: {global_metrics['totals']['total_axioms']}")
        print(f"Average reading level: Grade {global_metrics['averages']['avg_grade_level']}")


if __name__ == '__main__':
    main()
