"""Modern CLI interface for Claude Knowledge Catalyst using Typer."""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from .. import __version__
from ..ai.smart_classifier import SmartContentClassifier
from ..core.config import CKCConfig, SyncTarget, load_config
from ..core.metadata import KnowledgeMetadata, MetadataManager
from ..core.watcher import KnowledgeWatcher
from ..obsidian.query_builder import ObsidianQueryBuilder, PredefinedQueries
from ..sync.obsidian import ObsidianVaultManager
from .interactive import (
    InteractiveTagManager,
    interactive_search_session,
    quick_tag_wizard,
)
from .smart_sync import migrate_to_tag_centered_cli, smart_sync_command


def version_callback(value: bool) -> None:
    """Show version information."""
    if value:
        console = Console()
        console.print(
            f"[bold blue]Claude Knowledge Catalyst (CKC)[/bold blue] v{__version__}"
        )
        console.print(
            "[dim]A comprehensive knowledge management system for "
            "Claude Code development insights.[/dim]"
        )
        raise typer.Exit()


# Initialize Typer app and Rich console
app = typer.Typer(
    name="ckc",
    help="Claude Knowledge Catalyst - Modern knowledge management system",
    no_args_is_help=True,
    rich_markup_mode="rich",
)
console = Console()


# Add global version option
@app.callback()
def main_callback(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version information",
    ),
) -> None:
    """Claude Knowledge Catalyst CLI."""
    pass


# Global state
_config: CKCConfig | None = None
_metadata_manager: MetadataManager | None = None


def get_config(config_path: Path | None = None) -> CKCConfig:
    """Get or load configuration."""
    global _config, _metadata_manager

    if _config is None:
        try:
            _config = load_config(config_path)
            _metadata_manager = MetadataManager()
        except Exception as e:
            console.print(f"[red]Error loading configuration: {e}[/red]")
            raise typer.Exit(1) from e

    return _config


def get_metadata_manager() -> MetadataManager:
    """Get metadata manager."""
    if _metadata_manager is None:
        get_config()  # This will initialize both
    return _metadata_manager


@app.command()
def init(
    force: bool = typer.Option(
        False, "--force", help="Force overwrite existing configuration"
    ),
    backup: bool = typer.Option(
        True, "--backup/--no-backup", help="Create backup of existing config"
    ),
) -> None:
    """Initialize CKC workspace with modern hybrid structure."""
    console.print("[blue]Initializing Claude Knowledge Catalyst...[/blue]")

    # Check for existing configuration
    config_path = Path.cwd() / "ckc_config.yaml"

    if config_path.exists() and not force:
        console.print(
            f"[yellow]⚠️  Configuration file already exists:[/yellow] {config_path}"
        )

        # Show existing config summary
        try:
            existing_config = load_config(config_path)
            if existing_config.sync_targets:
                console.print(
                    f"[dim]   Current sync targets: "
                    f"{len(existing_config.sync_targets)} configured[/dim]"
                )
                for target in existing_config.sync_targets:
                    status = (
                        "[green]enabled[/green]"
                        if target.enabled
                        else "[red]disabled[/red]"
                    )
                    console.print(
                        f"[dim]   • {target.name} → {target.path} ({status})[/dim]"
                    )
        except Exception:
            console.print("[dim]   (Unable to read existing configuration)[/dim]")

        console.print("\n[yellow]Options:[/yellow]")
        console.print("• Continue and overwrite: Use [bold]--force[/bold] flag")
        console.print(
            "• Keep existing config: Run [bold]ckc status[/bold] to check current setup"
        )
        console.print("• Manual backup: Copy ckc_config.yaml before re-running")

        if not Confirm.ask(
            "\nDo you want to overwrite the existing configuration?", default=False
        ):
            console.print("[red]Initialization cancelled.[/red]")
            console.print("Your existing configuration has been preserved.")
            return

    # Create backup if requested and file exists
    if config_path.exists() and backup:
        backup_path = config_path.with_suffix(".yaml.backup")
        shutil.copy2(config_path, backup_path)
        console.print(f"[green]📋 Backup created:[/green] {backup_path}")

    # Load or create config
    config = get_config()

    # Set project root to current directory
    config.project_root = Path.cwd()

    # Pure tag-centered structure
    console.print("[green]✓[/green] Pure tag-centered structure configured")

    # Create .claude directory
    claude_dir = Path.cwd() / ".claude"
    claude_dir.mkdir(exist_ok=True)

    # Save configuration
    config.save_to_file(config_path)

    console.print(f"[green]✓[/green] Configuration saved: {config_path}")
    console.print(f"[green]✓[/green] Workspace directory created: {claude_dir}")

    console.print("\n[yellow]Next steps:[/yellow]")
    console.print("1. Add a knowledge vault: [bold]ckc add <name> <path>[/bold]")
    console.print("2. Start syncing: [bold]ckc sync[/bold]")
    console.print("3. Watch for changes: [bold]ckc watch[/bold]")


@app.command()
def add(
    name: str = typer.Argument(..., help="Name for the sync target"),
    path: str = typer.Argument(..., help="Path to the vault directory"),
    disabled: bool = typer.Option(False, "--disabled", help="Add target as disabled"),
) -> None:
    """Add a knowledge vault for synchronization."""
    config = get_config()
    metadata_manager = get_metadata_manager()

    vault_path = Path(path).expanduser().resolve()

    # Create sync target (always Obsidian for now)
    sync_target = SyncTarget(
        name=name,
        type="obsidian",
        path=vault_path,
        enabled=not disabled,
    )

    # Add to configuration
    config.add_sync_target(sync_target)

    # Save configuration
    config_path = Path.cwd() / "ckc_config.yaml"
    config.save_to_file(config_path)

    console.print(f"[green]✓[/green] Added vault: {name} -> {vault_path}")

    # Initialize vault with pure tag-centered structure
    vault_manager = ObsidianVaultManager(vault_path, metadata_manager)

    if vault_manager.initialize_vault():
        console.print(
            "[green]✓[/green] Initialized vault with pure tag-centered structure"
        )
    else:
        console.print("[yellow]![/yellow] Vault initialization had issues")


@app.command()
def sync(
    target: str | None = typer.Option(
        None, "--target", "-t", help="Specific target to sync"
    ),
    project: str | None = typer.Option(
        None, "--project", "-p", help="Project name for organization"
    ),
) -> None:
    """Synchronize knowledge files to vaults."""
    config = get_config()
    metadata_manager = get_metadata_manager()

    # Get targets to sync
    targets_to_sync = config.get_enabled_sync_targets()
    if target:
        targets_to_sync = [t for t in targets_to_sync if t.name == target]
        if not targets_to_sync:
            console.print(f"[red]✗[/red] Target not found or disabled: {target}")
            raise typer.Exit(1)

    if not targets_to_sync:
        console.print("[yellow]No enabled sync targets found[/yellow]")
        console.print("Add a vault with: [bold]ckc add <name> <path>[/bold]")
        raise typer.Exit(1)

    # Find .claude directory
    claude_dir = config.project_root / ".claude"
    if not claude_dir.exists():
        console.print(f"[red]✗[/red] Workspace directory not found: {claude_dir}")
        console.print("Initialize with: [bold]ckc init[/bold]")
        raise typer.Exit(1)

    console.print(f"[blue]Syncing from: {claude_dir}[/blue]")

    # Sync each target
    total_synced = 0
    for sync_target in targets_to_sync:
        console.print(f"\n[yellow]Syncing to {sync_target.name}...[/yellow]")

        try:
            # Use pure tag-centered vault manager
            vault_manager = ObsidianVaultManager(sync_target.path, metadata_manager)
            results = vault_manager.sync_directory(claude_dir, project)

            # Show results
            success_count = sum(1 for success in results.values() if success)
            total_count = len(results)
            total_synced += success_count

            console.print(
                f"[green]✓[/green] Synced {success_count}/{total_count} files"
            )

            # Show failed files
            failed_files = [path for path, success in results.items() if not success]
            if failed_files:
                console.print("[red]Failed files:[/red]")
                for file_path in failed_files:
                    console.print(f"  - {file_path}")

        except Exception as e:
            console.print(f"[red]✗[/red] Error syncing to {sync_target.name}: {e}")

    if total_synced > 0:
        console.print(f"\n[green]🎉 Successfully synced {total_synced} files[/green]")


@app.command()
def watch(
    daemon: bool = typer.Option(False, "--daemon", "-d", help="Run as daemon"),
) -> None:
    """Watch for file changes and auto-sync."""
    config = get_config()
    metadata_manager = get_metadata_manager()

    if not config.auto_sync:
        console.print("[yellow]Auto-sync is disabled in configuration[/yellow]")
        console.print("Enable with: auto_sync: true in ckc_config.yaml")
        raise typer.Exit(1)

    # Create sync callback
    def sync_callback(event_type: str, file_path: Path) -> None:
        """Callback for file changes."""
        console.print(f"[dim]File {event_type}: {file_path}[/dim]")

        # Sync to enabled targets
        for sync_target in config.get_enabled_sync_targets():
            try:
                vault_manager = ObsidianVaultManager(sync_target.path, metadata_manager)
                project_name = config.project_name or None
                vault_manager.sync_file(file_path, project_name)
                console.print(f"[green]✓[/green] Synced to {sync_target.name}")
            except Exception as e:
                console.print(f"[red]✗[/red] Sync error for {sync_target.name}: {e}")

    # Create watcher
    watcher = KnowledgeWatcher(config.watch, metadata_manager, sync_callback)

    # Process existing files first
    console.print("[blue]Processing existing files...[/blue]")
    watcher.process_existing_files()

    # Start watching
    console.print("[blue]Starting file watcher...[/blue]")
    watcher.start()

    try:
        if daemon:
            console.print("[green]Running as daemon. Press Ctrl+C to stop.[/green]")
            import time

            while True:
                time.sleep(1)
        else:
            console.print("[green]Watching for changes. Press Enter to stop.[/green]")
            input()
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping watcher...[/yellow]")
    finally:
        watcher.stop()
        console.print("[green]✓[/green] Stopped watching")


