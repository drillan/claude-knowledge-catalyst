# Claude Knowledge Catalyst (CKC) v0.9.1

**Claude Code ⇄ Obsidian シームレス統合システム**

Claude Code開発プロセスで生まれる知見を自動的にObsidianボルトと同期し、構造化された知識管理を実現。AI搭載分析により、手動分類の負荷を軽減します。

> **[📋 日本語版](README-ja.md)** | **[🌐 Documentation](https://claude-knowledge-catalyst.readthedocs.io/)**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/claude-knowledge-catalyst.svg)](https://pypi.org/project/claude-knowledge-catalyst/)
[![PyPI downloads](https://img.shields.io/pypi/dm/claude-knowledge-catalyst.svg)](https://pypi.org/project/claude-knowledge-catalyst/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Documentation](https://img.shields.io/badge/docs-readthedocs-brightgreen.svg)](https://claude-knowledge-catalyst.readthedocs.io/)

## 🎯 Claude Code ⇄ Obsidian シームレス統合

### 🔄 自動同期システム
- **リアルタイム同期**: `.claude/`ディレクトリの変更を即座にObsidianボルトに反映
- **双方向連携**: Claude Code開発とObsidian知識管理の完全統合
- **構造化組織**: Obsidianの強力な機能を活用した知識体系化

### 🤖 AI搭載メタデータ強化
- **自動分析**: コンテンツを解析してObsidian用メタデータを生成
- **インテリジェントタグ付け**: 手動分類負荷を軽減する多次元タグシステム
- **証拠ベース分類**: AI判定の根拠を明示した信頼性の高い組織化

```yaml
# AI強化メタデータ例（副次的効果）
type: [prompt, code, concept, resource]           # コンテンツ性質
tech: [python, react, fastapi, kubernetes, ...]   # 技術スタック
domain: [web-dev, ml, devops, mobile, ...]        # アプリケーション領域
team: [backend, frontend, ml-research, devops]    # チーム所有権
status: [draft, tested, production, deprecated]   # ライフサイクル状態
complexity: [beginner, intermediate, advanced]    # スキルレベル
confidence: [low, medium, high]                   # コンテンツ信頼性
```

### 🏛️ Obsidian最適化ボルト構造
```
obsidian-vault/
├── _system/          # テンプレートと設定
├── _attachments/     # メディアファイル
├── inbox/            # 未処理コンテンツ
├── active/           # 作業中コンテンツ
├── archive/          # 完了・非推奨コンテンツ
└── knowledge/        # 成熟した知識（メイン領域）
```

## Prerequisites

- **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
- **uv**: Modern Python package manager
  - **Installation**: Follow the [official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)
  - **Quick install**: `curl -LsSf https://astral.sh/uv/install.sh | sh` (Unix/macOS) or `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows)

## 🎯 3分でClaude Code ⇄ Obsidian連携体験

**シームレス統合を体験:**

```bash
# CKCをインストール
uv pip install claude-knowledge-catalyst

# Claude Codeプロジェクトで初期化
cd your-claude-project
uv run ckc init

# Obsidianボルトに接続
uv run ckc add my-vault /path/to/obsidian/vault

# .claude/ファイルをObsidianと同期
uv run ckc sync
```

**何が起こるか:**
- ✅ **シームレス統合**: Claude Code開発とObsidian知識管理の完全連携
- ✅ **自動構造化**: `.claude/`コンテンツをObsidian最適化構造で組織化
- ✅ **AI強化メタデータ**: 手動分類を軽減する自動タグ付け
- ✅ **リアルタイム同期**: 開発プロセスでの知識蓄積を即座に反映

## Core Features

### 🔄 Claude Code ⇄ Obsidian 完全統合
- **シームレス同期**: `.claude/`ディレクトリとObsidianボルトの自動双方向同期
- **構造化移行**: 既存Obsidianボルトの最適化と構造強化
- **動的クエリ生成**: Obsidian dataviewクエリの自動生成
- **知識発見**: Claude Code開発知見のObsidian内横断検索

### 🔒 Secure CLAUDE.md Sync
- **Privacy-First**: Section-level filtering for sensitive information
- **Configurable Exclusion**: Protect API keys, credentials, personal data
- **Safe by Default**: CLAUDE.md sync disabled unless explicitly enabled

### 📊 Obsidian統合アナリティクス
- **知識活用追跡**: Claude Code開発での知識利用パターン分析
- **プロンプト効果測定**: Obsidian内での成功率と改善提案
- **プロジェクト横断洞察**: 開発知見の関連性発見
- **チーム知識共有**: Obsidianを通じた協働知識管理

### 🎨 Obsidian最適化テンプレート
- **Claude Code特化**: プロンプト、コード、概念、リソース用Obsidianテンプレート
- **AI強化提案**: 開発コンテキストに基づく自動テンプレート選択
- **進化する構造**: プロジェクトの成長に応じたObsidianボルト最適化

## Quick Start

### Installation

```bash
# Install from PyPI using uv (recommended)
uv pip install claude-knowledge-catalyst

# Or using pip
pip install claude-knowledge-catalyst

# Or install from source for development
git clone https://github.com/drillan/claude-knowledge-catalyst.git
cd claude-knowledge-catalyst
uv sync --dev
```

### Claude Code プロジェクト統合

```bash
# Claude Codeプロジェクトに移動
cd your-claude-project

# CKCを初期化（.claude/ディレクトリを検出）
uv run ckc init

# Obsidianボルトに接続
uv run ckc add main-vault /path/to/your/obsidian/vault

# .claude/コンテンツの自動分析を体験
echo "# Git便利コマンド集

## ブランチ状態確認
\`\`\`bash
git branch -vv
git status --porcelain
\`\`\`" > .claude/git_tips.md

# AI分析とObsidian用メタデータ生成を確認
uv run ckc classify .claude/git_tips.md --show-evidence
```

### 既存Obsidianボルト強化

```bash
# 既存ObsidianボルトをClaude Code統合用に強化
uv run ckc migrate --source /existing/obsidian --target /enhanced/vault

# 変更内容をプレビュー
uv run ckc migrate --source /existing/obsidian --target /enhanced/vault --dry-run
```

## Available CLI Commands

### 🚀 AI-Powered Classification

```bash
# Automatic content analysis
uv run ckc classify file.md --show-evidence

# Batch classification
uv run ckc batch-classify .claude/

# Missing metadata detection
uv run ckc scan-missing-metadata
```

### 📁 Core Operations

```bash
# Zero-config initialization
uv run ckc init

# Vault connection
uv run ckc add vault-name /path/to/obsidian

# State-based synchronization
uv run ckc sync
uv run ckc sync --project "My Project"

# Real-time monitoring
uv run ckc watch

# System status
uv run ckc status
```

### 📊 Advanced Analytics

```bash
# File analysis with evidence
uv run ckc analyze .claude/my-prompt.md

# Cross-dimensional search
uv run ckc search --tech python --status production
uv run ckc search --team frontend --complexity advanced

# Project insights
uv run ckc project stats my-project
```

## Configuration

CKC uses a YAML configuration file with pure tag-centered settings:

```yaml
version: "1.0"
project_name: "My AI Project"
auto_sync: true

# Tag-centered architecture
tag_system:
  enabled: true
  multi_dimensional: true
  ai_classification: true
  confidence_threshold: 0.75

# 7-dimensional tag schema
tags:
  type_tags: ["prompt", "code", "concept", "resource"]
  tech_tags: ["python", "javascript", "react", "fastapi"]
  domain_tags: ["web-dev", "machine-learning", "devops"]
  team_tags: ["backend", "frontend", "ml-research"]
  status_tags: ["draft", "tested", "production", "deprecated"]
  complexity_tags: ["beginner", "intermediate", "advanced"]
  confidence_tags: ["low", "medium", "high"]

# Obsidian integration
sync_targets:
  - name: "main-vault"
    type: "obsidian"
    path: "/Users/me/Documents/ObsidianVault"
    enabled: true
    enhance_metadata: true

# AI-powered features
ai:
  auto_classification: true
  evidence_tracking: true
  natural_language_search: true

# State-based workflow
workflow:
  inbox_pattern: "status:draft"
  active_pattern: "status:tested"
  knowledge_pattern: "status:production"
  archive_pattern: "status:deprecated"

# Security settings
watch:
  include_claude_md: false  # Enable with caution
  claude_md_sections_exclude:
    - "# secrets"
    - "# private"
    - "# api-keys"
```

## Architecture

CKC implements a revolutionary pure tag-centered architecture:

- **Cognitive Load Zero**: Eliminates category decision fatigue
- **7-Dimensional Classification**: Multi-layer tag system for precise organization
- **AI-Powered Intelligence**: 75%+ accuracy content understanding
- **State-Based Workflow**: Organization by lifecycle, not content type
- **Dynamic Discovery**: Cross-dimensional knowledge search
- **Obsidian Enhancement**: Transform basic vaults → intelligent systems

## Pure Tag-Centered vs Traditional

### ❌ Traditional Category-Based Problems
```
├── prompts/          # "Is this a prompt or template?"
├── code/             # "Code snippet or tool?"
├── concepts/         # "Concept or best practice?"
└── misc/             # Catch-all confusion
```

**Issues:**
- Decision fatigue: Which category?
- Rigid boundaries: Content doesn't fit neatly
- Poor discoverability: Single-dimension search
- Maintenance overhead: Moving files between categories

### ✅ Pure Tag-Centered Solution
```
├── _system/          # System files and templates
├── inbox/            # Unprocessed items (workflow state)
├── active/           # Currently working (activity state)
├── archive/          # Deprecated/old (lifecycle state)
└── knowledge/        # Mature content (90% of files)
    └── Dynamic discovery through enhanced multi-layer tags
```

**Benefits:**
- 🧠 **Cognitive Load Reduction**: No "which category?" decisions
- 🔍 **Multi-Dimensional Discovery**: Search across tech, domain, team
- 📈 **Scalable Organization**: Tags evolve with your knowledge
- ⚡ **Flexible Workflow**: State-based, not content-based organization
- 🔗 **Rich Relationships**: Multi-project, multi-domain connections

## Documentation

- **[📖 Documentation](https://claude-knowledge-catalyst.readthedocs.io/)** - Complete user guide and developer reference
- **[🚀 Quick Start](https://claude-knowledge-catalyst.readthedocs.io/en/latest/quick-start/)** - 5-minute Pure Tag-Centered experience
- **[👥 User Guide](https://claude-knowledge-catalyst.readthedocs.io/en/latest/user-guide/)** - Practical usage methods
- **[🔧 Developer Guide](https://claude-knowledge-catalyst.readthedocs.io/en/latest/developer-guide/)** - Developer reference

## Try the Revolution

**Demo the cognitive transformation:**

```bash
# Experience tag-centered migration
./demo/tag_centered_demo.sh

# Try zero-config classification  
./demo/demo.sh

# Multi-team collaboration
./demo/multi_project_demo.sh
```

## Requirements

- **Python**: 3.11 or higher
- **Memory**: Minimum 512MB, Recommended 2GB for large vaults
- **Storage**: 10MB for CKC, varies based on vault size
- **OS**: Windows 10+, macOS 11+, Linux (Ubuntu 20.04+)

## Support & Community

- **Issues**: [GitHub Issues](https://github.com/drillan/claude-knowledge-catalyst/issues)
- **Discussions**: [GitHub Discussions](https://github.com/drillan/claude-knowledge-catalyst/discussions)
- **Documentation**: [Read the Docs](https://claude-knowledge-catalyst.readthedocs.io/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please see our [Contributing Guide](https://claude-knowledge-catalyst.readthedocs.io/en/latest/developer-guide/) for details.

---

**Welcome to the cognitive revolution!**  
*No more "which category?" decisions - experience pure, discoverable knowledge management.*

*Built with ❤️ by the Claude community*