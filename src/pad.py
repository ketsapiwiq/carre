class Pad:

    def __init__(self,name, parent, adress):
        self.name = name
        self.parent = parent
        self.adress = adress

##### GETTERS #####

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent

    def getAdress(self):
        return self.adress

##### SETTERS #####

    def setParent(self, newParent):
        self.parent = newParent

    def setName(self, newName):
        self.name = newName
