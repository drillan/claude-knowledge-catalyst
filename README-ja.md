# Claude Knowledge Catalyst (CKC) v0.10.1

**Claude Code ⇄ Obsidian シームレス統合システム**

Claude Code開発プロセスで生まれる知見を自動的にObsidianボルトと同期し、構造化された知識管理を実現。自動分析により、手動分類の負荷を軽減します。

> **[📋 English](README.md)** | **[🌐 ドキュメント](https://claude-knowledge-catalyst.readthedocs.io/)**

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

### 🤖 YAKE統合による自動メタデータ強化
- **高度キーワード抽出**: YAKE（Yet Another Keyword Extractor）による教師なしキーワード発見
- **多言語対応**: 日本語、英語、スペイン語、フランス語、ドイツ語、イタリア語、ポルトガル語
- **スマートタグ付け**: 信頼度スコアリング付きAIタグ提案
- **証拠ベース分類**: 自動判定の根拠を明示した信頼性の高い組織化

```yaml
# 強化メタデータ例（副次的効果）
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

## 前提条件

- **uv**: モダンなPythonパッケージマネージャー（Python 3.11+を自動管理）
  - **インストール**: [公式uv インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)に従ってください
  - **クイックインストール**: `curl -LsSf https://astral.sh/uv/install.sh | sh` (Unix/macOS) または `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows)
- **Python**: 個別インストール不要 - uvがPython 3.11+を自動管理

## 🎯 3分でClaude Code ⇄ Obsidian連携体験

> **🚀 v0.10.1 テスト安定化**: 396/396テスト通過率100%、48.09%カバレッジによる本格運用品質を実現。

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
- ✅ **強化メタデータ**: 手動分類を軽減する自動タグ付け
- ✅ **リアルタイム同期**: 開発プロセスでの知識蓄積を即座に反映

## コア機能

### 🔄 インテリジェントObsidian強化
- **基本 → 高度**: 単純なObsidianメタデータ → 豊富な多次元システムへ変換
- **AI移行**: 既存ボルトの自動強化
- **動的クエリ**: 洗練されたObsidian dataviewクエリ生成
- **クロス次元発見**: 複数タグ次元を横断した知識発見

### 🔒 セキュアなCLAUDE.md同期
- **プライバシーファースト**: 機密情報のセクションレベルフィルタリング
- **設定可能除外**: APIキー、認証情報、個人データの保護
- **デフォルトセーフ**: 明示的に有効化しない限りCLAUDE.md同期は無効

### 📊 高度アナリティクス
- **成功率追跡**: プロンプト効果性の監視
- **使用パターン**: 知識活用の理解
- **プロジェクト横断洞察**: 知識接続の発見
- **チーム協働**: 所有権と共有の追跡

### 🎨 動的テンプレートシステム
- **タイプ特化**: プロンプト、コード、概念、リソース用テンプレート
- **スマート提案**: インテリジェントテンプレート提案
- **進化する構造**: あなたの知識パターンに適応するテンプレート

## クイックスタート

### インストール

```bash
# uvを使用してPyPIからインストール（推奨）
uv pip install claude-knowledge-catalyst

# またはpipを使用
pip install claude-knowledge-catalyst

# または開発用にソースからインストール
git clone https://github.com/drillan/claude-knowledge-catalyst.git
cd claude-knowledge-catalyst
uv sync --dev
```

### ゼロ設定体験

```bash
# プロジェクトに移動
cd your-project

# ゼロ設定で初期化
uv run ckc init

# Obsidianボルトを追加
uv run ckc add main-vault /path/to/your/obsidian/vault

# AI分類を体験
echo "# Git便利コマンド集

## ブランチ状態確認
\`\`\`bash
git branch -vv
git status --porcelain
\`\`\`" > .claude/git_tips.md

# 自動推論を確認: type=code, tech=git, domain=development
uv run ckc classify .claude/git_tips.md --show-evidence
```

### Obsidian移行

```bash
# 既存Obsidianボルトを移行
uv run ckc migrate --source /existing/obsidian --target /enhanced/vault

# 変更なしで強化をプレビュー
uv run ckc migrate --source /existing/obsidian --target /enhanced/vault --dry-run
```

## 利用可能なCLIコマンド

### 🚀 自動分類

```bash
# 自動コンテンツ分析
uv run ckc classify file.md --show-evidence

# バッチ分類
uv run ckc batch-classify .claude/

# 欠損メタデータ検出
uv run ckc scan-missing-metadata
```

### 📁 コア操作

```bash
# ゼロ設定初期化
uv run ckc init

# ボルト接続
uv run ckc add vault-name /path/to/obsidian

# 状態ベース同期
uv run ckc sync
uv run ckc sync --project "My Project"

# リアルタイム監視
uv run ckc watch

# システム状態
uv run ckc status
```

### 📊 高度アナリティクス

```bash
# 証拠付きファイル分析
uv run ckc analyze .claude/my-prompt.md

# クロス次元検索
uv run ckc search --tech python --status production
uv run ckc search --team frontend --complexity advanced

# プロジェクト洞察
uv run ckc project stats my-project
```

## 設定

CKCは純粋タグ中心設定のYAML設定ファイルを使用します:

```yaml
version: "1.0"
project_name: "My AI Project"
auto_sync: true

# タグ中心アーキテクチャ
tag_system:
  enabled: true
  multi_dimensional: true
  auto_classification: true
  confidence_threshold: 0.75

# 7次元タグスキーマ
tags:
  type_tags: ["prompt", "code", "concept", "resource"]
  tech_tags: ["python", "javascript", "react", "fastapi"]
  domain_tags: ["web-dev", "machine-learning", "devops"]
  team_tags: ["backend", "frontend", "ml-research"]
  status_tags: ["draft", "tested", "production", "deprecated"]
  complexity_tags: ["beginner", "intermediate", "advanced"]
  confidence_tags: ["low", "medium", "high"]

# Obsidian統合
sync_targets:
  - name: "main-vault"
    type: "obsidian"
    path: "/Users/me/Documents/ObsidianVault"
    enabled: true
    enhance_metadata: true

# 自動化機能
automation:
  auto_classification: true
  evidence_tracking: true
  natural_language_search: true

# 状態ベースワークフロー
workflow:
  inbox_pattern: "status:draft"
  active_pattern: "status:tested"
  knowledge_pattern: "status:production"
  archive_pattern: "status:deprecated"

# セキュリティ設定
watch:
  include_claude_md: false  # 慎重に有効化
  claude_md_sections_exclude:
    - "# secrets"
    - "# private"
    - "# api-keys"
```

## アーキテクチャ

CKCは革命的な純粋タグ中心アーキテクチャを実装:

- **認知負荷ゼロ**: カテゴリ決定疲労の排除
- **7次元分類**: 精密組織化のための多層タグシステム
- **自動インテリジェンス**: パターンマッチングコンテンツ理解
- **状態ベースワークフロー**: コンテンツタイプではなくライフサイクルによる組織化
- **動的発見**: クロス次元知識検索
- **Obsidian強化**: 基本ボルト → インテリジェントシステム変換

## 純粋タグ中心 vs 従来型

### ❌ 従来のカテゴリベースの問題
```
├── prompts/          # 「これはプロンプト？テンプレート？」
├── code/             # 「コードスニペット？ツール？」
├── concepts/         # 「概念？ベストプラクティス？」
└── misc/             # キャッチオール混乱
```

**問題点:**
- 決定疲労: どのカテゴリ？
- 硬直境界: コンテンツがうまく適合しない
- 発見性の欠如: 単次元検索
- メンテナンス負荷: カテゴリ間でのファイル移動

### ✅ 純粋タグ中心ソリューション
```
├── _system/          # システムファイルとテンプレート
├── inbox/            # 未処理アイテム（ワークフロー状態）
├── active/           # 現在作業中（活動状態）
├── archive/          # 非推奨・古い（ライフサイクル状態）
└── knowledge/        # 成熟コンテンツ（90%のファイル）
    └── 強化多層タグによる動的発見
```

**利点:**
- 🧠 **認知負荷削減**: 「どのカテゴリ？」決定なし
- 🔍 **多次元発見**: 技術、ドメイン、チーム横断検索
- 📈 **スケーラブル組織化**: タグが知識と共に進化
- ⚡ **柔軟ワークフロー**: コンテンツベースではなく状態ベース組織化
- 🔗 **豊富な関係性**: マルチプロジェクト、マルチドメイン接続

## ドキュメント

- **[📖 ドキュメント](https://claude-knowledge-catalyst.readthedocs.io/)** - 完全なユーザーガイドと開発者リファレンス
- **[🚀 クイックスタート](https://claude-knowledge-catalyst.readthedocs.io/en/latest/quick-start/)** - 5分純粋タグ中心体験
- **[👥 ユーザーガイド](https://claude-knowledge-catalyst.readthedocs.io/en/latest/user-guide/)** - 実践的な使用方法
- **[🔧 開発者ガイド](https://claude-knowledge-catalyst.readthedocs.io/en/latest/developer-guide/)** - 開発者リファレンス

## 革命を試す

**認知変革をデモ:**

```bash
# タグ中心移行を体験
./demo/tag_centered_demo.sh

# 自動分類を試す
./demo/demo.sh

# マルチチーム協働
./demo/multi_project_demo.sh
```

## 動作環境

- **Pythonランタイム**: 3.11以上（uvが自動管理）
- **パッケージマネージャー**: uv（Pythonインストールと依存関係管理を処理）
- **メモリ**: 最小512MB、大型ボルトには2GB推奨
- **ストレージ**: CKCに10MB、ボルトサイズに依存
- **OS**: Windows 10+、macOS 11+、Linux (Ubuntu 20.04+)

## サポート & コミュニティ

- **課題**: [GitHub Issues](https://github.com/drillan/claude-knowledge-catalyst/issues)
- **ディスカッション**: [GitHub Discussions](https://github.com/drillan/claude-knowledge-catalyst/discussions)
- **ドキュメント**: [Read the Docs](https://claude-knowledge-catalyst.readthedocs.io/)

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 貢献

貢献を歓迎します！詳細は[貢献ガイド](https://claude-knowledge-catalyst.readthedocs.io/en/latest/developer-guide/)を参照してください。

---

**認知革命へようこそ！**  
*もう「どのカテゴリ？」と悩む必要はありません - 純粋で発見可能な知識管理を体験してください。*

*Claude コミュニティが ❤️ を込めて開発*