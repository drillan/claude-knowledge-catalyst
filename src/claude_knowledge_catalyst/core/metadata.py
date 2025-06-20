"""Metadata management for knowledge files."""

import re
from datetime import datetime
from pathlib import Path
from typing import Any

import frontmatter
from pydantic import BaseModel, Field

from .tag_standards import TagStandardsManager


class KnowledgeMetadata(BaseModel):
    """Pure tag-centered metadata for knowledge items."""

    title: str = Field(..., description="Title of the knowledge item")
    created: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )
    version: str = Field(default="1.0", description="Version of the content")

    # === Pure Multi-layered Tag Architecture ===
    
    # Basic classification (required)
    type: str = Field(default="prompt", description="Content type: prompt, code, concept, resource")
    status: str = Field(default="draft", description="Status: draft, tested, production, deprecated")
    
    # Technical domains (multiple selection allowed)
    tech: list[str] = Field(default_factory=list, description="Technology stack: python, javascript, api, etc.")
    domain: list[str] = Field(default_factory=list, description="Domain areas: web-dev, data-science, automation, etc.")
    
    # Quality indicators
    success_rate: int | None = Field(None, description="Success rate percentage (0-100)")
    complexity: str | None = Field(None, description="Complexity level: beginner, intermediate, advanced")
    confidence: str | None = Field(None, description="Confidence level: low, medium, high")
    
    # Project relationships
    projects: list[str] = Field(default_factory=list, description="Associated project names")
    team: list[str] = Field(default_factory=list, description="Team areas: backend, frontend, devops, etc.")
    
    # Claude-specific metadata
    claude_model: list[str] = Field(default_factory=list, description="Claude models: opus, sonnet, haiku")
    claude_feature: list[str] = Field(default_factory=list, description="Claude features: code-generation, analysis, creative")
    
    # Evolutionary tags (free-form)
    tags: list[str] = Field(default_factory=list, description="Free-form evolutionary tags")
    
    # System metadata
    author: str | None = Field(None, description="Author of the content")
    source: str | None = Field(None, description="Source file path")
    checksum: str | None = Field(None, description="Content checksum for change detection")
    purpose: str | None = Field(None, description="Purpose of this knowledge item")

    model_config = {"json_encoders": {datetime: lambda v: v.isoformat()}}


