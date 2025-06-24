---
author: null
category: concept
claude_feature:
- code-generation
- debugging
claude_model: []
complexity: advanced
confidence: medium
created: 2025-06-19 00:00:00
domain:
- ai-ml
- automation
- data-science
- devops
- mobile
- security
- testing
- web-dev
project: claude-knowledge-catalyst
projects:
- claude-knowledge-catalyst
purpose: CKCプロジェクトの開発環境設定とベストプラクティスの包括的ガイド
quality: high
status: production
subcategory: Development_Patterns
success_rate: null
tags:
- best-practices
- development
- environment
- guide
- python
- uv
team: []
tech:
- api
- git
- javascript
- python
- typescript
title: 開発環境ガイド
type: prompt
updated: 2025-06-21 00:04:32.024531
version: '1.0'
---

# 開発環境ガイド

Claude Knowledge Catalyst (CKC) の開発環境設定、コマンド、ベストプラクティスについて説明します。

## Development Environment

### Package Management
This project uses **uv** for modern Python package management. Always use uv commands for development:

```bash
# Install dependencies
uv sync --dev

# Run commands
uv run pytest
uv run ruff check src/ tests/
uv run ruff format src/ tests/
uv run mypy src/

# Add new dependencies
uv add package-name
uv add --dev dev-package-name
```

### Python Version
- **Required**: Python 3.11+
- **Specified in**: `.python-version` file
- **Use**: `uv python pin 3.11` to ensure correct version

## Development Commands

### Testing
```bash
uv run pytest                 # Run all tests
uv run pytest tests/test_config.py  # Run specific test file
uv run pytest --cov         # Run with coverage

# 🚨 IMPORTANT: このプロジェクトではテスト実行にuvを使用します
# ❌ python -m pytest ではなく ✅ uv run pytest を使用してください
```

### Code Quality
```bash
uv run ruff check src/ tests/   # Lint code (includes import sorting)
uv run ruff format src/ tests/  # Format code
uv run mypy src/                # Type checking
```

### Application Commands
```bash
uv run ckc init              # Initialize CKC in current directory
uv run ckc sync add vault obsidian /path/to/vault  # Add sync target
uv run ckc watch             # Start file watching
uv run ckc status            # Show current status
```

## Best Practices

### When Adding New Features
1. Use Pydantic models for data structures
2. Add comprehensive tests for new functionality
3. Update CLI commands if user-facing
4. Follow existing error handling patterns
5. Use type hints throughout

### Code Standards
- Follow PEP 8 with Ruff formatting and linting
- Use descriptive variable and function names
- Add docstrings for public APIs
- Implement proper error handling
- Use pathlib.Path for file operations

### Testing Requirements
- Unit tests for all core functionality
- Integration tests for sync operations
- Mock external dependencies appropriately
- Test error conditions and edge cases

## Configuration Management

### Files
- `ckc_config.yaml`: Main configuration file
- `pyproject.toml`: Project metadata and tool configuration
- `.python-version`: Python version specification

### Key Configuration Sections
- **sync_targets**: Knowledge management tool connections
- **tags**: Multi-dimensional tagging system
- **watch**: File monitoring settings
- **templates**: Template customization paths

## Common Development Tasks

### Adding a New Sync Target
1. Create new module in `sync/` directory
2. Implement sync manager class
3. Update configuration schema
4. Add CLI commands
5. Write comprehensive tests

### Extending Metadata System
1. Update KnowledgeMetadata model
2. Enhance extraction logic in MetadataManager
3. Update template system if needed
4. Add tests for new metadata fields

### Creating New Templates
1. Add template to TemplateManager
2. Create helper methods for template creation
3. Update CLI to support new template type
4. Document template structure

## UV Package Management詳細

### プロジェクト管理の基本
uvを使用したモダンなPython開発では、プロジェクトベースのアプローチを採用します。

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

プロジェクト情報の確認:
```bash
# プロジェクトの情報を表示
uv info

# 現在のPython環境を表示
uv python show
```

