from src.app import app
import json

def test_ajout_renommage_suppression_pads():
    app.test_client().post("/")
    # Ajout
    name = "Coucou je suis un pad"
    parent = "Documentation"
    idCo = -1
    response = app.test_client().post("/api/add/pad",json={'name': name, 'parent': parent, 'idCo':idCo})
    assert response.status_code == 204
    assert verificationPad(name)

    #Renommage
    newName = "Padoum"
    response = app.test_client().post("/api/rename/pad", json={'oldName': name, 'newName': newName, 'parent': parent})
    assert response.status_code == 204
    assert verificationPad(newName)
    assert not verificationPad(name)

    #suppression
    response = app.test_client().post("/api/remove/pad", json={'name': newName, 'parent': parent, 'idCo': idCo})
    assert response.status_code == 204
    assert not verificationPad(newName)



##
# Ajout et suppression d'un pad en étant connecté
##
def test_ajout_suppression_connecte():
    response = app.test_client().post("/api/login", json={'pseudo': 'Erolf', 'password': 'erolf'})
    name = "Coucou je suis un pad"
    parent = "Documentation"
    idCo = response.json["data"]
    response = app.test_client().post("/api/add/pad",json={'name': name, 'parent': parent, 'idCo':idCo})
    assert response.status_code == 204
    assert verificationPad(name)
    response = app.test_client().post("/api/remove/pad", json={'name' : name, 'parent': parent, 'idCo': idCo})
    assert response.status_code == 204
    assert not verificationPad(name)

##
#  Ajout d'un pad en étant connecté et suppression avec une déconnexion entre temps
##
def test_ajout_connecte_suppression_non_connecte():
    # Ajout du pad en étant connecté
    response = app.test_client().post("/api/login", json={'pseudo': 'Erolf', 'password': 'erolf'})
    name = "Coucou je suis un pad"
    parent = "Documentation"
    idCo = response.json["data"]
    response = app.test_client().post("/api/add/pad",json={'name': name, 'parent': parent, 'idCo':idCo})
    assert response.status_code == 204
    assert verificationPad(name)

    # Suppression du pad en étant pas connecté
    response = app.test_client().post("/api/remove/pad", json={'name' : name, 'parent': parent, 'idCo': -1})
    assert response.status_code == 204
    assert verificationPad(name)

    # Vraie Suppression
    response = app.test_client().post("/api/remove/pad", json={'name' : name, 'parent': parent, 'idCo': idCo})
    assert response.status_code == 204
    assert not verificationPad(name)

##
# Ajouter un pad avec un compte puis essayer de le supprimer avec un compte différent
##
def test_ajout_suppression_comptes_differents():
    # Ajout du pad en étant connecté
    response = app.test_client().post("/api/login", json={'pseudo': 'Erolf', 'password': 'erolf'})
    name = "Pad_test4"
    parent = "Documentation"
    idCo1 = response.json["data"]
    response = app.test_client().post("/api/add/pad",json={'name': name, 'parent': parent, 'idCo':idCo1})
    assert response.status_code == 204
    assert verificationPad(name)

    #Suppresion du pad en étant connecté avec un compte différent
    response = app.test_client().post("/api/login", json={'pseudo': 'Santa Klaus', 'password': 'hohoho'})
    idCo2 = response.json["data"]
    response = app.test_client().post("/api/remove/pad", json={'name' : name, 'parent': parent, 'idCo': idCo2})
    assert response.status_code == 204
    assert verificationPad(name)

    #Vraie Suppression
    response = app.test_client().post("/api/remove/pad", json={'name': name, 'parent': parent, 'idCo': idCo1})
    assert response.status_code == 204
    assert not verificationPad(name)


def verificationPad(name):
    response = app.test_client().post("api/init/menu")
    menu = response.data.decode()
    menu = json.loads(menu)
    for i in menu:
        if(i['name'] == name):
            return True
    return False
