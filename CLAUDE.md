# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Knowledge Catalyst (CKC) is a comprehensive knowledge management system that automatically synchronizes Claude Code development insights with tools like Obsidian. It's built with Python 3.11+ and uses modern development practices.

## 開発環境・コマンド
詳細な開発環境設定、コマンド、ベストプラクティスについては:
> [🔧 開発環境ガイド](.claude/development.md)

## Project Architecture

> **詳細アーキテクチャドキュメント**: CKCの包括的な設計思想と実装詳細については、以下のドキュメントを参照してください：
> - [📋 アーキテクチャ概要](.claude/architecture/overview.md) - システム全体の設計思想とコンポーネント構成
> - [🏷️ メタデータシステム](.claude/architecture/metadata_system.md) - フロントマター、タグ、プロジェクト管理の詳細仕様
> - [💬 プロンプト管理システム](.claude/architecture/prompt_management.md) - プロンプト記録・分析・改善の包括システム
> - [🗂️ 分類・Obsidian統合](.claude/architecture/classification_obsidian.md) - ハイブリッド構造による知識分類とObsidian深層統合

### Core Components
- **core/config.py**: Configuration management with Pydantic models
- **core/metadata.py**: Automatic metadata extraction and enhancement
- **core/watcher.py**: File system monitoring with debouncing
- **sync/obsidian.py**: Obsidian vault integration and structured organization
- **templates/manager.py**: Template system for knowledge items
- **cli/main.py**: Command-line interface with Click and Rich

### Key Design Patterns
- **Pydantic models** for configuration and data validation
- **Plugin architecture** for extensible sync targets
- **Template-driven** content generation
- **Event-driven** file synchronization
- **Structured metadata** for intelligent organization

## Knowledge Management Features

### Obsidian Integration
- Automatic vault structure creation based on PARA method
- Enhanced frontmatter with rich metadata
- Intelligent file categorization and placement
- Cross-project knowledge linking

### Metadata Enhancement
- Auto-extraction from frontmatter and content
- Tag inference from content analysis
- Success rate tracking for prompts
- Version history management

### Template System
- Prompt development templates
- Code snippet documentation
- Concept explanation structure
- Project log and improvement tracking

