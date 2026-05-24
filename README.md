# 推奨設定
## git
```bash
# 結合テスト仕様書のファイル名を日本語にする場合
git config --global core.quotepath false
```

# 使い方
## 結合テスト仕様書
```bash
# 全体で共有するデータセットを作成する
# ./storage/integrated_test/global_config/データセット.yml

# バッチのテストを作成する
# ./storage/integrated_test/batch
# ./storage/integrated_test/batch_config
# ./storage/integrated_test/batch_config_example

# コンポーネントのテストを作成する
# ./storage/integrated_test/component
# ./storage/integrated_test/component_config
# ./storage/integrated_test/component_config_example

# ファイルのテストを作成する
# ./storage/integrated_test/file
# ./storage/integrated_test/file_config
# ./storage/integrated_test/file_config_example

# 画面のテストを作成する
# ./storage/integrated_test/view
# ./storage/integrated_test/view_config
# ./storage/integrated_test/view_config_example
```

# チートシート
```bash
# 結合テスト仕様書作成(全て)
poetry run python create_integrated_test.py
# 結合テスト仕様書作成(指定)
poetry run python create_integrated_test.py batch 注文データ処理

# 単体テスト
python -m unittest tests.{module_name}
```
