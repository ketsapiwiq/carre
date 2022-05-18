import json, configparser
from src import functionalities, pad, directory
from treelib import Node, Tree
import json

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
        tempTree.create_node("Root", "Root", data= directory.Directory("Root", "Root"))
        tempTree = createTree(menu["Root"]["children"], tempTree, "Root")

        self.ficTree = tempTree

        self.tree = self.ficTree
        nodes = self.tree.all_nodes()
        for i in range(0, len(nodes)):
            data = []
            data.append(nodes[i].data.getParent())
            # Si le noeud est un pad, on rajoute l'adresse et le contenu
            if isinstance(nodes[i].data, pad.Pad):
                data.append(nodes[i].data.getAdress())
                data.append(nodes[i].data.getContenu())
            nodes[i].data = data
        return nodes

    def writeData(self):
        # A FAIRE
        ## Faire les vérifs entre les 2 arbres et gérer les conflits
        try :
            fileMenu = open(self.path, "w")
            json.dump(self.tree.to_dict(with_data=True), fileMenu)
            self.ficTree = self.tree
            return 0
        except IOError as err:
            print("Erreur fichier : {0}" .format(err))
            return -1

    def delete(self, name):
        # A tester avec un nom qui n'existe pas, le nom d'un pad qui existe et le nom d'un dossier
        self.tree.remove_node(name)


    def move(self, name, movePoint):
        self.tree.move_node(name,movePoint)

    def add(self, pad):
        data = []
        #data.append(pad.getParent())
        #data.append(pad.getAdress())
        #data.append(pad.getContenu())
        data.append(pad[0])
        data.append(pad[1])
        data.append(pad[2])
        self.tree.create_node(pad[0], pad[0], parent=pad[1], data=data)
        print("Ajout d'un bidule")


    def addDirectory(self, directory):
        data = []
        data.append(directory.getParent())
        self.tree.create_node(directory.getName(), directory.getName(), parent=directory.getParent(), data=data)

    def rename(self, oldName, newName):
        self.tree.update_node(oldName, tag=newName, identifier=newName)


def loadJSON(self):
    try:
        file = open(self.path,"r")
        menu = json.load(file)
        file.close()
        return menu
    except IOError as err:
        print("Erreur fichier : {0}" .format(err))
        return -1


def createTree(menu, tempTree, parent):
    if isinstance(menu,list):
        for i in range(0, len(menu)):
            cles = list(menu[i].keys())[0]
            # Répertoire  avec enfants
            if list(menu[i][cles].keys())[0] == "children":
                dir = directory.Directory(cles, parent)
                tempTree.create_node(cles, cles, parent=parent, data = dir)
                # On ré-itère sur les enfants du répertoire
                createTree(menu[i][cles]["children"], tempTree, cles)
            # Pad
            elif len(menu[i][cles]['data']) > 1 :
                padNode = pad.Pad(cles, parent, menu[i][cles]['data'][1], menu[i][cles]['data'][2])
                tempTree.create_node(cles, cles, parent=parent, data=padNode)
            # Répertoire sans enfants
            else:
                dir = directory.Directory(cles, parent)
                tempTree.create_node(cles, cles, parent=parent, data=dir)
    return tempTree