### 仮想環境の管理
uvは仮想環境の作成と管理を自動化し、プロジェクトごとに独立した環境を提供します。

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

### パッケージ管理
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

### 依存関係管理
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

### コマンドの実行
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
```

### Pythonバージョン管理
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

### ベストプラクティス
プロジェクト管理のベストプラクティス:
- 新しいプロジェクトでは必ず`uv init`から始める
- `pyproject.toml`を直接編集せず、`uv add`/`uv remove`を使用する
- `uv.lock`ファイルをバージョン管理システムにコミットして、チーム全体で同じ依存関係を共有する
- 定期的に`uv lock --upgrade`を実行して依存関係を最新に保つ

開発ワークフローのベストプラクティス:
- `uv run`を活用して仮想環境の有効化を自動化する
- CI/CDパイプラインでは`uv sync`を使用して高速で確実な環境構築を行う
- 開発用依存関係は`--dev`オプションを使用して本番環境と分離する

## バージョン管理戦略

### 現在のバージョニング状況（2025年6月19日更新）

CKCプロジェクトでは、適切なセマンティックバージョニング（SemVer）を採用し、パブリックリリースに向けた戦略的なバージョン管理を実装しています。

#### 現在のバージョン設定
- **現在のバージョン**: `v0.9.0`
- **開発ステータス**: Beta（プレリリース）
- **位置づけ**: パブリックリリース前の最終調整段階

#### バージョン管理ファイル
```
src/claude_knowledge_catalyst/__init__.py → __version__ = "0.9.0"
README.md → v0.9.0 表記で統一
pyproject.toml → "Development Status :: 4 - Beta"
```

#### 動的バージョン管理
- **hatch** を使用した動的バージョン管理を採用
- `pyproject.toml` の `[tool.hatch.version]` 設定により `__init__.py` から自動取得
- CLI から `uv run ckc --version` でバージョン確認可能

#### 将来のリリース計画
```
v0.9.x (現在)     → アルファ版改善・バグ修正
v1.0.0           → 初回パブリックリリース（機能安定化、ドキュメント完備）
v1.1.0           → AI支援機能拡張（コンテンツ改善提案、高度アナリティクス）
v1.2.0           → 構造管理機能（自動最適化、詳細検証）
v2.0.0           → エンタープライズ機能（Web インターフェース、チーム協働）
```

#### セマンティックバージョニング原則
- **PATCH (1.0.0 → 1.0.1)**: 後方互換性のあるバグ修正のみ
- **MINOR (1.0.0 → 1.1.0)**: 後方互換性のある新機能追加や改善
- **MAJOR (1.0.0 → 2.0.0)**: 後方互換性のない変更（破壊的変更）

#### バージョン確認コマンド
```bash
# バージョン情報の確認
uv run ckc --version
uv run ckc -v

# hatchによるバージョン確認
uv run hatch version

# Pythonからの確認
python -c "import src.claude_knowledge_catalyst; print(src.claude_knowledge_catalyst.__version__)"
```

#### バージョン変更プロセス
1. `src/claude_knowledge_catalyst/__init__.py` の `__version__` を更新
2. `README.md` 内のバージョン表記を統一
3. 必要に応じて `pyproject.toml` の Development Status を更新
4. 動的バージョン管理の動作確認
5. CLI からのバージョン確認テスト

この戦略により、プロジェクトの成熟度を適切に表現し、パブリックリリースに向けた明確なロードマップを提供しています。

## リリース管理戦略

### 現在のリリース管理状況（2025年6月19日更新）

CKCプロジェクトでは、モダンなリリース管理プロセスを採用し、自動化とベストプラクティスに基づいた戦略的なリリース管理を実装しています。

#### リリース管理の基本方針
- **Keep a Changelog形式**: 標準的なchangelog管理
- **セマンティックバージョニング**: 明確なバージョン戦略
- **自動PyPI公開**: GitHub Actions による自動化
- **Trusted Publisher**: セキュアなパッケージ公開
- **品質保証**: リリース前の包括的テスト

#### 現在のリリース状況
- **最新リリース**: `v0.9.1` (2025年6月19日)
- **PyPI公開状況**: ✅ 公開済み ([PyPI](https://pypi.org/project/claude-knowledge-catalyst/))
- **リリースタイプ**: Feature Release (CLAUDE.md同期機能追加)
- **次期リリース**: `v0.9.2` (バグ修正・改善)

### リリースプロセス

#### 1. プレリリース準備
```bash
# 開発ブランチでの最終確認
uv run pytest --cov                    # 全テスト実行
uv run ruff check src/ tests/          # コード品質チェック
uv run mypy src/                       # 型チェック

