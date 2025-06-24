"""Main CLI interface for Claude Knowledge Catalyst."""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from ..ai.ai_assistant import create_ai_assistant
from ..analytics.knowledge_analytics import generate_analytics_report
from ..analytics.usage_statistics import create_usage_collector
from ..automation.structure_automation import run_automated_maintenance
from ..core.config import CKCConfig, SyncTarget, load_config
from ..core.metadata import MetadataManager
from ..core.watcher import KnowledgeWatcher
from ..sync.compatibility import BackwardCompatibilityManager

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
@click.option(
    "--structure",
    type=click.Choice(["legacy", "hybrid"]),
    default="hybrid",
    help="Structure type to initialize",
)
@click.pass_context
def init(ctx: click.Context, structure: str) -> None:
    """Initialize CKC in the current directory."""
    config: CKCConfig = ctx.obj["config"]

    console.print("[blue]Initializing Claude Knowledge Catalyst...[/blue]")

    # Set project root to current directory
    config.project_root = Path.cwd()

    # Configure hybrid structure if requested
    if structure == "hybrid":
        config.hybrid_structure.enabled = True
        config.hybrid_structure.numbering_system = "ten_step"
        config.hybrid_structure.auto_classification = True
        console.print(
            "[green]✓[/green] Hybrid structure enabled with 10-step numbering"
        )
    else:
        config.hybrid_structure.enabled = False
        console.print("[blue]ℹ[/blue] Legacy structure mode")

    # Create .claude directory if it doesn't exist
    claude_dir = Path.cwd() / ".claude"
    claude_dir.mkdir(exist_ok=True)

    # Create default config file
    config_path = Path.cwd() / "ckc_config.yaml"
    config.save_to_file(config_path)

    console.print(f"[green]✓[/green] Created configuration file: {config_path}")
    console.print(f"[green]✓[/green] Created .claude directory: {claude_dir}")

    # Show structure-specific next steps
    console.print("\n[yellow]Next steps:[/yellow]")
    console.print("1. Configure sync targets with: [bold]ckc sync add[/bold]")

    if structure == "hybrid":
        console.print(
            "2. Configure structure with: [bold]ckc structure configure[/bold]"
        )
        console.print("3. Initialize vault structure: [bold]ckc structure init[/bold]")
        console.print("4. Start watching for changes with: [bold]ckc watch[/bold]")
    else:
        console.print("2. Start watching for changes with: [bold]ckc watch[/bold]")
        console.print(
            "3. Consider upgrading to hybrid: [bold]ckc migrate --to hybrid[/bold]"
        )

    console.print("4. Sync existing files with: [bold]ckc sync run[/bold]")


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

        # Use appropriate manager based on configuration
        compat_manager = BackwardCompatibilityManager(path, config)
        vault_manager = compat_manager.get_appropriate_manager(metadata_manager)

        if hasattr(vault_manager, "initialize"):
            success = vault_manager.initialize()
        else:
            success = vault_manager.initialize_vault()

        if success:
            console.print(f"[green]✓[/green] Initialized Obsidian vault at {path}")

            # Ensure compatibility
            compat_success = compat_manager.ensure_compatibility()
            if not compat_success:
                console.print("[yellow]![/yellow] Some compatibility issues detected")
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
                # Use appropriate manager based on configuration
                compat_manager = BackwardCompatibilityManager(sync_target.path, config)
                vault_manager = compat_manager.get_appropriate_manager(metadata_manager)

                if hasattr(vault_manager, "sync_claude_directory"):
                    results = vault_manager.sync_claude_directory(claude_dir, project)
                else:
                    # Use directory sync method
                    results = vault_manager.sync_directory(claude_dir, project)

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
                    # Use appropriate manager based on configuration
                    compat_manager = BackwardCompatibilityManager(
                        sync_target.path, config
                    )
                    vault_manager = compat_manager.get_appropriate_manager(
                        metadata_manager
                    )

                    project_name = config.project_name or None
                    vault_manager.sync_file(file_path, project_name)
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
            projects = ", ".join(metadata.related_projects)
            console.print(f"\n[blue]Related Projects:[/blue] {projects}")

        # Purpose
        if metadata.purpose:
            console.print(f"\n[blue]Purpose:[/blue] {metadata.purpose}")

    except Exception as e:
        console.print(f"[red]Error analyzing file: {e}[/red]")


@cli.group()
def analytics() -> None:
    """Analytics and reporting commands."""
    pass


