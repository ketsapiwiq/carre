class InvalidNameError(Exception):

    def __init__(self):
        self.info = "InvalidNameError : Le nom du pad ou du répertoire n'a pas été trouvé, il a peut être été déplacé ou supprimé."

    # __str__ is to print() the value
    def __str__(self):
        return(repr(self.info))

class DuplicateError(Exception):

    def __init__(self):
        self.info = "DuplicateError : Un pad ou un dossier portant le même nom est déjà présent dans le menu"

    # __str__ is to print() the value
    def __str__(self):
        return(repr(self.info))


class InvalidActionError(Exception):

    def __init__(self):
        self.info = "InvalidActionError (INTERNAL ERROR): L'action n'a pas été reconnue, ré-essayez ou faîtes remonter le bug"

    # __str__ is to print() the value
    def __str__(self):
        return(repr(self.info))
