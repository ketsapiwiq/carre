#!/bin/bash

# 1er param : nom du dossier dans lequel on veut installer le projet
    #if [ ! -d "$1" ] 
    #then
    #    mkdir "$1"
    #    echo "Création du fichier"
    #else
    #    cd "$1"
    #fi

    #Installation des dépendances
    fic="requirements.txt"
    pip install virutalenv
    virtualenv "$1"
    #Input Field Separator
    IFS=$'\n'
    for ligne in $(cat $fic)
    do
        pip install ligne
    done
    #Configuration et lancement de Flask
    export FLASK_APP=app.py
    printenv FLASK_APP
    export FLASK_ENV=development
    flask run
    xdg-open 127.0.0.1:5000/

