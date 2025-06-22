"""Smart sync functionality for CKC CLI."""

import glob
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

import typer
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from ..core.config import CKCConfig
from ..core.metadata import KnowledgeMetadata, MetadataManager
from ..sync.hybrid_manager import KnowledgeClassifier

console = Console()


def scan_metadata_status(directory: str = ".claude") -> tuple[list[Path], list[Path]]:
    """メタデータ状況をスキャン"""
    pattern = f"{directory}/**/*.md"
    all_files = [Path(f) for f in glob.glob(pattern, recursive=True)]

    has_metadata = []
    needs_classification = []

    for file_path in all_files:
        if has_frontmatter(file_path):
            has_metadata.append(file_path)
        else:
            needs_classification.append(file_path)

    return has_metadata, needs_classification


def has_frontmatter(file_path: Path) -> bool:
    """フロントマターの存在確認"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # YAML frontmatter pattern
        pattern = r"^---\s*\n.*?\n---\s*\n"
        return bool(re.match(pattern, content, re.DOTALL))
    except Exception:
        return False


def classify_file_intelligent(
    file_path: Path, config: CKCConfig, metadata_manager: MetadataManager
) -> dict[str, Any]:
    """インテリジェントファイル分類"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Use existing KnowledgeClassifier for consistent classification
        classifier = KnowledgeClassifier(config.hybrid_structure)

        # Create minimal metadata for classification
        minimal_metadata = KnowledgeMetadata(
            title=file_path.stem, category=None, tags=[]
        )

        # Analyze content and determine classification
        classification = analyze_content_advanced(content, file_path, classifier)

        return {"success": True, "classification": classification, "confidence": "high"}
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "classification": get_default_classification(),
        }


def analyze_content_advanced(
    content: str, file_path: Path, classifier: KnowledgeClassifier
) -> dict[str, Any]:
    """高度なコンテンツ分析"""
    filename = file_path.name.lower()
    content_lower = content.lower()
    file_path_str = str(file_path)

    # Architecture files
    if "architecture" in file_path_str or any(
        term in content for term in ["アーキテクチャ", "architecture", "system design"]
    ):
        return {
            "category": "concept",
            "subcategory": "Development_Patterns",
            "tags": ["architecture", "design", "system", "structure"],
            "complexity": "advanced",
            "quality": "high",
        }

    # Command files in commands directory
    if "commands" in file_path_str:
        if any(
            lang in content_lower for lang in ["#!/bin/bash", "bash", "shell", "git"]
        ):
            return {
                "category": "command",
                "subcategory": "slash_commands",
                "tags": ["command", "shell", "automation", "script"],
                "complexity": "intermediate",
                "quality": "medium",
            }
        elif any(lang in content_lower for lang in ["python", "uv run", "import"]):
            return {
                "category": "command",
                "subcategory": "cli_tools",
                "tags": ["command", "python", "automation", "script"],
                "complexity": "intermediate",
                "quality": "high",
            }
        elif any(
            term in content_lower
            for term in ["プロンプト", "prompt", "分類", "classification"]
        ):
            return {
                "category": "command",
                "subcategory": "automation",
                "tags": ["command", "template", "classification", "automation"],
                "complexity": "intermediate",
                "quality": "high",
            }
        else:
            return {
                "category": "command",
                "subcategory": "scripts",
                "tags": ["command", "automation", "workflow"],
                "complexity": "beginner",
                "quality": "medium",
            }

    # Debug files
    if "debug" in file_path_str or "issue" in filename:
        return {
            "category": "project_log",
            "tags": ["debug", "issue", "troubleshooting", "problem-solving"],
            "complexity": "intermediate",
            "quality": "medium",
        }

    # Documentation files
    if any(
        term in content_lower
        for term in ["documentation", "ドキュメント", "guide", "ガイド", "readme"]
    ):
        return {
            "category": "resource",
            "subcategory": "Documentation",
            "tags": ["documentation", "guide", "reference", "manual"],
            "complexity": "intermediate",
            "quality": "high",
        }

    # Concept files (comprehensive detection)
    if any(
        term in content_lower
        for term in [
            "概念",
            "concept",
            "設計",
            "design",
            "考察",
            "戦略",
            "strategy",
            "改善",
        ]
    ):
        if any(
            term in content_lower
            for term in ["ai", "claude", "llm", "machine learning", "人工知能"]
        ):
            return {
                "category": "concept",
                "subcategory": "AI_Fundamentals",
                "tags": ["concept", "ai", "claude", "fundamentals"],
                "complexity": "advanced",
                "quality": "high",
            }
        elif any(
            term in content_lower
            for term in ["best practice", "ベストプラクティス", "guideline", "standard"]
        ):
            return {
                "category": "concept",
                "subcategory": "Best_Practices",
                "tags": ["concept", "best-practices", "guidelines", "standards"],
                "complexity": "intermediate",
                "quality": "high",
            }
        else:
            return {
                "category": "concept",
                "subcategory": "Development_Patterns",
                "tags": ["concept", "development", "patterns", "theory"],
                "complexity": "intermediate",
                "quality": "high",
            }

    # Roadmap and planning files
    if any(
        term in content_lower
        for term in ["roadmap", "ロードマップ", "planning", "計画", "feature"]
    ):
        return {
            "category": "resource",
            "subcategory": "Documentation",
            "tags": ["roadmap", "planning", "features", "development"],
            "complexity": "intermediate",
            "quality": "high",
        }

    # Default classification
    return get_default_classification()


