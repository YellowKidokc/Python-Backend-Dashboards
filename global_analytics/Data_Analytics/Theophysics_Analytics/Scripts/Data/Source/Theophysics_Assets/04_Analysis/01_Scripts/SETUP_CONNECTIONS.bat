@echo off
echo ============================================================
echo  Connection Setup - Interactive Configuration
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if requirements are installed
python -c "import requests; import psycopg2" >nul 2>&1
if errorlevel 1 (
    echo Requirements not installed!
    echo Running installer...
    echo.
    call INSTALL_CONNECTIONS.bat
)

echo Starting interactive setup...
echo.
python connection_setup.py

pause

