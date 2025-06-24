"""Structure management CLI commands for CKC."""

from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from ..core.config import CKCConfig, load_config
from ..core.hybrid_config import NumberingSystem
from ..core.metadata import MetadataManager
from ..core.structure_validator import StructureHealthMonitor, validate_structure
from ..sync.compatibility import (
    BackwardCompatibilityManager,
    StructureCompatibilityManager,
)
from ..sync.hybrid_manager import HybridObsidianVaultManager

console = Console()


@click.group()
def structure() -> None:
    """Manage vault structure configuration."""
    pass


@structure.command()
@click.option("--config-path", type=click.Path(), help="Path to configuration file")
@click.option("--vault-path", type=click.Path(), help="Path to vault directory")
def status(config_path: str | None, vault_path: str | None) -> None:
    """Show current structure status."""
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
            # Get from first obsidian sync target
            obsidian_targets = [t for t in config.sync_targets if t.type == "obsidian"]
            if not obsidian_targets:
                console.print("❌ No Obsidian vault configured", style="red")
                return
            vault_dir = obsidian_targets[0].path

        # Create compatibility manager
        compat_manager = BackwardCompatibilityManager(vault_dir, config)
        struct_compat = StructureCompatibilityManager(vault_dir, config)

        # Detect current structure
        current_structure = struct_compat.detect_current_structure()

        # Create status table
        table = Table(title="🏗️ Structure Status")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        table.add_column("Status", style="green")

        # Basic information
        table.add_row(
            "Vault Path", str(vault_dir), "✅" if vault_dir.exists() else "❌"
        )
        table.add_row("Current Structure", current_structure.title(), "ℹ️")
        table.add_row(
            "Hybrid Enabled",
            str(config.hybrid_structure.enabled),
            "✅" if config.hybrid_structure.enabled else "⏸️",
        )
        table.add_row(
            "Numbering System",
            config.hybrid_structure.numbering_system.value.title(),
            "ℹ️",
        )
        table.add_row(
            "Auto Classification",
            str(config.hybrid_structure.auto_classification),
            "✅" if config.hybrid_structure.auto_classification else "⏸️",
        )
        table.add_row(
            "Legacy Support",
            str(config.hybrid_structure.legacy_support),
            "✅" if config.hybrid_structure.legacy_support else "⚠️",
        )

        console.print(table)

        # Compatibility check
        issues = compat_manager.validate_compatibility()
        if issues:
            console.print("\n⚠️ Compatibility Issues:", style="yellow")
            for issue in issues:
                console.print(f"  • {issue}", style="yellow")
        else:
            console.print("\n✅ No compatibility issues detected", style="green")

        # Structure validation if vault exists and hybrid is enabled
        if vault_dir.exists() and config.hybrid_structure.enabled:
            console.print("\n🔍 Running structure validation...")
            validation_result = validate_structure(vault_dir, config.hybrid_structure)

            if validation_result.passed:
                console.print("✅ Structure validation passed", style="green")
            else:
                console.print("❌ Structure validation failed", style="red")
                for error in validation_result.errors:
                    console.print(f"  • {error}", style="red")

            if validation_result.warnings:
                console.print("⚠️ Warnings:", style="yellow")
                for warning in validation_result.warnings:
                    console.print(f"  • {warning}", style="yellow")

        # Show recommendations
        _show_recommendations(config, current_structure)

    except Exception as e:
        console.print(f"❌ Error checking structure status: {e}", style="red")


@structure.command()
@click.option("--config-path", type=click.Path(), help="Path to configuration file")
@click.option("--vault-path", type=click.Path(), help="Path to vault directory")
@click.option("--fix", is_flag=True, help="Automatically fix issues where possible")
def validate(config_path: str | None, vault_path: str | None, fix: bool) -> None:
    """Validate structure integrity."""
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
            # Get from first obsidian sync target
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

        # Run validation
        console.print("🔍 Validating structure integrity...")
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Validating...", total=None)
            validation_result = validate_structure(vault_dir, config.hybrid_structure)
            progress.update(task, completed=True)

        # Show results
        console.print(validation_result)

        # Show statistics
        if validation_result.statistics:
            stats = validation_result.statistics
            stats_panel = Panel(
                f"""Total Directories: {stats.get("total_directories", 0)}
Total Files: {stats.get("total_files", 0)}
Markdown Files: {stats.get("markdown_files", 0)}
README Coverage: {stats.get("readme_files", 0)}/{stats.get("total_directories", 0)}

Tier Distribution:
  • System: {stats.get("tier_distribution", {}).get("system", 0)}
  • Core: {stats.get("tier_distribution", {}).get("core", 0)}
  • Auxiliary: {stats.get("tier_distribution", {}).get("auxiliary", 0)}

Largest Directory: {stats.get("largest_directory", "N/A")}
({stats.get("largest_directory_size", 0)} bytes)""",
                title="📊 Structure Statistics",
                border_style="blue",
            )
            console.print(stats_panel)

        # Auto-fix if requested
        if fix and not validation_result.passed:
            console.print("\n🔧 Attempting to fix issues...")
            _attempt_auto_fix(vault_dir, config, validation_result)

    except Exception as e:
        console.print(f"❌ Error validating structure: {e}", style="red")


