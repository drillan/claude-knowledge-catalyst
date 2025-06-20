"""Tests for smart content classification system."""

import pytest
from pathlib import Path
from typing import List, Dict

from claude_knowledge_catalyst.ai.smart_classifier import (
    SmartContentClassifier, 
    ClassificationResult, 
    ConfidenceLevel
)
from claude_knowledge_catalyst.core.metadata import KnowledgeMetadata


class TestSmartContentClassifier:
    """Test suite for SmartContentClassifier."""

    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return SmartContentClassifier()

    @pytest.fixture
    def sample_python_content(self):
        """Sample Python code content."""
        return """```python
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# Usage example
import sys
from pathlib import Path

result = calculate_fibonacci(10)
print(f"Fibonacci(10) = {result}")
```"""

    @pytest.fixture
    def sample_javascript_content(self):
        """Sample JavaScript code content."""
        return """```javascript
const express = require('express');
const app = express();

app.get('/api/users', async (req, res) => {
    try {
        const users = await User.findAll();
        res.json(users);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
```"""

    @pytest.fixture
    def sample_prompt_content(self):
        """Sample prompt content."""
        return """# Code Review Assistant

Please review the following code and provide feedback on:

1. Code quality and readability
2. Performance optimizations
3. Security considerations
4. Best practices compliance

Focus on constructive feedback that helps improve the code while maintaining its functionality."""

    def test_classifier_initialization(self, classifier):
        """Test classifier initialization."""
        assert classifier.tag_standards is not None
        assert hasattr(classifier, 'tech_patterns')
        assert hasattr(classifier, 'category_patterns')
        assert hasattr(classifier, 'complexity_indicators')

    def test_technology_classification_python(self, classifier, sample_python_content):
        """Test Python technology classification."""
        result = classifier.classify_technology(sample_python_content)
        
        assert result.suggested_value == 'python'
        assert result.confidence >= ConfidenceLevel.HIGH.value
        assert 'def ' in result.evidence or 'import ' in result.evidence

    def test_technology_classification_javascript(self, classifier, sample_javascript_content):
        """Test JavaScript technology classification."""
        result = classifier.classify_technology(sample_javascript_content)
        
        assert result.suggested_value == 'javascript'
        assert result.confidence >= ConfidenceLevel.MEDIUM.value
        assert any('const ' in ev or 'require(' in ev for ev in result.evidence)

    def test_category_classification_code(self, classifier, sample_python_content):
        """Test code category classification."""
        result = classifier.classify_category(sample_python_content)
        
        assert result.suggested_value == 'code'
        assert result.confidence >= ConfidenceLevel.MEDIUM.value

    def test_category_classification_prompt(self, classifier, sample_prompt_content):
        """Test prompt category classification."""
        result = classifier.classify_category(sample_prompt_content)
        
        assert result.suggested_value == 'prompt'
        assert result.confidence >= ConfidenceLevel.MEDIUM.value
        assert any('review' in ev.lower() or 'feedback' in ev.lower() for ev in result.evidence)

    def test_complexity_classification_simple(self, classifier):
        """Test complexity classification for simple content."""
        simple_content = "# Simple Note\n\nThis is a basic note with minimal content."
        
        result = classifier.classify_complexity(simple_content)
        
        assert result.suggested_value in ['beginner', 'simple']
        assert result.confidence >= ConfidenceLevel.MEDIUM.value

    def test_complexity_classification_complex(self, classifier, sample_python_content):
        """Test complexity classification for complex content."""
        complex_content = f"""
        # Advanced Python Patterns
        
        {sample_python_content}
        
        ## Design Patterns Implementation
        
        This demonstrates several advanced concepts:
        - Recursive algorithms
        - Performance optimization techniques
        - Error handling strategies
        - Asynchronous programming patterns
        
        The implementation uses metaclasses, decorators, and context managers
        to provide a robust, scalable solution.
        """
        
        result = classifier.classify_complexity(complex_content)
        
        assert result.suggested_value in ['advanced', 'expert', 'complex']
        assert result.confidence >= ConfidenceLevel.MEDIUM.value

    def test_tag_suggestions_generation(self, classifier, sample_python_content):
        """Test comprehensive tag suggestions."""
        suggestions = classifier.generate_tag_suggestions(sample_python_content)
        
        assert len(suggestions) > 0
        
        # Should contain technology tags
        tech_tags = [s for s in suggestions if s.tag_type == 'technology']
        assert len(tech_tags) > 0
        assert any(t.suggested_value == 'python' for t in tech_tags)
        
        # Should contain category tags
        category_tags = [s for s in suggestions if s.tag_type == 'category']
        assert len(category_tags) > 0

    def test_metadata_enhancement(self, classifier, sample_python_content):
        """Test metadata enhancement functionality."""
        initial_metadata = KnowledgeMetadata(
            title="Fibonacci Calculator",
            description="A simple implementation"
        )
        
        enhanced = classifier.enhance_metadata(initial_metadata, sample_python_content)
        
        assert enhanced.title == initial_metadata.title
        assert len(enhanced.tags) > len(initial_metadata.tags)
        assert any('python' in tag for tag in enhanced.tags)

    def test_classification_confidence_levels(self, classifier):
        """Test different confidence levels in classification."""
        # High confidence content
        high_conf_content = "def main(): import os; from pathlib import Path"
        result = classifier.classify_technology(high_conf_content)
        assert result.confidence >= ConfidenceLevel.HIGH.value
        
        # Low confidence content
        low_conf_content = "This is some general text without specific indicators."
        result = classifier.classify_technology(low_conf_content)
        assert result.confidence <= ConfidenceLevel.MEDIUM.value

    def test_edge_cases(self, classifier):
        """Test classification with edge cases."""
        edge_cases = [
            "",  # Empty content
            "   ",  # Whitespace only
            "# Title Only",  # Minimal content
            "Mixed content with python and javascript code together",  # Multiple technologies
        ]
        
        for content in edge_cases:
            try:
                suggestions = classifier.generate_tag_suggestions(content)
                # Should handle gracefully
                assert isinstance(suggestions, list)
            except Exception as e:
                pytest.fail(f"Classifier failed on edge case '{content}': {e}")

    @pytest.mark.parametrize("content,expected_tech", [
        ("pip install numpy\nimport pandas", "python"),
        ("npm install express\nconst app = require('express')", "javascript"),
        ("docker build -t myapp .\nDockerfile content", "docker"),
        ("SELECT * FROM users WHERE id = 1", "sql"),
        ("git commit -m 'Initial commit'\ngit push origin main", "git"),
    ])
    def test_technology_patterns(self, classifier, content, expected_tech):
        """Test specific technology pattern recognition."""
        result = classifier.classify_technology(content)
        assert result.suggested_value == expected_tech

    def test_category_patterns(self, classifier):
        """Test category pattern recognition."""
        test_cases = [
            ("Please help me with this task", "prompt"),
            ("def fibonacci(n): return n if n <= 1", "code"),
            ("Machine learning is a subset of AI", "concept"),
            ("Check out this useful library: https://github.com/", "resource"),
        ]
        
        for content, expected_category in test_cases:
            result = classifier.classify_category(content)
            assert result.suggested_value == expected_category

    def test_multi_technology_content(self, classifier):
        """Test content with multiple technologies."""
        mixed_content = """
        # Full Stack Application
        
        ## Backend (Python)
        ```python
        from flask import Flask
        app = Flask(__name__)
        ```
        
        ## Frontend (JavaScript)
        ```javascript
        const api = fetch('/api/data');
        ```
        
        ## Database (SQL)
        ```sql
        SELECT * FROM users;
        ```
        """
        
        suggestions = classifier.generate_tag_suggestions(mixed_content)
        tech_suggestions = [s for s in suggestions if s.tag_type == 'technology']
        
        # Should detect multiple technologies
        assert len(tech_suggestions) >= 2
        tech_values = {s.suggested_value for s in tech_suggestions}
        assert 'python' in tech_values or 'javascript' in tech_values


