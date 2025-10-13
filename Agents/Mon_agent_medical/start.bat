@echo off
echo ====================================
echo   Agent Medical - Demarrage
echo ====================================
echo.
echo Etape 1: Installation des dependances...
pip install -r requirements.txt
echo.
echo Etape 2: Demarrage de parlant-qna...
echo Ouvrez un autre terminal et executez: parlant-qna serve
echo.
echo Etape 3: Ajoutez des FAQ avec:
echo parlant-qna add -q "Question?" -a "Reponse"
echo.
echo Etape 4: Une fois parlant-qna lance, appuyez sur Entree pour demarrer l'agent...
pause
echo.
echo Demarrage de l'agent medical...
python my_healthcare_agent.py --module parlant_qna.module

