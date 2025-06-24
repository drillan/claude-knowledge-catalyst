"""Structure validation system for CKC hybrid structures."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .hybrid_config import DirectoryTier, HybridStructureConfig


class ValidationResult:
    """Result of structure validation."""

    def __init__(self) -> None:
        self.passed: bool = True
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: list[str] = []
        self.timestamp: datetime = datetime.now()
        self.statistics: dict[str, Any] = {}

    def add_error(self, message: str) -> None:
        """Add validation error."""
        self.errors.append(message)
        self.passed = False

    def add_warning(self, message: str) -> None:
        """Add validation warning."""
        self.warnings.append(message)

    def add_info(self, message: str) -> None:
        """Add validation info."""
        self.info.append(message)

    def set_statistics(self, stats: dict[str, Any]) -> None:
        """Set validation statistics."""
        self.statistics = stats

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "passed": self.passed,
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info,
            "timestamp": self.timestamp.isoformat(),
            "statistics": self.statistics,
        }

    def __str__(self) -> str:
        """String representation of validation result."""
        status = "✅ PASSED" if self.passed else "❌ FAILED"

        lines = [f"Structure Validation: {status}"]

        if self.errors:
            lines.append(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                lines.append(f"  - {error}")

        if self.warnings:
            lines.append(f"\n⚠️ Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                lines.append(f"  - {warning}")

        if self.info:
            lines.append(f"\n💡 Info ({len(self.info)}):")
            for info in self.info:
                lines.append(f"  - {info}")

        return "\n".join(lines)


class StructureValidator:
    """Validates hybrid structure integrity and compliance."""

    def __init__(self, vault_path: Path, hybrid_config: HybridStructureConfig):
        self.vault_path = vault_path
        self.config = hybrid_config

    def validate_full_structure(self) -> ValidationResult:
        """Perform comprehensive structure validation."""
        result = ValidationResult()

        if not self.vault_path.exists():
            result.add_error(f"Vault directory does not exist: {self.vault_path}")
            return result

        # Core validation checks
        self._validate_directory_structure(result)
        self._validate_numbering_consistency(result)
        self._validate_tier_compliance(result)
        self._validate_readme_coverage(result)
        self._validate_metadata_compliance(result)

        # Generate statistics
        stats = self._generate_statistics()
        result.set_statistics(stats)

        return result

    def _validate_directory_structure(self, result: ValidationResult) -> None:
        """Validate directory structure against configuration."""
        expected_structure = self.config.get_default_structure()

        # Validate system directories
        if "system_dirs" in expected_structure:
            for dir_name, _description in expected_structure["system_dirs"].items():
                dir_path = self.vault_path / dir_name

                if not dir_path.exists():
                    result.add_error(f"Missing system directory: {dir_name}")
                elif not dir_path.is_dir():
                    result.add_error(f"System path is not a directory: {dir_name}")
                else:
                    result.add_info(f"System directory verified: {dir_name}")

        # Validate core directories
        if "core_dirs" in expected_structure:
            for dir_name, _description in expected_structure["core_dirs"].items():
                dir_path = self.vault_path / dir_name

                if not dir_path.exists():
                    result.add_error(f"Missing core directory: {dir_name}")
                elif not dir_path.is_dir():
                    result.add_error(f"Core path is not a directory: {dir_name}")
                else:
                    result.add_info(f"Core directory verified: {dir_name}")

        # Validate auxiliary directories
        if "auxiliary_dirs" in expected_structure:
            for dir_name, _description in expected_structure["auxiliary_dirs"].items():
                dir_path = self.vault_path / dir_name

                if not dir_path.exists():
                    result.add_warning(f"Missing auxiliary directory: {dir_name}")
                elif not dir_path.is_dir():
                    result.add_warning(f"Auxiliary path is not a directory: {dir_name}")
                else:
                    result.add_info(f"Auxiliary directory verified: {dir_name}")

        # Check for unexpected directories
        self._check_unexpected_directories(result, expected_structure)

    def _validate_numbering_consistency(self, result: ValidationResult) -> None:
        """Validate numbering system consistency."""
        numbered_dirs = []

        for item in self.vault_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                classification = self.config.classify_directory(item.name)
                if classification.number is not None:
                    numbered_dirs.append((item.name, classification.number))

        # Sort by number
        numbered_dirs.sort(key=lambda x: x[1])

        # Validate numbering based on system type
        if self.config.numbering_system.value == "ten_step":
            self._validate_ten_step_numbering(result, numbered_dirs)
        else:
            self._validate_sequential_numbering(result, numbered_dirs)

    def _validate_ten_step_numbering(
        self, result: ValidationResult, numbered_dirs: list[tuple]
    ) -> None:
        """Validate ten-step numbering system."""
        expected_base_numbers = [0, 10, 20, 30]
        actual_numbers = [num for _, num in numbered_dirs]

        # Check base numbers exist
        for base_num in expected_base_numbers:
            if base_num not in actual_numbers:
                result.add_warning(f"Missing base number directory: {base_num:02d}_*")

        # Check numbering gaps and conflicts
        for dir_name, number in numbered_dirs:
            if number % 10 == 0:  # Base number
                if number not in expected_base_numbers:
                    result.add_warning(f"Unexpected base number: {dir_name} ({number})")
            else:  # Intermediate number
                # Check if it's appropriately positioned
                lower_base = (number // 10) * 10
                lower_base + 10

                if lower_base not in actual_numbers:
                    result.add_warning(
                        f"Intermediate number without base: {dir_name} "
                        f"(missing {lower_base:02d}_*)"
                    )

    def _validate_sequential_numbering(
        self, result: ValidationResult, numbered_dirs: list[tuple]
    ) -> None:
        """Validate sequential numbering system."""
        if not numbered_dirs:
            return

        # Check for gaps in sequence
        numbers = [num for _, num in numbered_dirs]
        for i in range(len(numbers) - 1):
            if numbers[i + 1] - numbers[i] > 1:
                gap_start = numbers[i] + 1
                gap_end = numbers[i + 1] - 1
                result.add_warning(
                    f"Gap in numbering: {gap_start:02d} to {gap_end:02d}"
                )

        # Check if starts from 00
        if numbers[0] != 0:
            result.add_warning(
                f"Numbering doesn't start from 00, starts from {numbers[0]:02d}"
            )

    def _validate_tier_compliance(self, result: ValidationResult) -> None:
        """Validate directory tier compliance."""
        tier_counts = dict.fromkeys(DirectoryTier, 0)

        for item in self.vault_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                classification = self.config.classify_directory(item.name)
                tier_counts[classification.tier] += 1

                # Validate tier-specific rules
                if classification.tier == DirectoryTier.SYSTEM:
                    if not item.name.startswith("_"):
                        result.add_error(
                            f"System directory doesn't start with '_': {item.name}"
                        )

                elif classification.tier == DirectoryTier.CORE:
                    if classification.number is None:
                        result.add_error(
                            f"Core directory missing number prefix: {item.name}"
                        )

                elif classification.tier == DirectoryTier.AUXILIARY:
                    if item.name.startswith("_") or classification.number is not None:
                        result.add_warning(
                            f"Auxiliary directory has unexpected prefix: {item.name}"
                        )

        # Report tier distribution
        result.add_info(
            f"Directory distribution - System: {tier_counts[DirectoryTier.SYSTEM]}, "
            f"Core: {tier_counts[DirectoryTier.CORE]}, "
            f"Auxiliary: {tier_counts[DirectoryTier.AUXILIARY]}"
        )

    def _validate_readme_coverage(self, result: ValidationResult) -> None:
        """Validate README.md coverage."""
        missing_readmes = []

        for item in self.vault_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                readme_path = item / "README.md"
                if not readme_path.exists():
                    missing_readmes.append(item.name)

        if missing_readmes:
            result.add_warning(
                f"Directories missing README.md: {', '.join(missing_readmes)}"
            )
        else:
            result.add_info("All directories have README.md files")

    def _validate_metadata_compliance(self, result: ValidationResult) -> None:
        """Validate metadata compliance in files."""
        markdown_files = list(self.vault_path.rglob("*.md"))
        files_without_frontmatter = 0

        for md_file in markdown_files:
            if md_file.name == "README.md":
                continue  # Skip README files

            try:
                content = md_file.read_text(encoding="utf-8")
                if not content.startswith("---"):
                    files_without_frontmatter += 1
            except (OSError, UnicodeDecodeError):
                result.add_warning(f"Could not read file for metadata check: {md_file}")

        total_content_files = len(markdown_files) - len(
            list(self.vault_path.rglob("README.md"))
        )

        if total_content_files > 0:
            metadata_coverage = (
                (total_content_files - files_without_frontmatter)
                / total_content_files
                * 100
            )
            result.add_info(
                f"Metadata coverage: {metadata_coverage:.1f}% "
                f"({total_content_files - files_without_frontmatter}/"
                f"{total_content_files} files)"
            )

            if files_without_frontmatter > 0:
                result.add_warning(
                    f"{files_without_frontmatter} files missing frontmatter metadata"
                )

    def _check_unexpected_directories(
        self, result: ValidationResult, expected_structure: dict[str, dict[str, str]]
    ) -> None:
        """Check for unexpected directories in vault root."""
        expected_names: set[str] = set()

        for tier_dirs in expected_structure.values():
            expected_names.update(tier_dirs.keys())

        # Add standard allowed directories
        expected_names.update([".obsidian", ".git"])

        actual_dirs = {d.name for d in self.vault_path.iterdir() if d.is_dir()}
        unexpected = actual_dirs - expected_names

        if unexpected:
            result.add_warning(f"Unexpected directories found: {', '.join(unexpected)}")

    def _generate_statistics(self) -> dict[str, Any]:
        """Generate structure statistics."""
        tier_distribution: dict[str, int] = {tier.value: 0 for tier in DirectoryTier}

        stats: dict[str, Any] = {
            "total_directories": 0,
            "total_files": 0,
            "markdown_files": 0,
            "readme_files": 0,
            "tier_distribution": tier_distribution,
            "numbering_system": self.config.numbering_system.value,
            "largest_directory": None,
            "largest_directory_size": 0,
        }

        if not self.vault_path.exists():
            return stats

        for item in self.vault_path.rglob("*"):
            if item.is_file():
                stats["total_files"] += 1
                if item.suffix == ".md":
                    stats["markdown_files"] += 1
                    if item.name == "README.md":
                        stats["readme_files"] += 1

        for item in self.vault_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                stats["total_directories"] += 1

                # Count tier distribution
                classification = self.config.classify_directory(item.name)
                stats["tier_distribution"][classification.tier.value] += 1

                # Find largest directory
                try:
                    dir_size = sum(
                        f.stat().st_size for f in item.rglob("*") if f.is_file()
                    )
                    if dir_size > stats["largest_directory_size"]:
                        stats["largest_directory_size"] = dir_size
                        stats["largest_directory"] = item.name
                except OSError:
                    pass

        return stats


class StructureHealthMonitor:
    """Monitors structure health over time."""

    def __init__(self, vault_path: Path, hybrid_config: HybridStructureConfig):
        self.vault_path = vault_path
        self.config = hybrid_config
        self.validator = StructureValidator(vault_path, hybrid_config)
        self.health_log_path = vault_path / ".ckc" / "health_log.json"

    def run_health_check(self) -> ValidationResult:
        """Run health check and log results."""
        result = self.validator.validate_full_structure()

        # Log results
        self._log_health_result(result)

        return result

    def _log_health_result(self, result: ValidationResult) -> None:
        """Log health check result."""
        # Ensure log directory exists
        self.health_log_path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing log
        log_entries = []
        if self.health_log_path.exists():
            try:
                with open(self.health_log_path, encoding="utf-8") as f:
                    log_entries = json.load(f)
            except (json.JSONDecodeError, OSError):
                log_entries = []

        # Add new entry
        log_entries.append(result.to_dict())

        # Keep only last 100 entries
        log_entries = log_entries[-100:]

        # Save log
        try:
            with open(self.health_log_path, "w", encoding="utf-8") as f:
                json.dump(log_entries, f, indent=2, ensure_ascii=False)
        except OSError as e:
            print(f"Warning: Could not save health log: {e}")

    def get_health_trend(self, days: int = 7) -> dict[str, Any]:
        """Get health trend for specified number of days."""
        if not self.health_log_path.exists():
            return {"trend": "no_data", "entries": []}

        try:
            with open(self.health_log_path, encoding="utf-8") as f:
                log_entries = json.load(f)
        except (json.JSONDecodeError, OSError):
            return {"trend": "no_data", "entries": []}

        # Filter entries from last N days
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        recent_entries = []

        for entry in log_entries:
            try:
                entry_time = datetime.fromisoformat(entry["timestamp"]).timestamp()
                if entry_time >= cutoff_date:
                    recent_entries.append(entry)
            except (ValueError, KeyError):
                continue

        if not recent_entries:
            return {"trend": "no_recent_data", "entries": []}

        # Analyze trend
        passing_count = sum(1 for entry in recent_entries if entry.get("passed", False))
        total_count = len(recent_entries)

        trend_analysis = {
            "trend": "stable" if passing_count == total_count else "declining",
            "entries": recent_entries,
            "passing_rate": passing_count / total_count * 100,
            "total_checks": total_count,
            "latest_passed": recent_entries[-1].get("passed", False)
            if recent_entries
            else False,
        }

        return trend_analysis


def validate_structure(
    vault_path: Path, hybrid_config: HybridStructureConfig
) -> ValidationResult:
    """Convenience function to validate structure."""
    validator = StructureValidator(vault_path, hybrid_config)
    return validator.validate_full_structure()


def monitor_structure_health(
    vault_path: Path, hybrid_config: HybridStructureConfig
) -> ValidationResult:
    """Convenience function to run health monitoring."""
    monitor = StructureHealthMonitor(vault_path, hybrid_config)
    return monitor.run_health_check()
