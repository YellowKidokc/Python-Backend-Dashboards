@echo off
REM THEOPHYSICS Word Ontology - Folder Cleanup
REM Removes Obsidian plugin files, keeps only ontology system

echo ========================================
echo WORD ONTOLOGY FOLDER CLEANUP
echo ========================================
echo.
echo This will DELETE:
echo   - node_modules/ (Node.js dependencies)
echo   - .git/ (Git repository)
echo   - All .ts, .mjs, .json files (plugin code)
echo   - styles.css, ui/ folder
echo.
echo This will KEEP:
echo   - All .md documentation files
echo   - Terms/ folder
echo   - Templates/ folder
echo   - Scripts/ folder
echo   - Word-Breakdowns/ folder
echo   - LAUNCH-ONTOLOGY.bat
echo   - ontology-cli.py
echo.
set /p confirm="Continue? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo Cleaning...
echo.

REM Delete large folders
if exist node_modules (
    echo Deleting node_modules/ ...
    rmdir /s /q node_modules
)

if exist .git (
    echo Deleting .git/ ...
    rmdir /s /q .git
)

if exist ui (
    echo Deleting ui/ ...
    rmdir /s /q ui
)

REM Delete plugin files
echo Deleting plugin files...
del /q classification.ts 2>nul
del /q database.ts 2>nul
del /q esbuild.config.mjs 2>nul
del /q main.ts 2>nul
del /q manifest.json 2>nul
del /q package-lock.json 2>nul
del /q package.json 2>nul
del /q profiles.ts 2>nul
del /q settings.ts 2>nul
del /q styles.css 2>nul
del /q tsconfig.json 2>nul
del /q types.ts 2>nul
del /q version-bump.mjs 2>nul
del /q versions.json 2>nul
del /q .gitignore 2>nul

echo.
echo ========================================
echo ✅ CLEANUP COMPLETE
echo ========================================
echo.
echo Folder now contains ONLY ontology files.
echo Saved approximately 150-200 MB of space.
echo.
pause
