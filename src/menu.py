import json, configparser
from src import functionalities, pad

objMenu = []


class Menu:

    path = None
    # @nono : Attention aux chemins relatifs codé en dur dans le code,
    # voir les variables globales et les fichiers de configurations
    # voir le TOML comme format de configuration

    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read('config.ini')
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
                objMenu.append(pad)

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
                except IOError as err:
                    print("Erreur fichier : {0}"  .format(err))
                    return -1
        raise Exception("Pad invalide, nom du dossier parent inexistant")
