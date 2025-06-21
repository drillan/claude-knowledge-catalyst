# CLAUDE.md同期ガイド

Claude Knowledge Catalyst (CKC) では、プロジェクトの `CLAUDE.md` ファイルをObsidian vaultに同期する機能を提供しています。この機能により、Claude Code への指示やプロジェクト固有の設定をナレッジベースとして活用できます。

## 機能概要

CLAUDE.md同期機能では以下のことが可能です：

- **自動同期**: CLAUDE.mdファイルの変更を自動的にObsidianに反映
- **セキュリティ対応**: 機密情報を含むセクションを同期から除外
- **メタデータ強化**: プロジェクト情報と開発コンテキストを自動付与
- **柔軟な設定**: プロジェクトに応じたカスタマイズが可能

## 設定方法

### 基本設定

プロジェクトルートの `ckc_config.yaml` で設定します：

```yaml
watch:
  # CLAUDE.md synchronization settings
  include_claude_md: true  # CLAUDE.md ファイルをObsidianに同期
  claude_md_patterns:
    - "CLAUDE.md"
    - ".claude/CLAUDE.md"
  claude_md_sections_exclude:
    - "# secrets"
    - "# private" 
    - "# confidential"
```

### 設定オプション詳細

| オプション | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| `include_claude_md` | boolean | `false` | CLAUDE.md同期の有効/無効 |
| `claude_md_patterns` | list | `["CLAUDE.md", ".claude/CLAUDE.md"]` | 同期対象ファイルパターン |
| `claude_md_sections_exclude` | list | `[]` | 除外するセクションヘッダー |

## セキュリティとプライバシー

### セクション除外機能

機密情報を含むセクションは同期から自動的に除外できます：

```yaml
watch:
  claude_md_sections_exclude:
    - "# secrets"        # API キーなどの秘密情報
    - "# private"        # 個人的なメモ
    - "# confidential"   # 機密プロジェクト情報
    - "# internal"       # 社内専用情報
    - "# credentials"    # 認証情報
```

### 除外の動作例

以下のCLAUDE.mdファイルがある場合：

```markdown
# Project Overview
このプロジェクトは...

# Architecture
システム構成は...

# secrets
API_KEY=sk-1234567890
DATABASE_URL=postgresql://...

# Commands
pytest を実行して...

# private
個人的なメモ：明日までに...
```

`claude_md_sections_exclude: ["# secrets", "# private"]` の設定では：

**同期される内容**:
```markdown
# Project Overview
このプロジェクトは...

# Architecture  
システム構成は...

# Commands
pytest を実行して...
```

**除外される内容**:
- `# secrets` セクション全体
- `# private` セクション全体

## 使用シナリオ

### 推奨される使用例

```{admonition} ✅ 推奨シナリオ
:class: tip

- **個人開発**: 全ての開発コンテキストを一元管理
- **チーム開発**: Obsidianを共有知識ベースとして活用
- **学習記録**: Claude Code との協働で得た知見を蓄積
- **プロジェクト横断**: 成功パターンやベストプラクティスを共有
```

### 避けるべき使用例

```{admonition} ❌ 避けるべきシナリオ
:class: warning

- **機密プロジェクト**: 秘匿性の高い情報が含まれる場合
- **API キー含有**: 除外設定なしでの認証情報露出
- **規制対象**: コンプライアンス要件がある場合
- **外部共有**: 不特定多数がアクセスできる環境
```

## メタデータの活用

CLAUDE.mdファイルには以下の特別なメタデータが自動付与されます：

### 基本メタデータ
- `file_type: claude_config` - ファイル種別
- `is_claude_md: true` - CLAUDE.mdファイルの識別
- `project_root` - プロジェクトルートパス
- `sections_filtered` - フィルタリング有効フラグ

### コンテンツ解析メタデータ
- `has_project_overview` - プロジェクト概要の有無
- `has_architecture_info` - アーキテクチャ情報の有無
- `has_commands` - コマンド情報の有無
- `has_guidelines` - ガイドライン情報の有無
- `section_count` - セクション数

### Obsidianでの活用例