# バージョン更新
# src/claude_knowledge_catalyst/__init__.py の __version__ を更新
# README.md, README-ja.md のバージョン表記を更新

# CHANGELOG.md の更新
# Keep a Changelog形式で新機能・修正・変更を記録
```

#### 2. リリースコミット作成
```bash
# リリース用コミットの作成
git add .
git commit -m "chore: Prepare release v0.9.x

- Update version to 0.9.x
- Update CHANGELOG.md with new features
- Update documentation for new release

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# タグの作成
git tag -a v0.9.x -m "Release v0.9.x

New Features:
- Feature A
- Feature B

Bug Fixes:
- Fix A
- Fix B

Documentation:
- Updated installation guides
- Added new examples"
```

#### 3. 自動PyPI公開
```bash
# mainブランチへのプッシュとタグプッシュ
git push origin main
git push origin v0.9.x

# GitHub Actions が自動実行:
# 1. テストの実行
# 2. パッケージのビルド
# 3. PyPI への自動公開（Trusted Publisher）
```

### リリース管理ファイル

#### CHANGELOG.md (Keep a Changelog形式)
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.1] - 2025-06-19

### Added
- 🔒 Secure CLAUDE.md synchronization with section-level filtering
- Privacy-first design with sensitive information protection
- Configurable exclusion patterns for API keys and credentials

### Enhanced
- 📊 Enhanced metadata generation for CLAUDE.md files
- 🛡️ Case-insensitive section filtering support
- 🎯 Flexible configuration options for different project needs

### Security
- CLAUDE.md sync disabled by default for security
- Section-based filtering to exclude sensitive information
```

#### GitHub Actions Workflow (.github/workflows/publish.yml)
```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/claude-knowledge-catalyst
    permissions:
      id-token: write  # Trusted Publisher

    steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v3

    - name: Build package
      run: uv build

    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        packages-dir: dist/
```

### リリースタイプ別戦略

#### パッチリリース (v0.9.1 → v0.9.2)
```bash
# バグ修正・小さな改善のみ
# 後方互換性を保持
# 緊急修正の場合は即座にリリース

git checkout -b hotfix/v0.9.2
# バグ修正コミット
git tag v0.9.2
git push origin main --tags
```

#### マイナーリリース (v0.9.x → v0.10.0)
```bash
# 新機能追加・拡張
# 後方互換性を保持
# 包括的テストとドキュメント更新

git checkout -b feature/v0.10.0
# 新機能開発
# ドキュメント更新
# テスト追加
git tag v0.10.0
git push origin main --tags
```

#### メジャーリリース (v0.x.x → v1.0.0)
```bash
# 破壊的変更・大幅な改修
# マイグレーションガイド提供
# 事前告知とベータ期間

git checkout -b major/v1.0.0
# 破壊的変更の実装
# マイグレーションガイド作成
# 包括的ドキュメント更新
git tag v1.0.0
git push origin main --tags
```

### リリース後の手順

#### 1. 公開確認
```bash
# PyPI公開確認
curl -s https://pypi.org/pypi/claude-knowledge-catalyst/json | jq '.info.version'

# インストールテスト
uv pip install claude-knowledge-catalyst==$VERSION
uv run ckc --version
```

#### 2. ドキュメント更新確認
- README.md のバージョン表記
- Read the Docs の自動更新
- GitHub Releases の作成

#### 3. コミュニティ通知
- GitHub Discussions での発表
- プロジェクト関係者への通知

