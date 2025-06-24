# Contributing to Claude Knowledge Catalyst

Thank you for your interest in contributing to Claude Knowledge Catalyst (CKC)! This guide will help you get started with contributing to the project.

## Table of Contents

- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Code Quality Standards](#code-quality-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Project-Specific Guidelines](#project-specific-guidelines)
- [Getting Help](#getting-help)

## Development Setup

### Prerequisites

- **Python 3.11+** (required)
- **uv** package manager (required)
- **Git** for version control

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/drillan/claude-knowledge-catalyst.git
   cd claude-knowledge-catalyst
   ```

2. **Install uv** (if not already installed):
   ```bash
   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Set up the development environment:**
   ```bash
   # Install dependencies and create virtual environment
   uv sync --dev

   # Install pre-commit hooks
   uv run pre-commit install
   ```

4. **Verify the setup:**
   ```bash
   # Run tests
   uv run pytest

   # Check code quality
   uv run ruff check src/ tests/
   uv run mypy src/

   # Test CLI functionality
   uv run ckc --help
   ```

## Development Workflow

### Branch Strategy

- **Main branch**: `main` - stable, production-ready code
- **Feature branches**: `feature/description` or `fix/description`
- **Development**: Always branch from `main`

### Creating a Feature Branch

```bash
# Create and switch to a new feature branch
git checkout -b feature/your-feature-name main

# Make your changes
# ... your development work ...

# Push your branch
git push origin feature/your-feature-name
```

### Daily Development Commands

```bash
# Run development checks (recommended before each commit)
uv run ruff check src/ tests/          # Lint code
uv run ruff format src/ tests/         # Format code
uv run mypy src/                       # Type checking
uv run pytest                         # Run tests

# Run all pre-commit hooks manually
uv run pre-commit run --all-files
```

## Code Quality Standards

### Automated Quality Checks

All code must pass these automated checks:

1. **Ruff Linting**: Code must pass `ruff check` without errors
2. **Ruff Formatting**: Code must be formatted with `ruff format`
3. **MyPy Type Checking**: All source files must pass type checking
4. **Tests**: All tests must pass with reasonable coverage
5. **Pre-commit Hooks**: All hooks must pass

### Code Style Guidelines

- **Type Hints**: Use type hints throughout the codebase
- **Pydantic Models**: Use for all configuration and data structures
- **pathlib.Path**: Use instead of `os.path` for file operations
- **Rich Console**: Use for all CLI output and formatting
- **Async/Await**: Use for I/O operations where applicable

### Documentation

- **Docstrings**: Use for all public functions and classes
- **Comments**: Explain complex logic and business decisions
- **README Updates**: Update if your changes affect usage
- **Type Documentation**: Keep type hints comprehensive

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_specific.py

# Run with verbose output
uv run pytest -v --tb=short
```

### Test Guidelines

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test interactions between components
- **Mock External Dependencies**: Use pytest fixtures
- **Test Coverage**: Maintain reasonable coverage (currently ~30%+)
- **Test Organization**: Mirror source structure in `tests/`

### Writing Tests

```python
# Example test structure
import pytest
from pathlib import Path
from claude_knowledge_catalyst.core.config import CKCConfig

def test_config_creation():
    """Test configuration creation and validation."""
    config = CKCConfig()
    assert config.project_name is not None
    assert isinstance(config.project_root, Path)
```

## Pull Request Process

### Before Submitting

1. **Run all quality checks:**
   ```bash
   uv run pre-commit run --all-files
   uv run pytest --cov=src
   ```

2. **Ensure CI will pass:**
   - All tests pass locally
   - Code is properly formatted
   - Type checking passes
   - No linting errors

3. **Update documentation** if needed
4. **Add/update tests** for new functionality

### PR Requirements

- **Descriptive Title**: Clearly describe the change
- **Detailed Description**: Explain what, why, and how
- **Link Issues**: Reference related issues with `Closes #123`
- **Small, Focused Changes**: Easier to review and merge
- **Clean Commit History**: Use meaningful commit messages

### Commit Message Format

```
type: Brief description of change

More detailed explanation if needed.

- List specific changes
- Reference issues: Closes #123
- Breaking changes: BREAKING CHANGE: description
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `ci`: CI/CD changes

## Project-Specific Guidelines

### Claude Code Integration

- **Development Context**: This project enhances Claude Code workflows
- **Testing with Claude**: Test functionality within Claude Code environment
- **File Watching**: Be aware of file system monitoring features
- **Obsidian Integration**: Test vault synchronization functionality

### Configuration Management

- **Pydantic Models**: All config uses Pydantic for validation
- **YAML Configuration**: Main config in `ckc_config.yaml`
- **Environment Variables**: Support for env-based configuration
- **Migration Support**: Handle config version upgrades

### Package Management

- **uv Only**: Use `uv` for all package operations
- **Lock Files**: Commit `uv.lock` for reproducible builds
- **Dependencies**: Add new deps via `uv add package-name`
- **Dev Dependencies**: Use `uv add --group dev package-name`

### Special Considerations

- **File System Monitoring**: Test on different OS types
- **Async Operations**: Handle async properly in tests
- **Git Integration**: Be aware of GitPython usage
- **Template System**: Test Jinja2 template rendering

## Getting Help

### Resources

- **Documentation**: Read the comprehensive docs
- **Issues**: Check existing [GitHub Issues](https://github.com/drillan/claude-knowledge-catalyst/issues)
- **Discussions**: Join [GitHub Discussions](https://github.com/drillan/claude-knowledge-catalyst/discussions)
- **Code Examples**: Look at existing tests and implementations

### Asking for Help

- **Search First**: Check issues and discussions
- **Provide Context**: Include error messages and steps to reproduce
- **Minimal Examples**: Create minimal reproducible examples
- **Environment Info**: Include Python version, OS, and uv version

### Development Issues

- **CI Failures**: Check GitHub Actions logs for detailed error info
- **Environment Problems**: Ensure `uv sync --dev` completed successfully
- **Type Errors**: Run `uv run mypy src/` for detailed type checking
- **Test Failures**: Run `uv run pytest -v` for verbose test output

## Code of Conduct

- **Be Respectful**: Treat all contributors with respect
- **Be Constructive**: Provide helpful feedback and suggestions
- **Be Patient**: Allow time for reviews and responses
- **Be Inclusive**: Welcome contributors of all backgrounds and skill levels

## Recognition

Contributors will be recognized in:
- **Release Notes**: Major contributions acknowledged
- **Documentation**: Contributor acknowledgments
- **Git History**: All contributions properly attributed

---

Thank you for contributing to Claude Knowledge Catalyst! Your contributions help make AI-powered knowledge management more accessible and effective for everyone.

For questions about this guide, please open an issue or start a discussion on GitHub.
