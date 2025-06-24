# Developer Guide

Claude Knowledge Catalystの開発者向けガイドです。プロジェクトへの貢献、アーキテクチャの理解、開発環境のセットアップについて説明します。

## Contents

```{toctree}
:maxdepth: 2
:caption: Developer Resources
:hidden:

```

## Overview

CKCは次のython開発手法を採用しています。

### 技術スタック

- **Python 3.11+**: 現代的なPython機能を活用
- **Pydantic**: データ検証と設定管理
- **Typer + Rich**: 美しいCLIインターフェース
- **Watchdog**: ファイルシステム監視
- **Jinja2**: テンプレートエンジン
- **GitPython**: Git統合
- **pytest**: テストフレームワーク

### アーキテクチャの概要

```{mermaid}
graph TB
    CLI[CLI Interface] --> Core[Core System]
    Core --> Config[Configuration]
    Core --> Metadata[Metadata Processing]
    Core --> Watcher[File Watcher]
    Core --> ClaudeMD[CLAUDE.md Processor]

    Core --> Sync[Sync System]
    Sync --> Obsidian[Obsidian Integration]
    Sync --> Templates[Template System]

    Core --> Analytics[Analytics]
    Analytics --> AUTO[Automation Assistant]

    Watcher --> ClaudeMD
    ClaudeMD --> Metadata

    style CLI fill:#e1f5fe
    style Core fill:#f3e5f5
    style Sync fill:#e8f5e8
    style Analytics fill:#fff3e0
    style ClaudeMD fill:#ffecb3
```

## Quick Start for Developers

### 1. 開発環境のセットアップ

#### 前提条件