### リリース管理のベストプラクティス

#### 事前準備
- 包括的テストの実行と通過確認
- ドキュメントの更新と整合性確認
- CHANGELOG.md の詳細記録
- バージョン番号の一貫性確認

#### リリース実行
- 本番環境でのテスト実行
- ロールバック手順の準備
- リリースタイミングの調整
- 自動化プロセスの監視

#### リリース後
- インストール可能性の確認
- コミュニティフィードバックの収集
- 緊急修正の準備
- 次期リリース計画の策定

### リリース管理ツール

#### 使用ツール
- **uv**: パッケージ管理・ビルド
- **GitHub Actions**: CI/CD・自動公開
- **hatch**: 動的バージョン管理
- **PyPI Trusted Publisher**: セキュアな公開

#### 監視・確認
```bash
# リリース状況確認
gh release list
gh workflow list
curl -s https://pypi.org/pypi/claude-knowledge-catalyst/json | jq '.releases | keys'

# ダウンロード統計
curl -s https://pypistats.org/api/packages/claude-knowledge-catalyst/recent
```

この包括的なリリース管理戦略により、品質の高い安定したリリースプロセスを維持し、ユーザーに信頼性の高いソフトウェアを提供しています。

## デモスクリプト実行ガイドライン

デモおよびテストスクリプトでは、プロジェクトのルートディレクトリから適切にCKCコマンドを実行し、デモ環境をクリーンに保つことが重要です。

### 実行方法の原則

**❌ 問題のあるパターン：**
```bash
# PythonコードをBashスクリプト内で直接呼び出し
uv run python -c "
import sys, os
sys.path.insert(0, '$PROJECT_ROOT/src')
os.chdir('$demo_dir')
from claude_knowledge_catalyst.cli.main import main
main()
" "$@"
```

**✅ 推奨パターン：**
```bash
# デモディレクトリで閉じた実行
cd demo_directory
uv run --project "$PROJECT_ROOT" ckc [command]
```

### デモ環境の分離原則

- demoディレクトリ内のファイル生成はdemoディレクトリ内で完結させる
- プロジェクトルートでの不要なファイル生成を防ぐ
- demo/CLAUDE.mdで環境設定ルールを明確化

### 分類システムの課題と改善

**既知の問題：**
- CKCが再分類時にcategoryメタデータを無視する傾向
- tagsのpythonを優先して誤分類する問題
- Improvement_Logディレクトリの用途混乱

**改善提案：**
- categoryメタデータ優先のルーティングシステム
- ディレクトリ用途の明確化
- 10刻み番号システムの適切な実装

### 知見更新ワークフロー

**プロジェクト知見の管理方針：**
新たな知見が得られた際は、以下のファイルを体系的に更新する：

- `.claude/context.md`: 背景・制約・技術選定理由
- `.claude/project-knowledge.md`: 実装パターン・設計決定
- `.claude/project-improvements.md`: 試行錯誤・改善記録
- `.claude/common-patterns.md`: 定型実装・コマンドパターン

**一時ファイル管理：**
デバッグやテスト生成ファイルは`.claude/debugging-guide.md`のルールに従って適切に移動または削除する。整理は定期的に実施し、プロジェクトの清潔性を保つ。

## Troubleshooting

### Common Issues
- **Import errors**: Check if using `uv run` prefix
- **Permission errors**: Ensure proper file permissions for sync targets
- **Configuration errors**: Validate YAML syntax in config files
- **Sync failures**: Check target paths and permissions

### Debug Mode
Use `--verbose` flag with CLI commands for detailed logging:
```bash
uv run ckc --verbose sync run
```

### UV Troubleshooting
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

## リリース手順

CKCの新バージョンをリリースする際の標準手順を説明します。

### 前提条件
- テストが全て通過している（`uv run pytest`）
- コード品質チェックが完了している（`uv run ruff check && uv run mypy`）
- ドキュメントが更新されている
- CHANGELOGが更新されている

### リリース手順（v0.10.0の例）

