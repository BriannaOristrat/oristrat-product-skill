@echo off
chcp 65001 >nul
setlocal
title Oristrat Skill Dashboard - Check
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0refresh_skill_dashboard.ps1" -Mode Check -OpenReport
set "EXIT_CODE=%ERRORLEVEL%"
echo.
if "%EXIT_CODE%"=="0" (
  echo Check completed. The status report was opened.
) else (
  echo Check completed with repositories requiring manual attention. Exit code: %EXIT_CODE%
)
pause
exit /b %EXIT_CODE%
