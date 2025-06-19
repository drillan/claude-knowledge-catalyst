"""Modern CLI interface for Claude Knowledge Catalyst using Typer."""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from ..core.config import CKCConfig, SyncTarget, load_config
from ..core.metadata import MetadataManager
from ..core.watcher import KnowledgeWatcher
from ..core.hybrid_config import NumberingSystem
from ..sync.hybrid_manager import HybridObsidianVaultManager
from .. import __version__

def version_callback(value: bool) -> None:
    """Show version information."""
    if value:
        console = Console()
        console.print(f"[bold blue]Claude Knowledge Catalyst (CKC)[/bold blue] v{__version__}")
        console.print("[dim]A comprehensive knowledge management system for Claude Code development insights.[/dim]")
        raise typer.Exit()


# Initialize Typer app and Rich console
app = typer.Typer(
    name="ckc",
    help="Claude Knowledge Catalyst - Modern knowledge management system",
    no_args_is_help=True,
    rich_markup_mode="rich"
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
        help="Show version information"
    )
) -> None:
    """Claude Knowledge Catalyst CLI."""
    pass

# Global state
_config: Optional[CKCConfig] = None
_metadata_manager: Optional[MetadataManager] = None


def get_config(config_path: Optional[Path] = None) -> CKCConfig:
    """Get or load configuration."""
    global _config, _metadata_manager
    
    if _config is None:
        try:
            _config = load_config(config_path)
            _metadata_manager = MetadataManager()
        except Exception as e:
            console.print(f"[red]Error loading configuration: {e}[/red]")
            raise typer.Exit(1)
    
    return _config


def get_metadata_manager() -> MetadataManager:
    """Get metadata manager."""
    if _metadata_manager is None:
        get_config()  # This will initialize both
    return _metadata_manager


@app.command()
def init() -> None:
    """Initialize CKC workspace with modern hybrid structure."""
    console.print("[blue]Initializing Claude Knowledge Catalyst...[/blue]")
    
    # Load or create config
    config = get_config()
    
    # Set project root to current directory
    config.project_root = Path.cwd()
    
    # Always use modern hybrid structure
    config.hybrid_structure.enabled = True
    config.hybrid_structure.numbering_system = NumberingSystem.TEN_STEP
    config.hybrid_structure.auto_classification = True
    
    console.print("[green]✓[/green] Modern hybrid structure configured")
    
    # Create .claude directory
    claude_dir = Path.cwd() / ".claude"
    claude_dir.mkdir(exist_ok=True)
    
    # Save configuration
    config_path = Path.cwd() / "ckc_config.yaml"
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
    disabled: bool = typer.Option(False, "--disabled", help="Add target as disabled")
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
    
    # Initialize vault with modern structure
    vault_manager = HybridObsidianVaultManager(vault_path, metadata_manager, config)
    
    if vault_manager.initialize_vault():
        console.print(f"[green]✓[/green] Initialized vault with modern structure")
    else:
        console.print("[yellow]![/yellow] Vault initialization had issues")


@app.command()
def sync(
    target: Optional[str] = typer.Option(None, "--target", "-t", help="Specific target to sync"),
    project: Optional[str] = typer.Option(None, "--project", "-p", help="Project name for organization")
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
            # Always use modern hybrid manager
            vault_manager = HybridObsidianVaultManager(sync_target.path, metadata_manager, config)
            results = vault_manager.sync_directory(claude_dir, project)
            
            # Show results
            success_count = sum(1 for success in results.values() if success)
            total_count = len(results)
            total_synced += success_count
            
            console.print(f"[green]✓[/green] Synced {success_count}/{total_count} files")
            
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
    daemon: bool = typer.Option(False, "--daemon", "-d", help="Run as daemon")
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
                vault_manager = HybridObsidianVaultManager(sync_target.path, metadata_manager, config)
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


@app.command()
def status() -> None:
    """Show current status and configuration."""
    config = get_config()
    
    console.print("[bold]Claude Knowledge Catalyst Status[/bold]\n")
    
    # Project info
    console.print(f"[blue]Project:[/blue] {config.project_name or 'Unnamed'}")
    console.print(f"[blue]Root:[/blue] {config.project_root}")
    console.print(f"[blue]Auto-sync:[/blue] {'Enabled' if config.auto_sync else 'Disabled'}")
    console.print(f"[blue]Structure:[/blue] Modern Hybrid (10-step)")
    
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
                "[green]✓[/green]" if target.enabled and target.path.exists()
                else "[red]✗[/red]"
            )
            console.print(f"  {status_icon} {target.name} -> {target.path}")


