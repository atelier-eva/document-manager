class IntegratedTestCase():
    def __init__(self, pattern, procedures, forecast, needsEvidence=True) -> None:
        self.forecast = forecast
        self.pattern = pattern
        self.procedures = procedures
        self.needsEvidence = needsEvidence

    def getForecasts(self) -> str:
        return self.forecast

    def getPattern(self) -> str:
        return self.pattern

    def getProcedures(self) -> list:
        return self.procedures
