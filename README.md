# 概要
結合テスト仕様書を Excel で生成する CLI ツール。

# インストール
[uv](https://docs.astral.sh/uv/) を使い、`main` ブランチの最新版を取り込む。

```bash
uv tool install document-manager --from git+https://github.com/atelier-eva/document-manager.git
```

更新する場合:

```bash
uv tool upgrade document-manager
```

# 推奨設定
## git
```bash
# 結合テスト仕様書のファイル名を日本語にする場合
git config --global core.quotepath false
```

# 使い方
## 初期化
任意のディレクトリで実行すると、カレントディレクトリに `storage/` 雛形が展開される。`*_config/` には設定ファイル、`*_example/` にはサンプル仕様、`global_config/` にはデータセット定義が置かれる。

```bash
document-manager init
# 既存ファイルを上書きしたい場合
document-manager init --force
```

## 入力ファイル形式
仕様書の入力ファイルは [Jinja2](https://jinja.palletsprojects.com/) テンプレートとして読み込まれる。レンダリング後に YAML / CSV としてパースされるため、テンプレート構文 (`{% for %}`, `{{ var }}`, `{% include %}` など) が利用できる。

| 種類 | 拡張子 |
| --- | --- |
| YAML 系（テストケース、テストデータ、事前準備・注意点、共通、テスト観点、データセット） | `.yml.j2` |
| マトリクス | `.csv.j2` |

`global_config/データセット.yml.j2` で定義した値はテンプレートのコンテキストとして全ファイルに渡される。

## 結合テスト仕様書
```bash
# 全体で共有するデータセットを作成する
# ./storage/integrated_test/global_config/データセット.yml.j2

# バッチのテストを作成する
# ./storage/integrated_test/batch
# ./storage/integrated_test/batch_config
# ./storage/integrated_test/batch_example

# コンポーネントのテストを作成する
# ./storage/integrated_test/component
# ./storage/integrated_test/component_config
# ./storage/integrated_test/component_example

# ファイルのテストを作成する
# ./storage/integrated_test/file
# ./storage/integrated_test/file_config
# ./storage/integrated_test/file_example

# 画面のテストを作成する
# ./storage/integrated_test/view
# ./storage/integrated_test/view_config
# ./storage/integrated_test/view_example
```

# チートシート
```bash
# 結合テスト仕様書作成(全て)
document-manager generate
# 結合テスト仕様書作成(指定)
document-manager generate batch 注文データ処理

# storage/ 雛形の展開
document-manager init
```

# 開発
リポジトリをクローンして開発する場合は `uv` を使う。

```bash
# 仮想環境作成 + ランタイム/開発依存のインストール
uv sync

# CLI のローカル動作確認
uv run document-manager generate batch 注文データ処理

# 単体テスト
uv run python -m unittest discover tests

# wheel ビルド (dist/ に出力)
uv build --wheel
```
