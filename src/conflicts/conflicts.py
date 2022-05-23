#import conflicts import DuplicateError, InvalidNameError, InvalidActionError
from src.conflicts import *
def errorManager(action, param, menu):
    # Doit vérifier que l'action est réalisable
    # A appeler dès qu'on fait une action
    # On vérifie si c'est possible
    # On lock le thread de l'action réalisant l'action


    # Faire des switch case selon les actions
    #Vérifier s'il n'y a pas de doublons de pads
    # Vérifier que le pad en question existe bien
    #....



    match action:
        case "ajoutPadFunc" | "addDirectory":
            # Vérifier les doublons : le nom du pad NE DOIT PAS déjà être présent dans le menu
            if isExist(param[0], menu):
                raise DuplicatePadError
            #Vérifier si le parent existe : le nom du répertoire DOIT être présent dans le menu
            if not isExist(param[1], menu):
                raise InvalidDirectoryError
            return True
        case "rename" | "remove":
            #Vérifier que le pad existe
            if not isExist(param[0], menu):
                raise InvalidNameError
            return True

    raise InvalidActionError


# Un pad et un répertoire ne peuvent pas avoir le même nom (contrainte liées à l'arbre)

# Postulat de départ : Il ne peut pas y avoir 2 pads ayant le même nom dans le carré même s'ils sont dans des répertoires différents
def isExist(name, menu):
    for i in range(0, len(menu)):
        if menu[i]['name'] == name:
            return True
    return False
