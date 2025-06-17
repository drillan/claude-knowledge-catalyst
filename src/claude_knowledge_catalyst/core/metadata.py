"""Metadata management for knowledge files."""

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import frontmatter
from pydantic import BaseModel, Field


class KnowledgeMetadata(BaseModel):
    """Metadata for a knowledge file."""
    
    title: str = Field(..., description="Title of the knowledge item")
    created: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    version: str = Field(default="1.0", description="Version of the content")
    
    # Content classification
    category: Optional[str] = Field(None, description="Primary category")
    tags: List[str] = Field(default_factory=list, description="Tags for classification")
    
    # Claude-specific metadata
    model: Optional[str] = Field(None, description="Claude model used")
    confidence: Optional[str] = Field(None, description="Confidence level")
    success_rate: Optional[int] = Field(None, description="Success rate percentage")
    
    # Project context
    purpose: Optional[str] = Field(None, description="Purpose of this knowledge item")
    related_projects: List[str] = Field(default_factory=list, description="Related project names")
    
    # Status and quality
    status: str = Field(default="draft", description="Status of the item")
    quality: Optional[str] = Field(None, description="Quality assessment")
    
    # Additional metadata
    author: Optional[str] = Field(None, description="Author of the content")
    source: Optional[str] = Field(None, description="Source file path")
    checksum: Optional[str] = Field(None, description="Content checksum for change detection")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class MetadataManager:
    """Manager for extracting, updating, and managing metadata."""
    
    def __init__(self, tag_config: Optional[Dict[str, List[str]]] = None):
        """Initialize metadata manager with tag configuration."""
        self.tag_config = tag_config or {
            "category": ["prompt", "code", "concept", "resource", "project_log"],
            "tech": ["python", "javascript", "react", "nodejs"],
            "claude": ["opus", "sonnet", "haiku"],
            "status": ["draft", "tested", "production", "deprecated"],
            "quality": ["high", "medium", "low", "experimental"]
        }
    
    def extract_metadata_from_file(self, file_path: Path) -> KnowledgeMetadata:
        """Extract metadata from a markdown file."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Parse frontmatter
        with open(file_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)
        
        metadata = post.metadata
        content = post.content
        
        # Extract title from metadata or content
        title = self._extract_title(metadata, content)
        
        # Extract tags from content and metadata
        tags = self._extract_tags(metadata, content)
        
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
            purpose=metadata.get("purpose"),
            related_projects=metadata.get("related_projects", []),
            status=metadata.get("status", "draft"),
            quality=metadata.get("quality"),
            author=metadata.get("author"),
            source=str(file_path.resolve()),
            checksum=self._calculate_checksum(content)
        )
    
    def update_file_metadata(self, file_path: Path, metadata: KnowledgeMetadata) -> None:
        """Update metadata in a markdown file."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read existing file
        with open(file_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)
        
        # Update metadata
        post.metadata.update(metadata.dict(exclude={"checksum", "source"}))
        
        # Write back to file
        with open(file_path, "w", encoding="utf-8") as f:
            frontmatter.dump(post, f)
    
    def _extract_title(self, metadata: Dict[str, Any], content: str) -> str:
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
    
    def _extract_tags(self, metadata: Dict[str, Any], content: str) -> List[str]:
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
        
        return sorted(list(tags))
    
    def _infer_tags_from_content(self, content: str) -> Set[str]:
        """Infer tags from content analysis."""
        tags = set()
        content_lower = content.lower()
        
        # Check for technology mentions
        tech_keywords = {
            "python": ["python", "pip", "conda", "pytest", "django", "flask"],
            "javascript": ["javascript", "js", "node", "npm", "react", "vue"],
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
        if any(pattern in content_lower for pattern in ["prompt", "claude", "ai", "llm"]):
            tags.add("prompt")
        
        # Check for code patterns
        if any(pattern in content for pattern in ["```", "def ", "function ", "class "]):
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
    
    def create_metadata_template(self, title: str, category: str = "draft") -> Dict[str, Any]:
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
    
    def validate_tags(self, tags: List[str]) -> List[str]:
        """Validate and normalize tags."""
        valid_tags = []
        
        for tag in tags:
            tag = tag.lower().strip()
            if tag and tag.replace("_", "").replace("-", "").isalnum():
                valid_tags.append(tag)
        
        return valid_tags
    
    def suggest_tags(self, content: str, existing_tags: List[str]) -> List[str]:
        """Suggest additional tags based on content analysis."""
        inferred = self._infer_tags_from_content(content)
        current = set(existing_tags)
        
        suggestions = []
        for tag in inferred:
            if tag not in current:
                suggestions.append(tag)
        
        return suggestions[:5]  # Limit to top 5 suggestions