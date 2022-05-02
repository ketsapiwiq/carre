from src import menu, pad
import time

def ajoutPadFunc(pad):
    newMenu = menu.Menu()
    newMenu.addPadToMenu(pad)


def recupMenu():
    newMenu = menu.Menu()
    return newMenu.recuperationMenu()

def creaNbPad(nb):
    start = time.time()
    for i in range (0,nb):
        newPad = pad.Pad("Pad"+str(i), "Accueil", "p/9tm8"+str(i))
        ajoutPadFunc(newPad)
    print(str(time.time() - start) + " seconds to create" + nb + "pads")

def renameDir(names):
    oldName = names[0]
    newName = names[1]
    newMenu = menu.Menu()
    newMenu.renameDirectory(oldName, newName)

def removePad(name):
    newMenu = menu.Menu()
    newMenu.removePad(name)

def renamePad(names):
    oldName = names[0]
    newName = names[1]
    newMenu = menu.Menu()
    newMenu.renamePad(oldName, newName)
