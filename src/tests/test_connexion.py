from src.app import app

def test_connexion_inscrit():
    pseudo = 'Erolf'
    password = 'erolf'
    response = app.test_client().post("/api/login", json={'pseudo': pseudo, 'password': password})
    idErolf = response.json["data"]
    assert idErolf != -1
    assert response.status_code == 200

    pseudo = 'Santa Klaus'
    password = 'hohoho'
    response = app.test_client().post("/api/login", json={'pseudo': pseudo, 'password': password})
    idSanta = response.json["data"]
    assert idSanta != -1
    assert response.status_code == 200

    assert idErolf != idSanta


def test_connexion_non_inscrit():
    pseudo = 'untrucaupif'
    password = 'unautretrucaupif'
    response = app.test_client().post("/api/login", json={'pseudo': pseudo, 'password': password})
    assert response.json["data"] == -1
    assert response.status_code == 200


def test_connexion_blank():
    pseudo=''
    password=''
    response = app.test_client().post("/api/login", json={'pseudo': pseudo, 'password': password})
    assert response.json["data"] == -1
    assert response.status_code == 200
