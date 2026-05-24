class ExcelSheetCellFill():
    def __init__(self, type, color) -> None:
        self.type = type
        self.color = color

    def getColor(self):
        return self.color

    def getType(self):
        return self.type
