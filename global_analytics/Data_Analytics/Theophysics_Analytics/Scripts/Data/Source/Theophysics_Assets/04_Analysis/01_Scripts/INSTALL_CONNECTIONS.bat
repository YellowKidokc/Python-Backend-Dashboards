@echo off
echo ============================================================
echo  Installing Connection Utilities - Cloudflare + PostgreSQL
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
echo Installing requirements...
python -m pip install requests psycopg2-binary
echo.

REM Test imports
echo Testing imports...
python -c "import requests; print('✓ requests installed')"
python -c "import psycopg2; print('✓ psycopg2 installed')"
echo.

echo ============================================================
echo  Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Run: python connection_setup.py
echo   2. Follow the prompts to configure Cloudflare and PostgreSQL
echo.
pause

