---
title: "ファイル分類コマンド"
created: "2025-06-19"
updated: "2025-06-19"
version: "1.0"
category: "prompt"
subcategory: "Templates"
tags: ["classification", "prompt", "template", "obsidian", "automation"]
complexity: "intermediate"
quality: "high"
purpose: "単一ファイルの分類用プロンプトテンプレート"
project: "claude-knowledge-catalyst"
status: "production"
---

# ファイル分類コマンド

## 使用方法
```bash
# 単一ファイルの分類
/classify-file .claude/development.md

# 内容確認付き分類
/classify-file-verbose .claude/development.md
```

## プロンプトテンプレート

以下のファイルを適切なObsidianカテゴリに分類してください：

**ファイルパス**: `{file_path}`
**ファイル名**: `{filename}`

**ファイル内容** (先頭部分):
```
{content_preview}
```

**利用可能カテゴリ**:
1. `20_Knowledge_Base/Concepts/Development_Patterns/` - 開発手法・ガイド・環境設定
2. `20_Knowledge_Base/Concepts/AI_Fundamentals/` - AI・LLM関連概念
3. `20_Knowledge_Base/Code_Snippets/Python/` - Python実行可能コード
4. `20_Knowledge_Base/Code_Snippets/JavaScript/` - JavaScript実行可能コード
5. `20_Knowledge_Base/Code_Snippets/Shell/` - シェルスクリプト・コマンド
6. `20_Knowledge_Base/Prompts/Templates/` - プロンプトテンプレート
7. `20_Knowledge_Base/Resources/Documentation/` - リファレンス・ドキュメント

**分類基準**:
- **Development_Patterns**: 開発プロセス、環境設定、手順書、ベストプラクティス
- **Code_Snippets**: 実行可能なコード、関数定義、スクリプト
- **Prompts**: LLM用指示文、プロンプトテンプレート
- **Concepts**: 概念説明、理論、アーキテクチャ解説
- **Resources**: 参考資料、外部リンク、ドキュメント

**出力形式**:
```yaml
recommended_path: "適切なカテゴリパス"
confidence: "high/medium/low"
reasoning: "分類理由の説明"
alternative_paths: ["代替候補1", "代替候補2"]
```

最適なカテゴリを判定してください。