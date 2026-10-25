@echo off
REM ==========================================================
REM  Genera el ejecutable portable de la aplicación (Windows)
REM  Resultado: dist\BusinessAnalytics_Guia9.exe
REM  Requiere: Python 3.13 (o similar) con pip, solo en el equipo
REM  donde se construye. El .exe resultante NO necesita Python.
REM ==========================================================
cd /d "%~dp0"
python -m pip install --upgrade pyinstaller matplotlib
python -m PyInstaller --onefile --windowed --clean --name BusinessAnalytics_Guia9 Aplicacion_Guia9_Business_Analytics.py
echo.
echo Listo. El ejecutable esta en la carpeta dist\BusinessAnalytics_Guia9.exe
pause