class TestClassificationResult:
    """Test suite for ClassificationResult."""

    def test_classification_result_creation(self):
        """Test ClassificationResult creation."""
        result = ClassificationResult(
            tag_type="technology",
            suggested_value="python",
            confidence=0.85,
            reasoning="Contains Python-specific syntax",
            evidence=["def ", "import "]
        )
        
        assert result.tag_type == "technology"
        assert result.suggested_value == "python"
        assert result.confidence == 0.85
        assert "Python" in result.reasoning
        assert len(result.evidence) == 2

    def test_confidence_level_enum(self):
        """Test ConfidenceLevel enum values."""
        assert ConfidenceLevel.VERY_HIGH.value == 0.9
        assert ConfidenceLevel.HIGH.value == 0.75
        assert ConfidenceLevel.MEDIUM.value == 0.6
        assert ConfidenceLevel.LOW.value == 0.4
        assert ConfidenceLevel.VERY_LOW.value == 0.2


class TestClassifierPerformance:
    """Test classifier performance and efficiency."""

    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return SmartContentClassifier()

    def test_large_content_handling(self, classifier):
        """Test classifier with large content."""
        # Create large content (simulate big file)
        large_content = "# Large Python File\n\n" + "def function_{}(): pass\n".format("x" * 100) * 100
        
        # Should handle large content without issues
        result = classifier.classify_technology(large_content)
        assert result.suggested_value == "python"
        assert result.confidence > 0

    def test_batch_classification(self, classifier):
        """Test batch classification of multiple contents."""
        contents = [
            "def python_function(): pass",
            "const jsVariable = 'hello';",
            "Please help me with this prompt",
            "SELECT * FROM database_table",
            "# Concept explanation here"
        ]
        
        results = []
        for content in contents:
            suggestions = classifier.generate_tag_suggestions(content)
            results.append(suggestions)
        
        assert len(results) == len(contents)
        # Each content should get some classification
        assert all(len(r) > 0 for r in results)

    def test_classification_consistency(self, classifier):
        """Test that classification is consistent across multiple runs."""
        content = "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"
        
        # Run classification multiple times
        results = []
        for _ in range(5):
            result = classifier.classify_technology(content)
            results.append(result.suggested_value)
        
        # Should be consistent
        assert all(r == results[0] for r in results)
        assert results[0] == "python"


