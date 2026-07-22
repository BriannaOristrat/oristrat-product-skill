@echo off
chcp 65001 >nul
setlocal
title Oristrat Skill Dashboard - Update External Sources
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0refresh_skill_dashboard.ps1" -Mode Update -OpenReport
set "EXIT_CODE=%ERRORLEVEL%"
echo.
if "%EXIT_CODE%"=="0" (
  echo Update completed. Clean fast-forward repositories were updated and the report was opened.
) else (
  echo Update completed with safe skips for dirty, diverged, or unreachable repositories. Exit code: %EXIT_CODE%
)
pause
exit /b %EXIT_CODE%
