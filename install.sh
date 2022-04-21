#!/bin/bash

# Création de l'environnement virtuel Python
virtualenv . && echo ">> environnement virtuel créé."
# Activation dudit environnement
source bin/activate && echo ">> environnement virtuel activé."

# Installation des dépendances
pip install -r requirements.txt && echo ">> Dépendances installées"

# Configuration et lancement de Flask
export FLASK_APP=app.py
export FLASK_ENV=development
nohup flask run &!
xdg-open http://127.0.0.1:5000
tail -f nohup.out
