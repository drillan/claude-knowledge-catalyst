"""Obsidian vault synchronization functionality."""

from pathlib import Path
from typing import Any

from ..core.config import SyncTarget
from ..core.metadata import KnowledgeMetadata, MetadataManager


class ObsidianVaultManager:
    """Manager for Obsidian vault operations."""

    def __init__(self, vault_path: Path, metadata_manager: MetadataManager):
        """Initialize Obsidian vault manager.

        Args:
            vault_path: Path to the Obsidian vault
            metadata_manager: Manager for metadata operations
        """
        self.vault_path = Path(vault_path)
        self.metadata_manager = metadata_manager

        # Hybrid vault structure with 10-step numbering system
        self.vault_structure = {
            "00_Catalyst_Lab": "実験・アイデア孵化の場",
            "10_Projects": "アクティブプロジェクト管理",
            "20_Knowledge_Base": "体系化された知見",
            "20_Knowledge_Base/Prompts": "プロンプト関連",
            "20_Knowledge_Base/Prompts/Templates": "汎用プロンプトテンプレート",
            "20_Knowledge_Base/Prompts/Best_Practices": "成功事例とベストプラクティス",
            "20_Knowledge_Base/Prompts/Improvement_Log": "プロンプト改善の記録",
            "20_Knowledge_Base/Code_Snippets": "再利用可能なコードスニペット",
            "20_Knowledge_Base/Code_Snippets/Python": "Python関連",
            "20_Knowledge_Base/Code_Snippets/JavaScript": "JavaScript関連",
            "20_Knowledge_Base/Code_Snippets/Bash": "Bash/Shell関連",
            "20_Knowledge_Base/Code_Snippets/Other_Languages": "その他言語",
            "20_Knowledge_Base/Concepts": "AI・LLM関連の概念整理",
            "20_Knowledge_Base/Concepts/API_Design": "API設計原則",
            "20_Knowledge_Base/Concepts/Software_Architecture": "ソフトウェア設計",
            "20_Knowledge_Base/Concepts/Development_Practices": "開発手法",
            "20_Knowledge_Base/Resources": "学習リソースと外部参考資料",
            "30_Wisdom_Archive": "高品質な知識資産",
            "_templates": "システムテンプレート",
            "Analytics": "知見の活用状況分析",
            "Archive": "古い・非推奨の知見",
        }

    def initialize_vault(self) -> bool:
        """Initialize Obsidian vault with proper structure.

        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Create vault directory if it doesn't exist
            self.vault_path.mkdir(parents=True, exist_ok=True)

            # Create directory structure
            for dir_path, description in self.vault_structure.items():
                full_path = self.vault_path / dir_path
                full_path.mkdir(parents=True, exist_ok=True)

                # Create a README.md in each directory to explain its purpose
                readme_path = full_path / "README.md"
                if not readme_path.exists():
                    readme_content = f"# {dir_path.split('/')[-1]}\n\n{description}"
                    readme_path.write_text(readme_content, encoding="utf-8")

            # Create vault configuration
            self._create_obsidian_config()

            print(f"Initialized Obsidian vault at: {self.vault_path}")
            return True

        except Exception as e:
            print(f"Error initializing vault: {e}")
            return False

    def sync_file(self, source_path: Path, project_name: str | None = None) -> bool:
        """Sync a single file to the Obsidian vault.

        Args:
            source_path: Path to the source file
            project_name: Name of the project (for organization)

        Returns:
            True if sync successful, False otherwise
        """
        try:
            if not source_path.exists():
                print(f"Source file does not exist: {source_path}")
                return False

            # Extract metadata to determine target location
            metadata = self.metadata_manager.extract_metadata_from_file(source_path)
            target_path = self._determine_target_path(
                metadata, source_path, project_name
            )

            # Ensure target directory exists
            target_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy file with enhanced metadata
            enhanced_content = self._enhance_content_for_obsidian(
                source_path, metadata, project_name
            )
            target_path.write_text(enhanced_content, encoding="utf-8")

            print(f"Synced: {source_path} -> {target_path}")
            return True

        except Exception as e:
            print(f"Error syncing file {source_path}: {e}")
            return False

    def sync_directory(
        self, source_dir: Path, project_name: str | None = None
    ) -> dict[str, bool]:
        """Sync an entire directory to the Obsidian vault.

        Args:
            source_dir: Path to the source directory
            project_name: Name of the project

        Returns:
            Dictionary mapping file paths to sync results
        """
        results = {}

        if not source_dir.exists():
            print(f"Source directory does not exist: {source_dir}")
            return results

        # Find all markdown files
        md_files = list(source_dir.rglob("*.md"))

        for file_path in md_files:
            success = self.sync_file(file_path, project_name)
            results[str(file_path)] = success

        return results

    def _determine_target_path(
        self, metadata: KnowledgeMetadata, source_path: Path, project_name: str | None
    ) -> Path:
        """Determine target path in vault based on metadata.

        Args:
            metadata: File metadata
            source_path: Original file path
            project_name: Project name

        Returns:
            Target path in the vault
        """
        # Shared Knowledge First (共有知識最優先): category-based classification
        # Always place categorized content in Knowledge_Base regardless of project_name

        # Determine if this is shared knowledge content
        is_shared_knowledge = metadata.category in ["prompt", "code", "concept"] or any(
            tag in ["prompt", "code", "concept"] for tag in metadata.tags
        )

        if is_shared_knowledge:
            # Force shared knowledge placement
            if metadata.category == "prompt" or "prompt" in metadata.tags:
                if (
                    metadata.status == "production"
                    and metadata.success_rate
                    and metadata.success_rate > 80
                ):
                    base_path = "20_Knowledge_Base/Prompts/Best_Practices"
                elif (
                    "improvement" in str(source_path).lower()
                    or "version" in metadata.model_dump()
                ):
                    base_path = "20_Knowledge_Base/Prompts/Improvement_Log"
                else:
                    base_path = "20_Knowledge_Base/Prompts/Templates"
            elif metadata.category == "code" or "code" in metadata.tags:
                # Determine language from tags or content
                if "python" in metadata.tags:
                    base_path = "20_Knowledge_Base/Code_Snippets/Python"
                elif "javascript" in metadata.tags:
                    base_path = "20_Knowledge_Base/Code_Snippets/JavaScript"
                elif any(tag in ["bash", "shell", "git"] for tag in metadata.tags):
                    base_path = "20_Knowledge_Base/Code_Snippets/Bash"
                else:
                    base_path = "20_Knowledge_Base/Code_Snippets/Other_Languages"
            elif metadata.category == "concept" or "concept" in metadata.tags:
                # Enhanced concept categorization
                if any(tag in ["api", "design"] for tag in metadata.tags):
                    base_path = "20_Knowledge_Base/Concepts/API_Design"
                elif any(tag in ["architecture", "system"] for tag in metadata.tags):
                    base_path = "20_Knowledge_Base/Concepts/Software_Architecture"
                elif any(
                    tag in ["development", "practices", "methodology"]
                    for tag in metadata.tags
                ):
                    base_path = "20_Knowledge_Base/Concepts/Development_Practices"
                else:
                    base_path = "20_Knowledge_Base/Concepts"
        elif "resource" in metadata.tags:
            base_path = "20_Knowledge_Base/Resources"
        elif project_name:
            # Project-specific content (only for truly uncategorized content)
            base_path = f"10_Projects/{project_name}/learnings"
        else:
            # Default to catalyst lab for uncategorized content
            base_path = "00_Catalyst_Lab"

        # Generate filename with metadata prefix
        filename = self._generate_filename(metadata, source_path)

        return self.vault_path / base_path / filename

    def _generate_filename(self, metadata: KnowledgeMetadata, source_path: Path) -> str:
        """Generate filename for the vault.

        Args:
            metadata: File metadata
            source_path: Original file path

        Returns:
            Generated filename
        """
        # Use title as base, fallback to original filename
        if metadata.title and metadata.title != "Untitled":
            base_name = metadata.title
        else:
            base_name = source_path.stem

        # Clean filename (remove special characters)
        import re

        clean_name = re.sub(r'[<>:"/\\|?*]', "_", base_name)

        # Add date prefix for better organization
        date_prefix = metadata.created.strftime("%Y%m%d")

        # Add version if specified
        version_suffix = ""
        if metadata.version and metadata.version != "1.0":
            version_suffix = f"_v{metadata.version}"

        return f"{date_prefix}_{clean_name}{version_suffix}.md"

    def _enhance_content_for_obsidian(
        self,
        source_path: Path,
        metadata: KnowledgeMetadata,
        project_name: str | None = None,
    ) -> str:
        """Enhance content with Obsidian-specific features.

        Args:
            source_path: Original file path
            metadata: File metadata
            project_name: Optional project name

        Returns:
            Enhanced content string
        """
        # Read original content
        original_content = source_path.read_text(encoding="utf-8")

        # Create enhanced frontmatter
        enhanced_frontmatter = self._create_obsidian_frontmatter(metadata, project_name)

        # Add Obsidian-specific enhancements
        enhancements = []

        # Add tag section
        if metadata.tags:
            tag_line = " ".join(f"#{tag}" for tag in metadata.tags)
            enhancements.append(f"\n**Tags:** {tag_line}\n")

        # Add related links section
        if metadata.related_projects:
            links = " | ".join(
                f"[[{project}]]" for project in metadata.related_projects
            )
            enhancements.append(f"\n**Related Projects:** {links}\n")

        # Add metadata summary
        summary_parts = []
        if metadata.model:
            summary_parts.append(f"**Model:** {metadata.model}")
        if metadata.success_rate:
            summary_parts.append(f"**Success Rate:** {metadata.success_rate}%")
        if metadata.confidence:
            summary_parts.append(f"**Confidence:** {metadata.confidence}")

        if summary_parts:
            enhancements.append(f"\n**Metadata:** {' | '.join(summary_parts)}\n")

        # Combine content
        if original_content.startswith("---"):
            # Replace existing frontmatter
            parts = original_content.split("---", 2)
            if len(parts) >= 3:
                content_without_frontmatter = parts[2].strip()
            else:
                content_without_frontmatter = original_content
        else:
            content_without_frontmatter = original_content

        enhanced_content = (
            enhanced_frontmatter
            + "\n"
            + "\n".join(enhancements)
            + "\n"
            + content_without_frontmatter
        )

        return enhanced_content

    def _create_obsidian_frontmatter(
        self, metadata: KnowledgeMetadata, project_name: str | None = None
    ) -> str:
        """Create Obsidian-compatible frontmatter.

        Args:
            metadata: File metadata
            project_name: Optional project name to ensure project field is set

        Returns:
            YAML frontmatter string
        """
        frontmatter_data = {
            "title": metadata.title,
            "created": metadata.created.isoformat(),
            "updated": metadata.updated.isoformat(),
            "tags": metadata.tags,
            "category": metadata.category,
            "status": metadata.status,
        }

        # Add optional fields
        if metadata.version:
            frontmatter_data["version"] = metadata.version
        if metadata.model:
            frontmatter_data["claude_model"] = metadata.model
        if metadata.confidence:
            frontmatter_data["confidence"] = metadata.confidence
        if metadata.success_rate:
            frontmatter_data["success_rate"] = metadata.success_rate
        if metadata.purpose:
            frontmatter_data["purpose"] = metadata.purpose

        # Ensure project field is always included when available
        project_to_use = metadata.project or project_name
        if project_to_use:
            frontmatter_data["project"] = project_to_use

        if metadata.related_projects:
            frontmatter_data["related_projects"] = metadata.related_projects
        if metadata.quality:
            frontmatter_data["quality"] = metadata.quality
        if metadata.author:
            frontmatter_data["author"] = metadata.author

        # Convert to YAML
        import yaml

        yaml_content = yaml.dump(
            frontmatter_data, default_flow_style=False, allow_unicode=True
        )

        return f"---\n{yaml_content}---"

    def _create_obsidian_config(self) -> None:
        """Create Obsidian vault configuration files."""
        obsidian_dir = self.vault_path / ".obsidian"
        obsidian_dir.mkdir(exist_ok=True)

        # Create app.json with basic settings
        app_config = {
            "attachmentFolderPath": "attachments",
            "promptDelete": False,
            "alwaysUpdateLinks": True,
            "newFileLocation": "folder",
            "newFileFolderPath": "00_Inbox",
            "useMarkdownLinks": True,
            "showLineNumber": True,
        }

        import json

        (obsidian_dir / "app.json").write_text(
            json.dumps(app_config, indent=2), encoding="utf-8"
        )

        # Create core-plugins.json
        core_plugins = [
            "file-explorer",
            "global-search",
            "switcher",
            "graph",
            "backlink",
            "outgoing-links",
            "tag-pane",
            "page-preview",
            "templates",
            "note-composer",
            "command-palette",
            "markdown-importer",
            "outline",
            "word-count",
        ]

        (obsidian_dir / "core-plugins.json").write_text(
            json.dumps(core_plugins, indent=2), encoding="utf-8"
        )

    def get_vault_stats(self) -> dict[str, int]:
        """Get statistics about the vault content.

        Returns:
            Dictionary with vault statistics
        """
        stats = {}

        for dir_name in self.vault_structure.keys():
            dir_path = self.vault_path / dir_name
            if dir_path.exists():
                md_files = list(dir_path.rglob("*.md"))
                stats[dir_name] = len(md_files)

        return stats

    def cleanup_empty_directories(self) -> int:
        """Remove empty directories from the vault.

        Returns:
            Number of directories removed
        """
        removed_count = 0

        # Walk through all directories
        for dir_path in self.vault_path.rglob("*/"):
            if dir_path.is_dir():
                try:
                    # Try to remove if empty (will fail if not empty)
                    dir_path.rmdir()
                    removed_count += 1
                except OSError:
                    # Directory not empty, continue
                    pass

        return removed_count


class ObsidianSyncManager:
    """High-level manager for Obsidian synchronization."""

    def __init__(self, sync_target: SyncTarget, metadata_manager: MetadataManager):
        """Initialize Obsidian sync manager.

        Args:
            sync_target: Sync target configuration
            metadata_manager: Metadata manager instance
        """
        self.sync_target = sync_target
        self.metadata_manager = metadata_manager
        self.vault_manager = ObsidianVaultManager(sync_target.path, metadata_manager)

    def initialize(self) -> bool:
        """Initialize the sync target.

        Returns:
            True if initialization successful
        """
        return self.vault_manager.initialize_vault()

    def sync_single_file(
        self, file_path: Path, project_name: str | None = None
    ) -> bool:
        """Sync a single file.

        Args:
            file_path: Path to the file to sync
            project_name: Optional project name

        Returns:
            True if sync successful
        """
        return self.vault_manager.sync_file(file_path, project_name)

    def sync_claude_directory(
        self, claude_dir: Path, project_name: str | None = None
    ) -> dict[str, bool]:
        """Sync entire .claude directory.

        Args:
            claude_dir: Path to .claude directory
            project_name: Optional project name

        Returns:
            Dictionary of sync results
        """
        return self.vault_manager.sync_directory(claude_dir, project_name)

    def get_sync_status(self) -> dict[str, Any]:
        """Get current sync status.

        Returns:
            Status dictionary
        """
        return {
            "target_name": self.sync_target.name,
            "target_path": str(self.sync_target.path),
            "enabled": self.sync_target.enabled,
            "vault_exists": self.sync_target.path.exists(),
            "vault_stats": self.vault_manager.get_vault_stats()
            if self.sync_target.path.exists()
            else {},
        }
