class Pad:

    def __init__(self, id, name, parent):
        self.id = id
        self.name = name
        self.parent = parent

    def getName(self):
        return self.name

    def getId(self):
        return self.id

    def getParent(self):
        return self.parent


