class IntegratedTest():
    def __init__(self, type, name, blocks, matrices=[], images=[], preparation=None, accounts=None) -> None:
        self.type = type
        self.name = name
        self.blocks = blocks
        self.matrices = matrices
        self.images = images
        self.preparation = preparation
        self.accounts = accounts

    def getAccounts(self):
        return self.accounts

    def getImages(self) -> list:
        return self.images

    def getMatrices(self) -> list:
        return self.matrices

    def getName(self) -> str:
        return self.name
    
    def getBlocks(self) -> list:
        return self.blocks

    def getPreparation(self):
        return self.preparation

    def getType(self) -> str:
        return self.type

    def hasImages(self) -> bool:
        return len(self.images) > 0

    def hasTestData(self) -> bool:
        return self.accounts != None
