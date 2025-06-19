"""Metadata management for knowledge files."""

import re
from datetime import datetime
from pathlib import Path
from typing import Any

import frontmatter
from pydantic import BaseModel, Field


class KnowledgeMetadata(BaseModel):
    """Metadata for a knowledge file."""

    title: str = Field(..., description="Title of the knowledge item")
    created: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )
    version: str = Field(default="1.0", description="Version of the content")

    # Content classification
    category: str | None = Field(None, description="Primary category")
    subcategory: str | None = Field(None, description="Specific subcategory within category")
    tags: list[str] = Field(default_factory=list, description="Tags for classification")

    # Claude-specific metadata
    model: str | None = Field(None, description="Claude model used")
    confidence: str | None = Field(None, description="Confidence level")
    success_rate: int | None = Field(None, description="Success rate percentage")

    # Project context
    project: str | None = Field(None, description="Primary project name")
    purpose: str | None = Field(None, description="Purpose of this knowledge item")
    related_projects: list[str] = Field(
        default_factory=list, description="Related project names"
    )

    # Status and quality
    status: str = Field(default="draft", description="Status of the item")
    quality: str | None = Field(None, description="Quality assessment")
    complexity: str | None = Field(None, description="Content complexity level")

    # Additional metadata
    author: str | None = Field(None, description="Author of the content")
    source: str | None = Field(None, description="Source file path")
    checksum: str | None = Field(
        None, description="Content checksum for change detection"
    )

    model_config = {"json_encoders": {datetime: lambda v: v.isoformat()}}