def get_default_classification() -> dict[str, Any]:
    """デフォルト分類"""
    return {
        "category": "concept",
        "subcategory": "Development_Patterns",
        "tags": ["misc", "unclassified"],
        "complexity": "intermediate",
        "quality": "medium",
    }


def generate_frontmatter(file_path: Path, classification: dict[str, Any]) -> str:
    """フロントマター生成"""
    filename = file_path.stem
    title = filename.replace("_", " ").replace("-", " ").title()

    today = datetime.now().strftime("%Y-%m-%d")

    frontmatter_data = {
        "title": title,
        "created": today,
        "updated": today,
        "version": "1.0",
        "category": classification["category"],
        "tags": classification["tags"],
        "complexity": classification["complexity"],
        "quality": classification["quality"],
        "purpose": f"Auto-generated metadata for {filename}",
        "project": "claude-knowledge-catalyst",
        "status": "draft",
    }

    # Add subcategory if present
    if "subcategory" in classification:
        frontmatter_data["subcategory"] = classification["subcategory"]

    # Generate YAML frontmatter
    yaml_content = yaml.dump(
        frontmatter_data, default_flow_style=False, allow_unicode=True
    )
    return f"---\n{yaml_content}---\n\n"


def apply_metadata_to_file(
    file_path: Path, classification: dict[str, Any], backup: bool = True
) -> dict[str, Any]:
    """ファイルにメタデータを適用"""
    try:
        # Create backup
        backup_path = None
        if backup:
            backup_path = Path(f"{file_path}.backup")
            shutil.copy2(file_path, backup_path)

        # Read original content
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Generate frontmatter
        frontmatter_content = generate_frontmatter(file_path, classification)

        # Write updated content
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{frontmatter_content}{content}")

        return {"success": True, "backup_path": backup_path}

    except Exception as e:
        return {"success": False, "error": str(e)}


def run_ckc_sync() -> dict[str, Any]:
    """CKC同期実行"""
    try:
        result = subprocess.run(
            ["uv", "run", "ckc", "sync"], capture_output=True, text=True, check=True
        )
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr}


