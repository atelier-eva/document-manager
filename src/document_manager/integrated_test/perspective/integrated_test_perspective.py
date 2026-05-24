class IntegratedTestPerspective():
    def __init__(self, name, cases) -> None:
        self.name = name
        self.cases = cases

    def getCases(self) -> list:
        return self.cases

    def getName(self) -> str:
        return self.name
