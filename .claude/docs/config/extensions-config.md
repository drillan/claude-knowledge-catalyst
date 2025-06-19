---
extensions:
  - myst_parser
  - sphinx.ext.autodoc
  - sphinx.ext.napoleon
  - sphinx.ext.viewcode
  - sphinx.ext.intersphinx

myst_enable_extensions:
  - amsmath
  - attrs_inline
  - colon_fence
  - deflist
  - dollarmath
  - fieldlist
  - html_admonition
  - html_image
  - linkify
  - replacements
  - smartquotes
  - strikethrough
  - substitution
  - tasklist

autodoc_default_options:
  members: true
  member-order: bysource
  special-members: __init__
  undoc-members: true

napoleon_google_docstring: true
napoleon_numpy_docstring: true
napoleon_include_init_with_doc: false

intersphinx_mapping:
  python:
    - https://docs.python.org/3
    - null
---

# Sphinx拡張機能設定

このファイルはSphinxの拡張機能とその設定を管理します。

## コア拡張機能:

### **MyST Parser**
Markdownサポートの中核となる拡張機能
- 豊富なMarkdown拡張機能
- reStructuredTextとの互換性
- 数式、図表、コードブロックのサポート

### **Autodoc**
Pythonコードからの自動ドキュメント生成
- docstringからの自動抽出
- クラス・関数・モジュールの文書化
- 型ヒントのサポート

### **Napoleon**
Google/NumPyスタイルのdocstringサポート
- 読みやすいdocstring形式
- パラメータと戻り値の構造化

### **Intersphinx**
外部ドキュメントへのクロスリファレンス
- Python公式ドキュメントへのリンク
- 他のSphinxプロジェクトとの連携

## 拡張機能の追加:

新しい拡張機能を追加する場合:
1. 上記YAML Front Matterの`extensions`リストに追加
2. 必要に応じて設定オプションを追加
3. `/sphinx-update`コマンドで反映
4. 必要なパッケージを`uv add --group docs`でインストール