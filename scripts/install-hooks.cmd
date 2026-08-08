@echo off
rem install-hooks.cmd - Windows equivalent of scripts/install-hooks.sh
rem Points git at .githooks/ so every commit runs surface-sync + quality (>=80).
rem Usage: install-hooks.cmd
setlocal

for /f "delims=" %%i in ('git rev-parse --show-toplevel 2^>nul') do set "REPO_ROOT=%%i"
if "%REPO_ROOT%"=="" (
    echo install-hooks: not a git repository
    exit /b 1
)

if not exist "%REPO_ROOT%\.githooks" (
    echo install-hooks: .githooks/ not found at repo root
    exit /b 1
)

git config core.hooksPath .githooks
echo core.hooksPath -^> .githooks
echo   Every 'git commit' now runs surface-sync + quality (^>=80) gates.
echo   Bypass once:  SKIP_QUALITY_GATE=1 git commit ...   (quality only)
echo                 git commit --no-verify ...           (all hooks)
echo   Uninstall:    git config --unset core.hooksPath
exit /b %ERRORLEVEL%
