"""Smart sync functionality for CKC CLI."""

import glob
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict, Any
import subprocess

import typer
import yaml
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..core.config import CKCConfig
from ..core.metadata import MetadataManager, KnowledgeMetadata
from ..sync.hybrid_manager import KnowledgeClassifier

console = Console()

def scan_metadata_status(directory: str = ".claude") -> Tuple[List[Path], List[Path]]:
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
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # YAML frontmatter pattern
        pattern = r'^---\s*\n.*?\n---\s*\n'
        return bool(re.match(pattern, content, re.DOTALL))
    except Exception:
        return False

def classify_file_intelligent(file_path: Path, config: CKCConfig, metadata_manager: MetadataManager) -> Dict[str, Any]:
    """インテリジェントファイル分類"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Use existing KnowledgeClassifier for consistent classification
        classifier = KnowledgeClassifier(config.hybrid_structure)
        
        # Create minimal metadata for classification
        minimal_metadata = KnowledgeMetadata(
            title=file_path.stem,
            category=None,
            tags=[]
        )
        
        # Analyze content and determine classification
        classification = analyze_content_advanced(content, file_path, classifier)
        
        return {
            'success': True,
            'classification': classification,
            'confidence': 'high'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'classification': get_default_classification()
        }

def analyze_content_advanced(content: str, file_path: Path, classifier: KnowledgeClassifier) -> Dict[str, Any]:
    """高度なコンテンツ分析"""
    filename = file_path.name.lower()
    content_lower = content.lower()
    file_path_str = str(file_path)
    
    # Architecture files
    if 'architecture' in file_path_str or any(term in content for term in ['アーキテクチャ', 'architecture', 'system design']):
        return {
            'category': 'concept',
            'subcategory': 'Development_Patterns',
            'tags': ['architecture', 'design', 'system', 'structure'],
            'complexity': 'advanced',
            'quality': 'high'
        }
    
    # Command files in commands directory
    if 'commands' in file_path_str:
        if any(lang in content_lower for lang in ['#!/bin/bash', 'bash', 'shell', 'git']):
            return {
                'category': 'command',
                'subcategory': 'slash_commands',
                'tags': ['command', 'shell', 'automation', 'script'],
                'complexity': 'intermediate',
                'quality': 'medium'
            }
        elif any(lang in content_lower for lang in ['python', 'uv run', 'import']):
            return {
                'category': 'command',
                'subcategory': 'cli_tools',
                'tags': ['command', 'python', 'automation', 'script'],
                'complexity': 'intermediate',
                'quality': 'high'
            }
        elif any(term in content_lower for term in ['プロンプト', 'prompt', '分類', 'classification']):
            return {
                'category': 'command',
                'subcategory': 'automation',
                'tags': ['command', 'template', 'classification', 'automation'],
                'complexity': 'intermediate',
                'quality': 'high'
            }
        else:
            return {
                'category': 'command',
                'subcategory': 'scripts',
                'tags': ['command', 'automation', 'workflow'],
                'complexity': 'beginner',
                'quality': 'medium'
            }
    
    # Debug files
    if 'debug' in file_path_str or 'issue' in filename:
        return {
            'category': 'project_log',
            'tags': ['debug', 'issue', 'troubleshooting', 'problem-solving'],
            'complexity': 'intermediate',
            'quality': 'medium'
        }
    
    # Documentation files
    if any(term in content_lower for term in ['documentation', 'ドキュメント', 'guide', 'ガイド', 'readme']):
        return {
            'category': 'resource',
            'subcategory': 'Documentation',
            'tags': ['documentation', 'guide', 'reference', 'manual'],
            'complexity': 'intermediate',
            'quality': 'high'
        }
    
    # Concept files (comprehensive detection)
    if any(term in content_lower for term in ['概念', 'concept', '設計', 'design', '考察', '戦略', 'strategy', '改善']):
        if any(term in content_lower for term in ['ai', 'claude', 'llm', 'machine learning', '人工知能']):
            return {
                'category': 'concept',
                'subcategory': 'AI_Fundamentals',
                'tags': ['concept', 'ai', 'claude', 'fundamentals'],
                'complexity': 'advanced',
                'quality': 'high'
            }
        elif any(term in content_lower for term in ['best practice', 'ベストプラクティス', 'guideline', 'standard']):
            return {
                'category': 'concept',
                'subcategory': 'Best_Practices',
                'tags': ['concept', 'best-practices', 'guidelines', 'standards'],
                'complexity': 'intermediate',
                'quality': 'high'
            }
        else:
            return {
                'category': 'concept',
                'subcategory': 'Development_Patterns',
                'tags': ['concept', 'development', 'patterns', 'theory'],
                'complexity': 'intermediate',
                'quality': 'high'
            }
    
    # Roadmap and planning files
    if any(term in content_lower for term in ['roadmap', 'ロードマップ', 'planning', '計画', 'feature']):
        return {
            'category': 'resource',
            'subcategory': 'Documentation',
            'tags': ['roadmap', 'planning', 'features', 'development'],
            'complexity': 'intermediate',
            'quality': 'high'
        }
    
    # Default classification
    return get_default_classification()

def get_default_classification() -> Dict[str, Any]:
    """デフォルト分類"""
    return {
        'category': 'concept',
        'subcategory': 'Development_Patterns',
        'tags': ['misc', 'unclassified'],
        'complexity': 'intermediate',
        'quality': 'medium'
    }

def generate_frontmatter(file_path: Path, classification: Dict[str, Any]) -> str:
    """フロントマター生成"""
    filename = file_path.stem
    title = filename.replace('_', ' ').replace('-', ' ').title()
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    frontmatter_data = {
        'title': title,
        'created': today,
        'updated': today,
        'version': '1.0',
        'category': classification['category'],
        'tags': classification['tags'],
        'complexity': classification['complexity'],
        'quality': classification['quality'],
        'purpose': f"Auto-generated metadata for {filename}",
        'project': 'claude-knowledge-catalyst',
        'status': 'draft'
    }
    
    # Add subcategory if present
    if 'subcategory' in classification:
        frontmatter_data['subcategory'] = classification['subcategory']
    
    # Generate YAML frontmatter
    yaml_content = yaml.dump(frontmatter_data, default_flow_style=False, allow_unicode=True)
    return f"---\n{yaml_content}---\n\n"

def apply_metadata_to_file(file_path: Path, classification: Dict[str, Any], backup: bool = True) -> Dict[str, Any]:
    """ファイルにメタデータを適用"""
    try:
        # Create backup
        backup_path = None
        if backup:
            backup_path = Path(f"{file_path}.backup")
            shutil.copy2(file_path, backup_path)
        
        # Read original content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate frontmatter
        frontmatter_content = generate_frontmatter(file_path, classification)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"{frontmatter_content}{content}")
        
        return {'success': True, 'backup_path': backup_path}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}

def run_ckc_sync() -> Dict[str, Any]:
    """CKC同期実行"""
    try:
        result = subprocess.run(['uv', 'run', 'ckc', 'sync'], 
                              capture_output=True, text=True, check=True)
        return {'success': True, 'output': result.stdout}
    except subprocess.CalledProcessError as e:
        return {'success': False, 'error': e.stderr}

def smart_sync_command(
    auto_apply: bool = False,
    dry_run: bool = False, 
    directory: str = ".claude",
    backup: bool = True,
    config: CKCConfig = None,
    metadata_manager: MetadataManager = None
) -> None:
    """Smart sync main logic"""
    
    console.print("[bold blue]🚀 CKC Smart Sync[/bold blue] - Intelligent Batch Classification")
    console.print("=" * 60)
    
    # Phase 1: Scan metadata status
    console.print("\n[bold yellow]📊 Phase 1:[/bold yellow] メタデータ状況スキャン")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Scanning files...", total=None)
        has_metadata, needs_classification = scan_metadata_status(directory)
        progress.update(task, completed=True)
    
    # Create status table
    table = Table(title="Metadata Status")
    table.add_column("Status", style="cyan")
    table.add_column("Count", justify="right", style="magenta")
    table.add_column("Files", style="green")
    
    table.add_row("✅ Has Metadata", str(len(has_metadata)), f"{len(has_metadata)} files")
    table.add_row("⚠️ Needs Classification", str(len(needs_classification)), f"{len(needs_classification)} files")
    
    console.print(table)
    
    if not needs_classification:
        console.print("\n[green]🎉 All files already classified![/green] Running sync only...")
        
        if not dry_run:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Running CKC sync...", total=None)
                sync_result = run_ckc_sync()
                progress.update(task, completed=True)
            
            if sync_result['success']:
                console.print("[green]✅ Sync completed successfully[/green]")
            else:
                console.print(f"[red]❌ Sync error:[/red] {sync_result['error']}")
        else:
            console.print("[yellow]🔍 Dry run: Would run CKC sync[/yellow]")
        return
    
    # Phase 2: Batch classification
    console.print(f"\n[bold yellow]🤖 Phase 2:[/bold yellow] Batch Classification ({len(needs_classification)} files)")
    
    successful_classifications = []
    failed_classifications = []
    
    with Progress(console=console) as progress:
        task = progress.add_task("Classifying files...", total=len(needs_classification))
        
        for file_path in needs_classification:
            console.print(f"  📋 Analyzing: [cyan]{file_path.name}[/cyan]")
            
            result = classify_file_intelligent(file_path, config, metadata_manager)
            if result['success']:
                successful_classifications.append((file_path, result['classification']))
                console.print(f"    ✅ Category: [green]{result['classification']['category']}[/green]")
            else:
                failed_classifications.append((file_path, result['error']))
                console.print(f"    ❌ Error: [red]{result['error']}[/red]")
            
            progress.advance(task)
    
    # Phase 3: Apply metadata
    if successful_classifications and not dry_run:
        console.print(f"\n[bold yellow]📝 Phase 3:[/bold yellow] Metadata Application ({len(successful_classifications)} files)")
        
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
            if result['success']:
                applied_files.append(file_path)
                console.print(f"  ✅ Applied: [green]{file_path.name}[/green]")
            else:
                console.print(f"  ❌ Failed: [red]{file_path.name}[/red] - {result['error']}")
    
    elif dry_run:
        console.print(f"\n[yellow]🔍 Dry run: Would apply metadata to {len(successful_classifications)} files[/yellow]")
        applied_files = []
    else:
        applied_files = []
    
    # Phase 4: CKC sync
    if not dry_run:
        console.print(f"\n[bold yellow]🔄 Phase 4:[/bold yellow] CKC Synchronization")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Running CKC sync...", total=None)
            sync_result = run_ckc_sync()
            progress.update(task, completed=True)
        
        if sync_result['success']:
            console.print("[green]✅ Sync completed successfully[/green]")
        else:
            console.print(f"[red]❌ Sync error:[/red] {sync_result['error']}")
    else:
        console.print(f"\n[yellow]🔍 Dry run: Would run CKC sync[/yellow]")
        sync_result = {'success': True}
    
    # Phase 5: Summary
    console.print(f"\n[bold yellow]📊 Phase 5:[/bold yellow] Summary")
    console.print("=" * 60)
    
    summary_table = Table(title="Processing Results")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Count", justify="right", style="magenta")
    summary_table.add_column("Status", style="green")
    
    summary_table.add_row("📁 Target Files", str(len(needs_classification)), "Scanned")
    summary_table.add_row("✅ Classification Success", str(len(successful_classifications)), "Completed")
    summary_table.add_row("❌ Classification Failed", str(len(failed_classifications)), "Manual Required")
    
    if not dry_run:
        summary_table.add_row("📝 Metadata Applied", str(len(applied_files) if 'applied_files' in locals() else 0), "Completed")
        summary_table.add_row("🔄 Sync Status", "1" if sync_result['success'] else "0", "Success" if sync_result['success'] else "Failed")
    else:
        summary_table.add_row("📝 Metadata Applied", "0", "Dry Run")
        summary_table.add_row("🔄 Sync Status", "0", "Dry Run")
    
    console.print(summary_table)
    
    if failed_classifications:
        console.print(f"\n[red]⚠️ Manual attention required for {len(failed_classifications)} files:[/red]")
        for file_path, error in failed_classifications:
            console.print(f"  - [yellow]{file_path}[/yellow]: {error}")
    
    if not dry_run and len(applied_files) > 0:
        console.print(f"\n[green]🎉 Successfully processed {len(applied_files)} files![/green]")
    elif dry_run:
        console.print(f"\n[yellow]🔍 Dry run completed. {len(successful_classifications)} files ready for processing.[/yellow]")