import logging
import os
import yaml
from jinja2 import Template
from src.integrated_test.case.integrated_test_case import IntegratedTestCase
from src.integrated_test.config.integrated_test_config import IntegratedTestConfig
from src.integrated_test.block.integrated_test_block import IntegratedTestBlock
from src.integrated_test.perspective.integrated_test_perspective import IntegratedTestPerspective

class IntegratedTestConfigRepository():
    def find(self) -> IntegratedTestConfig:
        # データセット読み込み
        dataSets = {}
        try:
            with open("./storage/integrated_test/global_config/データセット.yml", 'r') as file:
                dataSets = yaml.safe_load(file)
        except FileNotFoundError:
            pass

        configs = []
        typeNames = ['component', 'batch', 'file', 'view']
        for typeName in typeNames:
            path = f"./storage/integrated_test/{typeName}_config/共通.yml"

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

            blockPerspectives = []
            for perspectiveName in data:
                if data[perspectiveName] is None:
                    raise Exception(f"{path}の{perspectiveName}が空です")

                cases = []
                for case in data[perspectiveName]:
                    if case is None:
                        raise Exception(f"{path}の{perspectiveName}のテストケースが空です")
                    elif (not '想定結果' in case) or (not isinstance(case['想定結果'], list)):
                        raise Exception(f"{path}の{perspectiveName}の想定結果が空です")

                    cases.append(IntegratedTestCase(
                        case['パターン'],
                        case['手順'] if '手順' in case else [],
                        case['想定結果'],
                        case['エビデンス'] if 'エビデンス' in case and case['エビデンス'] == '要' else False
                    ))
                blockPerspectives.append(IntegratedTestPerspective(perspectiveName, cases))

            block = IntegratedTestBlock("共通", blockPerspectives)

            logging.info(f"./storage/integrated_test/{typeName}_config/テスト観点.ymlの読み込み開始")

            perspectives = None
            with open(f"./storage/integrated_test/{typeName}_config/テスト観点.yml", 'r') as file:
                template = Template(file.read())
                output = template.render(dataSets)
                perspectives = yaml.safe_load(output)

            configs.append(IntegratedTestConfig(typeName, block, perspectives))

        return configs
