# CLAUDE.md同期機能

Claude Knowledge Catalyst (CKC) では、プロジェクトの `CLAUDE.md` ファイルをObsidianに同期する機能を提供しています。

## 概要

`CLAUDE.md` ファイルは Claude Code への指示やプロジェクト固有の設定を含む重要なファイルです。この機能により、これらの開発コンテキストをObsidianで管理し、ナレッジベースとして活用できます。

## 設定方法

### 基本設定

`ckc_config.yaml` ファイルで CLAUDE.md 同期を有効にします：

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

### 設定オプション

- `include_claude_md`: CLAUDE.mdの同期を有効にするかどうか（デフォルト: false）
- `claude_md_patterns`: 同期対象とする CLAUDE.md ファイルのパターン
- `claude_md_sections_exclude`: 同期から除外するセクションヘッダーのリスト

## セキュリティとプライバシー

### 除外機能

機密情報を含むセクションは同期から除外できます：

```yaml
claude_md_sections_exclude:
  - "# secrets"        # API キーなどの秘密情報
  - "# private"        # 個人的なメモ
  - "# confidential"   # 機密プロジェクト情報
  - "# internal"       # 内部専用情報
```

### 除外される内容

指定したセクションヘッダー以下の全ての内容が除外されます。

例：
```markdown
# Project Overview
これは公開されます。

# secrets
API_KEY=secret123
DATABASE_URL=secret://...
# ↑ このセクション全体が除外されます

# Commands  
これも公開されます。
```

## メタデータ強化

CLAUDE.md ファイルには以下の特別なメタデータが自動付与されます：

- `file_type: claude_config`
- `is_claude_md: true`
- `project_root`: プロジェクトルートパス
- `sections_filtered`: セクションフィルタリングが有効かどうか
- `excluded_sections`: 除外されたセクションのリスト
- `has_project_overview`: プロジェクト概要が含まれているか
- `has_architecture_info`: アーキテクチャ情報が含まれているか
- `has_commands`: コマンド情報が含まれているか
- `has_guidelines`: ガイドライン情報が含まれているか

## 使用シナリオ

### 推奨される場合

- 個人開発プロジェクト
- チーム全体でObsidianを活用している場合
- CLAUDE.mdに機密情報が含まれていない場合
- ナレッジマネジメントを重視する場合

### 避けるべき場合

- 機密性の高いプロジェクト
- CLAUDE.mdにプロジェクト固有の秘匿情報が含まれる場合
- チームメンバーがObsidianを使用していない場合

## 実装詳細

- セクションフィルタリングは大文字小文字を区別しません
- 除外されたセクション以下の全ての内容（サブセクション含む）が除外されます
- 空のCLAUDE.mdファイルは同期されません
- ファイル名が正確に "CLAUDE.md" でない場合は同期されません

## トラブルシューティング

### CLAUDE.mdが同期されない場合

1. `include_claude_md: true` が設定されているか確認
2. ファイル名が正確に "CLAUDE.md" になっているか確認
3. ファイルが空でないか確認
4. 除外設定により全てのコンテンツが除外されていないか確認

### セクション除外が効かない場合

1. セクションヘッダーの形式が正確か確認（`# セクション名`）
2. 大文字小文字の違いは問題ありません
3. 除外パターンの記述に誤りがないか確認