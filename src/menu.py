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
        try:
            file = open(self.path,"r")
            menu = json.loads(file.read())
            file.close()
        except IOError as err:
            print("Erreur fichier : {0}" .format(err))
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
        try:
            fileRead = open(self.path,"r")
            menu = json.loads(fileRead.read())
            fileRead.close()
        except IOError as err:
            print("Erreur fichier : {0}"  .format(err))
            return -1

        for i in range (0, len(menu)):
            if(pad.getParent() == menu[i]['parent']):
                #Modifier la variable menu
                data = {'Nom' : pad.getName(), 'Adresse' : pad.getAdress()}
                menu[i]["pads"].append(data)
                #print(menu);
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
        try:
            fileMenu = open(self.path,"r")
            menu = json.loads(fileMenu.read())
            fileMenu.close()
            for i in range(0, len(menu)):
                if(oldName == menu[i]['parent']):
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
        try:
            fileMenu = open(self.path,"r")
            menu = json.loads(fileMenu.read())
            fileMenu.close()
            for i in range(0, len(menu)):
                for j in range(0,len(menu[i]["pads"])):
                    if(menu[i]["pads"][j]["Nom"] == name):
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
        try:
            fileMenu = open(self.path, "r")
            menu = json.loads(fileMenu.read())
            fileMenu.close()
            for i in range(0, len(menu)):
                for j in range (0, len(menu[i]["pads"])):
                    if(menu[i]["pads"][j]["Nom"] == oldName):
                        fileMenu = open(self.path,"w")
                        menu[i]["pads"][j]["Nom"] = newName
                        json.dump(menu, fileMenu)
                        fileMenu.close()
                        return 0
        except IOError as err:
            print("Erreur fichier : {0}" .format(err))
            return -1
