@echo off
REM ============================================================================
REM WINDSURF VAULT SCAFFOLDING - QUICK LAUNCHER
REM ============================================================================

echo.
echo ========================================
echo   WINDSURF VAULT SCAFFOLDING
echo ========================================
echo.

REM Check if PowerShell script exists
if not exist "%~dp0New-TheophysicsVault.ps1" (
    echo ERROR: New-TheophysicsVault.ps1 not found!
    echo Please ensure the PowerShell script is in the same directory.
    pause
    exit /b 1
)

REM Run PowerShell script in interactive mode
powershell.exe -ExecutionPolicy Bypass -File "%~dp0New-TheophysicsVault.ps1" -StructureType Interactive

echo.
echo ========================================
echo   COMPLETE
echo ========================================
echo.
pause
