@echo off
REM Script pour verifier l'installation sans lancer l'analyse
REM Double-cliquez sur ce fichier pour verifier que tout est pret

echo.
echo ================================================================
echo      VERIFICATION DE L'INSTALLATION LIGHTRAG
echo ================================================================
echo.

REM Se placer dans le bon dossier
cd /d "%~dp0"

python verifier_installation.py

echo.
echo.
echo Si tout est [OK], vous pouvez lancer : LANCER_ANALYSE.bat
echo.
pause
