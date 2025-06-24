"""Tests for template management."""

import tempfile
from pathlib import Path

import pytest
from claude_knowledge_catalyst.templates.manager import TemplateManager


class TestTemplateManager:
    """Test cases for TemplateManager class."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create temporary directory for templates
        self.temp_dir = tempfile.mkdtemp()
        self.template_dir = Path(self.temp_dir) / "templates"
        self.manager = TemplateManager(self.template_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_template_initialization(self):
        """Test template manager initialization."""
        assert self.template_dir.exists()
        assert self.manager.template_dir == self.template_dir

        # Check that default templates are created
        templates = self.manager.list_templates()
        expected_templates = [
            "prompt.md",
            "code_snippet.md",
            "concept.md",
            "project_log.md",
            "improvement_log.md",
        ]

        for template in expected_templates:
            assert template in templates

    def test_list_templates(self):
        """Test listing available templates."""
        templates = self.manager.list_templates()
        assert isinstance(templates, list)
        assert len(templates) > 0

        # All should be .md files
        for template in templates:
            assert template.endswith(".md")

    def test_get_template(self):
        """Test getting a template by name."""
        template = self.manager.get_template("prompt.md")
        assert template is not None

        # Test template rendering
        content = template.render(
            title="Test Prompt",
            purpose="Testing purposes",
            created_date="2024-01-01",
            version="1.0",
            model="Claude 3 Opus",
            category="prompt",
            status="draft",
            tags=["test", "prompt"],
        )

        assert "Test Prompt" in content
        assert "Testing purposes" in content
        assert "Claude 3 Opus" in content

    def test_create_from_template(self):
        """Test creating files from templates."""
        output_path = Path(self.temp_dir) / "test_output.md"
        variables = {
            "title": "Test Document",
            "purpose": "Testing template creation",
            "created_date": "2024-01-01",
            "version": "1.0",
            "model": "Claude 3 Opus",
            "category": "test",
            "status": "draft",
            "tags": ["test"],
        }

        success = self.manager.create_from_template("prompt.md", output_path, variables)

        assert success is True
        assert output_path.exists()

        content = output_path.read_text()
        assert "Test Document" in content
        assert "Testing template creation" in content

    def test_create_prompt_file(self):
        """Test creating prompt files using helper method."""
        output_path = Path(self.temp_dir) / "test_prompt.md"

        success = self.manager.create_prompt_file(
            title="Test Prompt",
            purpose="This is a test prompt",
            output_path=output_path,
            model="Claude 3 Sonnet",
            tags=["test", "example"],
        )

        assert success is True
        assert output_path.exists()

        content = output_path.read_text()
        assert "Test Prompt" in content
        assert "This is a test prompt" in content
        assert "Claude 3 Sonnet" in content
        assert "test, example" in content

    def test_create_code_snippet_file(self):
        """Test creating code snippet files using helper method."""
        output_path = Path(self.temp_dir) / "test_code.md"

        success = self.manager.create_code_snippet_file(
            title="Test Function",
            language="python",
            description="A test function for demonstration",
            output_path=output_path,
            tags=["python", "function", "test"],
        )

        assert success is True
        assert output_path.exists()

        content = output_path.read_text()
        assert "Test Function" in content
        assert "python" in content
        assert "A test function for demonstration" in content

    def test_create_concept_file(self):
        """Test creating concept files using helper method."""
        output_path = Path(self.temp_dir) / "test_concept.md"

        success = self.manager.create_concept_file(
            title="Test Concept",
            summary="This is a test concept for learning",
            output_path=output_path,
            tags=["learning", "concept"],
        )

        assert success is True
        assert output_path.exists()

        content = output_path.read_text()
        assert "Test Concept" in content
        assert "This is a test concept for learning" in content

    def test_template_not_found(self):
        """Test handling of non-existent templates."""
        from jinja2 import TemplateNotFound

        with pytest.raises(TemplateNotFound):
            self.manager.get_template("non_existent.md")

    def test_create_with_invalid_template(self):
        """Test creating file with non-existent template."""
        output_path = Path(self.temp_dir) / "output.md"

        success = self.manager.create_from_template("non_existent.md", output_path, {})

        assert success is False
        assert not output_path.exists()

    def test_template_variables_escaping(self):
        """Test that template variables are properly escaped."""
        # Create a custom template with potential XSS content
        custom_template_path = self.template_dir / "custom.md"
        custom_template_path.write_text("Title: {{ title }}")

        output_path = Path(self.temp_dir) / "test_escape.md"

        success = self.manager.create_from_template(
            "custom.md", output_path, {"title": "<script>alert('xss')</script>"}
        )

        assert success is True
        content = output_path.read_text()
        # Jinja2 should not escape by default since we're generating markdown
        assert "<script>" in content

    def test_template_with_missing_variables(self):
        """Test template rendering with missing variables."""
        output_path = Path(self.temp_dir) / "test_missing_vars.md"

        # Try to render prompt template with missing variables
        success = self.manager.create_from_template(
            "prompt.md",
            output_path,
            {"title": "Test"},  # Missing other required variables
        )

        # Should still succeed but with undefined variables
        assert success is True
        content = output_path.read_text()
        assert "Test" in content