@app.command()
def analyze(
    file_path: str = typer.Argument(..., help="Path to file to analyze")
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
        table.add_row("Category", metadata.category or "N/A")
        table.add_row("Project", metadata.project or "N/A")
        table.add_row("Status", metadata.status)
        table.add_row("Version", metadata.version)
        table.add_row("Created", metadata.created.strftime("%Y-%m-%d %H:%M:%S"))
        table.add_row("Updated", metadata.updated.strftime("%Y-%m-%d %H:%M:%S"))
        
        if metadata.success_rate:
            table.add_row("Success Rate", f"{metadata.success_rate}%")
        if metadata.model:
            table.add_row("Model", metadata.model)
        
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
        console.print(f"[red]✗[/red] Error analyzing file: {e}")
        raise typer.Exit(1)


@app.command()
def project(
    action: str = typer.Argument(..., help="Action: list, files, stats"),
    name: Optional[str] = typer.Argument(None, help="Project name")
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
    
    # Check sync targets for existing projects
    for target in config.get_enabled_sync_targets():
        projects_dir = target.path / "10_Projects"
        if projects_dir.exists():
            for project_dir in projects_dir.iterdir():
                if project_dir.is_dir() and not project_dir.name.startswith('.') and project_dir.name != "README.md":
                    projects.add(project_dir.name)
    
    # Also check .claude directory for potential projects
    claude_dir = config.project_root / ".claude"
    if claude_dir.exists():
        for item in claude_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                projects.add(item.name)
    
    # Check for files that indicate project organization
    for target in config.get_enabled_sync_targets():
        # Look for project-tagged files throughout the vault
        for md_file in target.path.rglob("*.md"):
            if md_file.name != "README.md" and not md_file.name.startswith('.'):
                try:
                    metadata = metadata_manager.extract_metadata_from_file(md_file)
                    if metadata.project:
                        projects.add(metadata.project)
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


def _list_project_files(config: CKCConfig, metadata_manager: MetadataManager, project_name: str) -> None:
    """List all files for a specific project."""
    files_found = []
    
    # Search in multiple locations
    for target in config.get_enabled_sync_targets():
        # 1. Check dedicated project directory
        project_dir = target.path / "10_Projects" / project_name
        if project_dir.exists():
            for file_path in project_dir.rglob("*.md"):
                if not file_path.name.startswith('.') and file_path.name != "README.md":
                    files_found.append(file_path)
        
        # 2. Search all files with matching project metadata
        for md_file in target.path.rglob("*.md"):
            if md_file.name != "README.md" and not md_file.name.startswith('.'):
                try:
                    metadata = metadata_manager.extract_metadata_from_file(md_file)
                    if metadata.project == project_name:
                        if md_file not in files_found:  # Avoid duplicates
                            files_found.append(md_file)
                except Exception:
                    continue
    
    # Also check .claude directory
    claude_project_dir = config.project_root / ".claude" / project_name
    if claude_project_dir.exists():
        for file_path in claude_project_dir.rglob("*.md"):
            if not file_path.name.startswith('.'):
                files_found.append(file_path)
    
    if not files_found:
        console.print(f"[yellow]No files found for project: {project_name}[/yellow]")
        console.print(f"\nTo add files to this project:")
        console.print(f"  1. Create files in .claude/{project_name}/")
        console.print(f"  2. Add 'project: {project_name}' to file frontmatter")
        console.print(f"  3. Run 'ckc sync' to synchronize")
        return
    
    console.print(f"[bold]Files in project '{project_name}':[/bold]\n")
    for file_path in sorted(files_found):
        try:
            metadata = metadata_manager.extract_metadata_from_file(file_path)
            location = "vault" if str(file_path).find("demo/shared_vault") != -1 else "source"
            console.print(f"  📄 {metadata.title} ({metadata.category or 'uncategorized'}) [{location}]")
        except Exception:
            location = "vault" if str(file_path).find("demo/shared_vault") != -1 else "source"
            console.print(f"  📄 {file_path.name} [{location}]")


def _show_project_stats(config: CKCConfig, metadata_manager: MetadataManager, project_name: str) -> None:
    """Show statistics for a specific project."""
    files_found = []
    categories = {}
    statuses = {}
    locations = {"source": 0, "vault": 0}
    
    # Search in multiple locations
    for target in config.get_enabled_sync_targets():
        # 1. Check dedicated project directory
        project_dir = target.path / "10_Projects" / project_name
        if project_dir.exists():
            for file_path in project_dir.rglob("*.md"):
                if not file_path.name.startswith('.') and file_path.name != "README.md":
                    try:
                        metadata = metadata_manager.extract_metadata_from_file(file_path)
                        files_found.append(metadata)
                        locations["vault"] += 1
                        
                        # Count categories
                        category = metadata.category or "uncategorized"
                        categories[category] = categories.get(category, 0) + 1
                        
                        # Count statuses
                        statuses[metadata.status] = statuses.get(metadata.status, 0) + 1
                        
                    except Exception:
                        continue
        
        # 2. Search all files with matching project metadata
        for md_file in target.path.rglob("*.md"):
            if md_file.name != "README.md" and not md_file.name.startswith('.'):
                try:
                    metadata = metadata_manager.extract_metadata_from_file(md_file)
                    if metadata.project == project_name:
                        # Avoid double counting files already found in project directory
                        if not any(f.title == metadata.title for f in files_found):
                            files_found.append(metadata)
                            locations["vault"] += 1
                            
                            # Count categories
                            category = metadata.category or "uncategorized"
                            categories[category] = categories.get(category, 0) + 1
                            
                            # Count statuses
                            statuses[metadata.status] = statuses.get(metadata.status, 0) + 1
                except Exception:
                    continue
    
    # Also check .claude directory
    claude_project_dir = config.project_root / ".claude" / project_name
    if claude_project_dir.exists():
        for file_path in claude_project_dir.rglob("*.md"):
            if not file_path.name.startswith('.'):
                try:
                    metadata = metadata_manager.extract_metadata_from_file(file_path)
                    files_found.append(metadata)
                    locations["source"] += 1
                    
                    # Count categories
                    category = metadata.category or "uncategorized"
                    categories[category] = categories.get(category, 0) + 1
                    
                    # Count statuses
                    statuses[metadata.status] = statuses.get(metadata.status, 0) + 1
                    
                except Exception:
                    continue
    
    if not files_found:
        console.print(f"[yellow]No files found for project: {project_name}[/yellow]")
        console.print(f"\nTo create files for this project:")
        console.print(f"  1. Create files in .claude/{project_name}/")
        console.print(f"  2. Add 'project: {project_name}' to file frontmatter")
        console.print(f"  3. Run 'ckc sync' to synchronize")
        return
    
    console.print(f"[bold]Statistics for project '{project_name}':[/bold]\n")
    console.print(f"📊 Total files: {len(files_found)}")
    
    # Location breakdown
    console.print("\n[blue]By Location:[/blue]")
    console.print(f"  Source (.claude): {locations['source']}")
    console.print(f"  Vault (synced): {locations['vault']}")
    
    # Categories breakdown
    if categories:
        console.print("\n[blue]By Category:[/blue]")
        for category, count in sorted(categories.items()):
            console.print(f"  {category}: {count}")
    
    # Status breakdown
    if statuses:
        console.print("\n[blue]By Status:[/blue]")
        for status, count in sorted(statuses.items()):
            console.print(f"  {status}: {count}")


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()