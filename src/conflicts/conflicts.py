from conflicts import DuplicateDirectoryError, DuplicatePadError, InvalidDirectoryError.py, InvalidPadError.py

def errorManager(action, param):
    # Doit vérifier que l'action est réalisable
    # A appeler dès qu'on fait une action
    # On vérifie si c'est possible
    # On lock le thread de l'action réalisant l'action


    # Faire des switch case selon les actions
    #Vérifier s'il n'y a pas de doublons de pads
    # Vérifier que le pad en question existe bien
    #....

    match action:
        case "add":
            return True
        case "remove":
            return True
        case "rename":
            return True

    raise InvalidActionError
