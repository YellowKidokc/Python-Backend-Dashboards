@echo off
echo ============================================================
echo  Stats System Deployment Tool
echo ============================================================
echo.

cd /d "%~dp0"

echo What would you like to do?
echo.
echo   1. Create deployment package (for copying elsewhere)
echo   2. Deploy to another vault (local instance)
echo   3. Aggregate local stats to global
echo   4. List registered instances
echo   0. Exit
echo.
set /p choice="Choice: "

if "%choice%"=="1" goto package
if "%choice%"=="2" goto deploy
if "%choice%"=="3" goto aggregate
if "%choice%"=="4" goto list
if "%choice%"=="0" exit

:package
echo.
set /p output="Enter output folder (e.g., D:\Backup): "
python deploy_stats_system.py package "%output%"
pause
exit

:deploy
echo.
set /p target="Enter target vault path: "
set /p name="Enter instance name: "
set /p global="Enter global vault path: "
python deploy_stats_system.py deploy "%target%" "%name%" "%global%"
pause
exit

:aggregate
echo.
python deploy_stats_system.py aggregate
pause
exit

:list
echo.
python deploy_stats_system.py list
pause
exit

