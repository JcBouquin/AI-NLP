@echo off
REM Script de demarrage du serveur MCP CrewAI avec variables d'environnement

cd /d "%~dp0"

REM Charger les variables depuis .env
for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
    set "%%a=%%b"
)

REM Lancer le serveur Python
".venv\Scripts\python.exe" server.py
