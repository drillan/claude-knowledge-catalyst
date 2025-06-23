"""Refactored intelligent content classification system.

This module provides a clean, modular approach to content classification
using pattern matching and optional YAKE keyword extraction.
"""

from pathlib import Path

from ..core.metadata import KnowledgeMetadata
from ..core.tag_standards import TagStandardsManager
from .classification_engine import ClassificationEngine, ClassificationResult
from .pattern_loader import PatternLoader

# YAKE integration (optional)
try:
    from .yake_extractor import YAKE_AVAILABLE, YAKEConfig, YAKEKeywordExtractor
except ImportError:
    YAKE_AVAILABLE = False
    YAKEKeywordExtractor = None
    YAKEConfig = None


class SmartContentClassifier:
    """AI-powered content classifier using pattern recognition and optional NLP.

    This refactored version provides:
    - Modular pattern loading from YAML files
    - Separation of concerns between pattern matching and YAKE integration
    - Improved maintainability and testability
    - Backward compatibility with existing API
    """

    def __init__(self, enable_yake: bool = True, patterns_dir: Path | None = None):
        """Initialize the content classifier.

        Args:
            enable_yake: Whether to enable YAKE keyword extraction.
            patterns_dir: Custom directory for pattern files. If None, uses default.
        """
        self.tag_standards = TagStandardsManager()
        self.enable_yake = enable_yake and YAKE_AVAILABLE

        # Initialize core classification engine
        pattern_loader = PatternLoader(patterns_dir)
        self.classification_engine = ClassificationEngine(pattern_loader)

        # Backward compatibility: expose patterns as attributes for existing tests
        self.tech_patterns = self.classification_engine.tech_patterns
        self.domain_patterns = self.classification_engine.domain_patterns
        self.type_patterns = (
            self.classification_engine.content_patterns
        )  # Note: renamed from type to content

        # Initialize YAKE extractor if available and enabled
        self.yake_extractor = None
        if self.enable_yake:
            self._initialize_yake()

    def _initialize_yake(self) -> None:
        """Initialize YAKE keyword extractor with optimized configuration."""
        try:
            yake_config = YAKEConfig(
                max_ngram_size=2,  # Optimized for performance
                top_keywords=8,  # Reduced for efficiency
                confidence_threshold=0.3,  # Higher threshold for better quality
                enable_content_filtering=True,
                max_content_length=3000,  # Limit for UI responsiveness
                cache_size=300,  # Smaller cache for memory efficiency
            )
            self.yake_extractor = YAKEKeywordExtractor(yake_config)
        except Exception:
            self.enable_yake = False
            self.yake_extractor = None

    def classify_content(
        self, content: str, file_path: str = ""
    ) -> list[ClassificationResult]:
        """Classify content using pattern matching and optional YAKE enhancement.

        Args:
            content: The text content to classify.
            file_path: Optional file path for additional context.

        Returns:
            List of classification results sorted by confidence.
        """
        # Get base classification from pattern engine
        results = self.classification_engine.classify_content(content, file_path)

        # Enhance with YAKE if available
        if self.enable_yake and self.yake_extractor:
            results = self._enhance_with_yake(content, results)

        # Add complexity and confidence classifications
        results.extend(self._classify_complexity(content))
        results.extend(self._classify_confidence(content))

        # Deduplicate and sort by confidence
        results = self._deduplicate_results(results)
        results.sort(key=lambda x: x.confidence, reverse=True)

        return results

    def _enhance_with_yake(
        self, content: str, pattern_results: list[ClassificationResult]
    ) -> list[ClassificationResult]:
        """Enhance pattern-based results with YAKE keyword extraction.

        Args:
            content: Original content for YAKE analysis.
            pattern_results: Results from pattern matching.

        Returns:
            Enhanced classification results.
        """
        try:
            # Skip YAKE for very short content to save processing
            if len(content.strip()) < 50:
                return pattern_results

            # Extract keywords using YAKE
            yake_keywords = self.yake_extractor.extract_keywords(content)
            if not yake_keywords:  # Early return if no keywords found
                return pattern_results

            keyword_texts = [
                kw.text.lower() for kw in yake_keywords[:5]
            ]  # Limit to top 5 for efficiency

            # Enhance existing results with YAKE confidence
            enhanced_results = []
            for result in pattern_results:
                enhanced_result = result

                # Boost confidence if YAKE found related keywords (optimized check)
                result_value_lower = result.suggested_value.lower()
                if any(
                    keyword in result_value_lower or result_value_lower in keyword
                    for keyword in keyword_texts
                ):
                    enhanced_result.confidence = min(0.95, result.confidence + 0.1)
                    enhanced_result.evidence.append("YAKE keyword validation")

                enhanced_results.append(enhanced_result)

            # Add new tech tags discovered by YAKE
            tech_keywords = self._extract_tech_from_yake(yake_keywords)
            for tech, confidence in tech_keywords.items():
                # Only add if not already detected by patterns
                existing_tech = [
                    r.suggested_value for r in enhanced_results if r.tag_type == "tech"
                ]
                if tech not in existing_tech:
                    enhanced_results.append(
                        ClassificationResult(
                            tag_type="tech",
                            suggested_value=tech,
                            confidence=confidence,
                            reasoning=f"YAKE keyword extraction detected {tech}",
                            evidence=[f"YAKE keyword: {tech}"],
                        )
                    )

            return enhanced_results

        except Exception:
            # If YAKE fails, return original results
            return pattern_results

    def _extract_tech_from_yake(self, keywords: list) -> dict[str, float]:
        """Extract technology tags from YAKE keywords.

        Args:
            keywords: List of YAKE keyword objects.

        Returns:
            Dictionary mapping technology names to confidence scores.
        """
        tech_mapping = {
            "fastapi": 0.8,
            "react": 0.8,
            "python": 0.8,
            "javascript": 0.8,
            "typescript": 0.8,
            "docker": 0.8,
            "kubernetes": 0.8,
            "postgresql": 0.7,
            "mysql": 0.7,
            "mongodb": 0.7,
            "redis": 0.7,
            "aws": 0.7,
            "azure": 0.7,
            "gcp": 0.7,
            "terraform": 0.7,
            "ansible": 0.7,
            "jenkins": 0.7,
            "nginx": 0.6,
            "apache": 0.6,
            "linux": 0.6,
            "ubuntu": 0.6,
            "windows": 0.6,
            "macos": 0.6,
        }

        detected_tech = {}
        for keyword in keywords:
            keyword_text = keyword.text.lower()
            if keyword_text in tech_mapping:
                # Use YAKE confidence (inverted) combined with our mapping
                yake_confidence = 1.0 - min(keyword.score, 1.0)
                mapped_confidence = tech_mapping[keyword_text]
                combined_confidence = (yake_confidence + mapped_confidence) / 2
                detected_tech[keyword_text] = combined_confidence

        return detected_tech

    def _classify_complexity(self, content: str) -> list[ClassificationResult]:
        """Classify content complexity based on length and technical depth.

        Args:
            content: Content to analyze.

        Returns:
            List with complexity classification result.
        """
        content_lower = content.lower()
        content_length = len(content)

        # Technical complexity indicators
        advanced_indicators = [
            "algorithm",
            "optimization",
            "performance",
            "scalability",
            "architecture",
            "design pattern",
            "distributed",
            "concurrent",
            "async",
            "parallel",
            "microservice",
            "infrastructure",
        ]

        beginner_indicators = [
            "basic",
            "simple",
            "introduction",
            "tutorial",
            "getting started",
            "hello world",
            "quick start",
            "beginner",
            "learn",
        ]

        advanced_count = sum(1 for ind in advanced_indicators if ind in content_lower)
        beginner_count = sum(1 for ind in beginner_indicators if ind in content_lower)

        # Determine complexity
        if advanced_count > beginner_count and advanced_count > 2:
            complexity = "advanced"
            confidence = 0.7
        elif beginner_count > 0 or content_length < 500:
            complexity = "beginner"
            confidence = 0.6
        else:
            complexity = "intermediate"
            confidence = 0.5

        return [
            ClassificationResult(
                tag_type="complexity",
                suggested_value=complexity,
                confidence=confidence,
                reasoning=f"Content analysis suggests {complexity} complexity level",
                evidence=[
                    f"Advanced indicators: {advanced_count}, Beginner indicators: {beginner_count}"
                ],
            )
        ]

    def _classify_confidence(self, content: str) -> list[ClassificationResult]:
        """Classify confidence level based on content quality indicators.

        Args:
            content: Content to analyze.

        Returns:
            List with confidence classification result.
        """
        content_lower = content.lower()

        high_confidence_indicators = [
            "tested",
            "proven",
            "production",
            "verified",
            "validated",
            "best practice",
            "recommended",
            "standard",
            "official",
            "stable",
            "mature",
            "released",
        ]

        low_confidence_indicators = [
            "draft",
            "experimental",
            "wip",
            "work in progress",
            "todo",
            "untested",
            "rough",
            "initial",
            "placeholder",
            "beta",
            "alpha",
            "unstable",
        ]

        high_count = sum(
            1 for ind in high_confidence_indicators if ind in content_lower
        )
        low_count = sum(1 for ind in low_confidence_indicators if ind in content_lower)

        if high_count > low_count and high_count > 0:
            confidence_level = "high"
            score = 0.7
        elif low_count > high_count and low_count > 0:
            confidence_level = "low"
            score = 0.6
        else:
            confidence_level = "medium"
            score = 0.5

        return [
            ClassificationResult(
                tag_type="confidence",
                suggested_value=confidence_level,
                confidence=score,
                reasoning=f"Quality indicators suggest {confidence_level} confidence",
                evidence=[
                    f"High indicators: {high_count}, Low indicators: {low_count}"
                ],
            )
        ]

    def _deduplicate_results(
        self, results: list[ClassificationResult]
    ) -> list[ClassificationResult]:
        """Remove duplicate results, keeping the highest confidence for each tag type + value.

        Args:
            results: List of classification results.

        Returns:
            Deduplicated list of results.
        """
        seen = {}
        for result in results:
            key = (result.tag_type, result.suggested_value)
            if key not in seen or result.confidence > seen[key].confidence:
                seen[key] = result

        return list(seen.values())

    def get_supported_patterns(self) -> dict[str, list[str]]:
        """Get all supported classification patterns.

        Returns:
            Dictionary mapping pattern types to pattern names.
        """
        return self.classification_engine.get_supported_patterns()

    def reload_patterns(self) -> None:
        """Reload classification patterns from files."""
        self.classification_engine.reload_patterns()

    def validate_configuration(self) -> dict[str, bool]:
        """Validate that all components are properly configured.

        Returns:
            Dictionary with validation results for each component.
        """
        validation = {
            "pattern_files": True,
            "yake_available": YAKE_AVAILABLE,
            "yake_enabled": self.enable_yake,
            "tag_standards": self.tag_standards is not None,
        }

        # Validate pattern files
        try:
            pattern_validation = self.classification_engine.validate_pattern_files()
            validation["pattern_files"] = all(pattern_validation.values())
            validation.update(pattern_validation)
        except Exception:
            validation["pattern_files"] = False

        return validation

    # Backward compatibility methods for existing tests
    def classify_technology(self, content: str) -> ClassificationResult:
        """Classify technology from content - returns single best match."""
        results = self.classification_engine._classify_patterns(
            content.lower(), self.tech_patterns, "tech"
        )

        if self.enable_yake and self.yake_extractor:
            results = self._enhance_with_yake(content, results)

        if not results:
            return ClassificationResult(
                tag_type="tech",
                suggested_value="unknown",
                confidence=0.2,
                reasoning="No technology patterns detected",
                evidence=[],
            )

        # Return highest confidence result
        best_result = max(results, key=lambda x: x.confidence)
        return best_result

    def classify_category(self, content: str) -> ClassificationResult:
        """Classify content category - returns single best match."""
        results = self.classification_engine._classify_patterns(
            content.lower(), self.type_patterns, "type"
        )

        if not results:
            return ClassificationResult(
                tag_type="type",
                suggested_value="unknown",
                confidence=0.2,
                reasoning="No category patterns detected",
                evidence=[],
            )

        # Return highest confidence result
        best_result = max(results, key=lambda x: x.confidence)
        return best_result

    def classify_complexity(self, content: str) -> ClassificationResult:
        """Classify content complexity - returns single best match."""
        results = self._classify_complexity(content)

        if not results:
            return ClassificationResult(
                tag_type="complexity",
                suggested_value="intermediate",
                confidence=0.3,
                reasoning="No complexity patterns detected, defaulting to intermediate",
                evidence=[],
            )

        # Return the single result (complexity classification returns one result)
        return results[0]

    def _extract_yake_keywords(self, content: str) -> list[str]:
        """Extract YAKE keywords as strings for backward compatibility."""
        if not self.enable_yake or not self.yake_extractor:
            return []

        try:
            yake_keywords = self.yake_extractor.extract_keywords(content)
            return [kw.text for kw in yake_keywords]
        except Exception:
            return []

    def generate_tag_suggestions(self, content: str) -> list[ClassificationResult]:
        """Generate comprehensive tag suggestions for content."""
        return self.classify_content(content)

    def enhance_metadata(
        self, metadata: KnowledgeMetadata, content: str
    ) -> KnowledgeMetadata:
        """Enhance existing metadata with AI-generated suggestions."""
        # Get classification suggestions
        suggestions = self.generate_tag_suggestions(content)

        # Create enhanced metadata using current metadata fields
        enhanced = KnowledgeMetadata(
            title=metadata.title,
            created=metadata.created,
            updated=metadata.updated,
            version=metadata.version,
            type=metadata.type,
            status=metadata.status,
            tech=metadata.tech.copy() if metadata.tech else [],
            domain=metadata.domain.copy() if metadata.domain else [],
            success_rate=metadata.success_rate,
            complexity=metadata.complexity,
            confidence=metadata.confidence,
            projects=metadata.projects.copy() if metadata.projects else [],
            team=metadata.team.copy() if metadata.team else [],
            claude_model=metadata.claude_model.copy() if metadata.claude_model else [],
            claude_feature=metadata.claude_feature.copy()
            if metadata.claude_feature
            else [],
            tags=metadata.tags.copy() if metadata.tags else [],
            author=metadata.author,
            source=metadata.source,
            checksum=metadata.checksum,
            purpose=metadata.purpose,
        )

        # Add high-confidence suggestions to appropriate fields
        new_tags = set(enhanced.tags)

        for suggestion in suggestions:
            if suggestion.confidence >= 0.6:  # Medium confidence threshold
                # Add as appropriate field or tag
                if suggestion.tag_type == "tech":
                    if suggestion.suggested_value not in enhanced.tech:
                        enhanced.tech.append(suggestion.suggested_value)

                elif suggestion.tag_type == "domain":
                    if suggestion.suggested_value not in enhanced.domain:
                        enhanced.domain.append(suggestion.suggested_value)

                elif suggestion.tag_type == "type" and enhanced.type == "prompt":
                    # Only override default type
                    enhanced.type = suggestion.suggested_value

                elif suggestion.tag_type == "complexity" and not enhanced.complexity:
                    enhanced.complexity = suggestion.suggested_value

                elif suggestion.tag_type == "claude_feature":
                    if suggestion.suggested_value not in enhanced.claude_feature:
                        enhanced.claude_feature.append(suggestion.suggested_value)

                # Always add as tag if not already present
                tag_value = suggestion.suggested_value.replace("_", "-")
                new_tags.add(tag_value)

        enhanced.tags = list(new_tags)

        return enhanced
