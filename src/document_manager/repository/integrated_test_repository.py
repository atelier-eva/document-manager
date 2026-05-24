import csv
import glob
import logging
import os
import re
import yaml
from jinja2 import Template
from PIL import Image
from src.integrated_test.data.integrated_test_data import IntegratedTestData
from src.integrated_test.case.integrated_test_case import IntegratedTestCase
from src.integrated_test.image.integrated_test_image import IntegratedTestImage
from src.integrated_test.matrix.integrated_test_matrix import IntegratedTestMatrix
from src.integrated_test.block.integrated_test_block import IntegratedTestBlock
from src.integrated_test.preparation.integrated_test_preparation import IntegratedTestPreparation
from src.integrated_test.perspective.integrated_test_perspective import IntegratedTestPerspective
from src.integrated_test.integrated_test import IntegratedTest

class IntegratedTestRepository():
    def find(self, typeName, name):
        # データセット読み込み
        dataSets = {}
        try:
            with open("./storage/integrated_test/global_config/データセット.yml", 'r') as file:
                dataSets = yaml.safe_load(file)
        except FileNotFoundError:
            pass

        blocks = self.getBlocks(f"./storage/integrated_test/{typeName}/{name}/テストケース.yml", dataSets)

        matrices = []
        matrixPaths = sorted(glob.glob(f"./storage/integrated_test/{typeName}/{name}/マトリクス/*"))
        for matrixPath in matrixPaths:
            with open(matrixPath, 'r') as file:
                reader = csv.reader(file)
                data = [row for row in reader]

                if ('エビデンス' in data[0]) and (data[0].index('エビデンス') != len(data[0]) - 1):
                    raise Exception(f"{matrixPath}のエビデンス列を最後列にしてください")

                matrices.append(IntegratedTestMatrix(os.path.splitext(os.path.basename(matrixPath))[0], data[0], data[1:]))

        images = []
        imagePaths = sorted(glob.glob(f"./storage/integrated_test/{typeName}/{name}/画面イメージ/*"))
        for imagePath in imagePaths:
            if os.path.isfile(imagePath):
                img = Image.open(imagePath)
                w, h = img.size
                images.append(IntegratedTestImage(imagePath, w, h))

        preparationPath = f"./storage/integrated_test/{typeName}/{name}/事前準備・注意点.yml"
        preparation = None
        if os.path.isfile(preparationPath):
            with open(preparationPath, 'r') as file:
                template = Template(file.read())
                output = template.render(dataSets)
                data = yaml.safe_load(output)
                preparation = IntegratedTestPreparation([] if data == None else data)

        testDataPath = f"./storage/integrated_test/{typeName}/{name}/テストデータ.yml"
        testData = None
        if os.path.isfile(testDataPath):
            with open(testDataPath, 'r') as file:
                template = Template(file.read())
                output = template.render(dataSets)
                data = yaml.safe_load(output)
                testData = IntegratedTestData(data)

        return IntegratedTest(typeName, name, blocks, matrices, images, preparation, testData)

    def get(self) -> list:
        integratedTests = []
        typeNames = ['batch', 'component', 'file', 'view']
        for typeName in typeNames:
            paths = glob.glob(fr"./storage/integrated_test/{typeName}/*/")
            for path in paths:
                result = re.match(fr"./storage/integrated_test/{typeName}/(.+)/", path)
                name = result.group(1)
                integratedTests.append(self.find(typeName, name))
        return integratedTests

    def getBlocks(self, path, dataSets) -> list:
        logging.info(f"{path}の読み込み開始")

        if not os.path.isfile(path):
            raise Exception(f"{path}が見つかりません")

        data = None
        with open(path, 'r') as file:
            template = Template(file.read())
            output = template.render(dataSets)
            data = yaml.safe_load(output)
        
        if data is None:
            raise Exception(f"{path}が空です")

        blocks = []
        for _, blockName in enumerate(data):
            if data[blockName] is None:
                raise Exception(f"{path}の{blockName}が空です")

            perspectives = []
            for _, perspectiveName in enumerate(data[blockName]):
                if data[blockName][perspectiveName] is None:
                    raise Exception(f"{path}の{blockName}の{perspectiveName}が空です")

                cases = []
                for _, case in enumerate(data[blockName][perspectiveName]):
                    if case is None:
                        raise Exception(f"{path}の{blockName}の{perspectiveName}のテストケースが空です")
                    elif (not '想定結果' in case) or (not isinstance(case['想定結果'], list)):
                        raise Exception(f"{path}の{blockName}の{perspectiveName}の想定結果が空です")

                    cases.append(IntegratedTestCase(
                        case['パターン'] if 'パターン' in case else '',
                        case['手順'] if '手順' in case else [],
                        case['想定結果'],
                        case['エビデンス'] if 'エビデンス' in case and case['エビデンス'] == '要' else False
                    ))
                perspectives.append(IntegratedTestPerspective(perspectiveName, cases))
            blocks.append(IntegratedTestBlock(blockName, perspectives))
        return blocks
