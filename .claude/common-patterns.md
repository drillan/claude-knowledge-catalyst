---
author: null
category: concept
claude_feature:
- code-generation
- analysis
claude_model: []
complexity: advanced
confidence: medium
created: 2025-06-19 00:00:00
domain:
- ai-ml
- automation
- data-science
- security
- testing
- web-dev
project: claude-knowledge-catalyst
projects:
- claude-knowledge-catalyst
purpose: CKC開発でよく使用するコマンドパターンの集約
quality: high
status: production
subcategory: Development_Patterns
success_rate: null
tags:
- best-practices
- commands
- development
- patterns
- workflow
team: []
tech:
- api
- git
- javascript
- python
- typescript
title: Common Patterns - よく使用するコマンドパターン
type: prompt
updated: 2025-06-21 00:04:32.031066
version: '1.0'
---

# Common Patterns - よく使用するコマンドパターン

> **関連情報**: 現在の優先課題とアクションアイテムについては `.claude/next_action.md` を参照

## 開発環境セットアップ

### プロジェクト初期化
```bash
# 新しいプロジェクトでの初期化
cd /path/to/new/project
uv run ckc init

# CKCの初期化確認
uv run ckc status
```

### 開発依存関係のインストール
```bash
# 開発環境の完全セットアップ
uv sync --dev

# 新しい依存関係の追加
uv add pydantic
uv add --dev pytest

# 依存関係の確認
uv tree
```

## 日常的な開発コマンド

### コード品質チェック
```bash
# 全体的なコード品質チェック（よく使用）
uv run ruff check src/ tests/ && uv run ruff format src/ tests/ && uv run mypy src/

# 段階的チェック
uv run ruff check src/ tests/     # リンティング
uv run ruff format src/ tests/    # フォーマット
uv run mypy src/                  # 型チェック
```

### テスト実行
```bash
# 全テスト実行
uv run pytest

# カバレッジ付きテスト
uv run pytest --cov=src --cov-report=html

# 特定のテストファイル
uv run pytest tests/test_config.py

# 特定のテストケース
uv run pytest tests/test_config.py::test_load_valid_config

# 失敗したテストのみ再実行
uv run pytest --lf
```

### CKC操作コマンド

#### 基本操作
```bash
# 現在のステータス確認
uv run ckc status

# 設定の表示
uv run ckc config show

# ヘルプの表示
uv run ckc --help
uv run ckc sync --help
```

#### 同期管理
```bash
# 同期ターゲットの一覧表示
uv run ckc sync list

# Obsidianボルトの追加
uv run ckc sync add my-vault obsidian /path/to/obsidian/vault

# 同期ターゲットの削除
uv run ckc sync remove my-vault

# 手動同期実行
uv run ckc sync run

# 特定ターゲットへの同期
uv run ckc sync run --target my-vault

# プロジェクトコンテキスト付き同期
uv run ckc sync run --project "Claude Knowledge Catalyst"
```

#### ファイル監視
```bash
# ファイル監視開始
uv run ckc watch

# 詳細ログ付き監視
uv run ckc --verbose watch

# 特定パターンのファイルのみ監視
uv run ckc watch --pattern "*.md"
```

## デバッグとトラブルシューティング

### ログとデバッグ
```bash
# 詳細ログでの実行
uv run ckc --verbose status
uv run ckc --verbose sync run

# 設定ファイルの問題診断
uv run ckc config validate

# 同期ターゲットの接続テスト
uv run ckc sync test my-vault
```

### ファイル分析
```bash
# メタデータ分析
uv run ckc analyze .claude/context.md

# ファイル内容の検証
uv run ckc validate .claude/project-knowledge.md
```

## Git操作パターン

### 基本的なGitワークフロー
```bash
# 現在の状態確認
git status
git diff

# ステージングと コミット
git add .claude/
git commit -m "Add knowledge management structure

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# プッシュ
git push origin main
```

### ブランチ操作
```bash
# 新機能ブランチの作成
git checkout -b feature/knowledge-management
git push -u origin feature/knowledge-management

# マージとクリーンアップ
git checkout main
git merge feature/knowledge-management
git branch -d feature/knowledge-management
git push origin --delete feature/knowledge-management
```

## 設定管理パターン

### 設定ファイルの編集
```bash
# 設定ファイルの編集
nano ckc_config.yaml
# または
code ckc_config.yaml

# 設定の検証
uv run ckc config validate

# デフォルト設定の生成
uv run ckc config init
```

### 環境変数の設定
```bash
# 開発環境での設定
export CKC_CONFIG_PATH="/path/to/ckc_config.yaml"
export CKC_LOG_LEVEL="DEBUG"
export CKC_VAULT_PATH="/path/to/obsidian/vault"
```

## パフォーマンス監視

### システムリソース監視
```bash
# CPU使用率の監視（ファイル監視中）
top -p $(pgrep -f "ckc watch")

# メモリ使用量の確認
ps aux | grep "ckc"

# ファイルディスクリプタの使用状況
lsof -p $(pgrep -f "ckc watch")
```

