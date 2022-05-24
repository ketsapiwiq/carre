class InvalidNameError(Exception):

    def __init__(self):
        self.info = "InvalidNameError : Le nom du pad ou du répertoire n'a pas été trouvé, il a peut être été déplacé ou supprimé."

    # __str__ is to print() the value
    def __str__(self):
        return(repr(self.info))
