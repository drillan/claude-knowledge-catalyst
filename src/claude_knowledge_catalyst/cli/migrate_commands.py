"""Migration CLI commands for CKC."""

import shutil
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn
from rich.table import Table

from ..core.config import CKCConfig, load_config
from ..core.hybrid_config import NumberingSystem
from ..sync.compatibility import MigrationSafetyValidator, StructureCompatibilityManager

console = Console()


class MigrationPlan:
    """Migration plan for structure conversion."""

    def __init__(self) -> None:
        self.operations = []
        self.estimated_time = 0.0
        self.backup_required = True
        self.safety_score = 100

    def add_directory_move(self, old_path: str, new_path: str) -> None:
        """Add directory move operation."""
        self.operations.append(
            {
                "type": "move_directory",
                "source": old_path,
                "target": new_path,
                "estimated_time": 5,  # seconds
            }
        )
        self.estimated_time += 5

    def add_directory_creation(self, path: str, description: str) -> None:
        """Add directory creation operation."""
        self.operations.append(
            {
                "type": "create_directory",
                "path": path,
                "description": description,
                "estimated_time": 1,
            }
        )
        self.estimated_time += 1

    def add_file_move(self, old_path: str, new_path: str) -> None:
        """Add file move operation."""
        self.operations.append(
            {
                "type": "move_file",
                "source": old_path,
                "target": new_path,
                "estimated_time": 0.1,
            }
        )
        self.estimated_time += 0.1

    def add_symlink_creation(self, link_path: str, target_path: str) -> None:
        """Add symlink creation operation."""
        self.operations.append(
            {
                "type": "create_symlink",
                "link": link_path,
                "target": target_path,
                "estimated_time": 0.5,
            }
        )
        self.estimated_time += 0.5


class MigrationResult:
    """Result of migration execution."""

    def __init__(self) -> None:
        self.success = False
        self.operations_completed = 0
        self.operations_total = 0
        self.backup_path = None
        self.errors = []
        self.warnings = []
        self.start_time = None
        self.end_time = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "operations_completed": self.operations_completed,
            "operations_total": self.operations_total,
            "backup_path": str(self.backup_path) if self.backup_path else None,
            "errors": self.errors,
            "warnings": self.warnings,
            "duration": (self.end_time - self.start_time).total_seconds()
            if self.start_time and self.end_time
            else None,
        }


