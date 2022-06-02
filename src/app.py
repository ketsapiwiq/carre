from flask import Flask, render_template, jsonify, request, redirect, url_for, Response
from src import pad, threads, directory, menu
import json,time, configparser, re, queue, threading, http.client, bcrypt, sqlite3
from flask_socketio import SocketIO, emit, disconnect, send
from src.conflicts import Errors, conflicts

###### To-Do
# Connexion :
#             - Créer un bouton de déconnexion
#             - Faire les vérifs pour les suppressions
#             - Créer un variable contenant l'ID de celui qui est connecté
#             - Changer le machin dans le menu pour que ce soit l'id de la personne et pas son pseudo
#             - Renvoyer les erreurs
# Implémenter le système de gestion de droits
# Implémenter BD pour les pads
# Optimiser la fonction d'affichage du menu :')
######

##### BUG(S)
#
#####
pathFlaskFolder = '../static'
# Fichier de configuration
ficIni = "config.ini"
#Queue d'évènements
queueEvent = queue.Queue()

menuCarre = menu.Menu()

idConnexion = -1

async_mode = None
app = Flask(__name__, template_folder=pathFlaskFolder, static_folder=pathFlaskFolder)
socketio = SocketIO(app, async_mode=async_mode)

def supervisor():
    #Gère la queue d'évnements et lance les threads associés
    while True:
        data = queueEvent.get()
        param = data[1:]
        if(conflictVerification(data[0], param)):
            threadEvent = threads.ThreadFunctionalities(data[0], param, menuCarre)
            threadEvent.start()
            threadEvent.join()
            queueEvent.task_done()

def conflictVerification(action, param):
    try:
        conflicts.errorManager(action, param, getMenu())
    except (Errors.InvalidNameError, Errors.DuplicateError, Errors.InvalidActionError) as err :
        displayError(str(err.info))
        return False
    return True

# Fais les vérifs
# Envoie le broadcast à tous les clients
def update():
    while True :
        time.sleep(2)
        socketio.emit('broadcast_response', getMenu())

def displayError(errorInformation):
    socketio.emit('error', errorInformation)

def getMenu():
    menu = None
    threadMenu = threads.ThreadFunctionalities("recupMenu", menu, menuCarre)
    threadMenu.start()
    threadMenu.join()
    menu = threadMenu.getStock()
    listMenu = []
    for i in range(0, len(menu)):
        if len(menu[i].data) > 1 :
            data = {"name": menu[i].tag, "parent": menu[i].data[0], "adresse": menu[i].data[1], "contenu": menu[i].data[2], "isDirectory": False, "proprietaire": menu[i].data[3]}
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
    # Création de la base de donénes si elle n'existe pas
    try:
        conn = sqlite3.connect('file:users.db?mode=rw', uri=True)
        conn.close()
    except sqlite3.OperationalError as err :
        create_db()
    return render_template('index.html', idConnexion=idConnexion)


@app.route("/connectionRedirect", methods=["POST"])
def redirection():
    return render_template('connexion.html')

##
# Vérifie les identifiants
##
@app.route("/api/login", methods=["POST"])
def login():
    if(request.method == 'POST'):
        pseudo = request.form['pseudo']
        password = request.form['password']
    try:
        conn = sqlite3.connect('users.db')
    except sqlite3.OperationalError as err :
        print("La base de données n'existe pas")

    #Vérifier que le pseudo soit bien enregistré dans la bd
    cursor = conn.cursor()

    cursor.execute("""SELECT pseudo, password, id from users WHERE pseudo=:pseudo""", {"pseudo": pseudo})
    result = cursor.fetchall()
    if len(result) != 0:
        #Si trouvé, récupérer le mot de passe et faire la vérif
        password = password.encode(encoding='UTF-8', errors='xmlcharrefreplace')
        if bcrypt.checkpw(password, result[0][1]):
            global idConnexion
            idConnexion = result[0][2]
        else :
            print("Identifiants incorrects")
    cursor.close()
    conn.close()
    return render_template('index.html', idConnexion=idConnexion)

