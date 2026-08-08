@echo off
rem skill.cmd - Windows shim for scripts/skill.py
rem Usage: skill <skill-name> [args...] | skill --list
setlocal
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%skill.py" %*
exit /b %ERRORLEVEL%
