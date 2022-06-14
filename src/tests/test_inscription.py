import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir,"../"))

from src.app import app

def test_inscription_basic():
    pseudo = "UnPseudo"
    password = "UnMotDePasse"
    response = app.test_client().post("/api/signup", json={'pseudo': pseudo, 'password': password})
    idCo = response.json["data"]
    assert response.status_code == 200
    assert idCo != -1

    ## L'utilisateur est déjà enregistré
    response = app.test_client().post("/api/signup", json={'pseudo': pseudo, 'password': password})
    id = response.json["data"]
    assert response.status_code == 200
    assert id == -1

    deleteAccount(pseudo, password)


def test_inscription_blank():
    pseudo = "      "
    password = "        "
    response = app.test_client().post("/api/signup", json={'pseudo': pseudo, 'password': password})
    id = response.json["data"]
    assert response.status_code == 200
    assert id == -1

def test_inscription_none():
    pseudo = ""
    password = ""
    response = app.test_client().post("/api/signup", json={'pseudo': pseudo, 'password': password})
    id = response.json["data"]
    assert response.status_code == 200
    assert id == -1

def test_inscription_pseudo_emoji():
    pseudo = "👾👽​👻​"
    password = "boooooouh"
    response = app.test_client().post("/api/signup", json={'pseudo': pseudo, 'password': password})
    id = response.json["data"]
    assert response.status_code == 200
    deleteAccount(pseudo, password)
    assert id != -1

def test_inscription_password_emoji():
    pseudo = "bouh"
    password = "👾👽​👻"
    response = app.test_client().post("/api/signup", json={'pseudo': pseudo, 'password': password})
    id = response.json["data"]
    assert response.status_code == 200
    deleteAccount(pseudo, password)
    assert id != -1


def test_inscription_japonais():
    pseudo = "わる"
    password = "しょうなり"
    response = app.test_client().post("/api/signup", json={'pseudo': pseudo, 'password': password})
    id = response.json["data"]
    assert response.status_code == 200
    deleteAccount(pseudo, password)
    assert id != -1


def test_inscription_russe():
    pseudo = "Живая"
    password = "культура"
    response = app.test_client().post("/api/signup", json={'pseudo': pseudo, 'password': password})
    id = response.json["data"]
    assert response.status_code == 200
    deleteAccount(pseudo, password)
    assert id != -1


def deleteAccount(pseudo, password):
    response = app.test_client().post("/api/login", json={'pseudo': pseudo, 'password': password})
    idCo = response.json["data"]
    # Lancer index pour le lancement des threads
    app.test_client().post("/")
    response = app.test_client().post("/api/deleteAccount", json={'idConnexion': idCo})
