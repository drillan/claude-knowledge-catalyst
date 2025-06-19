---
name: sphinx-build
description: Build Sphinx documentation in various formats
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
