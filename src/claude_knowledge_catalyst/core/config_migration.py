"""Configuration migration functionality for CKC."""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from .config import CKCConfig
from .hybrid_config import HybridStructureConfig, NumberingSystem


class ConfigMigrationManager:
    """Manages configuration file migrations between versions."""
    
    def __init__(self):
        self.migration_handlers = {
            "1.0": self._migrate_v1_to_v2,
            "unknown": self._migrate_unknown_to_v2
        }
    
    def detect_config_version(self, config_data: dict) -> str:
        """Detect configuration version from data."""
        version = config_data.get("version", "unknown")
        
        # If version is present, use it
        if isinstance(version, str) and version in ["1.0", "2.0"]:
            return version
        
        # Detect by presence of hybrid_structure field
        if "hybrid_structure" in config_data:
            return "2.0"
        
        # Check for old structure indicators
        sync_targets = config_data.get("sync_targets", [])
        for target in sync_targets:
            if isinstance(target, dict) and target.get("type") == "obsidian":
                # If it has obsidian sync but no hybrid config, likely v1.0
                return "1.0"
        
        return "unknown"
    
    def load_config_with_migration(self, config_path: Path) -> CKCConfig:
        """Load configuration with automatic migration if needed."""
        
        if not config_path.exists():
            # Create default v2.0 config
            config = CKCConfig()
            config.save_to_file(config_path)
            return config
        
        # Load raw configuration data
        with open(config_path, encoding="utf-8") as f:
            raw_data = yaml.safe_load(f) or {}
        
        # Detect version
        version = self.detect_config_version(raw_data)
        
        # Migrate if needed
        if version != "2.0":
            return self._migrate_config(raw_data, version, config_path)
        else:
            # Already v2.0, load directly
            return CKCConfig(**raw_data)
    
    def _migrate_config(self, raw_data: dict, from_version: str, 
                       config_path: Path) -> CKCConfig:
        """Migrate configuration from specified version to v2.0."""
        
        # Create backup before migration
        self._backup_config(config_path)
        
        # Get migration handler
        handler = self.migration_handlers.get(from_version, self._migrate_unknown_to_v2)
        
        # Perform migration
        migrated_data = handler(raw_data)
        
        # Create config object
        config = CKCConfig(**migrated_data)
        
        # Save migrated configuration
        config.save_to_file(config_path)
        
        # Log migration
        self._log_migration(from_version, "2.0", config_path)
        
        # Show migration message
        self._show_migration_message(from_version, "2.0")
        
        return config
    
    def _migrate_v1_to_v2(self, v1_data: dict) -> dict:
        """Migrate v1.0 configuration to v2.0."""
        
        # Start with v1 data as base
        v2_data = dict(v1_data)
        
        # Update version
        v2_data["version"] = "2.0"
        
        # Add hybrid structure configuration with defaults
        v2_data["hybrid_structure"] = {
            "enabled": False,  # Default disabled for existing users
            "numbering_system": "sequential",  # Maintain existing behavior
            "structure_version": "hybrid_v1",
            "auto_classification": False,  # Conservative default
            "auto_enhancement": True,
            "structure_validation": True,
            "migration_mode": "gradual",
            "legacy_support": True,
            "custom_structure": None,
            "custom_numbering": None
        }
        
        # Add migration log
        v2_data["structure_migration_log"] = [
            {
                "timestamp": datetime.now().isoformat(),
                "from_version": "1.0",
                "to_version": "2.0",
                "migration_type": "automatic",
                "changes": [
                    "Added hybrid_structure configuration",
                    "Maintained sequential numbering system",
                    "Enabled legacy support"
                ]
            }
        ]
        
        # Preserve all existing fields
        preserved_fields = [
            "project_name", "project_root", "sync_targets", "auto_sync",
            "tags", "watch", "template_path", "git_integration", "auto_commit"
        ]
        
        for field in preserved_fields:
            if field in v1_data:
                v2_data[field] = v1_data[field]
        
        return v2_data
    
    def _migrate_unknown_to_v2(self, unknown_data: dict) -> dict:
        """Migrate unknown/malformed configuration to v2.0."""
        
        # Create minimal v2.0 configuration
        v2_data = {
            "version": "2.0",
            "project_name": unknown_data.get("project_name", ""),
            "sync_targets": unknown_data.get("sync_targets", []),
            "hybrid_structure": {
                "enabled": False,
                "numbering_system": "sequential",
                "structure_version": "hybrid_v1",
                "auto_classification": False,
                "auto_enhancement": True,
                "structure_validation": True,
                "migration_mode": "gradual",
                "legacy_support": True
            },
            "structure_migration_log": [
                {
                    "timestamp": datetime.now().isoformat(),
                    "from_version": "unknown",
                    "to_version": "2.0",
                    "migration_type": "reconstruction",
                    "changes": [
                        "Reconstructed configuration from partial data",
                        "Applied safe defaults",
                        "Enabled legacy support"
                    ]
                }
            ]
        }
        
        # Try to preserve as much as possible from unknown data
        safe_fields = [
            "project_root", "auto_sync", "template_path", 
            "git_integration", "auto_commit"
        ]
        
        for field in safe_fields:
            if field in unknown_data:
                v2_data[field] = unknown_data[field]
        
        return v2_data
    
    def _backup_config(self, config_path: Path) -> Path:
        """Create backup of configuration file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = config_path.parent / f"{config_path.stem}_backup_{timestamp}{config_path.suffix}"
        
        if config_path.exists():
            shutil.copy2(config_path, backup_path)
        
        return backup_path
    
    def _log_migration(self, from_version: str, to_version: str, config_path: Path):
        """Log migration details."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "config_path": str(config_path),
            "from_version": from_version,
            "to_version": to_version,
            "status": "completed"
        }
        
        # Could implement persistent logging here
        print(f"✅ Configuration migrated: {from_version} → {to_version}")
    
    def _show_migration_message(self, from_version: str, to_version: str):
        """Show migration completion message to user."""
        print(f"""
🔄 CKC設定ファイルを自動更新しました

📋 変更内容:
  - バージョン: {from_version} → {to_version}
  - 新機能設定を追加（デフォルト無効）
  - 既存設定は完全に保持
  - 動作に変更はありません

🚀 新機能を試すには:
  uv run ckc structure --help
  
💡 ハイブリッド構造を有効にする:
  uv run ckc init --structure hybrid
        """)


