@echo off
setlocal enabledelayedexpansion

set "target=%cd%"
set "ts=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%"
set "ts=%ts: =0%"
set "out=%target%\AllCombined_%ts%.txt"

echo # Combined Document (%~n0) > "%out%"
echo.>> "%out%"
echo Generated: %date% %time% >> "%out%"
echo.>> "%out%"
echo --- >> "%out%"
echo.>> "%out%"

for %%F in ("%target%\*.md" "%target%\*.txt") do (
  if exist "%%~fF" (
    echo ### Source: %%~nxF >> "%out%"
    type "%%~fF" >> "%out%"
    echo.>> "%out%"
    echo --- >> "%out%"
    echo.>> "%out%"
  )
)

echo Wrote: %out%
endlocal
