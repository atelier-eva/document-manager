import logging
from lib.excel_lib import ExcelLib
from repository.integrated_test_config_repository import IntegratedTestConfigRepository
from repository.integrated_test_repository import IntegratedTestRepository
from src.integrated_test.integrated_test_specification import IntegratedTestSpecification
import sys

# 結合テスト仕様書を生成する
# コントローラー兼アプリケーションルール

# ログ設定
logging.basicConfig(
    filename='./storage/log/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

integratedTestConfigRepository = IntegratedTestConfigRepository()
integratedTestRepository = IntegratedTestRepository()

integratedTestConfigs = []
integratedTests = []
try:
    integratedTestConfigs = integratedTestConfigRepository.find()
    integratedTests = integratedTestRepository.get() if len(sys.argv) == 1 else [integratedTestRepository.find(sys.argv[1], sys.argv[2])]
except Exception as e:
    print(f"{e}")
    exit()

for index, integratedTest in enumerate(integratedTests):
    typeName = integratedTest.getType()

    # プレフィックス作成
    prefix = ""
    if typeName == 'batch':
        prefix = 'バッチ'
    elif typeName == 'component':
        prefix = 'コンポーネント'
    elif typeName == 'file':
        prefix = 'ファイル'
    elif typeName == 'view':
        prefix = 'ビュー'

    print(f"{prefix}_{integratedTest.getName()} 作成中...")

    # 結合テスト仕様書とタイプが同じの設定を取得
    integratedTestConfig = next((c for c in integratedTestConfigs if c.getType() == typeName), None)
    excel = IntegratedTestSpecification.toExcel(integratedTest, integratedTestConfig, prefix)
    ExcelLib.save(excel)
