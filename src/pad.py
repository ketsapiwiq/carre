class Pad:

    def __init__(self,name, parent, adress, contenu):
        self.name = name
        self.parent = parent
        self.adress = adress
        self.contenu = contenu

##### GETTERS #####

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent

    def getAdress(self):
        return self.adress

    def getContenu(self):
        return self.contenu

##### SETTERS #####

    def setParent(self, newParent):
        self.parent = newParent

    def setName(self, newName):
        self.name = newName

    def toString(self):
        return "Ce pad s'appelle " + self.name + ", il a pour parent " + self.parent + " et vous pouvez le trouver à l'adresse suivante : " + self.adress