@analytics.command("report")
@click.option("--days", default=30, help="Number of days to analyze")
@click.option("--output", type=click.Path(path_type=Path), help="Output file path")
@click.pass_context
def analytics_report(ctx: click.Context, days: int, output: Path | None) -> None:
    """Generate comprehensive analytics report."""
    config: CKCConfig = ctx.obj["config"]

    console.print(f"[blue]Generating analytics report for last {days} days...[/blue]")

    # Find first enabled Obsidian target for vault analysis
    vault_path = None
    for target in config.sync_targets:
        if target.enabled and target.type == "obsidian":
            vault_path = target.path
            break

    if not vault_path:
        console.print("[red]No enabled Obsidian sync target found[/red]")
        return

    try:
        # Generate knowledge analytics report
        knowledge_report = generate_analytics_report(vault_path, config)

        # Generate usage statistics
        usage_collector = create_usage_collector(vault_path, config)
        usage_report = usage_collector.generate_usage_report(days)

        # Display summary
        console.print("[green]✓[/green] Analytics report generated")
        console.print(
            f"[blue]Total files analyzed:[/blue] "
            f"{knowledge_report['report_sections']['overview']['total_files']}"
        )
        console.print(
            f"[blue]Total operations:[/blue] "
            f"{usage_report['operation_statistics']['total_operations']}"
        )

        # Show top recommendations
        recommendations = knowledge_report["report_sections"].get("recommendations", [])
        if recommendations:
            console.print("\n[yellow]Top Recommendations:[/yellow]")
            for i, rec in enumerate(recommendations[:3], 1):
                console.print(f"{i}. [{rec['priority'].upper()}] {rec['title']}")

        # Save to file if requested
        if output:
            combined_report = {
                "knowledge_analytics": knowledge_report,
                "usage_statistics": usage_report,
                "generated_at": knowledge_report["timestamp"],
            }

            import json

            with open(output, "w", encoding="utf-8") as f:
                json.dump(combined_report, f, indent=2, ensure_ascii=False, default=str)

            console.print(f"[green]✓[/green] Report saved to: {output}")

    except Exception as e:
        console.print(f"[red]Error generating analytics report: {e}[/red]")


@analytics.command("usage")
@click.option("--days", default=7, help="Number of days to analyze")
@click.pass_context
def analytics_usage(ctx: click.Context, days: int) -> None:
    """Show usage statistics."""
    config: CKCConfig = ctx.obj["config"]

    # Find vault path
    vault_path = None
    for target in config.sync_targets:
        if target.enabled and target.type == "obsidian":
            vault_path = target.path
            break

    if not vault_path:
        console.print("[red]No enabled Obsidian sync target found[/red]")
        return

    try:
        usage_collector = create_usage_collector(vault_path, config)
        report = usage_collector.generate_usage_report(days)

        console.print(f"[bold]Usage Statistics (Last {days} days)[/bold]\n")

        # Operation statistics
        ops = report["operation_statistics"]
        console.print(f"[blue]Operations:[/blue] {ops['total_operations']}")

        if ops["operation_types"]:
            console.print("[blue]Most common operations:[/blue]")
            for op_type, count in sorted(
                ops["operation_types"].items(), key=lambda x: x[1], reverse=True
            )[:5]:
                console.print(f"  • {op_type}: {count}")

        # Productivity metrics
        if "user_behavior" in report:
            productivity = report["user_behavior"].get("productivity_metrics", {})
            if productivity:
                score = productivity.get("productivity_score", 0)
                console.print(f"\n[blue]Productivity Score:[/blue] {score:.1f}/100")
                console.print(
                    f"[blue]Activities per hour:[/blue] "
                    f"{productivity.get('activities_per_hour', 0):.1f}"
                )

    except Exception as e:
        console.print(f"[red]Error generating usage statistics: {e}[/red]")


@cli.group()
def ai() -> None:
    """AI assistance commands."""
    pass


@ai.command("suggest")
@click.argument("file_path", type=click.Path(exists=True, path_type=Path))
@click.pass_context
def ai_suggest(ctx: click.Context, file_path: Path) -> None:
    """Get AI suggestions for improving content."""
    config: CKCConfig = ctx.obj["config"]

    try:
        ai_assistant = create_ai_assistant(Path.cwd(), config)
        suggestions = ai_assistant.suggest_content_improvements(file_path)

        console.print(f"[bold]AI Suggestions for: {file_path}[/bold]\n")

        if "suggestions" in suggestions:
            for i, suggestion in enumerate(suggestions["suggestions"], 1):
                priority_color = {"high": "red", "medium": "yellow", "low": "blue"}.get(
                    suggestion["priority"], "white"
                )

                console.print(
                    f"{i}. [{priority_color}]{suggestion['priority'].upper()}"
                    f"[/{priority_color}] {suggestion['suggestion']}"
                )
                console.print(f"   [dim]→ {suggestion['action']}[/dim]\n")
        else:
            console.print(
                "[green]No specific suggestions found - content looks good![/green]"
            )

    except Exception as e:
        console.print(f"[red]Error getting AI suggestions: {e}[/red]")


