"""Pattern loading and management for content classification."""

from pathlib import Path
from typing import Any

import yaml


class PatternLoader:
    """Loads and manages classification patterns from YAML files."""

    def __init__(self, patterns_dir: Path | None = None):
        """Initialize pattern loader.

        Args:
            patterns_dir: Directory containing pattern YAML files.
                         If None, uses default patterns directory.
        """
        if patterns_dir is None:
            self.patterns_dir = Path(__file__).parent / "patterns"
        else:
            self.patterns_dir = Path(patterns_dir)

        # Manual caching to avoid B019 warnings
        self._tech_patterns_cache = None
        self._domain_patterns_cache = None
        self._content_patterns_cache = None

    def load_tech_patterns(self) -> dict[str, dict[str, list[str]]]:
        """Load technology detection patterns.

        Returns:
            Dictionary of technology patterns with confidence levels.
        """
        if self._tech_patterns_cache is None:
            self._tech_patterns_cache = self._load_pattern_file("tech_patterns.yaml")
        return self._tech_patterns_cache

    def load_domain_patterns(self) -> dict[str, dict[str, list[str]]]:
        """Load domain classification patterns.

        Returns:
            Dictionary of domain patterns with confidence levels.
        """
        if self._domain_patterns_cache is None:
            self._domain_patterns_cache = self._load_pattern_file(
                "domain_patterns.yaml"
            )
        return self._domain_patterns_cache

    def load_content_patterns(self) -> dict[str, dict[str, list[str]]]:
        """Load content type patterns.

        Returns:
            Dictionary of content type patterns with confidence levels.
        """
        if self._content_patterns_cache is None:
            self._content_patterns_cache = self._load_pattern_file(
                "content_patterns.yaml"
            )
        return self._content_patterns_cache

    def _load_pattern_file(self, filename: str) -> dict[str, dict[str, list[str]]]:
        """Load patterns from a YAML file.

        Args:
            filename: Name of the YAML file to load.

        Returns:
            Dictionary of patterns loaded from the file.

        Raises:
            FileNotFoundError: If the pattern file doesn't exist.
            yaml.YAMLError: If the YAML file is malformed.
        """
        file_path = self.patterns_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Pattern file not found: {file_path}")

        try:
            with open(file_path, encoding="utf-8") as f:
                patterns = yaml.safe_load(f)

            # Validate pattern structure
            self._validate_patterns(patterns, filename)
            return patterns

        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing {filename}: {e}") from e

    def _validate_patterns(self, patterns: dict[str, Any], filename: str) -> None:
        """Validate that patterns have the expected structure.

        Args:
            patterns: The loaded patterns dictionary.
            filename: Name of the file being validated (for error messages).

        Raises:
            ValueError: If pattern structure is invalid.
        """
        if not isinstance(patterns, dict):
            raise ValueError(
                f"Invalid pattern file {filename}: root must be a dictionary"
            )

        for pattern_name, pattern_data in patterns.items():
            if not isinstance(pattern_data, dict):
                raise ValueError(
                    f"Invalid pattern {pattern_name} in {filename}: "
                    f"must be a dictionary"
                )

            # Check for required confidence levels
            required_levels = ["high_confidence", "medium_confidence", "keywords"]
            for level in required_levels:
                if level not in pattern_data:
                    raise ValueError(
                        f"Pattern {pattern_name} in {filename} missing required level: "
                        f"{level}"
                    )

                if not isinstance(pattern_data[level], list):
                    raise ValueError(
                        f"Pattern {pattern_name}.{level} in {filename} must be a list"
                    )

    def get_all_patterns(self) -> dict[str, dict[str, dict[str, list[str]]]]:
        """Get all loaded patterns organized by type.

        Returns:
            Dictionary with keys 'tech', 'domain', 'content' containing all patterns.
        """
        return {
            "tech": self.load_tech_patterns(),
            "domain": self.load_domain_patterns(),
            "content": self.load_content_patterns(),
        }

    def reload_patterns(self) -> None:
        """Clear cache and reload all patterns from files.

        This is useful when pattern files have been modified.
        """
        # Clear the LRU cache to force reload
        self.load_tech_patterns.cache_clear()
        self.load_domain_patterns.cache_clear()
        self.load_content_patterns.cache_clear()

    def get_pattern_files_info(self) -> dict[str, dict[str, Any]]:
        """Get information about pattern files.

        Returns:
            Dictionary with file information including existence and modification time.
        """
        files_info = {}
        pattern_files = [
            "tech_patterns.yaml",
            "domain_patterns.yaml",
            "content_patterns.yaml",
        ]

        for filename in pattern_files:
            file_path = self.patterns_dir / filename
            files_info[filename] = {
                "exists": file_path.exists(),
                "path": str(file_path),
                "modified": file_path.stat().st_mtime if file_path.exists() else None,
            }

        return files_info