class MigrationManager:
    """Manages structure migration operations."""

    def __init__(self, vault_path: Path, config: CKCConfig):
        self.vault_path = vault_path
        self.config = config
        self.compatibility = StructureCompatibilityManager(vault_path, config)

    def plan_migration(self, target_structure: str) -> MigrationPlan:
        """Create migration plan."""
        current_structure = self.compatibility.detect_current_structure()

        if current_structure == "legacy" and target_structure == "hybrid":
            return self._plan_legacy_to_hybrid()
        elif current_structure == "hybrid" and target_structure == "legacy":
            return self._plan_hybrid_to_legacy()
        else:
            raise ValueError(
                f"Migration not supported: {current_structure} → {target_structure}"
            )

    def _plan_legacy_to_hybrid(self) -> MigrationPlan:
        """Plan legacy to hybrid migration."""
        plan = MigrationPlan()

        # Directory mappings
        mappings = {
            "00_Inbox": "00_Catalyst_Lab",
            "01_Projects": "10_Projects",
            "02_Knowledge_Base": "20_Knowledge_Base",
            "03_Templates": "_templates",
            "04_Analytics": "Analytics",
            "05_Archive": "30_Wisdom_Archive",
        }

        # Check which directories exist and plan moves
        for old_dir, new_dir in mappings.items():
            old_path = self.vault_path / old_dir
            if old_path.exists():
                plan.add_directory_move(old_dir, new_dir)

        # Plan new directory creation
        new_dirs = [
            ("_attachments", "メディア・添付ファイル"),
            ("_scripts", "自動化スクリプト"),
            ("_docs", "システムドキュメント"),
            ("Archive", "非アクティブアーカイブ"),
            ("Evolution_Log", "改善・進化の記録"),
        ]

        for dir_name, description in new_dirs:
            plan.add_directory_creation(dir_name, description)

        # Plan Knowledge_Base subdirectory creation
        kb_subdirs = [
            "20_Knowledge_Base/Prompts/Templates",
            "20_Knowledge_Base/Prompts/Best_Practices",
            "20_Knowledge_Base/Prompts/Improvement_Log",
            "20_Knowledge_Base/Prompts/Domain_Specific",
            "20_Knowledge_Base/Code_Snippets/Python",
            "20_Knowledge_Base/Code_Snippets/JavaScript",
            "20_Knowledge_Base/Code_Snippets/TypeScript",
            "20_Knowledge_Base/Code_Snippets/Shell",
            "20_Knowledge_Base/Code_Snippets/Other_Languages",
            "20_Knowledge_Base/Concepts/AI_Fundamentals",
            "20_Knowledge_Base/Concepts/LLM_Architecture",
            "20_Knowledge_Base/Concepts/Development_Patterns",
            "20_Knowledge_Base/Concepts/Best_Practices",
            "20_Knowledge_Base/Resources/Documentation",
            "20_Knowledge_Base/Resources/Tutorials",
            "20_Knowledge_Base/Resources/Research_Papers",
            "20_Knowledge_Base/Resources/Tools_And_Services",
        ]

        for subdir in kb_subdirs:
            plan.add_directory_creation(subdir, "Knowledge base subdirectory")

        # Plan legacy compatibility symlinks if enabled
        if self.config.hybrid_structure.legacy_support:
            for old_dir, new_dir in mappings.items():
                plan.add_symlink_creation(old_dir, new_dir)

        return plan

    def _plan_hybrid_to_legacy(self) -> MigrationPlan:
        """Plan hybrid to legacy migration."""
        plan = MigrationPlan()

        # Reverse mappings
        mappings = {
            "00_Catalyst_Lab": "00_Inbox",
            "10_Projects": "01_Projects",
            "20_Knowledge_Base": "02_Knowledge_Base",
            "_templates": "03_Templates",
            "Analytics": "04_Analytics",
            "30_Wisdom_Archive": "05_Archive",
        }

        # Plan moves
        for hybrid_dir, legacy_dir in mappings.items():
            hybrid_path = self.vault_path / hybrid_dir
            if hybrid_path.exists():
                plan.add_directory_move(hybrid_dir, legacy_dir)

        return plan

    def execute_migration(
        self, plan: MigrationPlan, dry_run: bool = False
    ) -> MigrationResult:
        """Execute migration plan."""
        result = MigrationResult()
        result.start_time = datetime.now()
        result.operations_total = len(plan.operations)

        try:
            # Create backup if not dry run
            if not dry_run and plan.backup_required:
                result.backup_path = self._create_backup()

            # Execute operations
            for _i, operation in enumerate(plan.operations):
                if dry_run:
                    console.print(
                        f"Would execute: {operation['type']} - "
                        f"{operation.get('source', operation.get('path', ''))}"
                    )
                else:
                    success = self._execute_operation(operation)
                    if not success:
                        result.errors.append(f"Failed operation: {operation}")
                        break

                result.operations_completed += 1

            result.success = result.operations_completed == result.operations_total

        except Exception as e:
            result.errors.append(str(e))
            result.success = False

        result.end_time = datetime.now()
        return result

    def _create_backup(self) -> Path:
        """Create backup of vault."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = (
            self.vault_path.parent / f"{self.vault_path.name}_backup_{timestamp}"
        )

        shutil.copytree(self.vault_path, backup_path)
        return backup_path

    def _execute_operation(self, operation: dict) -> bool:
        """Execute single migration operation."""
        try:
            op_type = operation["type"]

            if op_type == "move_directory":
                source = self.vault_path / operation["source"]
                target = self.vault_path / operation["target"]

                if source.exists():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source), str(target))

            elif op_type == "create_directory":
                dir_path = self.vault_path / operation["path"]
                dir_path.mkdir(parents=True, exist_ok=True)

                # Create README
                readme_path = dir_path / "README.md"
                if not readme_path.exists():
                    readme_content = (
                        f"# {dir_path.name}\n\n{operation['description']}\n"
                    )
                    readme_path.write_text(readme_content, encoding="utf-8")

            elif op_type == "move_file":
                source = Path(operation["source"])
                target = Path(operation["target"])

                if source.exists():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source), str(target))

            elif op_type == "create_symlink":
                link_path = self.vault_path / operation["link"]
                target_path = self.vault_path / operation["target"]

                if target_path.exists() and not link_path.exists():
                    link_path.symlink_to(target_path, target_is_directory=True)

            return True

        except Exception as e:
            console.print(f"❌ Operation failed: {e}", style="red")
            return False


@click.group()
def migrate() -> None:
    """Migrate vault structure between different systems."""
    pass


@migrate.command()
@click.option("--config-path", type=click.Path(), help="Path to configuration file")
@click.option("--vault-path", type=click.Path(), help="Path to vault directory")
@click.option(
    "--to",
    type=click.Choice(["hybrid", "legacy"]),
    required=True,
    help="Target structure type",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without executing"
)
@click.option("--force", is_flag=True, help="Skip safety checks")
def plan(
    config_path: str | None,
    vault_path: str | None,
    to: str,
    dry_run: bool,
    force: bool,
) -> None:
    """Create and show migration plan."""
    try:
        # Load configuration
        config_file = (
            Path(config_path) if config_path else Path.cwd() / "ckc_config.yaml"
        )
        config = load_config(config_file)

        # Determine vault path
        if vault_path:
            vault_dir = Path(vault_path)
        else:
            obsidian_targets = [t for t in config.sync_targets if t.type == "obsidian"]
            if not obsidian_targets:
                console.print("❌ No Obsidian vault configured", style="red")
                return
            vault_dir = obsidian_targets[0].path

        if not vault_dir.exists():
            console.print(
                f"❌ Vault directory does not exist: {vault_dir}", style="red"
            )
            return

        # Safety validation
        if not force:
            console.print("🔍 Running safety checks...")
            validator = MigrationSafetyValidator(vault_dir, config)
            safety_result = validator.validate_migration_prerequisites()

            if not safety_result["safe_to_migrate"]:
                console.print("❌ Migration safety check failed:", style="red")
                for error in safety_result["errors"]:
                    console.print(f"  • {error}", style="red")
                return

            if safety_result["warnings"]:
                console.print("⚠️ Safety warnings:", style="yellow")
                for warning in safety_result["warnings"]:
                    console.print(f"  • {warning}", style="yellow")

        # Create migration plan
        console.print(f"📋 Creating migration plan to {to} structure...")
        migration_manager = MigrationManager(vault_dir, config)

        try:
            plan = migration_manager.plan_migration(to)
        except ValueError as e:
            console.print(f"❌ {e}", style="red")
            return

        # Show plan overview
        plan_panel = Panel(
            f"""Target Structure: {to.title()}
