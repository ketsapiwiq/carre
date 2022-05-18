from src import menu, pad
import time

menuPads = menu.Menu()

def ajoutPadFunc(pad):
    menuPads.add(pad)
    menuPads.writeData()

def recupMenu():
    return menuPads.loadData()


def creaNbPad(nb):
    start = time.time()
    for i in range (0,nb):
        newPad = pad.Pad("Pad"+str(i), "Accueil", "p/9tm8"+str(i))
        ajoutPadFunc(newPad)
    print(str(time.time() - start) + " seconds to create" + nb + "pads")

def rename(names):
    oldName = names[0]
    newName = names[1]
    menuPads.rename(oldName, newName)
    menuPads.writeData()

def remove(name):
    menuPads.delete(name[0])
    menuPads.writeData()


def addDirectory(dir):
    menuPads.addDirectory(dir[0])
    menuPads.writeData()
