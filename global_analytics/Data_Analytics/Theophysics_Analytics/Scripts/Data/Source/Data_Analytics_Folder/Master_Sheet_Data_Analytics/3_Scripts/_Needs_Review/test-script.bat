@echo off
REM ============================================================================
REM WINDSURF VAULT - TEST SCRIPT
REM Quick test to verify the script works
REM ============================================================================

echo.
echo ========================================
echo   WINDSURF VAULT - SYSTEM TEST
echo ========================================
echo.

REM Check current directory
echo Current Directory:
cd
echo.

REM Check if PowerShell script exists
echo Checking for New-TheophysicsVault.ps1...
if exist "%~dp0New-TheophysicsVault.ps1" (
    echo [OK] Script found!
) else (
    echo [ERROR] Script NOT found!
    echo Expected location: %~dp0New-TheophysicsVault.ps1
    pause
    exit /b 1
)
echo.

REM Check PowerShell version
echo Checking PowerShell version...
powershell.exe -Command "$PSVersionTable.PSVersion"
echo.

REM Test script syntax
echo Testing script syntax...
powershell.exe -ExecutionPolicy Bypass -Command "try { Get-Content '%~dp0New-TheophysicsVault.ps1' | Out-Null; Write-Host '[OK] Script syntax is valid' -ForegroundColor Green } catch { Write-Host '[ERROR] Script has syntax errors' -ForegroundColor Red; Write-Host $_.Exception.Message }"
echo.

REM Run dry-run test
echo Running DRY-RUN test (no files will be created)...
echo.
powershell.exe -ExecutionPolicy Bypass -File "%~dp0New-TheophysicsVault.ps1" -DryRun -VaultName "Test-Vault"

echo.
echo ========================================
echo   TEST COMPLETE
echo ========================================
echo.
echo If you saw no errors above, the script is working!
echo.
echo Next steps:
echo   1. Double-click: new-vault.bat
echo   2. Or run: .\New-TheophysicsVault.ps1
echo.
pause
