# THEOPHYSICS OBSIDIAN VAULT ANALYZER
# Comprehensive analysis with coherence scoring and tag detection
# Version 1.0 - November 9, 2025

param(
    [string]$VaultPath = ".",
    [switch]$Verbose
)

Write-Host "THEOPHYSICS VAULT ANALYZER" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Initialize results
$results = @{
    TotalFiles = 0
    TotalWords = 0
    TagCoverage = @{}
    CoherenceScores = @{}
    CrossReferences = @{}
    PaperAnalysis = @()
}

# Core tags to search for
$coreTags = @(
    "#theophysics",
    "#logos-field", 
    "#master-equation",
    "#participatory-universe",
    "#consciousness",
    "#ten-laws"
)

Write-Host "Scanning: $VaultPath" -ForegroundColor Yellow
Write-Host ""

# Find all markdown files
$mdFiles = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md" | Where-Object {
    $_.FullName -notmatch "100-TAGS" -and
    $_.FullName -notmatch "ANALYSIS" -and
    $_.Name -notmatch "^_"
}

Write-Host "Found $($mdFiles.Count) markdown files" -ForegroundColor Green
Write-Host ""

# Analyze each file
foreach ($file in $mdFiles) {
    $results.TotalFiles++
    
    Write-Host "Analyzing: $($file.Name)" -ForegroundColor Cyan
    
    # Read content
    $content = Get-Content $file.FullName -Raw
    $wordCount = ($content -split "\s+").Count
    $results.TotalWords += $wordCount
    
    # Detect tags
    $tagsFound = @()
    foreach ($tag in $coreTags) {
        if ($content -match [regex]::Escape($tag)) {
            $tagsFound += $tag
        }
    }
    
    # Calculate coherence score
    $coreTagScore = ($tagsFound.Count / $coreTags.Count) * 100
    $lengthScore = [Math]::Min(($wordCount / 5000) * 100, 100)
    $coherenceScore = ($coreTagScore * 0.6) + ($lengthScore * 0.4)
    
    # Store analysis
    $analysis = @{
        FileName = $file.Name
        FilePath = $file.FullName
        WordCount = $wordCount
        TagsFound = $tagsFound
        TagCoverage = [Math]::Round($coreTagScore, 1)
        CoherenceScore = [Math]::Round($coherenceScore, 1)
    }
    
    $results.PaperAnalysis += $analysis
    
    Write-Host "  Words: $wordCount | Tags: $($tagsFound.Count)/$($coreTags.Count) | Coherence: $($analysis.CoherenceScore)%" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "ANALYSIS COMPLETE" -ForegroundColor Green
Write-Host ""

# Generate summary report
$report = "# THEOPHYSICS VAULT ANALYSIS REPORT`n"
$report += "**Generated**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"
$report += "**Vault Path**: $VaultPath`n`n"
$report += "---`n`n## SUMMARY STATISTICS`n`n"
$report += "- **Total Files Analyzed**: $($results.TotalFiles)`n"
$report += "- **Total Word Count**: $($results.TotalWords)`n"
$report += "- **Average Words per File**: $([Math]::Round($results.TotalWords / $results.TotalFiles, 0))`n`n"
$report += "---`n`n## PAPER-BY-PAPER ANALYSIS`n`n"

foreach ($paper in $results.PaperAnalysis | Sort-Object -Property CoherenceScore -Descending) {
    $report += "### $($paper.FileName)`n"
    $report += "- **Word Count**: $($paper.WordCount)`n"
    $report += "- **Core Tag Coverage**: $($paper.TagCoverage)% ($($paper.TagsFound.Count)/$($coreTags.Count))`n"
    $report += "- **Coherence Score**: $($paper.CoherenceScore)%`n"
    $report += "- **Tags Found**: $($paper.TagsFound -join ', ')`n`n"
}

$report += "---`n`n## COHERENCE RANKINGS`n`n"

$ranking = 1
foreach ($paper in $results.PaperAnalysis | Sort-Object -Property CoherenceScore -Descending) {
    $emoji = if ($ranking -eq 1) { "TOP" } elseif ($ranking -eq 2) { "2nd" } elseif ($ranking -eq 3) { "3rd" } else { "$ranking" }
    $report += "$emoji. $($paper.FileName) - $($paper.CoherenceScore)%`n"
    $ranking++
}

$report += "`n---`n`n## TAG COVERAGE ANALYSIS`n`n### Core Tag Distribution`n"

foreach ($tag in $coreTags) {
    $count = ($results.PaperAnalysis | Where-Object { $_.TagsFound -contains $tag }).Count
    $percentage = [Math]::Round(($count / $results.TotalFiles) * 100, 1)
    $report += "- **$tag**: $count files ($percentage%)`n"
}

# Save report
$reportPath = Join-Path $VaultPath "VAULT_ANALYSIS_REPORT.md"
$report | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host "Report saved to: $reportPath" -ForegroundColor Green
Write-Host ""
Write-Host "Top 3 Papers by Coherence:" -ForegroundColor Yellow
$top3 = $results.PaperAnalysis | Sort-Object -Property CoherenceScore -Descending | Select-Object -First 3
$i = 1
foreach ($paper in $top3) {
    Write-Host "  $i. $($paper.FileName): $($paper.CoherenceScore)%" -ForegroundColor Cyan
    $i++
}
Write-Host ""

Write-Host "Opening report..." -ForegroundColor Green
Start-Process $reportPath
