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
    
    Core --> Sync[Sync System]
    Sync --> Obsidian[Obsidian Integration]
    Sync --> Templates[Template System]
    
    Core --> Analytics[Analytics]
    Analytics --> AI[AI Assistant]
    
    style CLI fill:#e1f5fe
    style Core fill:#f3e5f5
    style Sync fill:#e8f5e8
    style Analytics fill:#fff3e0
```

## Quick Start for Developers

### 1. 開発環境のセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/drillan/claude-knowledge-catalyst.git
cd claude-knowledge-catalyst

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

## Next Steps

今後、以下のセクションを順次追加予定です：

- **Architecture** - 詳細なアーキテクチャ解説
- **Contributing** - 貢献ガイドライン  
- **Development Setup** - 開発環境の詳細設定
- **Testing** - テスト戦略とベストプラクティス
- **API Development** - API開発ガイド