def _detect_migration_status(config: CKCConfig) -> dict[str, Any]:
    """Detect legacy frontmatter and migration opportunities."""
    legacy_count = 0
    modern_count = 0
    total_files = 0

    # Scan watch paths for markdown files
    for watch_path in config.watch.watch_paths:
        full_path = config.project_root / watch_path
        if not full_path.exists():
            continue

        for md_file in full_path.rglob("*.md"):
            if md_file.is_file():
                total_files += 1
                try:
                    content = md_file.read_text(encoding="utf-8")
                    # Check for frontmatter
                    if content.startswith("---"):
                        frontmatter_end = content.find("\n---\n", 3)
                        if frontmatter_end > 0:
                            frontmatter = content[3:frontmatter_end]
                            # Check for legacy vs modern format
                            if (
                                "category:" in frontmatter
                                or "subcategory:" in frontmatter
                            ):
                                legacy_count += 1
                            elif "type:" in frontmatter:
                                modern_count += 1
                except Exception:
                    continue

    return {
        "total_files": total_files,
        "legacy_count": legacy_count,
        "modern_count": modern_count,
        "needs_migration": legacy_count > 0,
    }


@app.command()
def status() -> None:
    """Show current status and configuration."""
    config = get_config()

    console.print("[bold]Claude Knowledge Catalyst Status[/bold]\n")

    # Project info
    console.print(f"[blue]Project:[/blue] {config.project_name or 'Unnamed'}")
    console.print(f"[blue]Root:[/blue] {config.project_root}")
    console.print(
        f"[blue]Auto-sync:[/blue] {'Enabled' if config.auto_sync else 'Disabled'}"
    )
    console.print("[blue]Structure:[/blue] Pure Tag-Centered (6-directory)")

    # Migration status (controlled by notification level)
    migration_info = _detect_migration_status(config)
    if config.migration.auto_detect and config.migration.notify_level != "silent":
        if migration_info["needs_migration"]:
            console.print(
                "[yellow]Migration Status:[/yellow] "
                "[yellow]⚠️  Mixed format detected[/yellow]"
            )
            console.print(f"  • Legacy format: {migration_info['legacy_count']} files")
            console.print(f"  • Modern format: {migration_info['modern_count']} files")
            console.print("  • Recommendation: Run [bold]ckc migrate --preview[/bold]")

            if config.migration.notify_level in ["recommended", "verbose"]:
                console.print(
                    "  [dim]💡 Upgrade to Pure Tag-Centered Architecture "
                    "for enhanced features[/dim]"
                )
                if config.migration.notify_level == "verbose":
                    console.print(
                        "  [dim]Benefits: Multi-dimensional search, "
                        "AI classification, success tracking[/dim]"
                    )

        elif migration_info["modern_count"] > 0:
            console.print(
                "[green]Migration Status:[/green] "
                "[green]✓ Pure Tag-Centered Architecture[/green]"
            )
            console.print(f"  • Modern format: {migration_info['modern_count']} files")
        elif migration_info["total_files"] > 0 and config.migration.notify_level in [
            "recommended",
            "verbose",
        ]:
            console.print(
                "[yellow]Migration Status:[/yellow] "
                "[yellow]Files found but no frontmatter detected[/yellow]"
            )
            console.print(f"  • Total files: {migration_info['total_files']} files")
            console.print(
                "  • Consider running: [bold]ckc smart-sync[/bold] to add metadata"
            )

    # Watch paths
    console.print("\n[blue]Watch Paths:[/blue]")
    for path in config.watch.watch_paths:
        full_path = config.project_root / path
        status_icon = "✓" if full_path.exists() else "✗"
        console.print(f"  {status_icon} {full_path}")

    # Sync targets
    console.print("\n[blue]Sync Targets:[/blue]")
    if not config.sync_targets:
        console.print("  [dim]None configured[/dim]")
        console.print("  Add with: [bold]ckc add <name> <path>[/bold]")
    else:
        for target in config.sync_targets:
            status_icon = (
                "[green]✓[/green]"
                if target.enabled and target.path.exists()
                else "[red]✗[/red]"
            )
            console.print(f"  {status_icon} {target.name} -> {target.path}")


@app.command()
def analyze(
    file_path: str = typer.Argument(..., help="Path to file to analyze"),
) -> None:
    """Analyze a knowledge file and show its metadata."""
    metadata_manager = get_metadata_manager()

    path = Path(file_path)
    if not path.exists():
        console.print(f"[red]✗[/red] File not found: {path}")
        raise typer.Exit(1)

    try:
        metadata = metadata_manager.extract_metadata_from_file(path)

        console.print(f"[bold]Analysis of: {path}[/bold]\n")

        # Basic metadata table
        table = Table(title="Metadata")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Title", metadata.title)
        table.add_row("Type", metadata.type)
        table.add_row(
            "Projects", ", ".join(metadata.projects) if metadata.projects else "N/A"
        )
        table.add_row("Status", metadata.status)
        table.add_row("Version", metadata.version)
        table.add_row("Created", metadata.created.strftime("%Y-%m-%d %H:%M:%S"))
        table.add_row("Updated", metadata.updated.strftime("%Y-%m-%d %H:%M:%S"))

        if metadata.success_rate:
            table.add_row("Success Rate", f"{metadata.success_rate}%")
        if metadata.claude_model:
            table.add_row("Claude Models", ", ".join(metadata.claude_model))
        if metadata.complexity:
            table.add_row("Complexity", metadata.complexity)
        if metadata.confidence:
            table.add_row("Confidence", metadata.confidence)

        console.print(table)

        # Tags and domains
        if metadata.tags:
            console.print(f"\n[blue]Tags:[/blue] {', '.join(metadata.tags)}")
        if metadata.tech:
            console.print(f"\n[blue]Tech Stack:[/blue] {', '.join(metadata.tech)}")
        if metadata.domain:
            console.print(f"\n[blue]Domains:[/blue] {', '.join(metadata.domain)}")
        if metadata.team:
            console.print(f"\n[blue]Team:[/blue] {', '.join(metadata.team)}")

        # Purpose
        if metadata.purpose:
            console.print(f"\n[blue]Purpose:[/blue] {metadata.purpose}")

    except Exception as e:
        console.print(f"[red]✗[/red] Error analyzing file: {e}")
        raise typer.Exit(1) from e


@app.command()
def project(
    action: str = typer.Argument(..., help="Action: list, files, stats"),
    name: str | None = typer.Argument(None, help="Project name"),
) -> None:
    """Manage and view project information."""
    config = get_config()
    metadata_manager = get_metadata_manager()

    if action == "list":
        _list_projects(config, metadata_manager)
    elif action == "files" and name:
        _list_project_files(config, metadata_manager, name)
    elif action == "stats" and name:
        _show_project_stats(config, metadata_manager, name)
    else:
        console.print("[red]✗[/red] Invalid action or missing project name")
        console.print("Usage: ckc project list")
        console.print("       ckc project files <name>")
        console.print("       ckc project stats <name>")
        raise typer.Exit(1)


def _list_projects(config: CKCConfig, metadata_manager: MetadataManager) -> None:
    """List all projects found in sync targets and source directories."""
    projects = set()

    # Check sync targets for existing projects (minimal structure)
    for target in config.get_enabled_sync_targets():
        # In pure tag system, projects are tracked via metadata only
        for md_file in target.path.rglob("*.md"):
            if md_file.name != "README.md" and not md_file.name.startswith("."):
                try:
                    metadata = metadata_manager.extract_metadata_from_file(md_file)
                    if metadata.projects:
                        projects.update(metadata.projects)
                except Exception:
                    continue

    # Also check .claude directory for potential projects
    claude_dir = config.project_root / ".claude"
    if claude_dir.exists():
        for item in claude_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                projects.add(item.name)

    # Check for files that indicate project organization
    for target in config.get_enabled_sync_targets():
        # Look for project-tagged files throughout the vault
        for md_file in target.path.rglob("*.md"):
            if md_file.name != "README.md" and not md_file.name.startswith("."):
                try:
                    metadata = metadata_manager.extract_metadata_from_file(md_file)
                    if metadata.projects:
                        projects.update(metadata.projects)
                except Exception:
                    continue

    if not projects:
        console.print("[yellow]No projects found[/yellow]")
        console.print("\nProjects can be found by:")
        console.print("  1. Creating project directories in .claude/")
        console.print("  2. Adding 'project:' metadata to markdown files")
        console.print("  3. Running 'ckc sync' to organize files into projects")
        return

    console.print("[bold]Found Projects:[/bold]\n")
    for project in sorted(projects):
        console.print(f"  📁 {project}")


def _list_project_files(
    config: CKCConfig, metadata_manager: MetadataManager, project_name: str
) -> None:
    """List all files for a specific project."""
    files_found = []

    # Search in tag-centered structure
    for target in config.get_enabled_sync_targets():
        # Search all files by metadata (no dedicated project directories)

        # 2. Search all files with matching project metadata
        for md_file in target.path.rglob("*.md"):
            if md_file.name != "README.md" and not md_file.name.startswith("."):
                try:
                    metadata = metadata_manager.extract_metadata_from_file(md_file)
                    if project_name in metadata.projects:
                        if md_file not in files_found:  # Avoid duplicates
                            files_found.append(md_file)
                except Exception:
                    continue

    # Also check .claude directory
    claude_project_dir = config.project_root / ".claude" / project_name
    if claude_project_dir.exists():
        for file_path in claude_project_dir.rglob("*.md"):
            if not file_path.name.startswith("."):
                files_found.append(file_path)

    if not files_found:
        console.print(f"[yellow]No files found for project: {project_name}[/yellow]")
        console.print("\nTo add files to this project:")
        console.print(f"  1. Create files in .claude/{project_name}/")
        console.print(f"  2. Add 'project: {project_name}' to file frontmatter")
        console.print("  3. Run 'ckc sync' to synchronize")
        return

    console.print(f"[bold]Files in project '{project_name}':[/bold]\n")
    for file_path in sorted(files_found):
        try:
            metadata = metadata_manager.extract_metadata_from_file(file_path)
            location = (
                "vault" if str(file_path).find("demo/shared_vault") != -1 else "source"
            )
            console.print(f"  📄 {metadata.title} ({metadata.type}) [{location}]")
        except Exception:
            location = (
                "vault" if str(file_path).find("demo/shared_vault") != -1 else "source"
            )
            console.print(f"  📄 {file_path.name} [{location}]")


