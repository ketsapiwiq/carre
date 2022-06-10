#import conflicts import DuplicateError, InvalidNameError, InvalidActionError
from src.conflicts import Errors
def errorManager(action, param, menu):

    match action:
        case "ajoutPadFunc":
            # Vérifier les doublons : le nom du pad NE DOIT PAS déjà être présent dans le menu
            if isPadExist(param[0], menu, param[1]):
                raise Errors.DuplicateError()
            #Vérifier si le parent existe : le nom du répertoire DOIT être présent dans le menu
            return True
        case "addDirectory":
            if isExist(param[0], menu):
                raise Errors.DuplicateError()
            return True
        case "removeDir":
            #Vérifier que le pad et le répertoire existent
            if not isExist(param[0], menu):
                raise Errors.InvalidNameError()
            return True
        case "removePad":
            #Vérifier que le pad et le répertoire existent
            if not (isExist(param[0], menu) & isExist(param[1], menu)):
                raise Errors.InvalidNameError()
            return True

        case "renameDir":
            #Le nouveau nom ne doit pas correspondre à un élement du menu
            print("oldName : " + param[0] + " newName : " + param[1])
            if isExist(param[1], menu):
                raise Errors.DuplicateError()

            # L'ancien nom doit corresondre à un élement du menu
            if not isExist(param[0], menu):
                raise Errors.InvalidNameError()

            return True

        case "renamePad":
            #Le nouveau nom ne doit pas correspondre à un élement du menu
            print("oldName : " + param[0] + " newName : " + param[1])
            if isExist(param[1], menu):
                raise Errors.DuplicateError()

            # L'ancien nom doit corresondre à un élement du menu
            if not (isExist(param[0], menu) & isExist(param[2], menu)):
                raise Errors.InvalidNameError()

            return True
        case "deleteAccount":
            return True

    print("Action non valide : " + action)
    raise Errors.InvalidActionError()


# Un pad et un répertoire ne peuvent pas avoir le même nom (contrainte liées à l'arbre)

# Postulat de départ : Il ne peut pas y avoir 2 pads ayant le même nom dans le carré même s'ils sont dans des répertoires différents
#Postulat v.2 : 2 pads peuvent avoir le même nom tant qu'il ne sont pas dans le même dossier

##
# @param name : nom du pad à chercher
# @return True si on trouve le nom dans la liste du menu
##
def isPadExist(name, menu, parent):
    for i in range(0, len(menu)):
        if menu[i]['name'] == name:
            #Si le parent n'est pas le même --> OK
            if(menu[i]['parent'] == parent):
                return True
            else:
                return False
    return False


##
# Return True si le répertoire existe déjà
##
def isExist(name, menu):
    for i in range(0, len(menu)):
        if menu[i]['name'] == name:
            print(menu[i]['name'] + " a été trouvé, le nom de base était : " + name)
            return True
    return False
