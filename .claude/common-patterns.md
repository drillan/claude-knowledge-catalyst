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

# YAKE統合後のテスト実行パターン
uv run pytest tests/test_yake_extractor.py -v
uv run pytest tests/test_ai_smart_classifier.py -v
uv run pytest --tb=short  # 147 tests passing確認

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

### コードレビュー前チェックスクリプト（CI/CD対応）
```bash
#!/bin/bash
# pre-review.sh - CI/CDパイプライン準拠

echo "🔍 コードレビュー前チェック開始 (CI/CD準拠)"

# CI/CDと同等の品質チェック実行
echo "📋 リンティング (blocking)..."
uv run ruff check src/ tests/ || exit 1

echo "🎨 フォーマットチェック (blocking)..."
uv run ruff format --check src/ tests/ || exit 1

echo "🧪 必須テスト実行 (blocking)..."
uv run pytest tests/test_essential_features.py || exit 1

echo "🔒 セキュリティスキャン (blocking)..."
uv run bandit -r src/ || exit 1

echo "📦 ビルド検証 (blocking)..."
uv build || exit 1

echo "🔍 型チェック (non-blocking warning)..."
uv run mypy src/ || echo "⚠️ Type check warnings (non-blocking)"

echo "🧪 全テスト実行 (coverage)..."
uv run pytest --cov=src --cov-report=term-missing || echo "⚠️ Some tests failed (check coverage)"

echo "📄 ドキュメント更新チェック..."
uv run ckc config validate || exit 1

echo "✅ CI/CD準拠チェック完了! PR準備OK"
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

## YAKE統合開発パターン (v0.10.0+)

### YAKE機能のテスト
```bash
# YAKE抽出器の個別テスト
uv run pytest tests/test_yake_extractor.py::TestYAKEKeywordExtractor::test_extract_keywords_english -v

# 多言語対応テスト
uv run pytest tests/test_yake_extractor.py::TestYAKEKeywordExtractor::test_extract_keywords_japanese -v

# SmartClassifier統合テスト
uv run pytest tests/test_ai_smart_classifier.py::TestSmartContentClassifier::test_enhance_metadata -v

# YAKE統合全体テスト
uv run pytest tests/test_yake_extractor.py tests/test_ai_smart_classifier.py -v
```

### YAKE設定の調整パターン
```python
# ckc_config.yaml でのYAKE設定カスタマイズ例
ai_classification:
  yake_enabled: true
  yake_config:
    max_ngram_size: 3           # 技術用語(1-3語)に最適
    deduplication_threshold: 0.7 # 重複排除閾値
    max_keywords: 20            # 抽出上限
    confidence_threshold: 0.5   # 品質フィルタ
    supported_languages:
      japanese: "ja"
      english: "en"
```

### YAKE統合デバッグパターン
```bash
# YAKE抽出の確認（開発時）
uv run python -c "
from claude_knowledge_catalyst.ai.yake_extractor import YAKEKeywordExtractor
extractor = YAKEKeywordExtractor()
result = extractor.extract_keywords('FastAPIの認証システム実装', 'ja')
print([k.text for k in result])
"

# SmartClassifier統合確認
uv run python -c "
from claude_knowledge_catalyst.ai.smart_classifier import SmartContentClassifier
classifier = SmartContentClassifier(enable_yake=True)
suggestions = classifier.generate_tag_suggestions('FastAPI JWT authentication')
print([s.suggested_value for s in suggestions])
"
```

### リリース準備パターン (v0.10.0での知見)
```bash
# 1. フィーチャーブランチでの開発
git checkout -b feature/yake-integration
# ... 開発作業 ...

# 2. テスト全体実行と確認
uv run pytest --tb=short
# 期待: 147 passed, X skipped, 0 failures

# 3. 不要ファイルクリーンアップ
rm -rf demo/ comparison-test/ migration-test/ coverage.json
git add .gitignore  # 除外パターン追加

# 4. ドキュメント整合性確認
# - README.md: バージョン更新
# - CHANGELOG.md: 新機能記載
# - docs/: 新機能ガイド追加

# 5. mainマージとタグ作成
git checkout main
git merge feature/yake-integration
git tag -a v0.10.0 -m "Release v0.10.0: YAKE Integration"

# 6. 最終テスト
uv run pytest --tb=short  # 147 passed確認
```

### YAKE統合時の一般的な問題と解決
```bash
# 問題1: numpy.float64型エラー
# 解決: float()変換を追加
score_float = float(score) if not isinstance(score, (int, float)) else score

