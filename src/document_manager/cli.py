import argparse
import importlib.resources as resources
import logging
import os
import shutil
import sys
from pathlib import Path

from document_manager.lib.excel_lib import ExcelLib
from document_manager.repository.integrated_test_config_repository import IntegratedTestConfigRepository
from document_manager.repository.integrated_test_repository import IntegratedTestRepository
from document_manager.integrated_test.integrated_test_specification import IntegratedTestSpecification

# 結合テスト仕様書を生成する
# コントローラー兼アプリケーションルール

def main() -> int:
    parser = argparse.ArgumentParser(prog="document-manager")
    sub = parser.add_subparsers(dest="command")

    g = sub.add_parser("generate", help="結合テスト仕様書を生成")
    g.add_argument("type", nargs="?", choices=["batch", "component", "file", "view"])
    g.add_argument("name", nargs="?")

    i = sub.add_parser("init", help="カレントディレクトリに storage 雛形を展開")
    i.add_argument("--force", action="store_true", help="既存ファイルを上書きする")

    args = parser.parse_args()

    if args.command == "init":
        return run_init(force=args.force)
    if args.command in (None, "generate"):
        type_name = getattr(args, "type", None)
        name = getattr(args, "name", None)
        return run_generate(type_name, name)

    parser.print_help()
    return 1


def run_generate(type_name, name) -> int:
    # ログ設定
    os.makedirs('./storage/log', exist_ok=True)
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
        if type_name and name:
            integratedTests = [integratedTestRepository.find(type_name, name)]
        elif type_name or name:
            print("type と name は両方指定してください")
            return 1
        else:
            integratedTests = integratedTestRepository.get()
    except Exception as e:
        print(f"{e}")
        return 1

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

    return 0


def run_init(force: bool = False) -> int:
    src_root = resources.files("document_manager").joinpath("templates", "integrated_test")
    dest_root = Path("./storage/integrated_test")

    counts = {"copied": 0, "skipped": 0}
    _copy_tree(src_root, dest_root, force, counts)
    print(f"完了: {counts['copied']} 件作成, {counts['skipped']} 件スキップ")
    return 0


def _copy_tree(src, dest: Path, force: bool, counts: dict) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target_name = item.name
        if target_name.endswith(".example"):
            target_name = target_name[: -len(".example")]
        target = dest / target_name

        if item.is_dir():
            _copy_tree(item, target, force, counts)
            continue

        if target.exists() and not force:
            print(f"skip (exists): {target}")
            counts["skipped"] += 1
            continue

        with item.open("rb") as fsrc, open(target, "wb") as fdst:
            shutil.copyfileobj(fsrc, fdst)
        print(f"created: {target}")
        counts["copied"] += 1


if __name__ == "__main__":
    sys.exit(main())
