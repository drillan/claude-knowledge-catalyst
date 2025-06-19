# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Knowledge Catalyst (CKC) is a comprehensive knowledge management system that automatically synchronizes Claude Code development insights with tools like Obsidian. It's built with Python 3.11+ and uses modern development practices.

## 開発環境・コマンド
詳細な開発環境設定、コマンド、ベストプラクティスについては:
> [🔧 開発環境ガイド](.claude/development.md)

## Project Architecture

> **📋 包括的ドキュメント**: CKCの設計思想、使用方法、実装詳細については、以下の公式ドキュメントを参照してください：
> - [🚀 公式ドキュメント](https://claude-knowledge-catalyst.readthedocs.io/) - 完全なユーザーガイドと開発者リファレンス
> - [📖 Quick Start](https://claude-knowledge-catalyst.readthedocs.io/en/latest/quick-start/) - 5分で始める導入ガイド
> - [👥 User Guide](https://claude-knowledge-catalyst.readthedocs.io/en/latest/user-guide/) - 実践的な使用方法
> - [🔧 Developer Guide](https://claude-knowledge-catalyst.readthedocs.io/en/latest/developer-guide/) - 開発者向けリファレンス
> - [📋 API Reference](https://claude-knowledge-catalyst.readthedocs.io/en/latest/api-reference/) - 技術仕様

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

