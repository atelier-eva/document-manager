class IntegratedTestMatrix():
    def __init__(self, name, header, data) -> None:
        self.name = name
        self.header = header
        self.data = data

    def getEvidenceIndex(self):
        return self.header.index('エビデンス') if 'エビデンス' in self.header else None

    def getName(self):
        return self.name

    def getHeader(self):
        return self.header

    def getData(self):
        return self.data
