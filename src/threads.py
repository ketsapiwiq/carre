
import threading,time
from src import functionalities

class ThreadFunctionalities(threading.Thread):

    ##
    # @param fonction : Nom de la fonction à exécuter
    # @param stock : variable permettant le retour de valeur ou le passage d'un paramètre
    ##
    def __init__(self, fonction, stock):
        threading.Thread.__init__(self)
        self.fonction = fonction
        self.stock = stock

    def getStock(self):
        return self.stock

    def run(self):
        lock = threading.Lock()
        match self.fonction :
            case "recupMenu" :
                with lock :
                    self.stock = functionalities.recupMenu()
                    return self.stock
            case "ajoutPadFunc" :
                with lock :
                    functionalities.ajoutPadFunc(self.stock)
                    return 0
            case "testPerf" :
                with lock :
                    functionalities.creaPad(self.stock)
                    return 0
            case "rename":
                with lock :
                    functionalities.rename(self.stock)
                    return 0
            case "remove":
                with lock :
                    functionalities.remove(self.stock)
                    return 0
            case "addDirectory":
                with lock :
                    functionalities.addDirectory(self.stock)
                    return 0

        return -1
