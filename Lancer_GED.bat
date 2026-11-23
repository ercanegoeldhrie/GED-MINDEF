@echo off
title GED MINDEF - Système de Contrôle
cd /d %~dp0

if not exist .env (
    echo Fichier .env manquant : copiez .env.example en .env et renseignez DJANGO_SECRET_KEY.
    pause
    exit /b 1
)

echo Vérification des mises à jour...
git pull origin main

echo Démarrage du serveur de la Défense...
call venv\Scripts\activate
python manage.py migrate --noinput
start chrome "http://127.0.0.1:8000/"
python manage.py runserver
pause
