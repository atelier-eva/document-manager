import csv
import glob
import io
import logging
import os
import re
import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from PIL import Image
from document_manager.integrated_test.data.integrated_test_data import IntegratedTestData
from document_manager.integrated_test.case.integrated_test_case import IntegratedTestCase
from document_manager.integrated_test.image.integrated_test_image import IntegratedTestImage
from document_manager.integrated_test.matrix.integrated_test_matrix import IntegratedTestMatrix
from document_manager.integrated_test.block.integrated_test_block import IntegratedTestBlock
from document_manager.integrated_test.preparation.integrated_test_preparation import IntegratedTestPreparation
from document_manager.integrated_test.perspective.integrated_test_perspective import IntegratedTestPerspective
from document_manager.integrated_test.integrated_test import IntegratedTest

class IntegratedTestRepository():
    storageRoot = "./storage/integrated_test"

    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(self.storageRoot))

    def find(self, typeName, name):
        # データセット読み込み
        dataSets = self._loadDataSets()

        blocks = self.getBlocks(f"{typeName}/{name}/テストケース.yml.j2", dataSets)

        matrices = []
        matrixDir = f"{self.storageRoot}/{typeName}/{name}/マトリクス"
        matrixPaths = sorted(glob.glob(f"{matrixDir}/*.csv.j2"))
        for matrixPath in matrixPaths:
            relPath = os.path.relpath(matrixPath, self.storageRoot)
            template = self.env.get_template(relPath)
            rendered = template.render(dataSets)
            reader = csv.reader(io.StringIO(rendered))
            data = [row for row in reader]

            if ('エビデンス' in data[0]) and (data[0].index('エビデンス') != len(data[0]) - 1):
                raise Exception(f"{matrixPath}のエビデンス列を最後列にしてください")

            matrices.append(IntegratedTestMatrix(self._stripExtension(matrixPath, ".csv.j2"), data[0], data[1:]))

        images = []
        imagePaths = sorted(glob.glob(f"{self.storageRoot}/{typeName}/{name}/画面イメージ/*"))
        for imagePath in imagePaths:
            if os.path.isfile(imagePath):
                img = Image.open(imagePath)
                w, h = img.size
                images.append(IntegratedTestImage(imagePath, w, h))

        preparation = None
        preparationRel = f"{typeName}/{name}/事前準備・注意点.yml.j2"
        try:
            template = self.env.get_template(preparationRel)
        except TemplateNotFound:
            template = None
        if template is not None:
            data = yaml.safe_load(template.render(dataSets))
            preparation = IntegratedTestPreparation([] if data is None else data)

        testData = None
        testDataRel = f"{typeName}/{name}/テストデータ.yml.j2"
        try:
            template = self.env.get_template(testDataRel)
        except TemplateNotFound:
            template = None
        if template is not None:
            data = yaml.safe_load(template.render(dataSets))
            testData = IntegratedTestData(data)

        return IntegratedTest(typeName, name, blocks, matrices, images, preparation, testData)

    def get(self) -> list:
        integratedTests = []
        typeNames = ['batch', 'component', 'file', 'view']
        for typeName in typeNames:
            paths = glob.glob(fr"{self.storageRoot}/{typeName}/*/")
            for path in paths:
                result = re.match(fr"{re.escape(self.storageRoot)}/{typeName}/(.+)/", path)
                name = result.group(1)
                integratedTests.append(self.find(typeName, name))
        return integratedTests

    def getBlocks(self, relPath, dataSets) -> list:
        absPath = f"{self.storageRoot}/{relPath}"
        logging.info(f"{absPath}の読み込み開始")

        try:
            template = self.env.get_template(relPath)
        except TemplateNotFound:
            raise Exception(f"{absPath}が見つかりません")

        data = yaml.safe_load(template.render(dataSets))

        if data is None:
            raise Exception(f"{absPath}が空です")

        blocks = []
        for _, blockName in enumerate(data):
            if data[blockName] is None:
                raise Exception(f"{absPath}の{blockName}が空です")

            perspectives = []
            for _, perspectiveName in enumerate(data[blockName]):
                if data[blockName][perspectiveName] is None:
                    raise Exception(f"{absPath}の{blockName}の{perspectiveName}が空です")

                cases = []
                for _, case in enumerate(data[blockName][perspectiveName]):
                    if case is None:
                        raise Exception(f"{absPath}の{blockName}の{perspectiveName}のテストケースが空です")
                    elif (not '想定結果' in case) or (not isinstance(case['想定結果'], list)):
                        raise Exception(f"{absPath}の{blockName}の{perspectiveName}の想定結果が空です")

                    cases.append(IntegratedTestCase(
                        case['パターン'] if 'パターン' in case else '',
                        case['手順'] if '手順' in case else [],
                        case['想定結果'],
                        case['エビデンス'] if 'エビデンス' in case and case['エビデンス'] == '要' else False
                    ))
                perspectives.append(IntegratedTestPerspective(perspectiveName, cases))
            blocks.append(IntegratedTestBlock(blockName, perspectives))
        return blocks

    def _loadDataSets(self) -> dict:
        try:
            template = self.env.get_template("global_config/データセット.yml.j2")
        except TemplateNotFound:
            return {}
        data = yaml.safe_load(template.render())
        return data if data is not None else {}

    @staticmethod
    def _stripExtension(path: str, extension: str) -> str:
        base = os.path.basename(path)
        if base.endswith(extension):
            return base[: -len(extension)]
        return os.path.splitext(base)[0]
