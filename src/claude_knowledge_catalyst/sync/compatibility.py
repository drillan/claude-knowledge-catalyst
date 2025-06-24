"""Compatibility management for hybrid and legacy structures."""

import shutil
from pathlib import Path
from typing import Any

from ..core.config import CKCConfig
from ..core.metadata import KnowledgeMetadata
from .hybrid_manager import HybridObsidianVaultManager
from .obsidian import ObsidianVaultManager


class StructureCompatibilityManager:
    """Manages compatibility between hybrid and legacy structures."""

    def __init__(self, vault_path: Path, config: CKCConfig):
        self.vault_path = vault_path
        self.config = config
        self.legacy_mappings = self._get_legacy_mappings()

    def _get_legacy_mappings(self) -> dict[str, str]:
        """Get mappings from legacy to hybrid directory names."""
        return {
            "00_Inbox": "00_Catalyst_Lab",
            "01_Projects": "10_Projects",
            "02_Knowledge_Base": "20_Knowledge_Base",
            "03_Templates": "_templates",
            "04_Analytics": "Analytics",
            "05_Archive": "30_Wisdom_Archive",
        }

    def detect_current_structure(self) -> str:
        """Detect current vault structure type."""
        if not self.vault_path.exists():
            return "none"

        existing_dirs = [d.name for d in self.vault_path.iterdir() if d.is_dir()]

        # Check for hybrid structure indicators
        ten_step_dirs = [
            d for d in existing_dirs if d.startswith(("00_", "10_", "20_", "30_"))
        ]
        system_dirs = [d for d in existing_dirs if d.startswith("_")]

        if ten_step_dirs and system_dirs:
            return "hybrid"
        elif any(
            d.startswith(("00_", "01_", "02_", "03_", "04_", "05_"))
            for d in existing_dirs
        ):
            return "legacy"
        elif existing_dirs:
            return "unknown"
        else:
            return "none"

    def ensure_legacy_access(self) -> bool:
        """Ensure legacy directory access through symlinks or compatibility bridges."""
        if (
            not self.config.hybrid_structure.enabled
            or not self.config.hybrid_structure.legacy_support
        ):
            return True  # No compatibility needed

        structure_type = self.detect_current_structure()
        if structure_type != "hybrid":
            return True  # Not a hybrid structure

        success = True

        for legacy_name, hybrid_name in self.legacy_mappings.items():
            legacy_path = self.vault_path / legacy_name
            hybrid_path = self.vault_path / hybrid_name

            if hybrid_path.exists() and not legacy_path.exists():
                try:
                    # Create symlink from legacy to hybrid name
                    legacy_path.symlink_to(hybrid_path, target_is_directory=True)
                    print(f"✅ Legacy access created: {legacy_name} → {hybrid_name}")
                except OSError as e:
                    # Symlink creation failed, try compatibility bridge
                    print(f"⚠️ Symlink failed for {legacy_name}: {e}")
                    bridge_success = self._create_compatibility_bridge(
                        legacy_path, hybrid_path
                    )
                    if not bridge_success:
                        success = False

        return success

    def _create_compatibility_bridge(
        self, legacy_path: Path, hybrid_path: Path
    ) -> bool:
        """Create compatibility bridge when symlinks fail."""
        try:
            # Create legacy directory with redirect README
            legacy_path.mkdir(exist_ok=True)

            redirect_content = f"""# 📁 Directory Moved

This directory has been moved to maintain better organization.

**New Location**: `{hybrid_path.name}`

## 🔄 Quick Navigation
- [Go to new location]({hybrid_path.name})

## 📝 Note
This compatibility bridge will be maintained for 6 months to ensure smooth transition.
After that period, please update your workflows to use the new location.

---
*Compatibility bridge created by CKC v2.0*
"""

            readme_path = legacy_path / "README.md"
            readme_path.write_text(redirect_content, encoding="utf-8")

            print(f"✅ Compatibility bridge created: {legacy_path.name}")
            return True

        except Exception as e:
            print(
                f"❌ Failed to create compatibility bridge for {legacy_path.name}: {e}"
            )
            return False

    def cleanup_legacy_bridges(self) -> int:
        """Clean up legacy compatibility bridges."""
        cleaned_count = 0

        for legacy_name in self.legacy_mappings.keys():
            legacy_path = self.vault_path / legacy_name

            if legacy_path.exists():
                if legacy_path.is_symlink():
                    # Remove symlink
                    legacy_path.unlink()
                    cleaned_count += 1
                    print(f"🗑️ Removed legacy symlink: {legacy_name}")
                elif legacy_path.is_dir():
                    # Check if it's a compatibility bridge
                    readme_path = legacy_path / "README.md"
                    if (
                        readme_path.exists()
                        and "Compatibility bridge created by CKC"
                        in readme_path.read_text()
                    ):
                        shutil.rmtree(legacy_path)
                        cleaned_count += 1
                        print(f"🗑️ Removed compatibility bridge: {legacy_name}")

        return cleaned_count


