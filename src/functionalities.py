from src import menu, pad
import time

menuPads = menu.Menu()

def ajoutPadFunc(pad):
    menuPads.addPadToMenu(pad)

def recupMenu():
    return menuPads.recuperationMenu()

def creaNbPad(nb):
    start = time.time()
    for i in range (0,nb):
        newPad = pad.Pad("Pad"+str(i), "Accueil", "p/9tm8"+str(i))
        ajoutPadFunc(newPad)
    print(str(time.time() - start) + " seconds to create" + nb + "pads")

def renameDir(names):
    oldName = names[0]
    newName = names[1]
    menuPads.renameDirectory(oldName, newName)


def removePad(name):
    menuPads.removePad(name)

def renamePad(names):
    oldName = names[0]
    newName = names[1]
    menuPads.renamePad(oldName, newName)

def addDirectory(name):
    menuPads.addDirectory(name)
