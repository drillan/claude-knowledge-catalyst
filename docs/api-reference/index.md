# API Reference

Claude Knowledge Catalystの包括的なAPIリファレンスです。

## Overview

このAPIリファレンスでは、CKCの全てのモジュール、クラス、関数の詳細な仕様を提供します。

## Modules

```{toctree}
:maxdepth: 2
:hidden:

configuration
```

## Core Modules

### Configuration Management
- [Configuration Reference](configuration.md) - 完全な設定リファレンス
- `core.config` - 設定管理とPydanticモデル
- `core.hybrid_config` - ハイブリッド設定システム
- `core.claude_md_processor` - CLAUDE.md処理システム

### Metadata Processing
- `core.metadata` - メタデータ抽出と強化
- `core.watcher` - ファイルシステム監視

### Data Structures
- `core.structure_validator` - データ構造検証

## Synchronization System

### Obsidian Integration
- `sync.obsidian` - Obsidianボルト統合
- `sync.hybrid_manager` - ハイブリッド同期管理
- `sync.compatibility` - 互換性管理

## Template System

### Template Management
- `templates.manager` - テンプレート管理システム
- `templates.hybrid_templates` - ハイブリッドテンプレート

## Command Line Interface

### CLI Commands
- `cli.main` - メインCLIインターフェース
- `cli.migrate_commands` - 移行コマンド
- `cli.structure_commands` - 構造管理コマンド

## Analytics & Automation

### Knowledge Analytics
- `analytics.knowledge_analytics` - 知識分析システム
- `analytics.usage_statistics` - 使用統計

### Automation Tools
- `automation.metadata_enhancer` - メタデータ自動強化
- `automation.structure_automation` - 構造自動化

## Automation Integration

### Automation Assistant
- `automation.assistant` - 自動化統合インターフェース

## Auto-Generated API Documentation

以下は、Pythonコードのdocstringから自動生成されるAPIドキュメントです：

```{eval-rst}
.. automodule:: claude_knowledge_catalyst
   :members:
   :undoc-members:
   :show-inheritance:
```

## Usage Examples

### Basic Configuration

```python
from claude_knowledge_catalyst.core.config import CKCConfig

# 設定の読み込み
config = CKCConfig.load_from_file("config.yaml")

# 設定の検証
if config.validate():
    print("設定は有効です")
```

### Metadata Extraction

```python
from claude_knowledge_catalyst.core.metadata import MetadataExtractor

# メタデータ抽出器の初期化
extractor = MetadataExtractor()

# ファイルからメタデータを抽出
metadata = extractor.extract_from_file("example.md")
print(f"抽出されたタグ: {metadata.tags}")
```

### Obsidian Synchronization

```python
from claude_knowledge_catalyst.sync.obsidian import ObsidianSync

# Obsidian同期の初期化
sync = ObsidianSync(vault_path="~/Documents/MyVault")

# 同期の実行
sync.sync_all()
```

## Type Definitions

CKCで使用される主要な型定義：

```python
from typing import Dict, List, Optional, Union
from pydantic import BaseModel

class KnowledgeItem(BaseModel):
    """知識アイテムの基本構造"""
    title: str
    content: str
    tags: List[str]
    maturity_level: int
    project: Optional[str] = None
    success_rate: Optional[float] = None

class ProjectMetadata(BaseModel):
    """プロジェクトメタデータ"""
    name: str
    description: str
    technologies: List[str]
    status: str
```

## Error Handling

CKCのエラーハンドリングパターン：

```python
from claude_knowledge_catalyst.core.exceptions import (
    CKCError,
    ConfigurationError,
    SyncError,
    ValidationError
)

try:
    # CKC操作
    result = some_ckc_operation()
except ConfigurationError as e:
    print(f"設定エラー: {e}")
except SyncError as e:
    print(f"同期エラー: {e}")
except CKCError as e:
    print(f"CKCエラー: {e}")
```

## Logging

CKCのログ設定：

```python
import logging
from claude_knowledge_catalyst.core.logging import setup_logging

# ログ設定の初期化
setup_logging(level=logging.INFO)

# ログの使用
logger = logging.getLogger(__name__)
logger.info("CKC操作を開始します")
```
