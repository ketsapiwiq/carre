#import conflicts import DuplicateError, InvalidNameError, InvalidActionError
from src.conflicts import Errors
def errorManager(action, param, menu):

    match action:
        case "ajoutPadFunc" | "addDirectory":
            # Vérifier les doublons : le nom du pad NE DOIT PAS déjà être présent dans le menu
            if isExist(param[0], menu):
                raise Errors.DuplicatePadError()
            #Vérifier si le parent existe : le nom du répertoire DOIT être présent dans le menu
            if not isExist(param[1], menu):
                raise Errors.InvalidDirectoryError()
            return True
        case "rename" | "remove":
            #Vérifier que le pad existe
            if not isExist(param[0], menu):
                raise Errors.InvalidNameError()
            return True

    raise Errors.InvalidActionError()


# Un pad et un répertoire ne peuvent pas avoir le même nom (contrainte liées à l'arbre)

# Postulat de départ : Il ne peut pas y avoir 2 pads ayant le même nom dans le carré même s'ils sont dans des répertoires différents
def isExist(name, menu):
    for i in range(0, len(menu)):
        if menu[i]['name'] == name:
            return True
    return False
