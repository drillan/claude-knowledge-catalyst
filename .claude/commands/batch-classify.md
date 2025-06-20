---
title: "バッチ分類コマンド"
created: "2025-06-19"
updated: "2025-06-19"
version: "1.0"
category: "code"
subcategory: "Shell"
tags: ["command", "batch", "classification", "automation", "claude"]
complexity: "intermediate"
quality: "medium"
purpose: "ディレクトリ内ファイルの一括分類処理コマンド"
project: "claude-knowledge-catalyst"
status: "experimental"
---

# バッチ分類コマンド

## 使用方法
```bash
# .claudeディレクトリ全体の分類見直し
/batch-classify .claude/

# 特定ディレクトリの分類
/batch-classify .claude/architecture/
```

## 処理フロー

1. **ファイル一覧取得**: 指定ディレクトリ内の.mdファイルを列挙
2. **現在の分類確認**: Obsidianボルト内での現在位置を確認  
3. **最適分類判定**: Claude統合分類システムで適切なカテゴリを判定
4. **移動提案**: 現在位置と推奨位置が異なる場合は移動を提案
5. **バッチ処理**: 承認後に一括移動実行

## 出力例

```yaml
classification_results:
  - file: ".claude/architecture/overview.md"
    current: "20_Knowledge_Base/Code_Snippets/Other_Languages/"
    recommended: "20_Knowledge_Base/Concepts/Development_Patterns/"
    confidence: "high"
    action: "move"
    
  - file: ".claude/debug/issue01.md" 
    current: "20_Knowledge_Base/Code_Snippets/JavaScript/"
    recommended: "20_Knowledge_Base/Resources/Documentation/"
    confidence: "medium"
    action: "move"

summary:
  total_files: 32
  needs_reclassification: 12
  high_confidence: 8
  medium_confidence: 4
```

## 実装ポイント

- **非破壊的**: 元ファイルは保持、Obsidian側のみ移動
- **確認ステップ**: 移動前にユーザー確認
- **ロールバック**: 移動履歴の保持と復元機能