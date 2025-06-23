"""AI assistance functionality for CKC."""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from ..automation.metadata_enhancer import AdvancedMetadataEnhancer
from ..core.config import CKCConfig
from ..core.metadata import KnowledgeMetadata, MetadataManager


class AIKnowledgeAssistant:
    """AI-powered knowledge management assistant."""

    def __init__(self, vault_path: Path, config: CKCConfig):
        self.vault_path = vault_path
        self.config = config
        self.metadata_manager = MetadataManager()
        self.metadata_enhancer = AdvancedMetadataEnhancer(config)

        # AI assistance settings
        self.ai_dir = vault_path / ".ckc" / "ai_assistance"
        self.ai_dir.mkdir(parents=True, exist_ok=True)

        # Knowledge patterns and templates
        self.knowledge_patterns = self._load_knowledge_patterns()
        self.suggestion_cache = {}

    def suggest_content_improvements(self, file_path: Path) -> dict[str, Any]:
        """Suggest improvements for existing content."""
        if not file_path.exists():
            return {"error": "File not found"}

        content = file_path.read_text(encoding="utf-8")
        metadata = self.metadata_manager.extract_metadata_from_file(file_path)

        suggestions = {
            "file_path": str(file_path),
            "timestamp": datetime.now().isoformat(),
            "suggestions": [],
        }

        # Content structure suggestions
        structure_suggestions = self._analyze_content_structure(content)
        suggestions["suggestions"].extend(structure_suggestions)

        # Metadata enhancement suggestions
        metadata_suggestions = self._suggest_metadata_improvements(metadata, content)
        suggestions["suggestions"].extend(metadata_suggestions)

        # Content quality suggestions
        quality_suggestions = self._suggest_quality_improvements(content, metadata)
        suggestions["suggestions"].extend(quality_suggestions)

        # Related content suggestions
        related_suggestions = self._suggest_related_content(content, metadata)
        suggestions["suggestions"].extend(related_suggestions)

        return suggestions

    def suggest_knowledge_organization(self) -> dict[str, Any]:
        """Suggest improvements to overall knowledge organization."""
        suggestions = {
            "timestamp": datetime.now().isoformat(),
            "organization_suggestions": [],
        }

        # Analyze vault structure
        vault_analysis = self._analyze_vault_structure()

        # Suggest directory reorganization
        directory_suggestions = self._suggest_directory_improvements(vault_analysis)
        suggestions["organization_suggestions"].extend(directory_suggestions)

        # Suggest content consolidation
        consolidation_suggestions = self._suggest_content_consolidation(vault_analysis)
        suggestions["organization_suggestions"].extend(consolidation_suggestions)

        # Suggest knowledge gaps
        gap_suggestions = self._identify_knowledge_gaps(vault_analysis)
        suggestions["organization_suggestions"].extend(gap_suggestions)

        return suggestions

    def generate_content_template(
        self, content_type: str, context: dict | None = None
    ) -> str:
        """Generate intelligent content templates."""
        context = context or {}

        templates = {
            "prompt": self._generate_prompt_template(context),
            "code_snippet": self._generate_code_template(context),
            "concept": self._generate_concept_template(context),
            "project_log": self._generate_project_log_template(context),
            "experiment": self._generate_experiment_template(context),
            "resource": self._generate_resource_template(context),
        }

        return templates.get(
            content_type, self._generate_generic_template(content_type, context)
        )

    def suggest_tags_and_categories(
        self, content: str, existing_metadata: KnowledgeMetadata | None = None
    ) -> dict[str, list[str]]:
        """Suggest intelligent tags and categories for content."""
        suggestions = {"tags": [], "categories": [], "confidence_scores": {}}

        # Use enhanced metadata analysis
        if existing_metadata:
            enhanced_metadata = self.metadata_enhancer.enhance_metadata(
                Path("temp"), content
            )

            # Extract suggested tags from enhancement
            suggested_tags = [
                tag
                for tag in enhanced_metadata.tags
                if tag not in (existing_metadata.tags if existing_metadata else [])
            ]
            suggestions["tags"] = suggested_tags[:10]  # Top 10 suggestions

        # Category suggestions based on content analysis
        category_suggestions = self._suggest_categories(content)
        suggestions["categories"] = category_suggestions

        # Calculate confidence scores
        suggestions["confidence_scores"] = self._calculate_suggestion_confidence(
            content, suggestions
        )

        return suggestions

    def provide_content_insights(self, file_path: Path) -> dict[str, Any]:
        """Provide AI-powered insights about content."""
        if not file_path.exists():
            return {"error": "File not found"}

        content = file_path.read_text(encoding="utf-8")
        metadata = self.metadata_manager.extract_metadata_from_file(file_path)

        insights = {
            "file_path": str(file_path),
            "analysis_timestamp": datetime.now().isoformat(),
            "content_analysis": {},
            "knowledge_connections": {},
            "improvement_potential": {},
            "usage_predictions": {},
        }

        # Deep content analysis
        insights["content_analysis"] = self._analyze_content_deeply(content, metadata)

        # Knowledge network analysis
        insights["knowledge_connections"] = self._analyze_knowledge_connections(
            content, metadata
        )

        # Improvement potential assessment
        insights["improvement_potential"] = self._assess_improvement_potential(
            content, metadata
        )

        # Usage prediction
        insights["usage_predictions"] = self._predict_content_usage(content, metadata)

        return insights

    def _analyze_content_structure(self, content: str) -> list[dict[str, str]]:
        """Analyze content structure and suggest improvements."""
        suggestions = []

        # Check for headings
        headings = re.findall(r"^(#+)\s+(.+)$", content, re.MULTILINE)
        if not headings:
            suggestions.append(
                {
                    "type": "structure",
                    "priority": "medium",
                    "suggestion": "Add headings to improve content structure",
                    "action": "Consider adding # Main Heading and ## Sub Headings",
                }
            )

        # Check for introduction
        lines = content.split("\n")
        first_content_line = None
        for line in lines:
            if line.strip() and not line.startswith("---") and not line.startswith("#"):
                first_content_line = line
                break

        if not first_content_line or len(first_content_line) < 50:
            suggestions.append(
                {
                    "type": "structure",
                    "priority": "medium",
                    "suggestion": "Add introduction to explain content purpose",
                    "action": "Write 1-2 sentences explaining what this content covers",
                }
            )

        # Check for examples
        if "example" not in content.lower() and "```" not in content:
            suggestions.append(
                {
                    "type": "content",
                    "priority": "low",
                    "suggestion": "Consider adding examples to illustrate key concepts",
                    "action": "Add code examples or practical illustrations",
                }
            )

        # Check for conclusion
        if "conclusion" not in content.lower() and "summary" not in content.lower():
            suggestions.append(
                {
                    "type": "structure",
                    "priority": "low",
                    "suggestion": "Consider adding a conclusion or summary section",
                    "action": "Summarize key takeaways at the end",
                }
            )

        return suggestions

    def _suggest_metadata_improvements(
        self, metadata: KnowledgeMetadata, content: str
    ) -> list[dict[str, str]]:
        """Suggest metadata improvements."""
        suggestions = []

        # Check title quality
        if not metadata.title or metadata.title == "Untitled":
            suggestions.append(
                {
                    "type": "metadata",
                    "priority": "high",
                    "suggestion": "Add a descriptive title",
                    "action": "Create title that clearly describes the content purpose",
                }
            )

        # Check tag sufficiency
        if len(metadata.tags) < 3:
            suggestions.append(
                {
                    "type": "metadata",
                    "priority": "medium",
                    "suggestion": "Add more tags for better discoverability",
                    "action": (
                        f"Current tags: {metadata.tags}. "
                        "Consider adding 2-3 more relevant tags"
                    ),
                }
            )

        # Check content type assignment (pure tag system)
        if not metadata.type or metadata.type == "prompt":
            suggested_type = self._suggest_content_types(content)
            if suggested_type:
                suggestions.append(
                    {
                        "type": "metadata",
                        "priority": "medium",
                        "suggestion": f"Assign content type: {suggested_type[0]}",
                        "action": (
                            f"Add type: {suggested_type[0]} "
                            "based on content analysis"
                        ),
                    }
                )

        # Check purpose definition
        if not metadata.purpose:
            suggestions.append(
                {
                    "type": "metadata",
                    "priority": "low",
                    "suggestion": "Define the purpose of this content",
                    "action": "Add 1-2 sentences explaining why this content exists",
                }
            )

        return suggestions

    def _suggest_quality_improvements(
        self, content: str, metadata: KnowledgeMetadata
    ) -> list[dict[str, str]]:
        """Suggest quality improvements."""
        suggestions = []

        # Check for TODO items
        todo_count = len(re.findall(r"todo|TODO|fixme|FIXME", content, re.IGNORECASE))
        if todo_count > 0:
            suggestions.append(
                {
                    "type": "quality",
                    "priority": "medium",
                    "suggestion": f"Complete {todo_count} pending TODO items",
                    "action": "Review and address outstanding TODO/FIXME items",
                }
            )

        # Check content length
        word_count = len(content.split())
        if word_count < 100:
            suggestions.append(
                {
                    "type": "quality",
                    "priority": "medium",
                    "suggestion": "Expand content for better comprehensiveness",
                    "action": (
                        "Current content is quite brief. "
                        "Consider adding more detail and context"
                    ),
                }
            )
        elif word_count > 2000:
            suggestions.append(
                {
                    "type": "quality",
                    "priority": "low",
                    "suggestion": "Consider breaking into smaller, focused pieces",
                    "action": (
                        "Content is extensive. "
                        "Consider splitting into multiple focused documents"
                    ),
                }
            )

        # Check for broken links (basic check)
        broken_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
        if broken_links:
            suggestions.append(
                {
                    "type": "quality",
                    "priority": "low",
                    "suggestion": "Verify external links are working",
                    "action": f"Check {len(broken_links)} links for accessibility",
                }
            )

        return suggestions

    def _suggest_related_content(
        self, content: str, metadata: KnowledgeMetadata
    ) -> list[dict[str, str]]:
        """Suggest related content connections."""
        suggestions = []

        # Find similar content by tags
        similar_files = self._find_similar_content(metadata.tags)
        if similar_files:
            suggestions.append(
                {
                    "type": "connection",
                    "priority": "low",
                    "suggestion": (
                        f"Consider linking to {len(similar_files)} related files"
                    ),
                    "action": f"Related content: {', '.join(similar_files[:3])}",
                }
            )

        # Suggest cross-references
        potential_references = self._identify_potential_references(content)
        if potential_references:
            suggestions.append(
                {
                    "type": "connection",
                    "priority": "low",
                    "suggestion": "Add cross-references to related concepts",
                    "action": (
                        f"Consider referencing: {', '.join(potential_references[:3])}"
                    ),
                }
            )

        return suggestions

    def _analyze_vault_structure(self) -> dict[str, Any]:
        """Analyze overall vault structure."""
        analysis = {
            "total_files": 0,
            "directory_distribution": {},
            "tag_usage": {},
            "category_distribution": {},
            "orphaned_files": [],
            "duplicate_content": [],
        }

        # Scan all markdown files
        md_files = list(self.vault_path.rglob("*.md"))
        analysis["total_files"] = len(md_files)

        for md_file in md_files:
            if md_file.name == "README.md":
                continue

            try:
                # Directory distribution
                relative_path = md_file.relative_to(self.vault_path)
                main_dir = (
                    str(relative_path.parts[0]) if relative_path.parts else "root"
                )
                analysis["directory_distribution"][main_dir] = (
                    analysis["directory_distribution"].get(main_dir, 0) + 1
                )

                # Extract metadata
                metadata = self.metadata_manager.extract_metadata_from_file(md_file)

                # Tag usage
                for tag in metadata.tags:
                    analysis["tag_usage"][tag] = analysis["tag_usage"].get(tag, 0) + 1

                # Category distribution
                if metadata.type:
                    analysis["type_distribution"][metadata.type] = (
                        analysis["type_distribution"].get(metadata.type, 0) + 1
                    )

                # Check for orphaned files (no tags, no type)
                if not metadata.tags and not metadata.type:
                    analysis["orphaned_files"].append(str(md_file))

            except Exception:
                continue

        return analysis

    def _suggest_directory_improvements(
        self, vault_analysis: dict[str, Any]
    ) -> list[dict[str, str]]:
        """Suggest directory structure improvements."""
        suggestions = []

        # Check for unbalanced directories
        dir_dist = vault_analysis["directory_distribution"]
        if dir_dist:
            max_files = max(dir_dist.values())
            min_files = min(dir_dist.values())

            if max_files > min_files * 5:  # Significant imbalance
                overloaded_dirs = [
                    d for d, count in dir_dist.items() if count == max_files
                ]
                suggestions.append(
                    {
                        "type": "organization",
                        "priority": "medium",
                        "suggestion": (
                            f"Directory '{overloaded_dirs[0]}' has too many files "
                            f"({max_files})"
                        ),
                        "action": (
                            "Consider creating subdirectories to better "
                            "organize content"
                        ),
                    }
                )

        # Check for orphaned files
        orphaned_count = len(vault_analysis["orphaned_files"])
        if orphaned_count > 0:
            suggestions.append(
                {
                    "type": "organization",
                    "priority": "high",
                    "suggestion": f"{orphaned_count} files lack proper organization",
                    "action": (
                        "Add tags and categories to orphaned files for "
                        "better organization"
                    ),
                }
            )

        return suggestions

    def _suggest_content_consolidation(
        self, vault_analysis: dict[str, Any]
    ) -> list[dict[str, str]]:
        """Suggest content consolidation opportunities."""
        suggestions = []

        # Check for duplicate or similar tags
        tag_usage = vault_analysis["tag_usage"]
        similar_tags = self._find_similar_tags(list(tag_usage.keys()))

        if similar_tags:
            suggestions.append(
                {
                    "type": "consolidation",
                    "priority": "low",
                    "suggestion": (
                        f"Consider consolidating similar tags: {similar_tags[:3]}"
                    ),
                    "action": "Review tag taxonomy and merge similar concepts",
                }
            )

        # Check for underused categories
        cat_dist = vault_analysis["category_distribution"]
        underused_categories = [cat for cat, count in cat_dist.items() if count < 2]

        if underused_categories:
            suggestions.append(
                {
                    "type": "consolidation",
                    "priority": "low",
                    "suggestion": (
                        f"Categories with only 1 file: {underused_categories[:3]}"
                    ),
                    "action": (
                        "Consider merging underused categories or expanding content"
                    ),
                }
            )

        return suggestions

    def _identify_knowledge_gaps(
        self, vault_analysis: dict[str, Any]
    ) -> list[dict[str, str]]:
        """Identify potential knowledge gaps."""
        suggestions = []

        # Check for missing fundamental concepts
        common_concepts = [
            "documentation",
            "best-practices",
            "troubleshooting",
            "getting-started",
        ]
        existing_tags = set(vault_analysis["tag_usage"].keys())

        missing_concepts = [
            concept for concept in common_concepts if concept not in existing_tags
        ]
        if missing_concepts:
            suggestions.append(
                {
                    "type": "gap",
                    "priority": "medium",
                    "suggestion": (
                        f"Consider adding content for: {missing_concepts[:2]}"
                    ),
                    "action": "Create foundational content for common knowledge areas",
                }
            )

        # Check for unbalanced content types
        categories = vault_analysis["category_distribution"]
        if "prompt" in categories and "code" not in categories:
            suggestions.append(
                {
                    "type": "gap",
                    "priority": "low",
                    "suggestion": "Consider adding code examples to complement prompts",
                    "action": (
                        "Balance prompt content with practical code implementations"
                    ),
                }
            )

        return suggestions

    def _generate_prompt_template(self, context: dict) -> str:
        """Generate intelligent prompt template."""
        template = """---
title: "{title}"
category: "prompt"
tags: ["prompt", "ai", "{domain}"]
status: "draft"
quality: "experimental"
purpose: "Template for {purpose}"
created: "{timestamp}"
updated: "{timestamp}"
---

# {title}

## Purpose
{purpose_description}

## Context
{context_description}

## Prompt Template

```
{prompt_content}
```

## Usage Guidelines
- **When to use**: {usage_when}
- **Expected outcome**: {expected_outcome}
- **Customization points**: {customization_points}

## Examples

### Example 1: {example_title}
```
{example_prompt}
```

**Expected Response**: {example_response}

## Variations
{variations}

## Success Rate
- **Estimated success rate**: {success_rate}%
- **Confidence level**: {confidence}

## Related
- {related_content}

## Notes
{additional_notes}
"""

        # Fill in context-specific values
        filled_template = template.format(
            title=context.get("title", "New Prompt Template"),
            domain=context.get("domain", "general"),
            purpose=context.get("purpose", "AI interaction guidance"),
            purpose_description=context.get(
                "purpose_description", "Describe the specific purpose of this prompt"
            ),
            context_description=context.get(
                "context_description", "Describe when and why to use this prompt"
            ),
            timestamp=datetime.now().isoformat(),
            prompt_content=context.get(
                "prompt_content", "[Insert your prompt template here]"
            ),
            usage_when=context.get(
                "usage_when", "Specify conditions for using this prompt"
            ),
            expected_outcome=context.get(
                "expected_outcome", "Describe expected AI response"
            ),
            customization_points=context.get(
                "customization_points", "List parts that can be customized"
            ),
            example_title=context.get("example_title", "Basic Usage"),
            example_prompt=context.get("example_prompt", "[Example prompt usage]"),
            example_response=context.get(
                "example_response", "[Example expected response]"
            ),
            variations=context.get(
                "variations",
                "- Variation 1: [Description]\n- Variation 2: [Description]",
            ),
            success_rate=context.get("success_rate", "85"),
            confidence=context.get("confidence", "medium"),
            related_content=context.get(
                "related_content", "[[Link to related content]]"
            ),
            additional_notes=context.get(
                "additional_notes", "Any additional notes or considerations"
            ),
        )

        return filled_template

    def _generate_code_template(self, context: dict) -> str:
        """Generate code snippet template."""
        template = """---
title: "{title}"
category: "code"
tags: ["code", "{language}", "{domain}"]
status: "draft"
quality: "experimental"
purpose: "Code example for {purpose}"
created: "{timestamp}"
updated: "{timestamp}"
---

# {title}

## Overview
{overview}

## Code

```{language}
{code_content}
```

## Explanation
{explanation}

## Usage
{usage_instructions}

## Requirements
- {requirements}

## Examples
{examples}

## Notes
{notes}
"""

        return template.format(
            title=context.get("title", "New Code Snippet"),
            language=context.get("language", "python"),
            domain=context.get("domain", "general"),
            purpose=context.get("purpose", "code implementation"),
            timestamp=datetime.now().isoformat(),
            overview=context.get(
                "overview", "Brief description of what this code does"
            ),
            code_content=context.get("code_content", "# Insert your code here\npass"),
            explanation=context.get("explanation", "Detailed explanation of the code"),
            usage_instructions=context.get(
                "usage_instructions", "How to use this code"
            ),
            requirements=context.get(
                "requirements", "List dependencies and requirements"
            ),
            examples=context.get("examples", "Provide usage examples"),
            notes=context.get("notes", "Additional notes and considerations"),
        )

    def _generate_concept_template(self, context: dict) -> str:
        """Generate concept explanation template."""
        template = """---
title: "{title}"
category: "concept"
tags: ["concept", "{domain}"]
status: "draft"
quality: "experimental"
purpose: "Explain {concept_name}"
created: "{timestamp}"
updated: "{timestamp}"
---

# {title}

## Definition
{definition}

## Key Components
{key_components}

## How It Works
{how_it_works}

## Why It Matters
{importance}

## Examples
{examples}

## Common Misconceptions
{misconceptions}

## Related Concepts
{related_concepts}

## Further Reading
{further_reading}
"""

        return template.format(
            title=context.get("title", "New Concept"),
            domain=context.get("domain", "general"),
            concept_name=context.get("concept_name", "this concept"),
            timestamp=datetime.now().isoformat(),
            definition=context.get(
                "definition", "Clear, concise definition of the concept"
            ),
            key_components=context.get(
                "key_components", "List the main components or aspects"
            ),
            how_it_works=context.get(
                "how_it_works", "Explain the mechanism or process"
            ),
            importance=context.get(
                "importance", "Explain why this concept is important"
            ),
            examples=context.get("examples", "Provide concrete examples"),
            misconceptions=context.get(
                "misconceptions", "Address common misunderstandings"
            ),
            related_concepts=context.get(
                "related_concepts", "Link to related concepts"
            ),
            further_reading=context.get(
                "further_reading", "Suggest additional resources"
            ),
        )

    def _generate_project_log_template(self, context: dict) -> str:
        """Generate project log template."""
        template = """---
title: "{title}"
category: "project_log"
tags: ["project", "{project_name}"]
status: "active"
quality: "medium"
purpose: "Track progress for {project_name}"
created: "{timestamp}"
updated: "{timestamp}"
---

# {title}

## Project Overview
**Objective**: {objective}
**Status**: {status}
**Priority**: {priority}

## Progress Log

### {current_date}
- {progress_entry}

## Next Steps
- [ ] {next_step}

## Challenges & Solutions
{challenges}

## Resources
{resources}

## Notes
{notes}
"""

        return template.format(
            title=context.get("title", "Project Log"),
            project_name=context.get("project_name", "project"),
            timestamp=datetime.now().isoformat(),
            current_date=datetime.now().strftime("%Y-%m-%d"),
            objective=context.get("objective", "Define project objective"),
            status=context.get("status", "in_progress"),
            priority=context.get("priority", "medium"),
            progress_entry=context.get("progress_entry", "Record today's progress"),
            next_step=context.get("next_step", "Define next action item"),
            challenges=context.get("challenges", "Document challenges and solutions"),
            resources=context.get("resources", "List relevant resources"),
            notes=context.get("notes", "Additional notes and observations"),
        )

    def _generate_experiment_template(self, context: dict) -> str:
        """Generate experiment template."""
        template = """---
title: "{title}"
category: "experiment"
tags: ["experiment", "{domain}"]
status: "experimental"
quality: "experimental"
purpose: "Explore {hypothesis}"
created: "{timestamp}"
updated: "{timestamp}"
---

# {title}

## Hypothesis
{hypothesis}

## Methodology
{methodology}

## Results
{results}

## Analysis
{analysis}

## Conclusion
{conclusion}

## Next Steps
{next_steps}
"""

        return template.format(
            title=context.get("title", "New Experiment"),
            domain=context.get("domain", "general"),
            timestamp=datetime.now().isoformat(),
            hypothesis=context.get(
                "hypothesis", "State your hypothesis or research question"
            ),
            methodology=context.get("methodology", "Describe experimental approach"),
            results=context.get("results", "Record experimental results"),
            analysis=context.get("analysis", "Analyze the results"),
            conclusion=context.get("conclusion", "Draw conclusions"),
            next_steps=context.get("next_steps", "Plan follow-up experiments"),
        )

    def _generate_resource_template(self, context: dict) -> str:
        """Generate resource collection template."""
        template = """---
title: "{title}"
category: "resource"
tags: ["resource", "{domain}"]
status: "active"
quality: "medium"
purpose: "Curate resources for {topic}"
created: "{timestamp}"
updated: "{timestamp}"
---

# {title}

## Overview
{overview}

## Key Resources

### Documentation
- {doc_resource}

### Tools
- {tool_resource}

### Articles & Guides
- {article_resource}

### Videos & Tutorials
- {video_resource}

## Notes
{notes}
"""

        return template.format(
            title=context.get("title", "Resource Collection"),
            domain=context.get("domain", "general"),
            topic=context.get("topic", "topic"),
            timestamp=datetime.now().isoformat(),
            overview=context.get("overview", "Brief overview of resource collection"),
            doc_resource=context.get(
                "doc_resource", "[Resource Title](URL) - Description"
            ),
            tool_resource=context.get(
                "tool_resource", "[Tool Name](URL) - Description"
            ),
            article_resource=context.get(
                "article_resource", "[Article Title](URL) - Description"
            ),
            video_resource=context.get(
                "video_resource", "[Video Title](URL) - Description"
            ),
            notes=context.get("notes", "Additional notes about these resources"),
        )

    def _generate_generic_template(self, content_type: str, context: dict) -> str:
        """Generate generic template for unknown content types."""
        template = """---
title: "{title}"
category: "{category}"
tags: ["{category}"]
status: "draft"
quality: "experimental"
purpose: "{purpose}"
created: "{timestamp}"
updated: "{timestamp}"
---

# {title}

## Overview
{overview}

## Content
{content}

## Notes
{notes}
"""

        return template.format(
            title=context.get("title", f"New {content_type.title()}"),
            category=content_type,
            purpose=context.get("purpose", f"Document {content_type} information"),
            timestamp=datetime.now().isoformat(),
            overview=context.get("overview", f"Brief overview of this {content_type}"),
            content=context.get("content", f"Main {content_type} content goes here"),
            notes=context.get("notes", "Additional notes and observations"),
        )

    def _suggest_categories(self, content: str) -> list[str]:
        """Suggest categories based on content analysis."""
        content_lower = content.lower()

        category_patterns = {
            "prompt": ["prompt", "ai", "claude", "gpt", "llm"],
            "code": ["code", "function", "class", "import", "def", "```"],
            "concept": ["concept", "theory", "principle", "understand"],
            "project_log": ["project", "progress", "milestone", "deadline"],
            "experiment": ["experiment", "test", "hypothesis", "result"],
            "resource": ["resource", "link", "tool", "documentation", "guide"],
        }

        category_scores = {}
        for category, patterns in category_patterns.items():
            score = sum(content_lower.count(pattern) for pattern in patterns)
            if score > 0:
                category_scores[category] = score

        # Return top 3 suggestions
        sorted_categories = sorted(
            category_scores.items(), key=lambda x: x[1], reverse=True
        )
        return [cat for cat, _ in sorted_categories[:3]]

    def _calculate_suggestion_confidence(
        self, content: str, suggestions: dict
    ) -> dict[str, float]:
        """Calculate confidence scores for suggestions."""
        confidence_scores = {}

        # Simple confidence calculation based on content analysis
        word_count = len(content.split())

        for suggestion_type, items in suggestions.items():
            if items:
                base_confidence = min(
                    0.9, word_count / 1000
                )  # More content = higher confidence
                confidence_scores[suggestion_type] = base_confidence
            else:
                confidence_scores[suggestion_type] = 0.0

        return confidence_scores

    def _analyze_content_deeply(
        self, content: str, metadata: KnowledgeMetadata
    ) -> dict[str, Any]:
        """Perform deep content analysis."""
        analysis = {
            "readability": self._assess_readability(content),
            "technical_depth": self._assess_technical_depth(content),
            "completeness": self._assess_completeness(content),
            "actionability": self._assess_actionability(content),
            "uniqueness": self._assess_uniqueness(content),
        }

        return analysis

    def _analyze_knowledge_connections(
        self, content: str, metadata: KnowledgeMetadata
    ) -> dict[str, Any]:
        """Analyze connections to other knowledge."""
        connections = {
            "internal_links": len(re.findall(r"\[\[([^\]]+)\]\]", content)),
            "external_links": len(re.findall(r"\[([^\]]+)\]\(http[^)]+\)", content)),
            "tag_overlap": self._calculate_tag_overlap(metadata.tags),
            "concept_mentions": self._identify_concept_mentions(content),
        }

        return connections

    def _assess_improvement_potential(
        self, content: str, metadata: KnowledgeMetadata
    ) -> dict[str, Any]:
        """Assess potential for content improvement."""
        potential = {
            "structure_score": self._score_structure_quality(content),
            "metadata_score": self._score_metadata_quality(metadata),
            "content_score": self._score_content_quality(content),
            "overall_potential": "medium",  # Would be calculated from above scores
        }

        return potential

    def _predict_content_usage(
        self, content: str, metadata: KnowledgeMetadata
    ) -> dict[str, Any]:
        """Predict how content might be used."""
        predictions = {
            "likely_frequency": "medium",
            "target_audience": self._predict_audience(content),
            "usage_scenarios": self._predict_scenarios(content, metadata),
            "shelf_life": self._predict_shelf_life(content, metadata),
        }

        return predictions

    def _find_similar_content(self, tags: list[str]) -> list[str]:
        """Find content with similar tags."""
        similar_files = []

        # This would search through vault for files with overlapping tags
        # Simplified implementation for now
        if tags:
            # Search for files with any matching tags
            for md_file in self.vault_path.rglob("*.md"):
                if md_file.name != "README.md":
                    try:
                        file_metadata = (
                            self.metadata_manager.extract_metadata_from_file(md_file)
                        )
                        if any(tag in file_metadata.tags for tag in tags):
                            similar_files.append(md_file.name)
                    except Exception:
                        continue

        return similar_files[:10]  # Return top 10

    def _identify_potential_references(self, content: str) -> list[str]:
        """Identify potential cross-references in content."""
        # Look for concept keywords that might be linkable
        potential_refs = []

        concepts = [
            "authentication",
            "authorization",
            "api",
            "database",
            "framework",
            "algorithm",
            "pattern",
            "architecture",
            "security",
            "performance",
        ]

        content_lower = content.lower()
        for concept in concepts:
            if concept in content_lower:
                potential_refs.append(concept)

        return potential_refs[:5]

    def _find_similar_tags(self, tags: list[str]) -> list[str]:
        """Find similar or duplicate tags."""
        similar_groups = []

        for i, tag1 in enumerate(tags):
            for tag2 in tags[i + 1 :]:
                # Simple similarity check
                if self._tags_are_similar(tag1, tag2):
                    similar_groups.append(f"{tag1}/{tag2}")

        return similar_groups[:5]

    def _tags_are_similar(self, tag1: str, tag2: str) -> bool:
        """Check if two tags are similar."""
        # Simple similarity check
        return (
            tag1.lower() in tag2.lower()
            or tag2.lower() in tag1.lower()
            or self._levenshtein_distance(tag1.lower(), tag2.lower()) <= 2
        )

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def _load_knowledge_patterns(self) -> dict[str, Any]:
        """Load knowledge patterns from configuration."""
        patterns_file = self.ai_dir / "knowledge_patterns.json"

        default_patterns = {
            "content_types": [
                "prompt",
                "code",
                "concept",
                "project_log",
                "experiment",
                "resource",
            ],
            "quality_indicators": ["tested", "verified", "comprehensive", "validated"],
            "improvement_triggers": ["todo", "incomplete", "outdated", "unclear"],
        }

        if patterns_file.exists():
            try:
                with open(patterns_file, encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return default_patterns

        return default_patterns

    # Helper methods for analysis (simplified implementations)
    def _assess_readability(self, content: str) -> float:
        """Assess content readability (0-1)."""
        # Simplified readability assessment
        sentences = len(re.findall(r"[.!?]+", content))
        words = len(content.split())

        if sentences == 0 or words == 0:
            return 0.5

        avg_sentence_length = words / sentences
        return max(0.0, min(1.0, 1.0 - (avg_sentence_length - 15) / 30))

    def _assess_technical_depth(self, content: str) -> float:
        """Assess technical depth of content (0-1)."""
        technical_terms = [
            "algorithm",
            "architecture",
            "implementation",
            "optimization",
            "framework",
        ]
        code_blocks = len(re.findall(r"```", content))

        tech_score = sum(content.lower().count(term) for term in technical_terms)
        return min(1.0, (tech_score + code_blocks) / 10)

    def _assess_completeness(self, content: str) -> float:
        """Assess content completeness (0-1)."""
        word_count = len(content.split())
        has_conclusion = "conclusion" in content.lower() or "summary" in content.lower()
        has_examples = "example" in content.lower() or "```" in content

        completeness = (
            (word_count / 1000)
            + (0.2 if has_conclusion else 0)
            + (0.2 if has_examples else 0)
        )
        return min(1.0, completeness)

    def _assess_actionability(self, content: str) -> float:
        """Assess how actionable the content is (0-1)."""
        action_words = ["how to", "step", "guide", "tutorial", "implement", "create"]
        action_score = sum(content.lower().count(word) for word in action_words)

        return min(1.0, action_score / 5)

    def _assess_uniqueness(self, content: str) -> float:
        """Assess content uniqueness (0-1)."""
        # Simplified uniqueness assessment
        # In a real implementation, this would compare against existing content
        return 0.7  # Placeholder

    def _calculate_tag_overlap(self, tags: list[str]) -> float:
        """Calculate overlap with existing tags."""
        # Simplified implementation
        return len(set(tags)) / max(1, len(tags))

    def _identify_concept_mentions(self, content: str) -> list[str]:
        """Identify mentioned concepts."""
        concepts = ["api", "database", "security", "performance", "architecture"]
        mentioned = [concept for concept in concepts if concept in content.lower()]
        return mentioned

    def _score_structure_quality(self, content: str) -> float:
        """Score structural quality (0-1)."""
        headings = len(re.findall(r"^#+", content, re.MULTILINE))
        lists = len(re.findall(r"^[-*+]", content, re.MULTILINE))

        return min(1.0, (headings + lists) / 10)

    def _score_metadata_quality(self, metadata: KnowledgeMetadata) -> float:
        """Score metadata quality (0-1)."""
        score = 0
        if metadata.title and metadata.title != "Untitled":
            score += 0.2
        if metadata.tags:
            score += 0.2
        if metadata.type:
            score += 0.2
        if metadata.purpose:
            score += 0.2
        if metadata.confidence:
            score += 0.2

        return score

    def _score_content_quality(self, content: str) -> float:
        """Score overall content quality (0-1)."""
        word_count = len(content.split())
        has_structure = bool(re.search(r"^#+", content, re.MULTILINE))
        has_examples = "example" in content.lower()

        quality = 0
        if word_count > 100:
            quality += 0.3
        if has_structure:
            quality += 0.3
        if has_examples:
            quality += 0.4

        return quality

    def _predict_audience(self, content: str) -> str:
        """Predict target audience."""
        if "beginner" in content.lower() or "introduction" in content.lower():
            return "beginner"
        elif "advanced" in content.lower() or "expert" in content.lower():
            return "expert"
        else:
            return "intermediate"

    def _predict_scenarios(
        self, content: str, metadata: KnowledgeMetadata
    ) -> list[str]:
        """Predict usage scenarios."""
        scenarios = []

        if metadata.type == "prompt":
            scenarios.append("AI interaction guidance")
        elif metadata.type == "code":
            scenarios.append("Implementation reference")
        elif metadata.type == "concept":
            scenarios.append("Learning and understanding")

        return scenarios

    def _predict_shelf_life(self, content: str, metadata: KnowledgeMetadata) -> str:
        """Predict content shelf life."""
        if "api" in content.lower() or "version" in content.lower():
            return "short"  # APIs change frequently
        elif metadata.type == "concept":
            return "long"  # Concepts are more stable
        else:
            return "medium"

    def _suggest_content_types(self, content: str) -> list[str]:
        """Suggest content types based on content analysis."""
        suggested_types = []
        content_lower = content.lower()

        # Check for prompt patterns
        if any(
            pattern in content_lower
            for pattern in ["prompt", "claude", "ask", "request", "generate"]
        ):
            suggested_types.append("prompt")

        # Check for code patterns
        if any(
            pattern in content
            for pattern in [
                "```",
                "def ",
                "function ",
                "class ",
                "import ",
                "const ",
                "let ",
            ]
        ):
            suggested_types.append("code")

        # Check for concept patterns
        if any(
            pattern in content_lower
            for pattern in ["concept", "theory", "principle", "methodology", "approach"]
        ):
            suggested_types.append("concept")

        # Check for resource patterns
        if any(
            pattern in content_lower
            for pattern in ["resource", "link", "reference", "documentation", "guide"]
        ):
            suggested_types.append("resource")

        # Return most likely type first
        return suggested_types if suggested_types else ["prompt"]


def create_ai_assistant(vault_path: Path, config: CKCConfig) -> AIKnowledgeAssistant:
    """Convenience function to create AI assistant."""
    return AIKnowledgeAssistant(vault_path, config)