- **Python 3.11+**: [Pythonをダウンロード](https://www.python.org/downloads/)
- **uv**: [公式uvインストールガイド](https://docs.astral.sh/uv/getting-started/installation/)
- **Git**: バージョン管理用

#### セットアップ手順

```bash
# リポジトリをクローン
git clone https://github.com/drillan/claude-knowledge-catalyst.git
cd claude-knowledge-catalyst

# 仮想環境を作成
uv venv

# 仮想環境を有効化
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 開発依存関係をインストール
uv sync --dev

# pre-commitフックを設定
uv run pre-commit install
```

### 2. コードの品質チェック

```bash
# リンターを実行
uv run ruff check .

# フォーマッターを実行
uv run ruff format .

# 型チェックを実行
uv run mypy src/
```

### 3. テストの実行

```bash
# 全てのテストを実行
uv run pytest

# カバレッジ付きでテスト実行
uv run pytest --cov=claude_knowledge_catalyst
```

## コア設計原則

### 1. **Single Responsibility Principle**
各モジュールは単一の責任を持ち、明確に定義された役割を果たします。

### 2. **Dependency Injection**
設定と依存関係は外部から注入され、テスタビリティを向上させます。

### 3. **Event-Driven Architecture**
ファイルシステムの変更をイベントとして処理し、非同期で効率的な同期を実現します。

### 4. **Plugin Architecture**
新しい同期ターゲットやメタデータプロセッサーを容易に追加できる拡張可能な設計です。

## Development Workflow

### 1. **Feature Development**

```bash
# 新しいブランチを作成
git checkout -b feature/new-feature

# 開発を行う
# ... コードの変更 ...

# テストを実行
uv run pytest

# コミット
git add .
git commit -m "feat: add new feature"

# プッシュしてPRを作成
git push origin feature/new-feature
```

### 2. **Code Review Process**

- **自動チェック**: GitHub Actionsで自動的に実行
- **コードレビュー**: 少なくとも1人のレビューが必要
- **テストカバレッジ**: 新機能には適切なテストが必要
- **ドキュメント**: APIの変更には対応するドキュメント更新が必要

## Contributing Guidelines

### コーディング規約

```python
# Good: 明確な型アノテーション
def extract_metadata(file_path: Path) -> Dict[str, Any]:
    """ファイルからメタデータを抽出します。

    Args:
        file_path: 処理するファイルのパス

    Returns:
        抽出されたメタデータの辞書

    Raises:
        FileNotFoundError: ファイルが存在しない場合
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return {"title": "example", "tags": ["python"]}

# Good: Pydanticモデルの使用
class KnowledgeItem(BaseModel):
    """知識アイテムのデータモデル"""
    title: str = Field(..., description="アイテムのタイトル")
    content: str = Field(..., description="アイテムの内容")
    tags: List[str] = Field(default_factory=list, description="タグのリスト")
    created_at: datetime = Field(default_factory=datetime.now)
```

### テストの書き方

```python
import pytest
from claude_knowledge_catalyst.core.metadata import MetadataExtractor

class TestMetadataExtractor:
    """メタデータ抽出のテストクラス"""

    @pytest.fixture
    def extractor(self):
        """テスト用のメタデータ抽出器を作成"""
        return MetadataExtractor()

    def test_extract_from_markdown(self, extractor, tmp_path):
        """Markdownファイルからのメタデータ抽出をテスト"""
        # Arrange
        markdown_file = tmp_path / "test.md"
        markdown_file.write_text("""---
title: Test Document
tags: [test, example]
---

# Test Content
""")

        # Act
        result = extractor.extract_from_file(markdown_file)

        # Assert
        assert result["title"] == "Test Document"
        assert "test" in result["tags"]
        assert "example" in result["tags"]
```

## CLAUDE.md処理システムの実装

### 設計方針

CLAUDE.md同期機能は以下の設計方針に基づいて実装されています：

1. **セキュリティファースト**: デフォルトで無効化、明示的な有効化が必要
2. **柔軟なフィルタリング**: セクション単位での除外機能
3. **メタデータ強化**: CLAUDE.md専用の詳細メタデータ生成
4. **非破壊的処理**: 元ファイルは変更せず、フィルタリング後の内容を同期

### 実装アーキテクチャ

```{mermaid}
graph TD
    Config[WatchConfig] --> Watcher[KnowledgeWatcher]
    Watcher --> Handler[KnowledgeFileEventHandler]
    Handler --> Processor[ClaudeMdProcessor]

    Processor --> Filter[Section Filtering]
    Processor --> Meta[Metadata Generation]

    Filter --> Content[Filtered Content]
    Meta --> Enhanced[Enhanced Metadata]

    Content --> Sync[Obsidian Sync]
    Enhanced --> Sync

    style Config fill:#e3f2fd
    style Processor fill:#ffecb3
    style Filter fill:#f3e5f5
    style Meta fill:#e8f5e8
```

### 主要コンポーネント

#### 1. ClaudeMdProcessor

```python
class ClaudeMdProcessor:
    """CLAUDE.md専用プロセッサー"""

    def __init__(self, sections_exclude: list[str] | None = None):
        """除外セクションを指定して初期化"""
        self.sections_exclude = sections_exclude or []
        self.exclude_patterns = [
            re.compile(rf"^{re.escape(section.strip())}$", re.IGNORECASE)
            for section in self.sections_exclude
        ]

    def process_claude_md(self, file_path: Path) -> str:
        """CLAUDE.mdを処理してフィルタリング済み内容を返す"""
        # セクションフィルタリングロジック

    def get_metadata_for_claude_md(self, file_path: Path) -> dict[str, Any]:
        """CLAUDE.md専用メタデータを生成"""
        # メタデータ生成ロジック
```

#### 2. WatchConfig拡張

```python
class WatchConfig(BaseModel):
    """ファイル監視設定"""

    # 既存設定...

    # CLAUDE.md関連設定
    include_claude_md: bool = Field(
        default=False,
        description="CLAUDE.md同期の有効/無効"
    )
    claude_md_patterns: list[str] = Field(
        default=["CLAUDE.md", ".claude/CLAUDE.md"],
        description="同期対象ファイルパターン"
    )
    claude_md_sections_exclude: list[str] = Field(
        default=[],
        description="除外するセクションヘッダー"
    )
```

#### 3. ファイル監視統合

```python
class KnowledgeFileEventHandler(FileSystemEventHandler):
    """ファイルイベントハンドラー"""

    def __init__(self, watch_config: WatchConfig, ...):
        # CLAUDE.mdプロセッサーを初期化
        self.claude_md_processor = ClaudeMdProcessor(
            sections_exclude=watch_config.claude_md_sections_exclude
        )

    def _should_process_file(self, file_path: Path) -> bool:
        """ファイル処理対象判定"""
        # CLAUDE.mdパターンチェック
        if self.watch_config.include_claude_md:
            for pattern in self.watch_config.claude_md_patterns:
                if file_path.name == "CLAUDE.md" or file_path.match(pattern):
                    return True
        # 通常のファイルパターンチェック
        ...
```

### セキュリティ実装

#### 1. デフォルト無効化

```python
# 設定のデフォルト値で安全性を確保
include_claude_md: bool = Field(default=False)  # 明示的にFalse
```

#### 2. セクションフィルタリング

```python
def _filter_sections(self, content: str) -> str:
    """セクション単位でコンテンツをフィルタリング"""
    lines = content.split('\n')
    filtered_lines = []
    skip_section = False

    for line in lines:
        if line.strip().startswith('#'):
            # セクションヘッダー検出
            skip_section = self._should_exclude_section(line.strip())
            if not skip_section:
                filtered_lines.append(line)
        else:
            # セクション内容の処理
            if not skip_section:
                filtered_lines.append(line)

    return '\n'.join(filtered_lines)
```

#### 3. 大文字小文字非依存マッチング

```python
# 除外パターンの生成（大文字小文字無視）
self.exclude_patterns = [
    re.compile(rf"^{re.escape(section.strip())}$", re.IGNORECASE)
    for section in self.sections_exclude
]
```

### テスト戦略

#### 1. 単体テスト

```python
class TestClaudeMdProcessor:
    """CLAUDE.mdプロセッサーのテスト"""

    def test_section_filtering_case_insensitive(self):
        """大文字小文字を区別しないセクション除外"""
        processor = ClaudeMdProcessor(["# Secrets", "# Private"])
        # 大文字小文字の異なるセクションでテスト

    def test_empty_file_handling(self):
        """空ファイルの処理"""
        # 空のCLAUDE.mdファイルは同期されないことを確認

    def test_metadata_generation(self):
        """メタデータ生成のテスト"""
        # プロジェクト情報、セクション解析のテスト
```

#### 2. 統合テスト

```python
class TestCLAUDEMDIntegration:
    """CLAUDE.md機能の統合テスト"""

    def test_watch_integration(self):
        """ファイル監視との統合テスト"""
        # 実際のファイル変更をシミュレート

    def test_obsidian_sync_integration(self):
        """Obsidian同期との統合テスト"""
        # フィルタリングされたコンテンツが正しく同期されることを確認
```

### パフォーマンス考慮事項

#### 1. 遅延初期化

```python
# プロセッサーはファイル監視初期化時のみ作成
self.claude_md_processor = ClaudeMdProcessor(...)
```

#### 2. パターンマッチングの最適化

```python
# 事前コンパイルされた正規表現を使用
self.exclude_patterns = [re.compile(...) for ...]
```

#### 3. ファイルサイズ制限

```python
def should_sync_claude_md(self, file_path: Path) -> bool:
    """大きなファイルの同期を避ける"""
    if file_path.stat().st_size > MAX_FILE_SIZE:
        return False
```

## Next Steps

今後、以下のセクションを順次追加予定です：

- **Architecture** - 詳細なアーキテクチャ解説
- **Contributing** - 貢献ガイドライン
- **Development Setup** - 開発環境の詳細設定
- **Testing** - テスト戦略とベストプラクティス
- **API Development** - API開発ガイド