def smart_sync_command(
    auto_apply: bool = False,
    dry_run: bool = False,
    directory: str = ".claude",
    backup: bool = True,
    config: CKCConfig = None,
    metadata_manager: MetadataManager = None,
    min_confidence: float = 0.7,
) -> None:
    """Smart sync main logic"""

    console.print(
        "[bold blue]🚀 CKC Smart Sync[/bold blue] - Intelligent Batch Classification"
    )
    console.print("=" * 60)

    # Phase 1: Scan metadata status
    console.print("\n[bold yellow]📊 Phase 1:[/bold yellow] メタデータ状況スキャン")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning files...", total=None)
        has_metadata, needs_classification = scan_metadata_status(directory)
        progress.update(task, completed=True)

    # Create status table
    table = Table(title="Metadata Status")
    table.add_column("Status", style="cyan")
    table.add_column("Count", justify="right", style="magenta")
    table.add_column("Files", style="green")

    table.add_row(
        "✅ Has Metadata", str(len(has_metadata)), f"{len(has_metadata)} files"
    )
    table.add_row(
        "⚠️ Needs Classification",
        str(len(needs_classification)),
        f"{len(needs_classification)} files",
    )

    console.print(table)

    if not needs_classification:
        console.print(
            "\n[green]🎉 All files already classified![/green] Running sync only..."
        )

        if not dry_run:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Running CKC sync...", total=None)
                sync_result = run_ckc_sync()
                progress.update(task, completed=True)

            if sync_result["success"]:
                console.print("[green]✅ Sync completed successfully[/green]")
            else:
                console.print(f"[red]❌ Sync error:[/red] {sync_result['error']}")
        else:
            console.print("[yellow]🔍 Dry run: Would run CKC sync[/yellow]")
        return

    # Phase 2: Batch classification
    console.print(
        f"\n[bold yellow]🤖 Phase 2:[/bold yellow] Batch Classification ({len(needs_classification)} files)"
    )

    successful_classifications = []
    failed_classifications = []

    with Progress(console=console) as progress:
        task = progress.add_task(
            "Classifying files...", total=len(needs_classification)
        )

        for file_path in needs_classification:
            console.print(f"  📋 Analyzing: [cyan]{file_path.name}[/cyan]")

            result = classify_file_intelligent(file_path, config, metadata_manager)
            if result["success"]:
                successful_classifications.append((file_path, result["classification"]))
                console.print(
                    f"    ✅ Category: [green]{result['classification']['category']}[/green]"
                )
            else:
                failed_classifications.append((file_path, result["error"]))
                console.print(f"    ❌ Error: [red]{result['error']}[/red]")

            progress.advance(task)

    # Phase 3: Apply metadata
    if successful_classifications and not dry_run:
        console.print(
            f"\n[bold yellow]📝 Phase 3:[/bold yellow] Metadata Application ({len(successful_classifications)} files)"
        )

        applied_files = []

        for file_path, classification in successful_classifications:
            if not auto_apply:
                # Show preview
                preview_table = Table(title=f"Metadata Preview: {file_path.name}")
                preview_table.add_column("Field", style="cyan")
                preview_table.add_column("Value", style="magenta")

                for key, value in classification.items():
                    preview_table.add_row(key, str(value))

                console.print(preview_table)

                apply_choice = typer.confirm(f"Apply metadata to {file_path.name}?")
                if not apply_choice:
                    continue

            result = apply_metadata_to_file(file_path, classification, backup)
            if result["success"]:
                applied_files.append(file_path)
                console.print(f"  ✅ Applied: [green]{file_path.name}[/green]")
            else:
                console.print(
                    f"  ❌ Failed: [red]{file_path.name}[/red] - {result['error']}"
                )

    elif dry_run:
        console.print(
            f"\n[yellow]🔍 Dry run: Would apply metadata to {len(successful_classifications)} files[/yellow]"
        )
        applied_files = []
    else:
        applied_files = []

    # Phase 4: CKC sync
    if not dry_run:
        console.print("\n[bold yellow]🔄 Phase 4:[/bold yellow] CKC Synchronization")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running CKC sync...", total=None)
            sync_result = run_ckc_sync()
            progress.update(task, completed=True)

        if sync_result["success"]:
            console.print("[green]✅ Sync completed successfully[/green]")
        else:
            console.print(f"[red]❌ Sync error:[/red] {sync_result['error']}")
    else:
        console.print("\n[yellow]🔍 Dry run: Would run CKC sync[/yellow]")
        sync_result = {"success": True}

    # Phase 5: Summary
    console.print("\n[bold yellow]📊 Phase 5:[/bold yellow] Summary")
    console.print("=" * 60)

    summary_table = Table(title="Processing Results")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Count", justify="right", style="magenta")
    summary_table.add_column("Status", style="green")

    summary_table.add_row("📁 Target Files", str(len(needs_classification)), "Scanned")
    summary_table.add_row(
        "✅ Classification Success", str(len(successful_classifications)), "Completed"
    )
    summary_table.add_row(
        "❌ Classification Failed", str(len(failed_classifications)), "Manual Required"
    )

    if not dry_run:
        summary_table.add_row(
            "📝 Metadata Applied",
            str(len(applied_files) if "applied_files" in locals() else 0),
            "Completed",
        )
        summary_table.add_row(
            "🔄 Sync Status",
            "1" if sync_result["success"] else "0",
            "Success" if sync_result["success"] else "Failed",
        )
    else:
        summary_table.add_row("📝 Metadata Applied", "0", "Dry Run")
        summary_table.add_row("🔄 Sync Status", "0", "Dry Run")

    console.print(summary_table)

    if failed_classifications:
        console.print(
            f"\n[red]⚠️ Manual attention required for {len(failed_classifications)} files:[/red]"
        )
        for file_path, error in failed_classifications:
            console.print(f"  - [yellow]{file_path}[/yellow]: {error}")

    if not dry_run and len(applied_files) > 0:
        console.print(
            f"\n[green]🎉 Successfully processed {len(applied_files)} files![/green]"
        )
    elif dry_run:
        console.print(
            f"\n[yellow]🔍 Dry run completed. {len(successful_classifications)} files ready for processing.[/yellow]"
        )


