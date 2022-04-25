import json
from src import fonctionnalities, pad

objMenu = []


class Menu:

    path = "../static/Modele/menu.json"

    ##
    # Récupère le menu dans un tableau
    ##
    def recuperationMenu(self):
        file = open(self.path,"r")
        menu = json.loads(file.read())
        file.close()
        for i in range(0, len(menu)):
            parent = menu[i]["parent"]
            for j in range(0, len(menu[i]["pads"])):
                newPad = pad.Pad(menu[i]["pads"][j]["Nom"], parent, menu[i]["pads"][j]["Adresse"])
                objMenu.append(pad)

        print(objMenu)
        return menu

    ##
    #   Met à jour le menu
    #   @param pad : Le pad à ajouter dans le menu
    ##
    def addPadToMenu(self, pad):
        try:
            fileRead = open(self.path,"r")
            menu = json.loads(fileRead.read())
        except IOError:
            print("Il y a un problème avec le fichier")
        fileRead = open(self.path,"r")
        menu = json.loads(fileRead.read())
        fileRead.close()

        for i in range (0, len(menu)):
            if(pad.getParent() == menu[i]['parent']):
                #Modifier la variable menu
                data = {'Nom' : pad.getName(), 'Adresse' : pad.getAdress()}
                menu[i]["pads"].append(data)
                print(menu);
                # Tout renvoyer dans le fichier Json
                try:
                    fileWrite = open(self.path, "w")
                except IOError :
                    print("Il y a un problème avec l'ouverture du fichier")
                json.dump(menu, fileWrite)
                fileWrite.close()
                return 0
        raise Exception("Pad invalide, nom du dossier parent inexistant")