#### 1. 最終準備
```bash
# 全てのテストを実行
uv run pytest

# コード品質チェック
uv run ruff check src/ tests/
uv run ruff format src/ tests/
uv run mypy src/

# デモスクリプトのテスト（必要に応じて）
./demo/demo.sh
./demo/tag_centered_demo.sh
```

#### 2. 変更をコミット
```bash
# 全ての変更をステージング
git add .
git add .claude/  # 開発ドキュメントも含める

# 統合コミット作成
git commit -m "enhance: Complete v0.10.0 with improved demos and updated .claude

- Add YAKE integration demonstration in demo.sh
- Fix CLI command compatibility in tag_centered_demo.sh
- Improve shell syntax compliance (shellcheck clean)
- Update README.md with accurate v0.10.0 feature descriptions
- Fix cleanup.sh directory structure alignment
- Update .claude/ knowledge base with v0.10.0 improvements

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

#### 3. タグ作成（既存タグ更新の場合）
```bash
# 既存タグを削除（未公開の場合のみ）
git tag -d v0.10.0

# 新しいタグを作成
git tag -a v0.10.0 -m "Release v0.10.0: YAKE Integration with Enhanced Demos

🚀 Core Features:
- Advanced YAKE keyword extraction system
- Multi-language support (7 languages including Japanese)
- Hybrid classification (pattern matching + AI enhancement)
- 147 passing tests, enhanced stability

🎯 Enhanced Demo Experience:
- Interactive YAKE integration demonstration
- Multi-language content analysis showcase
- Complete shell syntax compliance

📚 Knowledge Base Updates:
- Comprehensive development patterns
- YAKE integration lessons and best practices

Built with ❤️ by the Claude community"
```

#### 4. リモートにプッシュ
```bash
# mainブランチをプッシュ
git push origin main

# タグをプッシュ
git push origin v0.10.0
```

#### 5. GitHub Releasesを作成
```bash
# GitHub CLIを使用してリリースを作成
gh release create v0.10.0 \
  --title "Claude Knowledge Catalyst v0.10.0 - YAKE Integration Release" \
  --notes "$(cat <<'EOF'
# 🚀 Claude Knowledge Catalyst v0.10.0: YAKE Integration Release

## 🆕 Revolutionary Features

### YAKE Integration & Hybrid Classification
- **Advanced Keyword Extraction**: YAKE (Yet Another Keyword Extractor) unsupervised algorithm
- **Multi-language Support**: 7 languages including English, Japanese, Spanish, French, German, Italian, Portuguese
- **Hybrid Classification**: Pattern matching + AI enhancement for superior accuracy

### Enhanced Demo Experience
- **Interactive YAKE Demonstration**: Experience keyword extraction in action
- **Multi-language Content Analysis**: English + Japanese technical content
- **Complete Shell Compliance**: Error-free demo execution

## 🔧 Technical Improvements

### Test Suite Excellence
- **147 Passing Tests**: 0 failures, production-ready stability
- **Enhanced Coverage**: Improved from 19.33% to 28.25%
- **YAKE Module Coverage**: 88% with comprehensive test cases

## 🚀 Getting Started

\`\`\`bash
# Install or upgrade
pip install claude-knowledge-catalyst==0.10.0

# Experience YAKE integration
./demo/demo.sh
\`\`\`

**Built with ❤️ by the Claude community**
EOF
)"
```

#### 6. リリース確認
```bash
# リリースが正常に作成されたことを確認
gh release list

# 出力例:
# Claude Knowledge Catalyst v0.10.0 - YAKE Integration Release  Latest  v0.10.0  2025-06-22T09:35:11Z
```

### リリース後の確認事項

#### GitHub確認
- [ ] GitHub Releasesページで新バージョンが表示されている
- [ ] リリースノートが正確に表示されている
- [ ] "Latest"タグが新バージョンに付いている

#### 機能確認
- [ ] デモスクリプトが正常に動作する
- [ ] 新機能が期待通りに動作する
- [ ] 後方互換性が保たれている

### トラブルシューティング

