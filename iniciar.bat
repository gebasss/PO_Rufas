@echo off
rem Inicia o servidor local e abre a aplicacao no navegador.
cd /d "%~dp0backend"
start "" http://127.0.0.1:8000
..\.venv\Scripts\python.exe -m dietopt.server --port 8000
