import unittest

from document_manager.excel.excel_specification import ExcelSpecification

class TestExcelSpecification(unittest.IntegratedTestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName)

    def test_getAlphabet(self):
        self.assertEqual(ExcelSpecification.getAlphabet(0), "A")
        self.assertEqual(ExcelSpecification.getAlphabet(25), "Z")