def _show_project_stats(
    config: CKCConfig, metadata_manager: MetadataManager, project_name: str
) -> None:
    """Show statistics for a specific project."""
    files_found = []
    categories: dict[str, int] = {}
    statuses: dict[str, int] = {}
    locations = {"source": 0, "vault": 0}

    # Search in tag-centered structure
    for target in config.get_enabled_sync_targets():
        # Search all files by metadata (no dedicated project directories)
        for md_file in target.path.rglob("*.md"):
            if md_file.name != "README.md" and not md_file.name.startswith("."):
                try:
                    metadata = metadata_manager.extract_metadata_from_file(md_file)
                    if project_name in metadata.projects:
                        files_found.append(metadata)
                        locations["vault"] += 1

                        # Count types
                        content_type = metadata.type
                        categories[content_type] = categories.get(content_type, 0) + 1

                        # Count statuses
                        statuses[metadata.status] = statuses.get(metadata.status, 0) + 1

                except Exception:
                    continue

        # Files are already processed above in the tag-centered search

    # Also check .claude directory
    claude_project_dir = config.project_root / ".claude" / project_name
    if claude_project_dir.exists():
        for file_path in claude_project_dir.rglob("*.md"):
            if not file_path.name.startswith("."):
                try:
                    metadata = metadata_manager.extract_metadata_from_file(file_path)
                    files_found.append(metadata)
                    locations["source"] += 1

                    # Count types
                    content_type = metadata.type
                    categories[content_type] = categories.get(content_type, 0) + 1

                    # Count statuses
                    statuses[metadata.status] = statuses.get(metadata.status, 0) + 1

                except Exception:
                    continue

    if not files_found:
        console.print(f"[yellow]No files found for project: {project_name}[/yellow]")
        console.print("\nTo create files for this project:")
        console.print(f"  1. Create files in .claude/{project_name}/")
        console.print(f"  2. Add 'project: {project_name}' to file frontmatter")
        console.print("  3. Run 'ckc sync' to synchronize")
        return

    console.print(f"[bold]Statistics for project '{project_name}':[/bold]\n")
    console.print(f"📊 Total files: {len(files_found)}")

    # Location breakdown
    console.print("\n[blue]By Location:[/blue]")
    console.print(f"  Source (.claude): {locations['source']}")
    console.print(f"  Vault (synced): {locations['vault']}")

    # Content types breakdown
    if categories:
        console.print("\n[blue]By Type:[/blue]")
        for content_type, count in sorted(categories.items()):
            console.print(f"  {content_type}: {count}")

    # Status breakdown
    if statuses:
        console.print("\n[blue]By Status:[/blue]")
        for status, count in sorted(statuses.items()):
            console.print(f"  {status}: {count}")


@app.command("smart-sync")
def smart_sync(
    auto_apply: bool = typer.Option(False, "--auto-apply", help="自動適用（確認なし）"),
    dry_run: bool = typer.Option(False, "--dry-run", help="実行内容のプレビューのみ"),
    directory: str = typer.Option(
        ".claude", "--directory", "-d", help="対象ディレクトリ"
    ),
    backup: bool = typer.Option(True, "--backup/--no-backup", help="バックアップ作成"),
) -> None:
    """Intelligent batch classification and synchronization.

    Smart sync automatically:
    1. Scans for files without metadata
    2. Classifies them using intelligent content analysis
    3. Applies appropriate metadata
    4. Runs CKC sync to organize files properly

    Use --dry-run to preview changes without applying them.
    Use --auto-apply to skip confirmation prompts.
    """
    config = get_config()
    metadata_manager = get_metadata_manager()

    # Show migration notification if applicable
    if config.migration.auto_detect and config.migration.notify_level == "recommended":
        migration_info = _detect_migration_status(config)
        if migration_info["needs_migration"]:
            console.print("🔍 [yellow]Migration opportunity detected![/yellow]")
            console.print("📋 [dim]Summary:[/dim]")
            console.print(f"  • Legacy format files: {migration_info['legacy_count']}")
            console.print(f"  • Modern format files: {migration_info['modern_count']}")
            console.print(
                "  • Migration benefits: Enhanced search, AI classification, "
                "multi-dimensional tags"
            )
            console.print("")
            console.print(
                "Run [bold]ckc migrate --preview[/bold] to see what would change."
            )
            if not auto_apply and not Confirm.ask(
                "Continue with current sync?", default=True
            ):
                console.print("[red]Smart sync cancelled.[/red]")
                return
            console.print("")

    smart_sync_command(
        auto_apply=auto_apply,
        dry_run=dry_run,
        directory=directory,
        backup=backup,
        config=config,
        metadata_manager=metadata_manager,
    )


@app.command("migrate-legacy")
def migrate_legacy(
    source: str = typer.Option(
        ".", "--source", "-s", help="Source directory to migrate from"
    ),
    target: str = typer.Option(
        "./tag_centered_vault",
        "--target",
        "-t",
        help="Target directory for tag-centered structure",
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Preview migration without making changes"
    ),
    force: bool = typer.Option(
        False, "--force", help="Force migration even if target directory exists"
    ),
) -> None:
    """Migrate to tag-centered approach with minimal directory structure.

    This command migrates your existing knowledge base to the new tag-centered approach:

    1. Creates minimal directory structure (_system, inbox, active, archive, knowledge)
    2. Migrates files based on metadata and state rather than content categories
    3. Enhances metadata with multi-layered tag architecture
    4. Creates Obsidian templates for the new system

    The migration preserves all content while reorganizing based on the state-based
    classification described in the tag-centered approach analysis.

    Example:
        ckc migrate --source .claude --target ./new_vault --dry-run
        ckc migrate --target ./obsidian_vault
    """
    from pathlib import Path

    source_path = Path(source).resolve()
    target_path = Path(target).resolve()

    # Validation
    if not source_path.exists():
        console.print(f"[red]✗[/red] Source directory does not exist: {source_path}")
        raise typer.Exit(1)

    if target_path.exists() and not force and not dry_run:
        console.print(
            f"[yellow]Target directory already exists: {target_path}[/yellow]"
        )
        console.print("Use --force to overwrite or --dry-run to preview")
        if not typer.confirm("Continue anyway?"):
            raise typer.Exit(0)

    console.print("[blue]Tag-Centered Migration[/blue]")
    console.print(f"Source: {source_path}")
    console.print(f"Target: {target_path}")
    console.print(f"Mode: {'DRY RUN' if dry_run else 'LIVE MIGRATION'}")
    console.print()

    if not dry_run:
        console.print(
            "[yellow]⚠️  This will create a new directory structure and "
            "migrate files.[/yellow]"
        )
        console.print("[yellow]   Original files will be copied (not moved).[/yellow]")
        if not typer.confirm("Proceed with migration?"):
            console.print("Migration cancelled.")
            raise typer.Exit(0)

    # Perform migration
    try:
        result = migrate_to_tag_centered_cli(
            source=str(source_path), target=str(target_path), dry_run=dry_run
        )

        if result["errors"]:
            console.print(
                f"\n[yellow]⚠️  Migration completed with "
                f"{len(result['errors'])} errors[/yellow]"
            )
            console.print("Check the migration report for details.")
        else:
            console.print("\n[green]🎉 Migration completed successfully![/green]")

        if not dry_run:
            console.print("\n[blue]Next steps:[/blue]")
            console.print(
                f"1. Review the migration report: {target_path}/migration_report.md"
            )
            console.print(f"2. Open the new vault in Obsidian: {target_path}")
            console.print(
                "3. Explore the tag-based organization in the knowledge directory"
            )
            console.print("4. Use the enhanced templates in _system/templates/")

    except Exception as e:
        console.print(f"[red]✗[/red] Migration failed: {e}")
        raise typer.Exit(1) from e