@app.route("/api/signup", methods=["POST"])
def sign_up():
    if(request.method == 'POST'):
        pseudo = request.form['pseudo']
        password = request.form['password']
        if not inputValidation(pseudo):
            raise Exception
    try :
        conn = sqlite3.connect('users.db')
    except sqlite3.OperationalError as err :
        print("La base de données n'existe pas");

    cursor = conn.cursor()

    #Vérifier que l'utilisateur n'existe pas
    cursor.execute("SELECT pseudo FROM users WHERE pseudo= :pseudo", {"pseudo": pseudo})
    result = cursor.fetchall()
    if len(result) == 0 :
        password = password.encode(encoding='UTF-8', errors='xmlcharrefreplace')
        try:
            # Insertion d'un nouvel utilisateur
            cursor.execute("INSERT INTO users(pseudo, password) VALUES (:pseudo, :password)", {"pseudo" : pseudo, "password" : bcrypt.hashpw(password, bcrypt.gensalt())})
            conn.commit()

            #Récupération de l'id
            cursor.execute("SELECT id FROM users WHERE pseudo=:pseudo", {"pseudo": pseudo})
            result = cursor.fetchall()
            global idConnexion
            idConnexion = result[0][0]

        except sqlite3.Error as e :
            print("Erreur lors de l'insertion de données")
    else :
        print("Vous êtes déjà enregistré dans la base de données, authentifiez-vous")
    cursor.close()
    conn.close()
    return render_template('index.html', idConnexion=idConnexion)


@app.route("/api/deconnect", methods=["POST"])
def deconnect():
    global idConnexion
    idConnexion = -1
    return render_template('index.html', idConnexion=idConnexion)

def create_db():
    print("Création de la base de données")
    try:
        conn = sqlite3.connect('users.db')
        sql = '''CREATE TABLE users (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  pseudo TEXT NOT NULL,
                  password TEXT NOT NULL
           );'''
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        print("Connexion SQLite est fermée")
    except sqlite3.Error as error:
        print("Erreur lors de la création de la table SQLite", error)

@app.route("/api/deleteAccount", methods=["POST"])
def deleteAccount():
    global idConnexion
    #Update de tous les pads de l'utilisateur
    data = ["deleteAccount", idConnexion]
    queueEvent.put(data)
    queueEvent.join()

    #Suppression de la base de données
    try :
        conn = sqlite3.connect('users.db')
    except sqlite3.OperationalError as err :
        print("La base de données n'existe pas")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=:id", {"id": idConnexion})
        conn.commit()

        cursor.execute("SELECT pseudo FROM users")
        result = cursor.fetchall()
        print(result)

        cursor.close()
        conn.close()
    except sqlite.DatabaseError as err:
        print("DatabaseError : " + err)

    idConnexion = -1
    return render_template("index.html", idConnexion=idConnexion)

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

        adress = "p/9tm8" + name.replace(" |.","")

        dataPad=["ajoutPadFunc", name, parent, adress, " ", idConnexion]

        queueEvent.put(dataPad)
        queueEvent.join()

        return ("", http.HTTPStatus.NO_CONTENT)


@app.route("/api/remove/pad", methods=['POST'])
def removePad():
    name = request.get_json()['name']
    parent = request.get_json()['parent']
    data = ["removePad", name, parent, idConnexion]
    queueEvent.put(data)
    queueEvent.join()
    return ("", http.HTTPStatus.NO_CONTENT)

@app.route("/api/rename/pad", methods=['POST'])
def renamePad():
    param = request.get_json()
    oldName = param['oldName']
    newName = param['newName']
    parent = param['parent']
    if not inputValidation(newName) and not inputValidation(oldName):
        raise NameError ("Nom du pad non valide")
    data = ["renamePad",oldName, newName, parent]
    queueEvent.put(data)
    queueEvent.join()
    return ("", http.HTTPStatus.NO_CONTENT)

@app.route("/api/remove/dir", methods=['POST'])
def removeDir():
    name = request.get_json()['nameDir']
    if not inputValidation(name) :
        raise NameError("Nom du répertoire non valide")

    data = ["removeDir", name]
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
    data = ["renameDir", oldName, newName]
    queueEvent.put(data)
    queueEvent.join()
    return ("", http.HTTPStatus.NO_CONTENT)

def inputValidation(input):
    match = re.search("[><?;!&,]+", input)
    if match != None:
        return False
    else:
        return True


app.run(debug = True)


#voir log flask