class BackwardCompatibilityManager:
    """Manages backward compatibility for existing CKC installations."""

    def __init__(self, vault_path: Path, config: CKCConfig):
        self.vault_path = vault_path
        self.config = config
        self.compatibility = StructureCompatibilityManager(vault_path, config)

    def get_appropriate_manager(self, metadata_manager) -> ObsidianVaultManager:
        """Get appropriate vault manager based on configuration."""

        if self.config.hybrid_structure.enabled:
            # Use hybrid manager
            return HybridObsidianVaultManager(
                self.vault_path, metadata_manager, self.config
            )
        else:
            # Use legacy manager
            return ObsidianVaultManager(self.vault_path, metadata_manager)

    def ensure_compatibility(self) -> bool:
        """Ensure compatibility between structures."""

        # Detect current structure
        current_structure = self.compatibility.detect_current_structure()

        if (
            current_structure == "hybrid"
            and self.config.hybrid_structure.legacy_support
        ):
            # Ensure legacy access for hybrid structure
            return self.compatibility.ensure_legacy_access()
        elif current_structure == "legacy" and self.config.hybrid_structure.enabled:
            # Offer migration suggestion
            self._suggest_migration()
            return True
        else:
            # No compatibility actions needed
            return True

    def _suggest_migration(self) -> None:
        """Suggest migration to hybrid structure."""
        print(
            """
💡 Migration Suggestion

Your vault is using the legacy structure, but hybrid structure is enabled in
configuration.
Consider migrating to take advantage of improved organization:

  uv run ckc migrate --to hybrid --dry-run  # Preview migration
  uv run ckc migrate --to hybrid           # Execute migration

Benefits of hybrid structure:
- Better scalability with 10-step numbering
- Clearer organization with three-tier classification
- Enhanced automation capabilities
        """
        )

    def validate_compatibility(self) -> list[str]:
        """Validate compatibility and return list of issues."""
        issues = []

        current_structure = self.compatibility.detect_current_structure()

        # Check configuration consistency
        if self.config.hybrid_structure.enabled and current_structure == "legacy":
            if not self.config.hybrid_structure.legacy_support:
                issues.append(
                    "Hybrid structure enabled but legacy support disabled "
                    "with legacy vault"
                )

        # Check for conflicting directories
        if current_structure == "hybrid":
            legacy_dirs = [
                self.vault_path / name
                for name in self.compatibility.legacy_mappings.keys()
            ]
            hybrid_dirs = [
                self.vault_path / name
                for name in self.compatibility.legacy_mappings.values()
            ]

            for legacy_path, hybrid_path in zip(legacy_dirs, hybrid_dirs, strict=False):
                if (
                    legacy_path.exists()
                    and hybrid_path.exists()
                    and not legacy_path.is_symlink()
                    and legacy_path.resolve() != hybrid_path.resolve()
                ):
                    issues.append(
                        f"Conflicting directories: {legacy_path.name} and "
                        f"{hybrid_path.name}"
                    )

        return issues


