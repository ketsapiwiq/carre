from src import menu 

newMenu = menu.Menu()


def ajoutPadFunc():
    print("Coucou ! ajout d'un pad")
    #newPad = Pad()
    #return render_template('index.html')


def testMenu(pad):
    newMenu = menu.Menu()
    newMenu.addPadToMenu(pad)

def recupMenu():
    return newMenu.recuperationMenu()