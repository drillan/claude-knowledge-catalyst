"""Configuration management for Claude Knowledge Catalyst."""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, field_validator

from .hybrid_config import HybridStructureConfig


class SyncTarget(BaseModel):
    """Configuration for sync target (e.g., Obsidian vault)."""

    name: str = Field(..., description="Name of the sync target")
    type: str = Field(..., description="Type of sync target (obsidian, notion, etc.)")
    path: Path = Field(..., description="Path to the sync target")
    enabled: bool = Field(
        default=True, description="Whether this sync target is enabled"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Validate sync target type."""
        supported_types = ["obsidian", "notion", "file"]
        if v.lower() not in supported_types:
            raise ValueError(
                f"Unsupported sync type: {v}. Supported: {supported_types}"
            )
        return v.lower()


class TagConfig(BaseModel):
    """Configuration for tag management."""

    category_tags: list[str] = Field(
        default=["prompt", "code", "concept", "resource", "project_log"],
        description="Category tags for content classification",
    )
    tech_tags: list[str] = Field(
        default=["python", "javascript", "react", "nodejs"],
        description="Technology-specific tags",
    )
    claude_tags: list[str] = Field(
        default=["opus", "sonnet", "haiku"], description="Claude model-specific tags"
    )
    status_tags: list[str] = Field(
        default=["draft", "tested", "production", "deprecated"],
        description="Status tags for content lifecycle",
    )
    quality_tags: list[str] = Field(
        default=["high", "medium", "low", "experimental"],
        description="Quality assessment tags",
    )


class WatchConfig(BaseModel):
    """Configuration for file watching."""

    watch_paths: list[Path] = Field(
        default=[Path(".claude")], description="Paths to watch for changes"
    )
    file_patterns: list[str] = Field(
        default=["*.md", "*.txt"], description="File patterns to watch"
    )
    ignore_patterns: list[str] = Field(
        default=[".git", "__pycache__", "*.pyc"], description="Patterns to ignore"
    )
    debounce_seconds: float = Field(
        default=1.0, description="Debounce time for file change events"
    )
    # CLAUDE.md sync configuration
    include_claude_md: bool = Field(
        default=False, description="Include CLAUDE.md files in synchronization"
    )
    claude_md_patterns: list[str] = Field(
        default=["CLAUDE.md", ".claude/CLAUDE.md"],
        description="Patterns to match CLAUDE.md files",
    )
    claude_md_sections_exclude: list[str] = Field(
        default=[],
        description=(
            "Section headers to exclude from CLAUDE.md sync "
            "(e.g., '# secrets', '# private')"
        ),
    )


class MigrationConfig(BaseModel):
    """Configuration for migration features."""

    auto_detect: bool = Field(
        default=True, description="Automatically detect migration opportunities"
    )
    notify_level: str = Field(
        default="recommended",
        description="Notification level: 'silent', 'minimal', 'recommended', 'verbose'",
    )
    backup_before: bool = Field(
        default=True, description="Create backup before migration"
    )
    mixed_format_warning: bool = Field(
        default=True, description="Show warnings when using mixed formats"
    )

    @field_validator("notify_level")
    @classmethod
    def validate_notify_level(cls, v: str) -> str:
        """Validate notification level."""
        valid_levels = ["silent", "minimal", "recommended", "verbose"]
        if v.lower() not in valid_levels:
            raise ValueError(
                f"Invalid notify_level: {v}. Valid options: {valid_levels}"
            )
        return v.lower()


class CKCConfig(BaseModel):
    """Main configuration for Claude Knowledge Catalyst."""

    version: str = Field(default="2.0", description="Configuration version")
    project_name: str = Field(default="", description="Name of the project")
    project_root: Path = Field(
        default_factory=lambda: Path.cwd(), description="Root path of the project"
    )

    # Sync configuration
    sync_targets: list[SyncTarget] = Field(
        default_factory=list, description="List of sync targets"
    )
    auto_sync: bool = Field(
        default=True, description="Enable automatic synchronization"
    )

    # Tag and metadata configuration
    tags: TagConfig = Field(default_factory=TagConfig, description="Tag configuration")

    # File watching configuration
    watch: WatchConfig = Field(
        default_factory=WatchConfig, description="File watching configuration"
    )

    # Template configuration
    template_path: Path = Field(
        default=Path("templates"), description="Path to template files"
    )

    # Git integration
    git_integration: bool = Field(default=True, description="Enable Git integration")
    auto_commit: bool = Field(default=False, description="Enable automatic commits")

    # Hybrid structure configuration (new in v2.0)
    hybrid_structure: HybridStructureConfig = Field(
        default_factory=lambda: HybridStructureConfig(),
        description="Hybrid structure configuration",
    )

    # Migration configuration
    migration: MigrationConfig = Field(
        default_factory=MigrationConfig,
        description="Migration and notification configuration",
    )

    @field_validator("project_root", "template_path", mode="before")
    @classmethod
    def resolve_paths(cls, v: str | Path) -> Path:
        """Resolve relative paths."""
        try:
            return Path(v).resolve()
        except (FileNotFoundError, OSError):
            # If path can't be resolved (e.g., during testing or if dir doesn't exist),
            # return the path as-is to avoid breaking config loading
            return Path(v)

    @classmethod
    def load_from_file(cls, config_path: str | Path) -> "CKCConfig":
        """Load configuration from YAML file."""
        config_path = Path(config_path)

        if not config_path.exists():
            # Return default configuration for new projects
            return cls()

        with open(config_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls(**data)

    def save_to_file(self, config_path: str | Path) -> None:
        """Save configuration to YAML file."""
        config_path = Path(config_path)
        # Note: Don't create parent directories as config files are typically
        # saved in existing directories (like project root)

        # Convert to dict and handle Path objects
        data = self.model_dump()
        self._convert_paths_to_str(data)

        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    def _convert_paths_to_str(self, data: dict[str, Any]) -> None:
        """Convert Path objects and Enums to strings for YAML serialization."""
        for key, value in data.items():
            if isinstance(value, Path):
                data[key] = str(value)
            elif hasattr(value, "value"):  # Enum objects
                data[key] = value.value
            elif isinstance(value, dict):
                self._convert_paths_to_str(value)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, Path):
                        value[i] = str(item)
                    elif hasattr(item, "value"):  # Enum objects
                        value[i] = item.value
                    elif isinstance(item, dict):
                        self._convert_paths_to_str(item)

    def get_enabled_sync_targets(self) -> list[SyncTarget]:
        """Get list of enabled sync targets."""
        return [target for target in self.sync_targets if target.enabled]

    def add_sync_target(self, target: SyncTarget) -> None:
        """Add a new sync target."""
        # Remove existing target with same name
        self.sync_targets = [t for t in self.sync_targets if t.name != target.name]
        self.sync_targets.append(target)

    def remove_sync_target(self, name: str) -> bool:
        """Remove sync target by name."""
        original_count = len(self.sync_targets)
        self.sync_targets = [t for t in self.sync_targets if t.name != name]
        return len(self.sync_targets) < original_count


def get_default_config_path() -> Path:
    """Get the default configuration file path."""
    return Path.cwd() / "ckc_config.yaml"


def load_config(config_path: str | Path | None = None) -> CKCConfig:
    """Load configuration from file or create default."""
    if config_path is None:
        config_path = get_default_config_path()

    return CKCConfig.load_from_file(config_path)