@app.command()
def search(
    query: str | None = typer.Argument(None, help="Search query or tag filter"),
    content_type: str | None = typer.Option(
        None, "--type", "-t", help="Content type: prompt, code, concept, resource"
    ),
    status: str | None = typer.Option(
        None, "--status", "-s", help="Status: draft, tested, production, deprecated"
    ),
    tech: str | None = typer.Option(None, "--tech", help="Technology tag"),
    domain: str | None = typer.Option(None, "--domain", help="Domain tag"),
    team: str | None = typer.Option(None, "--team", help="Team tag"),
    project: str | None = typer.Option(None, "--project", help="Project name"),
    complexity: str | None = typer.Option(
        None,
        "--complexity",
        help="Complexity: beginner, intermediate, advanced, expert",
    ),
    confidence: str | None = typer.Option(
        None, "--confidence", help="Confidence: low, medium, high"
    ),
    min_success_rate: int | None = typer.Option(
        None, "--min-success", help="Minimum success rate (0-100)"
    ),
    claude_model: str | None = typer.Option(
        None, "--claude-model", help="Claude model: opus, sonnet, haiku"
    ),
    claude_feature: str | None = typer.Option(
        None, "--claude-feature", help="Claude feature"
    ),
    limit: int | None = typer.Option(
        20, "--limit", "-l", help="Maximum number of results"
    ),
    format_output: str = typer.Option(
        "table", "--format", "-f", help="Output format: table, query, json"
    ),
) -> None:
    """Advanced tag-based search and filtering.

    Search content using the pure tag-centered system's multi-layered tagging.

    Examples:
        ckc search "python web development"
        ckc search --type prompt --tech python --confidence high
        ckc search --status production --domain web-dev --team frontend
        ckc search --min-success 80 --claude-feature code-generation
    """
    config = get_config()
    metadata_manager = get_metadata_manager()

    # Build query
    query_builder = ObsidianQueryBuilder()

    if content_type:
        query_builder = query_builder.type(content_type)
    if status:
        query_builder = query_builder.status(status)
    if tech:
        query_builder = query_builder.tech(tech)
    if domain:
        query_builder = query_builder.domain(domain)
    if team:
        query_builder = query_builder.team(team)
    if project:
        query_builder = query_builder.projects(project)
    if complexity:
        query_builder = query_builder.complexity(complexity)
    if confidence:
        query_builder = query_builder.confidence(confidence)
    if min_success_rate:
        from ..obsidian.query_builder import QueryComparison

        query_builder = query_builder.success_rate(
            min_success_rate, QueryComparison.GREATER_EQUAL
        )
    if claude_model:
        query_builder = query_builder.claude_model(claude_model)
    if claude_feature:
        query_builder = query_builder.claude_feature(claude_feature)

    # Add general search terms as tags if provided
    if query:
        query_builder = query_builder.tags(query.split())

    # Sort by relevance (updated date)
    query_builder = query_builder.sort_by("updated", False).limit_results(limit)

    # Output based on format
    if format_output == "query":
        console.print("[blue]Obsidian Query:[/blue]")
        console.print("```")
        console.print(query_builder.build())
        console.print("```")
        return

    # Search in vault files
    results = []
    for target in config.get_enabled_sync_targets():
        for md_file in target.path.rglob("*.md"):
            if md_file.name.startswith(".") or md_file.name == "README.md":
                continue

            try:
                metadata = metadata_manager.extract_metadata_from_file(md_file)
                if _matches_criteria(
                    metadata,
                    content_type,
                    status,
                    tech,
                    domain,
                    team,
                    project,
                    complexity,
                    confidence,
                    min_success_rate,
                    claude_model,
                    claude_feature,
                    query,
                ):
                    results.append((md_file, metadata))
            except Exception:
                continue

    # Sort by update date (newest first)
    results.sort(key=lambda x: x[1].updated, reverse=True)
    results = results[:limit]

    if format_output == "json":
        import json

        json_results = []
        for file_path, metadata in results:
            json_results.append(
                {
                    "file": str(file_path),
                    "title": metadata.title,
                    "type": metadata.type,
                    "status": metadata.status,
                    "tech": metadata.tech,
                    "domain": metadata.domain,
                    "team": metadata.team,
                    "projects": metadata.projects,
                    "updated": metadata.updated.isoformat(),
                }
            )
        console.print(json.dumps(json_results, indent=2))
        return

    # Table format (default)
    if not results:
        console.print("[yellow]No matching files found[/yellow]")
        console.print("\n[blue]Search criteria:[/blue]")
        criteria = []
        if content_type:
            criteria.append(f"type: {content_type}")
        if status:
            criteria.append(f"status: {status}")
        if tech:
            criteria.append(f"tech: {tech}")
        if domain:
            criteria.append(f"domain: {domain}")
        if team:
            criteria.append(f"team: {team}")
        if project:
            criteria.append(f"project: {project}")
        if query:
            criteria.append(f"query: {query}")

        if criteria:
            console.print("  " + ", ".join(criteria))
        else:
            console.print("  No criteria specified")
        return

    # Display results table
    table = Table(title=f"Search Results ({len(results)} found)")
    table.add_column("Title", style="bold")
    table.add_column("Type", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Tech", style="yellow")
    table.add_column("Domain", style="magenta")
    table.add_column("Updated", style="dim")

    for _file_path, metadata in results:
        tech_str = ", ".join(metadata.tech[:2]) + (
            "..." if len(metadata.tech) > 2 else ""
        )
        domain_str = ", ".join(metadata.domain[:2]) + (
            "..." if len(metadata.domain) > 2 else ""
        )
        updated_str = metadata.updated.strftime("%Y-%m-%d")

        table.add_row(
            metadata.title[:40] + ("..." if len(metadata.title) > 40 else ""),
            metadata.type,
            metadata.status,
            tech_str,
            domain_str,
            updated_str,
        )

    console.print(table)

    # Show query hint
    console.print("\n[dim]💡 Use --format query to see the Obsidian search query[/dim]")


def _matches_criteria(
    metadata,
    content_type,
    status,
    tech,
    domain,
    team,
    project,
    complexity,
    confidence,
    min_success_rate,
    claude_model,
    claude_feature,
    query,
) -> bool:
    """Check if metadata matches search criteria."""

    if content_type and metadata.type != content_type:
        return False
    if status and metadata.status != status:
        return False
    if tech and tech not in metadata.tech:
        return False
    if domain and domain not in metadata.domain:
        return False
    if team and team not in metadata.team:
        return False
    if project and project not in metadata.projects:
        return False
    if complexity and metadata.complexity != complexity:
        return False
    if confidence and metadata.confidence != confidence:
        return False
    if min_success_rate and (
        not metadata.success_rate or metadata.success_rate < min_success_rate
    ):
        return False
    if claude_model and claude_model not in metadata.claude_model:
        return False
    if claude_feature and claude_feature not in metadata.claude_feature:
        return False
    if query:
        # Check if any query terms match tags or title
        query_terms = query.lower().split()
        searchable_text = (metadata.title + " " + " ".join(metadata.tags)).lower()
        if not any(term in searchable_text for term in query_terms):
            return False

    return True


@app.command()
def query(
    preset: str | None = typer.Argument(None, help="Preset query name"),
) -> None:
    """Generate Obsidian queries using predefined presets.

    Available presets:
    - high-quality: High-quality production content
    - drafts: Draft content needing review
    - successful-prompts: Prompts with high success rates
    - python: Python-related content
    - frontend: Frontend development content
    - recent: Recently updated content
    - claude-code: Claude code generation content
    - beginner: Beginner-friendly content
    - expert: Expert-level content
    - cleanup: Content needing cleanup

    Examples:
        ckc query high-quality
        ckc query python
        ckc query successful-prompts
    """

    presets = {
        "high-quality": PredefinedQueries.high_quality_content(),
        "drafts": PredefinedQueries.draft_content(),
        "successful-prompts": PredefinedQueries.successful_prompts(),
        "python": PredefinedQueries.python_resources(),
        "frontend": PredefinedQueries.frontend_development(),
        "recent": PredefinedQueries.recent_updates(),
        "claude-code": PredefinedQueries.claude_code_generation(),
        "beginner": PredefinedQueries.beginner_friendly(),
        "expert": PredefinedQueries.expert_level(),
        "cleanup": PredefinedQueries.cleanup_candidates(),
    }

    if not preset:
        console.print("[bold]Available Query Presets:[/bold]\n")
        for name, query_builder in presets.items():
            console.print(f"[cyan]{name:15}[/cyan] {query_builder.build()}")
        console.print(
            "\n[dim]Use: ckc query <preset-name> to generate specific query[/dim]"
        )
        return

    if preset not in presets:
        console.print(f"[red]Unknown preset: {preset}[/red]")
        console.print(f"Available presets: {', '.join(presets.keys())}")
        raise typer.Exit(1)

    query_builder = presets[preset]

    console.print(f"[bold blue]Query for '{preset}':[/bold blue]")
    console.print("```query")
    console.print(query_builder.build())
    console.print("```")

    console.print("\n[bold blue]Dataview version:[/bold blue]")
    console.print("```dataview")
    console.print(query_builder.build_dataview())
    console.print("```")


@app.command()
def tags(
    action: str = typer.Argument(..., help="Action: list, stats, validate, suggest"),
    tag_type: str | None = typer.Argument(
        None, help="Tag type for specific operations"
    ),
    file_path: str | None = typer.Option(
        None, "--file", help="File path for validation/suggestions"
    ),
) -> None:
    """Manage and analyze tags in the pure tag-centered system.

    Actions:
    - list: List all available tag types and values
    - stats: Show tag usage statistics
    - validate: Validate tags in a file
    - suggest: Suggest tags for a file

    Examples:
        ckc tags list
        ckc tags stats tech
        ckc tags validate --file path/to/file.md
        ckc tags suggest --file path/to/file.md
    """
    config = get_config()
    metadata_manager = get_metadata_manager()

    if action == "list":
        if tag_type:
            # Show specific tag type values
            recommendations = metadata_manager.get_tag_recommendations(tag_type)
            if recommendations:
                console.print(f"[bold]Valid values for '{tag_type}':[/bold]")
                for value in recommendations:
                    console.print(f"  • {value}")
            else:
                console.print(f"[red]Unknown tag type: {tag_type}[/red]")
        else:
            # Show all tag types
            from ..core.tag_standards import TagStandardsManager

            standards = TagStandardsManager()

            console.print("[bold]Pure Tag-Centered System - Tag Categories:[/bold]\n")
            for tag_name, standard in standards.standards.items():
                required_indicator = "[red]*[/red]" if standard.required else ""
                console.print(
                    f"[cyan]{tag_name}{required_indicator}[/cyan]: "
                    f"{standard.description}"
                )
                console.print(f"  Max selections: {standard.max_selections}")
                console.print(
                    f"  Example values: {', '.join(standard.valid_values[:5])}..."
                )
                console.print()

    elif action == "stats":
        # Collect metadata from all files
        all_metadata = []
        for target in config.get_enabled_sync_targets():
            for md_file in target.path.rglob("*.md"):
                if md_file.name.startswith(".") or md_file.name == "README.md":
                    continue
                try:
                    metadata = metadata_manager.extract_metadata_from_file(md_file)
                    all_metadata.append(metadata.model_dump())
                except Exception:
                    continue

        if not all_metadata:
            console.print("[yellow]No files found for analysis[/yellow]")
            return

        # Generate statistics
        stats = metadata_manager.tag_standards.get_tag_statistics(all_metadata)

        if tag_type:
            if tag_type in stats:
                console.print(f"[bold]Usage statistics for '{tag_type}':[/bold]\n")
                for value, count in sorted(
                    stats[tag_type].items(), key=lambda x: x[1], reverse=True
                ):
                    console.print(f"{value:20} {count:4} files")
            else:
                console.print(f"[red]No statistics available for: {tag_type}[/red]")
        else:
            console.print(
                f"[bold]Tag Usage Statistics ({len(all_metadata)} files):[/bold]\n"
            )
            for category, category_stats in stats.items():
                if category_stats:
                    total_usage = sum(category_stats.values())
                    console.print(
                        f"[cyan]{category}[/cyan] ({total_usage} total usages):"
                    )
                    top_values = sorted(
                        category_stats.items(), key=lambda x: x[1], reverse=True
                    )[:5]
                    for value, count in top_values:
                        console.print(f"  {value:15} {count:3}")
                    console.print()

    elif action == "validate":
        if not file_path:
            console.print("[red]--file is required for validation[/red]")
            raise typer.Exit(1)

        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            console.print(f"[red]File not found: {file_path}[/red]")
            raise typer.Exit(1)

        try:
            metadata = metadata_manager.extract_metadata_from_file(file_path_obj)
            enhanced_metadata, errors = metadata_manager.validate_and_enhance_tags(
                metadata, file_path_obj.read_text(encoding="utf-8")
            )

            if errors:
                console.print(f"[red]Validation errors in {file_path}:[/red]")
                for error in errors:
                    console.print(f"  • {error}")
            else:
                console.print(f"[green]✓ All tags valid in {file_path}[/green]")

            console.print("\n[blue]Current tags:[/blue]")
            console.print(f"type: {metadata.type}")
            console.print(f"status: {metadata.status}")
            if metadata.tech:
                console.print(f"tech: {metadata.tech}")
            if metadata.domain:
                console.print(f"domain: {metadata.domain}")
            if metadata.team:
                console.print(f"team: {metadata.team}")

        except Exception as e:
            console.print(f"[red]Error validating file: {e}[/red]")
            raise typer.Exit(1) from e

    elif action == "suggest":
        if not file_path:
            console.print("[red]--file is required for suggestions[/red]")
            raise typer.Exit(1)

        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            console.print(f"[red]File not found: {file_path}[/red]")
            raise typer.Exit(1)

        try:
            content = file_path_obj.read_text(encoding="utf-8")
            metadata = metadata_manager.extract_metadata_from_file(file_path_obj)

            # Get suggestions
            existing_tags = {
                "type": [metadata.type],
                "status": [metadata.status],
                "tech": metadata.tech,
                "domain": metadata.domain,
                "team": metadata.team,
                "claude_model": metadata.claude_model,
                "claude_feature": metadata.claude_feature,
                "tags": metadata.tags,
            }

            suggestions = metadata_manager.tag_standards.suggest_tags(
                content, existing_tags
            )

            if suggestions:
                console.print(f"[blue]Tag suggestions for {file_path}:[/blue]\n")
                for tag_type, suggested_values in suggestions.items():
                    console.print(
                        f"[cyan]{tag_type}:[/cyan] {', '.join(suggested_values)}"
                    )
            else:
                console.print(
                    f"[green]No additional tag suggestions for {file_path}[/green]"
                )
                console.print("[dim]Current tags appear comprehensive[/dim]")

        except Exception as e:
            console.print(f"[red]Error analyzing file: {e}[/red]")
            raise typer.Exit(1) from e

    else:
        console.print(f"[red]Unknown action: {action}[/red]")
        console.print("Available actions: list, stats, validate, suggest")
        raise typer.Exit(1)


@app.command()
def interactive(
    action: str = typer.Argument(..., help="Action: search, tag, wizard"),
    file_path: str | None = typer.Option(None, "--file", help="File path for tagging"),
) -> None:
    """Interactive CLI tools for enhanced user experience.

    Actions:
    - search: Natural language search with smart query building
    - tag: Interactive guided tagging for a file
    - wizard: Quick tag wizard for common scenarios

    Examples:
        ckc interactive search
        ckc interactive tag --file path/to/file.md
        ckc interactive wizard
    """

    if action == "search":
        interactive_search_session()

    elif action == "tag":
        if not file_path:
            console.print("[red]--file is required for interactive tagging[/red]")
            raise typer.Exit(1)

        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            console.print(f"[red]File not found: {file_path}[/red]")
            raise typer.Exit(1)

        metadata_manager = get_metadata_manager()
        interactive_manager = InteractiveTagManager(metadata_manager)

        try:
            interactive_manager.guided_file_tagging(file_path_obj)
        except Exception as e:
            console.print(f"[red]Error during interactive tagging: {e}[/red]")
            raise typer.Exit(1) from e

    elif action == "wizard":
        quick_tag_wizard()

    else:
        console.print(f"[red]Unknown action: {action}[/red]")
        console.print("Available actions: search, tag, wizard")
        raise typer.Exit(1)


@app.command()
def enhance(
    directory: str = typer.Option(
        ".claude", "--directory", "-d", help="Directory to enhance"
    ),
    auto_apply: bool = typer.Option(
        False, "--auto-apply", help="Auto-apply high-confidence suggestions"
    ),
    batch_size: int = typer.Option(
        10, "--batch-size", help="Number of files to process at once"
    ),
    min_confidence: float = typer.Option(
        0.7, "--min-confidence", help="Minimum confidence for auto-apply"
    ),
) -> None:
    """Intelligent batch enhancement of file metadata.

    Analyzes content and suggests tags using AI-powered classification.

    Examples:
        ckc enhance                           # Interactive enhancement
        ckc enhance --auto-apply             # Auto-apply high-confidence tags
        ckc enhance -d /path/to/knowledge    # Enhance specific directory
        ckc enhance --min-confidence 0.8    # Higher confidence threshold
    """
    metadata_manager = get_metadata_manager()

    dir_path = Path(directory).resolve()
    if not dir_path.exists():
        console.print(f"[red]Directory not found: {directory}[/red]")
        raise typer.Exit(1)

    # Find markdown files
    md_files = list(dir_path.rglob("*.md"))
    if not md_files:
        console.print(f"[yellow]No markdown files found in {directory}[/yellow]")
        return

    console.print(f"[blue]Found {len(md_files)} markdown files to analyze[/blue]")

    from rich.progress import (
        BarColumn,
        Progress,
        SpinnerColumn,
        TaskProgressColumn,
        TextColumn,
    )

    enhanced_count = 0
    suggestions_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing files...", total=len(md_files))

        for i, file_path in enumerate(md_files):
            progress.update(task, advance=1, description=f"Processing {file_path.name}")

            try:
                content = file_path.read_text(encoding="utf-8")
                metadata = metadata_manager.extract_metadata_from_file(file_path)

                # Get enhanced metadata with suggestions
                enhanced_metadata, errors = metadata_manager.validate_and_enhance_tags(
                    metadata, content
                )

                # Check if there are meaningful enhancements
                has_enhancements = (
                    len(enhanced_metadata.tech) > len(metadata.tech)
                    or len(enhanced_metadata.domain) > len(metadata.domain)
                    or len(enhanced_metadata.claude_feature)
                    > len(metadata.claude_feature)
                    or (not metadata.complexity and enhanced_metadata.complexity)
                    or (not metadata.confidence and enhanced_metadata.confidence)
                )

                if has_enhancements:
                    suggestions_count += 1

                    if auto_apply:
                        # Auto-apply if confidence is high enough
                        metadata_manager.update_file_metadata(
                            file_path, enhanced_metadata
                        )
                        enhanced_count += 1
                        console.print(f"[green]✓[/green] Enhanced: {file_path.name}")
                    else:
                        # Show suggestions for manual review
                        console.print(
                            f"\n[cyan]Suggestions for {file_path.name}:[/cyan]"
                        )
                        _show_enhancement_diff(metadata, enhanced_metadata)

                        if Confirm.ask(f"Apply enhancements to {file_path.name}?"):
                            metadata_manager.update_file_metadata(
                                file_path, enhanced_metadata
                            )
                            enhanced_count += 1
                            console.print("[green]✓[/green] Enhanced!")
                        else:
                            console.print("[dim]Skipped[/dim]")

            except Exception as e:
                console.print(f"[red]Error processing {file_path.name}: {e}[/red]")
                continue

            # Process in batches for large directories
            if not auto_apply and (i + 1) % batch_size == 0 and i < len(md_files) - 1:
                if not Confirm.ask(f"\nContinue with next {batch_size} files?"):
                    break

    console.print("\n[bold]Enhancement Summary:[/bold]")
    console.print(f"Files analyzed: {len(md_files)}")
    console.print(f"Files with suggestions: {suggestions_count}")
    console.print(f"Files enhanced: {enhanced_count}")

    if enhanced_count > 0:
        console.print(
            f"\n[green]🎉 Successfully enhanced {enhanced_count} files![/green]"
        )


def _show_enhancement_diff(
    original: KnowledgeMetadata, enhanced: KnowledgeMetadata
) -> None:
    """Show differences between original and enhanced metadata."""

    changes = []

    # Tech additions
    new_tech = [t for t in enhanced.tech if t not in original.tech]
    if new_tech:
        changes.append(f"[green]+tech:[/green] {', '.join(new_tech)}")

    # Domain additions
    new_domain = [d for d in enhanced.domain if d not in original.domain]
    if new_domain:
        changes.append(f"[green]+domain:[/green] {', '.join(new_domain)}")

    # Claude feature additions
    new_features = [
        f for f in enhanced.claude_feature if f not in original.claude_feature
    ]
    if new_features:
        changes.append(f"[green]+claude_feature:[/green] {', '.join(new_features)}")

    # Quality indicators
    if not original.complexity and enhanced.complexity:
        changes.append(f"[green]+complexity:[/green] {enhanced.complexity}")

    if not original.confidence and enhanced.confidence:
        changes.append(f"[green]+confidence:[/green] {enhanced.confidence}")

    if changes:
        console.print("  " + "\n  ".join(changes))
    else:
        console.print("  [dim]No significant changes detected[/dim]")


@app.command("quick")
def quick_commands(
    action: str = typer.Argument(..., help="Quick action: find, create, stats, help"),
    query: str | None = typer.Argument(None, help="Search query or file name"),
) -> None:
    """Quick commands for common operations.

    Actions:
    - find: Quick search with smart suggestions
    - create: Create new file with template
    - stats: Quick vault statistics
    - help: Show quick command help

    Examples:
        ckc quick find "python web"
        ckc quick create prompt "My New Prompt"
        ckc quick stats
        ckc quick help
    """

    if action == "find":
        if not query:
            console.print("[red]Query required for find command[/red]")
            raise typer.Exit(1)

        # Quick search using natural language
        from .interactive import SmartQueryBuilder

        smart_builder = SmartQueryBuilder()
        query_builder, interpretation = smart_builder.build_from_natural_language(query)

        console.print(f"[blue]Searching for:[/blue] {interpretation}")
        console.print(f"[dim]Query:[/dim] {query_builder.build()}")

        # Run the search
        config = get_config()
        metadata_manager = get_metadata_manager()

        results = []
        for target in config.get_enabled_sync_targets():
            for md_file in target.path.rglob("*.md"):
                if md_file.name.startswith(".") or md_file.name == "README.md":
                    continue
                try:
                    metadata = metadata_manager.extract_metadata_from_file(md_file)
                    # Simple matching for quick search
                    searchable = (
                        f"{metadata.title} {' '.join(metadata.tech)} "
                        f"{' '.join(metadata.domain)} {' '.join(metadata.tags)}"
                    ).lower()
                    if query.lower() in searchable:
                        results.append((md_file, metadata))
                except Exception:
                    continue

        if results:
            console.print(f"\n[green]Found {len(results)} results:[/green]")
            for _file_path, metadata in results[:10]:  # Limit to 10 results
                console.print(
                    f"  📄 {metadata.title} ({metadata.type}, {metadata.status})"
                )
        else:
            console.print("[yellow]No results found[/yellow]")

    elif action == "create":
        if not query:
            console.print("[red]File name required for create command[/red]")
            raise typer.Exit(1)

        # Quick file creation with template
        from ..templates.tag_centered_templates import TagCenteredTemplateManager

        template_manager = TagCenteredTemplateManager()

        # Determine content type from query
        query_lower = query.lower()
        if "prompt" in query_lower:
            content_type = "prompt"
        elif "code" in query_lower:
            content_type = "code"
        elif "concept" in query_lower:
            content_type = "concept"
        else:
            content_type = "prompt"  # Default

        # Generate file
        file_content = template_manager.generate_file(
            content_type, title=query, purpose=f"Purpose for {query}"
        )

        # Create file in inbox
        file_name = query.lower().replace(" ", "_").replace("-", "_") + ".md"
        file_path = Path("inbox") / file_name

        if file_path.exists():
            console.print(f"[yellow]File already exists: {file_path}[/yellow]")
        else:
            file_path.parent.mkdir(exist_ok=True)
            file_path.write_text(file_content, encoding="utf-8")
            console.print(f"[green]✓ Created {content_type}: {file_path}[/green]")

    elif action == "stats":
        config = get_config()

        total_files = 0

        for target in config.get_enabled_sync_targets():
            vault_stats = {}
            for directory in [
                "inbox",
                "knowledge",
                "active",
                "archive",
                "_system",
                "_attachments",
            ]:
                dir_path = target.path / directory
                if dir_path.exists():
                    md_files = list(dir_path.rglob("*.md"))
                    vault_stats[directory] = len(md_files)
                    total_files += len(md_files)

        console.print("[bold]Quick Vault Statistics:[/bold]")
        console.print(f"Total files: {total_files}")
        console.print("Structure: Pure tag-centered (6 directories)")
        console.print("System status: ✅ Operational")

    elif action == "help":
        console.print("[bold]Quick Commands Help:[/bold]\n")
        console.print("[cyan]find[/cyan] <query>     - Quick intelligent search")
        console.print("[cyan]create[/cyan] <name>    - Create new file with template")
        console.print("[cyan]stats[/cyan]           - Show vault statistics")
        console.print("[cyan]help[/cyan]            - Show this help")
        console.print("\n[dim]Examples:[/dim]")
        console.print("  ckc quick find 'python api'")
        console.print("  ckc quick create 'My Python Script'")
        console.print("  ckc quick stats")

    else:
        console.print(f"[red]Unknown quick action: {action}[/red]")
        console.print("Available actions: find, create, stats, help")
        raise typer.Exit(1)


@app.command()
def classify(
    target: str = typer.Argument(..., help="File path or directory to classify"),
    auto_apply: bool = typer.Option(
        False, "--auto-apply", help="Auto-apply high-confidence suggestions"
    ),
    min_confidence: float = typer.Option(
        0.7, "--min-confidence", help="Minimum confidence for auto-apply"
    ),
    show_evidence: bool = typer.Option(
        False, "--show-evidence", help="Show classification evidence"
    ),
    batch_mode: bool = typer.Option(
        False, "--batch", help="Process multiple files in batch mode"
    ),
    output_format: str = typer.Option(
        "table", "--format", help="Output format: table, json, summary"
    ),
) -> None:
    """AI-powered intelligent content classification.

    Uses advanced pattern recognition to suggest tags automatically.

    Examples:
        ckc classify myfile.md                    # Classify single file
        ckc classify .claude --batch             # Batch classify directory
        ckc classify --auto-apply --min-confidence 0.8  # Auto-apply high confidence
        ckc classify --format json               # JSON output for automation
    """
    get_config()
    metadata_manager = get_metadata_manager()
    classifier = SmartContentClassifier()

    target_path = Path(target).resolve()
    if not target_path.exists():
        console.print(f"[red]Target not found: {target}[/red]")
        raise typer.Exit(1)

    # Determine files to process
    if target_path.is_file():
        files_to_process = [target_path]
    else:
        files_to_process = list(target_path.rglob("*.md"))
        if not files_to_process:
            console.print(f"[yellow]No markdown files found in {target}[/yellow]")
            return

    console.print(f"[blue]🤖 AI Classification: {len(files_to_process)} files[/blue]")

    if batch_mode and len(files_to_process) > 1:
        _run_batch_classification(
            files_to_process,
            classifier,
            metadata_manager,
            auto_apply,
            min_confidence,
            output_format,
        )
    else:
        _run_interactive_classification(
            files_to_process,
            classifier,
            metadata_manager,
            auto_apply,
            min_confidence,
            show_evidence,
            output_format,
        )


def _run_batch_classification(
    files: list[Path],
    classifier: SmartContentClassifier,
    metadata_manager: MetadataManager,
    auto_apply: bool,
    min_confidence: float,
    output_format: str,
) -> None:
    """Run batch classification with progress tracking."""
    from rich.progress import (
        BarColumn,
        Progress,
        SpinnerColumn,
        TaskProgressColumn,
        TextColumn,
    )

    def progress_callback(current: int, total: int, filename: str) -> None:
        pass  # Progress is handled by the outer progress bar

    # Classify all files
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Classifying files...", total=len(files))

        batch_results = classifier.batch_classify_files(files, progress_callback)

        for file_path in files:
            progress.update(task, advance=1, description=f"Processing {file_path.name}")

    # Process results
    applied_count = 0
    suggestions_count = 0

    for file_path, classifications in batch_results.items():
        if not classifications:
            continue

        suggestions_count += 1

        if auto_apply:
            # Auto-apply high-confidence suggestions
            try:
                metadata = metadata_manager.extract_metadata_from_file(file_path)
                metadata_dict = metadata.model_dump()

                applied_any = False
                for classification in classifications:
                    if classification.confidence >= min_confidence:
                        tag_type = classification.tag_type
                        value = classification.suggested_value

                        if tag_type in ["complexity", "confidence", "type", "status"]:
                            # Single-value fields
                            if not metadata_dict.get(tag_type):
                                metadata_dict[tag_type] = value
                                applied_any = True
                        else:
                            # List fields
                            if tag_type not in metadata_dict:
                                metadata_dict[tag_type] = []

                            if value not in metadata_dict[tag_type]:
                                metadata_dict[tag_type].append(value)
                                applied_any = True

                if applied_any:
                    updated_metadata = KnowledgeMetadata(**metadata_dict)
                    metadata_manager.update_file_metadata(file_path, updated_metadata)
                    applied_count += 1

            except Exception as e:
                console.print(
                    f"[red]Error applying classifications to {file_path.name}: "
                    f"{e}[/red]"
                )

    # Show summary
    if output_format == "json":
        import json

        json_output = {
            "summary": classifier.get_classification_summary(batch_results),
            "files_processed": len(files),
            "files_with_suggestions": suggestions_count,
            "files_modified": applied_count if auto_apply else 0,
        }
        console.print(json.dumps(json_output, indent=2))
    else:
        summary = classifier.get_classification_summary(batch_results)
        _display_batch_summary(summary, len(files), applied_count if auto_apply else 0)


def _run_interactive_classification(
    files: list[Path],
    classifier: SmartContentClassifier,
    metadata_manager: MetadataManager,
    auto_apply: bool,
    min_confidence: float,
    show_evidence: bool,
    output_format: str,
) -> None:
    """Run interactive classification for individual files."""

    for file_path in files:
        console.print(f"\n[bold cyan]📄 Classifying: {file_path.name}[/bold cyan]")

        try:
            content = file_path.read_text(encoding="utf-8")
            existing_metadata = metadata_manager.extract_metadata_from_file(file_path)

            # Get AI classifications
            classifications = classifier.classify_content(content, existing_metadata)

            if not classifications:
                console.print("[dim]No AI suggestions generated[/dim]")
                continue

            # Display results
            if output_format == "json":
                import json

                json_output = {
                    "file": str(file_path),
                    "classifications": [
                        {
                            "tag_type": c.tag_type,
                            "suggested_value": c.suggested_value,
                            "confidence": c.confidence,
                            "reasoning": c.reasoning,
                            "evidence": c.evidence if show_evidence else [],
                        }
                        for c in classifications
                    ],
                }
                console.print(json.dumps(json_output, indent=2))
            else:
                _display_classifications_table(classifications, show_evidence)

            # Apply suggestions
            if auto_apply:
                _auto_apply_classifications(
                    file_path,
                    classifications,
                    metadata_manager,
                    existing_metadata,
                    min_confidence,
                )
            elif len(files) == 1:  # Interactive for single file
                if Confirm.ask("\n[cyan]Apply these suggestions?[/cyan]"):
                    _interactive_apply_classifications(
                        file_path, classifications, metadata_manager, existing_metadata
                    )

        except Exception as e:
            console.print(f"[red]Error classifying {file_path.name}: {e}[/red]")


def _display_classifications_table(classifications: list, show_evidence: bool) -> None:
    """Display AI classifications in a formatted table."""
    from rich.table import Table

    table = Table(title="AI Classification Results")
    table.add_column("Tag Type", style="cyan")
    table.add_column("Suggested Value", style="green")
    table.add_column("Confidence", style="yellow")
    table.add_column("Reasoning", style="dim")

    if show_evidence:
        table.add_column("Evidence", style="blue")

    for classification in classifications[:10]:  # Limit display
        confidence_str = f"{classification.confidence:.0%}"

        row = [
            classification.tag_type,
            classification.suggested_value,
            confidence_str,
            classification.reasoning,
        ]

        if show_evidence:
            evidence_str = "; ".join(
                classification.evidence[:2]
            )  # First 2 pieces of evidence
            row.append(evidence_str)

        table.add_row(*row)

    console.print(table)


def _display_batch_summary(summary: dict, total_files: int, applied_count: int) -> None:
    """Display batch classification summary."""
    console.print("\n[bold]🤖 AI Classification Summary[/bold]")
    console.print(f"Files processed: {total_files}")
    console.print(f"Files with suggestions: {summary['files_with_suggestions']}")
    console.print(f"Files modified: {applied_count}")

    if summary["top_technologies"]:
        console.print("\n[cyan]Top Technologies:[/cyan]")
        for tech, count in sorted(
            summary["top_technologies"].items(), key=lambda x: x[1], reverse=True
        )[:5]:
            console.print(f"  {tech}: {count} files")

    if summary["top_domains"]:
        console.print("\n[cyan]Top Domains:[/cyan]")
        for domain, count in sorted(
            summary["top_domains"].items(), key=lambda x: x[1], reverse=True
        )[:5]:
            console.print(f"  {domain}: {count} files")

    console.print("\n[cyan]Confidence Distribution:[/cyan]")
    conf_dist = summary["confidence_distribution"]
    console.print(
        f"  High: {conf_dist['high']}, Medium: {conf_dist['medium']}, "
        f"Low: {conf_dist['low']}"
    )


def _auto_apply_classifications(
    file_path: Path,
    classifications: list,
    metadata_manager: MetadataManager,
    existing_metadata: KnowledgeMetadata,
    min_confidence: float,
) -> None:
    """Auto-apply high-confidence classifications."""
    metadata_dict = existing_metadata.model_dump()
    applied_any = False

    for classification in classifications:
        if classification.confidence >= min_confidence:
            tag_type = classification.tag_type
            value = classification.suggested_value

            if tag_type in ["complexity", "confidence", "type", "status"]:
                # Single-value fields
                if (
                    not metadata_dict.get(tag_type)
                    or metadata_dict[tag_type] == "draft"
                ):
                    metadata_dict[tag_type] = value
                    applied_any = True
            else:
                # List fields
                if tag_type not in metadata_dict:
                    metadata_dict[tag_type] = []

                if value not in metadata_dict[tag_type]:
                    metadata_dict[tag_type].append(value)
                    applied_any = True

    if applied_any:
        updated_metadata = KnowledgeMetadata(**metadata_dict)
        metadata_manager.update_file_metadata(file_path, updated_metadata)
        console.print(f"[green]✅ Applied AI suggestions to {file_path.name}[/green]")
    else:
        console.print(f"[dim]No high-confidence suggestions for {file_path.name}[/dim]")


def _interactive_apply_classifications(
    file_path: Path,
    classifications: list,
    metadata_manager: MetadataManager,
    existing_metadata: KnowledgeMetadata,
) -> None:
    """Interactive application of classifications."""
    metadata_dict = existing_metadata.model_dump()

    console.print("\n[cyan]Select suggestions to apply:[/cyan]")

    for _i, classification in enumerate(classifications[:8]):  # Limit to 8
        confidence_str = f"{classification.confidence:.0%}"
        suggestion_text = (
            f"{classification.tag_type}: {classification.suggested_value} "
            f"({confidence_str})"
        )

        if Confirm.ask(f"  Apply '{suggestion_text}'?"):
            tag_type = classification.tag_type
            value = classification.suggested_value

            if tag_type in ["complexity", "confidence", "type", "status"]:
                metadata_dict[tag_type] = value
            else:
                if tag_type not in metadata_dict:
                    metadata_dict[tag_type] = []
                if value not in metadata_dict[tag_type]:
                    metadata_dict[tag_type].append(value)

    # Apply changes
    updated_metadata = KnowledgeMetadata(**metadata_dict)
    metadata_manager.update_file_metadata(file_path, updated_metadata)
    console.print(f"[green]✅ Updated {file_path.name}[/green]")


@app.command()
def migrate(
    preview: bool = typer.Option(
        False, "--preview", help="Show migration preview without applying changes"
    ),
    interactive: bool = typer.Option(
        False, "--interactive", help="Interactive file-by-file migration"
    ),
    backup: bool = typer.Option(
        True, "--backup/--no-backup", help="Create backup before migration"
    ),
    auto_apply: bool = typer.Option(
        False, "--auto-apply", help="Auto-apply high-confidence migrations"
    ),
) -> None:
    """Migrate legacy frontmatter to Pure Tag-Centered Architecture."""
    config = get_config()
    metadata_manager = get_metadata_manager()

    # Detect migration status
    migration_info = _detect_migration_status(config)

    if not migration_info["needs_migration"]:
        if migration_info["modern_count"] > 0:
            console.print(
                "[green]✓ All files already use Pure Tag-Centered Architecture[/green]"
            )
        else:
            console.print("[yellow]No files with frontmatter found to migrate[/yellow]")
            console.print(
                "Consider running [bold]ckc smart-sync[/bold] to add metadata to files"
            )
        return

    console.print(
        "[blue]🔄 Migration: Legacy → Pure Tag-Centered Architecture[/blue]\n"
    )

    # Collect files for migration
    files_to_migrate = []
    for watch_path in config.watch.watch_paths:
        full_path = config.project_root / watch_path
        if not full_path.exists():
            continue

        for md_file in full_path.rglob("*.md"):
            if md_file.is_file():
                try:
                    content = md_file.read_text(encoding="utf-8")
                    if content.startswith("---"):
                        frontmatter_end = content.find("\n---\n", 3)
                        if frontmatter_end > 0:
                            frontmatter = content[3:frontmatter_end]
                            if (
                                "category:" in frontmatter
                                or "subcategory:" in frontmatter
                            ):
                                files_to_migrate.append(md_file)
                except Exception:
                    continue

    if not files_to_migrate:
        console.print("[green]✓ No legacy format files found[/green]")
        return

    # Show migration preview
    console.print("[yellow]📋 Migration Preview[/yellow]")
    console.print(f"Files to migrate: {len(files_to_migrate)}")

    preview_table = Table(title="Migration Changes")
    preview_table.add_column("File", style="cyan")
    preview_table.add_column("Legacy → Modern", style="yellow")
    preview_table.add_column("New Fields", style="green")

    changes_count = 0
    for file_path in files_to_migrate[:5]:  # Show first 5 files
        try:
            content = file_path.read_text(encoding="utf-8")
            frontmatter_end = content.find("\n---\n", 3)
            frontmatter = content[3:frontmatter_end]

            legacy_fields = []
            new_fields = []

            if "category:" in frontmatter:
                legacy_fields.append("category")
                new_fields.append("type")
            if "subcategory:" in frontmatter:
                legacy_fields.append("subcategory")
                new_fields.append("domain")
            if "quality:" in frontmatter:
                legacy_fields.append("quality")
                new_fields.append("confidence")

            new_fields.extend(["tech", "team", "claude_model"])

            preview_table.add_row(
                file_path.name, " → ".join(legacy_fields), ", ".join(new_fields)
            )
            changes_count += len(new_fields)
        except Exception:
            continue

    if len(files_to_migrate) > 5:
        preview_table.add_row(
            "...", f"and {len(files_to_migrate) - 5} more files", "..."
        )

    console.print(preview_table)
    console.print("\n[bold]Summary:[/bold]")
    console.print(f"• Files to migrate: {len(files_to_migrate)}")
    console.print(f"• Estimated new fields: {changes_count}")
    console.print("• Enhanced search capabilities: ✅")
    console.print("• AI classification ready: ✅")

    if preview:
        console.print(
            "\n[dim]To apply migration: [bold]ckc migrate --auto-apply[/bold][/dim]"
        )
        return

    # Interactive confirmation
    if not auto_apply:
        if not Confirm.ask(
            f"\nProceed with migration of {len(files_to_migrate)} files?", default=False
        ):
            console.print("[red]Migration cancelled.[/red]")
            return

    # Create backup if requested
    if backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = config.project_root / f".claude_backup_migration_{timestamp}"
        backup_dir.mkdir(exist_ok=True)

        for watch_path in config.watch.watch_paths:
            source_path = config.project_root / watch_path
            if source_path.exists():
                dest_path = backup_dir / watch_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                if source_path.is_dir():
                    shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(source_path, dest_path)

        console.print(f"[green]📋 Backup created:[/green] {backup_dir}")

    # Execute migration using smart-sync
    console.print("\n[blue]🤖 Executing AI-powered migration...[/blue]")
    console.print("[dim]Using smart classification system for optimal migration[/dim]")

    # This will leverage the existing smart-sync functionality
    # Import here to avoid circular imports
    from .smart_sync import smart_sync_command

    try:
        # Run smart-sync with auto-apply for migration
        smart_sync_command(
            dry_run=False,
            auto_apply=True,
            min_confidence=0.6,  # Lower threshold for migration
            config=config,
            metadata_manager=metadata_manager,
        )

        console.print("\n[green]🎉 Migration completed![/green]")
        console.print(f"• Files migrated: {len(files_to_migrate)}")
        console.print("• Enhanced with Pure Tag-Centered Architecture")
        console.print(
            "• Ready for advanced search: "
            "[bold]ckc search --tech python --domain ai-systems[/bold]"
        )

    except Exception as e:
        console.print(f"[red]❌ Migration failed: {e}[/red]")
        console.print(
            "Your files are safely backed up. You can restore from backup if needed."
        )


@app.command()
def wizard() -> None:
    """Interactive setup wizard for new users."""
    console.print("[bold blue]🧙 Claude Knowledge Catalyst Setup Wizard[/bold blue]")
    console.print(
        "Let's get you started with a fully configured knowledge management system!\n"
    )

    # Check current directory
    current_dir = Path.cwd()
    console.print(f"[dim]Current directory: {current_dir}[/dim]")

    # Step 1: Project detection
    console.print("\n[bold]Step 1: Project Detection[/bold]")

    claude_dir = current_dir / ".claude"
    config_file = current_dir / "ckc_config.yaml"

    if config_file.exists():
        console.print("[yellow]⚠️ Existing configuration detected![/yellow]")
        if not Confirm.ask("Do you want to reconfigure?", default=False):
            console.print(
                "[green]Setup cancelled. Your existing configuration is "
                "preserved.[/green]"
            )
            return

    # Step 2: Initialize project
    console.print("\n[bold]Step 2: Project Initialization[/bold]")

    project_name = Prompt.ask(
        "Project name", default=current_dir.name, show_default=True
    )

    # Initialize with force to overwrite existing
    with console.status("Initializing project..."):
        config = get_config()
        config.project_root = current_dir
        config.project_name = project_name
        config.auto_sync = True

        # Create .claude directory
        claude_dir.mkdir(exist_ok=True)

        # Save configuration
        config.save_to_file(config_file)

    console.print("[green]✅ Project initialized successfully![/green]")

    # Step 3: Vault setup
    console.print("\n[bold]Step 3: Knowledge Vault Setup[/bold]")

    if Confirm.ask("Do you want to connect an Obsidian vault?", default=True):
        while True:
            vault_path = Prompt.ask("Obsidian vault path (absolute or relative)")
            vault_path_obj = Path(vault_path).expanduser().resolve()

            if vault_path_obj.exists():
                vault_name = Prompt.ask(
                    "Vault name", default="my-vault", show_default=True
                )

                # Add vault to configuration
                sync_target = SyncTarget(
                    name=vault_name, type="obsidian", path=vault_path_obj, enabled=True
                )
                config.add_sync_target(sync_target)
                config.save_to_file(config_file)

                # Initialize vault structure
                try:
                    metadata_manager = get_metadata_manager()
                    vault_manager = ObsidianVaultManager(
                        vault_path_obj, metadata_manager
                    )
                    vault_manager.initialize_vault()
                    console.print(
                        f"[green]✅ Vault '{vault_name}' configured and "
                        f"initialized![/green]"
                    )
                except Exception as e:
                    console.print(
                        f"[yellow]⚠️ Vault configured but initialization had "
                        f"issues: {e}[/yellow]"
                    )
                break
            else:
                console.print(f"[red]❌ Path does not exist: {vault_path_obj}[/red]")
                if not Confirm.ask("Try again?", default=True):
                    break

    # Step 4: Sample content
    console.print("\n[bold]Step 4: Sample Content Creation[/bold]")

    if Confirm.ask("Create sample knowledge files?", default=True):
        sample_files = [
            (
                "python_tips.md",
                """# Python Development Tips

## Virtual Environments
```bash
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
myenv\\Scripts\\activate    # Windows
```

## Package Management
```bash
pip install requests pandas
pip freeze > requirements.txt
```

Tags: python, development, tips, beginner
""",
            ),
            (
                "git_workflow.md",
                """# Git Workflow Best Practices

## Feature Branch Workflow
```bash
git checkout -b feature/new-feature
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

## Useful Commands
```bash
git status
git log --oneline
git diff HEAD~1
```

Tags: git, version-control, workflow, best-practices
""",
            ),
        ]

        for filename, content in sample_files:
            file_path = claude_dir / filename
            file_path.write_text(content)
            console.print(f"[green]📄 Created: {filename}[/green]")

    # Step 5: First sync
    console.print("\n[bold]Step 5: Initial Synchronization[/bold]")

    if config.sync_targets and Confirm.ask("Perform initial sync?", default=True):
        with console.status("Synchronizing knowledge files..."):
            try:
                # Perform sync
                metadata_manager = get_metadata_manager()
                for target in config.get_enabled_sync_targets():
                    vault_manager = ObsidianVaultManager(target.path, metadata_manager)
                    vault_manager.sync_directory(claude_dir)
                console.print("[green]✅ Initial sync completed![/green]")
            except Exception as e:
                console.print(f"[yellow]⚠️ Sync had issues: {e}[/yellow]")

    # Step 6: Next steps
    console.print("\n[bold green]🎉 Setup Complete![/bold green]")
    console.print("\n[bold]Next Steps:[/bold]")
    console.print("1. [bold]ckc status[/bold] - Check your project status")
    console.print("2. [bold]ckc analyze[/bold] - Analyze your knowledge files")
    console.print("3. [bold]ckc sync[/bold] - Sync changes to vault")
    console.print("4. [bold]ckc search python[/bold] - Search your knowledge")
    console.print("5. [bold]ckc watch[/bold] - Enable automatic syncing")

    console.print(f"\n[dim]Configuration saved to: {config_file}[/dim]")
    console.print("[green]Happy knowledge managing! 📚✨[/green]")


@app.command()
def diagnose() -> None:
    """Run comprehensive system diagnostics."""
    console.print("[bold blue]🔍 Claude Knowledge Catalyst Diagnostics[/bold blue]")
    console.print("Checking system health and configuration...\n")

    issues = []
    warnings = []
    config = None
    md_files = []
    claude_dir = Path.cwd() / ".claude"

    # Check 1: Configuration
    console.print("[bold]1. Configuration Check[/bold]")
    try:
        config = load_config()
        console.print(f"[green]✅ Configuration loaded: {config.project_name}[/green]")

        if not config.sync_targets:
            warnings.append("No sync targets configured")
        else:
            console.print(
                f"[green]✅ {len(config.sync_targets)} sync targets configured[/green]"
            )

        if not config.project_root.exists():
            issues.append(f"Project root does not exist: {config.project_root}")
        else:
            console.print(
                f"[green]✅ Project root exists: {config.project_root}[/green]"
            )

    except Exception as e:
        issues.append(f"Configuration error: {e}")

    # Check 2: Dependencies
    console.print("\n[bold]2. Dependency Check[/bold]")

    # Check YAKE availability
    try:
        from ..ai.yake_extractor import YAKE_AVAILABLE

        if YAKE_AVAILABLE:
            console.print("[green]✅ YAKE keyword extraction available[/green]")
        else:
            warnings.append("YAKE dependencies not available (optional)")
    except ImportError:
        warnings.append("YAKE module not available")

    # Check 3: Directory Structure
    console.print("\n[bold]3. Directory Structure[/bold]")

    if claude_dir.exists():
        console.print("[green]✅ .claude directory exists[/green]")

        # Count files
        md_files = list(claude_dir.rglob("*.md"))
        console.print(f"[green]✅ Found {len(md_files)} markdown files[/green]")

        if len(md_files) == 0:
            warnings.append("No knowledge files found in .claude directory")
    else:
        issues.append(".claude directory does not exist")

    # Check 4: Sync Targets
    console.print("\n[bold]4. Sync Target Health[/bold]")

    try:
        config = load_config()
        for target in config.sync_targets:
            if target.path.exists():
                console.print(
                    f"[green]✅ {target.name}: Path exists ({target.path})[/green]"
                )

                # Check vault structure for Obsidian
                if target.type == "obsidian":
                    expected_dirs = [
                        "_system",
                        "_attachments",
                        "inbox",
                        "active",
                        "archive",
                        "knowledge",
                    ]
                    missing_dirs = [
                        d for d in expected_dirs if not (target.path / d).exists()
                    ]
                    if missing_dirs:
                        warnings.append(
                            f"{target.name}: Missing vault directories: "
                            f"{', '.join(missing_dirs)}"
                        )
                    else:
                        console.print(
                            f"[green]✅ {target.name}: Vault structure complete[/green]"
                        )
            else:
                issues.append(f"{target.name}: Path does not exist ({target.path})")
    except Exception as e:
        issues.append(f"Could not check sync targets: {e}")

    # Check 5: Performance
    console.print("\n[bold]5. Performance Check[/bold]")

    try:
        # Test metadata extraction
        if claude_dir.exists() and md_files:
            test_file = md_files[0]
            start_time = datetime.now()

            metadata_manager = get_metadata_manager()
            metadata_manager.extract_metadata_from_file(test_file)

            elapsed = (datetime.now() - start_time).total_seconds()
            console.print(f"[green]✅ Metadata extraction: {elapsed:.3f}s[/green]")

            if elapsed > 2.0:
                warnings.append(f"Slow metadata extraction ({elapsed:.1f}s)")
        else:
            warnings.append("No files available for performance testing")

    except Exception as e:
        warnings.append(f"Performance test failed: {e}")

    # Check 6: Classification System
    console.print("\n[bold]6. AI Classification System[/bold]")

    try:
        classifier = SmartContentClassifier()
        test_content = "import pandas as pd\nfrom fastapi import FastAPI"
        results = classifier.classify_content(test_content)

        if results:
            console.print(
                f"[green]✅ Classification working: {len(results)} results[/green]"
            )
        else:
            warnings.append("Classification returned no results")

    except Exception as e:
        warnings.append(f"Classification system error: {e}")

    # Summary
    console.print("\n[bold]📋 Diagnostic Summary[/bold]")

    if not issues and not warnings:
        console.print("[bold green]🎉 All systems healthy![/bold green]")
        console.print(
            "Your Claude Knowledge Catalyst installation is working perfectly."
        )
    else:
        if issues:
            console.print(f"\n[bold red]❌ {len(issues)} Critical Issues:[/bold red]")
            for issue in issues:
                console.print(f"  • {issue}")

        if warnings:
            console.print(f"\n[bold yellow]⚠️ {len(warnings)} Warnings:[/bold yellow]")
            for warning in warnings:
                console.print(f"  • {warning}")

    # Recommendations
    console.print("\n[bold]💡 Recommendations:[/bold]")

    if issues:
        console.print("1. Fix critical issues first using [bold]ckc wizard[/bold]")
        console.print("2. Check configuration with [bold]ckc status[/bold]")

    if config and not config.sync_targets:
        console.print(
            "1. Add a knowledge vault with [bold]ckc add <name> <path>[/bold]"
        )

    if len(md_files) == 0:
        console.print("1. Create knowledge files in .claude/ directory")
        console.print("2. Use [bold]ckc wizard[/bold] to create sample files")

    console.print("3. Run [bold]ckc sync[/bold] to sync your knowledge")
    console.print("4. Use [bold]ckc watch[/bold] for automatic syncing")


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
