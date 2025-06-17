"""Main CLI interface for Claude Knowledge Catalyst."""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from ..core.config import CKCConfig, SyncTarget, load_config
from ..core.metadata import MetadataManager
from ..core.watcher import KnowledgeWatcher
from ..sync.obsidian import ObsidianSyncManager

console = Console()


@click.group()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, path_type=Path),
    help="Path to configuration file",
)
@click.pass_context
def cli(ctx: click.Context, config: Path | None) -> None:
    """Claude Knowledge Catalyst - Sync your Claude Code insights."""
    ctx.ensure_object(dict)

    # Load configuration
    try:
        ctx.obj["config"] = load_config(config)
        ctx.obj["metadata_manager"] = MetadataManager()
    except Exception as e:
        console.print(f"[red]Error loading configuration: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.pass_context
def init(ctx: click.Context) -> None:
    """Initialize CKC in the current directory."""
    config: CKCConfig = ctx.obj["config"]

    console.print("[blue]Initializing Claude Knowledge Catalyst...[/blue]")

    # Set project root to current directory
    config.project_root = Path.cwd()

    # Create .claude directory if it doesn't exist
    claude_dir = Path.cwd() / ".claude"
    claude_dir.mkdir(exist_ok=True)

    # Create default config file
    config_path = Path.cwd() / "ckc_config.yaml"
    config.save_to_file(config_path)

    console.print(f"[green]✓[/green] Created configuration file: {config_path}")
    console.print(f"[green]✓[/green] Created .claude directory: {claude_dir}")

    console.print("\n[yellow]Next steps:[/yellow]")
    console.print("1. Configure sync targets with: [bold]ckc sync add[/bold]")
    console.print("2. Start watching for changes with: [bold]ckc watch[/bold]")
    console.print("3. Sync existing files with: [bold]ckc sync run[/bold]")


@cli.group()
def sync() -> None:
    """Manage synchronization targets and operations."""
    pass


@sync.command("add")
@click.argument("name")
@click.argument("type", type=click.Choice(["obsidian", "notion", "file"]))
@click.argument("path", type=click.Path(path_type=Path))
@click.option("--disabled", is_flag=True, help="Add target as disabled")
@click.pass_context
def sync_add(
    ctx: click.Context, name: str, type: str, path: Path, disabled: bool
) -> None:
    """Add a new sync target."""
    config: CKCConfig = ctx.obj["config"]

    # Create sync target
    sync_target = SyncTarget(
        name=name,
        type=type,
        path=path,
        enabled=not disabled,
    )

    # Add to configuration
    config.add_sync_target(sync_target)

    # Save configuration
    config_path = Path.cwd() / "ckc_config.yaml"
    config.save_to_file(config_path)

    console.print(f"[green]✓[/green] Added sync target: {name} ({type}) -> {path}")

    # Initialize if it's Obsidian
    if type == "obsidian":
        metadata_manager: MetadataManager = ctx.obj["metadata_manager"]
        obsidian_manager = ObsidianSyncManager(sync_target, metadata_manager)
        if obsidian_manager.initialize():
            console.print(f"[green]✓[/green] Initialized Obsidian vault at {path}")
        else:
            console.print("[yellow]![/yellow] Failed to initialize Obsidian vault")


@sync.command("list")
@click.pass_context
def sync_list(ctx: click.Context) -> None:
    """List all sync targets."""
    config: CKCConfig = ctx.obj["config"]

    if not config.sync_targets:
        console.print("[yellow]No sync targets configured[/yellow]")
        return

    table = Table(title="Sync Targets")
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Path")
    table.add_column("Status")

    for target in config.sync_targets:
        status = "[green]Enabled[/green]" if target.enabled else "[red]Disabled[/red]"
        table.add_row(target.name, target.type, str(target.path), status)

    console.print(table)


@sync.command("remove")
@click.argument("name")
@click.pass_context
def sync_remove(ctx: click.Context, name: str) -> None:
    """Remove a sync target."""
    config: CKCConfig = ctx.obj["config"]

    if config.remove_sync_target(name):
        # Save configuration
        config_path = Path.cwd() / "ckc_config.yaml"
        config.save_to_file(config_path)
        console.print(f"[green]✓[/green] Removed sync target: {name}")
    else:
        console.print(f"[red]✗[/red] Sync target not found: {name}")


@sync.command("run")
@click.option("--target", help="Specific target to sync to")
@click.option("--project", help="Project name for organization")
@click.pass_context
def sync_run(ctx: click.Context, target: str | None, project: str | None) -> None:
    """Run synchronization for all or specific targets."""
    config: CKCConfig = ctx.obj["config"]
    metadata_manager: MetadataManager = ctx.obj["metadata_manager"]

    # Get targets to sync
    targets_to_sync = config.get_enabled_sync_targets()
    if target:
        targets_to_sync = [t for t in targets_to_sync if t.name == target]
        if not targets_to_sync:
            console.print(f"[red]✗[/red] Sync target not found or disabled: {target}")
            return

    if not targets_to_sync:
        console.print("[yellow]No enabled sync targets found[/yellow]")
        return

    # Find .claude directory
    claude_dir = config.project_root / ".claude"
    if not claude_dir.exists():
        console.print(f"[red]✗[/red] .claude directory not found at: {claude_dir}")
        return

    console.print(f"[blue]Syncing from: {claude_dir}[/blue]")

    # Sync each target
    for sync_target in targets_to_sync:
        console.print(
            f"\n[yellow]Syncing to {sync_target.name} ({sync_target.type})...[/yellow]"
        )

        try:
            if sync_target.type == "obsidian":
                obsidian_manager = ObsidianSyncManager(sync_target, metadata_manager)
                results = obsidian_manager.sync_claude_directory(claude_dir, project)

                # Show results
                success_count = sum(1 for success in results.values() if success)
                total_count = len(results)
                console.print(
                    f"[green]✓[/green] Synced {success_count}/{total_count} files"
                )

                # Show failed files
                failed_files = [
                    path for path, success in results.items() if not success
                ]
                if failed_files:
                    console.print("[red]Failed files:[/red]")
                    for file_path in failed_files:
                        console.print(f"  - {file_path}")

            else:
                message = (
                    f"[yellow]![/yellow] Sync type '{sync_target.type}' "
                    "not yet implemented"
                )
                console.print(message)

        except Exception as e:
            console.print(f"[red]✗[/red] Error syncing to {sync_target.name}: {e}")


@cli.command()
@click.option("--daemon", "-d", is_flag=True, help="Run as daemon")
@click.pass_context
def watch(ctx: click.Context, daemon: bool) -> None:
    """Start watching for file changes."""
    config: CKCConfig = ctx.obj["config"]
    metadata_manager: MetadataManager = ctx.obj["metadata_manager"]

    if not config.auto_sync:
        console.print("[yellow]Auto-sync is disabled in configuration[/yellow]")
        return

    # Create sync callback
    def sync_callback(event_type: str, file_path: Path) -> None:
        """Callback for file changes."""
        console.print(f"[dim]File {event_type}: {file_path}[/dim]")

        # Sync to enabled targets
        for sync_target in config.get_enabled_sync_targets():
            try:
                if sync_target.type == "obsidian":
                    obsidian_manager = ObsidianSyncManager(
                        sync_target, metadata_manager
                    )
                    project_name = config.project_name or None
                    obsidian_manager.sync_single_file(file_path, project_name)
            except Exception as e:
                console.print(f"[red]Sync error: {e}[/red]")

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


@cli.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """Show current status and configuration."""
    config: CKCConfig = ctx.obj["config"]

    console.print("[bold]Claude Knowledge Catalyst Status[/bold]\n")

    # Project info
    console.print(f"[blue]Project:[/blue] {config.project_name or 'Unnamed'}")
    console.print(f"[blue]Root:[/blue] {config.project_root}")
    console.print(
        f"[blue]Auto-sync:[/blue] {'Enabled' if config.auto_sync else 'Disabled'}"
    )

    # Watch paths
    console.print("\n[blue]Watch Paths:[/blue]")
    for path in config.watch.watch_paths:
        status = "✓" if path.exists() else "✗"
        console.print(f"  {status} {path}")

    # Sync targets
    console.print("\n[blue]Sync Targets:[/blue]")
    if not config.sync_targets:
        console.print("  [dim]None configured[/dim]")
    else:
        for target in config.sync_targets:
            status = (
                "[green]✓[/green]"
                if target.enabled and target.path.exists()
                else "[red]✗[/red]"
            )
            console.print(f"  {status} {target.name} ({target.type}) -> {target.path}")


@cli.command()
@click.argument("file_path", type=click.Path(exists=True, path_type=Path))
@click.pass_context
def analyze(ctx: click.Context, file_path: Path) -> None:
    """Analyze a specific file and show its metadata."""
    metadata_manager: MetadataManager = ctx.obj["metadata_manager"]

    try:
        metadata = metadata_manager.extract_metadata_from_file(file_path)

        console.print(f"[bold]Analysis of: {file_path}[/bold]\n")

        # Basic metadata
        table = Table(title="Metadata")
        table.add_column("Field")
        table.add_column("Value")

        table.add_row("Title", metadata.title)
        table.add_row("Created", metadata.created.strftime("%Y-%m-%d %H:%M:%S"))
        table.add_row("Updated", metadata.updated.strftime("%Y-%m-%d %H:%M:%S"))
        table.add_row("Version", metadata.version)
        table.add_row("Category", metadata.category or "N/A")
        table.add_row("Status", metadata.status)
        table.add_row("Model", metadata.model or "N/A")
        table.add_row(
            "Success Rate",
            f"{metadata.success_rate}%" if metadata.success_rate else "N/A",
        )

        console.print(table)

        # Tags
        if metadata.tags:
            console.print(f"\n[blue]Tags:[/blue] {', '.join(metadata.tags)}")

        # Related projects
        if metadata.related_projects:
            projects = ', '.join(metadata.related_projects)
            console.print(f"\n[blue]Related Projects:[/blue] {projects}")

        # Purpose
        if metadata.purpose:
            console.print(f"\n[blue]Purpose:[/blue] {metadata.purpose}")

    except Exception as e:
        console.print(f"[red]Error analyzing file: {e}[/red]")


def main() -> None:
    """Main entry point for the CLI."""
    cli()
