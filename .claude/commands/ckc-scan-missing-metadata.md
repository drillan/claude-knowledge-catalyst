---
title: "メタデータ欠損ファイル検出"
created: "2025-06-19"
updated: "2025-06-19"
version: "1.0"
category: "code"
subcategory: "Python"
tags: ["metadata", "scan", "command", "automation", "quality"]
complexity: "intermediate"
quality: "high"
purpose: "メタデータが不足しているファイルを検出・分析するコマンド"
project: "claude-knowledge-catalyst"
status: "production"
---

# メタデータ欠損ファイル検出

## 使用方法
```bash
/ckc-scan-missing-metadata
```

## 処理内容

### 1. ファイルスキャン
`.claude`ディレクトリ内の全Markdownファイルを検査し、フロントマターの有無を確認

### 2. 分類結果表示
```
メタデータ状況レポート
========================

✅ メタデータあり (15ファイル):
├── .claude/development.md
├── .claude/first-plan.md  
├── .claude/project-knowledge.md
└── ...

⚠️  メタデータなし (17ファイル):
├── .claude/architecture/overview.md
├── .claude/commands/learnings.md
├── .claude/debug/issue01.md
└── ...

📊 統計:
├── 全ファイル数: 32
├── 完了率: 47% (15/32)
└── 要分類: 17ファイル
```

### 3. 次のアクション提案
```
推奨アクション:
1. /ckc-classify-missing  # 未分類ファイルを一括分類
2. /ckc-classify <file>   # 個別ファイル分類  
3. /ckc-smart-sync        # 分類→同期を一括実行
```

## 実装ロジック

### フロントマター検出
```python
def has_frontmatter(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # YAMLフロントマターパターン
    pattern = r'^---\s*\n.*?\n---\s*\n'
    return bool(re.match(pattern, content, re.DOTALL))
```

### ファイル分析
```python
def analyze_file_metadata(file_path):
    return {
        'path': file_path,
        'has_frontmatter': has_frontmatter(file_path),
        'file_size': os.path.getsize(file_path),
        'modified': os.path.getmtime(file_path),
        'content_preview': get_content_preview(file_path, 200)
    }
```

### 優先度判定
```python
def calculate_priority(file_info):
    priority = 0
    
    # ファイル名による優先度
    if 'development' in file_info['path']:
        priority += 10
    if 'architecture' in file_info['path']:
        priority += 8
    if 'debug' in file_info['path']:
        priority += 5
        
    # 更新日時による優先度
    if file_info['modified'] > recent_threshold:
        priority += 5
        
    return priority
```

## 出力形式

### JSON形式
```json
{
  "scan_timestamp": "2025-06-19T18:00:00",
  "total_files": 32,
  "has_metadata": {
    "count": 15,
    "files": ["file1.md", "file2.md"]
  },
  "missing_metadata": {
    "count": 17,
    "files": [
      {
        "path": ".claude/architecture/overview.md",
        "priority": 18,
        "size": 2048,
        "preview": "# CKC アーキテクチャ概要..."
      }
    ]
  },
  "completion_rate": 0.47
}
```

### テーブル形式
```
| ファイル                              | メタデータ | 優先度 | サイズ | 最終更新    |
|--------------------------------------|-----------|-------|--------|------------|
| .claude/architecture/overview.md     | ❌        | 18    | 2.0KB  | 2h ago     |
| .claude/development.md               | ✅        | -     | 15.2KB | 1h ago     |
| .claude/debug/issue01.md             | ❌        | 12    | 856B   | 30m ago    |
```

## 活用方法

1. **定期チェック**: 週次でメタデータ状況を確認
2. **優先分類**: 高優先度ファイルから分類実行
3. **品質管理**: 完了率の継続的改善