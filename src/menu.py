import json, configparser
from src import functionalities, pad

objMenu = []
ficIni = 'config.ini'

class Menu:

    path = None
    # @nono : Attention aux chemins relatifs codé en dur dans le code,
    # voir les variables globales et les fichiers de configurations
    # voir le TOML comme format de configuration

    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read(ficIni)
        self.path = conf['python']['pathMenu']

    ##
    # Récupère le menu dans un tableau
    ##
    def recuperationMenu(self):
        menu = loadJSON(self)
        if menu != -1 :
            for i in range(0, len(menu)):
                parent = menu[i]["parent"]
                for j in range(0, len(menu[i]["pads"])):
                    newPad = pad.Pad(menu[i]["pads"][j]["Nom"], parent, menu[i]["pads"][j]["Adresse"])
                    objMenu.append(newPad)

        return menu

    ##
    #   Met à jour le menu
    #   @param pad : Le pad à ajouter dans le menu
    ##
    def addPadToMenu(self, pad):
        menu = loadJSON(self)
        if menu != -1 :
            for i in range (0, len(menu)):
                if(pad.getParent() == menu[i]['parent']):
                    #Modifier la variable menu
                    data = {'Nom' : pad.getName(), 'Adresse' : pad.getAdress()}
                    menu[i]["pads"].append(data)
                    # Tout renvoyer dans le fichier Json
                    try:
                        fileWrite = open(self.path, "w")
                        json.dump(menu, fileWrite)
                        fileWrite.close()
                        return 0
                    except IOError as err:
                        print("Erreur fichier : {0}"  .format(err))
                        return -1
        raise Exception("Pad invalide, nom du dossier parent inexistant")

    def renameDirectory(self, oldName, newName):
        for pad in objMenu:
            if(pad.getParent() == oldName):
                pad.setParent(newName)

        menu = loadJSON(self)
        if menu != -1 :
            for i in range(0, len(menu)):
                if(oldName == menu[i]['parent']):
                    try :
                        fileMenu = open(self.path, "w")
                        menu[i]["parent"] = newName
                        json.dump(menu, fileMenu)
                        fileMenu.close()
                        return 0
                    except IOError as err:
                        print("Erreur fichier : {0}" .format(err))
                        return -1

    def removePad(self, name):
        for i in range(0, len(objMenu)):
            if(objMenu[i].getName() == name):
                del objMenu[i]
                break

        menu = loadJSON(self)
        for i in range(0, len(menu)):
            for j in range(0,len(menu[i]["pads"])):
                if(menu[i]["pads"][j]["Nom"] == name):
                    try:
                        fileMenu = open(self.path,"w")
                        del menu[i]["pads"][j]
                        json.dump(menu, fileMenu)
                        fileMenu.close()
                        return 0
                    except IOError as err:
                        print("Erreur fichier : {0}" .format(err))
                        return -1

    def renamePad(self, oldName, newName):
        for i in range(0, len(objMenu)):
            if(objMenu[i].getName() == oldName):
                objMenu[i].setName(newName)
                break

        menu = loadJSON(self)
        for i in range(0, len(menu)):
            for j in range (0, len(menu[i]["pads"])):
                if(menu[i]["pads"][j]["Nom"] == oldName):
                    try:
                        fileMenu = open(self.path,"w")
                        menu[i]["pads"][j]["Nom"] = newName
                        json.dump(menu, fileMenu)
                        fileMenu.close()
                        return 0
                    except IOError as err:
                        print("Erreur fichier : {0}" .format(err))
                        return -1

def loadJSON(self):
    try:
        file = open(self.path,"r")
        menu = json.loads(file.read())
        file.close()
        return menu
    except IOError as err:
        print("Erreur fichier : {0}" .format(err))
        return -1