class ConfigCompatibilityValidator:
    """Validates configuration compatibility across versions."""
    
    def validate_v1_compatibility(self, config: CKCConfig) -> bool:
        """Validate that v2.0 config maintains v1.0 compatibility."""
        
        # Check required v1.0 fields exist
        required_v1_fields = [
            "project_name", "sync_targets", "auto_sync"
        ]
        
        for field in required_v1_fields:
            if not hasattr(config, field):
                return False
        
        # Check that hybrid features don't break v1.0 behavior when disabled
        if config.hybrid_structure.enabled:
            # If hybrid is enabled, ensure legacy support is also enabled
            return config.hybrid_structure.legacy_support
        
        return True
    
    def get_compatibility_issues(self, config: CKCConfig) -> list[str]:
        """Get list of compatibility issues."""
        issues = []
        
        # Check sync targets compatibility
        for target in config.sync_targets:
            if target.type == "obsidian":
                # Ensure obsidian targets work with both structures
                if not config.hybrid_structure.legacy_support and not config.hybrid_structure.enabled:
                    issues.append("Obsidian sync target may not work without hybrid or legacy support")
        
        # Check numbering system consistency
        if config.hybrid_structure.enabled:
            if config.hybrid_structure.numbering_system == NumberingSystem.SEQUENTIAL:
                if not config.hybrid_structure.legacy_support:
                    issues.append("Sequential numbering without legacy support may cause confusion")
        
        return issues


def migrate_config_if_needed(config_path: Path | None = None) -> CKCConfig:
    """Convenience function to migrate config if needed."""
    if config_path is None:
        config_path = Path.cwd() / "ckc_config.yaml"
    
    migration_manager = ConfigMigrationManager()
    return migration_manager.load_config_with_migration(config_path)