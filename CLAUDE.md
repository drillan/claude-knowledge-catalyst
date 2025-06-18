# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Knowledge Catalyst (CKC) is a comprehensive knowledge management system that automatically synchronizes Claude Code development insights with tools like Obsidian. It's built with Python 3.11+ and uses modern development practices.

## Development Environment

### Package Management
This project uses **uv** for modern Python package management. Always use uv commands for development:

```bash
# Install dependencies
uv sync --dev

# Run commands
uv run pytest
uv run ruff check src/ tests/
uv run ruff format src/ tests/
uv run mypy src/

# Add new dependencies
uv add package-name
uv add --dev dev-package-name
```

### Python Version
- **Required**: Python 3.11+
- **Specified in**: `.python-version` file
- **Use**: `uv python pin 3.11` to ensure correct version

## Development Commands

### Testing
```bash
uv run pytest                 # Run all tests
uv run pytest tests/test_config.py  # Run specific test file
uv run pytest --cov         # Run with coverage
```

### Code Quality
```bash
uv run ruff check src/ tests/   # Lint code (includes import sorting)
uv run ruff format src/ tests/  # Format code
uv run mypy src/                # Type checking
```

### Application Commands
```bash
uv run ckc init              # Initialize CKC in current directory
uv run ckc sync add vault obsidian /path/to/vault  # Add sync target
uv run ckc watch             # Start file watching
uv run ckc status            # Show current status
```

## Project Architecture

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

## Best Practices

### When Adding New Features
1. Use Pydantic models for data structures
2. Add comprehensive tests for new functionality
3. Update CLI commands if user-facing
4. Follow existing error handling patterns
5. Use type hints throughout

### Code Standards
- Follow PEP 8 with Ruff formatting and linting
- Use descriptive variable and function names
- Add docstrings for public APIs
- Implement proper error handling
- Use pathlib.Path for file operations

### Testing Requirements
- Unit tests for all core functionality
- Integration tests for sync operations
- Mock external dependencies appropriately
- Test error conditions and edge cases

## Configuration Management

### Files
- `ckc_config.yaml`: Main configuration file
- `pyproject.toml`: Project metadata and tool configuration
- `.python-version`: Python version specification

### Key Configuration Sections
- **sync_targets**: Knowledge management tool connections
- **tags**: Multi-dimensional tagging system
- **watch**: File monitoring settings
- **templates**: Template customization paths

## Common Development Tasks

### Adding a New Sync Target
1. Create new module in `sync/` directory
2. Implement sync manager class
3. Update configuration schema
4. Add CLI commands
5. Write comprehensive tests

### Extending Metadata System
1. Update KnowledgeMetadata model
2. Enhance extraction logic in MetadataManager
3. Update template system if needed
4. Add tests for new metadata fields

### Creating New Templates
1. Add template to TemplateManager
2. Create helper methods for template creation
3. Update CLI to support new template type
4. Document template structure

## Troubleshooting

### Common Issues
- **Import errors**: Check if using `uv run` prefix
- **Permission errors**: Ensure proper file permissions for sync targets
- **Configuration errors**: Validate YAML syntax in config files
- **Sync failures**: Check target paths and permissions

### Debug Mode
Use `--verbose` flag with CLI commands for detailed logging:
```bash
uv run ckc --verbose sync run
```