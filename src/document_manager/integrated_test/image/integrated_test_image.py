import os

class IntegratedTestImage():
    def __init__(self, path, width, height) -> None:
        self.path = path
        self.width = width
        self.height = height

    def getName(self):
        return os.path.basename(self.path)

    def getHeight(self):
        return self.height

    def getPath(self) -> str:
        return self.path

    def getWidth(self):
        return self.width
