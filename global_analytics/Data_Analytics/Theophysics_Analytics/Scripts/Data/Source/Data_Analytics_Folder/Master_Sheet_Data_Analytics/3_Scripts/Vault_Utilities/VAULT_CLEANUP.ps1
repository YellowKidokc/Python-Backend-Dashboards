# ═══════════════════════════════════════════════════════════════
# VAULT CLEANUP SCRIPT
# Purpose: Prepare vault for mass-market distribution
# Author: David Lowe / Claude
# Date: 2025-11-18
# ═══════════════════════════════════════════════════════════════

param(
    [switch]$DryRun = $false,
    [switch]$Verbose = $false
)

$VaultRoot = "D:\THEOPHYSICS_MASTER"
$AssetsDir = Join-Path $VaultRoot "00_VAULT_SYSTEM\Assets\Images"

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " VAULT CLEANUP - Mass Market Preparation" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - No changes will be made" -ForegroundColor Yellow
    Write-Host ""
}

$DeleteCount = 0
$MoveCount = 0
$Errors = @()

# ═══════════════════════════════════════════════════════════════
# FUNCTION: Safe Delete
# ═══════════════════════════════════════════════════════════════
function Remove-ItemSafe {
    param(
        [string]$Path,
        [string]$Reason
    )
    
    if (Test-Path $Path) {
        $item = Get-Item $Path
        if ($DryRun) {
            Write-Host "  [DRY RUN] Would delete: $($item.Name)" -ForegroundColor Gray
            if ($Verbose) { Write-Host "            Reason: $Reason" -ForegroundColor DarkGray }
        } else {
            try {
                Remove-Item $Path -Recurse -Force
                Write-Host "  ✓ Deleted: $($item.Name)" -ForegroundColor Green
                if ($Verbose) { Write-Host "    Reason: $Reason" -ForegroundColor DarkGray }
                $script:DeleteCount++
            } catch {
                Write-Host "  ✗ Failed: $($item.Name) - $($_.Exception.Message)" -ForegroundColor Red
                $script:Errors += "Delete failed: $Path"
            }
        }
    } elseif ($Verbose) {
        Write-Host "  ⊘ Not found: $Path" -ForegroundColor DarkGray
    }
}

# ═══════════════════════════════════════════════════════════════
# FUNCTION: Safe Move
# ═══════════════════════════════════════════════════════════════
function Move-ItemSafe {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$Reason
    )
    
    if (Test-Path $Source) {
        $item = Get-Item $Source
        $destPath = Join-Path $Destination $item.Name
        
        if ($DryRun) {
            Write-Host "  [DRY RUN] Would move: $($item.Name) → $Destination" -ForegroundColor Gray
            if ($Verbose) { Write-Host "            Reason: $Reason" -ForegroundColor DarkGray }
        } else {
            try {
                if (!(Test-Path $Destination)) {
                    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
                }
                Move-Item $Source $destPath -Force
                Write-Host "  ✓ Moved: $($item.Name) → $Destination" -ForegroundColor Green
                if ($Verbose) { Write-Host "    Reason: $Reason" -ForegroundColor DarkGray }
                $script:MoveCount++
            } catch {
                Write-Host "  ✗ Failed: $($item.Name) - $($_.Exception.Message)" -ForegroundColor Red
                $script:Errors += "Move failed: $Source"
            }
        }
    } elseif ($Verbose) {
        Write-Host "  ⊘ Not found: $Source" -ForegroundColor DarkGray
    }
}

# ═══════════════════════════════════════════════════════════════
# PHASE 1: Delete Broken Link Artifacts
# ═══════════════════════════════════════════════════════════════
Write-Host "PHASE 1: Removing Link Analysis Artifacts" -ForegroundColor Yellow
Write-Host "────────────────────────────────────────────────────────────────"

$LinkFiles = @(
    "broken_links.txt",
    "parsed_broken_links.txt",
    "parsed_broken_links_2.txt",
    "parsed_broken_links_3.txt",
    "parsed_broken_links_4.txt",
    "parsed_broken_links.csv"
)

foreach ($file in $LinkFiles) {
    Remove-ItemSafe -Path (Join-Path $VaultRoot $file) -Reason "Development artifact"
}

Write-Host ""

# ═══════════════════════════════════════════════════════════════
# PHASE 2: Delete Link Repair Scripts
# ═══════════════════════════════════════════════════════════════
Write-Host "PHASE 2: Removing Link Repair Scripts" -ForegroundColor Yellow
Write-Host "────────────────────────────────────────────────────────────────"

$ScriptFiles = @(
    "Check-BrokenMarkdownLinks.ps1",
    "Parse-BrokenLinks.ps1",
    "fix_links.ps1",
    "organize_images.ps1"
)