class MetadataManager:
    """Pure tag-centered metadata manager for knowledge items."""

    def __init__(self, tag_config: dict[str, list[str]] | None = None):
        """Initialize metadata manager with tag configuration."""
        self.tag_config = tag_config or self._get_default_tag_config()
        self.tag_standards = TagStandardsManager()

    def _get_default_tag_config(self) -> dict[str, list[str]]:
        """Get default tag configuration for pure tag system."""
        return {
            # Basic classification (required)
            "type": ["prompt", "code", "concept", "resource"],
            "status": ["draft", "tested", "production", "deprecated"],
            
            # Technical domains (extensible)
            "tech": ["python", "javascript", "typescript", "react", "nodejs", "api", 
                    "docker", "git", "aws", "gcp", "azure", "kubernetes", "terraform"],
            "domain": ["web-dev", "data-science", "automation", "devops", "ai-ml", 
                      "backend", "frontend", "mobile", "database", "security", "testing"],
            
            # Quality indicators
            "complexity": ["beginner", "intermediate", "advanced", "expert"],
            "confidence": ["low", "medium", "high"],
            
            # Team areas
            "team": ["backend", "frontend", "devops", "data", "mobile", "design", "qa", "ml"],
            
            # Claude models and features
            "claude_model": ["opus", "sonnet", "haiku"],
            "claude_feature": ["code-generation", "analysis", "creative", "debugging", 
                              "review", "documentation", "refactoring", "optimization"],
        }

    def extract_metadata_from_file(self, file_path: Path) -> KnowledgeMetadata:
        """Extract pure tag-centered metadata from a markdown file."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Parse frontmatter
        with open(file_path, encoding="utf-8") as f:
            post = frontmatter.load(f)

        metadata = post.metadata
        content = post.content

        # Extract title from metadata or content
        title = self._extract_title(metadata, content)

        # Extract pure tag-centered metadata
        tag_metadata = self._extract_tag_metadata(metadata, content)

        # Auto-detect projects if not specified
        projects = self._extract_projects(metadata, file_path)

        # Infer missing metadata from content analysis
        inferred_metadata = self._infer_metadata_from_content(content)

        # Merge all metadata sources (pure tag system only)
        final_metadata = {
            **tag_metadata,
            **inferred_metadata,
            "title": title,
            "created": self._parse_datetime(metadata.get("created")),
            "updated": self._parse_datetime(metadata.get("updated")),
            "version": metadata.get("version", "1.0"),
            "projects": projects,
            "purpose": metadata.get("purpose"),
            "author": metadata.get("author"),
            "source": str(file_path.resolve()),
            "checksum": self._calculate_checksum(content),
        }

        return KnowledgeMetadata(**final_metadata)
    
    def _extract_tag_metadata(self, metadata: dict[str, Any], content: str) -> dict[str, Any]:
        """Extract pure tag-centered metadata from file frontmatter and content."""
        result = {
            "type": metadata.get("type", self._infer_type_from_content(content)),
            "status": metadata.get("status", "draft"),
            "tech": self._ensure_list(metadata.get("tech", [])),
            "domain": self._ensure_list(metadata.get("domain", [])),
            "complexity": metadata.get("complexity"),
            "confidence": metadata.get("confidence"),
            "success_rate": metadata.get("success_rate"),
            "projects": self._ensure_list(metadata.get("projects", [])),
            "team": self._ensure_list(metadata.get("team", [])),
            "claude_model": self._ensure_list(metadata.get("claude_model", [])),
            "claude_feature": self._ensure_list(metadata.get("claude_feature", [])),
            "tags": self._ensure_list(metadata.get("tags", [])),
        }

        # Extract hashtags from content
        hashtags = self._extract_hashtags_from_content(content)
        result["tags"].extend(hashtags)

        # Infer technical tags from content
        inferred_tech = self._infer_tech_tags(content)
        result["tech"].extend(inferred_tech)

        # Infer domain tags from content
        inferred_domain = self._infer_domain_tags(content)
        result["domain"].extend(inferred_domain)

        # Deduplicate and validate all tag lists
        for key, value in result.items():
            if isinstance(value, list):
                result[key] = self._deduplicate_and_validate_tags(value)

        return result
    
    def _infer_type_from_content(self, content: str) -> str:
        """Infer content type from content analysis."""
        content_lower = content.lower()
        
        # Check for prompt patterns
        if any(pattern in content_lower for pattern in ["prompt", "claude", "ask", "request", "generate"]):
            return "prompt"
        
        # Check for code patterns
        if any(pattern in content for pattern in ["```", "def ", "function ", "class ", "import ", "const ", "let "]):
            return "code"
        
        # Check for concept patterns
        if any(pattern in content_lower for pattern in ["concept", "theory", "principle", "methodology", "approach"]):
            return "concept"
        
        # Check for resource patterns
        if any(pattern in content_lower for pattern in ["resource", "link", "reference", "documentation", "guide"]):
            return "resource"
        
        # Default to prompt if unclear
        return "prompt"
    
    def _infer_domain_tags(self, content: str) -> list[str]:
        """Infer domain tags from content analysis."""
        content_lower = content.lower()
        domain_tags = []
        
        # Domain detection patterns
        domain_patterns = {
            "web-dev": ["web", "html", "css", "frontend", "backend", "server", "client"],
            "data-science": ["data", "analysis", "pandas", "numpy", "ml", "ai", "analytics"],
            "automation": ["automation", "script", "cron", "task", "batch", "workflow"],
            "devops": ["deploy", "ci/cd", "infrastructure", "monitoring", "kubernetes", "docker"],
            "ai-ml": ["ai", "ml", "machine learning", "neural", "model", "training"],
            "mobile": ["mobile", "ios", "android", "app", "react native", "flutter"],
            "database": ["database", "sql", "mongodb", "postgres", "mysql", "redis"],
            "security": ["security", "auth", "encryption", "vulnerability", "secure"],
            "testing": ["test", "testing", "unit test", "integration", "qa", "quality"],
        }
        
        for domain, patterns in domain_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                domain_tags.append(domain)
        
        return domain_tags
    
    def _infer_metadata_from_content(self, content: str) -> dict[str, Any]:
        """Infer metadata from content analysis."""
        inferred = {}
        
        # Infer complexity from content length and structure
        if len(content) < 500:
            inferred["complexity"] = "beginner"
        elif len(content) < 2000:
            inferred["complexity"] = "intermediate"
        else:
            inferred["complexity"] = "advanced"
        
        # Infer confidence from content quality indicators
        if any(indicator in content.lower() for indicator in ["tested", "proven", "validated", "production"]):
            inferred["confidence"] = "high"
        elif any(indicator in content.lower() for indicator in ["experimental", "draft", "wip", "todo"]):
            inferred["confidence"] = "low"
        else:
            inferred["confidence"] = "medium"
        
        return inferred
    
    def _ensure_list(self, value: Any) -> list[str]:
        """Ensure value is a list of strings."""
        if value is None:
            return []
        if isinstance(value, str):
            return [value] if value.strip() else []
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        return [str(value).strip()] if str(value).strip() else []
    
    def _extract_hashtags_from_content(self, content: str) -> list[str]:
        """Extract hashtags from content."""
        import re
        hashtag_pattern = r"#(\w+)"
        hashtags = re.findall(hashtag_pattern, content)
        return list(set(hashtags))
    
    def _infer_tech_tags(self, content: str) -> list[str]:
        """Infer technology tags from content."""
        content_lower = content.lower()
        tech_tags = []
        
        # Enhanced technology detection
        tech_patterns = {
            "python": ["python", "pip", "conda", "pytest", "django", "flask", "fastapi", "asyncio"],
            "javascript": ["javascript", "js", "node.js", "npm", "yarn", "const ", "let ", "=>"],
            "typescript": ["typescript", "ts", "interface", "type ", ".ts", ".tsx"],
            "react": ["react", "jsx", "component", "useState", "useEffect", "props"],
            "nodejs": ["node.js", "nodejs", "express", "npm", "package.json"],
            "api": ["api", "rest", "graphql", "endpoint", "json", "http"],
            "docker": ["docker", "dockerfile", "container", "image", "compose"],
            "git": ["git", "commit", "branch", "merge", "pull request", "github"],
            "aws": ["aws", "s3", "ec2", "lambda", "cloudformation"],
            "database": ["sql", "mongodb", "postgres", "mysql", "redis"],
        }
        
        for tech, patterns in tech_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                tech_tags.append(tech)
        
        return tech_tags
    
    def _deduplicate_and_validate_tags(self, tags: list[str]) -> list[str]:
        """Remove duplicates and validate tag format."""
        if not tags:
            return []
        
        # Normalize and deduplicate
        normalized = []
        seen = set()
        
        for tag in tags:
            if isinstance(tag, str):
                tag = tag.lower().strip()
                if tag and tag not in seen and self._is_valid_tag(tag):
                    normalized.append(tag)
                    seen.add(tag)
        
        return sorted(normalized)
    
    def _is_valid_tag(self, tag: str) -> bool:
        """Validate if tag format is acceptable."""
        if not tag:
            return False
        # Allow alphanumeric, hyphens, underscores, and forward slashes
        return all(c.isalnum() or c in "-_/" for c in tag)
    
    def _extract_projects(self, metadata: dict[str, Any], file_path: Path) -> list[str]:
        """Extract project information from various sources."""
        projects = []
        
        # From metadata
        if "projects" in metadata:
            projects.extend(self._ensure_list(metadata["projects"]))
        
        # Legacy support
        if "project" in metadata:
            projects.extend(self._ensure_list(metadata["project"]))
        
        if "related_projects" in metadata:
            projects.extend(self._ensure_list(metadata["related_projects"]))
        
        # Auto-detect if no projects specified
        if not projects:
            auto_project = self._auto_detect_project(file_path)
            if auto_project:
                projects.append(auto_project)
        
        return self._deduplicate_and_validate_tags(projects)

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

    def create_tag_metadata_template(
        self, title: str, content_type: str = "prompt", status: str = "draft"
    ) -> dict[str, Any]:
        """Create pure tag-centered metadata template for new files."""
        return {
            "title": title,
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "version": "1.0",
            "type": content_type,
            "status": status,
            "tech": [],
            "domain": [],
            "complexity": None,
            "confidence": None,
            "success_rate": None,
            "projects": [],
            "team": [],
            "claude_model": [],
            "claude_feature": [],
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

    def suggest_tag_enhancements(self, content: str, existing_metadata: dict[str, Any]) -> dict[str, list[str]]:
        """Suggest tag enhancements based on content analysis."""
        suggestions = {
            "tech": [],
            "domain": [],
            "claude_feature": [],
            "tags": []
        }
        
        # Infer technical tags
        inferred_tech = self._infer_tech_tags(content)
        existing_tech = self._ensure_list(existing_metadata.get("tech", []))
        suggestions["tech"] = [tag for tag in inferred_tech if tag not in existing_tech]
        
        # Infer domain tags
        inferred_domain = self._infer_domain_tags(content)
        existing_domain = self._ensure_list(existing_metadata.get("domain", []))
        suggestions["domain"] = [tag for tag in inferred_domain if tag not in existing_domain]
        
        # Suggest Claude features based on content
        feature_patterns = {
            "code-generation": ["generate", "create", "build", "implement"],
            "analysis": ["analyze", "review", "examine", "evaluate"],
            "debugging": ["debug", "error", "fix", "troubleshoot"],
            "documentation": ["document", "readme", "guide", "explanation"],
            "optimization": ["optimize", "improve", "enhance", "performance"],
        }
        
        content_lower = content.lower()
        existing_features = self._ensure_list(existing_metadata.get("claude_feature", []))
        for feature, patterns in feature_patterns.items():
            if feature not in existing_features and any(pattern in content_lower for pattern in patterns):
                suggestions["claude_feature"].append(feature)
        
        # Extract hashtags as tag suggestions
        hashtags = self._extract_hashtags_from_content(content)
        existing_tags = self._ensure_list(existing_metadata.get("tags", []))
        suggestions["tags"] = [tag for tag in hashtags if tag not in existing_tags]
        
        return suggestions

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
    
    def validate_tag_metadata(self, metadata: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate tag-centered metadata structure and return errors."""
        errors = []
        
        # Required fields
        if not metadata.get("title"):
            errors.append("Title is required")
        
        # Validate type
        valid_types = self.tag_config.get("type", ["prompt", "code", "concept", "resource"])
        if metadata.get("type") not in valid_types:
            errors.append(f"Invalid type: {metadata.get('type')}. Valid: {valid_types}")
        
        # Validate status
        valid_statuses = self.tag_config.get("status", ["draft", "tested", "production", "deprecated"])
        if metadata.get("status") not in valid_statuses:
            errors.append(f"Invalid status: {metadata.get('status')}. Valid: {valid_statuses}")
        
        # Validate success_rate
        success_rate = metadata.get("success_rate")
        if success_rate is not None:
            if not isinstance(success_rate, int) or not 0 <= success_rate <= 100:
                errors.append("success_rate must be an integer between 0 and 100")
        
        # Validate complexity
        complexity = metadata.get("complexity")
        if complexity is not None:
            valid_complexity = self.tag_config.get("complexity", ["beginner", "intermediate", "advanced"])
            if complexity not in valid_complexity:
                errors.append(f"Invalid complexity: {complexity}. Valid: {valid_complexity}")
        
        # Validate confidence
        confidence = metadata.get("confidence")
        if confidence is not None:
            valid_confidence = self.tag_config.get("confidence", ["low", "medium", "high"])
            if confidence not in valid_confidence:
                errors.append(f"Invalid confidence: {confidence}. Valid: {valid_confidence}")
        
        return len(errors) == 0, errors
    
    def get_tag_statistics(self, metadata_list: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
        """Get statistics about tag usage across multiple files."""
        stats = {
            "type": {},
            "status": {},
            "tech": {},
            "domain": {},
            "complexity": {},
            "confidence": {},
            "claude_model": {},
            "claude_feature": {},
            "tags": {}
        }
        
        for metadata in metadata_list:
            # Count single-value fields
            for field in ["type", "status", "complexity", "confidence"]:
                value = metadata.get(field)
                if value:
                    stats[field][value] = stats[field].get(value, 0) + 1
            
            # Count list fields
            for field in ["tech", "domain", "claude_model", "claude_feature", "tags"]:
                values = self._ensure_list(metadata.get(field, []))
                for value in values:
                    stats[field][value] = stats[field].get(value, 0) + 1
        
        return stats
    
    def validate_and_enhance_tags(self, metadata: KnowledgeMetadata, content: str) -> tuple[KnowledgeMetadata, list[str]]:
        """Validate and enhance metadata tags using standards.
        
        Args:
            metadata: Current metadata
            content: File content for analysis
            
        Returns:
            Tuple of (enhanced_metadata, validation_errors)
        """
        # Convert to dict for validation
        metadata_dict = metadata.model_dump()
        
        # Validate current tags
        is_valid, errors = self.tag_standards.validate_metadata_tags(metadata_dict)
        
        # Get tag suggestions
        existing_tags = {
            "type": [metadata.type],
            "status": [metadata.status],
            "tech": metadata.tech,
            "domain": metadata.domain,
            "team": metadata.team,
            "claude_model": metadata.claude_model,
            "claude_feature": metadata.claude_feature,
            "tags": metadata.tags
        }
        
        suggestions = self.tag_standards.suggest_tags(content, existing_tags)
        
        # Enhance metadata with suggestions
        enhanced_dict = metadata_dict.copy()
        for tag_type, suggested_values in suggestions.items():
            if tag_type in enhanced_dict:
                current_values = enhanced_dict[tag_type] or []
                # Add suggestions that aren't already present
                for suggestion in suggested_values:
                    if suggestion not in current_values:
                        current_values.append(suggestion)
                enhanced_dict[tag_type] = current_values
        
        # Create enhanced metadata
        enhanced_metadata = KnowledgeMetadata(**enhanced_dict)
        
        return enhanced_metadata, errors
    
    def get_tag_recommendations(self, tag_type: str, partial_value: str = "") -> list[str]:
        """Get tag recommendations for autocomplete."""
        return self.tag_standards.get_tag_recommendations(tag_type, partial_value)
    
    def export_tag_documentation(self) -> str:
        """Export tag standards as markdown documentation."""
        return self.tag_standards.export_standards_as_markdown()
