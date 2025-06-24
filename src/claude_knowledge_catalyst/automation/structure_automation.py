"""Structure automation and validation tools for CKC."""

import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from ..core.config import CKCConfig
from ..core.metadata import KnowledgeMetadata, MetadataManager
from ..core.structure_validator import StructureHealthMonitor, StructureValidator


class AutomatedStructureManager:
    """Manages automated structure maintenance and optimization."""

    def __init__(self, vault_path: Path, config: CKCConfig):
        self.vault_path = vault_path
        self.config = config
        self.hybrid_config = config.hybrid_structure
        self.validator = StructureValidator(vault_path, self.hybrid_config)
        self.health_monitor = StructureHealthMonitor(vault_path, self.hybrid_config)
        self.metadata_manager = MetadataManager()

        # Automation settings
        self.automation_log_path = vault_path / ".ckc" / "automation_log.json"
        self.last_maintenance_path = vault_path / ".ckc" / "last_maintenance.json"

    def run_automated_maintenance(self) -> dict[str, Any]:
        """Run comprehensive automated maintenance."""
        maintenance_result: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "tasks_completed": [],
            "issues_found": [],
            "issues_fixed": [],
            "warnings": [],
            "performance": {},
        }

        start_time = datetime.now()

        try:
            # 1. Structure validation and auto-fix
            validation_task = self._run_structure_validation()
            maintenance_result["tasks_completed"].append("structure_validation")
            # Merge results safely
            for key, value in validation_task.items():
                if key in maintenance_result and isinstance(value, list):
                    maintenance_result[key].extend(value)
                else:
                    maintenance_result[key] = value

            # 2. Health monitoring
            health_task = self._run_health_monitoring()
            maintenance_result["tasks_completed"].append("health_monitoring")
            # Merge results safely
            for key, value in health_task.items():
                if key in maintenance_result and isinstance(value, list):
                    maintenance_result[key].extend(value)
                else:
                    maintenance_result[key] = value

            # 3. Metadata consistency check
            metadata_task = self._check_metadata_consistency()
            maintenance_result["tasks_completed"].append("metadata_consistency")
            # Merge results safely
            for key, value in metadata_task.items():
                if key in maintenance_result and isinstance(value, list):
                    maintenance_result[key].extend(value)
                else:
                    maintenance_result[key] = value

            # 4. Directory optimization
            optimization_task = self._optimize_directory_structure()
            maintenance_result["tasks_completed"].append("directory_optimization")
            # Merge results safely
            for key, value in optimization_task.items():
                if key in maintenance_result and isinstance(value, list):
                    maintenance_result[key].extend(value)
                else:
                    maintenance_result[key] = value

            # 5. Cleanup operations
            cleanup_task = self._run_cleanup_operations()
            maintenance_result["tasks_completed"].append("cleanup_operations")
            # Merge results safely
            for key, value in cleanup_task.items():
                if key in maintenance_result and isinstance(value, list):
                    maintenance_result[key].extend(value)
                else:
                    maintenance_result[key] = value

            # Record performance
            end_time = datetime.now()
            maintenance_result["performance"] = {
                "duration_seconds": (end_time - start_time).total_seconds(),
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
            }

            # Log maintenance
            self._log_maintenance_result(maintenance_result)

            return maintenance_result

        except Exception as e:
            maintenance_result["error"] = str(e)
            maintenance_result["status"] = "failed"
            return maintenance_result

    def _run_structure_validation(self) -> dict[str, Any]:
        """Run structure validation with auto-fix."""
        result: dict[str, Any] = {
            "validation_result": None,
            "auto_fixes": [],
            "issues_found": [],
            "issues_fixed": [],
            "warnings": [],
        }

        # Run validation
        validation_result = self.validator.validate_full_structure()
        result["validation_result"] = validation_result.to_dict()

        # Auto-fix issues where possible
        if not validation_result.passed:
            fixes = self._attempt_auto_fixes(validation_result)
            result["auto_fixes"] = fixes
            result["issues_found"].extend(validation_result.errors)
            result["issues_fixed"].extend(fixes)

        if validation_result.warnings:
            result["warnings"].extend(validation_result.warnings)

        return result

    def _run_health_monitoring(self) -> dict[str, Any]:
        """Run health monitoring and trend analysis."""
        result = {"health_status": None, "trends": None}

        # Current health check
        health_result = self.health_monitor.run_health_check()
        result["health_status"] = health_result.to_dict()

        # Trend analysis
        trend_data = self.health_monitor.get_health_trend(days=7)
        result["trends"] = trend_data

        # Health recommendations
        recommendations = self._generate_health_recommendations(
            health_result, trend_data
        )
        result["health_recommendations"] = recommendations

        return result

    def _check_metadata_consistency(self) -> dict[str, Any]:
        """Check and fix metadata consistency issues."""
        result: dict[str, Any] = {
            "files_checked": 0,
            "metadata_issues": [],
            "metadata_fixes": [],
        }

        # Find all markdown files
        md_files = list(self.vault_path.rglob("*.md"))
        result["files_checked"] = len(md_files)

        for md_file in md_files:
            if md_file.name == "README.md":
                continue

            try:
                # Check metadata
                metadata = self.metadata_manager.extract_metadata_from_file(md_file)
                issues = self._analyze_metadata_issues(metadata, md_file)

                if issues:
                    result["metadata_issues"].extend(issues)

                    # Auto-fix if enabled
                    if self.hybrid_config.auto_enhancement:
                        fixes = self._fix_metadata_issues(md_file, metadata, issues)
                        result["metadata_fixes"].extend(fixes)

            except Exception as e:
                result["metadata_issues"].append(
                    {"file": str(md_file), "issue": f"Error reading metadata: {e}"}
                )

        return result

    def _optimize_directory_structure(self) -> dict[str, Any]:
        """Optimize directory structure organization."""
        result: dict[str, Any] = {
            "optimizations": [],
            "moves_suggested": [],
            "empty_dirs_removed": 0,
        }

        # Remove empty directories
        empty_dirs = self._find_empty_directories()
        for empty_dir in empty_dirs:
            try:
                empty_dir.rmdir()
                result["empty_dirs_removed"] += 1
                result["optimizations"].append(
                    f"Removed empty directory: {empty_dir.name}"
                )
            except OSError:
                pass  # Directory not actually empty

        # Suggest file moves for better organization
        if self.hybrid_config.auto_classification:
            move_suggestions = self._analyze_file_placement()
            result["moves_suggested"] = move_suggestions

        return result

    def _run_cleanup_operations(self) -> dict[str, Any]:
        """Run cleanup operations."""
        result = {
            "temp_files_removed": 0,
            "old_backups_removed": 0,
            "log_files_rotated": 0,
        }

        # Clean temporary files
        temp_patterns = ["*.tmp", "*.temp", ".DS_Store", "Thumbs.db"]
        for pattern in temp_patterns:
            temp_files = list(self.vault_path.rglob(pattern))
            for temp_file in temp_files:
                try:
                    temp_file.unlink()
                    result["temp_files_removed"] += 1
                except OSError:
                    pass

        # Clean old backups (older than 30 days)
        backup_dir = self.vault_path.parent
        cutoff_date = datetime.now() - timedelta(days=30)

        for item in backup_dir.iterdir():
            if item.name.startswith(f"{self.vault_path.name}_backup_"):
                try:
                    # Parse backup timestamp
                    timestamp_str = item.name.split("_backup_")[1]
                    backup_date = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")

                    if backup_date < cutoff_date:
                        if item.is_dir():
                            shutil.rmtree(item)
                        else:
                            item.unlink()
                        result["old_backups_removed"] += 1
                except (ValueError, OSError):
                    pass

        # Rotate log files
        log_rotation_count = self._rotate_log_files()
        result["log_files_rotated"] = log_rotation_count

        return result

    def _attempt_auto_fixes(self, validation_result) -> list[str]:
        """Attempt to automatically fix validation issues."""
        fixes = []

        for error in validation_result.errors:
            if "Missing directory" in error:
                # Extract directory name
                dir_name = error.split(": ")[-1]
                dir_path = self.vault_path / dir_name

                try:
                    dir_path.mkdir(parents=True, exist_ok=True)

                    # Create README
                    readme_path = dir_path / "README.md"
                    if not readme_path.exists():
                        readme_content = (
                            f"# {dir_name}\n\nAutomatically created directory.\n"
                        )
                        readme_path.write_text(readme_content, encoding="utf-8")

                    fixes.append(f"Created missing directory: {dir_name}")
                except Exception as e:
                    fixes.append(f"Failed to create {dir_name}: {e}")

            elif "Missing README.md" in error:
                # Extract directory name
                dir_name = error.split(" in ")[-1]
                readme_path = self.vault_path / dir_name / "README.md"

                try:
                    readme_content = f"# {dir_name}\n\nAutomatically created README.\n"
                    readme_path.write_text(readme_content, encoding="utf-8")
                    fixes.append(f"Created README for: {dir_name}")
                except Exception as e:
                    fixes.append(f"Failed to create README for {dir_name}: {e}")

        return fixes

    def _analyze_metadata_issues(
        self, metadata: KnowledgeMetadata, file_path: Path
    ) -> list[dict[str, str]]:
        """Analyze metadata for common issues."""
        issues = []

        # Check for missing required fields
        if not metadata.title or metadata.title == "Untitled":
            issues.append(
                {
                    "file": str(file_path),
                    "type": "missing_title",
                    "issue": "File has no title or generic title",
                }
            )

        # Check for empty or minimal tags
        if len(metadata.tags) < 2:
            issues.append(
                {
                    "file": str(file_path),
                    "type": "insufficient_tags",
                    "issue": "File has fewer than 2 tags",
                }
            )

        # Check for outdated content (no updates in 6 months)
        if metadata.updated < datetime.now() - timedelta(days=180):
            issues.append(
                {
                    "file": str(file_path),
                    "type": "outdated_content",
                    "issue": "Content hasn't been updated in 6+ months",
                }
            )

        # Check for missing category
        if not metadata.category:
            issues.append(
                {
                    "file": str(file_path),
                    "type": "missing_category",
                    "issue": "File has no category assigned",
                }
            )

        return issues

    def _fix_metadata_issues(
        self, file_path: Path, metadata: KnowledgeMetadata, issues: list[dict]
    ) -> list[str]:
        """Attempt to fix metadata issues automatically."""
        fixes = []

        for issue in issues:
            issue_type = issue["type"]

            if issue_type == "missing_title":
                # Generate title from filename
                new_title = file_path.stem.replace("_", " ").replace("-", " ").title()
                metadata.title = new_title
                fixes.append(f"Generated title '{new_title}' for {file_path.name}")

            elif issue_type == "insufficient_tags":
                # Suggest tags based on content
                try:
                    content = file_path.read_text(encoding="utf-8")
                    # Note: suggest_tags method may not be implemented
                    if hasattr(self.metadata_manager, "suggest_tags"):
                        suggested_tags = self.metadata_manager.suggest_tags(
                            content, metadata.tags
                        )
                        if suggested_tags:
                            metadata.tags.extend(
                                suggested_tags[:3]
                            )  # Add up to 3 suggestions
                        fixes.append(
                            f"Added suggested tags {suggested_tags[:3]} to "
                            f"{file_path.name}"
                        )
                except Exception:
                    pass

            elif issue_type == "missing_category":
                # Infer category from directory location
                category = self._infer_category_from_path(file_path)
                if category:
                    metadata.category = category
                    fixes.append(f"Inferred category '{category}' for {file_path.name}")

        # Update file if fixes were made
        if fixes:
            try:
                self.metadata_manager.update_file_metadata(file_path, metadata)
            except Exception as e:
                fixes.append(f"Failed to update metadata for {file_path.name}: {e}")

        return fixes

    def _generate_health_recommendations(self, health_result, trend_data) -> list[str]:
        """Generate health improvement recommendations."""
        recommendations = []

        # Based on current health
        if not health_result.passed:
            recommendations.append(
                "Address validation errors to improve structure health"
            )

        if health_result.warnings:
            recommendations.append("Review and resolve validation warnings")

        # Based on trends
        if trend_data.get("trend") == "declining":
            recommendations.append(
                "Structure health is declining - investigate recent changes"
            )

        if trend_data.get("passing_rate", 100) < 80:
            recommendations.append("Passing rate below 80% - consider structure review")

        # General recommendations
        stats = health_result.statistics
        if stats.get("readme_files", 0) < stats.get("total_directories", 1):
            recommendations.append("Add README files to directories without them")

        if stats.get("metadata_coverage", 100) < 80:
            recommendations.append("Improve metadata coverage for better organization")

        return recommendations

    def _find_empty_directories(self) -> list[Path]:
        """Find empty directories that can be cleaned up."""
        empty_dirs = []

        for dir_path in self.vault_path.rglob("*/"):
            if dir_path.is_dir() and not dir_path.name.startswith("."):
                # Check if directory is empty (no files, only potentially empty subdirs)
                has_files = any(item.is_file() for item in dir_path.rglob("*"))
                if not has_files:
                    empty_dirs.append(dir_path)

        return empty_dirs

    def _analyze_file_placement(self) -> list[dict[str, str]]:
        """Analyze if files are optimally placed."""
        suggestions = []

        # This would implement sophisticated analysis
        # For now, return empty list
        return suggestions

    def _infer_category_from_path(self, file_path: Path) -> str | None:
        """Infer category from file path."""
        path_str = str(file_path).lower()

        if "prompt" in path_str:
            return "prompt"
        elif "code" in path_str or "snippet" in path_str:
            return "code"
        elif "concept" in path_str:
            return "concept"
        elif "resource" in path_str:
            return "resource"
        elif "project" in path_str:
            return "project_log"
        elif "experiment" in path_str or "catalyst" in path_str:
            return "experiment"

        return None

    def _rotate_log_files(self) -> int:
        """Rotate log files to prevent excessive growth."""
        rotated_count = 0

        log_files = [
            self.automation_log_path,
            self.vault_path / ".ckc" / "health_log.json",
        ]

        for log_file in log_files:
            if log_file.exists():
                try:
                    # Read current log
                    with open(log_file) as f:
                        log_data = json.load(f)

                    # Keep only last 100 entries
                    if isinstance(log_data, list) and len(log_data) > 100:
                        log_data = log_data[-100:]

                        # Write back
                        with open(log_file, "w") as f:
                            json.dump(log_data, f, indent=2)

                        rotated_count += 1
                except (json.JSONDecodeError, OSError):
                    pass

        return rotated_count

    def _log_maintenance_result(self, result: dict[str, Any]) -> None:
        """Log maintenance result."""
        # Ensure log directory exists
        self.automation_log_path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing log
        log_entries = []
        if self.automation_log_path.exists():
            try:
                with open(self.automation_log_path) as f:
                    log_entries = json.load(f)
            except (json.JSONDecodeError, OSError):
                log_entries = []

        # Add new entry
        log_entries.append(result)

        # Keep only last 50 entries
        log_entries = log_entries[-50:]

        # Save log
        try:
            with open(self.automation_log_path, "w") as f:
                json.dump(log_entries, f, indent=2, ensure_ascii=False)
        except OSError:
            pass

        # Update last maintenance timestamp
        try:
            with open(self.last_maintenance_path, "w") as f:
                json.dump(
                    {
                        "timestamp": result["timestamp"],
                        "status": "completed",
                        "duration": result["performance"]["duration_seconds"],
                    },
                    f,
                )
        except OSError:
            pass

    def should_run_maintenance(self) -> bool:
        """Check if maintenance should be run based on schedule."""
        if not self.last_maintenance_path.exists():
            return True

        try:
            with open(self.last_maintenance_path) as f:
                last_maintenance = json.load(f)

            last_time = datetime.fromisoformat(last_maintenance["timestamp"])

            # Run maintenance daily
            return datetime.now() - last_time > timedelta(days=1)

        except (json.JSONDecodeError, OSError, ValueError):
            return True

    def get_maintenance_history(self, days: int = 7) -> list[dict[str, Any]]:
        """Get maintenance history for specified days."""
        if not self.automation_log_path.exists():
            return []

        try:
            with open(self.automation_log_path) as f:
                log_entries = json.load(f)
        except (json.JSONDecodeError, OSError):
            return []

        # Filter by date
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_entries = []

        for entry in log_entries:
            try:
                entry_time = datetime.fromisoformat(entry["timestamp"])
                if entry_time >= cutoff_date:
                    recent_entries.append(entry)
            except (ValueError, KeyError):
                continue

        return recent_entries


