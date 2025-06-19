# 開発環境ガイド

Claude Knowledge Catalyst (CKC) の開発環境設定、コマンド、ベストプラクティスについて説明します。

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

## UV Package Management詳細

### プロジェクト管理の基本
uvを使用したモダンなPython開発では、プロジェクトベースのアプローチを採用します。

新しいプロジェクトの作成:
```bash
# 新しいプロジェクトディレクトリを作成して初期化
uv init my-project
cd my-project

# 既存のディレクトリでプロジェクトを初期化
uv init

# 特定のPythonバージョンを指定してプロジェクトを初期化
uv init --python 3.11
```

プロジェクト情報の確認:
```bash
# プロジェクトの情報を表示
uv info

# 現在のPython環境を表示
uv python show
```

### 仮想環境の管理
uvは仮想環境の作成と管理を自動化し、プロジェクトごとに独立した環境を提供します。

仮想環境の作成:
```bash
# デフォルトの仮想環境を作成
uv venv

# 特定の名前で仮想環境を作成
uv venv my-env

# 特定のPythonバージョンで仮想環境を作成
uv venv --python 3.11

# 仮想環境を削除してクリーンに再作成
uv venv --clear
```

### パッケージ管理
モダンなパッケージ管理（推奨）:
```bash
# パッケージをプロジェクトに追加
uv add requests
uv add "django>=4.0,<5.0"

# 複数のパッケージを同時に追加
uv add requests pandas numpy

# 開発用依存関係を追加
uv add --dev pytest ruff mypy

# パッケージを削除
uv remove requests

# すべての依存関係をインストール（pyproject.tomlから）
uv sync

# 開発用依存関係も含めてインストール
uv sync --dev
```

### 依存関係管理
```bash
# 依存関係をロック（固定）
uv lock

# 特定のパッケージのみを更新
uv lock --upgrade-package requests

# すべての依存関係を最新に更新
uv lock --upgrade

# ロックファイルに基づいて環境を同期
uv sync

# 依存関係ツリーを表示
uv tree
```

### コマンドの実行
基本的な実行コマンド:
```bash
# Pythonスクリプトを実行
uv run python script.py

# Pythonモジュールを実行
uv run -m pytest
uv run ruff check .
uv run ruff format .

# 一時的な依存関係でスクリプトを実行
uv run --with requests python -c "import requests; print(requests.get('https://httpbin.org/json').json())"
```

### Pythonバージョン管理
```bash
# 利用可能なPythonバージョンを表示
uv python list

# 特定のPythonバージョンをインストール
uv python install 3.11
uv python install 3.12

# プロジェクトのPythonバージョンを設定
uv python pin 3.11

# 現在使用中のPythonバージョンを表示
uv python show

# インストール済みのPythonバージョンを表示
uv python list --only-installed
```

### ベストプラクティス
プロジェクト管理のベストプラクティス:
- 新しいプロジェクトでは必ず`uv init`から始める
- `pyproject.toml`を直接編集せず、`uv add`/`uv remove`を使用する
- `uv.lock`ファイルをバージョン管理システムにコミットして、チーム全体で同じ依存関係を共有する
- 定期的に`uv lock --upgrade`を実行して依存関係を最新に保つ

開発ワークフローのベストプラクティス:
- `uv run`を活用して仮想環境の有効化を自動化する
- CI/CDパイプラインでは`uv sync`を使用して高速で確実な環境構築を行う
- 開発用依存関係は`--dev`オプションを使用して本番環境と分離する

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

### UV Troubleshooting
一般的な問題と解決方法:
```bash
# キャッシュが破損した場合
uv cache clean

# 依存関係の競合が発生した場合
uv lock --resolution lowest-direct

# 仮想環境をクリーンに再作成
uv venv --clear

# 詳細なエラー情報を表示
uv --verbose command

# プロジェクトの状態を確認
uv info
```

パフォーマンス最適化:
- 大規模なプロジェクトでは`--no-cache`オプションを避ける
- ネットワーク環境が不安定な場合は`--retries`オプションを使用
- 並列処理を活用するため、十分なメモリを確保する