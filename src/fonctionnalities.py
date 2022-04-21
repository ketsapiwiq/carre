from src import menu 


def ajoutPadFunc(pad):
    print("Coucou ! ajout d'un pad")
    newMenu = menu.Menu()
    newMenu.addPadToMenu(pad)
    

def recupMenu():
    newMenu = menu.Menu()
    return newMenu.recuperationMenu()