### 同期パフォーマンス
```bash
# 同期時間の測定
time uv run ckc sync run

# 同期ファイル数の確認
uv run ckc sync stats
```

## よく使用するファイル操作

### .claudeディレクトリの操作
```bash
# ディレクトリ構造の確認
tree .claude

# ファイルの一覧表示
ls -la .claude/

# 特定ファイルの内容確認
cat .claude/context.md
head -20 .claude/project-knowledge.md
tail -10 .claude/debug-log.md
```

### バックアップとリストア
```bash
# .claudeディレクトリのバックアップ
tar -czf claude-backup-$(date +%Y%m%d).tar.gz .claude/

# バックアップからのリストア
tar -xzf claude-backup-20240617.tar.gz
```

## トラブルシューティングパターン

### 一般的な問題の診断
```bash
# 設定ファイルの構文チェック
python -c "import yaml; yaml.safe_load(open('ckc_config.yaml'))"

# Python環境の確認
uv run python --version
uv run python -c "import claude_knowledge_catalyst; print('OK')"

# 依存関係の確認
uv run pip list | grep claude
```

### AI分類システムのテストパターン

```bash
# YAKE統合機能のテスト
uv run pytest tests/test_yake_extractor.py -v

# YAKE利用可能性の確認
uv run python -c "from claude_knowledge_catalyst.ai.yake_extractor import YAKE_AVAILABLE; print(f'YAKE Available: {YAKE_AVAILABLE}')"

# ハイブリッド分類のテスト
uv run pytest tests/test_ai_smart_classifier.py::TestYAKEIntegration -v

# 分類機能のクイックテスト
uv run python -c "
from claude_knowledge_catalyst.ai.smart_classifier import SmartContentClassifier
classifier = SmartContentClassifier()
result = classifier.classify_technology('def fibonacci(n): return n')
print(f'Tech: {result.suggested_value}, Confidence: {result.confidence:.2f}')
"

# 実用性能での分類テスト
uv run python -m claude_knowledge_catalyst.cli.main classify .claude --batch --format json

# 依存関係の追加/削除
uv add yake>=0.4.8 langdetect>=1.0.9 unidecode>=1.3.0  # YAKE機能有効化
uv remove yake langdetect unidecode                     # YAKE機能無効化
```

### 包括的評価パターン

```bash
# 6段階評価プロセスの実行
python migration-test/claude_migration_comparison.py

# テストカバレッジ測定
uv run pytest --cov=src/claude_knowledge_catalyst --cov-report=html --cov-report=term

# パフォーマンス比較テスト
uv run python comparison-test/comparison_script.py

# ブランチ別機能比較
git checkout baseline-v0.9.2 && uv run ckc classify .claude --batch
git checkout feature/yake-integration && uv run ckc classify .claude --batch
```

### ファイル権限の修正
```bash
# .claudeディレクトリの権限修正
chmod -R 755 .claude/
chmod 644 .claude/*.md

# 設定ファイルの権限修正
chmod 600 ckc_config.yaml
```

### 同期問題の診断
```bash
# 同期ターゲットの存在確認
ls -la /path/to/obsidian/vault

# 書き込み権限の確認
touch /path/to/obsidian/vault/.test_file && rm /path/to/obsidian/vault/.test_file

# ディスク容量の確認
df -h /path/to/obsidian/vault
```

## スクリプト自動化例

### 毎日の作業開始スクリプト
```bash
#!/bin/bash
# start-work.sh

echo "🚀 CKC作業開始"

# プロジェクトディレクトリに移動
cd /path/to/claude-knowledge-catalyst

# ステータス確認
echo "📊 現在のステータス:"
uv run ckc status

# ファイル監視開始
echo "👁️ ファイル監視開始"
uv run ckc watch &

echo "✅ セットアップ完了!"
```

### コードレビュー前チェックスクリプト
```bash
#!/bin/bash
# pre-review.sh

echo "🔍 コードレビュー前チェック開始"

# コード品質チェック
echo "📋 リンティング..."
uv run ruff check src/ tests/ || exit 1

echo "🎨 フォーマットチェック..."
uv run ruff format --check src/ tests/ || exit 1

echo "🔍 型チェック..."
uv run mypy src/ || exit 1

echo "🧪 テスト実行..."
uv run pytest || exit 1

echo "📄 ドキュメント更新チェック..."
uv run ckc config validate || exit 1

echo "✅ 全チェック完了! レビュー準備OK"
```

## 緊急時の対応コマンド

### サービス停止と再起動
```bash
# 監視プロセスの停止
pkill -f "ckc watch"

# プロセス確認
ps aux | grep ckc

# 強制終了（必要な場合のみ）
pkill -9 -f "ckc watch"

# サービス再起動
uv run ckc watch &
```

### 設定のリセット
```bash
# 設定ファイルのバックアップ
cp ckc_config.yaml ckc_config.yaml.backup

# デフォルト設定の再生成
uv run ckc config init --force

# 設定の復元（必要に応じて）
cp ckc_config.yaml.backup ckc_config.yaml
```