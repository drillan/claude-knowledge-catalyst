# Claude Knowledge Catalyst (CKC) v2.0

A comprehensive knowledge management system that automatically synchronizes your Claude Code development insights with advanced analytics, AI assistance, and intelligent organization.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](RELEASE_NOTES.md)

## ✨ What's New in v2.0

### 🏗️ Hybrid Structure System
- **10-step numbering** (00, 10, 20, 30) for flexible directory organization
- **Three-tier classification**: System directories (_), Core workflow (numbered), Auxiliary (unnumbered)
- **Backward compatibility** with existing CKC v1.0 vaults
- **Intelligent content classification** and auto-placement

### 📊 Advanced Analytics & Insights
- **Comprehensive knowledge analytics** with visualization support
- **Usage statistics and productivity metrics**
- **Knowledge evolution tracking** and trend analysis
- **Performance monitoring** and optimization recommendations

### 🤖 AI-Powered Assistance
- **Content improvement suggestions** with priority-based recommendations
- **Intelligent template generation** for 6 content types
- **Enhanced metadata analysis** with complexity and quality assessment
- **Smart tagging and categorization** recommendations

### ⚙️ Automation & Maintenance
- **Automated structure maintenance** with issue detection and auto-fixing
- **Metadata consistency checking** and enhancement
- **Health monitoring** with trend analysis
- **Scheduled maintenance** tasks

## Core Features

- **🔄 Automatic Synchronization**: Watch `.claude/` directories and sync changes in real-time
- **🏷️ Intelligent Metadata Management**: Auto-extract and enhance metadata with advanced AI analysis
- **📝 Rich Template System**: AI-generated templates for prompts, code snippets, concepts, and project logs
- **🔍 Advanced Organization**: Multi-dimensional tagging and hybrid structure for optimal discovery
- **⚡ Enhanced CLI Interface**: Comprehensive command-line tools with analytics, AI, and automation features
- **🎯 Obsidian Integration**: Deep integration with structured vault organization and intelligent linking
- **📊 Success Tracking**: Advanced analytics for prompt effectiveness and knowledge evolution
- **🔗 Project Correlation**: Cross-project knowledge linking with relationship mapping

## 🎯 Try CKC in 3 Minutes

**Want to see CKC in action before installing?** Run our interactive demo:

```bash
# Clone and run the demo
git clone https://github.com/driller/claude-knowledge-catalyst.git
cd claude-knowledge-catalyst
uv sync --dev

# Run main demo (recommended)
./demo/run_demo.sh user

# Or run directly
./demo/demo.sh

# Or explore other demos
./demo/run_demo.sh help
```

**What the demo shows:**
- ✅ Real user workflow with actual commands
- ✅ Automatic content classification and organization
- ✅ Obsidian vault generation with hybrid structure
- ✅ Multi-project knowledge sharing capabilities

[📖 Full demo documentation](demo/README.md)

## Quick Start

### Installation

```bash
# Install from source using uv (recommended)
git clone https://github.com/driller/claude-knowledge-catalyst.git
cd claude-knowledge-catalyst

# Initialize with uv
uv venv
uv sync --dev

# Or install with pip
pip install -e .
```

### Initialize in Your Project

```bash
# Navigate to your project directory
cd your-project

# Initialize CKC with hybrid structure (v2.0)
uv run ckc init --structure hybrid

# Add Obsidian vault as sync target
uv run ckc sync add my-vault obsidian /path/to/your/obsidian/vault

# Start watching for changes
uv run ckc watch

# Generate analytics report
uv run ckc analytics report --days 30

# Get AI suggestions for a file
uv run ckc ai suggest myfile.md

# Run automated maintenance
uv run ckc maintenance
```

### Upgrade from CKC v1.0

```bash
# Update to v2.0
uv add claude-knowledge-catalyst@2.0.0

# Migrate to hybrid structure
uv run ckc migrate --to hybrid

# Verify everything works
uv run ckc status
uv run ckc structure validate
```

### Sync Existing Knowledge

```bash
# Sync all files in .claude directory
uv run ckc sync run

# Sync to specific target
uv run ckc sync run --target my-vault

# Sync with project context
uv run ckc sync run --project "My Project Name"
```

## New CLI Commands (v2.0)

### Analytics & Insights

```bash
# Generate comprehensive analytics report
uv run ckc analytics report --days 30 --output report.json

# Show usage statistics
uv run ckc analytics usage --days 7

# View productivity metrics
uv run ckc analytics report | grep productivity
```

### AI Assistance

```bash
# Get content improvement suggestions
uv run ckc ai suggest .claude/prompt-optimization.md

# Generate intelligent templates
uv run ckc ai template prompt --title "API Integration"
uv run ckc ai template code --language python
uv run ckc ai template concept --title "Design Patterns"

# Get AI insights about content
uv run ckc ai insights .claude/my-prompt.md

# Get knowledge organization suggestions
uv run ckc ai organize
```

### Structure Management

```bash
# Check structure status
uv run ckc structure status

# Validate structure integrity
uv run ckc structure validate

# Configure structure settings
uv run ckc structure configure
```

### Migration & Maintenance

