
import threading,time
from src import menu

class ThreadFunctionalities(threading.Thread):

    ##
    # @param fonction : Nom de la fonction à exécuter
    # @param stock : variable permettant le retour de valeur ou le passage d'un paramètre
    # @param menu : instance du menu pour affectuer les modifs
    ##

    def __init__(self, fonction, stock, menu):
        threading.Thread.__init__(self)
        self.fonction = fonction
        self.stock = stock
        self.menuCarre = menu

    def getStock(self):
        return self.stock

    def run(self):
        lock = threading.Lock()
        match self.fonction :
            case "recupMenu" :
                with lock :
                    self.stock = self.menuCarre.loadData()
                    return self.stock
            case "ajoutPadFunc" :
                with lock :
                    self.menuCarre.add(self.stock)
                    self.menuCarre.writeData()
                    return 0
            case "renamePad":
                with lock :
                    self.menuCarre.rename(self.stock[0], self.stock[1], self.stock[2])
                    self.menuCarre.writeData()
                    return 0
            case "renameDir":
                with lock:
                    self.menuCarre.rename(self.stock[0], self.stock[1], None)
                    self.menuCarre.writeData()
            case "removePad":
                with lock :
                    self.menuCarre.delete(self.stock[0], self.stock[1], self.stock[2])
                    self.menuCarre.writeData()
                    return 0
            case "removeDir":
                with lock:
                    self.menuCarre.delete(self.stock[0], None, None)
                    self.menuCarre.writeData()
                    return 0
            case "addDirectory":
                with lock :
                    self.menuCarre.addDirectory(self.stock[0])
                    self.menuCarre.writeData()
                    return 0

        return -1