class LegacyFileHandler:
    """Handles legacy file operations with compatibility."""

    def __init__(self, config: CKCConfig):
        self.config = config

    def handle_legacy_sync(
        self,
        source_path: Path,
        target_manager: ObsidianVaultManager,
        metadata: KnowledgeMetadata,
        project_name: str | None = None,
    ) -> bool:
        """Handle file sync with legacy compatibility."""

        if isinstance(target_manager, HybridObsidianVaultManager):
            # Hybrid manager handles its own logic
            return target_manager.sync_file(source_path, project_name)
        else:
            # Legacy manager
            return target_manager.sync_file(source_path, project_name)

    def translate_legacy_path(self, legacy_path: str) -> str:
        """Translate legacy path to hybrid path if applicable."""

        if not self.config.hybrid_structure.enabled:
            return legacy_path

        # Check if path starts with legacy directory
        mappings = {
            "00_Inbox": "00_Catalyst_Lab",
            "01_Projects": "10_Projects",
            "02_Knowledge_Base": "20_Knowledge_Base",
            "03_Templates": "_templates",
            "04_Analytics": "Analytics",
            "05_Archive": "30_Wisdom_Archive",
        }

        for legacy_prefix, hybrid_prefix in mappings.items():
            if legacy_path.startswith(legacy_prefix):
                return legacy_path.replace(legacy_prefix, hybrid_prefix, 1)

        return legacy_path


class MigrationSafetyValidator:
    """Validates migration safety and prerequisites."""

    def __init__(self, vault_path: Path, config: CKCConfig):
        self.vault_path = vault_path
        self.config = config

    def validate_migration_prerequisites(self) -> dict[str, Any]:
        """Validate prerequisites for migration."""
        result: dict[str, Any] = {
            "safe_to_migrate": True,
            "warnings": [],
            "errors": [],
            "recommendations": [],
        }

        # Check vault exists and is accessible
        if not self.vault_path.exists():
            result["errors"].append("Vault directory does not exist")
            result["safe_to_migrate"] = False
            return result

        # Check for write permissions
        if not self._check_write_permissions():
            result["errors"].append(
                "Insufficient write permissions for vault directory"
            )
            result["safe_to_migrate"] = False

        # Check disk space
        free_space = self._get_free_space()
        vault_size = self._get_vault_size()

        if free_space < vault_size * 2:  # Need 2x space for backup
            result["warnings"].append(
                f"Low disk space. Have: {free_space}MB, Need: {vault_size * 2}MB"
            )

        # Check for active file handles
        if self._check_active_file_handles():
            result["warnings"].append(
                "Vault may be open in other applications. Close before migration."
            )

        # Check for custom modifications
        custom_mods = self._detect_custom_modifications()
        if custom_mods:
            result["warnings"].extend(custom_mods)
            result["recommendations"].append(
                "Review custom modifications before migration"
            )

        return result

    def _check_write_permissions(self) -> bool:
        """Check if we have write permissions to vault."""
        try:
            test_file = self.vault_path / ".ckc_permission_test"
            test_file.write_text("test")
            test_file.unlink()
            return True
        except (PermissionError, OSError):
            return False

    def _get_free_space(self) -> int:
        """Get free disk space in MB."""
        try:
            statvfs = shutil.disk_usage(self.vault_path)
            return statvfs.free // (1024 * 1024)  # Convert to MB
        except OSError:
            return 0

    def _get_vault_size(self) -> int:
        """Get vault size in MB."""
        try:
            total_size = sum(
                f.stat().st_size for f in self.vault_path.rglob("*") if f.is_file()
            )
            return total_size // (1024 * 1024)  # Convert to MB
        except OSError:
            return 0

    def _check_active_file_handles(self) -> bool:
        """Check for active file handles (basic check)."""
        # This is a basic implementation
        # In practice, might use platform-specific tools
        return False

    def _detect_custom_modifications(self) -> list[str]:
        """Detect custom modifications that might be affected by migration."""
        modifications = []

        # Check for custom .obsidian settings
        obsidian_dir = self.vault_path / ".obsidian"
        if obsidian_dir.exists():
            config_files = ["app.json", "workspace.json", "community-plugins.json"]
            for config_file in config_files:
                if (obsidian_dir / config_file).exists():
                    modifications.append(
                        f"Custom Obsidian configuration: {config_file}"
                    )

        # Check for non-standard directory structures
        expected_dirs = {"00_", "01_", "02_", "03_", "04_", "05_"}
        actual_dirs = {
            d.name[:3]
            for d in self.vault_path.iterdir()
            if d.is_dir() and len(d.name) >= 3
        }

        unexpected = (
            actual_dirs - expected_dirs - {".ob", "_te"}
        )  # Allow .obsidian, _templates etc
        if unexpected:
            modifications.append(
                f"Custom directory structure detected: {', '.join(unexpected)}"
            )

        return modifications
