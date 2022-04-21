import json

class Menu:
    ##
    # Référence sur le fichier json
    # Si possible, faire une classe statique
    # Faire les méthodes pour récup les infos ou pour les ajouter

    ## path not defined
    path = "static/Modele/menu.json"

    #def __init__(self):
    #    self.path = "/Modele/menu.json"

    def recuperationMenu(self):
        file = open(self.path,"r")
        menu = json.loads(file.read())
        file.close()
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