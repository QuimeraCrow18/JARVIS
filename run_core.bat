@echo off
title JOSAMICK CORE AI - CENTRO DE MANDO C2
color 0a
cls

echo ===================================================
echo           JOSAMICK CORE AI - CORE OPERATIVO
echo ===================================================
echo [i] Detectando infraestructura local...
echo [i] Activando entorno virtual de Python (.venv)...

call .venv\Scripts\activate

if %errorlevel% neq 0 (
    echo [X] ERROR: No se pudo activar el entorno .venv. Asegurate de que la carpeta existe.
    pause
    exit /b
)

echo [📡] ENLACE ACTIVO: Lanzando servidor Flask...
echo [🔗] PANEL DISPONIBLE EN: http://127.0.0.1:5000/dashboard
echo ---------------------------------------------------
echo [!] Para apagar el servidor de forma segura, presiona CTRL+C
echo ---------------------------------------------------

python server.py

pause
