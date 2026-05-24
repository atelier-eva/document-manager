class IntegratedTestBlock():
    def __init__(self, name, perspectives) -> None:
        self.name = name
        self.perspectives = perspectives

    def getName(self) -> str:
        return self.name

    def getPerspectives(self) -> list:
        return self.perspectives
