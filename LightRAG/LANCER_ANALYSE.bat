@echo off
REM Script pour lancer facilement l'analyse du document avec LightRAG
REM Double-cliquez sur ce fichier pour lancer le programme

echo.
echo ================================================================
echo           LIGHTRAG - ANALYSEUR DE DOCUMENTS
echo ================================================================
echo.
echo Ce script va lancer l'analyse de votre document :
echo "Presentation association mairie.docx"
echo.
echo Appuyez sur une touche pour continuer...
pause > nul

REM Se placer dans le bon dossier
cd /d "%~dp0"

echo.
echo [1/2] Verification de l'installation...
echo.
python verifier_installation.py

echo.
echo.
echo ================================================================
echo.
echo Si tous les tests sont [OK], le programme va demarrer.
echo Sinon, corrigez les problemes et relancez ce fichier.
echo.
echo ================================================================
echo.
echo Appuyez sur une touche pour lancer le programme principal...
echo (ou fermez cette fenetre pour annuler)
pause > nul

echo.
echo [2/2] Lancement du programme d'analyse...
echo.
python mon_premier_test.py

echo.
echo.
echo ================================================================
echo Programme termine !
echo ================================================================
echo.
pause
