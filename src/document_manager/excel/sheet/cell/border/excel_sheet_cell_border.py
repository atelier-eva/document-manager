class ExcelSheetCellBorder():
    def __init__(self, top, bottom, right, left) -> None:
        self.top = top
        self.bottom = bottom
        self.right = right
        self.left = left

    def getTop(self):
        return self.top

    def getBottom(self):
        return self.bottom

    def getRight(self):
        return self.right

    def getLeft(self):
        return self.left

    def hasTop(self):
        return self.top != None

    def hasBottom(self):
        return self.bottom != None

    def hasRight(self):
        return self.right != None

    def hasLeft(self):
        return self.left != None