Operations: {len(plan.operations)}
Estimated Time: {plan.estimated_time:.1f} seconds
Backup Required: {"Yes" if plan.backup_required else "No"}
Safety Score: {plan.safety_score}/100""",
            title="📋 Migration Plan Overview",
            border_style="blue",
        )
        console.print(plan_panel)

        # Show operations table
        table = Table(title="🔄 Migration Operations")
        table.add_column("Step", style="cyan")
        table.add_column("Operation", style="white")
        table.add_column("Details", style="green")
        table.add_column("Time", style="yellow")

        for i, operation in enumerate(plan.operations, 1):
            op_type = operation["type"].replace("_", " ").title()

            if operation["type"] == "move_directory":
                details = f"{operation['source']} → {operation['target']}"
            elif operation["type"] == "create_directory":
                details = f"Create {operation['path']}"
            elif operation["type"] == "create_symlink":
                details = f"Link {operation['link']} → {operation['target']}"
            else:
                details = operation.get("path", "")

            table.add_row(str(i), op_type, details, f"{operation['estimated_time']}s")

        console.print(table)

        # Execute if not dry-run
        if not dry_run:
            console.print("\n💡 To execute this plan, run:")
            console.print(f"  ckc migrate execute --to {to}")
        else:
            console.print("\n🔍 This was a dry run. No changes were made.")

    except Exception as e:
        console.print(f"❌ Error creating migration plan: {e}", style="red")


@migrate.command()
@click.option("--config-path", type=click.Path(), help="Path to configuration file")
@click.option("--vault-path", type=click.Path(), help="Path to vault directory")
@click.option(
    "--to",
    type=click.Choice(["hybrid", "legacy"]),
    required=True,
    help="Target structure type",
)
@click.option(
    "--backup/--no-backup", default=True, help="Create backup before migration"
)
@click.option("--force", is_flag=True, help="Skip confirmation prompts")
def execute(
    config_path: str | None,
    vault_path: str | None,
    to: str,
    backup: bool,
    force: bool,
) -> None:
    """Execute migration to target structure."""
    try:
        # Load configuration
        config_file = (
            Path(config_path) if config_path else Path.cwd() / "ckc_config.yaml"
        )
        config = load_config(config_file)

        # Determine vault path
        if vault_path:
            vault_dir = Path(vault_path)
        else:
            obsidian_targets = [t for t in config.sync_targets if t.type == "obsidian"]
            if not obsidian_targets:
                console.print("❌ No Obsidian vault configured", style="red")
                return
            vault_dir = obsidian_targets[0].path

        if not vault_dir.exists():
            console.print(
                f"❌ Vault directory does not exist: {vault_dir}", style="red"
            )
            return

        # Create migration plan
        migration_manager = MigrationManager(vault_dir, config)
        plan = migration_manager.plan_migration(to)
        plan.backup_required = backup

        # Confirmation
        if not force:
            console.print(f"⚠️ About to migrate vault structure to {to}")
            console.print(f"📁 Vault: {vault_dir}")
            console.print(f"🔄 Operations: {len(plan.operations)}")
            console.print(f"💾 Backup: {'Yes' if backup else 'No'}")

            confirm = click.confirm("\nProceed with migration?")
            if not confirm:
                console.print("❌ Migration cancelled")
                return

        # Execute migration
        console.print(f"🚀 Starting migration to {to} structure...")

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Migrating...", total=len(plan.operations))

            result = MigrationResult()
            result.start_time = datetime.now()
            result.operations_total = len(plan.operations)

            try:
                # Create backup
                if backup:
                    progress.update(task, description="Creating backup...")
                    result.backup_path = migration_manager._create_backup()
                    console.print(f"💾 Backup created: {result.backup_path}")

                # Execute operations
                for i, operation in enumerate(plan.operations):
                    progress.update(
                        task, description=f"Step {i + 1}: {operation['type']}"
                    )

                    success = migration_manager._execute_operation(operation)
                    if not success:
                        result.errors.append(f"Failed: {operation}")
                        break

                    result.operations_completed += 1
                    progress.update(task, advance=1)

                result.success = result.operations_completed == result.operations_total

            except Exception as e:
                result.errors.append(str(e))
                result.success = False

            result.end_time = datetime.now()

        # Show results
        if result.success:
            console.print("✅ Migration completed successfully!", style="green")

            # Update configuration
            if to == "hybrid":
                config.hybrid_structure.enabled = True
                config.hybrid_structure.numbering_system = NumberingSystem.TEN_STEP
            else:
                config.hybrid_structure.enabled = False
                config.hybrid_structure.numbering_system = NumberingSystem.SEQUENTIAL

            config.save_to_file(config_file)
            console.print(f"💾 Configuration updated: {config_file}")

            # Show next steps
            console.print("\n💡 Next Steps:")
            if to == "hybrid":
                console.print("  1. Validate structure: ckc structure validate")
                console.print("  2. Check health: ckc structure health")
                console.print("  3. Start using hybrid features")
            else:
                console.print("  1. Verify legacy structure")
                console.print("  2. Update any custom scripts")
        else:
            console.print("❌ Migration failed!", style="red")
            for error in result.errors:
                console.print(f"  • {error}", style="red")

            if result.backup_path:
                console.print("\n🔄 To restore backup:")
                console.print(f"  rm -rf {vault_dir}")
                console.print(f"  mv {result.backup_path} {vault_dir}")

    except Exception as e:
        console.print(f"❌ Error executing migration: {e}", style="red")


@migrate.command()
@click.option("--config-path", type=click.Path(), help="Path to configuration file")
@click.option("--vault-path", type=click.Path(), help="Path to vault directory")
def status(config_path: str | None, vault_path: str | None) -> None:
    """Show migration status and history."""
    try:
        # Load configuration
        config_file = (
            Path(config_path) if config_path else Path.cwd() / "ckc_config.yaml"
        )
        config = load_config(config_file)

        # Show current structure
        if vault_path:
            vault_dir = Path(vault_path)
        else:
            obsidian_targets = [t for t in config.sync_targets if t.type == "obsidian"]
            if obsidian_targets:
                vault_dir = obsidian_targets[0].path
            else:
                vault_dir = None

        # Current configuration
        table = Table(title="📊 Migration Status")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")

        table.add_row("Hybrid Enabled", str(config.hybrid_structure.enabled))
        table.add_row(
            "Numbering System", config.hybrid_structure.numbering_system.value.title()
        )
        table.add_row("Migration Mode", config.hybrid_structure.migration_mode.title())
        table.add_row("Legacy Support", str(config.hybrid_structure.legacy_support))

        if vault_dir and vault_dir.exists():
            compat = StructureCompatibilityManager(vault_dir, config)
            current_structure = compat.detect_current_structure()
            table.add_row("Current Structure", current_structure.title())

        console.print(table)

        # Migration history
        if config.structure_migration_log:
            console.print("\n📜 Migration History:")
            for entry in config.structure_migration_log[-5:]:  # Last 5 entries
                timestamp = entry.get("timestamp", "Unknown")
                from_version = entry.get("from_version", "Unknown")
                to_version = entry.get("to_version", "Unknown")
                migration_type = entry.get("migration_type", "Unknown")

                console.print(
                    f"  • {timestamp}: {from_version} → {to_version} ({migration_type})"
                )

    except Exception as e:
        console.print(f"❌ Error checking migration status: {e}", style="red")


if __name__ == "__main__":
    migrate()
