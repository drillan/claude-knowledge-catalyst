# Quick Start

5分でClaude Code ⇄ Obsidian連携を開始し、シームレス統合の革新的体験を始めましょう。

## 前提条件

- **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
- **uv**: Modern Python package manager
  - **インストール**: [公式uv インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)
  - **クイックインストール**: `curl -LsSf https://astral.sh/uv/install.sh | sh` (Unix/macOS)
- **Claude Codeプロジェクト**: `.claude/`ディレクトリを含むプロジェクト
- **Obsidianボルト**: 接続先のObsidianボルト

## Step 1: CKCインストール

```bash
# CKCをインストール
uv pip install claude-knowledge-catalyst

# インストール確認
uv run ckc --version
```

## Step 2: Claude Codeプロジェクトで初期化

```bash
# Claude Codeプロジェクトに移動
cd your-claude-project

# .claude/ディレクトリの存在を確認
ls -la .claude/

# CKCを初期化（.claude/ディレクトリを自動検出）
uv run ckc init
```

**何が起こるか:**
- プロジェクトディレクトリに`ckc_config.yaml`が作成されます
- `.claude/`ディレクトリがCKC管理対象として認識されます
- Obsidian統合のための基本設定が準備されます

## Step 3: Obsidianボルトに接続

```bash
# Obsidianボルトを追加
uv run ckc add main-vault /path/to/your/obsidian/vault

# 設定確認
uv run ckc status
```

**設定例:**
```yaml
# ckc_config.yaml（自動生成）
version: "1.0"
project_name: "your-claude-project"
auto_sync: true

sync_targets:
  - name: "main-vault"
    type: "obsidian"
    path: "/path/to/your/obsidian/vault"
    enabled: true
```

## Step 4: シームレス同期の体験

### 自動同期開始

```bash
# リアルタイム同期を開始
uv run ckc watch
```

### サンプルコンテンツで体験

````bash
# .claude/にサンプルファイルを作成
echo "# Git便利コマンド集

## ブランチ状態確認
```bash
git branch -vv
git status --porcelain
```

## リモート同期
```bash
git fetch --all
git pull origin main
```" > .claude/git_tips.md

# AI分析とObsidian用メタデータ生成を確認
uv run ckc classify .claude/git_tips.md --show-evidence
````

**AI分析結果例:**
```
AI分析結果:
├── type: code (信頼度: 91%)
│   └── 根拠: "```bash", "git", "コマンド集"
├── tech: [git, bash] (信頼度: 95%)
│   └── 根拠: "git branch", "git status", "bash"
├── domain: [development, version-control] (信頼度: 88%)
│   └── 根拠: バージョン管理、開発ツール
└── complexity: beginner (信頼度: 82%)
    └── 根拠: 基本的なgitコマンド
```

### Obsidianでの確認

```bash
# 同期実行
uv run ckc sync

# Obsidianボルトを確認
ls -la /path/to/your/obsidian/vault/knowledge/code/
```

**Obsidianで生成されるファイル例:**
```markdown
---
title: "Git便利コマンド集"
type: code
tech: [git, bash]
domain: [development, version-control]
complexity: beginner
confidence: high
claude_project: "your-claude-project"
source_path: ".claude/git_tips.md"
created: 2025-06-20
updated: 2025-06-20
---

# Git便利コマンド集

## ブランチ状態確認
```bash
git branch -vv
git status --porcelain
```

## リモート同期
```bash
git fetch --all
git pull origin main
```

## 関連知識
- [[Git Workflow]]
- [[Version Control Best Practices]]
```

## Step 5: 高度機能の体験

### プロンプト作成と分析

```bash
# プロンプトファイルを作成
echo "---
title: API設計レビュープロンプト  
type: prompt
---

# API設計レビュープロンプト

以下のAPI設計を以下の観点でレビューしてください：

1. **RESTful設計原則**への準拠
2. **セキュリティ**考慮事項
3. **パフォーマンス**最適化
4. **ドキュメント**の充実度

## API仕様
{API仕様をここに記載}

