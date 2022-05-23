from flask import Flask, render_template, jsonify, request, redirect, url_for, Response
from src import pad, threads, directory, functionalities
import json,time, configparser, re, queue, threading, http.client
from flask_socketio import SocketIO, emit, disconnect, send
from src.conflicts import conflicts

###### To-Do
# --> Faire la fonction de errorManager (Créer conflit.py pour gérer toutes les possibilités d'erreurs)
# Coder la fonction retournant les erreurs
# Refactoriser le code (fnct Ajax, fichier functionnalities)
# Possibilité d'avoir plusieurs pads ayant le même nom dans des répertoires différents
# Possibilité d'avoir les pads et les répoertoires ayant le même nom
# Optimiser la fonction d'affichage du menu :')

#En plus de catcher les erreurs ->Renvoyer la dernière version du menu non-confllictuelle
######

##### BUG
# Pas de bugs !!!!! \o/
#####
pathFlaskFolder = '../static'
# Fichier de configuration
ficIni = "config.ini"
#Queue d'évènements
queueEvent = queue.Queue()


async_mode = None
app = Flask(__name__, template_folder=pathFlaskFolder, static_folder=pathFlaskFolder)
socketio = SocketIO(app, async_mode=async_mode)

def supervisor():
    #Gère la queue d'évnements et lance les threads associés
    while True:
        data = queueEvent.get()
        param = data[1:]
        try:
            conflicts.errorManager(data[0], param, getMenu())
        except (DuplicateError, InvalidNameError, InvalidActionError) as err:
            displayError(err.info)
        threadEvent = threads.ThreadFunctionalities(data[0], param)
        threadEvent.start()
        threadEvent.join()
        queueEvent.task_done()

        #update()

# Fais les vérifs
# Envoie le broadcast à tous les clients
def update():
    while True :
        time.sleep(30)
        socketio.emit('broadcast_response', getMenu())

def displayError(errorInformation):
    # Rediriger vers le javascript
    print(errorInformation)



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
    initThread = threading.Thread(target=supervisor, daemon=True)
    initThread.start()
    updateThread = threading.Thread(target=update, daemon=True)
    updateThread.start()
    print(getMenu())
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
        parent = param['parent']
        if not inputValidation(name) and not inputValidation(parent):
            raise NameError ("Nom du pad non valide");

        adress = "p/9tm8" + name.replace(" ","")
        padAjout = pad.Pad(name, parent, adress, " ")

        dataPad=["ajoutPadFunc", name, parent, adress, " "]

        queueEvent.put(dataPad)
        queueEvent.join()

        return ("", http.HTTPStatus.NO_CONTENT)

@app.route("/api/remove/pad", methods=['POST'])
def removePad():
    name = request.get_json()['name']
    data = ["remove", name]
    queueEvent.put(data)
    queueEvent.join()
    return ("", http.HTTPStatus.NO_CONTENT)

@app.route("/api/rename/pad", methods=['POST'])
def renamePad():
    param = request.get_json()
    oldName = param['oldName']
    newName = param['newName']
    if not inputValidation(newName) and not inputValidation(oldName):
        raise NameError ("Nom du pad non valide")

    data = ["rename",oldName, newName]
    queueEvent.put(data)
    queueEvent.join()
    return ("", http.HTTPStatus.NO_CONTENT)

@app.route("/api/remove/dir", methods=['POST'])
def removeDir():
    name = request.get_json()['nameDir']
    if not inputValidation(name) :
        raise NameError("Nom du répertoire non valide")

    data = ["remove", name]
    queueEvent.put(data)
    queueEvent.join()
    return ("", http.HTTPStatus.NO_CONTENT)

@app.route("/api/add/dir", methods=['POST'])
def addDir():
    name = request.get_json()['name']
    parent = request.get_json()['parent']
    if not inputValidation(name) and not inputValidation(parent):
        raise NameError("Nom du dossier non valide")
    dir = directory.Directory(name, parent)
    data = ["addDirectory", dir]
    queueEvent.put(data)
    queueEvent.join()

    return ("", http.HTTPStatus.NO_CONTENT)

@app.route("/api/rename/dir", methods=['POST'])
def renameDir():
    paramAjax = request.get_json()
    oldName = paramAjax['oldName']
    newName = paramAjax['newName']
    if not inputValidation(newName) and not inputValidation(oldName):
        raise NameError ("Nom du dossier non valide")
    data = ["rename", oldName, newName]
    queueEvent.put(data)
    queueEvent.join()
    return ("", http.HTTPStatus.NO_CONTENT)

def inputValidation(input):
    match = re.search("[><?;!&]+", input)
    if match != None:
        return False
    else:
        return True


app.run(debug = True)


#voir log flask
