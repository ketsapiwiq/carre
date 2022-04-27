from src import menu, pad
import time

def ajoutPadFunc(pad):
    newMenu = menu.Menu()
    newMenu.addPadToMenu(pad)


def recupMenu():
    newMenu = menu.Menu()
    return newMenu.recuperationMenu()

def creaPad(nb):
    start = time.time()
    for i in range (0,nb):
        newPad = pad.Pad("Pad"+str(i), "Accueil", "p/9tm8"+str(i))
        ajoutPadFunc(newPad)
    print(str(time.time() - start) + " seconds to create" + nb + "pads")
    # @nono: To create nb pads plutôt ?