@structure.command()
@click.option("--config-path", type=click.Path(), help="Path to configuration file")
@click.option("--vault-path", type=click.Path(), help="Path to vault directory")
@click.option("--days", default=7, help="Number of days to show trend for")
def health(config_path: str | None, vault_path: str | None, days: int) -> None:
    """Show structure health monitoring."""
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
            # Get from first obsidian sync target
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

        # Run health check
        console.print("🏥 Running health check...")
        monitor = StructureHealthMonitor(vault_dir, config.hybrid_structure)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Health check...", total=None)
            current_result = monitor.run_health_check()
            progress.update(task, completed=True)

        # Show current health
        status_color = "green" if current_result.passed else "red"
        console.print(
            f"\n🏥 Current Health: [bold {status_color}]"
            f"{'HEALTHY' if current_result.passed else 'ISSUES'}[/bold {status_color}]"
        )

        if current_result.errors:
            console.print("\n❌ Current Issues:", style="red")
            for error in current_result.errors:
                console.print(f"  • {error}", style="red")

        if current_result.warnings:
            console.print("\n⚠️ Warnings:", style="yellow")
            for warning in current_result.warnings:
                console.print(f"  • {warning}", style="yellow")

        # Show trend
        trend_data = monitor.get_health_trend(days)
        if trend_data["trend"] != "no_data":
            console.print(f"\n📈 Health Trend ({days} days):")
            console.print(f"  • Passing Rate: {trend_data['passing_rate']:.1f}%")
            console.print(f"  • Total Checks: {trend_data['total_checks']}")
            console.print(
                f"  • Latest Status: "
                f"{'✅ PASS' if trend_data['latest_passed'] else '❌ FAIL'}"
            )

            trend_status = (
                "📈 Improving" if trend_data["passing_rate"] > 80 else "📉 Declining"
            )
            console.print(f"  • Trend: {trend_status}")
        else:
            console.print("\n📊 No historical health data available")

    except Exception as e:
        console.print(f"❌ Error checking structure health: {e}", style="red")


@structure.command()
@click.option("--config-path", type=click.Path(), help="Path to configuration file")
@click.option(
    "--enable/--disable", default=None, help="Enable or disable hybrid structure"
)
@click.option(
    "--numbering-system",
    type=click.Choice(["sequential", "ten_step"]),
    help="Set numbering system",
)
@click.option(
    "--auto-classification/--no-auto-classification",
    default=None,
    help="Enable or disable auto classification",
)
@click.option(
    "--legacy-support/--no-legacy-support",
    default=None,
    help="Enable or disable legacy support",
)
def configure(
    config_path: str | None,
    enable: bool | None,
    numbering_system: str | None,
    auto_classification: bool | None,
    legacy_support: bool | None,
) -> None:
    """Configure hybrid structure settings."""
    try:
        # Load configuration
        config_file = (
            Path(config_path) if config_path else Path.cwd() / "ckc_config.yaml"
        )
        config = load_config(config_file)

        changes_made = False

        # Apply changes
        if enable is not None:
            config.hybrid_structure.enabled = enable
            changes_made = True
            console.print(f"✅ Hybrid structure {'enabled' if enable else 'disabled'}")

        if numbering_system:
            config.hybrid_structure.numbering_system = NumberingSystem(numbering_system)
            changes_made = True
            console.print(f"✅ Numbering system set to: {numbering_system}")

        if auto_classification is not None:
            config.hybrid_structure.auto_classification = auto_classification
            changes_made = True
            console.print(
                f"✅ Auto classification "
                f"{'enabled' if auto_classification else 'disabled'}"
            )

        if legacy_support is not None:
            config.hybrid_structure.legacy_support = legacy_support
            changes_made = True
            console.print(
                f"✅ Legacy support {'enabled' if legacy_support else 'disabled'}"
            )

        if changes_made:
            # Save configuration
            config.save_to_file(config_file)
            console.print(f"\n💾 Configuration saved to: {config_file}")

            # Show recommendations after changes
            if enable and config.hybrid_structure.enabled:
                console.print("\n💡 Next Steps:")
                console.print("  1. Initialize vault structure: ckc structure init")
                console.print("  2. Validate structure: ckc structure validate")
                console.print("  3. Run health check: ckc structure health")
        else:
            console.print("ℹ️ No changes specified")

    except Exception as e:
        console.print(f"❌ Error configuring structure: {e}", style="red")


