"""Core classification engine for content analysis."""

from dataclasses import dataclass
from enum import Enum

from .pattern_loader import PatternLoader


class ConfidenceLevel(Enum):
    """Confidence levels for AI classifications."""

    VERY_HIGH = 0.9
    HIGH = 0.75
    MEDIUM = 0.6
    LOW = 0.4
    VERY_LOW = 0.2


@dataclass
class ClassificationResult:
    """Result of content classification."""

    tag_type: str
    suggested_value: str
    confidence: float
    reasoning: str
    evidence: list[str]


class ClassificationEngine:
    """Core engine for pattern-based content classification."""

    def __init__(self, pattern_loader: PatternLoader | None = None):
        """Initialize classification engine.

        Args:
            pattern_loader: Custom pattern loader. If None, uses default.
        """
        self.pattern_loader = pattern_loader or PatternLoader()
        self._load_patterns()

    def _load_patterns(self) -> None:
        """Load all classification patterns."""
        all_patterns = self.pattern_loader.get_all_patterns()
        self.tech_patterns = all_patterns["tech"]
        self.domain_patterns = all_patterns["domain"]
        self.content_patterns = all_patterns["content"]

    def classify_content(
        self, content: str, file_path: str = ""
    ) -> list[ClassificationResult]:
        """Classify content using pattern matching.

        Args:
            content: The text content to classify.
            file_path: Optional file path for additional context.

        Returns:
            List of classification results.
        """
        results = []
        content_lower = content.lower()

        # Classify technology
        tech_results = self._classify_patterns(
            content_lower, self.tech_patterns, "tech"
        )
        results.extend(tech_results)

        # Classify domain
        domain_results = self._classify_patterns(
            content_lower, self.domain_patterns, "domain"
        )
        results.extend(domain_results)

        # Classify content type
        type_results = self._classify_patterns(
            content_lower, self.content_patterns, "type"
        )
        results.extend(type_results)

        return results

    def _classify_patterns(
        self, content: str, patterns: dict[str, dict[str, list[str]]], tag_type: str
    ) -> list[ClassificationResult]:
        """Classify content against a set of patterns.

        Args:
            content: Lowercase content to analyze.
            patterns: Pattern dictionary to match against.
            tag_type: Type of tag being classified (tech, domain, type).

        Returns:
            List of classification results for this pattern type.
        """
        results = []

        for pattern_name, pattern_config in patterns.items():
            confidence, evidence = self._calculate_pattern_confidence(
                content, pattern_config
            )

            if confidence > 0.1:  # Minimum threshold
                reasoning = self._generate_reasoning(
                    pattern_name, evidence, confidence, tag_type
                )

                result = ClassificationResult(
                    tag_type=tag_type,
                    suggested_value=pattern_name,
                    confidence=confidence,
                    reasoning=reasoning,
                    evidence=evidence,
                )
                results.append(result)

        # Sort by confidence descending
        results.sort(key=lambda x: x.confidence, reverse=True)
        return results

    def _calculate_pattern_confidence(
        self, content: str, pattern_config: dict[str, list[str]]
    ) -> tuple[float, list[str]]:
        """Calculate confidence score for a pattern match.

        Args:
            content: Content to analyze.
            pattern_config: Pattern configuration with confidence levels.

        Returns:
            Tuple of (confidence_score, evidence_list).
        """
        evidence = []
        score = 0.0

        # High confidence patterns (weight: 1.0)
        for pattern in pattern_config.get("high_confidence", []):
            if pattern.lower() in content:
                evidence.append(f"High confidence: '{pattern}'")
                score += 1.0

        # Medium confidence patterns (weight: 0.6)
        for pattern in pattern_config.get("medium_confidence", []):
            if pattern.lower() in content:
                evidence.append(f"Medium confidence: '{pattern}'")
                score += 0.6

        # Keyword patterns (weight: 0.3)
        for pattern in pattern_config.get("keywords", []):
            if pattern.lower() in content:
                evidence.append(f"Keyword: '{pattern}'")
                score += 0.3

        # Normalize score based on pattern density
        if evidence:
            # Boost score if multiple patterns match
            multiplier = min(1.0 + (len(evidence) - 1) * 0.1, 1.5)
            score *= multiplier

            # Cap at maximum confidence
            score = min(score, 0.95)

        return score, evidence

    def _generate_reasoning(
        self, pattern_name: str, evidence: list[str], confidence: float, tag_type: str
    ) -> str:
        """Generate human-readable reasoning for classification.

        Args:
            pattern_name: Name of the matched pattern.
            evidence: List of evidence that led to this classification.
            confidence: Confidence score.
            tag_type: Type of classification.

        Returns:
            Human-readable reasoning string.
        """
        confidence_desc = self._get_confidence_description(confidence)
        evidence_summary = ", ".join(evidence[:3])  # Limit to top 3

        if len(evidence) > 3:
            evidence_summary += f" (and {len(evidence) - 3} more)"

        return (
            f"{confidence_desc} confidence in {tag_type} '{pattern_name}' "
            f"based on: {evidence_summary}"
        )

    def _get_confidence_description(self, confidence: float) -> str:
        """Convert confidence score to descriptive text.

        Args:
            confidence: Numerical confidence score.

        Returns:
            Descriptive confidence level.
        """
        if confidence >= ConfidenceLevel.VERY_HIGH.value:
            return "Very high"
        elif confidence >= ConfidenceLevel.HIGH.value:
            return "High"
        elif confidence >= ConfidenceLevel.MEDIUM.value:
            return "Medium"
        elif confidence >= ConfidenceLevel.LOW.value:
            return "Low"
        else:
            return "Very low"

    def get_supported_patterns(self) -> dict[str, list[str]]:
        """Get list of all supported patterns by type.

        Returns:
            Dictionary mapping pattern types to pattern names.
        """
        return {
            "tech": list(self.tech_patterns.keys()),
            "domain": list(self.domain_patterns.keys()),
            "content": list(self.content_patterns.keys()),
        }

    def reload_patterns(self) -> None:
        """Reload patterns from files.

        Useful when pattern files have been updated.
        """
        self.pattern_loader.reload_patterns()
        self._load_patterns()

    def validate_pattern_files(self) -> dict[str, bool]:
        """Validate that all pattern files are loadable.

        Returns:
            Dictionary mapping file names to validation status.
        """
        validation_results = {}

        try:
            self.pattern_loader.load_tech_patterns()
            validation_results["tech_patterns.yaml"] = True
        except Exception:
            validation_results["tech_patterns.yaml"] = False

        try:
            self.pattern_loader.load_domain_patterns()
            validation_results["domain_patterns.yaml"] = True
        except Exception:
            validation_results["domain_patterns.yaml"] = False

        try:
            self.pattern_loader.load_content_patterns()
            validation_results["content_patterns.yaml"] = True
        except Exception:
            validation_results["content_patterns.yaml"] = False

        return validation_results
