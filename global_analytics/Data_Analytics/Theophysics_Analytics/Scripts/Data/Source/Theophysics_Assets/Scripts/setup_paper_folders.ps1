# Simple Paper Folder Setup Script
# Creates Reference folders for P01-P12

$baseDir = "d:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL"
$csvPath = Join-Path $baseDir "MASTER_THEORY_REFERENCE_SHEET.csv"

Write-Host "`n=== Setting up Paper Reference Folders ===" -ForegroundColor Yellow

# Create folders for each paper
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
    $paperPath = Join-Path $baseDir $paper
    $referencesPath = Join-Path $paperPath "References"
    $markdownPath = Join-Path $referencesPath "Markdown"
    $pdfPath = Join-Path $referencesPath "PDFs"
    
    New-Item -ItemType Directory -Force -Path $referencesPath | Out-Null
    New-Item -ItemType Directory -Force -Path $markdownPath | Out-Null
    New-Item -ItemType Directory -Force -Path $pdfPath | Out-Null
    
    Write-Host "Created: $paper/References/{PDFs,Markdown}" -ForegroundColor Green
}

# Generate download list from CSV
Write-Host "`nGenerating download list..." -ForegroundColor Cyan

if (Test-Path $csvPath) {
    $theories = Import-Csv $csvPath
    $downloadList = @()
    
    foreach ($theory in $theories) {
        if ($theory.Primary_Author -and 
            $theory.Primary_Author -ne "David Lowe" -and 
            $theory.Primary_Author -ne "Various" -and
            $theory.Primary_Author -ne "Biblical") {
            
            $downloadList += [PSCustomObject]@{
                Paper = $theory.Paper_Number
                Theory = $theory.Theory_Name
                Author = $theory.Primary_Author
                SearchQuery = "$($theory.Primary_Author) $($theory.Theory_Name)"
                Domain = $theory.Domain
            }
        }
    }
    
    $downloadListPath = Join-Path $baseDir "PAPERS_TO_DOWNLOAD.csv"
    $downloadList | Export-Csv -Path $downloadListPath -NoTypeInformation
    Write-Host "Created: PAPERS_TO_DOWNLOAD.csv ($($downloadList.Count) papers)" -ForegroundColor Green
}

Write-Host "`n=== Setup Complete! ===" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Open PAPERS_TO_DOWNLOAD.csv to see what to download" -ForegroundColor White
Write-Host "2. Download PDFs to P##-Paper-Name/References/PDFs/" -ForegroundColor White
Write-Host "3. Run: python convert_papers_to_markdown.py" -ForegroundColor White
Write-Host "4. Converted markdown will be in P##-Paper-Name/References/Markdown/" -ForegroundColor White
