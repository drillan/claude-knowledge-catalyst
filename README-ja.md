# Claude Knowledge Catalyst (CKC) v0.9.1

**知識の触媒作用を実現する統合的な知識管理システム**

Claude Code との開発プロセスで生まれる知見を自動的に構造化し、Obsidian との深層統合により長期的な知識資産として蓄積・活用するための包括的なプラットフォームです。

> **[📋 English](README.md)** | **[🌐 ドキュメント](https://claude-knowledge-catalyst.readthedocs.io/)**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/claude-knowledge-catalyst.svg)](https://pypi.org/project/claude-knowledge-catalyst/)
[![PyPI downloads](https://img.shields.io/pypi/dm/claude-knowledge-catalyst.svg)](https://pypi.org/project/claude-knowledge-catalyst/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Documentation](https://img.shields.io/badge/docs-readthedocs-brightgreen.svg)](https://claude-knowledge-catalyst.readthedocs.io/)
[![Read the Docs](https://readthedocs.org/projects/claude-knowledge-catalyst/badge/?version=latest)](https://claude-knowledge-catalyst.readthedocs.io/en/latest/)

## 前提条件

Claude Knowledge Catalystを使い始める前に、以下をインストールしてください：

- **Python 3.11+**: [Python をダウンロード](https://www.python.org/downloads/)
- **uv**: モダンなPythonパッケージマネージャー・プロジェクトマネージャー
  - **インストール**: [公式uv インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)に従ってください
  - **クイックインストール**: `curl -LsSf https://astral.sh/uv/install.sh | sh` (Unix/macOS) または `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows)

## コア機能

### 🔄 自動同期システム
- `.claude/` ディレクトリの変更をリアルタイム監視・同期
- .claude ディレクトリと Obsidian ボルトのシームレス連携

### 🔒 セキュアなCLAUDE.md同期
- セクションレベルフィルタリングによるCLAUDE.mdファイルの安全な同期
- 機密情報保護を重視したプライバシーファースト設計
- API キー、認証情報、個人データの設定可能な除外パターン

### 🏷️ インテリジェントメタデータ管理
- 自動プロジェクト検出、タグ推論、文脈解析
- 開発コンテキストのメタデータ強化生成

### 📝 テンプレートシステム
- プロンプト、コード、概念、ログの知識タイプ別テンプレート
- 構造化されたコンテンツ組織

### 🔍 適応型システム基盤
- 知識成熟度の視覚化のための10ステップ番号システム
- 段階的構造化: カオス(00) → プロジェクト(10) → 知識ベース(20) → 知恵資産(30)
- 成功率、実行履歴、コンテンツ解析に基づくインテリジェント分類

### 🎯 Obsidian深層統合
- 双方向リンクとグラフビュー活用による構造化ボルト
- PARA methodに基づく知識組織
- プロジェクト横断での知識発見と相互参照

### ⚡ 包括的CLI
- 初期化、同期、監視、分析のための統合コマンドライン
- プログレスインジケーター付きのリッチコンソール出力

### 📊 プロジェクト分析
- ファイル統計、カテゴリ分布、ステータス管理
- プロジェクト横断での知識リンクと発見

## 🎯 3分でCKCを試す

**CKCのクイックスタート:**

```bash
# 仮想環境を作成・有効化
uv venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# CKCをインストール
uv pip install claude-knowledge-catalyst

# プロジェクトで初期化
cd your-project
uv run ckc init

# Obsidianボルトを追加
uv run ckc add my-vault /path/to/obsidian/vault

# 同期を開始
uv run ckc sync
```

**実行内容：**
- ✅ 知識管理構造のセットアップ
- ✅ Obsidianボルトとの接続
- ✅ 自動コンテンツ同期の開始
- ✅ インテリジェントメタデータ抽出の有効化

## クイックスタート

### 仮想環境のセットアップ

```bash
# 仮想環境を作成
uv venv

# 仮想環境を有効化
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

### インストール

```bash
# PyPIからuv pip を使用してインストール（推奨）
uv pip install claude-knowledge-catalyst

# またはuv addを使用（Pythonプロジェクトの場合）
uv add claude-knowledge-catalyst

# またはpipを使用
pip install claude-knowledge-catalyst

# または開発用にソースからインストール
git clone https://github.com/drillan/claude-knowledge-catalyst.git
cd claude-knowledge-catalyst
uv sync --dev
```

### プロジェクトでの初期化

```bash
# プロジェクトディレクトリに移動
cd your-project

# ハイブリッド構造でCKCを初期化
uv run ckc init

# Obsidianボルトを同期ターゲットとして追加
uv run ckc add my-vault /path/to/your/obsidian/vault

# 変更の監視を開始
uv run ckc watch
```

### CLAUDE.md同期の有効化（オプション）

```bash
# 設定ファイルを編集
vim ckc_config.yaml
```

設定に以下を追加:
```yaml
watch:
  include_claude_md: true
  claude_md_sections_exclude:
    - "# secrets"
    - "# private"
    - "# confidential"
```

> **🔒 セキュリティ注意**: CLAUDE.md同期はデフォルトで無効化されています。機密情報に対して適切なセクション除外を設定した後でのみ有効化してください。

### 以前のバージョンからのアップグレード

```bash
# v0.9.1（最新版）にuv pipを使用してアップデート（推奨）
uv pip install --upgrade claude-knowledge-catalyst

# またはuv addを使用（Pythonプロジェクトの場合）
uv add claude-knowledge-catalyst@latest

# またはpipを使用
pip install --upgrade claude-knowledge-catalyst

# 正常に動作することを確認
uv run ckc status
```

### Sync Existing Knowledge

```bash
# Sync all files in .claude directory
uv run ckc sync

# Sync to specific target
uv run ckc sync --target my-vault

# Sync with project context
uv run ckc sync --project "My Project Name"
```

> **📚 詳細ガイド**: より詳しいセットアップと使用方法については、[公式ドキュメント](https://claude-knowledge-catalyst.readthedocs.io/)の[Quick Start](https://claude-knowledge-catalyst.readthedocs.io/en/latest/quick-start/)と[Getting Started](https://claude-knowledge-catalyst.readthedocs.io/en/latest/getting-started/)をご覧ください。

## 利用可能なCLIコマンド

### 📁 基本操作

```bash
# ワークスペース初期化
uv run ckc init

# 同期ターゲット追加
uv run ckc add main-vault ~/Documents/ObsidianVault

# ファイル同期実行
uv run ckc sync
uv run ckc sync --target main-vault
uv run ckc sync --project "My Project"

# リアルタイム監視
uv run ckc watch

# 現在状況確認
uv run ckc status
```

### 📊 分析・プロジェクト管理

```bash
# ファイル詳細分析
uv run ckc analyze .claude/prompt-optimization.md

# プロジェクト一覧表示
uv run ckc project list

# プロジェクト内ファイル一覧
uv run ckc project files claude-knowledge-catalyst

# プロジェクト統計
uv run ckc project stats claude-knowledge-catalyst
```

## Configuration

CKC uses a YAML configuration file (`ckc_config.yaml`) that supports:

- **Multiple sync targets**: Connect to various knowledge management tools
- **Custom tagging schemas**: Define your own categorization system  
- **Flexible watch patterns**: Configure which files and directories to monitor
- **Template customization**: Modify or add new content templates

Example configuration:

```yaml
version: "1.0"
project_name: "My AI Project"
auto_sync: true

sync_targets:
  - name: "main-vault"
    type: "obsidian" 
    path: "/Users/me/Documents/ObsidianVault"
    enabled: true

tags:
  category_tags: ["prompt", "code", "concept", "resource"]
  tech_tags: ["python", "javascript", "react"]
  claude_tags: ["opus", "sonnet", "haiku"]
  status_tags: ["draft", "tested", "production"]

watch:
  watch_paths: [".claude"]
  file_patterns: ["*.md", "*.txt"]
  debounce_seconds: 1.0
```

## 知識組織化システム

CKC v0.9.0 は **適応型システム基盤** により、知識の自然進化をサポートします：

```
Obsidian_Vault/
├── 00_Catalyst_Lab/             # 🧪 実験・アイデア孵化の場
│   ├── brainstorming/           # 未加工アイデア
│   ├── experiments/             # 実験的取り組み
│   └── rapid_prototypes/        # 迅速プロトタイピング
│
├── 10_Projects/                 # 🚀 アクティブプロジェクト管理
│   ├── active/                  # 進行中プロジェクト
│   ├── planning/                # 計画段階
│   └── review/                  # レビュー・評価段階
│
├── 20_Knowledge_Base/           # 📚 体系化された知見
│   ├── Prompts/                 # プロンプト関連
│   │   ├── Templates/           # 汎用プロンプトテンプレート
│   │   ├── Best_Practices/      # 成功事例・ベストプラクティス
│   │   └── Improvement_Log/     # プロンプト改善の記録
│   ├── Code_Snippets/           # 再利用可能なコードスニペット
│   │   ├── Python/              # Python関連
│   │   ├── JavaScript/          # JavaScript関連
│   │   ├── Bash/                # Bash/Shell関連
│   │   └── Other_Languages/     # その他言語
│   ├── Concepts/                # AI・LLM関連の概念整理
│   │   ├── API_Design/          # API設計原則
│   │   ├── Software_Architecture/ # ソフトウェア設計
│   │   └── Development_Practices/ # 開発手法
│   └── Resources/               # 学習リソースと外部参考資料
│
├── 30_Wisdom_Archive/           # 💎 高品質な知識資産
│   ├── Best_Practices/          # ベストプラクティス集
│   ├── Lessons_Learned/         # 教訓と反省
│   └── Strategic_Insights/      # 戦略的知見
│
├── _templates/                  # 🏗️ システムテンプレート
├── Analytics/                   # 📊 知見の活用状況分析
└── Archive/                     # 📦 古い・非推奨の知見
```

### 知識進化プロセス

```
Raw Ideas → Structured Insights → Validated Knowledge → Wisdom Assets
   (00)         (10-20)              (20-30)            (30+)

🧪 実験段階 → 🚀 プロジェクト → 📚 知識ベース → 💎 知恵資産
```

## Advanced Features

### Metadata Enhancement

Every knowledge item is automatically enhanced with rich metadata:

```yaml
---
title: "Python Async Code Generation"
created: "2024-06-17T10:30:00"
updated: "2024-06-17T15:45:00"
version: "1.2"
claude_model: "Claude 3 Opus"
category: "prompt"
status: "production"
success_rate: 87
confidence: "high"
purpose: "Generate async Python code with proper error handling"
tags: [prompt, python, async, code-generation]
related_projects: ["web-scraper", "api-service"]
---
```

### Template System

Built-in templates for common knowledge types:

- **Prompt Templates**: Structure for prompt development and iteration
- **Code Snippets**: Reusable code with documentation
- **Concept Notes**: AI/LLM concepts and explanations
- **Project Logs**: Development session recordings
- **Improvement Logs**: Tracking prompt and process improvements

### Success Tracking

Track the effectiveness of your prompts and techniques:

- Success rate monitoring
- Version comparison
- Improvement trends
- Best practice identification

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/drillan/claude-knowledge-catalyst.git
cd claude-knowledge-catalyst

# Install development dependencies with uv
uv sync --dev

# Install pre-commit hooks
uv run pre-commit install

# Run tests
uv run pytest

# Run linting and formatting
uv run ruff check src/ tests/     # Lint
uv run ruff format src/ tests/    # Format
uv run mypy src/                  # Type checking
```

### プロジェクト構造

```
src/claude_knowledge_catalyst/
├── core/                          # コア機能
│   ├── config.py                  # 設定管理（CKCConfig, SyncTarget）
│   ├── metadata.py                # メタデータ抽出・管理（KnowledgeMetadata）
│   ├── watcher.py                 # ファイルシステム監視
│   ├── hybrid_config.py           # ハイブリッド構造設定
│   └── structure_validator.py     # 構造整合性検証
├── sync/                          # 同期システム
│   ├── obsidian.py                # Obsidian統合（ObsidianVaultManager）
│   ├── hybrid_manager.py          # ハイブリッド同期管理
│   └── compatibility.py           # 後方互換性
├── templates/                     # テンプレートシステム
│   ├── manager.py                 # テンプレート管理（TemplateManager）
│   └── hybrid_templates.py        # ハイブリッド専用テンプレート
├── ai/                           # AI支援機能
│   └── ai_assistant.py           # AI分析・提案システム
├── analytics/                    # アナリティクス
│   ├── knowledge_analytics.py    # 知識分析エンジン
│   └── usage_statistics.py      # 使用統計
├── automation/                   # 自動化
│   ├── metadata_enhancer.py     # メタデータ自動強化
│   └── structure_automation.py  # 構造自動最適化
└── cli/                          # CLI インターフェース
    ├── main.py                   # メインCLI
    ├── migrate_commands.py       # 移行コマンド
    └── structure_commands.py     # 構造管理コマンド
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 [Documentation](https://claude-knowledge-catalyst.readthedocs.io/)
- 🐛 [Issue Tracker](https://github.com/drillan/claude-knowledge-catalyst/issues)
- 💬 [Discussions](https://github.com/drillan/claude-knowledge-catalyst/discussions)

## 今後の展開

CKC の将来計画と実装予定機能については、詳細な[開発ロードマップ](.claude/architecture/roadmap.md)をご参照ください。

### 次期リリース予定
- **v1.0.0**: 初回パブリックリリース（機能安定化、ドキュメント完備）
- **v1.1.0**: AI支援機能拡張（コンテンツ改善提案、高度アナリティクス）
- **v1.2.0**: 構造管理機能（自動最適化、詳細検証）
- **v2.0.0**: エンタープライズ機能（Web インターフェース、チーム協働）

---

**Claude Knowledge Catalyst** - AI開発プロセスで得られる知見を組織化・検索可能・再利用可能な知識資産に変換し、継続的な学習とイノベーションを加速する統合プラットフォーム。

> 🎯 **ビジョン**: 開発者の経験と洞察を蓄積し、知識の触媒作用により新しい発見と効率的な問題解決を実現する。