## 期待する出力
- 改善提案の優先順位付きリスト
- 具体的な修正例
- セキュリティリスクの指摘" > .claude/api_review_prompt.md

# AI分析実行
uv run ckc classify .claude/api_review_prompt.md --show-evidence
```

### 既存Obsidianボルト強化

```bash
# 既存ボルトをClaude Code統合用に強化
uv run ckc migrate --source /existing/obsidian --target /enhanced/vault --dry-run

# 実際の移行実行
uv run ckc migrate --source /existing/obsidian --target /enhanced/vault
```

## 基本的なワークフロー

### 日常の開発フロー

```bash
# 1. プロジェクト開始
cd new-claude-project
uv run ckc init
uv run ckc add main-vault ~/ObsidianVault

# 2. 開発中の自動同期
uv run ckc watch &

# 3. Claude Code開発（.claude/に知見を蓄積）
# ... 開発作業 ...

# 4. 知識の検索・活用
uv run ckc search --tech python --success-rate ">80"
uv run ckc analyze .claude/my-prompt.md
```

### プロジェクト完了時

```bash
# プロジェクト総括
uv run ckc project stats current-project

# 知識の成熟化
uv run ckc sync --finalize
```

## 設定のカスタマイズ

### 基本設定

```yaml
# ckc_config.yaml
version: "1.0"
project_name: "Claude API Project"
auto_sync: true

# AI分析設定
ai:
  auto_classification: true
  confidence_threshold: 0.75
  evidence_tracking: true

# Obsidian最適化
obsidian:
  structure_type: "state_based"
  auto_queries: true
  template_generation: true
```

### セキュリティ設定

```yaml
# CLAUDE.md同期（オプション）
watch:
  include_claude_md: false  # デフォルトは無効
  claude_md_sections_exclude:
    - "# secrets"
    - "# private"
    - "# api-keys"
```

## Obsidianでの知識活用

### 自動生成クエリの活用

Obsidianボルトに自動生成される検索クエリ：

````markdown
# 高成功率プロンプト
```dataview
TABLE success_rate, tech, updated
FROM #prompt 
WHERE success_rate > 80
SORT success_rate DESC
```

# プロジェクト別コード
```dataview
LIST FROM [[Current Project]]
WHERE type = "code" AND status = "production"
```
````

### タグベース検索

````markdown
# 技術別知識
#tech/python AND #status/production

# チーム別知識  
#team/backend AND #complexity/intermediate

# ドメイン横断
#domain/api-design AND #confidence/high
```

## トラブルシューティング

### よくある問題

1. **同期されない**
   ```bash
   # 設定確認
   uv run ckc status
   
   # 手動同期
   uv run ckc sync --force
   ```

2. **AI分析が不正確**
   ```bash
   # 信頼度閾値調整
   uv run ckc config set ai.confidence_threshold 0.8
   ```

3. **Obsidianパスエラー**
   ```bash
   # パス確認
   uv run ckc config get sync_targets
   
   # パス更新
   uv run ckc config set sync_targets.0.path "/correct/path"
   ```

## 次のステップ

✅ **基本統合完了！** 以下で詳細を学習：

- **[Core Concepts](../user-guide/core-concepts.md)** - 統合アーキテクチャの詳細
- **[Obsidian Migration](../user-guide/obsidian-migration.md)** - 既存ボルトの強化方法
- **[Tag Architecture](../user-guide/tag-architecture.md)** - 多次元タグシステム
- **[Claude.md Sync](../user-guide/claude-md-sync.md)** - セキュアな同期設定

## Demo Scripts

統合機能を実際に体験：

```bash
# Obsidian移行デモ
./demo/tag_centered_demo.sh

# ゼロ設定分類デモ
./demo/demo.sh

# マルチチーム協働デモ
./demo/multi_project_demo.sh
```

---

**🎉 おめでとうございます！**  
Claude Code ⇄ Obsidian統合が完了しました。開発プロセスで生まれる知見が自動的にObsidianで構造化され、長期的な知識資産として活用できます。