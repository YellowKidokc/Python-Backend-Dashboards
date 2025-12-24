@echo off
REM THEOPHYSICS ANALYTICS - Quick Runner
REM Usage: analyze.bat <file.md>
REM        analyze.bat compare <file1> <file2>
REM        analyze.bat scan <directory>
REM        analyze.bat aggregate

python "%~dp0run_analytics.py" %*