class MetadataManager:
    """Manager for extracting, updating, and managing metadata."""

    def __init__(self, tag_config: dict[str, list[str]] | None = None):
        """Initialize metadata manager with tag configuration."""
        self.tag_config = tag_config or {
            "category": ["prompt", "code", "concept", "resource", "project_log"],
            "tech": ["python", "javascript", "react", "nodejs"],
            "claude": ["opus", "sonnet", "haiku"],
            "status": ["draft", "tested", "production", "deprecated"],
            "quality": ["high", "medium", "low", "experimental"],
        }

    def extract_metadata_from_file(self, file_path: Path) -> KnowledgeMetadata:
        """Extract metadata from a markdown file."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Parse frontmatter
        with open(file_path, encoding="utf-8") as f:
            post = frontmatter.load(f)

        metadata = post.metadata
        content = post.content

        # Extract title from metadata or content
        title = self._extract_title(metadata, content)

        # Extract tags from content and metadata
        tags = self._extract_tags(metadata, content)

        # Auto-detect project if not specified
        project = metadata.get("project") or self._auto_detect_project(file_path)

        # Create metadata object
        return KnowledgeMetadata(
            title=title,
            created=self._parse_datetime(metadata.get("created")),
            updated=self._parse_datetime(metadata.get("updated")),
            version=metadata.get("version", "1.0"),
            category=metadata.get("category"),
            tags=tags,
            model=metadata.get("model"),
            confidence=metadata.get("confidence"),
            success_rate=metadata.get("success_rate"),
            project=project,
            purpose=metadata.get("purpose"),
            related_projects=metadata.get("related_projects", []),
            status=metadata.get("status", "draft"),
            quality=metadata.get("quality"),
            author=metadata.get("author"),
            source=str(file_path.resolve()),
            checksum=self._calculate_checksum(content),
        )

    def update_file_metadata(
        self, file_path: Path, metadata: KnowledgeMetadata
    ) -> None:
        """Update metadata in a markdown file."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read existing file
        with open(file_path, encoding="utf-8") as f:
            post = frontmatter.load(f)

        # Update metadata
        post.metadata.update(metadata.model_dump(exclude={"checksum", "source"}))

        # Write back to file
        content = frontmatter.dumps(post)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _extract_title(self, metadata: dict[str, Any], content: str) -> str:
        """Extract title from metadata or content."""
        # Try metadata first
        if "title" in metadata:
            return metadata["title"]

        # Try to find first H1 heading
        h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()

        # Fallback to first non-empty line
        lines = content.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                return line[:50] + ("..." if len(line) > 50 else "")

        return "Untitled"

    def _extract_tags(self, metadata: dict[str, Any], content: str) -> list[str]:
        """Extract tags from metadata and content."""
        tags = set()

        # Tags from metadata
        if "tags" in metadata:
            if isinstance(metadata["tags"], list):
                tags.update(metadata["tags"])
            elif isinstance(metadata["tags"], str):
                tags.update(tag.strip() for tag in metadata["tags"].split(","))

        # Extract hashtags from content
        hashtag_pattern = r"#(\w+)"
        hashtags = re.findall(hashtag_pattern, content)
        tags.update(hashtags)

        # Infer tags from content
        inferred_tags = self._infer_tags_from_content(content)
        tags.update(inferred_tags)

        return sorted(tags)

    def _infer_tags_from_content(self, content: str) -> set[str]:
        """Infer tags from content analysis."""
        tags = set()
        content_lower = content.lower()

        # Check for technology mentions (精密なパターンマッチング)
        tech_keywords = {
            "python": ["python", "pip", "conda", "pytest", "django", "flask", "asyncio", "aiopg"],
            "javascript": ["javascript", "node.js", "npm install", "react", "vue.js", "const ", "let "],
            "react": ["react", "jsx", "component", "useState", "useEffect"],
            "docker": ["docker", "dockerfile", "container", "image"],
            "git": ["git", "commit", "branch", "merge", "pull request"],
        }

        for tag, keywords in tech_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                tags.add(tag)

        # Check for Claude model mentions
        claude_models = ["opus", "sonnet", "haiku"]
        for model in claude_models:
            if model in content_lower:
                tags.add(f"claude/{model}")

        # Check for prompt patterns
        if any(
            pattern in content_lower for pattern in ["prompt", "claude", "ai", "llm"]
        ):
            tags.add("prompt")

        # Check for code patterns
        if any(
            pattern in content for pattern in ["```", "def ", "function ", "class "]
        ):
            tags.add("code")

        return tags

    def _parse_datetime(self, dt_value: Any) -> datetime:
        """Parse datetime from various formats."""
        if dt_value is None:
            return datetime.now()

        if isinstance(dt_value, datetime):
            return dt_value

        if isinstance(dt_value, str):
            # Try ISO format first
            try:
                return datetime.fromisoformat(dt_value.replace("Z", "+00:00"))
            except ValueError:
                pass

            # Try common date formats
            formats = [
                "%Y-%m-%d",
                "%Y-%m-%d %H:%M:%S",
                "%Y/%m/%d",
                "%d/%m/%Y",
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(dt_value, fmt)
                except ValueError:
                    continue

        return datetime.now()

    def _calculate_checksum(self, content: str) -> str:
        """Calculate checksum for content change detection."""
        import hashlib

        return hashlib.md5(content.encode("utf-8")).hexdigest()

    def create_metadata_template(
        self, title: str, category: str = "draft"
    ) -> dict[str, Any]:
        """Create a metadata template for new files."""
        return {
            "title": title,
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "version": "1.0",
            "category": category,
            "status": "draft",
            "tags": [],
        }

    def validate_tags(self, tags: list[str]) -> list[str]:
        """Validate and normalize tags."""
        valid_tags = []

        for tag in tags:
            tag = tag.lower().strip()
            if tag and tag.replace("_", "").replace("-", "").isalnum():
                valid_tags.append(tag)

        return valid_tags

    def suggest_tags(self, content: str, existing_tags: list[str]) -> list[str]:
        """Suggest additional tags based on content analysis."""
        inferred = self._infer_tags_from_content(content)
        current = set(existing_tags)

        suggestions = []
        for tag in inferred:
            if tag not in current:
                suggestions.append(tag)

        return suggestions[:5]  # Limit to top 5 suggestions

    def _auto_detect_project(self, file_path: Path) -> str | None:
        """Auto-detect project name from file path and git context."""
        # Method 1: Check for .claude/project.yaml
        claude_dir = self._find_claude_directory(file_path)
        if claude_dir:
            project_config = claude_dir / "project.yaml"
            if project_config.exists():
                try:
                    import yaml
                    with open(project_config, 'r', encoding='utf-8') as f:
                        config = yaml.safe_load(f)
                        return config.get('project_name')
                except Exception:
                    pass
        
        # Method 2: Extract from git repository name
        git_project = self._detect_project_from_git(file_path)
        if git_project:
            return git_project
        
        # Method 3: Use parent directory name as fallback
        return self._detect_project_from_path(file_path)
    
    def _find_claude_directory(self, file_path: Path) -> Path | None:
        """Find the nearest .claude directory walking up the tree."""
        current = file_path.parent if file_path.is_file() else file_path
        
        while current != current.parent:  # Stop at filesystem root
            claude_dir = current / ".claude"
            if claude_dir.exists() and claude_dir.is_dir():
                return claude_dir
            current = current.parent
        
        return None
    
    def _detect_project_from_git(self, file_path: Path) -> str | None:
        """Detect project name from git repository."""
        try:
            import subprocess
            current = file_path.parent if file_path.is_file() else file_path
            
            # Find git root
            result = subprocess.run(
                ['git', 'rev-parse', '--show-toplevel'],
                cwd=current,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                git_root = Path(result.stdout.strip())
                return git_root.name
                
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        return None
    
    def _detect_project_from_path(self, file_path: Path) -> str | None:
        """Detect project name from file path structure."""
        # Look for common project indicators
        current = file_path.parent if file_path.is_file() else file_path
        
        # Walk up to find a directory that looks like a project root
        while current != current.parent:
            # Check for common project files
            project_indicators = [
                'package.json', 'pyproject.toml', 'Cargo.toml', 
                'go.mod', 'pom.xml', 'build.gradle', 'requirements.txt',
                '.git', 'README.md'
            ]
            
            if any((current / indicator).exists() for indicator in project_indicators):
                return current.name
            
            current = current.parent
        
        return None
