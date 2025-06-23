"""Tag standards and best practices for pure tag-centered system."""

from dataclasses import dataclass
from typing import Any


@dataclass
class TagStandard:
    """Standard tag definition with validation rules."""

    name: str
    description: str
    valid_values: list[str]
    required: bool = False
    max_selections: int = 10  # Maximum number of values that can be selected


class TagStandardsManager:
    """Manages tag standards and validation for pure tag-centered system."""

    def __init__(self) -> None:
        self.standards = self._initialize_standards()

    def _initialize_standards(self) -> dict[str, TagStandard]:
        """Initialize standard tag definitions."""
        return {
            # === 必須分類タグ ===
            "type": TagStandard(
                name="type",
                description="Content type classification",
                valid_values=["prompt", "code", "concept", "resource"],
                required=True,
                max_selections=1,
            ),
            "status": TagStandard(
                name="status",
                description="Development/lifecycle status",
                valid_values=["draft", "tested", "production", "deprecated"],
                required=True,
                max_selections=1,
            ),
            # === 技術スタック ===
            "tech": TagStandard(
                name="tech",
                description="Technology stack and tools",
                valid_values=[
                    # Languages
                    "python",
                    "javascript",
                    "typescript",
                    "rust",
                    "go",
                    "java",
                    "cpp",
                    "csharp",
                    "html",
                    "css",
                    "sql",
                    "bash",
                    "powershell",
                    # Frameworks & Libraries
                    "react",
                    "vue",
                    "angular",
                    "nodejs",
                    "express",
                    "fastapi",
                    "django",
                    "flask",
                    "pytorch",
                    "tensorflow",
                    "pandas",
                    "numpy",
                    "scikit-learn",
                    # Tools & Platforms
                    "docker",
                    "kubernetes",
                    "terraform",
                    "aws",
                    "gcp",
                    "azure",
                    "git",
                    "github",
                    "gitlab",
                    "jenkins",
                    "cicd",
                    "postgres",
                    "mysql",
                    "mongodb",
                    "redis",
                    "elasticsearch",
                    # Development Tools
                    "vscode",
                    "vim",
                    "neovim",
                    "intellij",
                    "pycharm",
                    "jupyter",
                    "colab",
                    "streamlit",
                    "gradio",
                ],
                required=False,
                max_selections=5,
            ),
            # === ドメイン領域 ===
            "domain": TagStandard(
                name="domain",
                description="Knowledge domain and application area",
                valid_values=[
                    # Development Areas
                    "web-dev",
                    "mobile-dev",
                    "desktop-dev",
                    "game-dev",
                    "backend",
                    "frontend",
                    "fullstack",
                    "devops",
                    "sre",
                    # Data & AI
                    "data-science",
                    "machine-learning",
                    "deep-learning",
                    "nlp",
                    "computer-vision",
                    "data-engineering",
                    "analytics",
                    "visualization",
                    # Specialized Domains
                    "cybersecurity",
                    "blockchain",
                    "iot",
                    "embedded",
                    "robotics",
                    "fintech",
                    "healthtech",
                    "edtech",
                    "e-commerce",
                    # Software Engineering
                    "architecture",
                    "design-patterns",
                    "testing",
                    "performance",
                    "scalability",
                    "reliability",
                    "monitoring",
                    "automation",
                    # Business & Process
                    "product-management",
                    "project-management",
                    "agile",
                    "scrum",
                    "documentation",
                    "communication",
                    "leadership",
                ],
                required=False,
                max_selections=3,
            ),
            # === チーム・役割 ===
            "team": TagStandard(
                name="team",
                description="Team role and responsibility area",
                valid_values=[
                    "frontend",
                    "backend",
                    "fullstack",
                    "mobile",
                    "devops",
                    "sre",
                    "data",
                    "ml",
                    "ai",
                    "research",
                    "security",
                    "qa",
                    "testing",
                    "design",
                    "ux",
                    "ui",
                    "product",
                    "management",
                    "leadership",
                ],
                required=False,
                max_selections=2,
            ),
            # === 品質指標 ===
            "complexity": TagStandard(
                name="complexity",
                description="Complexity level for learning and implementation",
                valid_values=["beginner", "intermediate", "advanced", "expert"],
                required=False,
                max_selections=1,
            ),
            "confidence": TagStandard(
                name="confidence",
                description="Confidence level in the content accuracy",
                valid_values=["low", "medium", "high"],
                required=False,
                max_selections=1,
            ),
            # === Claude特化メタデータ ===
            "claude_model": TagStandard(
                name="claude_model",
                description="Claude models that work well with this content",
                valid_values=["opus", "sonnet", "haiku", "sonnet-4"],
                required=False,
                max_selections=3,
            ),
            "claude_feature": TagStandard(
                name="claude_feature",
                description="Claude capabilities and use cases",
                valid_values=[
                    "code-generation",
                    "code-review",
                    "debugging",
                    "refactoring",
                    "analysis",
                    "research",
                    "documentation",
                    "explanation",
                    "creative",
                    "brainstorming",
                    "problem-solving",
                    "optimization",
                    "testing",
                    "architecture",
                    "design",
                ],
                required=False,
                max_selections=3,
            ),
        }

    def validate_tags(self, tag_type: str, values: list[str]) -> tuple[bool, list[str]]:
        """Validate tag values against standards.

        Args:
            tag_type: Type of tag (e.g., 'tech', 'domain')
            values: List of tag values to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if tag_type not in self.standards:
            return True, []  # Allow unknown tag types for extensibility

        standard = self.standards[tag_type]

        # Check if required field is missing
        if standard.required and not values:
            errors.append(f"Required tag '{tag_type}' is missing")
            return False, errors

        # Check maximum selections
        if len(values) > standard.max_selections:
            errors.append(
                (
                    f"Too many values for '{tag_type}' "
                    f"(max: {standard.max_selections}, got: {len(values)})"
                )
            )

        # Validate individual values
        for value in values:
            if value not in standard.valid_values:
                errors.append(
                    (
                        f"Invalid value '{value}' for tag '{tag_type}'. "
                        f"Valid values: {standard.valid_values[:10]}..."
                    )
                )

        return len(errors) == 0, errors

    def suggest_tags(
        self, content: str, existing_tags: dict[str, list[str]]
    ) -> dict[str, list[str]]:
        """Suggest additional tags based on content analysis.

        Args:
            content: Text content to analyze
            existing_tags: Currently assigned tags

        Returns:
            Dictionary of suggested tags by type
        """
        suggestions = {}
        content_lower = content.lower()

        # Tech stack suggestions
        if "tech" not in existing_tags or not existing_tags["tech"]:
            tech_suggestions = []
            for tech in self.standards["tech"].valid_values:
                if tech in content_lower and tech not in existing_tags.get("tech", []):
                    tech_suggestions.append(tech)
            if tech_suggestions:
                suggestions["tech"] = tech_suggestions[:3]  # Limit to top 3

        # Domain suggestions
        if "domain" not in existing_tags or not existing_tags["domain"]:
            domain_suggestions = []
            for domain in self.standards["domain"].valid_values:
                domain_keywords = domain.split("-")
                if any(keyword in content_lower for keyword in domain_keywords):
                    if domain not in existing_tags.get("domain", []):
                        domain_suggestions.append(domain)
            if domain_suggestions:
                suggestions["domain"] = domain_suggestions[:2]  # Limit to top 2

        # Claude feature suggestions
        if "claude_feature" not in existing_tags or not existing_tags["claude_feature"]:
            feature_patterns = {
                "code-generation": ["generate", "create", "build", "implement"],
                "analysis": ["analyze", "review", "examine", "evaluate"],
                "debugging": ["debug", "error", "fix", "troubleshoot"],
                "documentation": ["document", "readme", "guide", "explanation"],
                "optimization": ["optimize", "improve", "enhance", "performance"],
            }

            feature_suggestions = []
            for feature, patterns in feature_patterns.items():
                if any(pattern in content_lower for pattern in patterns):
                    if feature not in existing_tags.get("claude_feature", []):
                        feature_suggestions.append(feature)

            if feature_suggestions:
                suggestions["claude_feature"] = feature_suggestions[:2]

        return suggestions

    def get_tag_recommendations(
        self, tag_type: str, partial_value: str = ""
    ) -> list[str]:
        """Get tag recommendations for autocomplete.

        Args:
            tag_type: Type of tag to get recommendations for
            partial_value: Partial value for filtering

        Returns:
            List of recommended tag values
        """
        if tag_type not in self.standards:
            return []

        valid_values = self.standards[tag_type].valid_values

        if not partial_value:
            return valid_values[:10]  # Return first 10 for display

        # Filter by partial match
        matches = [
            value for value in valid_values if partial_value.lower() in value.lower()
        ]
        return matches[:10]  # Limit to 10 results

    def validate_metadata_tags(
        self, metadata_dict: dict[str, Any]
    ) -> tuple[bool, list[str]]:
        """Validate all tags in metadata dictionary.

        Args:
            metadata_dict: Dictionary containing metadata fields

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        all_errors = []
        is_valid = True

        for tag_type, standard in self.standards.items():
            if tag_type in metadata_dict:
                values = metadata_dict[tag_type]
                # Ensure it's a list
                if not isinstance(values, list):
                    values = [values] if values else []

                valid, errors = self.validate_tags(tag_type, values)
                if not valid:
                    is_valid = False
                    all_errors.extend(errors)

        return is_valid, all_errors

    def get_tag_statistics(
        self, metadata_list: list[dict[str, Any]]
    ) -> dict[str, dict[str, int]]:
        """Generate statistics about tag usage.

        Args:
            metadata_list: List of metadata dictionaries

        Returns:
            Statistics dictionary by tag type
        """
        stats: dict[str, dict[str, int]] = {}

        for tag_type in self.standards.keys():
            stats[tag_type] = {}

            for metadata in metadata_list:
                values = metadata.get(tag_type, [])
                if not isinstance(values, list):
                    values = [values] if values else []

                for value in values:
                    if value:  # Skip empty values
                        stats[tag_type][value] = stats[tag_type].get(value, 0) + 1

        return stats

    def export_standards_as_markdown(self) -> str:
        """Export tag standards as markdown documentation.

        Returns:
            Markdown formatted documentation
        """
        lines = [
            "# Pure Tag-Centered System: Tag Standards",
            "",
            (
                "This document defines the standardized tag system for the "
                "revolutionary tag-centered knowledge management approach."
            ),
            "",
            "## Core Principles",
            "",
            (
                "1. **State-based Classification**: Files are organized by status "
                "(draft/tested/production/deprecated) rather than content type"
            ),
            "2. **Multi-layered Tags**: Rich metadata through multiple tag dimensions",
            (
                "3. **Cognitive Load Reduction**: No complex directory hierarchies "
                "to navigate"
            ),
            "4. **Dynamic Organization**: Tags enable flexible views and queries",
            "",
            "## Tag Categories",
            "",
        ]

        for tag_type, standard in self.standards.items():
            lines.append(f"### {tag_type.title()}")
            lines.append("")
            lines.append(f"**Description**: {standard.description}")
            lines.append(f"**Required**: {'Yes' if standard.required else 'No'}")
            lines.append(f"**Max Selections**: {standard.max_selections}")
            lines.append("")
            lines.append("**Valid Values**:")
            for value in standard.valid_values:
                lines.append(f"- `{value}`")
            lines.append("")

        lines.extend(
            [
                "## Usage Examples",
                "",
                "### Example 1: Python API Documentation",
                "```yaml",
                "type: concept",
                "status: production",
                "tech: [python, fastapi]",
                "domain: [web-dev, backend]",
                "team: [backend]",
                "complexity: intermediate",
                "confidence: high",
                "```",
                "",
                "### Example 2: React Component Prompt",
                "```yaml",
                "type: prompt",
                "status: tested",
                "tech: [react, typescript]",
                "domain: [web-dev, frontend]",
                "team: [frontend]",
                "claude_feature: [code-generation]",
                "complexity: beginner",
                "```",
                "",
                "### Example 3: Machine Learning Research",
                "```yaml",
                "type: concept",
                "status: draft",
                "tech: [python, pytorch]",
                "domain: [machine-learning, research]",
                "team: [ml, research]",
                "complexity: expert",
                "confidence: medium",
                "```",
            ]
        )

        return "\n".join(lines)
