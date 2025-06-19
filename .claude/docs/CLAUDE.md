# ドキュメントガイド

このドキュメントはSphinxドキュメントに関する包括的なガイドです。

## アーキテクチャ

このプロジェクトはSphinxドキュメント生成の自動化システムです：

- **設定管理**: `.claude/docs/config/`でテーマや拡張機能を集中管理
- **コマンドシステム**: `.claude/commands/`でSphinx操作を標準化
- **技術スタック**: Sphinx + MyST Parser + Furo テーマ + uv パッケージ管理

## 開発用コマンド

### 基本的なワークフロー
```bash
# 初期セットアップ
uv sync --group docs

# Sphinxプロジェクト作成
/project:sphinx-create

# 設定更新
/project:sphinx-update

# ドキュメントビルド  
/project:sphinx-build
```

### ビルドコマンド
- `uv run sphinx-build -b html ./docs ./docs/_build/html` - HTMLビルド
- `uv run sphinx-build -E -a -b html ./docs ./docs/_build/html` - クリーンビルド
- `uv run sphinx-build -b latex ./docs ./docs/_build/latex` - LaTeXビルド

### 依存関係管理
```bash
# ドキュメント依存関係の同期
uv sync --group docs

# 新しいドキュメント用パッケージの追加
uv add <package-name> --group docs
```

## アーキテクチャ

### プロジェクト構造
このプロジェクトはSphinxドキュメント生成の自動化システムです。

- `docs/` - Sphinxドキュメントファイル
- `.claude/commands/` - プロジェクト固有のコマンド定義
- `.claude/docs/config/` - 設定ファイル（テーマ、拡張機能）

### 設定管理システム
設定は `.claude/docs/config/` 配下で管理され、YAML Front Matterを使用：

- `theme-settings.md` - テーマとその設定
- `extensions-config.md` - 拡張機能とその設定

### コマンドシステム
- `sphinx-create` - 新規Sphinxプロジェクトの初期化
- `sphinx-update` - 設定ファイルからconf.pyの更新
- `sphinx-build` - ドキュメントビルド

### 技術スタック
- **Sphinx**: ドキュメント生成エンジン
- **MyST Parser**: Markdownサポート
- **Furo**: デフォルトテーマ
- **uv**: Python パッケージ管理

## 重要な注意事項

設定変更時は必ず `/project:sphinx-update` を実行してconf.pyに反映させること。