class ExcelSheetImage():
    def __init__(self, path, size, rowIndex=0, columnIndex=0) -> None:
        self.path = path
        self.size = size
        self.rowIndex = rowIndex
        self.columnIndex = columnIndex

    def getColumnIndex(self):
        return self.columnIndex

    def getSize(self):
        return self.size

    def getPath(self):
        return self.path

    def getRowIndex(self):
        return self.rowIndex
