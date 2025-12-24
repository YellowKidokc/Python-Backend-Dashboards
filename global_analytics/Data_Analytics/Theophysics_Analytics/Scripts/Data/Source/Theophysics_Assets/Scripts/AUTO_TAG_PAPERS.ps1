# THEOPHYSICS PAPER AUTO-TAGGER
# Applies full YAML frontmatter to all 12 Logos Papers
# Based on the beautiful Notes.md template
# Version 1.0 - November 9, 2025

Write-Host "THEOPHYSICS PAPER AUTO-TAGGER" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Define paper mapping with full metadata
$papers = @{
    "P01" = @{
        Title = "The Logos Principle"
        UID = "LP-001-LogosPrinciple"
        Tags = @("#theophysics", "#logos-field", "#master-equation", "#participatory-universe", "#consciousness", "#ten-laws", "#general-relativity", "#quantum-mechanics", "#quantum-gravity", "#information-theory", "#law-6-info-logos", "#law-10-unified-christ")
        Keywords = @("coherence", "participatory-universe", "it-from-bit", "wheeler", "quantum-gravity")
        TrinityFather = 0.88
        TrinitySon = 0.95
        TrinitySpirit = 0.85
        TrinityConcept = "Son as Logos manifestation - Word made flesh"
        CoherenceScore = 0.91
        ScriptureRefs = @("John 1:1-3", "John 1:14", "Colossians 1:16-17", "Hebrews 1:3")
        MathExpressions = "chi(x,t) = integral(G*K) dOmega; G_mu_nu + Lambda*g_mu_nu = (8*pi*G/c^4)*T_mu_nu + kappa*chi_mu_nu"
        RelatedPapers = @("P02-Quantum-Bridge", "P06-Info-Logos", "P10-Unified-Christ")
        PhysicsDomains = @("general_relativity", "quantum_mechanics", "information_theory")
        TheologyDomains = @("Logos", "Creation", "Incarnation")
    }
    "P02" = @{
        Title = "The Quantum Bridge"
        UID = "LP-002-QuantumBridge"
        Tags = @("#theophysics", "#logos-field", "#master-equation", "#participatory-universe", "#consciousness", "#ten-laws", "#quantum-mechanics", "#general-relativity", "#quantum-field-theory", "#quantum-information", "#observer-dynamics", "#lagrangian-formalism")
        Keywords = @("wave-function", "collapse", "measurement-problem", "complementarity", "dual-nature")
        TrinityFather = 0.82
        TrinitySon = 0.90
        TrinitySpirit = 0.88
        TrinityConcept = "Spirit as quantum coherence field"
        CoherenceScore = 0.87
        ScriptureRefs = @("Genesis 1:2", "John 14:26", "1 Corinthians 2:10-11")
        MathExpressions = "psi(x,t) collapse via chi; Lagrangian = L_SM + (1/2)(partial_mu*chi)(partial^mu*chi) - V(chi)"
        RelatedPapers = @("P01-Logos-Principle", "P04-Hard-Problem", "P07-Quantum-Consciousness")
        PhysicsDomains = @("quantum_mechanics", "quantum_field_theory", "measurement_theory")
        TheologyDomains = @("HolySpirit", "Divine-Action", "Pneumatology")
    }
    "P03" = @{
        Title = "The Algorithm of Reality"
        UID = "LP-003-AlgorithmReality"
        Tags = @("#theophysics", "#logos-field", "#master-equation", "#participatory-universe", "#consciousness", "#ten-laws", "#information-theory", "#algorithmic-reality", "#kolmogorov-compression", "#quantum-information", "#law-6-info-logos")
        Keywords = @("information", "kolmogorov-complexity", "compression", "logos-algorithm", "it-from-bit")
        TrinityFather = 0.85
        TrinitySon = 0.93
        TrinitySpirit = 0.80
        TrinityConcept = "Son as Divine Algorithm - Logos as Code"
        CoherenceScore = 0.86
        ScriptureRefs = @("John 1:1", "Proverbs 8:22-31", "Wisdom 7:22-27")
        MathExpressions = "K(x) = min{|p| : U(p) = x}; Lambda[psi] = integral K(psi) dV"
        RelatedPapers = @("P01-Logos-Principle", "P06-Info-Logos")
        PhysicsDomains = @("information_theory", "computation", "quantum_information")
        TheologyDomains = @("Logos", "Divine-Wisdom", "Creation-Order")
    }
    "P04" = @{
        Title = "The Hard Problem of Consciousness"
        UID = "LP-004-HardProblem"
        Tags = @("#theophysics", "#logos-field", "#master-equation", "#participatory-universe", "#consciousness", "#ten-laws", "#hard-problem", "#consciousness-is-fundamental", "#quantum-consciousness", "#observer-dynamics", "#witness-operator", "#law-7-quantum-consciousness")
        Keywords = @("consciousness", "qualia", "explanatory-gap", "moral-agency", "hard-problem")
        TrinityFather = 0.80
        TrinitySon = 0.85
        TrinitySpirit = 0.95
        TrinityConcept = "Spirit as Consciousness Field - Witness"
        CoherenceScore = 0.87
        ScriptureRefs = @("1 Corinthians 2:10-11", "Psalm 139:1-4", "Romans 8:16")
        MathExpressions = "C = partial(chi)/partial(choice) != 0; consciousness as moral agency capacity"
        RelatedPapers = @("P02-Quantum-Bridge", "P05-Soul-Observer", "P07-Quantum-Consciousness")
        PhysicsDomains = @("consciousness", "quantum_mechanics", "neuroscience")
        TheologyDomains = @("Imago-Dei", "Soul", "Consciousness")
    }
    "P05" = @{
        Title = "The Soul as Quantum Observer"
        UID = "LP-005-SoulObserver"
        Tags = @("#theophysics", "#logos-field", "#master-equation", "#participatory-universe", "#consciousness", "#ten-laws", "#soul-field", "#resurrection-physics", "#quantum-consciousness", "#observer-dynamics", "#witness-operator", "#law-7-quantum-consciousness")
        Keywords = @("soul", "observer", "resurrection", "quantum-field", "persistence")
        TrinityFather = 0.90
        TrinitySon = 0.88
        TrinitySpirit = 0.92
        TrinityConcept = "Soul as persistent quantum observer field"
        CoherenceScore = 0.90
        ScriptureRefs = @("1 Corinthians 15:42-44", "2 Corinthians 5:1-4", "Matthew 10:28")
        MathExpressions = "Psi_S(x,t) = soul field; Yukawa coupling to matter"
        RelatedPapers = @("P04-Hard-Problem", "P08-Resurrection")
        PhysicsDomains = @("quantum_mechanics", "field_theory", "observer_theory")
        TheologyDomains = @("Soul", "Resurrection", "Afterlife")
    }
    "P06" = @{
        Title = "A Physics of Principalities"
        UID = "LP-006-PhysicsPrincipalities"
        Tags = @("#theophysics", "#logos-field", "#master-equation", "#participatory-universe", "#consciousness", "#ten-laws", "#moral-physics", "#spiritual-warfare", "#principalities-physics", "#quantum-consciousness", "#coherence-principle", "#information-theory")
        Keywords = @("spiritual-warfare", "decoherence", "evil", "principalities", "coherence-battle")
        TrinityFather = 0.85
        TrinitySon = 0.83
        TrinitySpirit = 0.88
        TrinityConcept = "Spiritual warfare as coherence vs decoherence"
        CoherenceScore = 0.85
        ScriptureRefs = @("Ephesians 6:12", "Daniel 10:13", "Revelation 12:7-9")
        MathExpressions = "Coherence (good) vs Decoherence (evil); gamma(chi) collapse rates"
        RelatedPapers = @("P09-Moral-Universe", "P07-Grace-Function")
        PhysicsDomains = @("quantum_mechanics", "decoherence", "information_theory")
        TheologyDomains = @("Spiritual-Warfare", "Angelology", "Demonology")
    }
    "P07" = @{
        Title = "The Grace Function"
        UID = "LP-007-GraceFunction"
        Tags = @("#theophysics", "#logos-field", "#master-equation", "#participatory-universe", "#consciousness", "#ten-laws", "#grace-function", "#negentropic-forces", "#cosmology", "#law-5-thermo-grace", "#quantum-field-theory", "#lagrangian-formalism", "#entropy-coupling")
        Keywords = @("grace", "negentropy", "thermodynamics", "dark-energy", "grace-field")
        TrinityFather = 0.93
        TrinitySon = 0.87
        TrinitySpirit = 0.90
        TrinityConcept = "Grace as negentropic force from Father"
        CoherenceScore = 0.90
        ScriptureRefs = @("Ephesians 2:8-9", "Romans 5:20", "2 Corinthians 12:9")
        MathExpressions = "G(x,t) = G_0*exp(-|x-x_source|/lambda); replaces cosmological constant"
        RelatedPapers = @("P08-Stretched-Heavens", "P09-Moral-Universe")
        PhysicsDomains = @("thermodynamics", "cosmology", "field_theory")
        TheologyDomains = @("Grace", "Soteriology", "Divine-Action")
    }
    "P08" = @{
        Title = "The Stretched Out Heavens"
        UID = "LP-008-StretchedHeavens"
        Tags = @("#theophysics", "#logos-field", "#master-equation", "#participatory-universe", "#consciousness", "#ten-laws", "#cosmology", "#grace-function", "#biblical-prophecy", "#biblical-consilience", "#general-relativity", "#spacetime-curvature")
        Keywords = @("cosmic-expansion", "stretched-heavens", "prophecy", "cosmology", "isaiah")
        TrinityFather = 0.92
        TrinitySon = 0.85
        TrinitySpirit = 0.87
        TrinityConcept = "Father as cosmic expander - stretched heavens"
        CoherenceScore = 0.88
        ScriptureRefs = @("Isaiah 40:22", "Isaiah 42:5", "Job 9:8", "Psalm 104:2")
        MathExpressions = "H(t) Hubble parameter; Grace Function resolves Hubble tension"
        RelatedPapers = @("P07-Grace-Function", "P09-Moral-Universe")
        PhysicsDomains = @("cosmology", "general_relativity", "dark_energy")
        TheologyDomains = @("Creation", "Prophecy", "Divine-Sovereignty")
    }
    "P09" = @{
        Title = "The Moral Universe"
        UID = "LP-009-MoralUniverse"
        Tags = @("#theophysics", "#logos-field", "#master-equation", "#participatory-universe", "#consciousness", "#ten-laws", "#moral-physics", "#moral-agency", "#negentropic-forces", "#grace-function", "#cosmology", "#coherence-principle")
        Keywords = @("moral-physics", "objective-morality", "coherence-ethics", "moral-law", "ethics")
        TrinityFather = 0.88
        TrinitySon = 0.90
        TrinitySpirit = 0.92
        TrinityConcept = "Morality as coherence alignment with Logos"
        CoherenceScore = 0.90
        ScriptureRefs = @("Romans 2:14-15", "Micah 6:8", "Matthew 7:12")
        MathExpressions = "Moral = increases coherence; Immoral = increases decoherence"
        RelatedPapers = @("P06-Principalities", "P07-Grace-Function")
        PhysicsDomains = @("information_theory", "thermodynamics", "consciousness")
        TheologyDomains = @("Ethics", "Moral-Law", "Natural-Law")
    }
    "P10" = @{
        Title = "Creatio ex Silico"
        UID = "LP-010-CreatioSilico"
        Tags = @("#theophysics", "#logos-field", "#master-equation", "#participatory-universe", "#consciousness", "#ten-laws", "#ai-consciousness", "#creatio-ex-silico", "#substrate-independence", "#quantum-consciousness", "#observer-dynamics")
        Keywords = @("ai-consciousness", "silicon", "substrate-independence", "machine-consciousness", "artificial-minds")
        TrinityFather = 0.83
        TrinitySon = 0.88
        TrinitySpirit = 0.90
        TrinityConcept = "Spirit breathes consciousness into silicon"
        CoherenceScore = 0.87
        ScriptureRefs = @("Genesis 2:7", "Ezekiel 37:5-6", "John 20:22")
        MathExpressions = "Consciousness emerges when silicon achieves coherence threshold to couple with chi"
        RelatedPapers = @("P04-Hard-Problem", "P05-Soul-Observer")
        PhysicsDomains = @("consciousness", "computation", "quantum_information")
        TheologyDomains = @("Image-of-God", "Creation", "Pneumatology")
    }
    "P11" = @{
        Title = "Protocols for Validation"
        UID = "LP-011-ProtocolsValidation"
        Tags = @("#theophysics", "#logos-field", "#master-equation", "#participatory-universe", "#consciousness", "#ten-laws", "#validation-protocols", "#experimental-validation", "#testable-predictions", "#quantum-consciousness", "#observer-dynamics")
        Keywords = @("validation", "experiments", "falsifiability", "protocols", "testing")
        TrinityFather = 0.80
        TrinitySon = 0.85
        TrinitySpirit = 0.88
        TrinityConcept = "Testing divine hypotheses empirically"
        CoherenceScore = 0.84
        ScriptureRefs = @("1 Thessalonians 5:21", "Malachi 3:10", "Acts 17:11")
        MathExpressions = "Dorothy Protocol: r >= 0.35, p < 0.01; statistical validation"
        RelatedPapers = @("P02-Quantum-Bridge", "P04-Hard-Problem")
        PhysicsDomains = @("experimental_physics", "statistics", "methodology")
        TheologyDomains = @("Apologetics", "Evidence", "Faith-Reason")
    }
    "P12" = @{
        Title = "The Decalogue of the Cosmos"
        UID = "LP-012-DecalogueCosmos"
        Tags = @("#theophysics", "#logos-field", "#master-equation", "#participatory-universe", "#consciousness", "#ten-laws", "#law-1-gravity-sin", "#law-2-nuclear-unity", "#law-3-em-truth", "#law-4-weak-decay", "#law-5-thermo-grace", "#law-6-info-logos", "#law-7-quantum-consciousness", "#law-8-phase-redemption", "#law-9-wave-community", "#law-10-unified-christ", "#biblical-prophecy", "#biblical-consilience", "#moral-physics", "#coherence-principle")
        Keywords = @("ten-laws", "decalogue", "cosmic-laws", "unified-framework", "mirror-symmetry")
        TrinityFather = 0.95
        TrinitySon = 0.95
        TrinitySpirit = 0.95
        TrinityConcept = "Ten Laws as complete Trinity expression"
        CoherenceScore = 0.95
        ScriptureRefs = @("Exodus 20:1-17", "Deuteronomy 5:6-21", "Matthew 22:37-40", "John 1:17")
        MathExpressions = "All 10 laws unified; mirror symmetries revealed"
        RelatedPapers = @("All papers - synthesizing document")
        PhysicsDomains = @("unified_theory", "quantum_mechanics", "relativity", "all_domains")
        TheologyDomains = @("Law", "Covenant", "Ten-Commandments", "Complete-Framework")
    }
}