```bash
# Migrate to hybrid structure
uv run ckc migrate --to hybrid

# Show migration plan
uv run ckc migrate plan

# Run automated maintenance
uv run ckc maintenance

# Force maintenance regardless of schedule
uv run ckc maintenance --force
```

### Traditional Commands

```bash
# Analyze metadata and content
uv run ckc analyze .claude/prompt-optimization.md

# List all sync targets
uv run ckc sync list

# Add a new target
uv run ckc sync add notes-vault obsidian ~/Documents/Notes

# View current status
uv run ckc status
```

## Configuration

CKC uses a YAML configuration file (`ckc_config.yaml`) that supports:

- **Multiple sync targets**: Connect to various knowledge management tools
- **Custom tagging schemas**: Define your own categorization system  
- **Flexible watch patterns**: Configure which files and directories to monitor
- **Template customization**: Modify or add new content templates

Example configuration:

```yaml
version: "1.0"
project_name: "My AI Project"
auto_sync: true

sync_targets:
  - name: "main-vault"
    type: "obsidian" 
    path: "/Users/me/Documents/ObsidianVault"
    enabled: true

tags:
  category_tags: ["prompt", "code", "concept", "resource"]
  tech_tags: ["python", "javascript", "react"]
  claude_tags: ["opus", "sonnet", "haiku"]
  status_tags: ["draft", "tested", "production"]

watch:
  watch_paths: [".claude"]
  file_patterns: ["*.md", "*.txt"]
  debounce_seconds: 1.0
```

## Knowledge Organization

CKC automatically organizes your knowledge into a structured system inspired by the PARA method:

```
Obsidian_Vault/
├── 00_Inbox/                    # Unprocessed items
├── 01_Projects/                 # Project-specific knowledge
│   ├── ProjectA/learnings/
│   └── ProjectB/learnings/
├── 02_Knowledge_Base/           # Shared knowledge
│   ├── Prompts/
│   │   ├── Templates/           # Reusable prompt templates
│   │   ├── Best_Practices/      # High-success prompts
│   │   └── Improvement_Log/     # Prompt evolution tracking
│   ├── Code_Snippets/
│   │   ├── Python/
│   │   ├── JavaScript/
│   │   └── Other_Languages/
│   ├── Concepts/                # AI/LLM concepts and learnings
│   └── Resources/               # External references
├── 03_Templates/                # Note templates
├── 04_Analytics/                # Usage and effectiveness metrics
└── 05_Archive/                  # Deprecated knowledge
```

## Advanced Features

### Metadata Enhancement

Every knowledge item is automatically enhanced with rich metadata:

```yaml
---
title: "Python Async Code Generation"
created: "2024-06-17T10:30:00"
updated: "2024-06-17T15:45:00"
version: "1.2"
claude_model: "Claude 3 Opus"
category: "prompt"
status: "production"
success_rate: 87
confidence: "high"
purpose: "Generate async Python code with proper error handling"
tags: [prompt, python, async, code-generation]
related_projects: ["web-scraper", "api-service"]
---
```

### Template System

Built-in templates for common knowledge types:

- **Prompt Templates**: Structure for prompt development and iteration
- **Code Snippets**: Reusable code with documentation
- **Concept Notes**: AI/LLM concepts and explanations
- **Project Logs**: Development session recordings
- **Improvement Logs**: Tracking prompt and process improvements

### Success Tracking

Track the effectiveness of your prompts and techniques:

- Success rate monitoring
- Version comparison
- Improvement trends
- Best practice identification

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/driller/claude-knowledge-catalyst.git
cd claude-knowledge-catalyst

# Install development dependencies with uv
uv sync --dev

# Install pre-commit hooks
uv run pre-commit install

# Run tests
uv run pytest

# Run linting and formatting
uv run ruff check src/ tests/     # Lint
uv run ruff format src/ tests/    # Format
uv run mypy src/                  # Type checking
```

### Project Structure

```
src/claude_knowledge_catalyst/
├── core/                   # Core functionality
│   ├── config.py          # Configuration management
│   ├── metadata.py        # Metadata extraction and management
│   └── watcher.py         # File system monitoring
├── sync/                  # Synchronization modules
│   └── obsidian.py        # Obsidian integration
├── templates/             # Template system
│   └── manager.py         # Template management
└── cli/                   # Command-line interface
    └── main.py            # CLI implementation
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 [Documentation](https://github.com/driller/claude-knowledge-catalyst/wiki)
- 🐛 [Issue Tracker](https://github.com/driller/claude-knowledge-catalyst/issues)
- 💬 [Discussions](https://github.com/driller/claude-knowledge-catalyst/discussions)

## Roadmap

- [ ] **Web Interface**: Browser-based management dashboard
- [ ] **Notion Integration**: Support for Notion as sync target
- [ ] **AI-Powered Insights**: Automated knowledge analysis and suggestions
- [ ] **Team Collaboration**: Multi-user knowledge sharing features
- [ ] **Advanced Analytics**: Detailed effectiveness metrics and reporting
- [ ] **Plugin System**: Extensible architecture for custom integrations

---

**Claude Knowledge Catalyst** - Transform your AI development insights into organized, searchable, and reusable knowledge assets.
