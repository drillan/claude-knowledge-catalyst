# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Knowledge Catalyst (CKC) is a comprehensive knowledge management system that automatically synchronizes Claude Code development insights with tools like Obsidian. It's built with Python 3.11+ and uses modern development practices with uv package management.

## Essential Development Commands

### Package Management (uv required)
```bash
# Install dependencies and setup environment
uv sync --dev

# Run tests
uv run pytest
uv run pytest tests/test_specific.py  # Single test file
uv run pytest --cov                   # With coverage

# Code quality checks (run before commits)
uv run ruff check src/ tests/          # Lint code
uv run ruff format src/ tests/         # Format code  
uv run mypy src/                       # Type checking

# Run the CLI application
uv run ckc --help                      # Show help
uv run ckc init                        # Initialize project
uv run ckc sync                        # Sync content
```

### Building and Distribution
```bash
# Build package
uv build

# Install locally for testing
uv pip install -e .
```

## Development Environment Setup
- Python 3.11+ (managed by uv)
- Package manager: **uv** (required, not pip)
- Configuration file: `ckc_config.yaml`
- Main CLI entry: `src/claude_knowledge_catalyst/cli/main.py`

## Project Architecture

CKC implements a tag-centered knowledge management system with modular architecture:

### Core System Architecture
```
src/claude_knowledge_catalyst/
├── core/                    # Core system components
│   ├── config.py           # Pydantic-based configuration management
│   ├── metadata.py         # Metadata extraction and enhancement
│   ├── watcher.py          # File system monitoring with debouncing
│   └── tag_standards.py    # Tag validation and standards
├── cli/                     # Command-line interface
│   ├── main.py             # Main CLI entry (Typer-based)
│   ├── smart_sync.py       # Smart synchronization commands
│   └── interactive.py      # Interactive CLI features
├── sync/                    # Synchronization engines
│   ├── obsidian.py         # Obsidian vault integration
│   └── hybrid_manager.py   # Multi-target sync management
├── ai/                      # AI-powered features
│   ├── smart_classifier.py # Content classification
│   └── yake_extractor.py   # YAKE keyword extraction
├── templates/               # Template system
│   └── manager.py          # Template management
└── analytics/               # Analytics and reporting
    └── knowledge_analytics.py
```

### Key Design Patterns
- **Tag-Centered Architecture**: Multi-dimensional tagging instead of hierarchical categories
- **Pydantic Models**: Type-safe configuration and data validation
- **Plugin Architecture**: Extensible sync targets (Obsidian, future integrations)
- **Event-Driven Sync**: Real-time file monitoring and synchronization
- **AI-Enhanced Metadata**: Automated content classification and tagging
- **Template-Driven Content**: Consistent structure across knowledge items

### Configuration System
- **Primary Config**: `ckc_config.yaml` (Pydantic-validated)
- **Multi-dimensional Tags**: 7-layer tagging system (type, tech, domain, team, status, complexity, confidence)
- **Sync Targets**: Pluggable destination systems (currently Obsidian-focused)
- **Workflow States**: inbox → active → knowledge → archive progression

## Development Workflow

### Adding New Features
1. **Create feature branch**: Follow Git flow practices
2. **Update models**: Modify Pydantic models in `core/config.py` if needed
3. **Add CLI commands**: Extend `cli/main.py` using Typer patterns
4. **Implement core logic**: Add functionality to appropriate modules
5. **Write tests**: Add comprehensive tests in `tests/`
6. **Update documentation**: Modify docstrings and README as needed

### Testing Strategy
- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test sync operations and CLI workflows  
- **Mock external dependencies**: Use pytest fixtures for file systems
- **Coverage target**: Maintain reasonable test coverage (currently ~28%)

### Code Standards
- **Type hints**: Use throughout codebase (mypy enforced)
- **Pydantic models**: For all configuration and data structures
- **Async/await**: For I/O operations where applicable
- **Rich console**: For all CLI output and formatting
- **pathlib.Path**: For all file operations (not os.path)

