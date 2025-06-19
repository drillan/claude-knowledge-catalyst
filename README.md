# Claude Knowledge Catalyst (CKC) v0.9.1

**A comprehensive knowledge management system that catalyzes knowledge transformation**

Automatically structures insights from Claude Code development processes and integrates deeply with Obsidian to accumulate and utilize long-term knowledge assets.

> **[📋 日本語版](README-ja.md)** | **[🌐 Documentation](https://claude-knowledge-catalyst.readthedocs.io/)**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/claude-knowledge-catalyst.svg)](https://pypi.org/project/claude-knowledge-catalyst/)
[![PyPI downloads](https://img.shields.io/pypi/dm/claude-knowledge-catalyst.svg)](https://pypi.org/project/claude-knowledge-catalyst/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Documentation](https://img.shields.io/badge/docs-readthedocs-brightgreen.svg)](https://claude-knowledge-catalyst.readthedocs.io/)
[![Read the Docs](https://readthedocs.org/projects/claude-knowledge-catalyst/badge/?version=latest)](https://claude-knowledge-catalyst.readthedocs.io/en/latest/)

## Prerequisites

Before getting started with Claude Knowledge Catalyst, ensure you have the following:

- **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
- **uv**: Modern Python package manager and project manager
  - **Installation**: Follow the [official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)
  - **Quick install**: `curl -LsSf https://astral.sh/uv/install.sh | sh` (Unix/macOS) or `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows)

## Core Features

### 🔄 Automatic Synchronization System
- Real-time monitoring and sync of `.claude/` directory changes
- Seamless integration between `.claude` directory and Obsidian vault

### 🔒 Secure CLAUDE.md Sync
- Safe synchronization of CLAUDE.md files with section-level filtering
- Privacy-first design with sensitive information protection
- Configurable exclusion patterns for API keys, credentials, and personal data

### 🏷️ Intelligent Metadata Management
- Automatic project detection, tag inference, and context analysis
- Enhanced metadata generation for development context

### 📝 Template System
- Knowledge type-specific templates for prompts, code, concepts, and logs
- Structured content organization

### 🔍 Adaptive System Foundation
- 10-step numbering system for knowledge maturity visualization
- Progressive structuring: Chaos(00) → Projects(10) → Knowledge Base(20) → Wisdom Archive(30)
- Intelligent classification based on success rates, execution history, and content analysis

### 🎯 Deep Obsidian Integration
- Structured vault with bidirectional links and graph view utilization
- PARA method-based knowledge organization
- Cross-project knowledge discovery and cross-referencing

### ⚡ Comprehensive CLI
- Unified command-line for initialization, sync, monitoring, and analysis
- Rich console output with progress indicators

### 📊 Project Analytics
- File statistics, category distribution, and status management
- Cross-project knowledge linking and discovery

## 🎯 Try CKC in 3 Minutes

**Quick start with CKC:**

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install CKC
uv pip install claude-knowledge-catalyst

# Initialize in your project
cd your-project
uv run ckc init

# Add Obsidian vault
uv run ckc add my-vault /path/to/obsidian/vault

# Start syncing
uv run ckc sync
```

**What this does:**
- ✅ Sets up knowledge management structure
- ✅ Connects to your Obsidian vault
- ✅ Begins automatic content synchronization
- ✅ Enables intelligent metadata extraction

## Quick Start

### Setup Virtual Environment

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

### Installation

```bash
# Install from PyPI using uv pip (recommended)
uv pip install claude-knowledge-catalyst

# Or install with uv add (for Python projects)
uv add claude-knowledge-catalyst

# Or using pip
pip install claude-knowledge-catalyst

# Or install from source for development
git clone https://github.com/drillan/claude-knowledge-catalyst.git
cd claude-knowledge-catalyst
uv sync --dev
```

### Initialize in Your Project

```bash
# Navigate to your project directory
cd your-project

# Initialize CKC with hybrid structure
uv run ckc init

# Add Obsidian vault as sync target
uv run ckc add my-vault /path/to/your/obsidian/vault

# Start watching for changes
uv run ckc watch
```

### Enable CLAUDE.md Sync (Optional)

```bash
# Edit configuration file
vim ckc_config.yaml
```

Add to your configuration:
```yaml
watch:
  include_claude_md: true
  claude_md_sections_exclude:
    - "# secrets"
    - "# private"
    - "# confidential"
```

> **🔒 Security Note**: CLAUDE.md sync is disabled by default. Only enable it after configuring appropriate section exclusions for your sensitive information.

### Upgrade from Previous Versions

```bash
# Update to v0.9.1 (latest) using uv pip (recommended)
uv pip install --upgrade claude-knowledge-catalyst

# Or using uv add (for Python projects)
uv add claude-knowledge-catalyst@latest

# Or using pip
pip install --upgrade claude-knowledge-catalyst

# Verify everything works
uv run ckc status
```

### Sync Existing Knowledge

```bash
# Sync all files in .claude directory
uv run ckc sync

# Sync to specific target
uv run ckc sync --target my-vault

# Sync with project context
uv run ckc sync --project "My Project Name"
```

> **📚 Detailed Guide**: For more detailed setup and usage instructions, see the [official documentation](https://claude-knowledge-catalyst.readthedocs.io/) [Quick Start](https://claude-knowledge-catalyst.readthedocs.io/en/latest/quick-start/) and [Getting Started](https://claude-knowledge-catalyst.readthedocs.io/en/latest/getting-started/).

## Available CLI Commands

### 📁 Basic Operations

```bash
# Workspace initialization
uv run ckc init

# Add sync target
uv run ckc add main-vault ~/Documents/ObsidianVault

# File synchronization
uv run ckc sync
uv run ckc sync --target main-vault
uv run ckc sync --project "My Project"

# Real-time monitoring
uv run ckc watch

# Current status check
uv run ckc status
```

### 📊 Analysis & Project Management

```bash
# Detailed file analysis
uv run ckc analyze .claude/prompt-optimization.md

# List projects
uv run ckc project list

# List files in project
uv run ckc project files claude-knowledge-catalyst

# Project statistics
uv run ckc project stats claude-knowledge-catalyst
```

## Configuration

CKC uses a YAML configuration file (`ckc_config.yaml`) that supports:

- **Multiple sync targets**: Connect to various knowledge management tools
- **Custom tagging schemas**: Define your own categorization system  
- **Flexible watch patterns**: Configure which files and directories to monitor
- **Template customization**: Modify or add new content templates
- **CLAUDE.md sync settings**: Secure synchronization with section filtering

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

watch:
  include_claude_md: false  # Enable with caution
  claude_md_sections_exclude:
    - "# secrets"
    - "# private"
```

## Architecture

Claude Knowledge Catalyst implements a modern, extensible architecture:

- **Event-driven synchronization** with file system monitoring
- **Plugin architecture** for multiple knowledge management tools
- **Pydantic-based configuration** with validation
- **Template-driven content generation**
- **Intelligent metadata extraction and enhancement**

## Requirements

- **Python**: 3.11 or higher
- **Memory**: Minimum 512MB, Recommended 2GB for large vaults
- **Storage**: 10MB for CKC, varies based on vault size
- **OS**: Windows 10+, macOS 11+, Linux (Ubuntu 20.04+)

## Documentation

- **[📖 Documentation](https://claude-knowledge-catalyst.readthedocs.io/)** - Complete user guide and developer reference
- **[🚀 Quick Start](https://claude-knowledge-catalyst.readthedocs.io/en/latest/quick-start/)** - 5-minute introduction guide
- **[👥 User Guide](https://claude-knowledge-catalyst.readthedocs.io/en/latest/user-guide/)** - Practical usage methods
- **[🔧 Developer Guide](https://claude-knowledge-catalyst.readthedocs.io/en/latest/developer-guide/)** - Developer reference

## Support & Community

- **Issues**: [GitHub Issues](https://github.com/drillan/claude-knowledge-catalyst/issues)
- **Discussions**: [GitHub Discussions](https://github.com/drillan/claude-knowledge-catalyst/discussions)
- **Documentation**: [Read the Docs](https://claude-knowledge-catalyst.readthedocs.io/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please see our [Contributing Guide](https://claude-knowledge-catalyst.readthedocs.io/en/latest/developer-guide/) for details.

---

*Built with ❤️ by the Claude community*