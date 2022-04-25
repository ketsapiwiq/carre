from flask import Flask, render_template, jsonify, request, redirect, url_for
from src import pad, threads
import json,time

app = Flask(__name__, template_folder='../static', static_folder='../static')

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

@app.route("/api/add/pad",  methods=['POST','GET'])
def ajouterPad():
    start = time.time()
    name = request.form.get('name')
    parent = request.form.get('parent')
    adress = "p/9tm8" + name
    padAjout = pad.Pad(name, parent, adress)
    threadAjoutPad = threads.ThreadFunctionalities("ajoutPadFunc", padAjout)
    threadAjoutPad.start()
    threadAjoutPad.join()
    print(str(time.time() - start) + " seconds to add a pad")
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
