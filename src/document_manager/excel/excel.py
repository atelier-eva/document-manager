class Excel():
    def __init__(self, name, excelSheets) -> None:
        self.name = name
        self.excelSheets = excelSheets

    def getName(self):
        return self.name

    def getSheets(self):
        return self.excelSheets
