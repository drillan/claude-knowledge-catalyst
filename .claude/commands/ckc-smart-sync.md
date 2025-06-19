---
title: "CKCスマート同期コマンド"
created: "2025-06-19"
updated: "2025-06-19"
version: "2.0"
category: "code"
subcategory: "Python"
tags: ["sync", "automation", "claude", "workflow", "smart", "cli"]
complexity: "advanced"
quality: "high"
purpose: "CKC CLIスマート同期コマンドのスラッシュコマンドラッパー"
project: "claude-knowledge-catalyst"
status: "production"
---

# CKCスマート同期コマンド

## 概要
CKCの`smart-sync`コマンドを呼び出すスラッシュコマンド。
インテリジェントなバッチ分類と同期を実行します。

## 使用方法

### スラッシュコマンド（推奨）
```bash
# 基本実行（確認付き）
/ckc-smart-sync

# プレビューモード（実行なし）
/ckc-smart-sync-dry-run

# 自動適用モード（確認なし）
/ckc-smart-sync-auto
```

### 直接CLIコマンド
```bash
# 基本実行（確認付き）
uv run ckc smart-sync

# 自動適用モード（確認なし）
uv run ckc smart-sync --auto-apply

# プレビューモード（実行なし）
uv run ckc smart-sync --dry-run

# 特定ディレクトリを対象
uv run ckc smart-sync --directory .claude/custom

# バックアップなしで実行
uv run ckc smart-sync --no-backup
```

## 処理フロー

### Phase 1: メタデータ存在チェック
```python
def scan_metadata_status():
    files = glob('.claude/**/*.md')
    has_metadata = []
    needs_classification = []
    
    for file in files:
        if has_frontmatter(file):
            has_metadata.append(file)
        else:
            needs_classification.append(file)
    
    return has_metadata, needs_classification
```

### Phase 2: Claude統合分類
未分類ファイルに対してClaude分析実行:

**ファイル**: `{file_path}`
**内容プレビュー**: `{content_preview}`

以下の形式で分類してください:
```yaml
classification:
  category: "適切なカテゴリ"
  tags: ["タグ1", "タグ2", "タグ3"]
  complexity: "beginner/intermediate/expert"
  quality: "high/medium/low"
  purpose: "ファイルの目的説明"
```

### Phase 3: メタデータ適用
```python
def apply_metadata(file_path, classification):
    # バックアップ作成
    backup_path = f"{file_path}.backup"
    shutil.copy2(file_path, backup_path)
    
    # フロントマター生成
    frontmatter = generate_frontmatter(classification)
    
    # ファイル更新
    with open(file_path, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.write(f"{frontmatter}\n{content}")
```

### Phase 4: CKC同期実行
```bash
uv run ckc sync
```

## エラーハンドリング

### バックアップ&復旧
```python
def rollback_changes(file_list):
    for file_path in file_list:
        backup_path = f"{file_path}.backup"
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, file_path)
            os.remove(backup_path)
```

### 分類失敗時の対応
- デフォルトメタデータの適用
- 手動分類モードへの移行
- スキップして既存メタデータファイルのみ同期

## 実行例

```bash
# メタデータスキャン結果
Found 32 files in .claude/
├── Has metadata: 15 files ✓
└── Needs classification: 17 files ⚠️

# Claude分類実行
Classifying: .claude/architecture/overview.md
└── Category: Concepts/Development_Patterns
└── Confidence: High
└── Apply? [y/N]: y

# メタデータ適用
Applied metadata to 17 files
├── Success: 16 files ✓
└── Failed: 1 file ❌

# CKC同期実行  
uv run ckc sync
└── Synced 31/32 files ✓
```

## 設定オプション

```yaml
smart_sync:
  auto_apply: false          # 自動適用 vs 確認要求
  backup_enabled: true       # バックアップ作成
  fallback_category: "10-Inbox"  # 分類失敗時のデフォルト
  confidence_threshold: "medium"  # 適用する最低信頼度
```