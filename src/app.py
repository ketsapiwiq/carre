from flask import Flask, render_template, jsonify, request, redirect, url_for, Response
from src import pad, threads, directory
import json,time, configparser, re

## @nono : Attention aux chemins relatifs
## À changer par une variable d'environnement ou une clé de configuration ?
pathFlaskFolder = '../static'
# Fichier de configuration
ficIni = "config.ini"

app = Flask(__name__, template_folder=pathFlaskFolder, static_folder=pathFlaskFolder)


def getMenu():
    menu = None
    threadMenu = threads.ThreadFunctionalities("recupMenu", menu)
    threadMenu.start()
    threadMenu.join()
    menu = threadMenu.getStock()
    listMenu = []
    for i in range(0, len(menu)):
        if len(menu[i].data) > 1 :
            data = {"name": menu[i].tag, "parent": menu[i].data[0], "adresse": menu[i].data[1], "contenu": menu[i].data[2], "isDirectory": False}
        else:
            data = {"name": menu[i].tag, "parent": menu[i].data[0], "isDirectory": True}
        listMenu.append(data)
    return listMenu


##
#   fonction d'entrée : redirige vers la page d'accueil
##
@app.route("/", methods=['POST', 'GET'])
def index():
    #fonctionnalities.creaNbPad(10000)
    return render_template('index.html')


@app.route("/api/init/menu")
def initMenu():
    menu = getMenu()
    return json.dumps(menu)

@app.route("/api/init/var")
def initVariables():
    variables = dict()
    conf = configparser.ConfigParser()
    conf.read(ficIni)
    for key in conf['js']:
        variables[key] = conf['js'][key]
    return variables

@app.route("/api/add/pad",  methods=['POST'])
def ajouterPad():
    if (request.method == 'POST') :
        param = request.get_json()
        name = param['name']
        if not inputValidation(name):
            raise NameError ("Nom du pad non valide");

        parent = param['parent']
        adress = "p/9tm8" + name
        padAjout = pad.Pad(name, parent, adress, " ")
        threadAjoutPad = threads.ThreadFunctionalities("ajoutPadFunc", padAjout)
        threadAjoutPad.start()
        threadAjoutPad.join()

    # En fait ici l'idée c'est que le serveur retourne directement du json
    # et n'ai pas besoin de faire de redirection du tout : le client
    # reste sur la page d'index, et c'est le Javascript qui se charge de faire
    # la "navigation"
        return json.dumps(getMenu())

@app.route("/api/remove/pad", methods=['POST'])
def removePad():
    name = request.get_json()['name']
    threadRemovePad = threads.ThreadFunctionalities("remove", name)
    threadRemovePad.start()
    threadRemovePad.join()
    return json.dumps(getMenu())

@app.route("/api/rename/pad", methods=['POST'])
def renamePad():
    param = request.get_json()
    oldName = param['oldName']
    newName = param['newName']
    if not inputValidation(newName):
        raise NameError ("Nom du pad non valide")

    names = [oldName, newName]
    threadRenamePad = threads.ThreadFunctionalities("renamePad", names)
    threadRenamePad.start()
    threadRenamePad.join()
    return json.dumps(getMenu())

@app.route("/api/remove/dir", methods=['POST'])
def removeDir():
    nameDir = request.form.get('nameDir')
    threadDeleteDirectory = threads.ThreadFunctionalities("deleteDirectory", nameDir)
    threadDeleteDirectory.start()
    threadDeleteDirectory.join()
    return initMenu()

@app.route("/api/add/dir", methods=['POST'])
def addDir():
    name = request.get_json()['name']
    parent = request.get_json()['parent']
    if not inputValidation(name):
        raise NameError("Nom du dossier non valide")
    dir = directory.Directory(name, parent)
    threadAddDirectory = threads.ThreadFunctionalities("addDirectory",dir)
    threadAddDirectory.start()
    threadAddDirectory.join()
    return json.dumps(getMenu())

@app.route("/api/rename/dir", methods=['POST'])
def renameDir():
    paramAjax = request.get_json()
    oldName = paramAjax['oldName']
    newName = paramAjax['newName']
    if not inputValidation(newName):
        raise NameError ("Nom du dossier non valide");
    param = [oldName, newName]
    threadRenameDir = threads.ThreadFunctionalities("renameDirectory", param)
    threadRenameDir.start()
    threadRenameDir.join()
    return json.dumps(getMenu())

def inputValidation(input):
    match = re.search("[><?;!&]+", input)
    if match != None:
        return False
    else:
        return True


app.run(debug = True)


#voir log flask
