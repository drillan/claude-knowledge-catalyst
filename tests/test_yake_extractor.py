"""Tests for YAKE keyword extraction functionality."""

from unittest.mock import patch

import pytest

from claude_knowledge_catalyst.ai.yake_extractor import (
    YAKE_AVAILABLE,
    Keyword,
    LanguageDetector,
    TextNormalizer,
    YAKEConfig,
    YAKEKeywordExtractor,
    create_yake_extractor,
)


class TestYAKEConfig:
    """Test suite for YAKEConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = YAKEConfig()

        assert config.max_ngram_size == 2  # Optimized default
        assert config.deduplication_threshold == 0.7
        assert config.top_keywords == 10  # Optimized default
        assert config.language_auto_detect is True
        assert "en" in config.supported_languages
        assert "ja" in config.supported_languages
        assert config.min_keyword_length == 2
        assert config.max_keyword_length == 30  # Optimized default
        assert config.cache_size == 500  # Optimized default
        assert config.enable_normalization is True
        assert config.confidence_threshold == 0.2  # Optimized default
        assert config.enable_content_filtering is True  # New optimization
        assert config.max_content_length == 5000  # New optimization

    def test_custom_config(self):
        """Test custom configuration."""
        config = YAKEConfig(
            max_ngram_size=2,
            top_keywords=10,
            supported_languages=["en"],
            enable_normalization=False,
        )

        assert config.max_ngram_size == 2
        assert config.top_keywords == 10
        assert config.supported_languages == ["en"]
        assert config.enable_normalization is False


class TestLanguageDetector:
    """Test suite for LanguageDetector."""

    @pytest.fixture
    def detector(self):
        """Create language detector instance."""
        return LanguageDetector()

    def test_language_detection_english(self, detector):
        """Test English language detection."""
        text = "This is a sample English text about machine learning and artificial intelligence."

        result = detector.detect_language(text)
        assert result in ["en", "en"]  # Should detect English

    def test_language_detection_short_text(self, detector):
        """Test language detection with short text."""
        text = "Hi"

        result = detector.detect_language(text)
        assert result == "en"  # Should default to English for short text

    def test_clean_for_detection(self, detector):
        """Test text cleaning for language detection."""
        text_with_code = """
        # Python Code Example
        ```python
        def hello():
            print("Hello World")
        ```

        This is a sample text with `inline code` and URLs https://example.com
        that should be cleaned for better language detection.
        """

        cleaned = detector._clean_for_detection(text_with_code)

        assert "```" not in cleaned
        assert "def hello" not in cleaned
        assert "`inline code`" not in cleaned
        assert "https://example.com" not in cleaned
        assert "sample text" in cleaned

    @patch("claude_knowledge_catalyst.ai.yake_extractor.YAKE_AVAILABLE", False)
    def test_fallback_when_dependencies_missing(self, detector):
        """Test fallback behavior when YAKE dependencies are missing."""
        text = "Some text in any language"

        result = detector.detect_language(text)
        assert result == "en"


class TestTextNormalizer:
    """Test suite for TextNormalizer."""

    def test_normalize_text_basic(self):
        """Test basic text normalization."""
        text = "This is a sample text with API and URL references."

        result = TextNormalizer.normalize_text(text)

        # Should preserve technical terms
        assert "API" in result
        assert "URL" in result

    def test_normalize_text_disabled(self):
        """Test normalization when disabled."""
        text = "Special characters: àéîöü"

        result = TextNormalizer.normalize_text(text, enable_unicode_normalization=False)
        assert result == text

    def test_technical_terms_preservation(self):
        """Test that important technical terms are preserved."""
        text = "Working with json api and html css"

        result = TextNormalizer.normalize_text(text)

        # Should normalize to uppercase for technical terms
        assert "JSON" in result.upper()
        assert "API" in result.upper()
        assert "HTML" in result.upper()
        assert "CSS" in result.upper()


@pytest.mark.skipif(not YAKE_AVAILABLE, reason="YAKE dependencies not available")
class TestYAKEKeywordExtractor:
    """Test suite for YAKEKeywordExtractor when dependencies are available."""

    @pytest.fixture
    def extractor(self):
        """Create YAKE extractor instance."""
        config = YAKEConfig(top_keywords=10)
        return YAKEKeywordExtractor(config)

    @pytest.fixture
    def sample_tech_content(self):
        """Sample technical content for testing."""
        return """
        # Machine Learning Pipeline

        This document describes a machine learning pipeline using Python and scikit-learn.
        The pipeline includes data preprocessing, feature extraction, model training, and evaluation.

        ## Key Components
        - Data validation and cleaning
        - Feature engineering with pandas
        - Model selection and hyperparameter tuning
        - Performance evaluation metrics

        The implementation uses modern DevOps practices including CI/CD, containerization with Docker,
        and deployment to cloud infrastructure.
        """

    @pytest.fixture
    def sample_japanese_content(self):
        """Sample Japanese technical content."""
        return """
        機械学習アルゴリズム

        この文書では、Pythonを使用した機械学習の実装について説明します。
        データ分析、特徴量エンジニアリング、モデル学習の各段階を含みます。

        主要な技術：
        - データ前処理とクリーニング
        - scikit-learnを用いたモデル構築
        - アーキテクチャ設計
        - パフォーマンス評価
        """

    def test_extractor_initialization(self, extractor):
        """Test extractor initialization."""
        assert extractor.config.top_keywords == 10
        assert len(extractor._extractors) > 0
        assert "en" in extractor._extractors

    def test_extract_keywords_english(self, extractor, sample_tech_content):
        """Test keyword extraction from English content."""
        keywords = extractor.extract_keywords(sample_tech_content)

        assert len(keywords) > 0
        assert len(keywords) <= extractor.config.top_keywords

        # Check keyword structure
        for keyword in keywords:
            assert isinstance(keyword, Keyword)
            assert isinstance(keyword.text, str)
            assert isinstance(keyword.score, float)
            assert isinstance(keyword.confidence, float)
            assert keyword.language == "en"
            assert len(keyword.text) >= extractor.config.min_keyword_length
            assert len(keyword.text) <= extractor.config.max_keyword_length

        # Should contain relevant technical terms
        keyword_texts = [k.text.lower() for k in keywords]
        expected_terms = ["machine learning", "python", "data", "model"]

        found_terms = sum(
            1 for term in expected_terms if any(term in text for text in keyword_texts)
        )
        assert found_terms > 0

    def test_extract_keywords_japanese(self, extractor, sample_japanese_content):
        """Test keyword extraction from Japanese content."""
        keywords = extractor.extract_keywords(sample_japanese_content, language="ja")

        assert len(keywords) > 0

        # Check that Japanese terms are extracted
        keyword_texts = [k.text for k in keywords]
        japanese_patterns = ["機械学習", "Python", "データ", "アルゴリズム"]

        found_japanese = sum(
            1
            for pattern in japanese_patterns
            if any(pattern in text for text in keyword_texts)
        )
        assert found_japanese > 0

    def test_extract_keywords_auto_language_detection(
        self, extractor, sample_tech_content
    ):
        """Test automatic language detection."""
        keywords = extractor.extract_keywords(sample_tech_content)

        assert len(keywords) > 0
        # Should detect English automatically
        assert all(k.language == "en" for k in keywords)

    def test_extract_keywords_empty_content(self, extractor):
        """Test extraction with empty content."""
        keywords = extractor.extract_keywords("")
        assert keywords == []

        keywords = extractor.extract_keywords("   ")
        assert keywords == []

    def test_extract_keywords_short_content(self, extractor):
        """Test extraction with very short content."""
        keywords = extractor.extract_keywords("Hi")
        assert keywords == []  # Too short for meaningful extraction

    def test_extract_keywords_batch(self, extractor, sample_tech_content):
        """Test batch keyword extraction."""
        contents = [
            sample_tech_content,
            "Python programming and software development",
            "Database design and SQL optimization",
        ]

        results = extractor.extract_keywords_batch(contents)

        assert len(results) == len(contents)
        assert all(isinstance(result, list) for result in results)
        assert all(len(result) > 0 for result in results)

    def test_keyword_filtering_by_length(self, extractor):
        """Test that keywords are filtered by length."""
        # Content designed to generate very short and very long keywords
        content = (
            "A B C very-long-technical-term-that-exceeds-maximum-length-significantly"
        )

        keywords = extractor.extract_keywords(content)

        for keyword in keywords:
            assert len(keyword.text) >= extractor.config.min_keyword_length
            assert len(keyword.text) <= extractor.config.max_keyword_length

    def test_confidence_calculation(self, extractor, sample_tech_content):
        """Test confidence score calculation."""
        keywords = extractor.extract_keywords(sample_tech_content)

        for keyword in keywords:
            # Confidence should be between 0 and 1
            assert 0.0 <= keyword.confidence <= 1.0
            # YAKE score should be positive (lower is better)
            assert keyword.score >= 0.0

        # Keywords should be sorted by confidence (descending)
        confidences = [k.confidence for k in keywords]
        assert confidences == sorted(confidences, reverse=True)

    def test_get_extractor_info(self, extractor):
        """Test extractor information retrieval."""
        info = extractor.get_extractor_info()

        assert "yake_available" in info
        assert "supported_languages" in info
        assert "initialized_extractors" in info
        assert "config" in info

        assert info["yake_available"] is True
        assert isinstance(info["supported_languages"], list)
        assert isinstance(info["initialized_extractors"], list)
        assert isinstance(info["config"], dict)


class TestYAKEKeywordExtractorWithoutDependencies:
    """Test suite for YAKEKeywordExtractor when dependencies are not available."""

    @patch("claude_knowledge_catalyst.ai.yake_extractor.YAKE_AVAILABLE", False)
    def test_initialization_without_dependencies(self):
        """Test extractor initialization when YAKE is not available."""
        extractor = YAKEKeywordExtractor()

        assert extractor.config is not None
        assert len(extractor._extractors) == 0

    @patch("claude_knowledge_catalyst.ai.yake_extractor.YAKE_AVAILABLE", False)
    def test_extraction_without_dependencies(self):
        """Test extraction behavior when YAKE is not available."""
        extractor = YAKEKeywordExtractor()

        keywords = extractor.extract_keywords("Sample technical content")
        assert keywords == []

    @patch("claude_knowledge_catalyst.ai.yake_extractor.YAKE_AVAILABLE", False)
    def test_extractor_info_without_dependencies(self):
        """Test extractor info when dependencies are not available."""
        extractor = YAKEKeywordExtractor()

        info = extractor.get_extractor_info()
        assert info["yake_available"] is False


class TestConvenienceFunctions:
    """Test suite for convenience functions."""

    def test_create_yake_extractor_default(self):
        """Test creating extractor with default config."""
        extractor = create_yake_extractor()

        assert isinstance(extractor, YAKEKeywordExtractor)
        assert isinstance(extractor.config, YAKEConfig)

    def test_create_yake_extractor_custom_config(self):
        """Test creating extractor with custom config."""
        config = YAKEConfig(top_keywords=5)
        extractor = create_yake_extractor(config)

        assert isinstance(extractor, YAKEKeywordExtractor)
        assert extractor.config.top_keywords == 5


class TestKeywordNamedTuple:
    """Test suite for Keyword named tuple."""

    def test_keyword_creation(self):
        """Test Keyword named tuple creation."""
        keyword = Keyword(
            text="machine learning", score=0.1, language="en", confidence=0.9
        )

        assert keyword.text == "machine learning"
        assert keyword.score == 0.1
        assert keyword.language == "en"
        assert keyword.confidence == 0.9

    def test_keyword_immutability(self):
        """Test that Keyword is immutable."""
        keyword = Keyword("test", 0.1, "en", 0.9)

        with pytest.raises(AttributeError):
            keyword.text = "modified"


class TestErrorHandling:
    """Test suite for error handling scenarios."""

    @pytest.mark.skipif(not YAKE_AVAILABLE, reason="YAKE dependencies not available")
    def test_extraction_with_invalid_content(self):
        """Test extraction with problematic content."""
        extractor = YAKEKeywordExtractor()

        # Should handle these gracefully without crashing
        test_cases = [
            None,  # This would be caught by the content check
            "",
            "\n\n\n",
            "123 456 789",  # Only numbers
            "!@#$%^&*()",  # Only punctuation
        ]

        for content in test_cases:
            if content is not None:  # Skip None test as it would fail earlier
                keywords = extractor.extract_keywords(content)
                assert isinstance(keywords, list)

    @pytest.mark.skipif(not YAKE_AVAILABLE, reason="YAKE dependencies not available")
    def test_unsupported_language_fallback(self):
        """Test fallback to English for unsupported languages."""
        config = YAKEConfig(supported_languages=["en"])  # Only English
        extractor = YAKEKeywordExtractor(config)

        # Should fall back to English extractor
        keywords = extractor.extract_keywords("Some content", language="fr")

        # Should still work (using English extractor as fallback)
        assert isinstance(keywords, list)
