@echo off
title Simulador Calculo Integral - Web
cd /d "%~dp0"

set "PY_CMD=python"
where python >nul 2>nul
if %errorlevel% neq 0 (
    where py >nul 2>nul
    if %errorlevel% equ 0 set "PY_CMD=py"
)

%PY_CMD% app_web.py
if %errorlevel% neq 0 (
    echo.
    echo Intentando abrir index.html directamente en el navegador...
    start "" "web\index.html"
    pause
)
