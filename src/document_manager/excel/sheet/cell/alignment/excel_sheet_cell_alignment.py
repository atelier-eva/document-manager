class ExcelSheetCellAlignment():
    def __init__(self, vertical: str, wrapText: bool = False) -> None:
        self.vertical = vertical
        self.wrapText = wrapText

    def getVertical(self):
        return self.vertical

    def getWrapText(self):
        return self.wrapText
