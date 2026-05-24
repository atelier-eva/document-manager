class ExcelSheet():
    def __init__(self, name, rows = [], widths = [], autoFilter = None, images = []) -> None:
        self.name = name
        self.rows = rows
        self.widths = widths
        self.autoFilter = autoFilter
        self.images = images

    def getAutoFilter(self):
        return self.autoFilter

    def getImages(self):
        return self.images

    def getName(self):
        return self.name

    def getRows(self):
        return self.rows

    def getWidths(self):
        return self.widths

    def hasAutoFilter(self):
        return self.autoFilter != None