# 問題2: tuple unpacking順序エラー
# 確認: YAKEは(text, score)でなく(score, text)を返す場合がある
keywords = yake_extractor.extract_keywords(text)
for keyword, score in keywords:  # 順序要確認

# 問題3: 言語検出失敗
# 解決: フォールバック機構
detected_lang = language or self.language_detector.detect_language(content)
if detected_lang not in self.config.supported_languages:
    detected_lang = 'en'  # デフォルト
```

## CI/CD操作パターン (Phase 3対応)

### GitHub Actions ローカル確認
```bash
# GitHub CLI経由でのワークフロー状況確認
gh workflow list
gh workflow view ci.yml
gh run list --workflow=ci.yml

# 最新ワークフロー実行の詳細
gh run view --log

# 失敗したジョブの詳細確認
gh run view <run_id> --job=<job_id> --log
```

### CI/CDパイプライン手動実行パターン
```bash
# リリース用タグ作成 (自動リリーストリガー)
git tag -a v1.2.3 -m "Release v1.2.3: New features and bug fixes"
git push origin v1.2.3

# プレリリース作成
git tag -a v1.2.3-rc1 -m "Release candidate v1.2.3-rc1"
git push origin v1.2.3-rc1

# タグ削除（必要時）
git tag -d v1.2.3
git push origin --delete v1.2.3
```

### 品質ゲート対応パターン
```bash
# PRマージ前の必須チェック (blocking)
uv run ruff check src/ tests/                    # Lint errors
uv run ruff format --check src/ tests/           # Format errors
uv run pytest tests/test_essential_features.py   # Essential tests
uv build                                         # Package build
uv run pytest --cov=src --cov-report=term | grep "TOTAL.*[2-5][0-9]%"  # Coverage ≥25%

# 警告レベルチェック (non-blocking)
uv run mypy src/                                 # Type check warnings
uv run pytest tests/test_integration_comprehensive.py  # Integration warnings
uv run bandit -r src/                            # Security warnings
```

### 依存関係管理自動化
```bash
# 手動依存関係更新（週次メンテナンス準拠）
uv lock --upgrade
uv sync

# セキュリティチェック
uv run safety check
uv run bandit -r src/

# 更新後のテスト確認
uv run pytest --tb=short

# 自動PR作成用の変更準備
git add uv.lock
git commit -m "chore: update dependencies"
```

### リリース管理パターン
```bash
# リリース準備チェックリスト
echo "🚀 リリース準備チェック"
echo "✅ All tests passing: $(uv run pytest --tb=no -q && echo 'PASS' || echo 'FAIL')"
echo "✅ Coverage adequate: $(uv run pytest --cov=src --cov-report=term | grep TOTAL)"
echo "✅ Build successful: $(uv build && echo 'PASS' || echo 'FAIL')"
echo "✅ Security clean: $(uv run bandit -r src/ -q && echo 'PASS' || echo 'FAIL')"

# セマンティックバージョン判定
echo "📋 Version increment guidance:"
echo "- patch (x.x.X): Bug fixes, documentation"
echo "- minor (x.X.x): New features, backward compatible"
echo "- major (X.x.x): Breaking changes"

# リリースノート準備
echo "📝 Release notes template:"
echo "## New Features"
echo "## Bug Fixes"
echo "## Breaking Changes"
echo "## Documentation"
```

### モニタリング・ヘルスチェック
```bash
# プロジェクト健全性の週次確認
echo "📊 Project Health Report $(date)"
echo "- Active branches: $(git branch -r | wc -l)"
echo "- Test coverage: $(uv run pytest --cov=src --cov-report=term | grep TOTAL)"
echo "- Dependencies: $(uv pip list | wc -l) packages"
echo "- Last release: $(git tag --sort=-version:refname | head -1)"
echo "- Open issues: $(gh issue list --state open | wc -l)"
echo "- Open PRs: $(gh pr list --state open | wc -l)"

# CI/CDパイプライン成功率
gh run list --workflow=ci.yml --limit=10 --json conclusion | jq '.[] | .conclusion' | sort | uniq -c
```

### トラブルシューティング：CI/CD編
```bash
# GitHub Actions デバッグ
# 1. ワークフロー失敗の原因特定
gh run view --log | grep -E "(FAIL|ERROR|✗)"

# 2. 特定ジョブの詳細確認
gh run view <run_id> --job test --log

# 3. secrets/variables確認（管理者のみ）
gh secret list
gh variable list

# 4. ワークフロー再実行
gh run rerun <run_id>

# 5. ローカルでの CI 環境再現
docker run --rm -v $(pwd):/workspace -w /workspace python:3.11 bash -c "
    pip install uv &&
    uv sync --dev &&
    uv run pytest --tb=short
"
```
