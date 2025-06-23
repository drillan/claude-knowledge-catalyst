"""YAKE keyword extraction integration for enhanced content classification."""

import logging
import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import NamedTuple, Optional

try:
    import langdetect
    import yake
    from unidecode import unidecode

    YAKE_AVAILABLE = True
except ImportError:
    YAKE_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class YAKEConfig:
    """Configuration for YAKE keyword extraction."""

    max_ngram_size: int = 2  # Reduced from 3 for better performance
    deduplication_threshold: float = 0.7
    top_keywords: int = 10  # Reduced from 15 for better performance
    language_auto_detect: bool = True
    supported_languages: list[str] = field(default_factory=lambda: ["en", "ja"])
    min_keyword_length: int = 2
    max_keyword_length: int = 30  # Reduced from 50 for memory efficiency
    cache_size: int = 500  # Reduced from 1000 for memory efficiency
    enable_normalization: bool = True
    confidence_threshold: float = 0.2  # Increased for better filtering
    enable_content_filtering: bool = True  # New: Enable pre-filtering for large content
    max_content_length: int = 5000  # New: Limit content length for processing


class Keyword(NamedTuple):
    """Keyword extraction result."""

    text: str
    score: float
    language: str
    confidence: float


class LanguageDetector:
    """Language detection with optimized caching."""

    def __init__(self, cache_size: int = 200):
        self._cache_size = cache_size

    @lru_cache(maxsize=200)  # Reduced cache size for memory efficiency
    def detect_language(self, text: str) -> str:
        """Detect the primary language of the text."""
        if not YAKE_AVAILABLE:
            return "en"

        try:
            # Clean text for better detection
            clean_text = self._clean_for_detection(text)
            if len(clean_text) < 10:
                return "en"  # Default for short text

            detected = langdetect.detect(clean_text)

            # Map common language codes
            language_map = {
                "ja": "ja",
                "en": "en",
                "zh-cn": "zh",
                "zh-tw": "zh",
                "ko": "ko",
                "fr": "fr",
                "de": "de",
                "es": "es",
            }

            return language_map.get(detected, "en")

        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
            return "en"

    def _clean_for_detection(self, text: str) -> str:
        """Clean text for better language detection."""
        # Remove code blocks
        text = re.sub(r"```[\s\S]*?```", "", text)
        # Remove inline code
        text = re.sub(r"`[^`]+`", "", text)
        # Remove URLs
        text = re.sub(r"https?://\S+", "", text)
        # Remove excessive whitespace
        text = re.sub(r"\s+", " ", text)

        return text.strip()


class TextNormalizer:
    """Text normalization for keyword extraction."""

    @staticmethod
    def normalize_text(text: str, enable_unicode_normalization: bool = True) -> str:
        """Normalize text for better keyword extraction."""
        if not enable_unicode_normalization:
            return text

        try:
            # Unicode normalization for mixed-script text
            normalized = unidecode(text) if YAKE_AVAILABLE else text

            # Preserve important technical terms
            technical_patterns = [
                (r"\bAPI\b", "API"),
                (r"\bURL\b", "URL"),
                (r"\bHTTP\b", "HTTP"),
                (r"\bJSON\b", "JSON"),
                (r"\bXML\b", "XML"),
                (r"\bSQL\b", "SQL"),
                (r"\bCSS\b", "CSS"),
                (r"\bHTML\b", "HTML"),
                (r"\bUI\b", "UI"),
                (r"\bUX\b", "UX"),
            ]

            for pattern, replacement in technical_patterns:
                normalized = re.sub(
                    pattern, replacement, normalized, flags=re.IGNORECASE
                )

            return normalized

        except Exception as e:
            logger.warning(f"Text normalization failed: {e}")
            return text


