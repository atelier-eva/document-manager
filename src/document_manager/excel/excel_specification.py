import string

class ExcelSpecification():
    @classmethod
    def getAlphabet(self, index):
        alphabet = string.ascii_uppercase
        return alphabet[index]
