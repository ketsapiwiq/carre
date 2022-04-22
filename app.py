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


@app.route("/api/init/menu")
def initMenu():
    # !Vérifier qu'il n'y ait rien dans le fichier
    menu = fonctionnalities.recupMenu()
    return json.dumps(menu)

@app.route("/api/add/pad",  methods=['POST','GET'])
def ajouterPad():
    print("La redirection marche !")
    name = request.form.get('name')
    parent = request.form.get('parent')
    adress = "p/9tm8" + name
    padAjout = pad.Pad(name, parent, adress)
    fonctionnalities.ajoutPadFunc(padAjout)
    return redirect(url_for('index'))

@app.route("/api/remove/pad")
def removePad():
    print("Remove pad")

@app.route("/api/rename/pad")
def renamePad():
    print("Rename pad")

@app.route("/api/remove/dir")
def removeDir():
    print("Remove directory")

@app.route("/api/add/dir")
def addDir():
    print("Add directory")

@app.route("/api/rename/dir")
def renameDir():
    print("Rename directory")


app.run(debug = True)
