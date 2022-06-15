import json, configparser
from src import pad, directory

# import pad, directory
from treelib import Node, Tree
import json

ficIni = "../config.ini"


class Menu:

    path = None
    # @nono : Attention aux chemins relatifs codé en dur dans le code,
    # voir les variables globales et les fichiers de configurations
    # voir le TOML comme format de configuration

    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read(ficIni)
        self.path = conf["python"]["pathMenu"]
        # Arbre où les modifications sont faites
        self.tree = Tree()
        # Arbre correspondant au fichier
        self.ficTree = Tree()

    ##
    # Récupère le menu du fichier JSON dans un dictionnaire
    # A partir de celui-ci, un arbre représentant le menu est créé
    # @return nodes : liste des noeuds de l'arbre, contient le nom et le parent de chaque noeud
    ##
    def loadData(self):
        menu = loadJSON(self)

        tempTree = Tree()
        dataRoot = []
        dataRoot.append("Root")
        tempTree.create_node("Root", "Root", data=dataRoot)
        tempTree = createTree(menu["Root"]["children"], tempTree, "Root")

        self.ficTree = tempTree

        self.tree = self.ficTree
        nodes = self.tree.all_nodes()

        return nodes

    def writeData(self):
        try:
            fileMenu = open(self.path, "w")
            json.dump(self.tree.to_dict(with_data=True), fileMenu)
            self.ficTree = self.tree
            return 0
        except IOError as err:
            print("Erreur fichier : {0}".format(err))
            return -1

    def delete(self, name, parent, idConnexion):
        if parent == None:
            # Vérifier que tous les pads présents dans le dossier appartiennent à l'utilsateur ou à personne
            canDelete = True
            children = self.tree.children(name)
            for child in children:
                if len(child.data) > 2 and not (
                    child.data[3] == "-1" or child.data[3] == str(idConnexion)
                ):
                    canDelete = False
            if canDelete:
                self.tree.remove_node(name)
        else:
            # Trouver le bon pad et récupérer son id de connexion
            idCoPad = self.tree.get_node(name + parent).data[3]
            # Si l'id de connexion == à celui passé en param ou si celui est trouvé == -1 --> On peut supprimer
            if idCoPad == str(idConnexion) or str(idCoPad) == "-1":
                self.tree.remove_node(name + parent)

    ##
    # Lors de la suppression d'un utilisateur, tous les pads qu'il a deviennent sans proprietaire
    # param @idConnexion : L'Id de connexion de l'utilisateur à supprimer
    ##
    def updatePads(self, idConnexion):
        nodes = self.tree.all_nodes()
        print("id utilisateur : " + str(idConnexion))
        for node in nodes:
            if len(node.data) > 2:
                if node.data[3] == str(idConnexion):
                    node.data[3] = -1
                    print(node.data[3])

    def move(self, name, movePoint):
        self.tree.move_node(name, movePoint)

    def add(self, pad):
        data = []
        # Nom du parent
        data.append(pad[1])
        # Adresse du pad
        data.append(pad[2])
        # Contenu du pad
        data.append(pad[3])
        # Propriétaire du pad
        data.append(str(pad[4]))
        nodes = self.tree.all_nodes()
        self.tree.create_node(pad[0], pad[0] + pad[1], parent=pad[1], data=data)

    def addDirectory(self, directory):
        data = []
        data.append(directory.getParent())
        self.tree.create_node(
            directory.getName(),
            directory.getName(),
            parent=directory.getParent(),
            data=data,
        )

    def rename(self, oldName, newName, parent):
        if parent == None:
            parent = ""
        self.tree.update_node(
            oldName + parent, tag=newName, identifier=newName + parent
        )


def loadJSON(self):
    try:
        file = open(self.path, "r")
        menu = json.load(file)
        file.close()
        return menu
    except IOError as err:
        print("Erreur fichier : {0}".format(err))
        return -1


def createTree(menu, tempTree, parent):
    if isinstance(menu, list):
        for i in range(0, len(menu)):
            cles = list(menu[i].keys())[0]
            # Répertoire  avec enfants
            if list(menu[i][cles].keys())[0] == "children":
                dataDir = []
                dataDir.append(parent)
                tempTree.create_node(cles, cles, parent=parent, data=dataDir)
                # On ré-itère sur les enfants du répertoire
                createTree(menu[i][cles]["children"], tempTree, cles)
            # Pad
            elif len(menu[i][cles]["data"]) > 1:
                dataPad = []
                dataPad.append(parent)
                dataPad.append(menu[i][cles]["data"][1])
                dataPad.append(menu[i][cles]["data"][2])
                dataPad.append(str(menu[i][cles]["data"][3]))
                tempTree.create_node(cles, cles + parent, parent=parent, data=dataPad)

            # Répertoire sans enfants
            else:
                dataDir = []
                dataDir.append(parent)
                tempTree.create_node(cles, cles, parent=parent, data=dataDir)

    return tempTree
