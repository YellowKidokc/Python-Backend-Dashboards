"""
Highcharts HTML to PNG Renderer
Renders Highcharts HTML files to PNG images using headless browser.

Requirements:
- playwright or selenium
- Or use Highcharts export server (if available)
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def check_playwright():
    """Check if playwright is installed."""
    try:
        import playwright
        return True
    except ImportError:
        return False


def install_playwright():
    """Install playwright and browsers."""
    print("Installing playwright...")
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    print("✅ Playwright installed")


def render_html_to_png(html_path: Path, output_path: Path, width: int = 1200, height: int = 800) -> bool:
    """
    Render HTML file to PNG using playwright.
    
    Args:
        html_path: Path to HTML file
        output_path: Path to save PNG
        width: Image width in pixels
        height: Image height in pixels
    
    Returns:
        True if successful, False otherwise
    """
    try:
        from playwright.sync_api import sync_playwright
        
        html_path = Path(html_path).resolve()
        output_path = Path(output_path).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': width, 'height': height})
            
            # Load HTML file - convert Windows path to file:// URL
            file_url = html_path.as_uri()
            page.goto(file_url)
            
            # Wait for chart to render (Highcharts needs time)
            # Wait for Highcharts to load and render
            page.wait_for_load_state('networkidle')  # Wait for network to be idle
            page.wait_for_timeout(3000)  # Extra 3 seconds for chart rendering
            
            # Take screenshot
            page.screenshot(path=str(output_path), full_page=False)
            
            browser.close()
        
        return True
    
    except ImportError:
        print("❌ Playwright not installed. Install with: pip install playwright && playwright install chromium")
        return False
    except Exception as e:
        print(f"❌ Error rendering {html_path}: {e}")
        return False


def render_all_charts_in_paper(paper_path: Path) -> List[Path]:
    """
    Find and render all Highcharts HTML files in a paper's charts folder.
    
    Args:
        paper_path: Path to paper folder (e.g., P01-Logos-Principle)
    
    Returns:
        List of rendered PNG paths
    """
    charts_folder = paper_path / "charts"
    assets_images = paper_path / "_Assets" / "Images"
    
    if not charts_folder.exists():
        print(f"⚠️  No charts folder in {paper_path.name}")
        return []
    
    assets_images.mkdir(parents=True, exist_ok=True)
    
    html_files = list(charts_folder.glob("*.html"))
    rendered = []
    
    for html_file in html_files:
        # Generate PNG filename
        png_name = html_file.stem + ".png"
        png_path = assets_images / png_name
        
        print(f"Rendering {html_file.name}...")
        if render_html_to_png(html_file, png_path):
            rendered.append(png_path)
            print(f"  ✅ Saved to {png_path}")
        else:
            print(f"  ❌ Failed to render {html_file.name}")
    
    return rendered


def render_all_papers(base_path: Path) -> dict:
    """
    Render all Highcharts in all papers.
    
    Args:
        base_path: Path to COMPLETE_LOGOS_PAPERS_FINAL folder
    
    Returns:
        Dictionary mapping paper names to list of rendered PNGs
    """
    results = {}
    
    # Find all paper folders
    paper_folders = [p for p in base_path.iterdir() if p.is_dir() and p.name.startswith("P") and p.name[1:3].isdigit()]
    
    for paper_folder in sorted(paper_folders):
        paper_id = paper_folder.name
        print(f"\n📊 Processing {paper_id}...")
        
        rendered = render_all_charts_in_paper(paper_folder)
        results[paper_id] = rendered
        
        if rendered:
            print(f"  ✅ Rendered {len(rendered)} charts")
        else:
            print(f"  ℹ️  No charts found or rendered")
    
    return results


def main():
    """CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Render Highcharts HTML to PNG')
    parser.add_argument('--paper', help='Paper ID (e.g., P01) or "all" for all papers')
    parser.add_argument('--html', help='Single HTML file to render')
    parser.add_argument('--output', help='Output PNG path (for single file)')
    parser.add_argument('--install', action='store_true', help='Install playwright')
    
    args = parser.parse_args()
    
    if args.install:
        install_playwright()
        return
    
    if not check_playwright():
        print("❌ Playwright not installed.")
        print("Install with: python render_highcharts.py --install")
        return
    
    base_path = Path(r"D:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL")
    
    if args.html:
        # Render single file
        html_path = Path(args.html)
        output_path = Path(args.output) if args.output else html_path.with_suffix('.png')
        render_html_to_png(html_path, output_path)
    
    elif args.paper == "all":
        # Render all papers
        results = render_all_papers(base_path)
        print(f"\n✅ Complete! Rendered charts in {len(results)} papers")
    
    elif args.paper:
        # Render specific paper
        paper_id = args.paper.replace("P", "").zfill(2)
        paper_folders = list(base_path.glob(f"P{paper_id}-*"))
        if paper_folders:
            render_all_charts_in_paper(paper_folders[0])
        else:
            print(f"❌ Paper {args.paper} not found")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

