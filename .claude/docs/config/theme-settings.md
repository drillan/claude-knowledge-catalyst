---
author: null
claude_feature: []
claude_model: []
complexity: beginner
confidence: medium
created: 2025-06-21 00:04:32.048527
domain:
- ai-ml
- data-science
- web-dev
html_theme: furo
html_theme_options:
  dark_css_variables:
    color-brand-content: '#E5B62F'
    color-brand-primary: '#E5B62F'
  light_css_variables:
    color-brand-content: '#336790'
    color-brand-primary: '#336790'
  sidebar_hide_name: true
html_title: プロジェクトドキュメント
projects:
- claude-knowledge-catalyst
purpose: null
status: draft
success_rate: null
tags: []
team: []
tech: []
title: Sphinx テーマ設定
type: code
updated: 2025-06-21 00:04:32.048633
version: '1.0'
---

# Sphinx テーマ設定

このファイルは Sphinx の HTML テーマとその設定を管理します。

## 利用可能なテーマ:

### **Furo** (推奨)

モダンで清潔なデザインのテーマ

```bash
uv add furo --group docs
```

### **Sphinx RTD Theme**

Read the Docs スタイルの定番テーマ

```bash
uv add sphinx-rtd-theme --group docs
```

### **Sphinx Book Theme**

Jupyter Book スタイルのテーマ

```bash
uv add sphinx-book-theme --group docs
```

## テーマ固有オプション:

上記の YAML Front Matter でテーマオプションを設定できます。
`/sphinx-update`コマンドで`conf.py`に自動反映されます。