foreach ($file in $ScriptFiles) {
    Remove-ItemSafe -Path (Join-Path $VaultRoot $file) -Reason "Maintenance script not needed by users"
}

Write-Host ""

# ═══════════════════════════════════════════════════════════════
# PHASE 3: Delete Backup and Temporary Folders
# ═══════════════════════════════════════════════════════════════
Write-Host "PHASE 3: Removing Backup/Temp Folders" -ForegroundColor Yellow
Write-Host "────────────────────────────────────────────────────────────────"

$TempFolders = @(
    ".obsidian_backup_20251117_045252",
    "_gsdata_"
)

foreach ($folder in $TempFolders) {
    Remove-ItemSafe -Path (Join-Path $VaultRoot $folder) -Reason "Backup/system folder"
}

Write-Host ""

# ═══════════════════════════════════════════════════════════════
# PHASE 4: Delete Invalid Files
# ═══════════════════════════════════════════════════════════════
Write-Host "PHASE 4: Removing Invalid Files" -ForegroundColor Yellow
Write-Host "────────────────────────────────────────────────────────────────"

$InvalidFiles = @(
    "().md",
    "Untitled.base"
)

foreach ($file in $InvalidFiles) {
    Remove-ItemSafe -Path (Join-Path $VaultRoot $file) -Reason "Empty/invalid filename"
}

Write-Host ""

# ═══════════════════════════════════════════════════════════════
# PHASE 5: Delete Flat/ Folder (Duplicate System)
# ═══════════════════════════════════════════════════════════════
Write-Host "PHASE 5: Removing Duplicate System Files" -ForegroundColor Yellow
Write-Host "────────────────────────────────────────────────────────────────"

$FlatFolder = Join-Path $VaultRoot "00_VAULT_SYSTEM\Flat"
if (Test-Path $FlatFolder) {
    if ($DryRun) {
        $fileCount = (Get-ChildItem $FlatFolder -Recurse -File).Count
        Write-Host "  [DRY RUN] Would delete Flat/ folder ($fileCount files)" -ForegroundColor Gray
    } else {
        try {
            $fileCount = (Get-ChildItem $FlatFolder -Recurse -File).Count
            Remove-Item $FlatFolder -Recurse -Force
            Write-Host "  ✓ Deleted: Flat/ folder ($fileCount files)" -ForegroundColor Green
            $script:DeleteCount += $fileCount
        } catch {
            Write-Host "  ✗ Failed to delete Flat/ folder: $($_.Exception.Message)" -ForegroundColor Red
            $script:Errors += "Delete failed: Flat/ folder"
        }
    }
}

Write-Host ""

# ═══════════════════════════════════════════════════════════════
# PHASE 6: Organize Images
# ═══════════════════════════════════════════════════════════════
Write-Host "PHASE 6: Organizing Images" -ForegroundColor Yellow
Write-Host "────────────────────────────────────────────────────────────────"

$Images = @(
    "01_hubble_tension.png",
    "01_hubble_tension (3).png",
    "moral_universe_3d.png",
    "P4consciousness_fundamental_field_3d.png",
    "T02-Self-Referential-Logos.png",
    "Universal wave function collapse.png"
)

foreach ($image in $Images) {
    $sourcePath = Join-Path $VaultRoot $image
    if (Test-Path $sourcePath) {
        Move-ItemSafe -Source $sourcePath -Destination $AssetsDir -Reason "Organize assets"
    }
}

Write-Host ""

# ═══════════════════════════════════════════════════════════════
# SUMMARY REPORT
# ═══════════════════════════════════════════════════════════════
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " CLEANUP SUMMARY" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "  DRY RUN COMPLETE - No changes were made" -ForegroundColor Yellow
    Write-Host "  Run without -DryRun flag to execute changes" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ Deleted: $DeleteCount items" -ForegroundColor Green
    Write-Host "  ✓ Moved: $MoveCount items" -ForegroundColor Green
    
    if ($Errors.Count -gt 0) {
        Write-Host ""
        Write-Host "  ⚠️  Errors encountered: $($Errors.Count)" -ForegroundColor Red
        foreach ($err in $Errors) {
            Write-Host "     - $err" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " NEXT STEPS" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "  1. Run vault scanner:" -ForegroundColor White
Write-Host "     python 00_VAULT_SYSTEM\vault_refresh_v2.py --vault . --verbose" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Generate concept hubs:" -ForegroundColor White
Write-Host "     python 00_VAULT_SYSTEM\concept_hub_generator.py --db 00_VAULT_SYSTEM\theophysics.db" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Create cross-references:" -ForegroundColor White
Write-Host "     python 00_VAULT_SYSTEM\auto_linker.py" -ForegroundColor Gray
Write-Host ""
Write-Host "  4. Open GLOBAL_VAULT_STATS.md in Obsidian to view analytics" -ForegroundColor White
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
