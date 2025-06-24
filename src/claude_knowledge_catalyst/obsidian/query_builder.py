"""Obsidian query builder for pure tag-centered system."""

from dataclasses import dataclass
from enum import Enum


class QueryOperator(Enum):
    """Query operators for Obsidian search."""

    AND = "AND"
    OR = "OR"
    NOT = "NOT"


class QueryComparison(Enum):
    """Comparison operators for numeric fields."""

    EQUALS = "="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="


@dataclass
class QueryCondition:
    """Individual query condition."""

    field: str
    value: str | int | list[str]
    operator: QueryOperator = QueryOperator.AND
    comparison: QueryComparison | None = None
    negate: bool = False


class ObsidianQueryBuilder:
    """Builder for Obsidian queries optimized for tag-centered system."""

    def __init__(self) -> None:
        self.conditions: list[QueryCondition] = []
        self.sort_field: str | None = None
        self.sort_ascending: bool = True
        self.limit: int | None = None

    def type(self, content_type: str) -> "ObsidianQueryBuilder":
        """Filter by content type."""
        self.conditions.append(QueryCondition("type", content_type))
        return self

    def status(self, status: str) -> "ObsidianQueryBuilder":
        """Filter by status."""
        self.conditions.append(QueryCondition("status", status))
        return self

    def tech(self, technologies: str | list[str]) -> "ObsidianQueryBuilder":
        """Filter by technology tags."""
        if isinstance(technologies, str):
            technologies = [technologies]
        for tech in technologies:
            self.conditions.append(QueryCondition("tech", tech))
        return self

    def domain(self, domains: str | list[str]) -> "ObsidianQueryBuilder":
        """Filter by domain tags."""
        if isinstance(domains, str):
            domains = [domains]
        for domain in domains:
            self.conditions.append(QueryCondition("domain", domain))
        return self

    def team(self, teams: str | list[str]) -> "ObsidianQueryBuilder":
        """Filter by team tags."""
        if isinstance(teams, str):
            teams = [teams]
        for team in teams:
            self.conditions.append(QueryCondition("team", team))
        return self

    def projects(self, project_names: str | list[str]) -> "ObsidianQueryBuilder":
        """Filter by project associations."""
        if isinstance(project_names, str):
            project_names = [project_names]
        for project in project_names:
            self.conditions.append(QueryCondition("projects", project))
        return self

    def complexity(self, level: str) -> "ObsidianQueryBuilder":
        """Filter by complexity level."""
        self.conditions.append(QueryCondition("complexity", level))
        return self

    def confidence(self, level: str) -> "ObsidianQueryBuilder":
        """Filter by confidence level."""
        self.conditions.append(QueryCondition("confidence", level))
        return self

    def success_rate(
        self, rate: int, comparison: QueryComparison = QueryComparison.GREATER_EQUAL
    ) -> "ObsidianQueryBuilder":
        """Filter by success rate."""
        self.conditions.append(
            QueryCondition("success_rate", rate, comparison=comparison)
        )
        return self

    def claude_model(self, models: str | list[str]) -> "ObsidianQueryBuilder":
        """Filter by Claude model tags."""
        if isinstance(models, str):
            models = [models]
        for model in models:
            self.conditions.append(QueryCondition("claude_model", model))
        return self

    def claude_feature(self, features: str | list[str]) -> "ObsidianQueryBuilder":
        """Filter by Claude feature tags."""
        if isinstance(features, str):
            features = [features]
        for feature in features:
            self.conditions.append(QueryCondition("claude_feature", feature))
        return self

    def tags(self, tag_list: str | list[str]) -> "ObsidianQueryBuilder":
        """Filter by general tags."""
        if isinstance(tag_list, str):
            tag_list = [tag_list]
        for tag in tag_list:
            self.conditions.append(QueryCondition("tags", tag))
        return self

    def path(self, path_pattern: str) -> "ObsidianQueryBuilder":
        """Filter by file path."""
        self.conditions.append(QueryCondition("path", path_pattern))
        return self

    def created_after(self, date: str) -> "ObsidianQueryBuilder":
        """Filter by creation date (after)."""
        self.conditions.append(
            QueryCondition("created", date, comparison=QueryComparison.GREATER_THAN)
        )
        return self

    def updated_after(self, date: str) -> "ObsidianQueryBuilder":
        """Filter by update date (after)."""
        self.conditions.append(
            QueryCondition("updated", date, comparison=QueryComparison.GREATER_THAN)
        )
        return self

    def exclude_status(self, status: str) -> "ObsidianQueryBuilder":
        """Exclude specific status."""
        self.conditions.append(QueryCondition("status", status, negate=True))
        return self

    def exclude_type(self, content_type: str) -> "ObsidianQueryBuilder":
        """Exclude specific content type."""
        self.conditions.append(QueryCondition("type", content_type, negate=True))
        return self

    def sort_by(self, field: str, ascending: bool = True) -> "ObsidianQueryBuilder":
        """Sort results by field."""
        self.sort_field = field
        self.sort_ascending = ascending
        return self

    def limit_results(self, count: int) -> "ObsidianQueryBuilder":
        """Limit number of results."""
        self.limit = count
        return self

    def build(self) -> str:
        """Build the final Obsidian query string."""
        if not self.conditions:
            return ""

        query_parts = []

        for condition in self.conditions:
            part = self._build_condition(condition)
            if part:
                query_parts.append(part)

        # Combine conditions
        query = " ".join(query_parts)

        # Add sorting
        if self.sort_field:
            direction = "asc" if self.sort_ascending else "desc"
            query += f" sort:{self.sort_field}:{direction}"

        # Add limit
        if self.limit:
            query += f" limit:{self.limit}"

        return query.strip()

    def _build_condition(self, condition: QueryCondition) -> str:
        """Build individual condition string."""
        field = condition.field
        value = condition.value

        # Handle negation
        prefix = "-" if condition.negate else ""

        # Handle comparison operators
        if condition.comparison:
            if condition.comparison == QueryComparison.GREATER_THAN:
                return f"{prefix}{field}:>{value}"
            elif condition.comparison == QueryComparison.LESS_THAN:
                return f"{prefix}{field}:<{value}"
            elif condition.comparison == QueryComparison.GREATER_EQUAL:
                return f"{prefix}{field}:>={value}"
            elif condition.comparison == QueryComparison.LESS_EQUAL:
                return f"{prefix}{field}:<={value}"
            else:  # EQUALS
                return f"{prefix}{field}:{value}"

        # Handle list values
        if isinstance(value, list):
            conditions = [f"{prefix}{field}:{v}" for v in value]
            return "(" + " OR ".join(conditions) + ")"

        # Handle string values
        if " " in str(value):
            return f'{prefix}{field}:"{value}"'
        else:
            return f"{prefix}{field}:{value}"

    def build_dataview(self) -> str:
        """Build Dataview query for Obsidian."""
        if not self.conditions:
            return "TABLE file.name as Name, type, status, tech, domain"

        # Build WHERE clause
        where_conditions = []
        for condition in self.conditions:
            where_part = self._build_dataview_condition(condition)
            if where_part:
                where_conditions.append(where_part)

        query = "TABLE file.name as Name, type, status, tech, domain, projects\n"

        if where_conditions:
            query += "WHERE " + " AND ".join(where_conditions) + "\n"

        if self.sort_field:
            direction = "asc" if self.sort_ascending else "desc"
            query += f"SORT {self.sort_field} {direction}\n"

        if self.limit:
            query += f"LIMIT {self.limit}"

        return query.strip()

    def _build_dataview_condition(self, condition: QueryCondition) -> str:
        """Build Dataview condition."""
        field = condition.field
        value = condition.value

        # Handle negation
        operator = "!=" if condition.negate else "="

        # Handle comparison operators
        if condition.comparison:
            if condition.comparison == QueryComparison.GREATER_THAN:
                operator = ">"
            elif condition.comparison == QueryComparison.LESS_THAN:
                operator = "<"
            elif condition.comparison == QueryComparison.GREATER_EQUAL:
                operator = ">="
            elif condition.comparison == QueryComparison.LESS_EQUAL:
                operator = "<="

        # Handle list values (for array fields)
        if isinstance(value, list):
            conditions = [f'contains({field}, "{v}")' for v in value]
            return "(" + " OR ".join(conditions) + ")"

        # Handle array fields
        if field in [
            "tech",
            "domain",
            "team",
            "projects",
            "claude_model",
            "claude_feature",
            "tags",
        ]:
            if condition.negate:
                return f'!contains({field}, "{value}")'
            else:
                return f'contains({field}, "{value}")'

        # Handle regular fields
        if isinstance(value, str):
            return f'{field} {operator} "{value}"'
        else:
            return f"{field} {operator} {value}"