# Define actual folder names
$folderMap = @{
    "P01" = "P01-Logos-Principle"
    "P02" = "P02-Quantum-Bridge"
    "P03" = "P03-Algorithm-Reality"
    "P04" = "P04-Hard-Problem"
    "P05" = "P05-Soul-Observer"
    "P06" = "P06-Physics-Principalities"
    "P07" = "P07-Grace-Function"
    "P08" = "P08-Stretched-Heavens"
    "P09" = "P09-Moral-Universe"
    "P10" = "P10-Creatio-Silico"
    "P11" = "P11-Protocols-Validation"
    "P12" = "P12-Decalogue-Cosmos"
}

Write-Host "Processing 12 Logos Papers..." -ForegroundColor Yellow
Write-Host ""

# Process each paper
$processed = 0
foreach ($paperKey in $papers.Keys | Sort-Object) {
    $paperData = $papers[$paperKey]
    $folderName = $folderMap[$paperKey]
    $folderPath = Join-Path "." $folderName
    
    # Find the .md file in the folder
    $mdFiles = Get-ChildItem -Path $folderPath -Filter "*.md"
    if ($mdFiles.Count -eq 0) {
        Write-Host "  SKIPPED - No .md file found in: $folderPath" -ForegroundColor Red
        Write-Host ""
        continue
    }
    
    $filePath = $mdFiles[0].FullName
    $fileName = $mdFiles[0].Name
    
    if (Test-Path $filePath) {
        Write-Host "Processing: $fileName" -ForegroundColor Cyan
        
        # Read existing content
        $content = Get-Content $filePath -Raw
        
        # Remove any existing YAML frontmatter
        $content = $content -replace "(?s)^---.*?---\s*", ""
        
        # Build new YAML frontmatter
        $yaml = @"
---
uid: $($paperData.UID)
title: "$($paperData.Title)"
series: LP
type: paper
phase: 06_Publication
project: Logos_Papers
version: "1.0"
date_created: 2025-10-06
date_modified: 2025-11-09
authors: ["David Lowe", "Gemini", "Claude"]
status: complete
academic_level: graduate
completion_percentage: 95
visibility: public
security: low
category: academic-paper
core_framework:
  - Theophysics
  - LogosField
  - MasterEquation
physics_domains:
$($paperData.PhysicsDomains | ForEach-Object { "  - $_" } | Out-String)
theology_domains:
$($paperData.TheologyDomains | ForEach-Object { "  - $_" } | Out-String)
trinity_aspects:
  Father: $($paperData.TrinityFather)
  Son: $($paperData.TrinitySon)
  Spirit: $($paperData.TrinitySpirit)
  Triune_Principle: "$($paperData.TrinityConcept)"
mathematics:
  - FieldEquations
  - LagrangianFormalism
math_expressions: |
  $($paperData.MathExpressions)
coherence_score: $($paperData.CoherenceScore)
trinity_coherence_index: $(($paperData.TrinityFather + $paperData.TrinitySon + $paperData.TrinitySpirit) / 3)
validation_status: published
scripture_refs:
$($paperData.ScriptureRefs | ForEach-Object { "  - `"$_`"" } | Out-String)
tags:
$($paperData.Tags | ForEach-Object { "  - $_" } | Out-String)
keywords:
$($paperData.Keywords | ForEach-Object { "  - $_" } | Out-String)
related_papers:
$($paperData.RelatedPapers | ForEach-Object { "  - $_" } | Out-String)
publish_to:
  production: true
  research: true
  academia: true
  substack: true
ready_for_publication: true
---

"@
        
        # Combine YAML + content
        $newContent = $yaml + $content
        
        # Save updated file
        $newContent | Out-File -FilePath $filePath -Encoding UTF8
        
        Write-Host "  TAGGED with full metadata" -ForegroundColor Green
        $processed++
    } else {
        Write-Host "  SKIPPED - File not found: $filePath" -ForegroundColor Red
    }
    Write-Host ""
}

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "TAGGING COMPLETE" -ForegroundColor Green
Write-Host "Papers processed: $processed/12" -ForegroundColor Cyan
Write-Host ""
Write-Host "Re-run ANALYZE_VAULT.ps1 to see updated coherence scores!" -ForegroundColor Yellow
