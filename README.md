# Claude Knowledge Catalyst (CKC)

A comprehensive knowledge management system that automatically synchronizes your Claude Code development insights with tools like Obsidian, enabling seamless organization, search, and reuse of your AI-assisted development knowledge.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Features

- **🔄 Automatic Synchronization**: Watch `.claude/` directories and sync changes in real-time
- **🏷️ Intelligent Metadata Management**: Auto-extract and enhance metadata with tags, categories, and success metrics
- **📝 Rich Template System**: Pre-built templates for prompts, code snippets, concepts, and project logs
- **🔍 Advanced Organization**: Multi-dimensional tagging system for easy discovery and categorization
- **⚡ CLI Interface**: Powerful command-line tools for setup, management, and monitoring
- **🎯 Obsidian Integration**: Deep integration with Obsidian vaults including proper directory structure and linking
- **📊 Success Tracking**: Track prompt effectiveness and improvement over time
- **🔗 Project Correlation**: Link knowledge items across projects for better insights

## Quick Start

### Installation

```bash
# Install from source
git clone https://github.com/driller/claude-knowledge-catalyst.git
cd claude-knowledge-catalyst
pip install -e .
```

### Initialize in Your Project

```bash
# Navigate to your project directory
cd your-project

# Initialize CKC
ckc init

# Add Obsidian vault as sync target
ckc sync add my-vault obsidian /path/to/your/obsidian/vault

# Start watching for changes
ckc watch
```

### Sync Existing Knowledge

```bash
# Sync all files in .claude directory
ckc sync run

# Sync to specific target
ckc sync run --target my-vault

# Sync with project context
ckc sync run --project "My Project Name"
```

## Usage Examples

### Analyzing a Knowledge File

```bash
# Analyze metadata and content
ckc analyze .claude/prompt-optimization.md
```

### Managing Sync Targets

```bash
# List all sync targets
ckc sync list

# Add a new target
ckc sync add notes-vault obsidian ~/Documents/Notes

# Remove a target
ckc sync remove old-vault
```

### Checking System Status

```bash
# View current configuration and status
ckc status
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

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linting
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
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
