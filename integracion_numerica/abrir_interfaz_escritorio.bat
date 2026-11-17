@echo off
title Simulador Calculo Integral - GUI
cd /d "%~dp0"

set "PY_CMD=python"
where python >nul 2>nul
if %errorlevel% neq 0 (
    where py >nul 2>nul
    if %errorlevel% equ 0 set "PY_CMD=py"
)

%PY_CMD% app_gui.py
if %errorlevel% neq 0 (
    echo.
    echo Ocurrio un problema al abrir la interfaz de escritorio.
    pause
)