@structure.command()
@click.option("--config-path", type=click.Path(), help="Path to configuration file")
@click.option("--vault-path", type=click.Path(), help="Path to vault directory")
@click.option("--force", is_flag=True, help="Force initialization even if vault exists")
def init(config_path: str | None, vault_path: str | None, force: bool) -> None:
    """Initialize hybrid structure in vault."""
    try:
        # Load configuration
        config_file = (
            Path(config_path) if config_path else Path.cwd() / "ckc_config.yaml"
        )
        config = load_config(config_file)

        if not config.hybrid_structure.enabled:
            console.print(
                "❌ Hybrid structure is not enabled in configuration", style="red"
            )
            console.print("💡 Enable with: ckc structure configure --enable")
            return

        # Determine vault path
        if vault_path:
            vault_dir = Path(vault_path)
        else:
            # Get from first obsidian sync target
            obsidian_targets = [t for t in config.sync_targets if t.type == "obsidian"]
            if not obsidian_targets:
                console.print("❌ No Obsidian vault configured", style="red")
                console.print(
                    "💡 Add vault with: ckc sync add vault obsidian /path/to/vault"
                )
                return
            vault_dir = obsidian_targets[0].path

        # Check if vault already exists
        if vault_dir.exists() and not force:
            console.print(
                f"⚠️ Vault directory already exists: {vault_dir}", style="yellow"
            )
            console.print(
                "💡 Use --force to initialize anyway, or specify different path"
            )
            return

        # Initialize vault
        console.print(f"🏗️ Initializing hybrid structure at: {vault_dir}")

        metadata_manager = MetadataManager()
        vault_manager = HybridObsidianVaultManager(vault_dir, metadata_manager, config)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Initializing vault...", total=None)
            success = vault_manager.initialize_vault()
            progress.update(task, completed=True)

        if success:
            console.print(
                "✅ Hybrid structure initialized successfully!", style="green"
            )

            # Show structure info
            structure_info = vault_manager.get_structure_info()
            info_panel = Panel(
                f"""Structure Version: {structure_info["structure_version"]}
Numbering System: {structure_info["numbering_system"]}
Auto Classification: {structure_info["auto_classification"]}
Directory Count: {structure_info["directory_count"]}""",
                title="📋 Structure Information",
                border_style="green",
            )
            console.print(info_panel)

            # Next steps
            console.print("\n💡 Next Steps:")
            console.print("  1. Validate structure: ckc structure validate")
            console.print("  2. Start syncing files: ckc sync run")
            console.print("  3. Monitor health: ckc structure health")
        else:
            console.print("❌ Failed to initialize hybrid structure", style="red")

    except Exception as e:
        console.print(f"❌ Error initializing structure: {e}", style="red")


def _show_recommendations(config: CKCConfig, current_structure: str) -> None:
    """Show recommendations based on current configuration."""
    recommendations = []

    if not config.hybrid_structure.enabled:
        recommendations.append(
            "Consider enabling hybrid structure for improved organization"
        )

    if current_structure == "legacy" and config.hybrid_structure.enabled:
        recommendations.append(
            "Run migration to upgrade to hybrid structure: ckc migrate"
        )

    if (
        config.hybrid_structure.enabled
        and not config.hybrid_structure.auto_classification
    ):
        recommendations.append(
            "Enable auto-classification for better file organization"
        )

    if (
        current_structure == "hybrid"
        and not config.hybrid_structure.structure_validation
    ):
        recommendations.append(
            "Enable structure validation for better quality assurance"
        )

    if recommendations:
        console.print("\n💡 Recommendations:", style="blue")
        for rec in recommendations:
            console.print(f"  • {rec}", style="blue")


def _attempt_auto_fix(vault_dir: Path, config: CKCConfig, validation_result) -> None:
    """Attempt to automatically fix validation issues."""
    fixed_count = 0

    # Try to create missing README files
    for error in validation_result.errors:
        if "Missing directory" in error and "README.md" not in error:
            # Try to create missing directory
            dir_name = error.split(": ")[-1]
            dir_path = vault_dir / dir_name
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                readme_path = dir_path / "README.md"
                readme_content = f"# {dir_name}\n\nAutomatically created directory.\n"
                readme_path.write_text(readme_content, encoding="utf-8")
                console.print(f"✅ Fixed: Created directory and README for {dir_name}")
                fixed_count += 1
            except Exception as e:
                console.print(f"❌ Could not fix {dir_name}: {e}")

    if fixed_count > 0:
        console.print(f"\n🔧 Auto-fixed {fixed_count} issues")
        console.print("💡 Run validate again to check remaining issues")
    else:
        console.print("⚠️ No issues could be auto-fixed")


if __name__ == "__main__":
    structure()
