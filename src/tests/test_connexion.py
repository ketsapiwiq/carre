import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir,"../"))

from src.app import app

def test_connexion_inscrit():
    app.test_client().post("/")

    pseudo = 'Erolf'
    password = 'erolf'
    response = app.test_client().post("/api/signup", json={'pseudo': pseudo, 'password': password})
    assert response.status_code == 200
    id = response.json["data"]
    assert id != -1
    response = app.test_client().post("/api/login", json={'pseudo': pseudo, 'password': password})
    idErolf = response.json["data"]
    assert idErolf != -1
    assert response.status_code == 200

    pseudo = 'Santa Klaus'
    password = 'hohoho'
    reponse = app.test_client().post("/api/signup", json={'pseudo': pseudo, 'password': password})
    assert response.status_code == 200
    id = response.json["data"]
    assert id != -1
    response = app.test_client().post("/api/login", json={'pseudo': pseudo, 'password': password})
    idSanta = response.json["data"]
    assert idSanta != -1
    assert response.status_code == 200

    assert idErolf != idSanta

    app.test_client().post("/api/deleteAccount", json={'idConnexion': idErolf})
    app.test_client().post("/api/deleteAccount", json={'idConnexion': idSanta})


def test_connexion_non_inscrit():
    app.test_client().post("/")
    pseudo = 'untrucaupif'
    password = 'unautretrucaupif'
    response = app.test_client().post("/api/login", json={'pseudo': pseudo, 'password': password})
    assert response.json["data"] == -1
    assert response.status_code == 200


def test_connexion_blank():
    app.test_client().post("/")
    pseudo=''
    password=''
    response = app.test_client().post("/api/login", json={'pseudo': pseudo, 'password': password})
    assert response.json["data"] == -1
    assert response.status_code == 200
