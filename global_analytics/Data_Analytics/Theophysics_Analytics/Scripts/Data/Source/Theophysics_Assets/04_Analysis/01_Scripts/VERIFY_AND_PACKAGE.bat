@echo off
echo ============================================================
echo  Verify and Package Stats System
echo ============================================================
echo.

cd /d "%~dp0"

echo Step 1: Verifying all files are present...
echo.

set missing=0

if not exist "generate_stats.py" (
    echo ❌ Missing: generate_stats.py
    set missing=1
)
if not exist "generate_comparisons.py" (
    echo ❌ Missing: generate_comparisons.py
    set missing=1
)
if not exist "generate_global.py" (
    echo ❌ Missing: generate_global.py
    set missing=1
)
if not exist "deploy_stats_system.py" (
    echo ❌ Missing: deploy_stats_system.py
    set missing=1
)
if not exist "config.yaml" (
    echo ❌ Missing: config.yaml
    set missing=1
)
if not exist "RUN_ALL_STATS.bat" (
    echo ❌ Missing: RUN_ALL_STATS.bat
    set missing=1
)
if not exist "STATS_README.md" (
    echo ❌ Missing: STATS_README.md
    set missing=1
)
if not exist "DEPLOYMENT_GUIDE.md" (
    echo ❌ Missing: DEPLOYMENT_GUIDE.md
    set missing=1
)

if %missing%==1 (
    echo.
    echo ❌ Some files are missing! Please check above.
    pause
    exit /b 1
)

echo ✅ All core files present
echo.

echo Step 2: Checking Stats folder structure...
echo.

if not exist "..\..\..\Stats" (
    echo Creating Stats folder...
    mkdir "..\..\..\Stats"
    mkdir "..\..\..\Stats\Local"
    mkdir "..\..\..\Stats\Comparisons"
    mkdir "..\..\..\Stats\Global"
    echo ✅ Stats folders created
) else (
    echo ✅ Stats folder exists
)
echo.

echo Step 3: Verifying config.yaml settings...
python -c "import yaml; config = yaml.safe_load(open('config.yaml')); print(f\"Instance type: {config['instance']['type']}\"); print(f\"Instance name: {config['instance']['name']}\"); print(f\"Exclude patterns: {len(config['scanning']['exclude_patterns'])}\"); print('✅ Config valid')"
echo.

echo Step 4: Creating deployment package...
echo.

set timestamp=%date:~-4%%date:~-10,2%%date:~-7,2%-%time:~0,2%%time:~3,2%
set timestamp=%timestamp: =0%

set package_name=stats-system-%timestamp%
set package_path=..\..\..\..\..\%package_name%

echo Creating package: %package_path%
echo.

mkdir "%package_path%"

REM Copy core files
copy generate_stats.py "%package_path%\" >nul
copy generate_comparisons.py "%package_path%\" >nul
copy generate_global.py "%package_path%\" >nul
copy deploy_stats_system.py "%package_path%\" >nul
copy config.yaml "%package_path%\" >nul
copy RUN_ALL_STATS.bat "%package_path%\" >nul
copy STATS_README.md "%package_path%\" >nul
copy DEPLOYMENT_GUIDE.md "%package_path%\" >nul
copy DEPLOY_STATS_SYSTEM.bat "%package_path%\" >nul
copy VERIFY_AND_PACKAGE.bat "%package_path%\" >nul

REM Create Stats folders
mkdir "%package_path%\Stats"
mkdir "%package_path%\Stats\Local"
mkdir "%package_path%\Stats\Comparisons"
mkdir "%package_path%\Stats\Global"

echo ✅ Package created
echo.

echo Step 5: Creating ZIP archive...
echo.

REM Use PowerShell to create ZIP
powershell -command "Compress-Archive -Path '%package_path%' -DestinationPath '%package_path%.zip' -Force"

if exist "%package_path%.zip" (
    echo ✅ ZIP created: %package_path%.zip
    echo.
    echo You can now copy this ZIP file anywhere and extract it.
) else (
    echo ⚠️  ZIP creation failed. Package folder is ready but not zipped.
)

echo.
echo ============================================================
echo  ✅ Verification and Packaging Complete!
echo ============================================================
echo.
echo Package location: %package_path%
if exist "%package_path%.zip" echo ZIP file: %package_path%.zip
echo.
echo To deploy to another vault:
echo   1. Extract the ZIP
echo   2. Run DEPLOY_STATS_SYSTEM.bat
echo   3. Choose option 2 (Deploy to another vault)
echo.
pause

