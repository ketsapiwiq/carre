from src.app import app
import json

def test_ajout_renommer_suppression():
    app.test_client().post("/")
    #Ajout
    name = 'Dir1'
    response = app.test_client().post("/api/add/dir", json={'name': name, 'parent': 'Root'})
    assert response.status_code == 204
    assert verificationDir(name)
    #Renommage
    newName = 'Test_RenameDir1'
    response = app.test_client().post("/api/rename/dir", json={'oldName': name, 'newName': newName})
    assert response.status_code == 204
    assert verificationDir(newName)
    assert not verificationDir(name)
    #Suppression
    response = app.test_client().post("/api/remove/dir", json={'nameDir': newName, 'idCo': -1})
    assert response.status_code == 204
    assert not verificationDir(newName)


def test_ajout_suppression_avec_pads():
    assert True

def test_ajout_suppression_connecte():
    assert True

def test_ajout_suppression_avec_pads_pas_a_soit():
    assert True


def verificationDir(name):
    response = app.test_client().post("api/init/menu")
    menu = response.data.decode()
    menu = json.loads(menu)
    for i in menu:
        if(i['name'] == name):
            return True
    return False