class TestClassifierIntegration:
    """Integration tests for classifier with other components."""

    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return SmartContentClassifier()

    def test_integration_with_metadata(self, classifier):
        """Test integration with KnowledgeMetadata."""
        content = """
        # API Design Best Practices
        
        ```python
        from fastapi import FastAPI
        app = FastAPI()
        
        @app.get("/users")
        def get_users():
            return {"users": []}
        ```
        
        This demonstrates REST API design patterns.
        """
        
        metadata = KnowledgeMetadata(
            title="API Design Guide",
            description="Best practices for API development"
        )
        
        enhanced = classifier.enhance_metadata(metadata, content)
        
        # Should preserve original data
        assert enhanced.title == metadata.title
        assert enhanced.description == metadata.description
        
        # Should add appropriate tags
        assert any('python' in tag for tag in enhanced.tags)
        assert any('api' in tag for tag in enhanced.tags)
        assert 'code' in enhanced.category or 'concept' in enhanced.category

    def test_tag_standards_integration(self, classifier):
        """Test integration with tag standards system."""
        content = "def advanced_algorithm(): # Complex implementation here"
        
        suggestions = classifier.generate_tag_suggestions(content)
        
        # Should respect tag standards
        for suggestion in suggestions:
            assert suggestion.tag_type in ['technology', 'category', 'complexity', 'domain']
            assert isinstance(suggestion.suggested_value, str)
            assert len(suggestion.suggested_value) > 0