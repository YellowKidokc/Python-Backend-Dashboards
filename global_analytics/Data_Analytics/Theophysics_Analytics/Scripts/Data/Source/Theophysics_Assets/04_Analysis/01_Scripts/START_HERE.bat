@echo off
cls
color 0A
echo.
echo     ╔══════════════════════════════════════════════════════════╗
echo     ║                                                          ║
echo     ║       CONNECTION SETUP - Cloudflare + PostgreSQL        ║
echo     ║                                                          ║
echo     ╚══════════════════════════════════════════════════════════╝
echo.
echo.
echo     What would you like to do?
echo.
echo        1. Install requirements (first time)
echo        2. Configure connections (interactive setup)
echo        3. Test existing connections
echo        4. Read documentation
echo        0. Exit
echo.
echo.
set /p choice="     Enter choice: "

if "%choice%"=="1" (
    echo.
    echo Starting installation...
    call INSTALL_CONNECTIONS.bat
    goto end
)

if "%choice%"=="2" (
    echo.
    echo Starting setup...
    call SETUP_CONNECTIONS.bat
    goto end
)

if "%choice%"=="3" (
    echo.
    echo Testing connections...
    call TEST_CONNECTIONS.bat
    goto end
)

if "%choice%"=="4" (
    echo.
    echo Opening documentation...
    start QUICK_START.md
    timeout /t 2 >nul
    goto menu
)

if "%choice%"=="0" (
    echo.
    echo Goodbye!
    timeout /t 1 >nul
    exit
)

echo.
echo Invalid choice!
timeout /t 2 >nul
goto menu

:end
echo.
echo Press any key to return to menu...
pause >nul
cls
goto menu

:menu
cls
goto :eof

