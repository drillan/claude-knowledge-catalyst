"""Advanced metadata enhancement and analysis for CKC."""

import re
from datetime import datetime
from pathlib import Path
from typing import Any

from ..core.config import CKCConfig
from ..core.metadata import KnowledgeMetadata, MetadataManager


class AdvancedMetadataEnhancer:
    """Advanced metadata enhancement with content analysis."""

    def __init__(self, config: CKCConfig):
        self.config = config
        self.hybrid_config = config.hybrid_structure
        self.base_metadata_manager = MetadataManager()

        # Enhanced analysis patterns
        self.complexity_patterns = {
            "beginner": ["basic", "simple", "intro", "getting started", "tutorial"],
            "intermediate": ["advanced", "complex", "detailed", "comprehensive"],
            "expert": [
                "deep dive",
                "architecture",
                "optimization",
                "performance",
                "expert",
            ],
        }

        self.quality_indicators = {
            "high": ["tested", "production", "verified", "validated", "comprehensive"],
            "medium": ["draft", "review", "prototype", "experimental"],
            "low": ["todo", "wip", "placeholder", "incomplete"],
        }

        self.success_patterns = {
            "high_success": [
                "works perfectly",
                "great results",
                "highly effective",
                "excellent",
            ],
            "medium_success": ["works well", "good results", "effective", "useful"],
            "low_success": ["needs work", "issues", "problems", "failed"],
        }

    def enhance_metadata(
        self, file_path: Path, content: str | None = None
    ) -> KnowledgeMetadata:
        """Enhance metadata with advanced analysis."""
        # Start with base metadata
        base_metadata = self.base_metadata_manager.extract_metadata_from_file(file_path)

        # Read content if not provided
        if content is None:
            content = file_path.read_text(encoding="utf-8")

        # Apply enhancements
        enhanced_metadata = self._apply_enhancements(base_metadata, content, file_path)

        return enhanced_metadata

    def _apply_enhancements(
        self, metadata: KnowledgeMetadata, content: str, file_path: Path
    ) -> KnowledgeMetadata:
        """Apply various metadata enhancements."""

        # Content analysis
        content_analysis = self._analyze_content(content)

        # Enhance complexity assessment
        if not hasattr(metadata, "complexity"):
            metadata.complexity = self._assess_complexity(content, content_analysis)

        # Enhance confidence assessment (quality renamed to confidence)
        if not metadata.confidence or metadata.confidence == "experimental":
            metadata.confidence = self._assess_quality(
                content, content_analysis, metadata
            )

        # Enhance success rate estimation
        if not metadata.success_rate:
            metadata.success_rate = self._estimate_success_rate(
                content, content_analysis
            )

        # Enhanced tag inference
        enhanced_tags = self._infer_enhanced_tags(content, content_analysis, file_path)
        metadata.tags = list(set(metadata.tags + enhanced_tags))

        # Confidence assessment
        if not metadata.confidence:
            metadata.confidence = self._assess_confidence(
                content, content_analysis, metadata
            )

        # Purpose enhancement
        if not metadata.purpose:
            metadata.purpose = self._infer_purpose(content, content_analysis, file_path)

        # Related projects inference
        related_projects = self._infer_related_projects(content, file_path)
        if related_projects:
            metadata.projects = list(set(metadata.projects + related_projects))

        # Update timestamp
        metadata.updated = datetime.now()

        return metadata

    def _analyze_content(self, content: str) -> dict[str, Any]:
        """Comprehensive content analysis."""
        analysis = {
            "word_count": len(content.split()),
            "line_count": len(content.splitlines()),
            "code_blocks": len(re.findall(r"```[\s\S]*?```", content)),
            "links": len(re.findall(r"\[.*?\]\(.*?\)", content)),
            "headers": len(re.findall(r"^#+\s", content, re.MULTILINE)),
            "lists": len(re.findall(r"^\s*[-*+]\s", content, re.MULTILINE)),
            "emphasis": len(re.findall(r"\*\*.*?\*\*|__.*?__", content)),
            "questions": len(re.findall(r"\?", content)),
            "exclamations": len(re.findall(r"!", content)),
            "todos": len(re.findall(r"todo|TODO|fixme|FIXME", content, re.IGNORECASE)),
            "code_snippets": self._count_code_snippets(content),
            "technical_terms": self._count_technical_terms(content),
            "readability_score": self._calculate_readability_score(content),
        }

        # Structural analysis
        analysis["structure_quality"] = self._assess_structure_quality(content)
        analysis["completeness"] = self._assess_completeness(content)

        return analysis

    def _assess_complexity(self, content: str, analysis: dict[str, Any]) -> str:
        """Assess content complexity level."""
        content_lower = content.lower()

        # Check for complexity indicators
        complexity_scores = {"beginner": 0, "intermediate": 0, "expert": 0}

        for level, patterns in self.complexity_patterns.items():
            for pattern in patterns:
                complexity_scores[level] += content_lower.count(pattern)

        # Consider content metrics
        if analysis["word_count"] > 2000:
            complexity_scores["expert"] += 2
        elif analysis["word_count"] > 1000:
            complexity_scores["intermediate"] += 2
        else:
            complexity_scores["beginner"] += 1

        if analysis["code_blocks"] > 5:
            complexity_scores["expert"] += 2
        elif analysis["code_blocks"] > 2:
            complexity_scores["intermediate"] += 1

        if analysis["technical_terms"] > 10:
            complexity_scores["expert"] += 2
        elif analysis["technical_terms"] > 5:
            complexity_scores["intermediate"] += 1

        # Return highest scoring complexity
        return max(complexity_scores, key=lambda x: complexity_scores[x])

    def _assess_quality(
        self, content: str, analysis: dict[str, Any], metadata: KnowledgeMetadata
    ) -> str:
        """Assess content quality."""
        content_lower = content.lower()

        quality_scores = {"high": 0, "medium": 0, "low": 0}

        # Check quality indicators in content
        for level, patterns in self.quality_indicators.items():
            for pattern in patterns:
                quality_scores[level] += content_lower.count(pattern)

        # Consider content completeness
        if analysis["completeness"] > 0.8:
            quality_scores["high"] += 3
        elif analysis["completeness"] > 0.6:
            quality_scores["medium"] += 2
        else:
            quality_scores["low"] += 1

        # Consider structure quality
        if analysis["structure_quality"] > 0.8:
            quality_scores["high"] += 2
        elif analysis["structure_quality"] > 0.6:
            quality_scores["medium"] += 1

        # Consider metadata completeness
        if metadata.tags and len(metadata.tags) >= 3:
            quality_scores["high"] += 1

        if metadata.purpose:
            quality_scores["high"] += 1

        # Check for TODOs (indicates incomplete work)
        if analysis["todos"] > 0:
            quality_scores["low"] += analysis["todos"]

        # Return highest scoring quality, with preference for higher quality
        max_score = max(quality_scores.values())
        if quality_scores["high"] == max_score:
            return "high"
        elif quality_scores["medium"] == max_score:
            return "medium"
        else:
            return "low"

    def _estimate_success_rate(
        self, content: str, analysis: dict[str, Any]
    ) -> int | None:
        """Estimate success rate based on content analysis."""
        content_lower = content.lower()

        success_indicators = {"positive": 0, "negative": 0}

        # Check for success/failure patterns
        for level, patterns in self.success_patterns.items():
            for pattern in patterns:
                count = content_lower.count(pattern)
                if level == "high_success":
                    success_indicators["positive"] += count * 3
                elif level == "medium_success":
                    success_indicators["positive"] += count * 2
                elif level == "low_success":
                    success_indicators["negative"] += count * 2

        # Check for test results, metrics, etc.
        test_passes = len(re.findall(r"test.*pass|passed|success", content_lower))
        test_fails = len(re.findall(r"test.*fail|failed|error", content_lower))

        success_indicators["positive"] += test_passes * 2
        success_indicators["negative"] += test_fails

        # Calculate success rate
        total_indicators = (
            success_indicators["positive"] + success_indicators["negative"]
        )
        if total_indicators == 0:
            return None

        success_rate = (success_indicators["positive"] / total_indicators) * 100

        # Clamp between 0 and 100
        return max(0, min(100, int(success_rate)))

    def _infer_enhanced_tags(
        self, content: str, analysis: dict[str, Any], file_path: Path
    ) -> list[str]:
        """Infer enhanced tags from content analysis."""
        tags = []
        content_lower = content.lower()

        # Technology tags
        tech_patterns = {
            "python": [
                "python",
                "pip",
                "conda",
                "pytest",
                "flask",
                "django",
                "pandas",
                "numpy",
            ],
            "javascript": [
                "javascript",
                "js",
                "node",
                "npm",
                "react",
                "vue",
                "angular",
                "express",
            ],
            "typescript": ["typescript", "ts", "tsx", "interface", "type"],
            "web": ["html", "css", "web", "browser", "frontend", "backend"],
            "api": ["api", "rest", "graphql", "endpoint", "swagger"],
            "database": ["sql", "database", "mongodb", "postgresql", "mysql"],
            "cloud": ["aws", "azure", "gcp", "docker", "kubernetes", "serverless"],
            "ai": ["ai", "machine learning", "ml", "neural", "model", "training"],
            "data": ["data", "analytics", "visualization", "pandas", "numpy"],
        }

        for tag, patterns in tech_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                tags.append(tag)

        # Methodology tags
        methodology_patterns = {
            "testing": ["test", "unittest", "pytest", "jest", "testing"],
            "debugging": ["debug", "troubleshoot", "fix", "error", "bug"],
            "optimization": ["optimize", "performance", "speed", "efficiency"],
            "security": ["security", "auth", "encryption", "secure", "vulnerability"],
            "documentation": ["document", "readme", "guide", "tutorial", "manual"],
        }

        for tag, patterns in methodology_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                tags.append(tag)

        # Content type tags
        if analysis["code_blocks"] > 3:
            tags.append("code-heavy")

        if analysis["links"] > 5:
            tags.append("resource-rich")

        if analysis["word_count"] > 2000:
            tags.append("comprehensive")
        elif analysis["word_count"] < 300:
            tags.append("concise")

        # Complexity tags
        if analysis["technical_terms"] > 15:
            tags.append("technical")

        if analysis["readability_score"] < 0.3:
            tags.append("advanced")
        elif analysis["readability_score"] > 0.7:
            tags.append("beginner-friendly")

        return tags

    def _assess_confidence(
        self, content: str, analysis: dict[str, Any], metadata: KnowledgeMetadata
    ) -> str:
        """Assess confidence level in the content."""
        confidence_score = 0

        # High confidence indicators
        if metadata.success_rate and metadata.success_rate > 80:
            confidence_score += 3

        if analysis["structure_quality"] > 0.8:
            confidence_score += 2

        if analysis["completeness"] > 0.8:
            confidence_score += 2

        if analysis["code_blocks"] > 0 and "tested" in content.lower():
            confidence_score += 2

        # Medium confidence indicators
        if metadata.confidence == "high":
            confidence_score += 1

        if analysis["word_count"] > 500:
            confidence_score += 1

        # Low confidence indicators
        if analysis["todos"] > 0:
            confidence_score -= 2

        if "experimental" in content.lower():
            confidence_score -= 1

        if "untested" in content.lower():
            confidence_score -= 2

        # Convert to confidence level
        if confidence_score >= 6:
            return "high"
        elif confidence_score >= 3:
            return "medium"
        else:
            return "low"

    def _infer_purpose(
        self, content: str, analysis: dict[str, Any], file_path: Path
    ) -> str:
        """Infer the purpose of the content."""
        content_lower = content.lower()

        # Check for explicit purpose statements
        purpose_patterns = [
            r"purpose:?\s*(.+)",
            r"goal:?\s*(.+)",
            r"objective:?\s*(.+)",
            r"this\s+(?:document|file|guide)\s+(?:is|will|helps?)\s+(.+)",
        ]

        for pattern in purpose_patterns:
            match = re.search(pattern, content_lower)
            if match:
                return match.group(1).strip()[:100]  # First 100 chars

        # Infer from content type and structure
        if "tutorial" in content_lower or "guide" in content_lower:
            return "Educational guide for learning and implementation"

        if analysis["code_blocks"] > 3:
            return "Code examples and implementation reference"

        if "prompt" in str(file_path).lower():
            return "Prompt template for AI interactions"

        if "experiment" in content_lower:
            return "Experimental exploration and testing"

        if "project" in str(file_path).lower():
            return "Project documentation and management"

        return "Knowledge documentation and reference"

    def _infer_related_projects(self, content: str, file_path: Path) -> list[str]:
        """Infer related projects from content and file path."""
        projects = []

        # Extract project references from content
        project_patterns = [
            r"project:?\s*([a-zA-Z0-9_-]+)",
            r"related to:?\s*([a-zA-Z0-9_-]+)",
            r"\[\[([a-zA-Z0-9_-]+)\]\]",  # Wiki-style links
        ]

        for pattern in project_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            projects.extend(matches)

        # Infer from file path
        path_parts = file_path.parts
        for part in path_parts:
            if part.startswith("10_") or "project" in part.lower():
                # Extract project name
                project_name = part.replace("10_", "").replace("_", "-").lower()
                if project_name and project_name != "projects":
                    projects.append(project_name)

        return list(set(projects))

    def _count_code_snippets(self, content: str) -> int:
        """Count various types of code snippets."""
        # Code blocks
        code_blocks = len(re.findall(r"```[\s\S]*?```", content))

        # Inline code
        inline_code = len(re.findall(r"`[^`]+`", content))

        # Command line examples
        commands = len(re.findall(r"^\s*[$#]\s+", content, re.MULTILINE))

        return code_blocks + (inline_code // 3) + commands  # Weight code blocks more

    def _count_technical_terms(self, content: str) -> int:
        """Count technical terms and jargon."""
        technical_patterns = [
            r"\b(?:API|SDK|CLI|GUI|IDE|JSON|XML|HTTP|HTTPS|REST|GraphQL)\b",
            r"\b(?:function|method|class|object|variable|parameter|argument)\b",
            r"\b(?:database|server|client|frontend|backend|framework|library)\b",
            r"\b(?:algorithm|optimization|performance|scalability|architecture)\b",
        ]

        count = 0
        for pattern in technical_patterns:
            count += len(re.findall(pattern, content, re.IGNORECASE))

        return count

    def _calculate_readability_score(self, content: str) -> float:
        """Calculate a simple readability score (0-1, higher is more readable)."""
        sentences = len(re.findall(r"[.!?]+", content))
        words = len(content.split())

        if sentences == 0 or words == 0:
            return 0.5

        avg_sentence_length = words / sentences

        # Simple heuristic: shorter sentences are more readable
        # Optimal range is 15-20 words per sentence
        if 15 <= avg_sentence_length <= 20:
            readability = 1.0
        elif avg_sentence_length < 15:
            readability = 0.8 + (avg_sentence_length / 15) * 0.2
        else:
            readability = max(0.2, 1.0 - ((avg_sentence_length - 20) / 30))

        return min(1.0, max(0.0, readability))

    def _assess_structure_quality(self, content: str) -> float:
        """Assess the structural quality of the content (0-1)."""
        score = 0.0

        # Check for proper heading structure
        headings = re.findall(r"^(#+)\s+(.+)$", content, re.MULTILINE)
        if headings:
            score += 0.2

            # Check heading hierarchy
            heading_levels = [len(h[0]) for h in headings]
            if len(set(heading_levels)) > 1:  # Multiple heading levels
                score += 0.1

        # Check for introduction (content before first heading)
        first_heading_pos = content.find("\n#")
        if first_heading_pos > 100:  # At least 100 chars before first heading
            score += 0.2

        # Check for lists and structure
        if re.search(r"^\s*[-*+]\s", content, re.MULTILINE):
            score += 0.1

        if re.search(r"^\s*\d+\.\s", content, re.MULTILINE):
            score += 0.1

        # Check for code blocks with syntax highlighting
        code_blocks = re.findall(r"```(\w+)", content)
        if code_blocks:
            score += 0.2

        # Check for links and references
        if re.search(r"\[.*?\]\(.*?\)", content):
            score += 0.1

        return min(1.0, score)

    def _assess_completeness(self, content: str) -> float:
        """Assess content completeness (0-1)."""
        score = 0.0

        # Check for common incomplete markers
        incomplete_markers = ["todo", "fixme", "wip", "placeholder", "coming soon"]
        incomplete_count = sum(
            content.lower().count(marker) for marker in incomplete_markers
        )

        if incomplete_count == 0:
            score += 0.3
        else:
            score += max(0, 0.3 - (incomplete_count * 0.1))

        # Check for conclusion or summary
        if re.search(r"conclusion|summary|wrap.?up|in summary", content, re.IGNORECASE):
            score += 0.2

        # Check word count (longer content is often more complete)
        word_count = len(content.split())
        if word_count > 1000:
            score += 0.3
        elif word_count > 500:
            score += 0.2
        elif word_count > 200:
            score += 0.1

        # Check for examples
        if re.search(r"example|for instance|such as", content, re.IGNORECASE):
            score += 0.2

        return min(1.0, score)


def enhance_file_metadata(file_path: Path, config: CKCConfig) -> KnowledgeMetadata:
    """Convenience function to enhance a single file's metadata."""
    enhancer = AdvancedMetadataEnhancer(config)
    return enhancer.enhance_metadata(file_path)