class ScheduledAutomation:
    """Manages scheduled automation tasks."""

    def __init__(self, vault_path: Path, config: CKCConfig):
        self.vault_path = vault_path
        self.config = config
        self.automation_manager = AutomatedStructureManager(vault_path, config)

    def run_daily_maintenance(self) -> dict[str, Any]:
        """Run daily maintenance tasks."""
        if not self.automation_manager.should_run_maintenance():
            return {"status": "skipped", "reason": "maintenance not due"}

        return self.automation_manager.run_automated_maintenance()

    def run_weekly_optimization(self) -> dict[str, Any]:
        """Run weekly optimization tasks."""
        # More intensive optimization tasks
        result = {"timestamp": datetime.now().isoformat(), "optimization_tasks": []}

        # Deep structure analysis
        # Metadata quality analysis
        # Performance optimization

        return result

    def run_monthly_cleanup(self) -> dict[str, Any]:
        """Run monthly cleanup tasks."""
        # Major cleanup operations
        result = {"timestamp": datetime.now().isoformat(), "cleanup_tasks": []}

        # Archive old content
        # Compress logs
        # Update statistics

        return result


def run_automated_maintenance(vault_path: Path, config: CKCConfig) -> dict[str, Any]:
    """Convenience function to run automated maintenance."""
    automation_manager = AutomatedStructureManager(vault_path, config)
    return automation_manager.run_automated_maintenance()
