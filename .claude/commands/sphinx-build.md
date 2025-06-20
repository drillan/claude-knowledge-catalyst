---
author: null
claude_feature: []
claude_model: []
complexity: intermediate
confidence: medium
created: 2025-06-21 00:04:32.059683
description: Build Sphinx documentation in various formats
domain:
- ai-ml
- data-science
- web-dev
name: sphinx-build
projects:
- claude-knowledge-catalyst
purpose: null
status: draft
success_rate: null
tags: []
team: []
tech: []
title: Sphinx ドキュメントビルド
type: code
updated: 2025-06-21 00:04:32.059779
version: '1.0'
---

# Sphinx ドキュメントビルド

Sphinx ドキュメントを指定された形式でビルドします。

## ビルドオプション:

1. **HTML ビルド** (デフォルト)

```bash
uv run sphinx-build -b html ./docs ./docs/_build/html
```

2. **クリーンビルド**

```bash
uv run sphinx-build -E -a -b html ./docs ./docs/_build/html
```

3. **その他の形式**

- LaTeX: `-b latex`
- PDF: `-b latex` + LaTeX 処理
- EPUB: `-b epub`

## 使用方法:

- `/sphinx-build` - HTML ビルド
- `/sphinx-build clean` - クリーン HTML ビルド
- `/sphinx-build latex` - LaTeX ビルド

## 出力先:

- HTML: `docs/_build/html/`
- その他: `docs/_build/{format}/`

## 事前チェック:

- 依存関係の確認: `uv sync --group docs`
- 設定ファイルの整合性チェック
- ソースファイルの存在確認