from flask import Flask, render_template, jsonify, request, redirect, url_for
from src import fonctionnalities, pad
import json

app = Flask(__name__, template_folder='static')

##
#   fonction d'entrée redirige vers la page d'accueil
##
@app.route("/", methods=['POST','GET'])
def index():
    ## Redirection vers fonction permettant de récupérer les infos (controller)
    ## Affiche la page du pad
    return render_template('index.html')


@app.route("/initMenu")
def initMenu():
    # !Vérifier qu'il n'y ait rien dans le fichier
    menu = fonctionnalities.recupMenu()
    return json.dumps(menu)

@app.route("/ajouterPad",  methods=['POST','GET'])
def ajouterPad():
    print("La redirection marche !")
    name = request.form.get('name')
    parent = request.form.get('parent')
    adress = "p/9tm8" + name
    padAjout = pad.Pad(name, parent, adress)
    fonctionnalities.ajoutPadFunc(padAjout)

    print(url_for('index'))
    return redirect(url_for('index'))

app.run(debug = True)