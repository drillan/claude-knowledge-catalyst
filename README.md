# Claude Knowledge Catalyst (CKC) v0.10.0

**Claude Code ⇄ Obsidian Seamless Integration System**

Automatically synchronize insights from Claude Code development processes with Obsidian vaults for structured knowledge management. Automated analysis reduces manual classification overhead.

> **[📋 Japanese Version](README-ja.md)** | **[🌐 Documentation](https://claude-knowledge-catalyst.readthedocs.io/)**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/claude-knowledge-catalyst.svg)](https://pypi.org/project/claude-knowledge-catalyst/)
[![PyPI downloads](https://img.shields.io/pypi/dm/claude-knowledge-catalyst.svg)](https://pypi.org/project/claude-knowledge-catalyst/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Documentation](https://img.shields.io/badge/docs-readthedocs-brightgreen.svg)](https://claude-knowledge-catalyst.readthedocs.io/)

## 🎯 Claude Code ⇄ Obsidian Seamless Integration

### 🔄 Automatic Synchronization System
- **Real-time Sync**: Instantly reflect changes in `.claude/` directory to Obsidian vault
- **Bidirectional Integration**: Complete integration between Claude Code development and Obsidian knowledge management
- **Structured Organization**: Systematize knowledge using Obsidian's powerful features

### 🤖 Automated Metadata Enhancement with YAKE Integration
- **Advanced Keyword Extraction**: YAKE (Yet Another Keyword Extractor) for unsupervised keyword discovery
- **Multi-Language Support**: English, Japanese, Spanish, French, German, Italian, Portuguese
- **Smart Tagging**: AI-powered tag suggestions with confidence scoring
- **Evidence-Based Classification**: Reliable organization with clear rationale for automated decisions

```yaml
# Enhanced Metadata Example (Secondary Effect)
type: [prompt, code, concept, resource]           # Content nature
tech: [python, react, fastapi, kubernetes, ...]   # Technology stack
domain: [web-dev, ml, devops, mobile, ...]        # Application domain
team: [backend, frontend, ml-research, devops]    # Team ownership
status: [draft, tested, production, deprecated]   # Lifecycle state
complexity: [beginner, intermediate, advanced]    # Skill level
confidence: [low, medium, high]                   # Content reliability
```

### 🏛️ Obsidian-Optimized Vault Structure
```
obsidian-vault/
├── _system/          # Templates and configuration
├── _attachments/     # Media files
├── inbox/            # Unprocessed content
├── active/           # Work-in-progress content
├── archive/          # Completed/deprecated content
└── knowledge/        # Mature knowledge (main area)
```

## Prerequisites

- **uv**: Modern Python package manager (includes Python 3.11+ automatically)
  - **Installation**: Follow the [official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)
  - **Quick install**: `curl -LsSf https://astral.sh/uv/install.sh | sh` (Unix/macOS) or `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows)
- **Python**: Not required separately - uv manages Python 3.11+ automatically

## 🎯 3-Minute Claude Code ⇄ Obsidian Integration Experience

> **🚀 v0.10.0 YAKE Integration**: Advanced keyword extraction with 147 passing tests and 28.25% test coverage ensures production stability.

**Experience seamless integration:**

```bash
# Install CKC
uv pip install claude-knowledge-catalyst

# Initialize in Claude Code project
cd your-claude-project
uv run ckc init

# Connect to Obsidian vault
uv run ckc add my-vault /path/to/obsidian/vault

# Sync .claude/ files with Obsidian
uv run ckc sync
```

**What happens:**
- ✅ **Seamless Integration**: Complete integration between Claude Code development and Obsidian knowledge management
- ✅ **Automatic Structuring**: Organize `.claude/` content with Obsidian-optimized structure
- ✅ **Enhanced Metadata**: Automatic tagging that reduces manual classification
- ✅ **Real-time Sync**: Instantly reflect knowledge accumulation during development process

## Core Features

### 🔄 Claude Code ⇄ Obsidian Complete Integration
- **Seamless Sync**: Automatic bidirectional sync between `.claude/` directory and Obsidian vault
- **Structured Migration**: Optimization and structural enhancement of existing Obsidian vaults
- **Dynamic Query Generation**: Automatic generation of Obsidian dataview queries
- **Knowledge Discovery**: Cross-project search of Claude Code development insights within Obsidian

### 🚀 YAKE Keyword Extraction (New in v0.10.0)
- **Unsupervised Learning**: Extract keywords without training data
- **Multi-Language**: Automatic language detection and processing
- **Confidence Scoring**: Filter high-quality keyword suggestions
- **Technical Content**: Optimized for technical documentation and code

### 🔒 Secure CLAUDE.md Sync
- **Privacy-First**: Section-level filtering for sensitive information
- **Configurable Exclusion**: Protect API keys, credentials, personal data
- **Safe by Default**: CLAUDE.md sync disabled unless explicitly enabled

### 📊 Obsidian Integrated Analytics
- **Knowledge Usage Tracking**: Analyze knowledge utilization patterns in Claude Code development
- **Prompt Effectiveness Measurement**: Success rates and improvement suggestions within Obsidian
- **Cross-Project Insights**: Discover relationships between development insights
- **Team Knowledge Sharing**: Collaborative knowledge management through Obsidian

### 🎨 Obsidian-Optimized Templates
- **Claude Code Specialized**: Obsidian templates for prompts, code, concepts, and resources
- **Smart Suggestions**: Automatic template selection based on development context
- **Evolving Structure**: Obsidian vault optimization according to project growth

## Quick Start

### Installation

```bash
# Install from PyPI using uv (recommended)
uv pip install claude-knowledge-catalyst

# Or using pip
pip install claude-knowledge-catalyst

# Or install from source for development
git clone https://github.com/drillan/claude-knowledge-catalyst.git
cd claude-knowledge-catalyst
uv sync --dev
```

### Claude Code Project Integration

```bash
# Navigate to Claude Code project
cd your-claude-project

# Initialize CKC (detects .claude/ directory)
uv run ckc init

# Connect to Obsidian vault
uv run ckc add main-vault /path/to/your/obsidian/vault

# Experience automatic analysis of .claude/ content
echo "# Git Useful Commands

## Branch Status Check
\`\`\`bash
git branch -vv
git status --porcelain
\`\`\`" > .claude/git_tips.md

# Verify automated analysis and Obsidian metadata generation
uv run ckc classify .claude/git_tips.md --show-evidence
```

### Existing Obsidian Vault Enhancement

```bash
# Enhance existing Obsidian vault for Claude Code integration
uv run ckc migrate --source /existing/obsidian --target /enhanced/vault

# Preview changes
uv run ckc migrate --source /existing/obsidian --target /enhanced/vault --dry-run
```

## Available CLI Commands

### 🚀 Automated Classification

```bash
# Automatic content analysis
uv run ckc classify file.md --show-evidence

# Batch classification
uv run ckc batch-classify .claude/

# Missing metadata detection
uv run ckc scan-missing-metadata
```

### 📁 Core Operations

```bash
# Zero-config initialization
uv run ckc init

# Vault connection
uv run ckc add vault-name /path/to/obsidian

# State-based synchronization
uv run ckc sync
uv run ckc sync --project "My Project"

# Real-time monitoring
uv run ckc watch

# System status
uv run ckc status
```

### 📊 Advanced Analytics

```bash
# File analysis with evidence
uv run ckc analyze .claude/my-prompt.md

# Cross-dimensional search
uv run ckc search --tech python --status production
uv run ckc search --team frontend --complexity advanced

# Project insights
uv run ckc project stats my-project
```

## Configuration

CKC uses a YAML configuration file with pure tag-centered settings:

```yaml
version: "1.0"
project_name: "My AI Project"
auto_sync: true

# Tag-centered architecture
tag_system:
  enabled: true
  multi_dimensional: true
  auto_classification: true
  confidence_threshold: 0.75

# 7-dimensional tag schema
tags:
  type_tags: ["prompt", "code", "concept", "resource"]
  tech_tags: ["python", "javascript", "react", "fastapi"]
  domain_tags: ["web-dev", "machine-learning", "devops"]
  team_tags: ["backend", "frontend", "ml-research"]
  status_tags: ["draft", "tested", "production", "deprecated"]
  complexity_tags: ["beginner", "intermediate", "advanced"]
  confidence_tags: ["low", "medium", "high"]

# Obsidian integration
sync_targets:
  - name: "main-vault"
    type: "obsidian"
    path: "/Users/me/Documents/ObsidianVault"
    enabled: true
    enhance_metadata: true

# Automated features
automation:
  auto_classification: true
  evidence_tracking: true
  natural_language_search: true

# State-based workflow
workflow:
  inbox_pattern: "status:draft"
  active_pattern: "status:tested"
  knowledge_pattern: "status:production"
  archive_pattern: "status:deprecated"

# Security settings
watch:
  include_claude_md: false  # Enable with caution
  claude_md_sections_exclude:
    - "# secrets"
    - "# private"
    - "# api-keys"
```

## Architecture

CKC implements a revolutionary pure tag-centered architecture:

- **Cognitive Load Zero**: Eliminates category decision fatigue
- **7-Dimensional Classification**: Multi-layer tag system for precise organization
- **Automated Intelligence**: Pattern-matching content understanding
- **State-Based Workflow**: Organization by lifecycle, not content type
- **Dynamic Discovery**: Cross-dimensional knowledge search
- **Obsidian Enhancement**: Transform basic vaults → intelligent systems

## Pure Tag-Centered vs Traditional

### ❌ Traditional Category-Based Problems
```
├── prompts/          # "Is this a prompt or template?"
├── code/             # "Code snippet or tool?"
├── concepts/         # "Concept or best practice?"
└── misc/             # Catch-all confusion
```

**Issues:**
- Decision fatigue: Which category?
- Rigid boundaries: Content doesn't fit neatly
- Poor discoverability: Single-dimension search
- Maintenance overhead: Moving files between categories

### ✅ Pure Tag-Centered Solution
```
├── _system/          # System files and templates
├── inbox/            # Unprocessed items (workflow state)
├── active/           # Currently working (activity state)
├── archive/          # Deprecated/old (lifecycle state)
└── knowledge/        # Mature content (90% of files)
    └── Dynamic discovery through enhanced multi-layer tags
```

**Benefits:**
- 🧠 **Cognitive Load Reduction**: No "which category?" decisions
- 🔍 **Multi-Dimensional Discovery**: Search across tech, domain, team
- 📈 **Scalable Organization**: Tags evolve with your knowledge
- ⚡ **Flexible Workflow**: State-based, not content-based organization
- 🔗 **Rich Relationships**: Multi-project, multi-domain connections

## Documentation

- **[📖 Documentation](https://claude-knowledge-catalyst.readthedocs.io/)** - Complete user guide and developer reference
- **[🚀 Quick Start](https://claude-knowledge-catalyst.readthedocs.io/en/latest/quick-start/)** - 5-minute Pure Tag-Centered experience
- **[👥 User Guide](https://claude-knowledge-catalyst.readthedocs.io/en/latest/user-guide/)** - Practical usage methods
- **[🔧 Developer Guide](https://claude-knowledge-catalyst.readthedocs.io/en/latest/developer-guide/)** - Developer reference

## Try the Revolution

**Demo the cognitive transformation:**

```bash
# Experience tag-centered migration
./demo/tag_centered_demo.sh

# Try automated classification  
./demo/demo.sh

# Multi-team collaboration
./demo/multi_project_demo.sh
```

## Requirements

- **Python Runtime**: 3.11+ (managed automatically by uv)
- **Package Manager**: uv (handles Python installation and dependency management)
- **Memory**: Minimum 512MB, Recommended 2GB for large vaults
- **Storage**: 10MB for CKC, varies based on vault size
- **OS**: Windows 10+, macOS 11+, Linux (Ubuntu 20.04+)

## Support & Community

- **Issues**: [GitHub Issues](https://github.com/drillan/claude-knowledge-catalyst/issues)
- **Discussions**: [GitHub Discussions](https://github.com/drillan/claude-knowledge-catalyst/discussions)
- **Documentation**: [Read the Docs](https://claude-knowledge-catalyst.readthedocs.io/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please see our [Contributing Guide](https://claude-knowledge-catalyst.readthedocs.io/en/latest/developer-guide/) for details.

---

**Welcome to the cognitive revolution!**  
*No more "which category?" decisions - experience pure, discoverable knowledge management.*

*Built with ❤️ by the Claude community*