class PredefinedQueries:
    """Collection of predefined queries for common use cases."""

    @staticmethod
    def high_quality_content() -> ObsidianQueryBuilder:
        """Query for high-quality content."""
        return ObsidianQueryBuilder().status("production").confidence("high")

    @staticmethod
    def draft_content() -> ObsidianQueryBuilder:
        """Query for draft content needing review."""
        return ObsidianQueryBuilder().status("draft")

    @staticmethod
    def successful_prompts() -> ObsidianQueryBuilder:
        """Query for successful prompts."""
        return (
            ObsidianQueryBuilder()
            .type("prompt")
            .success_rate(80, QueryComparison.GREATER_EQUAL)
        )

    @staticmethod
    def python_resources() -> ObsidianQueryBuilder:
        """Query for Python-related content."""
        return ObsidianQueryBuilder().tech("python").sort_by("updated", False)

    @staticmethod
    def frontend_development() -> ObsidianQueryBuilder:
        """Query for frontend development content."""
        return (
            ObsidianQueryBuilder()
            .domain("web-dev")
            .team("frontend")
            .exclude_status("deprecated")
        )

    @staticmethod
    def recent_updates() -> ObsidianQueryBuilder:
        """Query for recently updated content."""
        return (
            ObsidianQueryBuilder()
            .updated_after("2024-01-01")
            .sort_by("updated", False)
            .limit_results(20)
        )

    @staticmethod
    def claude_code_generation() -> ObsidianQueryBuilder:
        """Query for Claude code generation content."""
        return (
            ObsidianQueryBuilder()
            .claude_feature("code-generation")
            .exclude_status("deprecated")
            .sort_by("success_rate", False)
        )

    @staticmethod
    def beginner_friendly() -> ObsidianQueryBuilder:
        """Query for beginner-friendly content."""
        return (
            ObsidianQueryBuilder()
            .complexity("beginner")
            .confidence("high")
            .exclude_status("deprecated")
        )

    @staticmethod
    def expert_level() -> ObsidianQueryBuilder:
        """Query for expert-level content."""
        return ObsidianQueryBuilder().complexity("expert").status("production")

    @staticmethod
    def cleanup_candidates() -> ObsidianQueryBuilder:
        """Query for content that might need cleanup."""
        return (
            ObsidianQueryBuilder()
            .status("draft")
            .updated_after("2023-01-01")  # Old drafts
            .sort_by("updated", True)
        )  # Oldest first


