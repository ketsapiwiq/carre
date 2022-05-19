from flask import Flask, render_template, jsonify, request, redirect, url_for, Response
from src import pad, threads, directory, functionalities
import json,time, configparser, re, queue, threading
from flask_socketio import SocketIO, emit, disconnect, send

###### Demain
# Faire la fonction de vérif
# Faire la dernière option : la création de sous-dossier
######
pathFlaskFolder = '../static'
# Fichier de configuration
ficIni = "config.ini"
#Queue d'évènements
queueEvent = queue.Queue()


async_mode = None
app = Flask(__name__, template_folder=pathFlaskFolder, static_folder=pathFlaskFolder)
socketio = SocketIO(app, async_mode=async_mode)

def supervisor():
    #Gère la queue d'évnements et lance les treads associés
    while True:
        data = queueEvent.get()
        param = data[1:]
        threadEvent = threads.ThreadFunctionalities(data[0], param)
        threadEvent.start()
        threadEvent.join()
        queueEvent.task_done()

        update()

# Fais les vérifs
# Envoie le broadcast à tous les clients
def update():

    menu = getMenu()
    #send(menu, json=True, broadcast=True)

@socketio.on('broadcast_message')
def handle_broadcast(data):
    print('received: ' + str(data))
    emit('broadcast_response', getMenu(), broadcast=True)


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

        adress = "p/9tm8" + name
        padAjout = pad.Pad(name, parent, adress, " ")

        dataPad=["ajoutPadFunc", name, parent, adress, " "]

        queueEvent.put(dataPad)
        #threadAjoutPad = threads.ThreadFunctionalities("ajoutPadFunc", padAjout)
        #threadAjoutPad.start()
        #threadAjoutPad.join()
        queueEvent.join()
        socketio.emit('broadcast_response', getMenu())
        return json.dumps(getMenu())

@app.route("/api/remove/pad", methods=['POST'])
def removePad():
    name = request.get_json()['name']
    data = ["remove", name]
    queueEvent.put(data)
    queueEvent.join()
    #threadRemovePad = threads.ThreadFunctionalities("remove", name)
    #threadRemovePad.start()
    #threadRemovePad.join()
    socketio.emit('broadcast_response', getMenu())
    return json.dumps(getMenu())

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
    #threadRenamePad = threads.ThreadFunctionalities("renamePad", names)
    #threadRenamePad.start()
    #threadRenamePad.join()
    socketio.emit('broadcast_response', getMenu())
    return json.dumps(getMenu())

@app.route("/api/remove/dir", methods=['POST'])
def removeDir():
    name = request.get_json()['nameDir']
    if not inputValidation(name) :
        raise NameError("Nom du répertoire non valide")

    data = ["remove", name]
    queueEvent.put(data)
    queueEvent.join()
    #threadRemovePad = threads.ThreadFunctionalities("remove", name)
    #threadRemovePad.start()
    #threadRemovePad.join()
    socketio.emit('broadcast_response', getMenu())
    return json.dumps(getMenu())

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

    #threadAddDirectory = threads.ThreadFunctionalities("addDirectory",dir)
    #threadAddDirectory.start()
    #threadAddDirectory.join()
    socketio.emit('broadcast_response', getMenu())
    return json.dumps(getMenu())

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
    #threadRenameDir = threads.ThreadFunctionalities("renameDirectory", param)
    #threadRenameDir.start()
    #threadRenameDir.join()
    socketio.emit('broadcast_response', getMenu())
    return json.dumps(getMenu())

def inputValidation(input):
    match = re.search("[><?;!&]+", input)
    if match != None:
        return False
    else:
        return True


app.run(debug = True)


#voir log flask
