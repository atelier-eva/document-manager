import logging
import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from document_manager.integrated_test.case.integrated_test_case import IntegratedTestCase
from document_manager.integrated_test.config.integrated_test_config import IntegratedTestConfig
from document_manager.integrated_test.block.integrated_test_block import IntegratedTestBlock
from document_manager.integrated_test.perspective.integrated_test_perspective import IntegratedTestPerspective

class IntegratedTestConfigRepository():
    storageRoot = "./storage/integrated_test"

    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(self.storageRoot))

    def find(self) -> IntegratedTestConfig:
        # データセット読み込み
        dataSets = self._loadDataSets()

        configs = []
        typeNames = ['component', 'batch', 'file', 'view']
        for typeName in typeNames:
            commonRel = f"{typeName}_config/共通.yml.j2"
            commonAbs = f"{self.storageRoot}/{commonRel}"

            logging.info(f"{commonAbs}の読み込み開始")

            try:
                template = self.env.get_template(commonRel)
            except TemplateNotFound:
                raise Exception(f"{commonAbs}が見つかりません")

            data = yaml.safe_load(template.render(dataSets))

            if data is None:
                raise Exception(f"{commonAbs}が空です")

            blockPerspectives = []
            for perspectiveName in data:
                if data[perspectiveName] is None:
                    raise Exception(f"{commonAbs}の{perspectiveName}が空です")

                cases = []
                for case in data[perspectiveName]:
                    if case is None:
                        raise Exception(f"{commonAbs}の{perspectiveName}のテストケースが空です")
                    elif (not '想定結果' in case) or (not isinstance(case['想定結果'], list)):
                        raise Exception(f"{commonAbs}の{perspectiveName}の想定結果が空です")

                    cases.append(IntegratedTestCase(
                        case['パターン'],
                        case['手順'] if '手順' in case else [],
                        case['想定結果'],
                        case['エビデンス'] if 'エビデンス' in case and case['エビデンス'] == '要' else False
                    ))
                blockPerspectives.append(IntegratedTestPerspective(perspectiveName, cases))

            block = IntegratedTestBlock("共通", blockPerspectives)

            perspectiveRel = f"{typeName}_config/テスト観点.yml.j2"
            perspectiveAbs = f"{self.storageRoot}/{perspectiveRel}"

            logging.info(f"{perspectiveAbs}の読み込み開始")

            try:
                template = self.env.get_template(perspectiveRel)
            except TemplateNotFound:
                raise Exception(f"{perspectiveAbs}が見つかりません")

            perspectives = yaml.safe_load(template.render(dataSets))

            configs.append(IntegratedTestConfig(typeName, block, perspectives))

        return configs

    def _loadDataSets(self) -> dict:
        try:
            template = self.env.get_template("global_config/データセット.yml.j2")
        except TemplateNotFound:
            return {}
        data = yaml.safe_load(template.render())
        return data if data is not None else {}
