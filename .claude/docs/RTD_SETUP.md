---
author: null
category: resource
claude_feature: []
claude_model: []
complexity: advanced
confidence: medium
created: 2025-06-20 00:00:00
domain:
- ai-ml
- data-science
- testing
- web-dev
project: claude-knowledge-catalyst
projects:
- claude-knowledge-catalyst
purpose: Auto-generated metadata for RTD_SETUP
quality: high
status: draft
subcategory: Documentation
success_rate: null
tags:
- documentation
- guide
- manual
- reference
team: []
tech:
- api
- git
- python
- typescript
title: Rtd Setup
type: prompt
updated: 2025-06-21 00:04:32.045981
version: '1.0'
---

# Read the Docs セットアップガイド

このファイルは、Claude Knowledge CatalystのドキュメントをRead the Docsでホスティングするための設定手順を説明します。

## 📋 完了済み設定

### 1. Read the Docs設定ファイル
- `.readthedocs.yaml` - RTD v2設定ファイル
- Ubuntu 24.04、Python 3.11環境
- PDF、HTMLZip形式の自動生成
- 検索最適化設定

### 2. 依存関係管理
- `pyproject.toml` - docs用依存関係をRTD互換形式に移行
- `docs/requirements.txt` - RTD用バックアップ要件ファイル
- 主要パッケージ：Sphinx 8.2.3+、MyST Parser 4.0.1+、Furo テーマ

### 3. Sphinx設定最適化
- RTD環境自動検出
- GitHub連携設定
- SEO最適化（メタデータ、構造化データ）
- Intersphinx外部リンク統合

## 🚀 Read the Docs設定手順

### 1. RTDアカウントでプロジェクトインポート
1. [Read the Docs](https://readthedocs.org/) にログイン
2. 「Import a Project」をクリック
3. GitHubリポジトリ `drillan/claude-knowledge-catalyst` を選択
4. プロジェクト名: `claude-knowledge-catalyst`

### 2. プロジェクト設定
- **言語**: Japanese (ja)
- **プログラミング言語**: Python
- **リポジトリURL**: `https://github.com/drillan/claude-knowledge-catalyst`
- **デフォルトブランチ**: `main`

### 3. ビルド設定
RTDは自動的に `.readthedocs.yaml` を検出し、以下の設定で動作します：
- Python 3.11
- Ubuntu 24.04
- Sphinx ビルダー
- docs/ ディレクトリからのビルド

### 4. Webhook設定
GitHubプッシュ時の自動ビルドは自動設定されます。

## 📊 ビルド仕様

### 想定ビルド時間
- **初回**: 3-5分（依存関係インストール含む）
- **更新**: 1-2分（増分ビルド）

### リソース使用量
- **メモリ**: ~500MB
- **ストレージ**: ~50MB
- **帯域幅**: ~10MB（HTML + PDF + ZIP）

### サポート形式
- **HTML**: メインドキュメント（レスポンシブ）
- **PDF**: オフライン配布用
- **HTMLZip**: ローカル閲覧用

## 🔗 期待されるURL構造

### プライマリURL
- **メイン**: https://claude-knowledge-catalyst.readthedocs.io/
- **安定版**: https://claude-knowledge-catalyst.readthedocs.io/en/stable/
- **最新版**: https://claude-knowledge-catalyst.readthedocs.io/en/latest/

### セクション別URL
- **クイックスタート**: https://claude-knowledge-catalyst.readthedocs.io/en/latest/quick-start/
- **ユーザーガイド**: https://claude-knowledge-catalyst.readthedocs.io/en/latest/user-guide/
- **開発者ガイド**: https://claude-knowledge-catalyst.readthedocs.io/en/latest/developer-guide/
- **APIリファレンス**: https://claude-knowledge-catalyst.readthedocs.io/en/latest/api-reference/

## ⚠️ 注意事項

### RTD制限
- **ビルド時間**: 10分制限（現在のプロジェクトでは十分）
- **月間ビルド数**: 無制限（OSS）
- **ストレージ**: 無制限（OSS）

### 警告解決
現在のビルド警告（3件）は機能に影響しません：
1. favicon未設定（オプション）
2. 外部インベントリ404（Typer）
3. docstring書式（軽微）

## 🎯 成功基準

### 技術基準
- ✅ ビルド成功率 >95%
- ✅ ページロード時間 <2秒
- ✅ モバイル対応（レスポンシブ）
- ✅ 検索機能動作

### 内容基準
- ✅ 全セクション正常表示
- ✅ 内部リンク正常動作
- ✅ Mermaidダイアグラム表示
- ✅ コードハイライト動作

---
*設定日: 2025年6月19日*  
*RTD v2設定ファイル使用*