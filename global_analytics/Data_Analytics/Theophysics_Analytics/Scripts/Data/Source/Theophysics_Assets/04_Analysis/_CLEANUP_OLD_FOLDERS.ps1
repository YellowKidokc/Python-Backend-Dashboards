# Cleanup Script for Old 04_Analysis Folders
# Run this AFTER verifying the new structure works correctly
#
# This script removes the old folder structure that has been migrated
# to the new numbered folders (01_Scripts, 02_System, etc.)

$basePath = "D:\THEOPHYSICS_MASTER\00_VAULT_SYSTEM\04_Analysis"

Write-Host "=== Theophysics 04_Analysis Cleanup Script ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will remove OLD folders that have been migrated to new structure."
Write-Host "Make sure you have verified the new folders work correctly first!"
Write-Host ""

$oldFolders = @(
    "scripts",
    "System",
    "Templates",
    "Dashboards",
    "Hubs",
    "Wizards",
    "Data Analytics",
    "Master Sheets",
    "ARCHIVE",
    "00_CURRENT",
    "02_Foundations",
    "05_Doctrine",
    "GLOBAL"
)

$oldFiles = @(
    "README_v2.md",
    "DASHBOARD.md",
    "00-SERIES-INDEX.md",
    "analyze_coherence.py",
    "00-REORGANIZATION-COMPLETE.md",
    "PAPER-STRUCTURE-TEMPLATE.md",
    "ENHANCEMENT-WORKFLOW.md",
    "PAPER-1-COMPLETE.md",
    "VAULT_ANALYSIS_REPORT.md",
    "COHERENCE_SYSTEM_DOCUMENTATION.md"
)

Write-Host "Folders to be removed:" -ForegroundColor Yellow
foreach ($folder in $oldFolders) {
    $fullPath = Join-Path $basePath $folder
    if (Test-Path $fullPath) {
        Write-Host "  - $folder" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Files to be removed:" -ForegroundColor Yellow
foreach ($file in $oldFiles) {
    $fullPath = Join-Path $basePath $file
    if (Test-Path $fullPath) {
        Write-Host "  - $file" -ForegroundColor Red
    }
}

Write-Host ""
$confirm = Read-Host "Type 'DELETE' to proceed with cleanup, or anything else to cancel"

if ($confirm -eq "DELETE") {
    Write-Host ""
    Write-Host "Removing old folders..." -ForegroundColor Yellow

    foreach ($folder in $oldFolders) {
        $fullPath = Join-Path $basePath $folder
        if (Test-Path $fullPath) {
            Remove-Item -Path $fullPath -Recurse -Force
            Write-Host "  Removed: $folder" -ForegroundColor Green
        }
    }

    Write-Host ""
    Write-Host "Removing old files..." -ForegroundColor Yellow

    foreach ($file in $oldFiles) {
        $fullPath = Join-Path $basePath $file
        if (Test-Path $fullPath) {
            Remove-Item -Path $fullPath -Force
            Write-Host "  Removed: $file" -ForegroundColor Green
        }
    }

    # Remove .gitkeep files from new structure (optional)
    Write-Host ""
    Write-Host "Cleaning up .gitkeep placeholder files..." -ForegroundColor Yellow
    Get-ChildItem -Path $basePath -Recurse -Filter ".gitkeep" | Remove-Item -Force

    Write-Host ""
    Write-Host "=== Cleanup Complete ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "New structure is now clean. Old files have been removed."

} else {
    Write-Host ""
    Write-Host "Cleanup cancelled. No files were removed." -ForegroundColor Yellow
}
