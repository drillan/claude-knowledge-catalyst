---
title: "ドキュメントガイド"
created: "2025-06-19"
updated: "2025-06-19"
version: "1.0"
category: "concept"
subcategory: "Development_Patterns"
tags: ["documentation", "sphinx", "guide", "architecture", "workflow"]
complexity: "intermediate"
quality: "high"
purpose: "Sphinxドキュメントシステムの包括的ガイド"
project: "claude-knowledge-catalyst"
status: "production"
---

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

## ドキュメンテーション方針

### 「AI」表現に関する方針

**背景**: 2025年6月21日に「AI」表現の見直しを実施。実装（ルールベースアルゴリズム）と表現の乖離を解消。

**基本方針**:
- 誇張的な「AI」表現を避け、技術的正確性を重視
- 実装に即した適切な表現を使用
- ユーザーにとって分かりやすい表現を優先

**表現ガイドライン**:
```yaml
# 推奨表現への変更
旧表現 → 新表現:
  "AI-powered": "Automated" / "Algorithm-based"
  "AI搭載": "自動化" / "自動"
  "AI分析": "自動分析" / "コンテンツ分析"
  "AIインテリジェント": "スマート" / "自動分類"
  "AI-Enhanced": "Enhanced" / "Smart-enhanced"
  "AI判定": "自動判定" / "パターン認識"

# 設定項目の変更
設定名変更:
  "ai_classification": "auto_classification"
  "ai:": "automation:"
```

**適用範囲**:
- README.md / README-ja.md
- docs/ 配下の全ドキュメント
- demo/README.md
- CHANGELOG.md
- 新規作成するドキュメント全般

**将来対応**:
- ロードマップでのML/AIモデル開発計画は保持
- 実際にAI/MLを実装した際は適切な表現に更新
- 技術的正確性を常に最優先