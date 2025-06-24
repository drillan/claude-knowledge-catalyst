---
author: null
claude_feature:
- code-generation
claude_model: []
complexity: intermediate
confidence: medium
created: 2025-06-21 00:04:32.056685
description: Initialize new Sphinx project with MyST Markdown support
domain:
- ai-ml
- automation
- data-science
- security
- web-dev
name: sphinx-create
projects:
- claude-knowledge-catalyst
purpose: null
status: draft
success_rate: null
tags: []
team: []
tech:
- docker
- git
- typescript
title: Sphinx プロジェクト初期化
type: prompt
updated: 2025-06-21 00:04:32.056819
version: '1.0'
---

# Sphinx プロジェクト初期化

新しい Sphinx ドキュメントプロジェクトを作成し、MyST Markdown サポートを自動設定します。

## 前提条件

- パッケージは uv で管理する
- ドキュメント関連のパッケージは `uv add` コマンドのオプションに `--group docs` をつける

## 実行内容:

1. **環境準備**

```bash
# 必要なパッケージをインストール
uv add sphinx --group docs
uv add "myst-parser" --group docs
```

2. プロジェクト情報取得

PROJECT_NAME:

- pyproject.toml から project.name と authors[0].name を取得
- 取得できない場合は `basename $PWD` (プロジェクトルートのディレクトリ名)から取得

AUTHOR_NAME:

- pyproject.toml から authors[0].name を取得
- 取得できない場合は次の優先順位で取得
  - `git config --get user.name` (Git のユーザ名)
  - `$USER` (OS のユーザ名)から取得

3. Sphinx プロジェクト作成

`sphinx-quickstart -q -p "PROJECT_NAME" -a "AUTHOR_NAME" ./docs`

4. Markdown へ変換

```bash
uvx --from "rst-to-myst[sphinx]" rst2myst convert docs/index.rst
rm docs/index.rst
```

5. 初期設定適用

- .claude/docs/config/の設定ファイルから初期テーマを適用
- 基本的な拡張機能を有効化

6. MyST 拡張機能 (デフォルト):

- amsmath (数式サポート)
- attrs_inline (インライン属性)
- colon_fence (コロンコードブロック)
- deflist (定義リスト)
- dollarmath (ドル記号数式)
- fieldlist (フィールドリスト)
- html_admonition (HTML 警告)
- html_image (HTML 画像)
- linkify (自動リンク)
- replacements (テキスト置換)
- smartquotes (スマートクォート)
- strikethrough (取り消し線)
- substitution (置換)
- tasklist (タスクリスト)

linkify を使う場合、次のコマンドでパッケージを追加する

`uv add linkify linkify-it-py --group docs`

7. ビルドのテスト

ドキュメントのビルドは @.claude/commands/sphinx-build.md に従って実行します