# === Tag-Centered Approach Implementation ===


class TagCenteredSmartSync:
    """Enhanced Smart Sync with tag-centered approach and minimal directory structure."""

    def __init__(self, config: CKCConfig | None = None):
        """Initialize tag-centered smart sync manager."""
        self.config = config or CKCConfig()
        self.metadata_manager = MetadataManager()
        self.console = Console()

        # Minimal directory structure as defined in the analysis document
        self.minimal_structure = {
            "_system": "システムファイル（テンプレート、設定）",
            "_attachments": "添付ファイル",
            "inbox": "未整理・一時的なファイル",
            "active": "アクティブに使用中のファイル",
            "archive": "非推奨・古いファイル",
            "knowledge": "主要な知識ファイル（90%のコンテンツ）",
        }

    def migrate_to_tag_centered_structure(
        self, source_path: Path, target_path: Path, dry_run: bool = False
    ) -> dict[str, Any]:
        """Migrate existing directory structure to tag-centered approach."""

        migration_stats = {
            "files_processed": 0,
            "files_migrated": 0,
            "metadata_enhanced": 0,
            "errors": [],
            "directory_changes": [],
        }

        self.console.print(
            Panel(
                f"🔄 Tag-Centered Migration\n"
                f"From: {source_path}\n"
                f"To: {target_path}\n"
                f"Dry Run: {dry_run}",
                title="Smart Sync Migration",
            )
        )

        try:
            # Create minimal directory structure
            if not dry_run:
                self._create_minimal_structure(target_path)
                migration_stats["directory_changes"].append(
                    "Created minimal directory structure"
                )

            # Scan and categorize files
            file_categorization = self._categorize_files_by_metadata(source_path)

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
            ) as progress:
                migration_task = progress.add_task(
                    "Migrating files...", total=len(file_categorization)
                )

                for file_info in file_categorization:
                    try:
                        self._migrate_single_file(
                            file_info, source_path, target_path, dry_run
                        )
                        migration_stats["files_migrated"] += 1

                        if file_info.get("metadata_enhanced"):
                            migration_stats["metadata_enhanced"] += 1

                    except Exception as e:
                        migration_stats["errors"].append(
                            f"Error migrating {file_info['path']}: {e}"
                        )

                    migration_stats["files_processed"] += 1
                    progress.advance(migration_task)

            # Generate migration report
            self._generate_migration_report(migration_stats, target_path, dry_run)

        except Exception as e:
            migration_stats["errors"].append(f"Migration failed: {e}")
            self.console.print(f"[red]Migration failed: {e}[/red]")

        return migration_stats

    def _create_minimal_structure(self, target_path: Path) -> None:
        """Create the minimal directory structure."""
        for dir_name, description in self.minimal_structure.items():
            dir_path = target_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)

            # Create README with description
            readme_path = dir_path / "README.md"
            if not readme_path.exists():
                readme_content = f"# {dir_name}\n\n{description}\n\n"

                if dir_name == "knowledge":
                    readme_content += self._get_knowledge_readme_content()

                readme_path.write_text(readme_content, encoding="utf-8")

    def _get_knowledge_readme_content(self) -> str:
        """Get enhanced README content for knowledge directory."""
        return """## タグ体系とクエリ例

このディレクトリでは、ディレクトリ構造ではなくタグベースの分類を使用します。

### 基本タグ構造

```yaml
# 基本分類（必須）
type: prompt                    # prompt, code, concept, resource
status: production              # draft, tested, production, deprecated

# 技術領域（複数選択可）
tech: [python, javascript, api]
domain: [web-dev, data-science, automation]

# 品質指標
success_rate: 85
complexity: intermediate        # beginner, intermediate, advanced
confidence: high               # low, medium, high

# プロジェクト関連
projects: [project-a, project-b]
team: [backend, frontend, devops]

# Claude特化
claude_model: [opus, sonnet]
claude_feature: [code-generation, analysis]

# 自由形式タグ
tags: [automation, best-practice, team-process]
```

### 動的クエリ例

```
# 高成功率のAPI関連プロンプトを動的抽出
TABLE success_rate, domains, updated 
FROM #prompt AND #api-design AND #best-practice 
WHERE success_rate > 80 
SORT success_rate DESC

# プロジェクト横断でのコード関連知見
LIST FROM (#code OR #prompt) AND #python 
WHERE contains(string(tags), "automation")
```

### ファイル命名規則

ファイル名は内容を表現し、分類はメタデータで管理します：
- `api-design-review-prompt.md`
- `python-async-best-practices.md`
- `claude-code-generation-techniques.md`
"""

    def _categorize_files_by_metadata(self, source_path: Path) -> list[dict[str, Any]]:
        """Categorize files based on their metadata and content."""
        file_categorization = []

        for file_path in source_path.rglob("*.md"):
            if file_path.is_file():
                try:
                    # Extract metadata
                    metadata = self.metadata_manager.extract_metadata_from_file(
                        file_path
                    )

                    # Determine target directory based on metadata
                    target_dir = self._determine_target_directory(metadata, file_path)

                    # Check if metadata needs enhancement
                    suggestions = self.metadata_manager.suggest_tag_enhancements(
                        file_path.read_text(encoding="utf-8"), metadata.model_dump()
                    )

                    file_categorization.append(
                        {
                            "path": file_path,
                            "relative_path": file_path.relative_to(source_path),
                            "metadata": metadata,
                            "target_directory": target_dir,
                            "suggestions": suggestions,
                            "metadata_enhanced": any(suggestions.values()),
                        }
                    )

                except Exception as e:
                    self.console.print(
                        f"[yellow]Warning: Could not process {file_path}: {e}[/yellow]"
                    )

        return file_categorization

    def _determine_target_directory(
        self, metadata: KnowledgeMetadata, file_path: Path
    ) -> str:
        """Determine target directory based on metadata and file characteristics."""
        # State-based classification as described in the document

        status = getattr(metadata, "status", "draft")

        # System files
        if "_" in str(file_path) and any(
            sys_dir in str(file_path)
            for sys_dir in ["_templates", "_attachments", "_scripts"]
        ):
            return "_system"

        # Archive for deprecated content
        if status == "deprecated":
            return "archive"

        # Active for current projects
        if status in ["draft", "tested"] and any(
            str(file_path).startswith(active_dir)
            for active_dir in ["active", "current", "wip"]
        ):
            return "active"

        # Inbox for unprocessed files
        if status == "draft" and not getattr(metadata, "type", None):
            return "inbox"

        # Knowledge for mature content (default for most files)
        return "knowledge"

    def _migrate_single_file(
        self,
        file_info: dict[str, Any],
        source_path: Path,
        target_path: Path,
        dry_run: bool,
    ) -> None:
        """Migrate a single file to the new structure."""
        source_file = file_info["path"]
        target_dir = target_path / file_info["target_directory"]
        target_file = target_dir / source_file.name

        # Handle naming conflicts
        if target_file.exists():
            base_name = target_file.stem
            suffix = target_file.suffix
            counter = 1
            while target_file.exists():
                target_file = target_dir / f"{base_name}_{counter}{suffix}"
                counter += 1

        if not dry_run:
            # Copy file
            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, target_file)

            # Enhance metadata if suggestions available
            if file_info["metadata_enhanced"]:
                self._apply_metadata_suggestions(target_file, file_info)

    def _apply_metadata_suggestions(
        self, file_path: Path, file_info: dict[str, Any]
    ) -> None:
        """Apply metadata enhancement suggestions to a file."""
        try:
            # Read current metadata
            current_metadata = self.metadata_manager.extract_metadata_from_file(
                file_path
            )
            metadata_dict = current_metadata.model_dump()

            # Apply suggestions
            suggestions = file_info["suggestions"]
            for field, suggested_values in suggestions.items():
                if suggested_values:  # Only apply if there are suggestions
                    current_values = metadata_dict.get(field, [])
                    if isinstance(current_values, list):
                        # Merge with existing values
                        metadata_dict[field] = list(
                            set(current_values + suggested_values)
                        )
                    else:
                        # For non-list fields, take the first suggestion if current is empty
                        if not current_values and suggested_values:
                            metadata_dict[field] = suggested_values[0]

            # Create updated metadata object
            updated_metadata = KnowledgeMetadata(**metadata_dict)

            # Update the file
            self.metadata_manager.update_file_metadata(file_path, updated_metadata)

        except Exception as e:
            self.console.print(
                f"[yellow]Warning: Could not enhance metadata for {file_path}: {e}[/yellow]"
            )

    def _generate_migration_report(
        self, stats: dict[str, Any], target_path: Path, dry_run: bool
    ) -> None:
        """Generate a migration report."""
        report_content = f"""# Tag-Centered Migration Report

## Summary
- Files Processed: {stats["files_processed"]}
- Files Migrated: {stats["files_migrated"]}
- Metadata Enhanced: {stats["metadata_enhanced"]}
- Errors: {len(stats["errors"])}

## Directory Structure Created
{chr(10).join(f"- {dir_name}: {desc}" for dir_name, desc in self.minimal_structure.items())}

## Migration Details
{chr(10).join(f"- {change}" for change in stats["directory_changes"])}

## Errors
{chr(10).join(f"- {error}" for error in stats["errors"]) if stats["errors"] else "No errors occurred."}

Generated: {datetime.now().isoformat()}
Dry Run: {dry_run}
"""

        # Save report
        report_path = target_path / "migration_report.md"
        if not dry_run:
            report_path.write_text(report_content, encoding="utf-8")

        # Display summary
        self.console.print(
            Panel(
                f"✅ Migration {'simulated' if dry_run else 'completed'}\n"
                f"📁 Files processed: {stats['files_processed']}\n"
                f"🔄 Files migrated: {stats['files_migrated']}\n"
                f"⚡ Metadata enhanced: {stats['metadata_enhanced']}\n"
                f"❌ Errors: {len(stats['errors'])}",
                title="Migration Complete",
            )
        )

    def create_obsidian_templates(self, target_path: Path) -> None:
        """Create Obsidian templates for the enhanced tag system."""
        templates_dir = target_path / "_system" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)

        # Enhanced prompt template
        prompt_template = """---
title: "{{title}}"
created: {{date:YYYY-MM-DD}}
updated: {{date:YYYY-MM-DD}}

# 基本分類（必須）
type: prompt
status: draft

# 技術領域（複数選択可）
tech: []
domain: []

# 品質指標
success_rate: 
complexity: intermediate
confidence: medium

# プロジェクト関連
projects: []
team: []

# Claude特化
claude_model: []
claude_feature: []

# 自由形式タグ（進化的）
tags: []
---

# {{title}}

## 概要


## プロンプト

```
Your prompt here...
```

## 使用例


## 成功パターン


## 改善ポイント

"""

        # Enhanced code template
        code_template = """---
title: "{{title}}"
created: {{date:YYYY-MM-DD}}
updated: {{date:YYYY-MM-DD}}

# 基本分類（必須）
type: code
status: draft

# 技術領域（複数選択可）
tech: []
domain: []

# 品質指標
complexity: intermediate
confidence: medium

# プロジェクト関連
projects: []
team: []

# 自由形式タグ（進化的）
tags: []
---

# {{title}}

## 概要


## コード

```python
# Your code here...
```

## 使用方法


## 依存関係


## テスト

"""

        # Save templates
        (templates_dir / "enhanced_prompt_template.md").write_text(
            prompt_template, encoding="utf-8"
        )
        (templates_dir / "enhanced_code_template.md").write_text(
            code_template, encoding="utf-8"
        )

        self.console.print("[green]✅ Obsidianテンプレートを作成しました[/green]")


def migrate_to_tag_centered_cli(
    source: str = ".", target: str = "./tag_centered_vault", dry_run: bool = False
) -> dict[str, Any]:
    """CLI function to migrate to tag-centered structure."""

    source_path = Path(source).resolve()
    target_path = Path(target).resolve()

    sync_manager = TagCenteredSmartSync()

    # Perform migration
    result = sync_manager.migrate_to_tag_centered_structure(
        source_path, target_path, dry_run
    )

    # Create Obsidian templates
    if not dry_run:
        sync_manager.create_obsidian_templates(target_path)

    return result
