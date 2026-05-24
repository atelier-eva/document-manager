class ExcelSheetCellStyle():
    def __init__(
        self,
        border = None,
        fill = None,
        alignment = None,
        font = None
    ) -> None:
        self.border = border
        self.fill = fill
        self.alignment = alignment
        self.font = font

    def getAlignment(self):
        return self.alignment

    def getBorder(self):
        return self.border

    def getFill(self):
        return self.fill

    def getFont(self):
        return self.font

    def hasFill(self):
        return self.fill != None

    def hasFont(self):
        return self.font != None
