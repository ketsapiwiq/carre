# 1er param : nom du dossier dans lequel on veut installer le projet
install(){
    if[! -d $1]; 
    then
        mkdir $1
    else
        cd $1
    fi

    #Installation des dépendances
    fic="requirements.txt"
    pip install virutalenv
    vitualenv $1
    #Input Field Separator
    IFS=$'\n'
    
    for ligne in $(cat $fic)
    do
        pip install ligne
    done
    #Configuration et lancement de Flask
    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run
    xdg-open 127.0.0.1:5000/ 
}