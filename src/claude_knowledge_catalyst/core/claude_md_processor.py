"""CLAUDE.md file processing utilities."""

import re
from pathlib import Path
from typing import Any


class ClaudeMdProcessor:
    """Processor for CLAUDE.md files with section filtering capabilities."""

    def __init__(self, sections_exclude: list[str] | None = None):
        """Initialize processor with excluded sections.

        Args:
            sections_exclude: List of section headers to exclude
                (e.g., ['# secrets', '# private'])
        """
        self.sections_exclude = sections_exclude or []
        # Normalize section patterns for case-insensitive matching
        self.exclude_patterns = [
            re.compile(rf"^{re.escape(section.strip())}$", re.IGNORECASE)
            for section in self.sections_exclude
        ]

    def process_claude_md(self, file_path: Path) -> str:
        """Process CLAUDE.md file and filter out excluded sections.

        Args:
            file_path: Path to the CLAUDE.md file

        Returns:
            Filtered content as string

        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file can't be read
        """
        if not file_path.exists():
            raise FileNotFoundError(f"CLAUDE.md file not found: {file_path}")

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
        except PermissionError as e:
            raise PermissionError(f"Cannot read CLAUDE.md file: {file_path}") from e

        if not self.sections_exclude:
            return content

        return self._filter_sections(content)

    def _filter_sections(self, content: str) -> str:
        """Filter out excluded sections from markdown content.

        Args:
            content: Original markdown content

        Returns:
            Filtered content with excluded sections removed
        """
        lines = content.split("\n")
        filtered_lines = []
        skip_section = False

        for line in lines:
            # Check if line is a section header
            if line.strip().startswith("#"):
                skip_section = self._should_exclude_section(line.strip())

                # If not skipping, add the section header
                if not skip_section:
                    filtered_lines.append(line)
            else:
                # Add line only if not in a skipped section
                if not skip_section:
                    filtered_lines.append(line)

        # Remove trailing empty lines
        while filtered_lines and not filtered_lines[-1].strip():
            filtered_lines.pop()

        return "\n".join(filtered_lines)

    def _should_exclude_section(self, section_header: str) -> bool:
        """Check if a section header should be excluded.

        Args:
            section_header: Section header line (e.g., "# Private Section")

        Returns:
            True if section should be excluded
        """
        for pattern in self.exclude_patterns:
            if pattern.match(section_header):
                return True
        return False

    def get_metadata_for_claude_md(self, file_path: Path) -> dict[str, Any]:
        """Generate enhanced metadata for CLAUDE.md files.

        Args:
            file_path: Path to the CLAUDE.md file

        Returns:
            Dictionary containing enhanced metadata
        """
        metadata = {
            "file_type": "claude_config",
            "is_claude_md": True,
            "project_root": str(
                file_path.parent
                if file_path.name == "CLAUDE.md"
                else file_path.parent.parent
            ),
            "sections_filtered": len(self.sections_exclude) > 0,
            "excluded_sections": self.sections_exclude.copy(),
        }

        # Try to extract additional info from the file
        try:
            content = self.process_claude_md(file_path)
            metadata.update(self._extract_content_metadata(content))
        except Exception:
            # If we can't read the file, just return basic metadata
            pass

        return metadata

    def _extract_content_metadata(self, content: str) -> dict[str, Any]:
        """Extract metadata from CLAUDE.md content.

        Args:
            content: Filtered content of CLAUDE.md

        Returns:
            Dictionary with extracted metadata
        """
        metadata: dict[str, Any] = {}

        # Count sections
        sections: list[str] = [
            line.strip() for line in content.split("\n") if line.strip().startswith("#")
        ]
        metadata["section_count"] = len(sections)
        metadata["sections"] = sections

        # Look for common patterns
        if "project overview" in content.lower():
            metadata["has_project_overview"] = True
        if "architecture" in content.lower():
            metadata["has_architecture_info"] = True
        if "command" in content.lower() or "cmd" in content.lower():
            metadata["has_commands"] = True
        if "best practice" in content.lower() or "guideline" in content.lower():
            metadata["has_guidelines"] = True

        return metadata

    def should_sync_claude_md(self, file_path: Path) -> bool:
        """Determine if a CLAUDE.md file should be synchronized.

        Args:
            file_path: Path to the CLAUDE.md file

        Returns:
            True if file should be synced
        """
        if not file_path.exists():
            return False

        # Basic checks
        if file_path.name != "CLAUDE.md":
            return False

        # Check if file is readable
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
        except (PermissionError, UnicodeDecodeError):
            return False

        # Don't sync empty files
        if not content.strip():
            return False

        # If all sections would be filtered out, don't sync
        if self.sections_exclude:
            filtered_content = self._filter_sections(content)
            if not filtered_content.strip():
                return False

        return True
