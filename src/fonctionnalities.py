from src import menu


def ajoutPadFunc(pad):
    newMenu = menu.Menu()
    newMenu.addPadToMenu(pad)


def recupMenu():
    newMenu = menu.Menu()
    return newMenu.recuperationMenu()
