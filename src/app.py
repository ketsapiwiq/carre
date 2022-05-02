from flask import Flask, render_template, jsonify, request, redirect, url_for
from src import pad, threads
import json,time, configparser, re

## @nono : Attention aux chemins relatifs
## À changer par une variable d'environnement ou une clé de configuration ?
app = Flask(__name__, template_folder='../static', static_folder='../static')

# Fichier de configuration
ficIni = "config.ini"

##
#   fonction d'entrée redirige vers la page d'accueil
##
@app.route("/", methods=['POST','GET'])
def index():
    #fonctionnalities.creaPad(10000)
    return render_template('index.html')


@app.route("/api/init/menu")
def initMenu():
    menu = None
    threadMenu = threads.ThreadFunctionalities("recupMenu", menu)
    threadMenu.start()
    threadMenu.join()
    menu = threadMenu.getStock()
    return json.dumps(menu)

@app.route("/api/init/var")
def initVariables():
    variables = dict()
    conf = configparser.ConfigParser()
    conf.read(ficIni)
    for key in conf['js']:
        variables[key] = conf['js'][key]
    return variables

@app.route("/api/add/pad",  methods=['POST','GET'])
def ajouterPad():
    name = request.form.get('name')
    #Faire la vérification
    #Prions la sainte regex pour que ça marche
    #\d+|[A-Z]+|[a-z]+)+/g
    #[><?;!]+
    match = re.search("[><?;!&]+", name)
    if match != None:
        raise NameError ("Nom du pad non valide");
        #print("Tentative d'attaque détectée, le FBI est à vos trousses");

    parent = request.form.get('parent')

    adress = "p/9tm8" + name
    padAjout = pad.Pad(name, parent, adress)
    threadAjoutPad = threads.ThreadFunctionalities("ajoutPadFunc", padAjout)
    threadAjoutPad.start()
    threadAjoutPad.join()

    # En fait ici l'idée c'est que le serveur retourne directement du json
    # et n'ai pas besoin de faire de redirection du tout : le client
    # reste sur la page d'index, et c'est le Javascript qui se charge de faire
    # la "navigation"

    return initMenu()

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

@app.route("/api/rename/dir", methods=['POST'])
def renameDir():
    oldName = request.form.get('oldName')
    newName = request.form.get('newName')
    match = re.search("[><?;!&]+", newName)
    if match != None:
        raise NameError ("Nom du dossier non valide");
    param = [oldName, newName]
    threadRenameDir = threads.ThreadFunctionalities("renameDirectory", param)
    threadRenameDir.start()
    threadRenameDir.join()
    return initMenu()


app.run(debug = True)


#voir log falsk