@ai.command("template")
@click.argument(
    "content_type",
    type=click.Choice(
        ["prompt", "code", "concept", "project_log", "experiment", "resource"]
    ),
)
@click.option("--title", help="Template title")
@click.option("--output", type=click.Path(path_type=Path), help="Output file path")
@click.pass_context
def ai_template(
    ctx: click.Context, content_type: str, title: str | None, output: Path | None
) -> None:
    """Generate intelligent content template."""
    config: CKCConfig = ctx.obj["config"]

    try:
        ai_assistant = create_ai_assistant(Path.cwd(), config)

        context = {}
        if title:
            context["title"] = title

        template_content = ai_assistant.generate_content_template(content_type, context)

        if output:
            output.write_text(template_content, encoding="utf-8")
            console.print(f"[green]✓[/green] Template saved to: {output}")
        else:
            console.print(f"[bold]{content_type.title()} Template:[/bold]\n")
            console.print(template_content)

    except Exception as e:
        console.print(f"[red]Error generating template: {e}[/red]")


@ai.command("insights")
@click.argument("file_path", type=click.Path(exists=True, path_type=Path))
@click.pass_context
def ai_insights(ctx: click.Context, file_path: Path) -> None:
    """Get AI-powered insights about content."""
    config: CKCConfig = ctx.obj["config"]

    try:
        ai_assistant = create_ai_assistant(Path.cwd(), config)
        insights = ai_assistant.provide_content_insights(file_path)

        console.print(f"[bold]AI Insights for: {file_path}[/bold]\n")

        # Content analysis
        if "content_analysis" in insights:
            analysis = insights["content_analysis"]
            console.print("[blue]Content Analysis:[/blue]")
            for metric, value in analysis.items():
                if isinstance(value, float):
                    console.print(f"  • {metric}: {value:.2f}")
                else:
                    console.print(f"  • {metric}: {value}")
            console.print()

        # Knowledge connections
        if "knowledge_connections" in insights:
            connections = insights["knowledge_connections"]
            console.print("[blue]Knowledge Connections:[/blue]")
            for metric, value in connections.items():
                console.print(f"  • {metric}: {value}")
            console.print()

        # Usage predictions
        if "usage_predictions" in insights:
            predictions = insights["usage_predictions"]
            console.print("[blue]Usage Predictions:[/blue]")
            for metric, value in predictions.items():
                console.print(f"  • {metric}: {value}")

    except Exception as e:
        console.print(f"[red]Error getting AI insights: {e}[/red]")


@cli.command("maintenance")
@click.option("--force", is_flag=True, help="Force maintenance even if recently run")
@click.pass_context
def maintenance(ctx: click.Context, force: bool) -> None:
    """Run automated maintenance tasks."""
    config: CKCConfig = ctx.obj["config"]

    # Find vault path
    vault_path = None
    for target in config.sync_targets:
        if target.enabled and target.type == "obsidian":
            vault_path = target.path
            break

    if not vault_path:
        console.print("[red]No enabled Obsidian sync target found[/red]")
        return

    try:
        console.print("[blue]Running automated maintenance...[/blue]")

        result = run_automated_maintenance(vault_path, config)

        if result.get("status") == "failed":
            console.print(f"[red]Maintenance failed: {result.get('error')}[/red]")
            return

        # Show results
        tasks = result.get("tasks_completed", [])
        console.print(f"[green]✓[/green] Completed {len(tasks)} maintenance tasks")

        for task in tasks:
            console.print(f"  • {task}")

        # Show issues found/fixed
        issues_found = len(result.get("issues_found", []))
        issues_fixed = len(result.get("issues_fixed", []))

        if issues_found > 0:
            console.print(f"\n[yellow]Issues found:[/yellow] {issues_found}")
            console.print(f"[green]Issues fixed:[/green] {issues_fixed}")

        # Show warnings
        warnings = result.get("warnings", [])
        if warnings:
            console.print("\n[yellow]Warnings:[/yellow]")
            for warning in warnings[:5]:  # Show first 5 warnings
                console.print(f"  • {warning}")

        # Show performance
        performance = result.get("performance", {})
        if performance:
            duration = performance.get("duration_seconds", 0)
            console.print(
                f"\n[blue]Maintenance completed in {duration:.1f} seconds[/blue]"
            )

    except Exception as e:
        console.print(f"[red]Error running maintenance: {e}[/red]")


def main() -> None:
    """Main entry point for the CLI."""
    cli()
