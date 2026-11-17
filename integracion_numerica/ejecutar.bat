@echo off
title Calculo Integral - Laboratorio de Integracion Numerica
cd /d "%~dp0"

set "PY_CMD=python"
where python >nul 2>nul
if %errorlevel% neq 0 (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        set "PY_CMD=py"
    )
)

echo =====================================================================
echo    CALCULO INTEGRAL · SIMULADOR DE INTEGRACION NUMERICA
echo =====================================================================
echo.
echo  Seleccione la forma en que desea mostrar el proyecto al profesor:
echo.
echo    [1] Interfaz Grafica de Escritorio (Ventana nativa interactiva)
echo    [2] Interfaz Web en el Navegador (Dashboard moderno interactivo)
echo    [3] Modo Consola Original (Tabla en terminal y ventana matplotlib)
echo.
set "OPCION=1"
set /p OPCION=" Elija una opcion (1, 2 o 3) [Por defecto: 1]: "

if "%OPCION%"=="2" goto MODO_WEB
if "%OPCION%"=="3" goto MODO_CONSOLA
goto MODO_GUI

:MODO_GUI
cls
echo Iniciando Interfaz Grafica de Escritorio...
%PY_CMD% app_gui.py
if %errorlevel% neq 0 (
    echo.
    echo [AVISO] La interfaz grafica devolvio un codigo de salida diferente de cero.
    echo Abriendo la version web de respaldo...
    %PY_CMD% app_web.py
)
goto FIN

:MODO_WEB
cls
echo Iniciando Interfaz Web interactiva...
%PY_CMD% app_web.py
goto FIN

:MODO_CONSOLA
cls
echo Ejecutando demostracion en consola...
%PY_CMD% main.py --cli --show
goto FIN

:FIN
echo.
echo Presione cualquier tecla para salir...
pause >nul
