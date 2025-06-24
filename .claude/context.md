---
author: null
category: concept
claude_feature:
- code-generation
claude_model: []
complexity: advanced
confidence: medium
created: 2025-06-19 00:00:00
domain:
- ai-ml
- data-science
- testing
- web-dev
project: claude-knowledge-catalyst
projects:
- claude-knowledge-catalyst
purpose: CKCプロジェクトの技術背景と開発制約の詳細
quality: high
status: production
subcategory: Development_Patterns
success_rate: null
tags:
- architecture
- background
- constraints
- context
- python
team: []
tech:
- python
- typescript
title: Context.md - プロジェクト背景と制約
type: prompt
updated: 2025-06-21 00:04:32.030015
version: '1.0'
---

# Context.md - プロジェクト背景と制約

## プロジェクト概要

**Claude Knowledge Catalyst (CKC)** は、Claude Code開発で得られた知見を自動的にObsidianなどの知識管理ツールと同期する包括的なナレッジマネジメントシステムです。

### 技術スタック
- **言語**: Python 3.11+
- **パッケージ管理**: uv (uvを使用した現代的なPython依存関係管理)
- **設定管理**: Pydantic（バリデーション付きデータモデル）
- **CLI**: Typer + Rich（美しいコマンドラインインターフェース）
- **ファイル監視**: Watchdog（デバウンス機能付きファイルシステム監視）
- **AI/ML**: YAKE (Yet Another Keyword Extractor) - 教師なしキーワード抽出
- **多言語対応**: langdetect, unidecode（自動言語検出と文字正規化）

### 核となる機能
1. **自動同期**: `.claude/`ディレクトリを監視してリアルタイム同期
2. **AI分類システム**: YAKE統合による高精度技術スタック検出とタグ自動生成
3. **メタデータ管理**: タグ、カテゴリ、成功指標による自動的なメタデータ強化
4. **テンプレートシステム**: プロンプト、コードスニペット、概念、プロジェクトログ用の豊富なテンプレート
5. **Obsidian統合**: Obsidianボルトとの深い統合（適切なディレクトリ構造とリンク）
6. **マルチプロジェクト対応**: 複数プロジェクトでのファイル分離と横断検索（詳細: `.claude/next_action.md`）
7. **成功追跡**: プロンプトの効果測定と継続的改善

## アーキテクチャ制約

### ディレクトリ構造
```
src/claude_knowledge_catalyst/
├── core/                   # コア機能
│   ├── config.py          # 設定管理
│   ├── metadata.py        # メタデータ抽出・管理
│   └── watcher.py         # ファイルシステム監視
├── ai/                    # AI分類システム
│   ├── smart_classifier.py # ハイブリッド分類エンジン
│   └── yake_extractor.py  # YAKE統合キーワード抽出
├── sync/                  # 同期モジュール
│   └── obsidian.py        # Obsidian統合
├── templates/             # テンプレートシステム
│   └── manager.py         # テンプレート管理
└── cli/                   # コマンドラインインターフェース
    └── main.py            # CLI実装
```

### 設計パターン
- **Pydanticモデル**: 設定とデータ検証
- **プラグインアーキテクチャ**: 拡張可能な同期ターゲット
- **ハイブリッドAI分類**: パターンマッチング + YAKE キーワード抽出
- **テンプレート駆動**: コンテンツ生成
- **イベント駆動**: ファイル同期
- **構造化メタデータ**: インテリジェントな組織化
- **後方互換性保証**: YAKE無効時のフォールバック機構

## 開発制約

### パッケージ管理
- **必須**: `uv`コマンドの使用（`pip`ではない）
- **開発環境セットアップ**: `uv sync --dev`
- **コマンド実行**: `uv run ckc [command]`
- **依存関係追加**: `uv add package-name`

### AI機能依存関係
```bash
# YAKE統合機能有効化
uv add yake>=0.4.8 langdetect>=1.0.9 unidecode>=1.3.0

# 分類機能無効時の動作確認
uv run pytest tests/test_yake_extractor.py::test_fallback_without_yake
```

### コード品質・CI/CD
```bash
# リンティング
uv run ruff check src/ tests/

# フォーマット
uv run ruff format src/ tests/

# 型チェック
uv run mypy src/

# テスト（AI機能含む）
uv run pytest tests/
uv run pytest --cov=src/claude_knowledge_catalyst --cov-report=html

# CI/CD (GitHub Actions)
# - 自動品質チェック（lint, format, test, security）
# - マルチPythonバージョンテスト（3.11, 3.12）
# - 自動リリース・PyPI公開
# - 依存関係脆弱性監視
```

### ファイルパス操作
- **必須**: `pathlib.Path`の使用（`os.path`ではない）
- **設定ファイル**: `ckc_config.yaml`（YAMLフォーマット）

## 重要な技術的決定

### メタデータ管理
- フロントマターとコンテンツから自動抽出
- 多次元タグシステム
- 成功率追跡（プロンプト効果測定）
- バージョン履歴管理

### Obsidian統合
- PARAメソッドに基づく自動ボルト構造作成
- 豊富なメタデータ付きフロントマター
- インテリジェントなファイル分類と配置
- クロスプロジェクト知識リンク

### エラーハンドリング
- 適切なエラーハンドリングパターンの実装
- 外部依存関係の適切なモック化
- エラー条件とエッジケースのテスト

## プロジェクト制約

### 設定管理
- `ckc_config.yaml`がメイン設定ファイル
- Pydanticによる設定検証
- 複数同期ターゲットのサポート

### 開発ワークフロー（CI/CD統合）
1. **新機能追加時**: Pydanticモデルを使用
2. **テスト**: 全ての核となる機能に包括的テスト
3. **CLI更新**: ユーザー向け機能の場合
4. **エラーハンドリング**: 既存パターンに従う
5. **型ヒント**: 全コードに型ヒント使用
6. **プルリクエスト**: 自動品質ゲート（blocking/non-blocking）
7. **リリース**: タグベース自動リリース（`v*`タグ）
8. **継続監視**: 依存関係・セキュリティ・プロジェクト健全性

### 知識組織システム
```
Obsidian_Vault/
├── 00_Inbox/                    # 未処理アイテム
├── 01_Projects/                 # プロジェクト固有知識
├── 02_Knowledge_Base/           # 共有知識
│   ├── Prompts/
│   ├── Code_Snippets/
│   ├── Concepts/
│   └── Resources/
├── 03_Templates/                # ノートテンプレート
├── 04_Analytics/                # 使用状況と効果指標
└── 05_Archive/                  # 非推奨知識
```

## 今後の課題

### 技術的負債
- テストカバレッジの向上
- より堅牢なエラーハンドリング
- パフォーマンス最適化

### 機能拡張
- Webインターフェース
- Notion統合
- AI駆動インサイト
- チームコラボレーション機能
- 高度な分析機能
- プラグインシステム
