from flask import Flask, render_template, jsonify, request
from Controller import fonctionnalities
from Controller import pad
import json

app = Flask(__name__, template_folder='static')

##
#   fonction d'entrée redirige vers la page d'accueil
##
@app.route("/")
def index():
    ## Redirection vers fonction permettant de récupérer les infos (controller)
    ## Affiche la page du pad
    return render_template('index.html')


@app.route("/initMenu")
def initMenu():
    # !Vérifier qu'il n'y ait rien dans le fichier
    menu = fonctionnalities.recupMenu()
    return json.dumps(menu)

@app.route("/ajouterPad",  methods=['POST'])
def ajouterPad():
    # Besoin du pad donc du nom et du parent
    # R2cupération des paramètres avec la méthode GET <= Pas terrible, POST c'est mieux
    #request.args.get()
    #padAjout = pad.Pad("","","")
    #fonctionnalities.ajoutPadFunc()
    print("La redirection marche !")
    return render_template('index.html')
app.run(debug = True)