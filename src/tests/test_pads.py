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
    #suppression name, parent, idCo
    response = app.test_client().post("/api/remove/pad", json={'name': name, 'parent': parent, 'idCo': idCo})
    assert response.status_code == 204
    assert not verificationPad(newName)


##
# Ajout et suppression d'un pad en étant connecté
##
def test_ajout_suppression_connecte():
    assert True

##
#  Ajout d'un pad en étant connecté et suppression avec une déconnexion entre temps
##
def test_ajout_connecte_suppression_non_connecte():
    assert True
##
# Ajouter un pad avec un compte puis essayer de le supprimer avec un compte différent
##
def test_ajout_suppression_comptes_differents():
    assert True


def verificationPad(name):
    response = app.test_client().post("api/init/menu")
    menu = response.data.decode()
    menu = json.loads(menu)
    print(type(menu[0]))
    for i in menu:
        if(i['name'] == name):
            return True
    return False
