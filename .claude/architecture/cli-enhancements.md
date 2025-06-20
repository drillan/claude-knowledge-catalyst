---
author: null
category: concept
claude_feature: []
claude_model: []
complexity: advanced
confidence: medium
created: 2025-06-19 00:00:00
domain:
- ai-ml
- automation
- data-science
- mobile
- web-dev
project: claude-knowledge-catalyst
projects:
- claude-knowledge-catalyst
purpose: CKC CLIの機能拡張とユーザビリティ向上提案
quality: high
status: pending
subcategory: Development_Patterns
success_rate: null
tags:
- architecture
- cli
- enhancement
- smart-sync
- user-experience
team: []
tech:
- python
title: CKC CLI機能拡張提案
type: prompt
updated: 2025-06-21 00:04:32.035846
version: '1.0'
---

# CKC CLI機能拡張提案

## 概要

CKCのCLIコマンドとして`smart-sync`機能を実装し、カスタムスラッシュコマンドから呼び出せるようにする提案。

## 提案背景

### 現在の課題
- メタデータなしファイルの手動分類が非効率
- バッチ処理機能がCKC本体に統合されていない
- Claude統合分類システムが独立したスクリプト

### 提案解決策
- `uv run ckc smart-sync`コマンドの実装
- 既存アーキテクチャとの統合
- カスタムスラッシュコマンドからの簡単アクセス

## 実装アーキテクチャ

### 1. CKC CLI統合

#### コマンド構造
```bash
uv run ckc smart-sync [OPTIONS]
uv run ckc classify-missing [OPTIONS]  
uv run ckc scan-metadata [OPTIONS]
```

#### CLIオプション
```python
@cli.command("smart-sync")
@click.option("--auto-apply", is_flag=True, help="自動適用（確認なし）")
@click.option("--dry-run", is_flag=True, help="実行内容のプレビューのみ")
@click.option("--directory", default=".claude", help="対象ディレクトリ")
@click.option("--backup/--no-backup", default=True, help="バックアップ作成")
def smart_sync(auto_apply: bool, dry_run: bool, directory: str, backup: bool):
    """Intelligent batch classification and synchronization"""
```

### 2. 実装ファイル配置

#### 新規モジュール作成
```
src/claude_knowledge_catalyst/
├── cli/
│   ├── main.py              # 既存（コマンド追加）
│   └── smart_sync.py        # 新規（smart-sync実装）
├── core/
│   ├── batch_classifier.py  # 新規（バッチ分類ロジック）
│   └── metadata_scanner.py  # 新規（メタデータスキャン）
```

#### 既存モジュール活用
- `core/metadata.py` - MetadataManagerクラス
- `sync/hybrid_manager.py` - KnowledgeClassifierクラス
- `core/config.py` - 設定管理

### 3. カスタムスラッシュコマンド連携

#### スラッシュコマンド定義
```markdown
# .claude/commands/ckc-smart-sync.md
## 使用方法
```bash
# 基本実行
uv run ckc smart-sync

# 自動適用モード
uv run ckc smart-sync --auto-apply

# プレビューモード
uv run ckc smart-sync --dry-run
```

## 機能仕様

### Phase 1: メタデータスキャン
```python
def scan_metadata_status(directory: str) -> tuple[list[Path], list[Path]]:
    """
    Returns: (has_metadata_files, needs_classification_files)
    """
```

### Phase 2: バッチ分類
```python
def classify_files_batch(files: list[Path]) -> list[ClassificationResult]:
    """
    既存のKnowledgeClassifierを活用したバッチ分類
    """
```

### Phase 3: メタデータ適用
```python
def apply_metadata_batch(classifications: list[ClassificationResult], 
                        backup: bool = True) -> BatchResult:
    """
    安全なバッチメタデータ適用
    """
```

### Phase 4: CKC同期
```python
def run_sync_process() -> SyncResult:
    """
    既存の同期システムを活用
    """
```

## ユーザビリティ向上

### 1. 直感的なコマンド体系
```bash
# 現在（分離）
python .claude/commands/script.py
uv run ckc sync

# 提案（統合）
uv run ckc smart-sync
uv run ckc --help  # 全コマンド一覧表示
```

### 2. Claude Codeとの連携
```bash
# Claude Codeスラッシュコマンド
/ckc-smart-sync → uv run ckc smart-sync

# オプション付き実行も可能
/ckc-smart-sync-auto → uv run ckc smart-sync --auto-apply
```

### 3. 設定システム統合
```yaml
# ckc_config.yaml
smart_sync:
  auto_apply: false
  backup_enabled: true
  confidence_threshold: "medium"
  fallback_category: "concept"
```

## 実装優先度

### 高優先度（即座実装）
1. **core/batch_classifier.py** - バッチ分類ロジック
2. **cli/smart_sync.py** - CLIコマンド実装
3. **main.py統合** - コマンド登録

### 中優先度（次期版）
1. **設定システム拡張** - smart-sync用設定オプション
2. **テストスイート** - 包括的テストケース
3. **エラーハンドリング** - 堅牢な例外処理

### 低優先度（将来拡張）
1. **Web UI連携** - ブラウザからの実行
2. **スケジューラー統合** - 定期自動実行
3. **AI改善学習** - 分類精度の継続改善

## 期待される効果

### 開発者エクスペリエンス
- **統一されたCLI体験** - 一貫したコマンド構造
- **既存システム活用** - 車輪の再発明なし
- **保守性向上** - 単一コードベースでの管理

### ユーザーエクスペリエンス  
- **簡単アクセス** - `/ckc-smart-sync`で即座実行
- **柔軟な実行** - オプションによる細かい制御
- **統合ヘルプ** - `--help`での包括的ガイド

### システム品質
- **コード再利用** - 既存分類ロジックの活用
- **設定一元化** - ckc_config.yamlでの統合管理
- **テスト統合** - 既存テストスイートへの追加

## 実装ロードマップ

### Week 1: 基盤実装
- [ ] `core/batch_classifier.py`作成
- [ ] `cli/smart_sync.py`作成
- [ ] 基本的なCLIコマンド登録

### Week 2: 機能統合
- [ ] 既存MetadataManager統合
- [ ] KnowledgeClassifier連携
- [ ] エラーハンドリング実装

### Week 3: テスト・最適化
- [ ] 包括的テストケース
- [ ] パフォーマンス最適化
- [ ] ドキュメント更新

### Week 4: Claude Code連携
- [ ] スラッシュコマンド作成
- [ ] 使用方法ドキュメント
- [ ] ユーザーガイド更新

## 技術的考慮事項

### 依存関係管理
- 新規依存関係の最小化
- 既存Pydanticモデルの活用
- クリーンなインポート構造

### パフォーマンス
- 大量ファイル処理の最適化
- メモリ効率的なバッチ処理
- 進捗表示とユーザーフィードバック

### 拡張性
- プラグイン可能な分類ロジック
- 設定可能な分類ルール
- 将来的なAI統合の準備

この提案により、CKCは真に統合された知識管理プラットフォームとしての地位を確立し、開発者とユーザー双方の生産性を大幅に向上させることができます。