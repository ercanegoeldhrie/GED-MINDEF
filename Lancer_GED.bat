@echo off
title GED MINDEF - Système de Contrôle
echo Démarrage du serveur de la Défense...
cd /d %~dp0
call venv\Scripts\activate
start chrome "http://127.0.0.1:8000/"
python manage.py runserver
pause

echo Vérification des mises à jour...
git pull origin main