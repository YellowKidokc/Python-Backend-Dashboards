# Paper Download and Organization Script
# This script helps download, convert, and organize academic papers

param(
    [string]$OutputDir = "d:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL",
    [string]$CSVPath = "d:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL\MASTER_THEORY_REFERENCE_SHEET.csv"
)

# Function to create paper folders
function Initialize-PaperFolders {
    $papers = @(
        "P01-Logos-Principle",
        "P02-Quantum-Bridge",
        "P03-Algorithm-Reality",
        "P04-Hard-Problem",
        "P05-Soul-Observer",
        "P06-Physics-Principalities",
        "P07-Grace-Function",
        "P08-Stretched-Heavens",
        "P09-Moral-Universe",
        "P10-Creatio-Silico",
        "P11-Protocols-Validation",
        "P12-Decalogue-Cosmos"
    )
    
    foreach ($paper in $papers) {
        $paperPath = Join-Path $OutputDir $paper
        $referencesPath = Join-Path $paperPath "References"
        $markdownPath = Join-Path $referencesPath "Markdown"
        $pdfPath = Join-Path $referencesPath "PDFs"
        
        New-Item -ItemType Directory -Force -Path $referencesPath | Out-Null
        New-Item -ItemType Directory -Force -Path $markdownPath | Out-Null
        New-Item -ItemType Directory -Force -Path $pdfPath | Out-Null
        
        Write-Host "✓ Created folders for $paper" -ForegroundColor Green
    }
}

# Function to generate download list from CSV
function Export-DownloadList {
    param([string]$CSVPath)
    
    $theories = Import-Csv $CSVPath
    $downloadList = @()
    
    foreach ($theory in $theories) {
        if ($theory.Primary_Author -and $theory.Primary_Author -ne "David Lowe" -and $theory.Primary_Author -ne "Various") {
            $downloadList += [PSCustomObject]@{
                Paper = $theory.Paper_Number
                Theory = $theory.Theory_Name
                Author = $theory.Primary_Author
                SearchQuery = "$($theory.Primary_Author) $($theory.Theory_Name)"
                Domain = $theory.Domain
            }
        }
    }
    
    $downloadList | Export-Csv -Path (Join-Path $OutputDir "PAPERS_TO_DOWNLOAD.csv") -NoTypeInformation
    Write-Host "✓ Created download list: PAPERS_TO_DOWNLOAD.csv" -ForegroundColor Green
    Write-Host "  Found $($downloadList.Count) papers to download" -ForegroundColor Cyan
}

# Function to create citation template
function New-CitationTemplate {
    param(
        [string]$PaperNumber,
        [string]$TheoryName,
        [string]$Author
    )
    
    $template = @"
---
theory: $TheoryName
author: $Author
paper: $PaperNumber
downloaded: $(Get-Date -Format "yyyy-MM-dd")
source: [Add source URL]
doi: [Add DOI if available]
---

# $TheoryName

## Author
$Author

## Key Concepts
[Extract key concepts here]

## Relevance to Theophysics
[How this relates to the Logos framework]

## Citations in Paper
[Where to cite this in $PaperNumber]

## Original Abstract
[Paste abstract here]

## Notes
[Your notes and coherence analysis]

---
*Auto-generated citation template*
"@
    
    return $template
}

# Main execution
Write-Host "`n=== Paper Download & Organization Tool ===" -ForegroundColor Yellow
Write-Host "This script prepares your paper organization structure`n" -ForegroundColor Yellow

# Step 1: Create folder structure
Write-Host "Step 1: Creating folder structure..." -ForegroundColor Cyan
Initialize-PaperFolders

# Step 2: Generate download list
Write-Host "`nStep 2: Generating download list from CSV..." -ForegroundColor Cyan
Export-DownloadList -CSVPath $CSVPath

# Step 3: Create README for manual download
$readmeContent = @"
# Paper Download Guide

## Automated Download Options

### 1. Using Zotero (Recommended)
1. Install Zotero: https://www.zotero.org/
2. Install browser connector
3. Import PAPERS_TO_DOWNLOAD.csv
4. Zotero will auto-fetch PDFs where available

### 2. Using Google Scholar
1. Open PAPERS_TO_DOWNLOAD.csv
2. Search each "SearchQuery" in Google Scholar
3. Look for [PDF] links on the right
4. Download to corresponding P##/References/PDFs/ folder

### 3. Using Sci-Hub (for paywalled papers)
1. Get DOI from Google Scholar
2. Visit: https://sci-hub.se/
3. Paste DOI
4. Download PDF

### 4. Using arXiv (for physics papers)
- Search: https://arxiv.org/
- Download PDF directly
- Many quantum/cosmology papers are here

## Converting PDF to Markdown

### Option 1: Using Pandoc
```powershell
# Install Pandoc first: https://pandoc.org/installing.html
pandoc input.pdf -o output.md --extract-media=./media
```

### Option 2: Using Python Script
```powershell
pip install pymupdf markdown
python convert_papers.py
```

### Option 3: Online Tools
- https://pdf2md.morethan.io/
- https://www.convertapi.com/pdf-to-md

## Organization Structure

Each paper folder (P01-P12) now has:
- References/
  - PDFs/           <- Put downloaded PDFs here
  - Markdown/       <- Put converted markdown here
  - citations.md    <- Auto-generated citation list

## Next Steps

1. Download papers using methods above
2. Convert PDFs to Markdown
3. Run coherence analysis on markdown files
4. Auto-link citations in main papers

## Key Papers to Prioritize

### P01 (Logos Principle)
- Wheeler: "Information, Physics, Quantum"
- John 1 (Bible - already have)

### P02 (Quantum Bridge)
- Von Neumann: "Mathematical Foundations of Quantum Mechanics"
- Radin: "Consciousness and the double-slit interference pattern"

### P04 (Hard Problem)
- Chalmers: "Facing Up to the Problem of Consciousness"
- Tononi: "Integrated Information Theory"
- Penrose & Hameroff: "Consciousness in the universe"

### P07 (Grace Function)
- Landauer: "Irreversibility and Heat Generation"
- Schrödinger: "What is Life?"

### P08 (Stretched Heavens)
- Einstein: General Relativity papers
- Hubble: Expansion papers
- Isaiah 40:22 (Bible - already have)

### P11 (Protocols Validation)
- Dean Radin: Double-slit experiments
- Roger Nelson: Global Consciousness Project papers

## Automation Ideas

Once papers are in Markdown:
1. Run coherence factor analysis
2. Auto-extract key quotes
3. Generate citation suggestions
4. Link related concepts across papers
"@

$readmeContent | Out-File -FilePath (Join-Path $OutputDir "DOWNLOAD_GUIDE.md") -Encoding UTF8
Write-Host "✓ Created DOWNLOAD_GUIDE.md with instructions" -ForegroundColor Green

Write-Host "`n=== Setup Complete! ===" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Review PAPERS_TO_DOWNLOAD.csv" -ForegroundColor White
Write-Host "2. Read DOWNLOAD_GUIDE.md for download methods" -ForegroundColor White
Write-Host "3. Download papers to P##/References/PDFs/" -ForegroundColor White
Write-Host "4. Convert to Markdown" -ForegroundColor White
Write-Host "5. Run coherence analysis" -ForegroundColor White