```markdown
---
file_type: claude_config
is_claude_md: true
project_root: "/path/to/project"
has_project_overview: true
has_commands: true
section_count: 4
tags: [claude-config, project-docs, development]
---

# MyProject - CLAUDE.md

> **Source**: `/path/to/project/CLAUDE.md`
> **Filtered**: 2 sections excluded for security

## Project Overview
...
```

## ベストプラクティス

### 1. セキュリティ重視の設定

```yaml
# セキュリティを重視した設定例
watch:
  include_claude_md: true
  claude_md_sections_exclude:
    - "# secrets"
    - "# private"
    - "# confidential" 
    - "# api-keys"
    - "# credentials"
    - "# internal"
```

### 2. 段階的なプライバシー設定

```markdown
# CLAUDE.md の構造例

# Project Overview
パブリックな情報

# Architecture
一般的な技術情報

# Commands  
開発コマンド

# Best Practices
チーム共有可能な知見

# private
# 個人的なメモや未確定情報

# secrets
# API キーやパスワード
```

### 3. チーム利用の場合

```yaml
# チーム利用時の推奨設定
watch:
  include_claude_md: true
  claude_md_patterns:
    - "CLAUDE.md"           # プロジェクトルート
    - "docs/CLAUDE.md"      # ドキュメントディレクトリ
  claude_md_sections_exclude:
    - "# personal"          # 個人的メモ
    - "# todo"              # 個人タスク
```

## トラブルシューティング

### CLAUDE.mdが同期されない

**確認事項**:
1. `include_claude_md: true` が設定されているか
2. ファイル名が正確に `CLAUDE.md` になっているか
3. ファイルが空でないか
4. 除外設定により全コンテンツが除外されていないか

**解決方法**:
```bash
# Claude統合設定確認
ckc config show --claude-integration

# CLAUDE.md同期状況確認
ckc watch status --claude-md

# 手動Claude統合同期
ckc sync --claude-md --force

# Claude統合診断
ckc diagnose --claude-integration
```

### セクション除外が効かない

**よくある原因**:
- セクションヘッダーの形式が間違っている
- 除外パターンの記述ミス
- 大文字小文字の認識違い（実際は区別しません）

**正しい設定例**:
```yaml
claude_md_sections_exclude:
  - "# secrets"     # ✅ 正しい
  - "# Secrets"     # ✅ 大文字小文字は関係なし
  - "secrets"       # ❌ # マークが必要
  - "## secrets"    # ❌ # は1つだけ
```

### メタデータが正しく設定されない

**確認方法**:
```bash
# Claude統合メタデータ確認
ckc metadata show path/to/CLAUDE.md --claude-analysis

# Claude特化メタデータ再生成
ckc metadata refresh path/to/CLAUDE.md --claude-enhanced

# Claude統合状態診断
ckc analyze claude-integration --project .
```

## Claude Code統合エコシステム

### 🔄 Claude Code開発ワークフロー統合
CLAUDE.md同期は[シームレス統合システム](core-concepts.md#シームレス統合システム)の中核として動作し、開発プロセス全体をObsidianと統合します。

### 🤖 自動強化メタデータシステム
[自動メタデータ強化](core-concepts.md#-自動メタデータ強化)により、Claude開発コンテキストに特化した豊富な情報が自動付与されます。

### 🏛️ Obsidian最適化統合
[Obsidian最適化ボルト構造](core-concepts.md#obsidian最適化ボルト構造)の一部として、ボルト構造とdataviewクエリを最適化します。

### 📊 Claude開発分析
[Claude Code統合設定](core-concepts.md#claude-code統合設定)と連携し、CLAUDE.md利用パターンから開発効率を測定・改善します。

## まとめ

CLAUDE.md同期機能により、Claude Code への指示とプロジェクトコンテキストを効果的にナレッジベース化できます。セキュリティとプライバシーを保ちながら、開発知見の蓄積と共有を実現しましょう。

:::{admonition} 💡 ヒント
:class: tip

初回設定時は `include_claude_md: false` のまま除外設定をテストし、期待通りに動作することを確認してから有効化することをお勧めします。
:::