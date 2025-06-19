# Getting Started

Claude Knowledge Catalystの詳細なセットアップガイドです。プロンプトエンジニアリングの基礎から実際の運用まで、段階的に学習できます。

## What is Claude Knowledge Catalyst?

Claude Knowledge Catalyst (CKC) は、Claude Codeとの開発プロセスで生まれる知見を自動的に構造化し、Obsidianとの深層統合により長期的な知識資産として蓄積・活用するための包括的なプラットフォームです。

### 主要な特徴

- **🔄 自動同期システム**: `.claude/` ディレクトリの変更をリアルタイム監視・同期
- **🏷️ インテリジェントメタデータ**: プロジェクト検出、タグ推論、文脈解析による自動抽出
- **📝 テンプレートシステム**: プロンプト、コード、概念、ログの知識タイプ別テンプレート
- **🔍 適応型組織化**: 10-step numbering による知識成熟度管理
- **🎯 Obsidian深層統合**: 構造化ボルト、双方向リンク、グラフビュー活用

## インストールと初期設定

### 1. 環境準備

```bash
# Python 3.11以上が必要
python --version

# uvパッケージマネージャーのインストール
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. プロジェクトセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/drillan/claude-knowledge-catalyst.git
cd claude-knowledge-catalyst

# 依存関係をインストール
uv sync --dev

# 初期化
uv run ckc init
```

### 3. 設定ファイルのカスタマイズ

生成された `.ckc/config.yaml` を編集して、あなたの環境に合わせて設定します：

```yaml
# Obsidianボルトのパス
obsidian_vault_path: "~/Documents/MyVault"

# 同期の詳細設定
sync:
  auto_sync: true
  watch_directories: [".claude"]
  
# メタデータ設定
metadata:
  auto_extract: true
  tag_inference: true
```

## 基本的なワークフロー

### ステップ1: プロジェクト初期化

新しいプロジェクトでCKCを使用する場合：

```bash
cd your-new-project
uv run ckc init
```

### ステップ2: Claude Codeでの開発

通常通りClaude Codeで開発を進めます。`.claude/` ディレクトリに作成されるファイルが自動的に監視されます。

### ステップ3: 自動同期の確認

```bash
# 同期状況を確認
uv run ckc status

# 手動同期（必要に応じて）
uv run ckc sync
```

## Next Steps

- [Core Concepts](../user-guide/core-concepts.md) - CKCの中核概念を理解
- [Tutorials](../user-guide/tutorials/index.md) - 実践的なチュートリアル
- **Best Practices** - 効果的な使用方法（準備中）