---
title: "CI/CD無限ループ問題 - トラブルシューティングガイド"
category: troubleshooting
type: guide
status: production
confidence: high
created: 2025-06-24
updated: 2025-06-24
author: Claude Code
project: claude-knowledge-catalyst
purpose: CI/CDパイプラインとpre-commitの無限ループ問題の診断と解決手順
tags:
  - ci-cd
  - troubleshooting
  - ruff
  - pre-commit
  - github-actions
tech:
  - ruff
  - pre-commit
  - github-actions
  - uv
  - python
domain:
  - devops
  - testing
complexity: advanced
---

# CI/CD無限ループ問題 - トラブルシューティングガイド

## 問題の概要

GitHub Actions CI/CDパイプラインとpre-commitフックの間で、リンティング・フォーマッティングツール（特にRuff）の動作不整合により無限ループが発生する問題。

## 症状の識別

### 典型的な症状
1. **ローカルでpre-commit成功 → CI失敗のサイクル**
2. **同じファイルに対して繰り返しエラー**
3. **`ruff format`が成功表示するのにCI失敗**
4. **修正後も同じエラーが再発**

### 確認コマンド
```bash
# ローカル環境でのチェック
uv run ruff check src/ tests/ --output-format=github
uv run ruff format src/ tests/ --check

# Pre-commit実行
uv run pre-commit run --all-files

# バージョン確認
uv run ruff --version
```

## 根本原因の診断

### 1. 動作モードの不整合確認

**Pre-commit設定確認**:
```bash
cat .pre-commit-config.yaml
```

確認ポイント:
- `args: [--fix]` → 自動修正モード
- `args: [--check]` → チェックのみモード
- `args`なし → デフォルト動作

**GitHub Actions設定確認**:
```bash
cat .github/workflows/ci.yml
```

確認ポイント:
- `--check`フラグの有無
- `--output-format=github`の使用

### 2. バージョン不整合の確認

```bash
# ローカルRuffバージョン
uv run ruff --version

# Pre-commitで使用されるバージョン
grep -A2 "astral-sh/ruff-pre-commit" .pre-commit-config.yaml
```

### 3. 実際の動作確認

```bash
# 同じファイルでテスト
echo "import   os,sys" > test_import.py

# ローカル環境
uv run ruff check test_import.py
uv run ruff format test_import.py --check

# Pre-commit環境
uv run pre-commit run --files test_import.py
```

## 解決手順

### Step 1: バージョン統一
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.6  # 最新の安定版に更新
    hooks:
      - id: ruff
      - id: ruff-format
```

### Step 2: 動作モード統一
```yaml
# Pre-commit: チェックのみに変更
- id: ruff
  name: ruff linting
  # args: [--fix] を削除

- id: ruff-format
  name: ruff formatting check
  args: [--check]  # チェックのみ
```

### Step 3: 設定の再インストール
```bash
# Pre-commitフック再インストール
uv run pre-commit clean
uv run pre-commit install --overwrite

# キャッシュクリア
uv run pre-commit clean
```

### Step 4: 検証
```bash
# 修正適用（手動）
uv run ruff check src/ tests/ --fix
uv run ruff format src/ tests/

# 確認
uv run pre-commit run --all-files
uv run ruff check src/ tests/ --output-format=github
```

## 予防策

### 1. 設定テンプレート

**推奨Pre-commit設定**:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.6  # 定期的に更新
    hooks:
      - id: ruff
        name: ruff linting
        # 注意: --fix は使用しない（CI一貫性のため）
      - id: ruff-format
        name: ruff formatting check
        args: [--check]
        # 注意: --check で統一
```

**推奨GitHub Actions設定**:
```yaml
- name: Lint with ruff
  run: uv run ruff check src/ tests/ --output-format=github

- name: Format check with ruff
  run: uv run ruff format src/ tests/ --check
```

### 2. 開発者ワークフロー

```bash
# 開発時の推奨ワークフロー
# 1. コード修正
# 2. 手動でリント・フォーマット
uv run ruff check src/ tests/ --fix
uv run ruff format src/ tests/

# 3. 確認
uv run pre-commit run --all-files

# 4. コミット
git add .
git commit -m "fix: description"
```

### 3. 監視とメンテナンス

```bash
# 定期的なバージョン確認（月次推奨）
uv run pre-commit autoupdate

# 設定整合性確認
diff <(uv run ruff --version) <(echo "期待バージョン")
```

## トラブルシューティングコマンド集

### 緊急時の即座修正
```bash
# すべてのエラーを一括修正
uv run ruff check src/ tests/ --fix --unsafe-fixes
uv run ruff format src/ tests/

# Pre-commit完全リセット
uv run pre-commit uninstall
uv run pre-commit clean
uv run pre-commit install
```

### デバッグ用コマンド
```bash
# 詳細な差分確認
uv run ruff format src/ tests/ --check --diff

# 特定ファイルの詳細チェック
uv run ruff check specific_file.py --show-fixes

# Pre-commit詳細実行
uv run pre-commit run --all-files --verbose
```

### CIでの詳細ログ取得
```yaml
# GitHub Actionsで詳細ログ
- name: Debug ruff issues
  run: |
    echo "Ruff version:"
    uv run ruff --version
    echo "Checking with diff:"
    uv run ruff format src/ tests/ --check --diff || true
    echo "Lint details:"
    uv run ruff check src/ tests/ --show-fixes || true
```

## よくある質問

### Q: なぜ`--fix`を使わないのか？
**A**: Pre-commitで自動修正すると、CI側でチェックのみ行うため、修正されたファイルが再度エラーとして検出される。一貫性のため、両方でチェックのみ実行。

### Q: バージョンアップのタイミングは？
**A**: 月次での`pre-commit autoupdate`実行を推奨。ただし、メジャーバージョンアップ時は動作変更の可能性があるため、テスト環境での事前確認が必要。

### Q: 緊急でCI通す必要がある場合は？
**A**: 一時的に`--no-verify`でコミットし、後で修正コミットを追加：
```bash
git commit --no-verify -m "urgent: bypass pre-commit for emergency"
# 後で修正
uv run ruff check src/ tests/ --fix
uv run ruff format src/ tests/
git add .
git commit -m "fix: apply ruff fixes post-emergency"
```

## 関連リソース

- [Ruff公式ドキュメント](https://docs.astral.sh/ruff/)
- [Pre-commit公式ドキュメント](https://pre-commit.com/)
- [プロジェクト改善履歴](.claude/project-improvements.md)
- [GitHub Actions CI設定](.github/workflows/ci.yml)
- [Pre-commit設定](.pre-commit-config.yaml)
