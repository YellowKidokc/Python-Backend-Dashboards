@echo off
echo ============================================================
echo  Testing YOUR Cloudflare Credentials
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if requests is installed
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Installing requests...
    pip install requests
    echo.
)

echo Running test...
echo.
python test_my_cloudflare.py

pause