class YAKEKeywordExtractor:
    """YAKE-based keyword extraction with multi-language support."""

    def __init__(self, config: YAKEConfig | None = None):
        """Initialize YAKE keyword extractor."""
        self.config = config or YAKEConfig()
        self.language_detector = LanguageDetector()
        self.text_normalizer = TextNormalizer()
        self._extractors: dict[str, yake.KeywordExtractor] = {}

        if not YAKE_AVAILABLE:
            logger.warning(
                "YAKE dependencies not available. Keyword extraction will be disabled."
            )
            return

        # Initialize extractors for supported languages
        self._initialize_extractors()

    def _initialize_extractors(self) -> None:
        """Initialize YAKE extractors for each supported language."""
        if not YAKE_AVAILABLE:
            return

        for lang in self.config.supported_languages:
            try:
                extractor = yake.KeywordExtractor(
                    lan=lang,
                    n=self.config.max_ngram_size,
                    dedupLim=self.config.deduplication_threshold,
                    top=self.config.top_keywords,
                    features=None,
                )
                self._extractors[lang] = extractor
                logger.debug(f"Initialized YAKE extractor for language: {lang}")

            except Exception as e:
                logger.warning(f"Failed to initialize YAKE extractor for {lang}: {e}")

    def extract_keywords(
        self, content: str, language: str | None = None
    ) -> list[Keyword]:
        """Extract keywords from content using YAKE with optimized processing."""
        if not YAKE_AVAILABLE:
            logger.warning("YAKE not available, returning empty keyword list")
            return []

        if not content or len(content.strip()) < self.config.min_keyword_length:
            return []

        try:
            # Pre-filter content for performance
            if self.config.enable_content_filtering:
                content = self._prefilter_content(content)
                if len(content) < self.config.min_keyword_length:
                    return []

            # Detect language if not provided (with content hash for caching)
            if language is None and self.config.language_auto_detect:
                # Use first 500 chars for language detection to reduce cache memory
                detection_sample = content[:500]
                language = self.language_detector.detect_language(detection_sample)

            language = language or "en"

            # Get appropriate extractor
            extractor = self._get_extractor(language)
            if not extractor:
                logger.warning(f"No extractor available for language: {language}")
                return []

            # Normalize text
            if self.config.enable_normalization:
                processed_content = self.text_normalizer.normalize_text(content)
            else:
                processed_content = content

            # Extract keywords
            raw_keywords = extractor.extract_keywords(processed_content)

            # Debug: Print the format of raw_keywords
            if raw_keywords:
                logger.debug(
                    f"YAKE raw keywords sample: {raw_keywords[0]} (type: {type(raw_keywords[0])})"
                )

            # Process and filter results
            keywords = self._process_keywords(raw_keywords, language)

            logger.debug(
                f"Extracted {len(keywords)} keywords from {len(content)} chars"
            )
            return keywords

        except Exception as e:
            logger.error(f"Keyword extraction failed: {e}")
            return []

    def _get_extractor(self, language: str) -> Optional["yake.KeywordExtractor"]:
        """Get YAKE extractor for specified language."""
        extractor = self._extractors.get(language)

        # Fallback to English if language not supported
        if not extractor and language != "en":
            extractor = self._extractors.get("en")
            logger.debug(f"Using English extractor as fallback for: {language}")

        return extractor

    def _prefilter_content(self, content: str) -> str:
        """Pre-filter content for optimal YAKE processing."""
        # Limit content length for performance
        if len(content) > self.config.max_content_length:
            # Take first and last portions to preserve important content
            half_limit = self.config.max_content_length // 2
            content = content[:half_limit] + content[-half_limit:]

        # Remove excessive code blocks that add noise
        import re

        # Limit consecutive code blocks
        content = re.sub(
            r"(```[\s\S]*?```\s*){3,}",
            lambda m: "```\n[Multiple code blocks truncated for performance]\n```\n",
            content,
        )

        # Remove very long lines that are likely data/logs
        lines = content.split("\n")
        filtered_lines = []
        for line in lines:
            if len(line) > 200:
                # Keep first 100 chars of long lines
                filtered_lines.append(line[:100] + "...")
            else:
                filtered_lines.append(line)

        return "\n".join(filtered_lines)

    def _process_keywords(
        self, raw_keywords: list[tuple[str, float]], language: str
    ) -> list[Keyword]:
        """Process and filter raw YAKE keywords."""
        keywords = []

        for text, score in raw_keywords:
            # Filter by length - ensure text is string
            text_str = str(text) if not isinstance(text, str) else text
            if not (
                self.config.min_keyword_length
                <= len(text_str)
                <= self.config.max_keyword_length
            ):
                continue

            # Filter by score (lower is better in YAKE) - ensure score is numeric
            score_float = float(score) if not isinstance(score, (int, float)) else score
            if score_float > (1.0 - self.config.confidence_threshold):
                continue

            # Clean keyword text
            cleaned_text = self._clean_keyword(text_str)
            if not cleaned_text:
                continue

            # Calculate confidence (inverse of YAKE score) - use already converted score
            confidence = max(0.0, 1.0 - score_float)

            keywords.append(
                Keyword(
                    text=cleaned_text,
                    score=score_float,
                    language=language,
                    confidence=confidence,
                )
            )

        # Sort by confidence (descending)
        keywords.sort(key=lambda k: k.confidence, reverse=True)

        return keywords[: self.config.top_keywords]

    def _clean_keyword(self, text: str) -> str:
        """Clean and validate keyword text."""
        # Remove extra whitespace
        text = " ".join(text.split())

        # Remove surrounding punctuation
        text = text.strip(".,;:!?()[]{}\"'-")

        # Skip if only punctuation/numbers
        if not re.search(r"[a-zA-Z\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]", text):
            return ""

        # Skip common stop patterns
        stop_patterns = [
            r"^\d+$",  # Only numbers
            r"^[^\w\s]+$",  # Only punctuation
            r"^\s*$",  # Only whitespace
        ]

        for pattern in stop_patterns:
            if re.match(pattern, text):
                return ""

        return text

    def extract_keywords_batch(self, contents: list[str]) -> list[list[Keyword]]:
        """Extract keywords from multiple documents efficiently."""
        results = []

        for content in contents:
            keywords = self.extract_keywords(content)
            results.append(keywords)

        return results

    def get_extractor_info(self) -> dict[str, any]:
        """Get information about available extractors."""
        return {
            "yake_available": YAKE_AVAILABLE,
            "supported_languages": self.config.supported_languages,
            "initialized_extractors": list(self._extractors.keys()),
            "config": self.config.__dict__,
        }


def create_yake_extractor(config: YAKEConfig | None = None) -> YAKEKeywordExtractor:
    """Convenience function to create YAKE extractor."""
    return YAKEKeywordExtractor(config)
