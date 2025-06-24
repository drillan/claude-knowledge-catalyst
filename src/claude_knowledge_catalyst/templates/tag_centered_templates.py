"""Template system for pure tag-centered knowledge management."""

from datetime import datetime
from pathlib import Path


class TagCenteredTemplateManager:
    """Manages templates for pure tag-centered system."""

    def __init__(self) -> None:
        self.templates = self._initialize_templates()

    def _initialize_templates(self) -> dict[str, str]:
        """Initialize template definitions."""
        return {
            "prompt": self._get_prompt_template(),
            "code": self._get_code_template(),
            "concept": self._get_concept_template(),
            "resource": self._get_resource_template(),
            "vault_readme": self._get_vault_readme_template(),
            "directory_readme": self._get_directory_readme_template(),
            "obsidian_query": self._get_obsidian_query_template(),
        }

    def _get_prompt_template(self) -> str:
        """Template for prompt files."""
        return """---
title: "{title}"
created: {created}
updated: {updated}
version: "1.0"

# === Pure Multi-layered Tag Architecture ===
type: prompt
status: draft
tech: []
domain: []
team: []
complexity: beginner
confidence: medium
success_rate: null
projects: []
claude_model: []
claude_feature: []
tags: []

# System metadata
author: null
purpose: "{purpose}"
---

# {title}

## Purpose
{purpose}

## Prompt Content

```
[Your prompt content here]
```

## Usage Examples

### Example 1
**Input:**
```
[Example input]
```

**Expected Output:**
```
[Expected output]
```

## Notes
-

## Related
-

---
*Generated with Pure Tag-Centered System*
"""

    def _get_code_template(self) -> str:
        """Template for code snippet files."""
        return """---
title: "{title}"
created: {created}
updated: {updated}
version: "1.0"

# === Pure Multi-layered Tag Architecture ===
type: code
status: draft
tech: []
domain: []
team: []
complexity: beginner
confidence: medium
projects: []
claude_model: []
claude_feature: []
tags: []

# System metadata
author: null
purpose: "{purpose}"
---

# {title}

## Purpose
{purpose}

## Code

```{language}
# Your code here
```

## Usage

```{language}
# Usage example
```

## Notes
-

## Dependencies
-

---
*Generated with Pure Tag-Centered System*
"""

    def _get_concept_template(self) -> str:
        """Template for concept documentation."""
        return """---
title: "{title}"
created: {created}
updated: {updated}
version: "1.0"

# === Pure Multi-layered Tag Architecture ===
type: concept
status: draft
tech: []
domain: []
team: []
complexity: beginner
confidence: medium
projects: []
claude_model: []
claude_feature: []
tags: []

# System metadata
author: null
purpose: "{purpose}"
---

# {title}

## Overview
{purpose}

## Key Concepts

### Concept 1
Description here.

### Concept 2
Description here.

## Implementation

### Approach 1
Steps and considerations.

### Approach 2
Alternative approach.

## Best Practices
-

## Common Pitfalls
-

## Related Concepts
-

---
*Generated with Pure Tag-Centered System*
"""

    def _get_resource_template(self) -> str:
        """Template for resource collections."""
        return """---
title: "{title}"
created: {created}
updated: {updated}
version: "1.0"

# === Pure Multi-layered Tag Architecture ===
type: resource
status: draft
tech: []
domain: []
team: []
complexity: beginner
confidence: medium
projects: []
claude_model: []
claude_feature: []
tags: []

# System metadata
author: null
purpose: "{purpose}"
---

# {title}

## Purpose
{purpose}

## Resources

### Documentation
-

### Tools
-

### Libraries/Frameworks
-

### Tutorials/Guides
-

### Articles/Papers
-

## Quick Reference
-

## Notes
-

---
*Generated with Pure Tag-Centered System*
"""

    def _get_vault_readme_template(self) -> str:
        """Template for main vault README."""
        return """# Pure Tag-Centered Knowledge Vault

Welcome to your revolutionary tag-centered knowledge management system!
This vault eliminates complex directory hierarchies and relies on intelligent
tagging for organization.

## Directory Structure (Minimal & State-Based)

```
📁 _system/          # System files (templates, scripts, configurations)
📁 _attachments/     # Binary files and attachments
📁 inbox/            # Draft content and unprocessed files
📁 active/           # Currently relevant content
📁 archive/          # Deprecated or outdated content
📁 knowledge/        # Main knowledge repository (90% of content)
```

## Core Philosophy

### 🏷️ Tag-Centered Organization
- **No complex directory hierarchies** - content is organized by state, not type
- **Multi-layered tagging** - rich metadata through standardized tags
- **Dynamic views** - use Obsidian queries to create custom organization
- **Cognitive load reduction** - eliminate classification decisions

### 📊 State-Based Classification
- `draft` → `inbox/` - Work in progress, ideas, unprocessed content
- `tested`/`production` → `knowledge/` - Validated, reliable content
- `deprecated` → `archive/` - Outdated but historically valuable
- Active work → `active/` - Currently relevant projects and tasks

## Tag System

### Required Tags
- **type**: `prompt`, `code`, `concept`, `resource`
- **status**: `draft`, `tested`, `production`, `deprecated`

### Multi-Layered Categories
- **tech**: Technology stack (`python`, `react`, `docker`, etc.)
- **domain**: Knowledge domain (`web-dev`, `data-science`, `devops`, etc.)
- **team**: Team responsibility (`frontend`, `backend`, `ml`, etc.)
- **projects**: Associated projects (array)

### Quality Indicators
- **complexity**: `beginner`, `intermediate`, `advanced`, `expert`
- **confidence**: `low`, `medium`, `high`
- **success_rate**: 0-100 (for prompts and processes)

### Claude-Specific
- **claude_model**: `opus`, `sonnet`, `haiku`
- **claude_feature**: `code-generation`, `analysis`, `debugging`, etc.

## Quick Start

1. **Create content** in any directory (usually `inbox/` for drafts)
2. **Add tags** using the standardized system
3. **Use Obsidian queries** to organize and find content
4. **Let the system** automatically place files based on status

## Obsidian Queries

### All Production Code
```query
type:code status:production
```

### Python Web Development
```query
tech:python domain:web-dev
```

### High-Confidence Prompts
```query
type:prompt confidence:high success_rate:>80
```

## Templates

Use the templates in `_system/templates/` for consistent formatting:
- **Prompt Template**: For Claude prompts and interactions
- **Code Template**: For code snippets and scripts
- **Concept Template**: For knowledge documentation
- **Resource Template**: For curated resource lists

## Evolution

This system evolves with your needs:
- Add new tags organically
- Create custom queries for new workflows
- Let content naturally flow between states
- Focus on creation, not organization

---
*Pure Tag-Centered System - Revolutionizing Knowledge Management*
"""

    def _get_directory_readme_template(self) -> str:
        """Template for directory README files."""
        return """# {directory_name}

{description}

## Purpose

This directory is part of the pure tag-centered system's minimal structure.
Content is organized by **state** rather than **type**.

## Content Guidelines

### What belongs here:
{content_guidelines}

### Tagging Strategy:
- Ensure `status: {expected_status}` is set correctly
- Use rich multi-layered tags for discoverability
- Focus on `tech`, `domain`, and `team` tags

## Obsidian Queries

### Content in this directory:
```query
path:"{directory_name}/"
```

### By content type:
```query
path:"{directory_name}/" type:prompt
path:"{directory_name}/" type:code
path:"{directory_name}/" type:concept
```

## Workflow

Files naturally flow between directories as their status changes:
- `inbox/` → `knowledge/` (when validated)
- `knowledge/` → `archive/` (when deprecated)
- `active/` ↔ other directories (based on current relevance)

---
*Generated with Pure Tag-Centered System*
"""

    def _get_obsidian_query_template(self) -> str:
        """Template for common Obsidian queries."""
        return """# Obsidian Queries for Pure Tag-Centered System

This document contains pre-built queries for organizing and discovering
content in the tag-centered system.

## Content Discovery

### By Type
```query
type:prompt
```
```query
type:code
```
```query
type:concept
```
```query
type:resource
```

### By Status
```query
status:draft
```
```query
status:production
```
```query
status:deprecated
```

### By Technology
```query
tech:python
```
```query
tech:javascript
```
```query
tech:react
```

### By Domain
```query
domain:web-dev
```
```query
domain:data-science
```
```query
domain:devops
```

## Quality Filters

### High-Quality Content
```query
confidence:high status:production
```

### Expert-Level Content
```query
complexity:advanced OR complexity:expert
```

### Successful Prompts
```query
type:prompt success_rate:>80
```

## Team Views

### Frontend Resources
```query
team:frontend
```

### Backend Code
```query
team:backend type:code
```

### ML Research
```query
team:ml domain:machine-learning
```

## Project Views

### Active Projects
```query
status:production projects:*
```

### Project-Specific Content
```query
projects:"ProjectName"
```

## Advanced Combinations

### Production Python Code for Web Development
```query
type:code tech:python domain:web-dev status:production
```

### High-Confidence Debugging Prompts
```query
type:prompt claude_feature:debugging confidence:high
```

### Beginner-Friendly Frontend Resources
```query
team:frontend complexity:beginner type:resource
```

## Dynamic Views

### Recently Updated
```query
updated:>2024-01-01
```

### Needs Review (Draft Status)
```query
status:draft created:<-30d
```

### Deprecated Content (Cleanup Candidates)
```query
status:deprecated updated:<-180d
```

---
*Pure Tag-Centered System Query Reference*
"""

    def generate_file(self, template_type: str, **kwargs) -> str:
        """Generate file content from template.

        Args:
            template_type: Type of template to use
            **kwargs: Variables to substitute in template

        Returns:
            Generated file content
        """
        if template_type not in self.templates:
            raise ValueError(f"Unknown template type: {template_type}")

        template = self.templates[template_type]

        # Set default values
        defaults = {
            "title": "Untitled",
            "purpose": "Purpose not specified",
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "language": "python",
            "directory_name": "Unknown",
            "description": "Description not provided",
            "content_guidelines": "Guidelines not specified",
            "expected_status": "draft",
        }

        # Merge with provided kwargs
        variables = {**defaults, **kwargs}

        return template.format(**variables)

    def create_vault_structure(
        self, vault_path: Path, include_examples: bool = True
    ) -> dict[str, bool]:
        """Create complete vault structure with templates.

        Args:
            vault_path: Path to vault directory
            include_examples: Whether to include example files

        Returns:
            Dictionary of created files and success status
        """
        results = {}

        # Create directories
        directories = {
            "_system": "System files (templates, configurations)",
            "_system/templates": "File templates",
            "_attachments": "Binary files and attachments",
            "inbox": "Draft content and unprocessed files (status: draft)",
            "active": "Currently relevant content",
            "archive": "Deprecated or outdated content (status: deprecated)",
            "knowledge": "Main knowledge repository (status: tested/production)",
        }

        for dir_path, description in directories.items():
            full_path = vault_path / dir_path
            try:
                full_path.mkdir(parents=True, exist_ok=True)
                results[f"directory_{dir_path}"] = True

                # Create README for each directory
                if dir_path != "_system/templates":  # Skip templates subdirectory
                    readme_content = self.generate_file(
                        "directory_readme",
                        directory_name=dir_path.split("/")[-1],
                        description=description,
                        content_guidelines=self._get_content_guidelines(dir_path),
                        expected_status=self._get_expected_status(dir_path),
                    )
                    readme_path = full_path / "README.md"
                    readme_path.write_text(readme_content, encoding="utf-8")
                    results[f"readme_{dir_path}"] = True

            except Exception as e:
                results[f"directory_{dir_path}"] = False
                print(f"Error creating {dir_path}: {e}")

        # Create main vault README
        try:
            vault_readme = self.generate_file("vault_readme")
            (vault_path / "README.md").write_text(vault_readme, encoding="utf-8")
            results["vault_readme"] = True
        except Exception as e:
            results["vault_readme"] = False
            print(f"Error creating vault README: {e}")

        # Create templates
        try:
            templates_dir = vault_path / "_system" / "templates"
            templates_dir.mkdir(parents=True, exist_ok=True)

            template_files = {
                "prompt_template.md": self.generate_file(
                    "prompt", title="New Prompt", purpose="Describe the prompt purpose"
                ),
                "code_template.md": self.generate_file(
                    "code",
                    title="New Code Snippet",
                    purpose="Describe what this code does",
                ),
                "concept_template.md": self.generate_file(
                    "concept", title="New Concept", purpose="Explain the concept"
                ),
                "resource_template.md": self.generate_file(
                    "resource",
                    title="New Resource Collection",
                    purpose="Curated resources for...",
                ),
            }

            for filename, content in template_files.items():
                (templates_dir / filename).write_text(content, encoding="utf-8")
                results[f"template_{filename}"] = True

        except Exception as e:
            results["templates"] = False
            print(f"Error creating templates: {e}")

        # Create Obsidian queries reference
        try:
            queries_content = self.generate_file("obsidian_query")
            (vault_path / "_system" / "Obsidian_Queries.md").write_text(
                queries_content, encoding="utf-8"
            )
            results["obsidian_queries"] = True
        except Exception as e:
            results["obsidian_queries"] = False
            print(f"Error creating Obsidian queries: {e}")

        # Create example files if requested
        if include_examples:
            try:
                self._create_example_files(vault_path)
                results["examples"] = True
            except Exception as e:
                results["examples"] = False
                print(f"Error creating examples: {e}")

        return results

    def _get_content_guidelines(self, directory: str) -> str:
        """Get content guidelines for directory."""
        guidelines = {
            "_system": "System files, templates, configurations, and documentation",
            "_attachments": "Binary files, images, PDFs, and other non-markdown assets",
            "inbox": "New content, drafts, ideas, and unprocessed information",
            "active": "Currently relevant content regardless of status",
            "archive": "Deprecated content that may still have historical value",
            "knowledge": "Validated, tested, and production-ready content",
        }
        return guidelines.get(
            directory.split("/")[0], "Content appropriate for this directory"
        )

    def _get_expected_status(self, directory: str) -> str:
        """Get expected status for directory."""
        status_map = {
            "inbox": "draft",
            "active": "any (based on current relevance)",
            "archive": "deprecated",
            "knowledge": "tested or production",
        }
        return status_map.get(directory.split("/")[0], "draft")

    def _create_example_files(self, vault_path: Path) -> None:
        """Create example files to demonstrate the system."""
        examples = [
            {
                "path": "inbox/example_prompt.md",
                "content": self.generate_file(
                    "prompt",
                    title="Example: Code Review Prompt",
                    purpose=(
                        "A prompt for comprehensive code review with security focus"
                    ),
                )
                .replace("draft", "draft")
                .replace("[]", "['code-review', 'security']")
                .replace(
                    "tags: ['code-review', 'security']",
                    "tags: ['code-review', 'security']\n"
                    "tech: ['python', 'javascript']\n"
                    "domain: ['web-dev', 'security']\n"
                    "team: ['backend', 'frontend']\n"
                    "claude_feature: ['code-review', 'analysis']",
                ),
            },
            {
                "path": "knowledge/example_concept.md",
                "content": self.generate_file(
                    "concept",
                    title="Example: Pure Tag-Centered Architecture",
                    purpose=(
                        "Explanation of the revolutionary tag-centered approach to "
                        "knowledge management"
                    ),
                )
                .replace("draft", "production")
                .replace("[]", "['architecture', 'knowledge-management']")
                .replace(
                    "tags: ['architecture', 'knowledge-management']",
                    "tags: ['architecture', 'knowledge-management']\n"
                    "tech: ['obsidian', 'markdown']\n"
                    "domain: ['knowledge-management', 'productivity']\n"
                    "team: ['product']\n"
                    "confidence: high\n"
                    "complexity: intermediate",
                ),
            },
            {
                "path": "knowledge/example_code.md",
                "content": self.generate_file(
                    "code",
                    title="Example: Python Tag Validation",
                    purpose=(
                        "Code snippet for validating tag structure in pure tag system"
                    ),
                    language="python",
                )
                .replace("draft", "tested")
                .replace("[]", "['validation', 'python']")
                .replace(
                    "tags: ['validation', 'python']",
                    "tags: ['validation', 'python']\n"
                    "tech: ['python']\n"
                    "domain: ['web-dev', 'automation']\n"
                    "team: ['backend']\n"
                    "claude_feature: ['code-generation']\n"
                    "confidence: high",
                ),
            },
        ]

        for example in examples:
            file_path = vault_path / example["path"]
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(example["content"], encoding="utf-8")
