class ExcelSheetCell():
    def __init__(self, value = "", style = None, validationData = None, hyperLink=None) -> None:
        self.value = value
        self.style = style
        self.validationData = validationData
        self.hyperLink = hyperLink

    def getValidationData(self) -> list:
        return self.validationData

    def getHyperLink(self) -> str:
        return self.hyperLink

    def getStyle(self):
        return self.style

    def getValue(self) -> str:
        return str(self.value)
    
    def hasHyperLink(self) -> bool:
        return self.hyperLink != None

    def hasStyle(self) -> bool:
        return self.style != None

    def hasValidationList(self):
        return self.validationData != None
