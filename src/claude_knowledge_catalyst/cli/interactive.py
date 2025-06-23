"""Interactive CLI components for enhanced user experience."""

import re
from dataclasses import dataclass
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from ..core.metadata import KnowledgeMetadata, MetadataManager
from ..core.tag_standards import TagStandardsManager
from ..obsidian.query_builder import ObsidianQueryBuilder

console = Console()


@dataclass
class TagSuggestion:
    """Tag suggestion with confidence score."""

    tag_type: str
    value: str
    confidence: float
    reason: str


class InteractiveTagManager:
    """Interactive tag management with intelligent suggestions."""

    def __init__(self, metadata_manager: MetadataManager):
        self.metadata_manager = metadata_manager
        self.tag_standards = TagStandardsManager()

    def guided_file_tagging(self, file_path: Path) -> KnowledgeMetadata:
        """Interactive guided tagging for a file."""
        console.print(
            f"\n[bold blue]🏷️ Interactive Tagging: {file_path.name}[/bold blue]"
        )

        # Read file content
        try:
            content = file_path.read_text(encoding="utf-8")
            existing_metadata = self.metadata_manager.extract_metadata_from_file(
                file_path
            )
        except Exception as e:
            console.print(f"[red]Error reading file: {e}[/red]")
            raise typer.Exit(1) from e

        # Show file preview
        self._show_file_preview(content)

        # Get intelligent suggestions
        suggestions = self._analyze_and_suggest(content, existing_metadata)

        # Interactive tagging session
        updated_metadata = self._interactive_tagging_session(
            existing_metadata, suggestions
        )

        # Validate and confirm
        is_valid, errors = self.metadata_manager.tag_standards.validate_metadata_tags(
            updated_metadata.model_dump()
        )

        if errors:
            console.print("\n[yellow]⚠️ Tag validation warnings:[/yellow]")
            for error in errors:
                console.print(f"  • {error}")

        if Confirm.ask(f"\n[green]Save updated tags to {file_path.name}?[/green]"):
            self.metadata_manager.update_file_metadata(file_path, updated_metadata)
            console.print("[green]✅ Tags updated successfully![/green]")

        return updated_metadata

    def _show_file_preview(self, content: str) -> None:
        """Show file content preview."""
        lines = content.split("\n")
        preview_lines = lines[:10] if len(lines) > 10 else lines

        # Extract frontmatter if present
        frontmatter_end = -1
        if content.startswith("---\n"):
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == "---":
                    frontmatter_end = i
                    break

        if frontmatter_end > 0:
            # Show frontmatter separately
            frontmatter = "\n".join(lines[1:frontmatter_end])
            main_content = "\n".join(lines[frontmatter_end + 1 : frontmatter_end + 6])

            console.print("\n[dim]Current frontmatter:[/dim]")
            console.print(Panel(frontmatter, title="Metadata", border_style="blue"))

            console.print("\n[dim]Content preview:[/dim]")
            console.print(Panel(main_content, title="Content", border_style="green"))
        else:
            # Show content preview
            preview_content = "\n".join(preview_lines)
            console.print("\n[dim]File preview:[/dim]")
            console.print(Panel(preview_content, title="Content", border_style="green"))

    def _analyze_and_suggest(
        self, content: str, metadata: KnowledgeMetadata
    ) -> list[TagSuggestion]:
        """Analyze content and generate intelligent tag suggestions."""
        suggestions = []

        # Get existing tags for comparison
        existing_tags = {
            "type": [metadata.type],
            "status": [metadata.status],
            "tech": metadata.tech,
            "domain": metadata.domain,
            "team": metadata.team,
            "claude_model": metadata.claude_model,
            "claude_feature": metadata.claude_feature,
            "tags": metadata.tags,
        }

        # Get standard suggestions
        standard_suggestions = self.metadata_manager.tag_standards.suggest_tags(
            content, existing_tags
        )

        # Convert to TagSuggestion objects with confidence scores
        for tag_type, values in standard_suggestions.items():
            for value in values:
                confidence = self._calculate_confidence(tag_type, value, content)
                reason = self._get_suggestion_reason(tag_type, value, content)

                suggestions.append(
                    TagSuggestion(
                        tag_type=tag_type,
                        value=value,
                        confidence=confidence,
                        reason=reason,
                    )
                )

        # Add type-specific suggestions
        suggestions.extend(self._get_advanced_suggestions(content, metadata))

        # Sort by confidence
        suggestions.sort(key=lambda x: x.confidence, reverse=True)

        return suggestions[:10]  # Top 10 suggestions

    def _calculate_confidence(self, tag_type: str, value: str, content: str) -> float:
        """Calculate confidence score for a tag suggestion."""
        content_lower = content.lower()
        value_lower = value.lower()

        # Direct mention = high confidence
        if value_lower in content_lower:
            return 0.9

        # Related keywords
        keyword_matches = 0
        keywords = value_lower.split("-")
        for keyword in keywords:
            if keyword in content_lower:
                keyword_matches += 1

        if keyword_matches > 0:
            return 0.7 + (keyword_matches * 0.1)

        # Technology patterns
        tech_patterns = {
            "python": ["def ", "import ", "pip", ".py"],
            "javascript": [" js ", "npm", "node", "const ", "let "],
            "react": ["jsx", "component", "props", "state"],
            "docker": ["dockerfile", "container", "image"],
        }

        if tag_type == "tech" and value in tech_patterns:
            pattern_matches = sum(
                1 for pattern in tech_patterns[value] if pattern in content_lower
            )
            if pattern_matches > 0:
                return 0.6 + (pattern_matches * 0.1)

        return 0.3  # Low confidence baseline

    def _get_suggestion_reason(self, tag_type: str, value: str, content: str) -> str:
        """Get human-readable reason for tag suggestion."""
        content_lower = content.lower()

        if value.lower() in content_lower:
            return f"'{value}' mentioned in content"

        # Technology-specific reasons
        if tag_type == "tech":
            if value == "python" and any(
                p in content_lower for p in ["def ", "import ", ".py"]
            ):
                return "Python code patterns detected"
            elif value == "javascript" and any(
                p in content_lower for p in ["const ", "npm", "node"]
            ):
                return "JavaScript patterns detected"
            elif value == "react" and any(
                p in content_lower for p in ["jsx", "component"]
            ):
                return "React patterns detected"

        return f"Content analysis suggests {tag_type}: {value}"

    def _get_advanced_suggestions(
        self, content: str, metadata: KnowledgeMetadata
    ) -> list[TagSuggestion]:
        """Get advanced context-aware suggestions."""
        suggestions = []
        content_lower = content.lower()

        # Complexity inference
        if not metadata.complexity:
            if len(content) < 500:
                suggestions.append(
                    TagSuggestion(
                        "complexity",
                        "beginner",
                        0.6,
                        "Short content suggests beginner level",
                    )
                )
            elif any(
                word in content_lower
                for word in ["advanced", "complex", "sophisticated"]
            ):
                suggestions.append(
                    TagSuggestion(
                        "complexity", "advanced", 0.8, "Advanced terminology detected"
                    )
                )

        # Confidence inference
        if not metadata.confidence:
            if any(
                word in content_lower for word in ["tested", "proven", "production"]
            ):
                suggestions.append(
                    TagSuggestion(
                        "confidence", "high", 0.7, "Production/tested indicators found"
                    )
                )
            elif any(
                word in content_lower for word in ["draft", "experimental", "wip"]
            ):
                suggestions.append(
                    TagSuggestion(
                        "confidence", "low", 0.6, "Draft/experimental indicators found"
                    )
                )

        # Claude feature inference
        if any(word in content_lower for word in ["generate", "create", "build"]):
            suggestions.append(
                TagSuggestion(
                    "claude_feature",
                    "code-generation",
                    0.7,
                    "Generation keywords detected",
                )
            )

        if any(word in content_lower for word in ["analyze", "review", "examine"]):
            suggestions.append(
                TagSuggestion(
                    "claude_feature", "analysis", 0.7, "Analysis keywords detected"
                )
            )

        return suggestions

    def _interactive_tagging_session(
        self, metadata: KnowledgeMetadata, suggestions: list[TagSuggestion]
    ) -> KnowledgeMetadata:
        """Run interactive tagging session."""
        console.print("\n[bold]📝 Current Tags:[/bold]")
        self._display_current_tags(metadata)

        if suggestions:
            console.print("\n[bold]💡 Smart Suggestions:[/bold]")
            self._display_suggestions(suggestions)

            if Confirm.ask("\n[cyan]Apply suggested tags?[/cyan]"):
                metadata = self._apply_suggestions(metadata, suggestions)

        # Manual tag editing
        if Confirm.ask("\n[cyan]Edit tags manually?[/cyan]"):
            metadata = self._manual_tag_editing(metadata)

        return metadata

    def _display_current_tags(self, metadata: KnowledgeMetadata) -> None:
        """Display current tags in a formatted table."""
        table = Table(title="Current Tags")
        table.add_column("Category", style="cyan")
        table.add_column("Values", style="green")

        table.add_row("type", metadata.type)
        table.add_row("status", metadata.status)

        if metadata.tech:
            table.add_row("tech", ", ".join(metadata.tech))
        if metadata.domain:
            table.add_row("domain", ", ".join(metadata.domain))
        if metadata.team:
            table.add_row("team", ", ".join(metadata.team))
        if metadata.complexity:
            table.add_row("complexity", metadata.complexity)
        if metadata.confidence:
            table.add_row("confidence", metadata.confidence)
        if metadata.claude_model:
            table.add_row("claude_model", ", ".join(metadata.claude_model))
        if metadata.claude_feature:
            table.add_row("claude_feature", ", ".join(metadata.claude_feature))
        if metadata.projects:
            table.add_row("projects", ", ".join(metadata.projects))
        if metadata.tags:
            table.add_row("tags", ", ".join(metadata.tags))

        console.print(table)

    def _display_suggestions(self, suggestions: list[TagSuggestion]) -> None:
        """Display tag suggestions with confidence scores."""
        table = Table(title="Smart Suggestions")
        table.add_column("Category", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Confidence", style="yellow")
        table.add_column("Reason", style="dim")

        for suggestion in suggestions:
            confidence_str = f"{suggestion.confidence:.0%}"
            table.add_row(
                suggestion.tag_type, suggestion.value, confidence_str, suggestion.reason
            )

        console.print(table)

    def _apply_suggestions(
        self, metadata: KnowledgeMetadata, suggestions: list[TagSuggestion]
    ) -> KnowledgeMetadata:
        """Apply suggested tags to metadata."""
        metadata_dict = metadata.model_dump()

        for suggestion in suggestions:
            if suggestion.confidence > 0.6:  # Only apply high-confidence suggestions
                tag_type = suggestion.tag_type
                value = suggestion.value

                if tag_type in ["complexity", "confidence", "type", "status"]:
                    # Single-value fields
                    if not metadata_dict.get(tag_type):
                        metadata_dict[tag_type] = value
                        console.print(f"[green]✓[/green] Added {tag_type}: {value}")
                else:
                    # List fields
                    if tag_type not in metadata_dict:
                        metadata_dict[tag_type] = []

                    if value not in metadata_dict[tag_type]:
                        metadata_dict[tag_type].append(value)
                        console.print(f"[green]✓[/green] Added {tag_type}: {value}")

        return KnowledgeMetadata(**metadata_dict)

    def _manual_tag_editing(self, metadata: KnowledgeMetadata) -> KnowledgeMetadata:
        """Manual tag editing with autocomplete."""
        metadata_dict = metadata.model_dump()

        console.print("\n[bold]Manual Tag Editing[/bold]")
        console.print("[dim]Press Enter to keep current value, or type new value[/dim]")

        # Edit required fields
        new_type = self._prompt_with_autocomplete(
            "type", metadata.type, self.tag_standards.standards["type"].valid_values
        )
        if new_type:
            metadata_dict["type"] = new_type

        new_status = self._prompt_with_autocomplete(
            "status",
            metadata.status,
            self.tag_standards.standards["status"].valid_values,
        )
        if new_status:
            metadata_dict["status"] = new_status

        # Edit optional fields
        optional_fields = [
            "tech",
            "domain",
            "team",
            "claude_model",
            "claude_feature",
            "projects",
            "tags",
        ]

        for field in optional_fields:
            if field in self.tag_standards.standards:
                valid_values = self.tag_standards.standards[field].valid_values
            else:
                valid_values = []

            current_values = metadata_dict.get(field, [])
            new_values = self._prompt_list_field(field, current_values, valid_values)

            if new_values is not None:
                metadata_dict[field] = new_values

        # Edit single-value optional fields
        single_fields = ["complexity", "confidence"]
        for field in single_fields:
            if field in self.tag_standards.standards:
                valid_values = self.tag_standards.standards[field].valid_values
                current_value = metadata_dict.get(field, "")
                new_value = self._prompt_with_autocomplete(
                    field, current_value, valid_values
                )
                if new_value:
                    metadata_dict[field] = new_value

        return KnowledgeMetadata(**metadata_dict)

    def _prompt_with_autocomplete(
        self, field_name: str, current_value: str, valid_values: list[str]
    ) -> str | None:
        """Prompt with autocomplete suggestions."""
        if valid_values:
            console.print(
                f"\n[cyan]{field_name}[/cyan] [dim](current: {current_value})[/dim]"
            )
            console.print(
                f"[dim]Valid options: {', '.join(valid_values[:5])}"
                f"{'...' if len(valid_values) > 5 else ''}[/dim]"
            )

        value = Prompt.ask(f"New {field_name}", default=current_value)

        if value == current_value:
            return None

        # Validate against known values
        if valid_values and value not in valid_values:
            if not Confirm.ask(
                f"[yellow]'{value}' is not a standard value. Use anyway?[/yellow]"
            ):
                return None

        return value

    def _prompt_list_field(
        self, field_name: str, current_values: list[str], valid_values: list[str]
    ) -> list[str] | None:
        """Prompt for list field values."""
        console.print(
            f"\n[cyan]{field_name}[/cyan] [dim](current: "
            f"{', '.join(current_values) if current_values else 'none'})[/dim]"
        )

        if valid_values:
            console.print(
                f"[dim]Valid options: {', '.join(valid_values[:8])}"
                f"{'...' if len(valid_values) > 8 else ''}[/dim]"
            )

        console.print(
            "[dim]Enter comma-separated values, or press Enter to keep current[/dim]"
        )

        value_str = Prompt.ask(f"New {field_name}", default=", ".join(current_values))

        if value_str == ", ".join(current_values):
            return None

        if not value_str.strip():
            return []

        new_values = [v.strip() for v in value_str.split(",") if v.strip()]

        # Validate values
        if valid_values:
            invalid_values = [v for v in new_values if v not in valid_values]
            if invalid_values:
                console.print(
                    f"[yellow]Warning: Non-standard values: "
                    f"{', '.join(invalid_values)}[/yellow]"
                )
                if not Confirm.ask("[yellow]Continue anyway?[/yellow]"):
                    return None

        return new_values


class SmartQueryBuilder:
    """Smart query builder with natural language processing."""

    def __init__(self):
        self.tag_standards = TagStandardsManager()

    def build_from_natural_language(
        self, query_text: str
    ) -> tuple[ObsidianQueryBuilder, str]:
        """Build query from natural language input."""
        console.print(f"\n[blue]🔍 Parsing query:[/blue] '{query_text}'")

        query_builder = ObsidianQueryBuilder()
        interpretations = []

        # Parse different query components
        query_lower = query_text.lower()

        # Content type detection
        if any(word in query_lower for word in ["prompt", "prompts"]):
            query_builder = query_builder.type("prompt")
            interpretations.append("Content type: prompt")
        elif any(word in query_lower for word in ["code", "snippet", "script"]):
            query_builder = query_builder.type("code")
            interpretations.append("Content type: code")
        elif any(word in query_lower for word in ["concept", "theory", "explanation"]):
            query_builder = query_builder.type("concept")
            interpretations.append("Content type: concept")
        elif any(word in query_lower for word in ["resource", "link", "reference"]):
            query_builder = query_builder.type("resource")
            interpretations.append("Content type: resource")

        # Status detection
        if any(word in query_lower for word in ["draft", "drafts", "wip"]):
            query_builder = query_builder.status("draft")
            interpretations.append("Status: draft")
        elif any(word in query_lower for word in ["production", "prod", "live"]):
            query_builder = query_builder.status("production")
            interpretations.append("Status: production")
        elif any(word in query_lower for word in ["tested", "verified"]):
            query_builder = query_builder.status("tested")
            interpretations.append("Status: tested")

        # Technology detection
        tech_keywords = {
            "python": ["python", "py", "pip", "django", "flask"],
            "javascript": ["javascript", "js", "node", "npm", "react", "vue"],
            "docker": ["docker", "container", "image"],
            "aws": ["aws", "amazon web services", "s3", "ec2"],
            "react": ["react", "jsx", "component"],
        }

        detected_tech = []
        for tech, keywords in tech_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_tech.append(tech)

        if detected_tech:
            query_builder = query_builder.tech(detected_tech)
            interpretations.append(f"Technology: {', '.join(detected_tech)}")

        # Quality filters
        if any(word in query_lower for word in ["high quality", "best", "excellent"]):
            query_builder = query_builder.confidence("high").status("production")
            interpretations.append("Quality filter: high confidence + production")

        if any(word in query_lower for word in ["beginner", "easy", "simple"]):
            query_builder = query_builder.complexity("beginner")
            interpretations.append("Complexity: beginner")
        elif any(word in query_lower for word in ["advanced", "complex", "expert"]):
            query_builder = query_builder.complexity("advanced")
            interpretations.append("Complexity: advanced")

        # Success rate for prompts
        success_match = re.search(r"success\s+rate\s+(\d+)", query_lower)
        if success_match:
            rate = int(success_match.group(1))
            from ..obsidian.query_builder import QueryComparison

            query_builder = query_builder.success_rate(
                rate, QueryComparison.GREATER_EQUAL
            )
            interpretations.append(f"Success rate: >= {rate}%")

        # Recent content
        if any(word in query_lower for word in ["recent", "latest", "new"]):
            query_builder = query_builder.updated_after("2024-01-01").sort_by(
                "updated", False
            )
            interpretations.append("Filter: recent updates")

        # Extract free-form tags
        remaining_words = query_lower.split()
        technical_words = [
            word
            for word in remaining_words
            if word
            not in ["the", "a", "an", "and", "or", "for", "with", "in", "on", "at"]
        ]

        if technical_words:
            query_builder = query_builder.tags(technical_words[:3])  # Limit to 3 tags
            interpretations.append(f"Free-form tags: {', '.join(technical_words[:3])}")

        interpretation_text = (
            "; ".join(interpretations)
            if interpretations
            else "No specific filters detected"
        )

        return query_builder, interpretation_text


def interactive_search_session() -> None:
    """Run an interactive search session."""
    console.print("\n[bold blue]🔍 Interactive Search Session[/bold blue]")
    console.print(
        "[dim]Type your search query in natural language, or 'quit' to exit[/dim]\n"
    )

    smart_builder = SmartQueryBuilder()

    while True:
        query_text = Prompt.ask("[cyan]Search query[/cyan]")

        if query_text.lower() in ["quit", "exit", "q"]:
            console.print("[yellow]Goodbye![/yellow]")
            break

        if not query_text.strip():
            continue

        # Build query from natural language
        query_builder, interpretation = smart_builder.build_from_natural_language(
            query_text
        )

        # Show interpretation
        console.print(f"\n[green]Interpreted as:[/green] {interpretation}")

        # Show generated query
        obsidian_query = query_builder.build()
        console.print("\n[blue]Obsidian Query:[/blue]")
        console.print(Panel(obsidian_query, title="Query", border_style="blue"))

        # Show dataview version
        dataview_query = query_builder.build_dataview()
        console.print("\n[blue]Dataview Query:[/blue]")
        console.print(Panel(dataview_query, title="Dataview", border_style="green"))

        # Ask if user wants to refine
        if Confirm.ask("\n[cyan]Search again?[/cyan]"):
            continue
        else:
            break


def quick_tag_wizard() -> None:
    """Quick wizard for common tagging scenarios."""
    console.print("\n[bold blue]🧙 Quick Tag Wizard[/bold blue]")

    scenarios = {
        "1": ("New Prompt", "prompt", "draft"),
        "2": ("Code Snippet", "code", "tested"),
        "3": ("Concept Documentation", "concept", "draft"),
        "4": ("Resource Collection", "resource", "draft"),
        "5": ("Production Prompt", "prompt", "production"),
    }

    console.print("\n[bold]Quick Scenarios:[/bold]")
    for key, (name, content_type, status) in scenarios.items():
        console.print(f"  {key}. {name} ({content_type}, {status})")

    choice = Prompt.ask(
        "\nSelect scenario", choices=list(scenarios.keys()) + ["custom"]
    )

    if choice == "custom":
        console.print("[yellow]Use 'ckc tags' command for custom tagging[/yellow]")
        return

    name, content_type, status = scenarios[choice]

    # Get file path
    file_path_str = Prompt.ask("\nFile path")
    file_path = Path(file_path_str)

    if not file_path.exists():
        console.print(f"[red]File not found: {file_path}[/red]")
        return

    # Create basic metadata

    # Interactive enhancement
    metadata_manager = MetadataManager()
    interactive_manager = InteractiveTagManager(metadata_manager)

    interactive_manager.guided_file_tagging(file_path)

    console.print(f"\n[green]✅ Quick tagging completed for {file_path.name}![/green]")
