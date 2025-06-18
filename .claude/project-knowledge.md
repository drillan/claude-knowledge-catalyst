# Project Knowledge - 技術的洞察とパターン

## アーキテクチャの決定事項

### パッケージ管理：uvの採用理由
- **現代的なPython開発**: uvは次世代のPythonパッケージマネージャー
- **高速な依存関係解決**: pipよりも大幅に高速
- **プロジェクト分離**: 仮想環境の自動管理
- **ロックファイル**: `uv.lock`による再現可能なビルド

### Pydanticによる設定管理
```python
# core/config.py の設計パターン
class CKCConfig(BaseModel):
    version: str = "1.0"
    project_name: str
    auto_sync: bool = True
    sync_targets: List[SyncTarget] = []
    
    class Config:
        extra = "forbid"  # 未知のフィールドを拒否
        validate_assignment = True  # 代入時バリデーション
```

**利点**:
- 実行時型チェック
- 自動的なデータ変換
- 包括的なバリデーション
- IDE補完サポート

### ファイル監視システム（Watchdog）
```python
# core/watcher.py の実装パターン
class DebounceHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable, debounce_seconds: float = 1.0):
        self._callback = callback
        self._debounce_seconds = debounce_seconds
        self._timer: Optional[Timer] = None
```

**キーポイント**:
- デバウンス機能で過度な同期を防止
- 非同期処理による応答性向上
- 設定可能な監視パターン

## 実装パターン

### エラーハンドリング戦略
```python
# 一貫したエラーハンドリングパターン
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"操作失敗: {e}")
    raise CKCError(f"処理に失敗しました: {e}") from e
except Exception as e:
    logger.exception("予期しないエラー")
    raise CKCError("内部エラーが発生しました") from e
```

### メタデータ抽出ロジック
```python
# core/metadata.py の核となるパターン
def extract_metadata(content: str, file_path: Path) -> KnowledgeMetadata:
    """ファイルからメタデータを抽出"""
    frontmatter = extract_frontmatter(content)
    
    # フロントマターが存在しない場合の自動生成
    if not frontmatter:
        frontmatter = generate_default_metadata(file_path)
    
    # コンテンツ分析による強化
    enhanced_metadata = analyze_content_patterns(content)
    
    return merge_metadata(frontmatter, enhanced_metadata)
```

### Obsidian同期の設計
```python
# sync/obsidian.py の組織化ロジック
class ObsidianSyncManager:
    def organize_content(self, metadata: KnowledgeMetadata) -> Path:
        """PARAメソッドに基づくファイル配置"""
        if metadata.category == "prompt":
            return self.vault_path / "02_Knowledge_Base" / "Prompts"
        elif metadata.category == "code":
            return self.vault_path / "02_Knowledge_Base" / "Code_Snippets"
        # ... その他のカテゴリ
```

## CLI設計パターン

### Clickとの統合
```python
# cli/main.py のコマンド構造
@click.group()
@click.option('--verbose', '-v', is_flag=True)
@click.pass_context
def cli(ctx, verbose):
    """Claude Knowledge Catalyst CLI"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose

@cli.group()
def sync():
    """同期関連コマンド"""
    pass

@sync.command()
@click.argument('name')
@click.argument('type')
@click.argument('path', type=click.Path(exists=True))
def add(name, type, path):
    """同期ターゲットを追加"""
    # 実装...
```

### Richによる美しい出力
```python
from rich.console import Console
from rich.table import Table

console = Console()

def display_status():
    table = Table(title="CKC Status")
    table.add_column("項目", style="cyan")
    table.add_column("値", style="green")
    
    table.add_row("プロジェクト", config.project_name)
    table.add_row("同期ターゲット", str(len(config.sync_targets)))
    
    console.print(table)
```

## テスト戦略

### 単体テストパターン
```python
# tests/test_config.py
import pytest
from pathlib import Path
from claude_knowledge_catalyst.core.config import load_config

def test_load_valid_config(tmp_path):
    """有効な設定ファイルの読み込みテスト"""
    config_content = """
version: "1.0"
project_name: "テストプロジェクト"
auto_sync: true
"""
    config_path = tmp_path / "ckc_config.yaml"
    config_path.write_text(config_content)
    
    config = load_config(config_path)
    assert config.project_name == "テストプロジェクト"
    assert config.auto_sync is True
```

### モックの活用
```python
# 外部依存関係のモック化
@patch('claude_knowledge_catalyst.sync.obsidian.Path.exists')
def test_obsidian_sync_with_missing_vault(mock_exists):
    mock_exists.return_value = False
    
    with pytest.raises(CKCError, match="ボルトが存在しません"):
        sync_manager.sync_file(test_file)
```

## パフォーマンス最適化

### 効率的なファイル処理
```python
# 大きなファイルの効率的な処理
def process_large_file(file_path: Path) -> None:
    """メモリ効率的なファイル処理"""
    with file_path.open('r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if line_num > MAX_LINES:
                break
            process_line(line)
```

### 同期の最適化
- バッチ処理による効率化
- 変更検出による不要な同期の回避
- 並行処理による高速化

## セキュリティ考慮事項

### ファイルパス検証
```python
def validate_path(path: Path, base_path: Path) -> bool:
    """パストラバーサル攻撃の防止"""
    try:
        path.resolve().relative_to(base_path.resolve())
        return True
    except ValueError:
        return False
```

### 設定ファイルの検証
- YAML安全読み込み（`yaml.safe_load`）
- 入力サニタイゼーション
- 権限の最小化

## 知られている制限事項

### プラットフォーム固有の問題
- Windows: ファイルパスの長さ制限
- macOS: ファイル名の正規化問題
- Linux: inotifyの制限

### スケーラビリティの課題
- 大量ファイル監視時のメモリ使用量
- 同期処理の並行性制限
- メタデータインデックスサイズ

## 継続的改善のポイント

### コード品質
- 型ヒントの完全性向上
- テストカバレッジ90%以上維持
- ドキュメント文字列の充実

### 機能拡張
- プラグインアーキテクチャの実装
- WebAPI提供の検討
- AI支援機能の統合

### ユーザビリティ
- エラーメッセージの改善
- 設定ウィザードの提供
- 詳細なログ出力オプション