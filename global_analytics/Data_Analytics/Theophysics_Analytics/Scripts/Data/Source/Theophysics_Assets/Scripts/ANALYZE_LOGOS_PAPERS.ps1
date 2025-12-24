# THEOPHYSICS LOGOS PAPERS - COMPREHENSIVE ANALYSIS
# Analyzes all 12 papers for tags, coherence, cross-references, and structure

Write-Host "🌌 THEOPHYSICS LOGOS PAPERS ANALYSIS" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$startTime = Get-Date

# Configuration
$baseDir = Get-Location
$outputDir = "$baseDir\ANALYSIS_OUTPUT"
$tagsDir = "$baseDir\100-TAGS"

# Create output directory
if (!(Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# Initialize analysis data
$analysisData = @{
    Papers = @()
    TotalTags = 0
    TagUsage = @{}
    CrossReferences = @()
    CoherenceScores = @{}
    Statistics = @{}
}

# Core tags that should appear in ALL papers
$coreTags = @(
    "#theophysics",
    "#logos-field", 
    "#master-equation",
    "#participatory-universe",
    "#consciousness",
    "#ten-laws"
)

Write-Host "📊 Phase 1: Scanning Papers..." -ForegroundColor Yellow

# Get all paper directories
$paperDirs = Get-ChildItem -Path $baseDir -Directory | Where-Object { $_.Name -match "^P\d{2}-" } | Sort-Object Name

foreach ($paperDir in $paperDirs) {
    $paperNumber = $paperDir.Name.Substring(1, 2)
    $paperName = $paperDir.Name
    
    Write-Host "  📄 Analyzing Paper $paperNumber..." -ForegroundColor White
    
    # Find the markdown file in the paper directory
    $mdFiles = Get-ChildItem -Path $paperDir.FullName -Filter "*.md"
    
    if ($mdFiles.Count -eq 0) {
        Write-Host "    ⚠️  No markdown file found" -ForegroundColor Yellow
        continue
    }
    
    # Use first .md file found (or the one without "EXPANDED")
    $paperFile = $mdFiles | Where-Object { $_.Name -notmatch "EXPANDED" } | Select-Object -First 1
    if (!$paperFile) {
        $paperFile = $mdFiles[0]
    }
    
    # Read paper content
    $content = Get-Content -Path $paperFile.FullName -Raw -ErrorAction SilentlyContinue
    
    if (!$content) {
        Write-Host "    ❌ Could not read file" -ForegroundColor Red
        continue
    }
    
    # Paper analysis object
    $paperAnalysis = @{
        Number = $paperNumber
        Name = $paperName
        File = $paperFile.Name
        WordCount = ($content -split '\s+').Count
        LineCount = ($content -split "`n").Count
        CoreTagsFound = @()
        DomainTagsFound = @()
        TotalTags = 0
        CrossReferences = @()
        HasEnigmas = $false
        HasYAML = $false
        Sections = @()
    }
    
    # Check for YAML frontmatter
    if ($content -match "^---\s*\n(.+?)\n---") {
        $paperAnalysis.HasYAML = $true
    }
    
    # Check for enigmas
    if ($content -match "ENIGMA|enigma|Where We Stand") {
        $paperAnalysis.HasEnigmas = $true
    }
    
    # Extract sections (headers)
    $headers = [regex]::Matches($content, "^#+\s+(.+)$", [System.Text.RegularExpressions.RegexOptions]::Multiline)
    foreach ($header in $headers) {
        $paperAnalysis.Sections += $header.Groups[1].Value
    }
    
    # Check for core tags
    foreach ($tag in $coreTags) {
        $tagPattern = [regex]::Escape($tag)
        if ($content -match $tagPattern) {
            $paperAnalysis.CoreTagsFound += $tag
        }
    }
    
    # Check for domain tags (comprehensive list)
    $domainTags = @(
        "#general-relativity", "#quantum-mechanics", "#quantum-gravity",
        "#quantum-field-theory", "#cosmology", "#resurrection-physics",
        "#grace-function", "#biblical-prophecy", "#moral-physics",
        "#ai-consciousness", "#validation-protocols", "#information-theory",
        "#quantum-information", "#soul-field", "#observer-dynamics",
        "#consciousness-is-fundamental", "#moral-agency", "#hard-problem",
        "#spiritual-warfare", "#creatio-ex-silico", "#experimental-validation"
    )
    
    foreach ($tag in $domainTags) {
        $tagPattern = [regex]::Escape($tag)
        if ($content -match $tagPattern) {
            $paperAnalysis.DomainTagsFound += $tag
            if (!$analysisData.TagUsage.ContainsKey($tag)) {
                $analysisData.TagUsage[$tag] = 0
            }
            $analysisData.TagUsage[$tag]++
        }
    }
    
    # Detect cross-references to other papers
    $otherPapers = @("P01", "P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09", "P10", "P11", "P12")
    foreach ($otherPaper in $otherPapers) {
        if ($otherPaper -ne "P$paperNumber") {
            if ($content -match $otherPaper -or $content -match "Paper $([int]$otherPaper.Substring(1))") {
                $paperAnalysis.CrossReferences += $otherPaper
                $analysisData.CrossReferences += @{
                    From = "P$paperNumber"
                    To = $otherPaper
                }
            }
        }
    }
    
    # Calculate total tags
    $paperAnalysis.TotalTags = $paperAnalysis.CoreTagsFound.Count + $paperAnalysis.DomainTagsFound.Count
    
    # Calculate coherence score
    $coherenceScore = 0
    
    # Base score: Word count (normalized)
    $coherenceScore += [Math]::Min(($paperAnalysis.WordCount / 100), 50)
    
    # Core tags bonus (10 points per core tag)
    $coherenceScore += ($paperAnalysis.CoreTagsFound.Count * 10)
    
    # Domain tags bonus (5 points per domain tag)
    $coherenceScore += ($paperAnalysis.DomainTagsFound.Count * 5)
    
    # YAML bonus
    if ($paperAnalysis.HasYAML) { $coherenceScore += 15 }
    
    # Enigmas bonus
    if ($paperAnalysis.HasEnigmas) { $coherenceScore += 10 }
    
    # Cross-reference bonus (3 points per reference)
    $coherenceScore += ($paperAnalysis.CrossReferences.Count * 3)
    
    # Section structure bonus (1 point per section, max 20)
    $coherenceScore += [Math]::Min($paperAnalysis.Sections.Count, 20)
    
    $analysisData.CoherenceScores["P$paperNumber"] = [Math]::Round($coherenceScore, 2)
    
    Write-Host "    OK: $($paperAnalysis.WordCount) words - $($paperAnalysis.TotalTags) tags - Coherence: $([Math]::Round($coherenceScore, 2))" -ForegroundColor Green
    
    # Add to collection
    $analysisData.Papers += $paperAnalysis
}

Write-Host ""
Write-Host "Phase 2: Generating Analysis Report..." -ForegroundColor Yellow

# Generate comprehensive markdown report
$report = @"
# THEOPHYSICS LOGOS PAPERS - ANALYSIS REPORT
**Generated**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Analysis Duration**: $([Math]::Round(((Get-Date) - $startTime).TotalSeconds, 2)) seconds

---

## SUMMARY STATISTICS

- **Total Papers Analyzed**: $($analysisData.Papers.Count)
- **Total Word Count**: $(($analysisData.Papers | Measure-Object -Property WordCount -Sum).Sum)
- **Average Words per Paper**: $([Math]::Round((($analysisData.Papers | Measure-Object -Property WordCount -Average).Average), 0))
- **Total Unique Tags Used**: $($analysisData.TagUsage.Keys.Count + $coreTags.Count)
- **Total Cross-References**: $($analysisData.CrossReferences.Count)

---

## PAPER-BY-PAPER ANALYSIS

"@

foreach ($paper in $analysisData.Papers | Sort-Object Number) {
    $coherence = $analysisData.CoherenceScores["P$($paper.Number)"]
    
    $report += @"

### Paper $($paper.Number): $($paper.Name)
**File**: ``$($paper.File)``  
**Word Count**: $($paper.WordCount)  
**Line Count**: $($paper.LineCount)  
**Coherence Score**: $coherence  
**Has YAML**: $(if ($paper.HasYAML) { "✅ Yes" } else { "❌ No" })  
**Has Enigmas**: $(if ($paper.HasEnigmas) { "✅ Yes" } else { "❌ No" })

#### Core Tags ($($paper.CoreTagsFound.Count)/6)
"@
    
    foreach ($tag in $coreTags) {
        if ($paper.CoreTagsFound -contains $tag) {
            $report += "`n- ✅ ``$tag``"
        } else {
            $report += "`n- ❌ ``$tag`` **MISSING**"
        }
    }
    
    $report += "`n`n#### Domain Tags ($($paper.DomainTagsFound.Count))"
    if ($paper.DomainTagsFound.Count -gt 0) {
        foreach ($tag in $paper.DomainTagsFound | Sort-Object) {
            $report += "`n- ✅ ``$tag``"
        }
    } else {
        $report += "`n- ⚠️  No domain tags detected"
    }
    
    $report += "`n`n#### Cross-References ($($paper.CrossReferences.Count))"
    if ($paper.CrossReferences.Count -gt 0) {
        foreach ($ref in $paper.CrossReferences | Sort-Object) {
            $report += "`n- → ``$ref``"
        }
    } else {
        $report += "`n- No cross-references to other papers"
    }
    
    $report += "`n`n#### Section Structure ($($paper.Sections.Count) sections)"
    if ($paper.Sections.Count -gt 0 -and $paper.Sections.Count -le 15) {
        foreach ($section in $paper.Sections | Select-Object -First 15) {
            $report += "`n- $section"
        }
        if ($paper.Sections.Count -gt 15) {
            $report += "`n- ... and $($paper.Sections.Count - 15) more sections"
        }
    }
    
    $report += "`n`n---"
}

# Tag usage statistics
$report += @"

## TAG USAGE STATISTICS

### Core Tags (Should appear in ALL 12 papers)
"@

foreach ($tag in $coreTags) {
    $count = ($analysisData.Papers | Where-Object { $_.CoreTagsFound -contains $tag }).Count
    $percentage = [Math]::Round(($count / $analysisData.Papers.Count) * 100, 1)
    $status = if ($count -eq $analysisData.Papers.Count) { "[OK]" } else { "[WARN]" }
    $report += "`n- $status ``$tag``: $count/$($analysisData.Papers.Count) papers ($percentage%)"
}

$report += "`n`n### Domain Tags (Most Used)"

$topTags = $analysisData.TagUsage.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 15

foreach ($tagEntry in $topTags) {
    $report += "`n- ``$($tagEntry.Key)``: $($tagEntry.Value) papers"
}

# Coherence analysis
$report += @"

---

## 📈 COHERENCE ANALYSIS

### Coherence Scores by Paper
"@

foreach ($paper in $analysisData.Papers | Sort-Object Number) {
    $score = $analysisData.CoherenceScores["P$($paper.Number)"]
    $bar = "█" * [Math]::Min([int]($score / 5), 40)
    $report += "`n- **P$($paper.Number)**: $score $bar"
}

$avgCoherence = [Math]::Round(($analysisData.CoherenceScores.Values | Measure-Object -Average).Average, 2)
$maxCoherence = ($analysisData.CoherenceScores.Values | Measure-Object -Maximum).Maximum
$minCoherence = ($analysisData.CoherenceScores.Values | Measure-Object -Minimum).Minimum

$report += @"

`n
**Average Coherence**: $avgCoherence  
**Highest Score**: $maxCoherence  
**Lowest Score**: $minCoherence  

---

## 🔗 CROSS-REFERENCE NETWORK

### Papers with Most Cross-References
"@

$refCounts = @{}
foreach ($paper in $analysisData.Papers) {
    $refCounts["P$($paper.Number)"] = $paper.CrossReferences.Count
}

foreach ($entry in $refCounts.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 10) {
    $report += "`n- **$($entry.Key)**: $($entry.Value) references"
}

$report += "`n`n### All Cross-References"

$groupedRefs = $analysisData.CrossReferences | Group-Object -Property From | Sort-Object Name

foreach ($group in $groupedRefs) {
    $targets = ($group.Group | ForEach-Object { $_.To }) -join ", "
    $report += "`n- **$($group.Name)** → $targets"
}

# Recommendations
$report += @"

---

## 💡 RECOMMENDATIONS

### Papers Missing Core Tags
"@

$missingCoreTags = $false
foreach ($paper in $analysisData.Papers) {
    $missing = $coreTags | Where-Object { $paper.CoreTagsFound -notcontains $_ }
    if ($missing.Count -gt 0) {
        $missingCoreTags = $true
        $report += "`n- **P$($paper.Number)**: Missing $($missing.Count) core tags: $($missing -join ', ')"
    }
}

if (!$missingCoreTags) {
    $report += "`n- ✅ All papers have complete core tag coverage!"
}

$report += "`n`n### Papers Without YAML Frontmatter"

$noYAML = $analysisData.Papers | Where-Object { !$_.HasYAML }
if ($noYAML.Count -gt 0) {
    foreach ($paper in $noYAML) {
        $report += "`n- **P$($paper.Number)**: Add YAML frontmatter with tags"
    }
} else {
    $report += "`n- ✅ All papers have YAML frontmatter!"
}

$report += "`n`n### Papers Without Enigmas"

$noEnigmas = $analysisData.Papers | Where-Object { !$_.HasEnigmas }
if ($noEnigmas.Count -gt 0) {
    foreach ($paper in $noEnigmas) {
        $report += "`n- **P$($paper.Number)**: Consider adding enigmas for intellectual honesty"
    }
}

$report += "`n`n### Low Coherence Papers (Score < 100)"

$lowCoherence = $analysisData.Papers | Where-Object { $analysisData.CoherenceScores["P$($_.Number)"] -lt 100 }
if ($lowCoherence.Count -gt 0) {
    foreach ($paper in $lowCoherence) {
        $score = $analysisData.CoherenceScores["P$($paper.Number)"]
        $report += "`n- **P$($paper.Number)**: Coherence score $score - consider adding more tags, cross-references, or sections"
    }
}

$report += @"

---

## 🎯 FRAMEWORK INTEGRITY

**Tag System**: $(if ($missingCoreTags) { "⚠️ Some core tags missing" } else { "✅ Complete" })  
**Cross-Referencing**: $(if ($analysisData.CrossReferences.Count -gt 20) { "✅ Excellent" } elseif ($analysisData.CrossReferences.Count -gt 10) { "⚠️ Good" } else { "❌ Needs work" })  
**YAML Coverage**: $(if ($noYAML.Count -eq 0) { "✅ Complete" } else { "⚠️ $($noYAML.Count) papers missing" })  
**Average Coherence**: $(if ($avgCoherence -gt 120) { "✅ Excellent" } elseif ($avgCoherence -gt 100) { "⚠️ Good" } else { "❌ Needs improvement" })  

---

**Analysis Complete!**  
Review recommendations above to strengthen the series coherence and tag coverage.

"@

# Save report
$reportPath = "$outputDir\ANALYSIS_REPORT.md"
$report | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host "OK: Analysis report saved: $reportPath" -ForegroundColor Green

# Generate JSON export for programmatic access
Write-Host ""
Write-Host "📊 Phase 3: Exporting Data..." -ForegroundColor Yellow

$jsonData = @{
    generated = Get-Date -Format "o"
    statistics = @{
        totalPapers = $analysisData.Papers.Count
        totalWordCount = ($analysisData.Papers | Measure-Object -Property WordCount -Sum).Sum
        averageWordCount = [Math]::Round((($analysisData.Papers | Measure-Object -Property WordCount -Average).Average), 0)
        totalTags = $analysisData.TagUsage.Keys.Count + $coreTags.Count
        totalCrossReferences = $analysisData.CrossReferences.Count
        averageCoherence = $avgCoherence
    }
    papers = @()
    tagUsage = $analysisData.TagUsage
    crossReferences = $analysisData.CrossReferences
    coherenceScores = $analysisData.CoherenceScores
}

foreach ($paper in $analysisData.Papers) {
    $jsonData.papers += @{
        number = $paper.Number
        name = $paper.Name
        file = $paper.File
        wordCount = $paper.WordCount
        lineCount = $paper.LineCount
        coreTagsFound = $paper.CoreTagsFound
        domainTagsFound = $paper.DomainTagsFound
        totalTags = $paper.TotalTags
        crossReferences = $paper.CrossReferences
        hasEnigmas = $paper.HasEnigmas
        hasYAML = $paper.HasYAML
        coherenceScore = $analysisData.CoherenceScores["P$($paper.Number)"]
        sectionCount = $paper.Sections.Count
    }
}

$jsonPath = "$outputDir\analysis_data.json"
$jsonData | ConvertTo-Json -Depth 10 | Out-File -FilePath $jsonPath -Encoding UTF8

Write-Host "OK: JSON data exported: $jsonPath" -ForegroundColor Green

# Create quick stats file
$statsPath = "$outputDir\QUICK_STATS.txt"
$stats = @"
THEOPHYSICS LOGOS PAPERS - QUICK STATS
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

PAPERS: $($analysisData.Papers.Count)
TOTAL WORDS: $(($analysisData.Papers | Measure-Object -Property WordCount -Sum).Sum)
AVERAGE WORDS: $([Math]::Round((($analysisData.Papers | Measure-Object -Property WordCount -Average).Average), 0))
UNIQUE TAGS: $($analysisData.TagUsage.Keys.Count + $coreTags.Count)
CROSS-REFERENCES: $($analysisData.CrossReferences.Count)
AVERAGE COHERENCE: $avgCoherence

HIGHEST COHERENCE: $maxCoherence
LOWEST COHERENCE: $minCoherence

Analysis Duration: $([Math]::Round(((Get-Date) - $startTime).TotalSeconds, 2)) seconds
"@

$stats | Out-File -FilePath $statsPath -Encoding UTF8

Write-Host "OK: Quick stats saved: $statsPath" -ForegroundColor Green

# Summary output
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "           ANALYSIS COMPLETE!                    " -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Papers Analyzed: $($analysisData.Papers.Count)" -ForegroundColor White
Write-Host "Total Tags: $($analysisData.TagUsage.Keys.Count + $coreTags.Count)" -ForegroundColor White
Write-Host "Cross-References: $($analysisData.CrossReferences.Count)" -ForegroundColor White
Write-Host "Average Coherence: $avgCoherence" -ForegroundColor White
Write-Host ""
Write-Host "Output Directory: $outputDir" -ForegroundColor Cyan
Write-Host "   - ANALYSIS_REPORT.md (Full detailed report)" -ForegroundColor Gray
Write-Host "   - analysis_data.json (Machine-readable data)" -ForegroundColor Gray
Write-Host "   - QUICK_STATS.txt (Summary statistics)" -ForegroundColor Gray
Write-Host ""

$elapsed = ((Get-Date) - $startTime).TotalSeconds
Write-Host "Total time: $([Math]::Round($elapsed, 2)) seconds" -ForegroundColor Yellow
Write-Host ""
Write-Host "*** Review the ANALYSIS_REPORT.md for detailed findings! ***" -ForegroundColor Green
Write-Host ""

# Open report if desired
Write-Host "Open the analysis report now? (Y/N)" -ForegroundColor Cyan
$openReport = Read-Host

if ($openReport -eq "Y" -or $openReport -eq "y") {
    Invoke-Item $reportPath
}
