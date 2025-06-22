# CLAUDE.md - Demo Directory Instructions

このファイルはClaude Codeがdemoディレクトリで作業する際の専用指示です。

## 🚨 CRITICAL: デモスクリプト標準パターン（必須遵守）

### ✅ 推奨パターン（必ず使用）

```bash
# Function to run CKC commands (デモディレクトリ内で実行)
run_ckc() {
    # PYTHONPATH設定でCKCを利用可能にし、現在のディレクトリで実行
    PYTHONPATH="$PROJECT_ROOT/src" "$PROJECT_ROOT/.venv/bin/python" -m claude_knowledge_catalyst.cli.main "$@"
}
```

**使用例:**
```bash
cd "$DEMO_DIR/my_project"  # デモプロジェクトディレクトリに移動
run_ckc init               # 現在のディレクトリでCKC初期化
run_ckc add vault-name /path/to/vault
run_ckc sync
run_ckc project list
```

**🚨 重要**: デモファイルは必ずdemoディレクトリ内に生成すること

### ❌ 禁止パターン（絶対に使用禁止）

```bash
# ❌ プロジェクトルートからの実行（ファイルがルートに作成される）
(cd "$PROJECT_ROOT" && uv run ckc "$@")

# ❌ 複雑なPython実行は禁止
uv run python -c "..."

# ❌ 内部実装の直接呼び出しは禁止
from claude_knowledge_catalyst.cli.main import main
from claude_knowledge_catalyst.cli.main import cli
```

### 🎯 デモディレクトリ分離の原則

**必須要件:**
1. **全ての設定ファイル**はdemoディレクトリ内に作成
2. **ckc_config.yaml**はプロジェクトルートに作成してはいけない
3. **デモ用ボルト**はdemo/内に配置
4. **プロジェクトルートを汚染しない**

## 📋 デモスクリプト必須要件

### 1. 実際のユーザー体験との一致
- デモで使用するコマンドは、実際のユーザーが使用するコマンドと完全に一致させること
- 内部実装の詳細をユーザーに見せないこと

### 2. 標準run_ckc関数の使用
- 全てのデモスクリプトで統一された`run_ckc`関数を使用すること
- 直接的なPython呼び出しやモジュール呼び出しは禁止

### 3. ユーザー向けコマンド表示
```bash
echo "$ ckc init"
run_ckc init

echo "$ ckc sync --project Frontend-Team"
run_ckc sync --project Frontend-Team
```

### 4. エラーハンドリング
- 適切なエラーメッセージ表示
- 失敗時の状況説明
- ユーザーが理解しやすい説明

## 🔧 デモスクリプト作成チェックリスト

**作成前確認:**
- [ ] `run_ckc`関数が標準パターンで実装されている
- [ ] 直接Python呼び出しが含まれていない
- [ ] 実際のCLIコマンド(`ckc`)のみを使用している

**内容確認:**
- [ ] ユーザーが実際に入力するコマンドを表示している
- [ ] デモの各ステップに適切な説明がある
- [ ] 生成される結果が期待通りに表示される

**テスト確認:**
- [ ] クリーンな環境でデモが正常に動作する
- [ ] エラー発生時に適切なメッセージが表示される
- [ ] クリーンアップが正常に機能する

## 🎯 デモの品質基準

### 高品質なデモの特徴
1. **実用性**: 実際のユースケースを反映
2. **明確性**: 各ステップの目的が明確
3. **再現性**: 環境に依存せず確実に動作
4. **教育的**: ユーザーがCKCの価値を理解できる

### 避けるべき実装
1. **複雑なワークアラウンド**: 内部実装への直接アクセス
2. **環境依存**: 特定の設定や状態に依存する処理
3. **隠れた前提**: 説明されていない前提条件

## 📁 デモファイル構造ガイドライン

### 標準的なデモスクリプト構造
```bash
#!/bin/bash

# [デモタイトル] for Claude Knowledge Catalyst
set -e

PROJECT_ROOT="/home/driller/repo/claude-knowledge-catalyst"
DEMO_DIR="$PROJECT_ROOT/demo"

# Function to run CKC commands
run_ckc() {
    (cd "$PROJECT_ROOT" && uv run ckc "$@")
}

# Setup
echo "🧹 Setting up demo environment..."
# [setup code]

# Demo steps
echo "👤 USER ACTION: [action description]"
echo "$ ckc [command]"
run_ckc [command]

# Results
echo "✅ Demo complete!"
# [results summary]
```

