# Quick Start

Claude Knowledge Catalystを5分で始めるためのガイドです。

## 前提条件

Claude Knowledge Catalystを使い始める前に、以下をインストールしてください：

- **Python 3.11+**: [Pythonをダウンロード](https://www.python.org/downloads/)
- **uv**: モダンなPythonパッケージマネージャー・プロジェクトマネージャー
  - **インストール**: [公式uvインストールガイド](https://docs.astral.sh/uv/getting-started/installation/)に従ってください
  - **クイックインストール**: `curl -LsSf https://astral.sh/uv/install.sh | sh` (Unix/macOS) または `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows)

## インストール

### 仮想環境のセットアップ

```bash
# 仮想環境を作成
uv venv

# 仮想環境を有効化
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

### CKCのインストール

```bash
# PyPIからuv pipを使用してインストール（推奨）
uv pip install claude-knowledge-catalyst

# またはuv addを使用（Pythonプロジェクトの場合）
uv add claude-knowledge-catalyst

# またはpipを使用
pip install claude-knowledge-catalyst

# または開発版をソースからインストール
git clone https://github.com/drillan/claude-knowledge-catalyst.git
cd claude-knowledge-catalyst
uv venv
source .venv/bin/activate  # Linux/macOS
uv sync --dev
```

## 基本的な使用方法

```bash
# CKCを初期化
uv run ckc init

# 設定ファイルを確認
cat ckc_config.yaml

# 同期を開始
uv run ckc sync
```

## CLAUDE.md同期の設定（オプション）

CLAUDE.mdファイルもObsidianに同期したい場合：

```bash
# 設定ファイルを編集
vim ckc_config.yaml
```

設定例：
```yaml
watch:
  include_claude_md: true
  claude_md_sections_exclude:
    - "# secrets"
    - "# private"
```

:::{warning}
**セキュリティ注意**: CLAUDE.mdには機密情報が含まれる場合があります。同期を有効にする前に、除外設定を適切に行ってください。
:::

## 期待される結果

初期化後、以下のような構造が作成されます：

```
your-project/
├── .ckc/
│   ├── config.yaml
│   └── templates/
├── .claude/
│   ├── knowledge/
│   └── prompts/
└── obsidian-vault/
    ├── Projects/
    ├── Areas/
    ├── Resources/
    └── Archive/
```

:::{note}
詳細な設定については、[Getting Started](../getting-started/index.md)で説明しています。
:::

## Next Steps

- [Getting Started](../getting-started/index.md) - 詳細なセットアップガイド
- [User Guide](../user-guide/index.md) - 実践的な使用方法
- [Tutorials](../user-guide/tutorials/index.md) - ステップバイステップのチュートリアル