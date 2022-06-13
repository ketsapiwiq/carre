class Directory:

    ##
    # @param name :  le nom du dossier
    # @param parent : le père du dossier, par défaut : root
    # @param pads : la liste des fils (dossier et/ou pads) /!\ Redondance d'infos, on peut récupérer ça via le menu
    ##
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        #self.sons = sons

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent

    def toString(self):
        return "Ce dossier s'appelle " + self.name