#### タグが既に存在する場合
```bash
# ローカルタグを削除
git tag -d v0.10.0

# リモートタグを削除（必要に応じて）
git push origin --delete v0.10.0

# 新しいタグを作成してプッシュ
git tag -a v0.10.0 -m "Release notes..."
git push origin v0.10.0
```

#### GitHub Releaseの修正
```bash
# リリースを削除
gh release delete v0.10.0

# 新しいリリースを作成
gh release create v0.10.0 --title "..." --notes "..."
```

### ベストプラクティス

1. **セマンティックバージョニング**: MAJOR.MINOR.PATCH形式を遵守
2. **包括的なリリースノート**: 新機能、改善、破壊的変更を明記
3. **デモ品質**: リリース前にデモスクリプトの動作を確認
4. **ドキュメント同期**: リリースと同時にドキュメントを更新
5. **後方互換性**: 既存ユーザーへの影響を最小限に

## 全CIチェック項目のローカル実行

### 🚀 自動化されたCI事前確認 (推奨)

**pre-commit**システムが設定済みです。コミット時に自動でCIチェックが実行されます：

```bash
# 初回設定（既に設定済み）
uv run pre-commit install

# 手動で全ファイルをチェック
uv run pre-commit run --all-files

# 特定のhookのみ実行
uv run pre-commit run ruff
uv run pre-commit run mypy
uv run pre-commit run pytest

# 緊急時：pre-commitをスキップ（非推奨）
git commit --no-verify -m "emergency commit"
```

**自動実行される項目：**
- ✅ Ruffリンティング&フォーマット（自動修正付き）
- ✅ mypy型チェック
- ✅ pytest全テスト実行
- ✅ パッケージビルドテスト
- ✅ YAML/TOML構文チェック
- ✅ 空白・改行チェック

### 📋 手動CI確認（バックアップ方法）

GitHubActions CIで実行される全てのチェック項目をローカルで事前実行する手順：

### 前提条件
```bash
# 依存関係がインストールされていることを確認
uv sync --dev
```

### 全チェック項目の実行
```bash
# 1. Ruff リンティング&フォーマット
uv run ruff check src/ tests/          # リント検査
uv run ruff format src/ tests/         # コードフォーマット

# 2. mypy 型チェック
uv run mypy src/                       # 型注釈チェック

# 3. pytest テスト実行
uv run pytest                         # 全テスト実行
uv run pytest --cov                   # カバレッジ付きテスト

# 4. パッケージビルドテスト
uv build                              # パッケージビルド確認

# 5. セキュリティチェック (optional)
uv run bandit -r src/                 # セキュリティスキャン (要インストール)

# 6. ドキュメント生成 (optional)
uv run mkdocs build                   # ドキュメントビルド (要インストール)
```

### ワンライナー実行
```bash
# 基本チェック (必須項目)
uv run ruff check src/ tests/ && uv run ruff format src/ tests/ && uv run mypy src/ && uv run pytest && uv build

# 詳細チェック (推奨)
uv run ruff check src/ tests/ && uv run ruff format src/ tests/ && uv run mypy src/ && uv run pytest --cov && uv build && echo "✅ All CI checks passed!"
```

### エラー発生時の対処
```bash
# Ruffエラー修正
uv run ruff check src/ tests/ --fix    # 自動修正可能なエラーを修正

# 型エラー確認
uv run mypy src/ --show-error-codes    # エラーコード付きで表示

# 特定テストのみ実行
uv run pytest tests/test_specific.py   # 特定ファイルのテスト
```

### CI設定ファイルの確認
CIの詳細設定は `.github/workflows/ci.yml` で確認可能：
- test job: pytest実行
- integration-tests job: 統合テスト
- build-test job: パッケージビルド
- security job: セキュリティチェック
- docs job: ドキュメント生成

### 注意事項
- 全チェックが通ってからコミット・プッシュすることを強く推奨
- エラーが残っている状態でのプッシュはCI失敗の原因となる
- 大規模変更時は段階的にチェックを実行して問題を早期発見する
