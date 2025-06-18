# uvを使用したPythonパッケージ管理ガイド

## プロジェクト管理の基本:

uvを使用したモダンなPython開発では、プロジェクトベースのアプローチを採用します。これにより、各プロジェクトが独立した環境と設定を持ち、依存関係の競合を回避できます。

新しいプロジェクトの作成:
```bash
# 新しいプロジェクトディレクトリを作成して初期化
uv init my-project
cd my-project

# 既存のディレクトリでプロジェクトを初期化
uv init

# 特定のPythonバージョンを指定してプロジェクトを初期化
uv init --python 3.11
```

`uv init`コマンドは、以下のファイルとディレクトリ構造を自動生成します：
- `pyproject.toml`: プロジェクトのメタデータと依存関係を管理
- `.python-version`: プロジェクトで使用するPythonバージョンを指定
- `README.md`: プロジェクトの説明文書
- `src/`: ソースコードディレクトリ（パッケージプロジェクトの場合）

プロジェクト情報の確認:
```bash
# プロジェクトの情報を表示
uv info

# 現在のPython環境を表示
uv python show
```

## 仮想環境の管理:

uvは仮想環境の作成と管理を自動化し、プロジェクトごとに独立した環境を提供します。多くの場合、uvは仮想環境を自動的に検出・作成するため、手動での管理は不要ですが、明示的な操作も可能です。

仮想環境の作成:
```bash
# デフォルトの仮想環境を作成
uv venv

# 特定の名前で仮想環境を作成
uv venv my-env

# 特定のPythonバージョンで仮想環境を作成
uv venv --python 3.11

# 仮想環境を削除してクリーンに再作成
uv venv --clear
```

仮想環境の有効化:
uvの多くのコマンドは仮想環境を自動的に検出して使用しますが、シェルで直接Pythonを実行する場合は仮想環境を有効化する必要があります：

```bash
# Unix-like システム（Linux, macOS）
source .venv/bin/activate

# Windows（Command Prompt）
.venv\Scripts\activate.bat

# Windows（PowerShell）
.venv\Scripts\Activate.ps1

# 仮想環境から抜ける
deactivate
```

## パッケージ管理:

uvは、従来のpipコマンドと互換性を保ちながら、より高速で信頼性の高いパッケージ管理を提供します。モダンなプロジェクト管理では`uv add`/`uv remove`を、従来のワークフローでは`uv pip`コマンドを使用できます。

モダンなパッケージ管理（推奨）:
```bash
# パッケージをプロジェクトに追加
uv add requests
uv add "django>=4.0,<5.0"

# 複数のパッケージを同時に追加
uv add requests pandas numpy

# 開発用依存関係を追加
uv add --dev pytest ruff mypy

# パッケージを削除
uv remove requests

# すべての依存関係をインストール（pyproject.tomlから）
uv sync

# 開発用依存関係も含めてインストール
uv sync --dev
```

## 依存関係管理:

uvは、再現可能な環境を構築するための強力な依存関係管理機能を提供します。これにより、開発、テスト、本番環境で同じ依存関係を確実に使用できます。

モダンな依存関係管理:
```bash
# 依存関係をロック（固定）
uv lock

# 特定のパッケージのみを更新
uv lock --upgrade-package requests

# すべての依存関係を最新に更新
uv lock --upgrade

# ロックファイルに基づいて環境を同期
uv sync

# 依存関係ツリーを表示
uv tree
```

## コマンドの実行:

uvは、仮想環境を明示的に有効化することなく、プロジェクトの適切な環境でコマンドを実行する機能を提供します。これにより、開発ワークフローが大幅に簡素化されます。

基本的な実行コマンド:
```bash
# Pythonスクリプトを実行
uv run python script.py

# Pythonモジュールを実行
uv run -m pytest
uv run ruff check .
uv run ruff format .

# 一時的な依存関係でスクリプトを実行
uv run --with requests python -c "import requests; print(requests.get('https://httpbin.org/json').json())"

# 複数の一時的な依存関係を指定
uv run --with requests --with beautifulsoup4 python scraper.py
```

実用的な使用例:
```bash
# テストの実行
uv run pytest tests/

# コードフォーマット
uv run ruff format src/

# リンティング
uv run ruff check src/

# Jupyter Notebookの起動
uv run jupyter notebook

# Django開発サーバーの起動
uv run python manage.py runserver
```

## Pythonバージョン管理:

uvは、プロジェクトごとに異なるPythonバージョンを管理する機能を提供します。これにより、システム全体のPython環境を変更することなく、プロジェクトに最適なPythonバージョンを使用できます。

Pythonバージョンの管理:
```bash
# 利用可能なPythonバージョンを表示
uv python list

# 特定のPythonバージョンをインストール
uv python install 3.11
uv python install 3.12

# プロジェクトのPythonバージョンを設定
uv python pin 3.11

# 現在使用中のPythonバージョンを表示
uv python show

# インストール済みのPythonバージョンを表示
uv python list --only-installed
```

## 設定とカスタマイズ:

uvの動作は、設定ファイルやコマンドラインオプションでカスタマイズできます。これにより、組織やプロジェクトの要件に合わせて動作を調整できます。

設定ファイルの場所:
- グローバル設定: `~/.config/uv/uv.toml`
- プロジェクト設定: `pyproject.toml`の`[tool.uv]`セクション

設定例:
```toml
# pyproject.toml内の設定例
[tool.uv]
index-url = "https://pypi.org/simple"
extra-index-url = ["https://download.pytorch.org/whl/cpu"]
no-cache = false
```

設定コマンド:
```bash
# 現在の設定を表示
uv config list

# 設定を変更
uv config set index-url https://pypi.org/simple

# キャッシュをクリア
uv cache clean

# 詳細なログを表示
uv --verbose add requests
```

## ベストプラクティス:

uvを効果的に使用するためのベストプラクティスを以下に示します。これらの実践により、より安全で効率的な開発環境を構築できます。

プロジェクト管理のベストプラクティス:
- 新しいプロジェクトでは必ず`uv init`から始める
- `pyproject.toml`を直接編集せず、`uv add`/`uv remove`を使用する
- `uv.lock`ファイルをバージョン管理システムにコミットして、チーム全体で同じ依存関係を共有する
- 定期的に`uv lock --upgrade`を実行して依存関係を最新に保つ

開発ワークフローのベストプラクティス:
- `uv run`を活用して仮想環境の有効化を自動化する
- CI/CDパイプラインでは`uv sync`を使用して高速で確実な環境構築を行う
- 開発用依存関係は`--dev`オプションを使用して本番環境と分離する

セキュリティのベストプラクティス:
- 信頼できるパッケージインデックスのみを使用する
- 定期的に`uv audit`（将来の機能）で脆弱性をチェックする
- ロックファイルを使用して依存関係のバージョンを固定する

## トラブルシューティング:

uvを使用する際によくある問題とその解決方法について説明します。

一般的な問題と解決方法:
```bash
# キャッシュが破損した場合
uv cache clean

# 依存関係の競合が発生した場合
uv lock --resolution lowest-direct

# 仮想環境をクリーンに再作成
uv venv --clear

# 詳細なエラー情報を表示
uv --verbose command

# プロジェクトの状態を確認
uv info
```

パフォーマンス最適化:
- 大規模なプロジェクトでは`--no-cache`オプションを避ける
- ネットワーク環境が不安定な場合は`--retries`オプションを使用
- 並列処理を活用するため、十分なメモリを確保する