## 🚨 Issue02 Prevention

**背景**: demo.shで直接Python実行が使用される問題が繰り返し発生

**防止策**: 
1. この指示に従った標準パターンの使用を強制
2. デモスクリプト修正時は必ずこの指示を参照
3. 新しいデモ作成時は標準テンプレートを使用

**レビューポイント**:
- `python -c`パターンの有無
- `run_ckc`関数の標準実装
- 実際のCLIコマンドとの一致性

## 📝 デモスクリプト作成テンプレート

新しいデモスクリプト作成時は、以下のテンプレートを使用してください：

```bash
#!/bin/bash

# [Demo Name] for Claude Knowledge Catalyst
set -e

PROJECT_ROOT="/home/driller/repo/claude-knowledge-catalyst"
DEMO_DIR="$PROJECT_ROOT/demo"

echo "🎯 [Demo Title]"
echo "=============================="
echo ""
echo "[Demo description]"
echo ""

# Cleanup previous runs
echo "🧹 Setting up demo environment..."
rm -rf "$DEMO_DIR/[demo_directories]"
mkdir -p "$DEMO_DIR/[demo_directories]"

# Function to run CKC commands (デモディレクトリ内で実行)
run_ckc() {
    PYTHONPATH="$PROJECT_ROOT/src" "$PROJECT_ROOT/.venv/bin/python" -m claude_knowledge_catalyst.cli.main "$@"
}

# Navigate to demo project directory
cd "$DEMO_DIR/[demo_project_dir]"

# Demo steps
echo "👤 USER ACTION: [Description]"
echo "$ ckc [command]"
run_ckc [command]

echo ""
echo "✅ Demo complete!"
echo ""
echo "🎯 What was demonstrated:"
echo "  ✅ [Feature 1]"
echo "  ✅ [Feature 2]"
echo ""
echo "📁 Demo files location:"
echo "  - Config: $DEMO_DIR/[demo_project_dir]/ckc_config.yaml"
echo "  - Vault: $DEMO_DIR/[demo_vault_dir]"
```

## 🔍 自動品質チェック

デモスクリプト修正時は、以下をチェックしてください：

```bash
# 禁止パターンが含まれていないことを確認
grep -E "cd.*PROJECT_ROOT.*uv run ckc|python -c" demo/*.sh
# 結果: 何も表示されないこと（プロジェクトルート実行パターンなし）

# プロジェクトルートに設定ファイルが作成されていないか確認
ls "$PROJECT_ROOT/ckc_config.yaml" 2>/dev/null && echo "❌ 設定ファイルがルートに作成されています" || echo "✅ 設定ファイル分離OK"

# 標準パターンが使用されていることを確認
grep -E "PYTHONPATH.*python -m claude_knowledge_catalyst" demo/*.sh
# 結果: 全てのスクリプトで統一されたrun_ckc関数が確認できること
```

## 🚨 Issue02 完全解決記録

**問題**: `demo/demo.sh`で複雑なPython直接呼び出しが使用されていた

**修正前**:
```bash
uv run python -c "
import sys, os
sys.path.insert(0, '$PROJECT_ROOT/src')
os.chdir('$demo_dir')
from claude_knowledge_catalyst.cli.main import main
main()
" "$@"
```

**修正後**:
```bash
run_ckc() {
    PYTHONPATH="$PROJECT_ROOT/src" "$PROJECT_ROOT/.venv/bin/python" -m claude_knowledge_catalyst.cli.main "$@"
}
```

**さらなる改善（デモディレクトリ分離）**:
- 🎯 プロジェクトルートからの実行を禁止
- 🎯 設定ファイルのデモディレクトリ内生成を強制
- 🎯 プロジェクトルートの汚染防止

**効果**:
- ✅ 実際のユーザー体験との一致
- ✅ デモファイルの完全分離
- ✅ プロジェクトルートのクリーン維持
- ✅ 再発防止の仕組み化

---

**重要**: このルールは品質向上と再発防止のために策定されました。
デモの信頼性とユーザー体験の向上のため、必ず遵守してください。

**Claude Code指示**: デモディレクトリでの作業時は、必ずこの標準パターンを使用し、
直接Python呼び出しは絶対に行わないでください。