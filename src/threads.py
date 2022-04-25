
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
        match self.fonction :
            case "recupMenu" :
                self.stock = functionalities.recupMenu()
                return self.stock
            case "ajoutPadFunc" :
                functionalities.ajoutPadFunc(self.stock)
                return 0;
            case " " :
                print("Pas de fonctions connues")
                return -1

        #try:
        #    self.stock = fonctionnalities.self.fonction()
        #    return self.stock
        #except NameError:
        #    print("La fonction n'existe pas")