def generate_obsidian_queries_file() -> str:
    """Generate comprehensive Obsidian queries documentation."""

    queries = {
        "Content Discovery": {
            "All Prompts": ObsidianQueryBuilder().type("prompt").build(),
            "All Code": ObsidianQueryBuilder().type("code").build(),
            "All Concepts": ObsidianQueryBuilder().type("concept").build(),
            "All Resources": ObsidianQueryBuilder().type("resource").build(),
        },
        "Quality Filters": {
            "High-Quality Content": PredefinedQueries.high_quality_content().build(),
            "Successful Prompts": PredefinedQueries.successful_prompts().build(),
            "Expert-Level Content": PredefinedQueries.expert_level().build(),
            "Beginner-Friendly": PredefinedQueries.beginner_friendly().build(),
        },
        "Technology Focus": {
            "Python Resources": PredefinedQueries.python_resources().build(),
            "JavaScript Content": ObsidianQueryBuilder().tech("javascript").build(),
            "React Development": ObsidianQueryBuilder()
            .tech("react")
            .domain("web-dev")
            .build(),
            "Docker & DevOps": ObsidianQueryBuilder()
            .tech(["docker", "kubernetes"])
            .build(),
        },
        "Team Views": {
            "Frontend Team": PredefinedQueries.frontend_development().build(),
            "Backend Resources": ObsidianQueryBuilder()
            .team("backend")
            .exclude_status("deprecated")
            .build(),
            "ML Research": ObsidianQueryBuilder()
            .team(["ml", "research"])
            .domain("machine-learning")
            .build(),
            "DevOps Tools": ObsidianQueryBuilder().team("devops").build(),
        },
        "Status & Workflow": {
            "Production Ready": ObsidianQueryBuilder().status("production").build(),
            "Needs Review": PredefinedQueries.draft_content().build(),
            "Recent Updates": PredefinedQueries.recent_updates().build(),
            "Cleanup Candidates": PredefinedQueries.cleanup_candidates().build(),
        },
        "Claude-Specific": {
            "Code Generation": PredefinedQueries.claude_code_generation().build(),
            "Analysis & Review": ObsidianQueryBuilder()
            .claude_feature(["analysis", "code-review"])
            .build(),
            "Debugging Help": ObsidianQueryBuilder()
            .claude_feature("debugging")
            .confidence("high")
            .build(),
            "Sonnet Optimized": ObsidianQueryBuilder().claude_model("sonnet").build(),
        },
    }

    # Generate markdown documentation
    lines = [
        "# Obsidian Queries for Pure Tag-Centered System",
        "",
        "This document contains optimized queries for the revolutionary "
        "tag-centered knowledge management system.",
        "",
        "## How to Use",
        "",
        "1. **Search Box**: Copy any query below into Obsidian's search box",
        "2. **Query Block**: Use in code blocks with 'query' language",
        "3. **Dataview**: Some queries include Dataview syntax for advanced tables",
        "",
        "## Query Categories",
        "",
    ]

    for category, category_queries in queries.items():
        lines.append(f"### {category}")
        lines.append("")

        for name, query in category_queries.items():
            lines.append(f"#### {name}")
            lines.append("```query")
            lines.append(query)
            lines.append("```")
            lines.append("")

    lines.extend(
        [
            "## Advanced Examples",
            "",
            "### Multi-Technology Web Development",
            "```query",
            ObsidianQueryBuilder()
            .tech(["react", "typescript", "nodejs"])
            .domain("web-dev")
            .status("production")
            .build(),
            "```",
            "",
            "### High-Impact Research Content",
            "```query",
            ObsidianQueryBuilder()
            .type("concept")
            .complexity("advanced")
            .confidence("high")
            .domain(["machine-learning", "research"])
            .build(),
            "```",
            "",
            "### Recently Active Projects",
            "```query",
            ObsidianQueryBuilder()
            .updated_after("2024-06-01")
            .exclude_status("deprecated")
            .sort_by("updated", False)
            .limit_results(10)
            .build(),
            "```",
            "",
            "## Dataview Queries",
            "",
            "### Technology Distribution Table",
            "```dataview",
            PredefinedQueries.high_quality_content().build_dataview(),
            "```",
            "",
            "### Team Productivity Dashboard",
            "```dataview",
            ObsidianQueryBuilder()
            .exclude_status("deprecated")
            .sort_by("updated", False)
            .build_dataview(),
            "```",
            "",
            "## Custom Query Builder",
            "",
            "Use the `ObsidianQueryBuilder` class to create custom queries:",
            "",
            "```python",
            "from claude_knowledge_catalyst.obsidian.query_builder import "
            "ObsidianQueryBuilder",
            "",
            "# Build custom query",
            "query = (ObsidianQueryBuilder()",
            "         .type('prompt')",
            "         .tech(['python', 'fastapi'])",
            "         .confidence('high')",
            "         .success_rate(85)",
            "         .sort_by('updated', False)",
            "         .build())",
            "```",
            "",
            "---",
            "*Generated with Pure Tag-Centered Query System*",
        ]
    )

    return "\n".join(lines)
