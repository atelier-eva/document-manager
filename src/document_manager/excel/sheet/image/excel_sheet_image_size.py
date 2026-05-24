class ExcelSheetImageSize():
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width
    
    def getResize(self, w):
        rate = w / self.width
        return ExcelSheetImageSize(self.width * rate, self.height * rate)
