class IntegratedTestConfig():
    def __init__(self, type, block, perspectives) -> None:
        self.type = type
        self.block = block
        self.perspectives = perspectives

    def getBlock(self):
        return self.block

    def getPerspectives(self) -> list:
        return self.perspectives

    def getType(self) -> str:
        return self.type
