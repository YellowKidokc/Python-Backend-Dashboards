@echo off
echo ============================================================
echo  Stats Generation Pipeline - Complete Workflow
echo ============================================================
echo.

cd /d "%~dp0"

echo Step 1: Generating local stats for all papers...
python generate_stats.py --all
if errorlevel 1 (
    echo ❌ Local stats generation failed
    pause
    exit /b 1
)
echo.

echo Step 2: Generating comparisons (all papers)...
python generate_comparisons.py Paper-01 Paper-02 Paper-03 Paper-04 Paper-05 Paper-06 Paper-07 Paper-08 Paper-09 Paper-10 Paper-11 Paper-12
echo.

echo Step 3: Generating global vault stats...
python generate_global.py
if errorlevel 1 (
    echo ❌ Global stats generation failed
    pause
    exit /b 1
)
echo.

echo ============================================================
echo  ✅ Complete! All statistics generated.
echo ============================================================
echo.
echo Check these folders:
echo   Stats\Local\         - Individual paper stats
echo   Stats\Comparisons\   - Multi-paper comparisons
echo   Stats\Global\        - Vault-wide analytics
echo.
pause

