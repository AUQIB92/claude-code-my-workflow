@echo off
rem sync_to_docs.cmd - Windows launcher for scripts/sync_to_docs.sh
rem Delegates to Git Bash (shipped with Git for Windows). Requires bash on PATH
rem or at "%ProgramFiles%\Git\bin\bash.exe".
rem Usage: sync_to_docs.cmd [target]
setlocal
set "SCRIPT_DIR=%~dp0"

set "BASH_EXE="
if exist "%ProgramFiles%\Git\bin\bash.exe" set "BASH_EXE=%ProgramFiles%\Git\bin\bash.exe"
if "%BASH_EXE%"=="" if exist "%ProgramFiles(x86)%\Git\bin\bash.exe" set "BASH_EXE=%ProgramFiles(x86)%\Git\bin\bash.exe"
if "%BASH_EXE%"=="" (
    for %%b in (bash) do (
        for /f "delims=" %%p in ('where bash 2^>nul') do set "BASH_EXE=%%p"
    )
)
if "%BASH_EXE%"=="" (
    echo sync_to_docs: Git Bash not found. Install Git for Windows.
    exit /b 1
)

"%BASH_EXE%" "%SCRIPT_DIR%sync_to_docs.sh" %*
exit /b %ERRORLEVEL%
