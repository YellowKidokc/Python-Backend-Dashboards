@echo off
REM THEOPHYSICS Word Ontology - Launcher
REM Starts the interactive command-line interface

echo ========================================
echo THEOPHYSICS WORD ONTOLOGY SYSTEM
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import sentence_transformers" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    echo.
    cd Scripts
    pip install -r requirements.txt
    cd ..
    echo.
    echo Dependencies installed.
    echo.
)

REM Launch the CLI
python ontology-cli.py

pause
