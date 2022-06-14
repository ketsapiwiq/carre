import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir,"../"))

from src.app import app
import json

def test_ajout_renommer_suppression():
    app.test_client().post("/")
    #Ajout
    name = 'Dir1'
    response = app.test_client().post("/api/add/dir", json={'name': name, 'parent': 'Root'})
    assert response.status_code == 204
    assert verificationInMenu(name)
    #Renommage
    newName = 'Test_RenameDir1'
    response = app.test_client().post("/api/rename/dir", json={'oldName': name, 'newName': newName})
    assert response.status_code == 204
    assert verificationInMenu(newName)
    assert not verificationInMenu(name)
    #Suppression
    response = app.test_client().post("/api/remove/dir", json={'nameDir': newName, 'idCo': -1})
    assert response.status_code == 204
    assert not verificationInMenu(newName)


def test_ajout_suppression_avec_pads():
    app.test_client().post("/")
    #Ajout du répertoire
    name = "Dir2"
    response = app.test_client().post("/api/add/dir", json={'name': name, 'parent': 'Root'})
    assert response.status_code == 204
    assert verificationInMenu(name)

    #Ajout des pads dans le répertoire
    nameP1 = "Pad2_1"
    nameP2 = "Pad2_2"
    app.test_client().post("/api/add/pad", json={'name': nameP1, 'parent': name, 'idCo': -1})
    app.test_client().post("/api/add/pad", json={'name': nameP2, 'parent': name, 'idCo': -1})

    #Suppression du dossier
    response = app.test_client().post("/api/remove/dir", json={'nameDir': name, 'idCo': -1})
    assert response.status_code == 204
    assert not verificationInMenu(name)
    assert not verificationInMenu(nameP1)
    assert not verificationInMenu(nameP2)


def test_ajout_suppression_connecte():
    app.test_client().post("/")
    #Ajout du répertoire
    name = "Dir3"
    response = app.test_client().post("/api/add/dir", json={'name': name, 'parent': 'Root'})
    assert response.status_code == 204
    assert verificationInMenu(name)

    #Connexion
    response = app.test_client().post("/api/login", json={'pseudo': 'Erolf', 'password': 'erolf'})
    idCo = response.json["data"]

    #Ajout des pads
    nameP1 = "Pad3_1"
    nameP2 = "Pad3_2"
    nameP3 = "Pad3_3"
    app.test_client().post("/api/add/pad", json={'name': nameP1, 'parent': name, 'idCo':idCo})
    app.test_client().post("/api/add/pad", json={'name': nameP2, 'parent': name, 'idCo': idCo})
    app.test_client().post("/api/add/pad", json={'name': nameP3, 'parent': name, 'idCo': -1})
    #Suppression
    response = app.test_client().post("/api/remove/dir", json={'nameDir': name, 'idCo': idCo})
    assert response.status_code == 204
    assert not verificationInMenu(name)
    assert not verificationInMenu(nameP1)
    assert not verificationInMenu(nameP2)
    assert not verificationInMenu(nameP3)

def test_ajout_connecte_suppression_pas_connecte():
    app.test_client().post("/")
    #Ajout du répertoire
    name = "Dir4"
    response = app.test_client().post("/api/add/dir", json={'name': name, 'parent': 'Root'})
    assert response.status_code == 204
    assert verificationInMenu(name)
    #Connexion
    response = app.test_client().post("/api/login", json={'pseudo': 'Erolf', 'password': 'erolf'})
    idCo = response.json["data"]
    #Ajout des pads
    nameP1 = "Pad3_1"
    nameP2 = "Pad3_2"
    nameP3 = "Pad3_3"
    app.test_client().post("/api/add/pad", json={'name': nameP1, 'parent': name, 'idCo':idCo})
    app.test_client().post("/api/add/pad", json={'name': nameP2, 'parent': name, 'idCo': idCo})
    app.test_client().post("/api/add/pad", json={'name': nameP3, 'parent': name, 'idCo': -1})
    #Suppression du dossier en étant connecté
    response = app.test_client().post("/api/remove/dir", json={'nameDir': name, 'idCo': -1})
    assert response.status_code == 204
    assert verificationInMenu(name)
    assert verificationInMenu(nameP1)
    assert verificationInMenu(nameP2)
    assert verificationInMenu(nameP3)
    #Vraie suppression
    response = app.test_client().post("/api/remove/dir", json={'nameDir': name, 'idCo': idCo})
    assert response.status_code == 204
    assert not verificationInMenu(name)
    assert not verificationInMenu(nameP1)
    assert not verificationInMenu(nameP2)
    assert not verificationInMenu(nameP3)


def verificationInMenu(name):
    response = app.test_client().post("api/init/menu")
    menu = response.data.decode()
    menu = json.loads(menu)
    for i in menu:
        if(i['name'] == name):
            return True
    return False
