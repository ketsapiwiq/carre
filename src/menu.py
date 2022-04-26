import json
from src import functionalities, pad

objMenu = []


class Menu:

    path = "../static/Modele/menu.json"
    # @nono : Attention aux chemins relatifs codé en dur dans le code,
    # voir les variables globales et les fichiers de configurations
    # voir le TOML comme format de configuration

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

        #print(objMenu)
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
            # @nono: ça serait bien d'afficher l'erreur au client et de
            # ne pas continuer l'éxécution de la fonction, ici on va itéré sur un
            # menu de taille 0 ou NULL, c'est dommage.
        fileRead = open(self.path,"r")
        menu = json.loads(fileRead.read())
        # @nono : la gestion d'exception ici ne sert pas ?
        fileRead.close()

        for i in range (0, len(menu)):
            if(pad.getParent() == menu[i]['parent']):
                #Modifier la variable menu
                data = {'Nom' : pad.getName(), 'Adresse' : pad.getAdress()}
                menu[i]["pads"].append(data)
                #print(menu);
                # Tout renvoyer dans le fichier Json
                try:
                    fileWrite = open(self.path, "w")
                except IOError :
                    print("Il y a un problème avec l'ouverture du fichier")
                json.dump(menu, fileWrite)
                fileWrite.close()
                # @nono : pareil, ici on va dump dans un fichier qui est possiblement
                # pas ouvert, et si on dump dedans on perds toutes nos données, c'est
                # dangereux comme comportement :/
                return 0
        raise Exception("Pad invalide, nom du dossier parent inexistant")
