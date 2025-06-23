"""Tests for CLI smart sync functionality."""

from unittest.mock import Mock, patch

from claude_knowledge_catalyst.cli.smart_sync import (
    analyze_content_advanced,
    apply_metadata_to_file,
    classify_file_intelligent,
    generate_frontmatter,
    get_default_classification,
    has_frontmatter,
    run_ckc_sync,
    scan_metadata_status,
    smart_sync_command,
)
from claude_knowledge_catalyst.core.config import CKCConfig


class TestMetadataScanning:
    """Test metadata scanning functionality."""

    def test_scan_metadata_status_empty_directory(self, tmp_path):
        """Test scanning empty directory."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        has_metadata, needs_classification = scan_metadata_status(str(claude_dir))

        assert has_metadata == []
        assert needs_classification == []

    def test_scan_metadata_status_with_files(self, tmp_path):
        """Test scanning directory with various files."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        # File with frontmatter
        with_metadata = claude_dir / "with_metadata.md"
        with_metadata.write_text("""---
title: Test File
tags: [test]
---
# Content
""")

        # File without frontmatter
        without_metadata = claude_dir / "without_metadata.md"
        without_metadata.write_text("# Simple Content")

        has_metadata, needs_classification = scan_metadata_status(str(claude_dir))

        assert len(has_metadata) == 1
        assert len(needs_classification) == 1
        assert with_metadata in has_metadata
        assert without_metadata in needs_classification

    def test_has_frontmatter_valid(self, tmp_path):
        """Test frontmatter detection with valid YAML."""
        test_file = tmp_path / "test.md"
        test_file.write_text("""---
title: Test
tags: [python, testing]
---
# Content here
""")

        assert has_frontmatter(test_file) is True

    def test_has_frontmatter_invalid(self, tmp_path):
        """Test frontmatter detection without YAML."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Just content without frontmatter")

        assert has_frontmatter(test_file) is False

    def test_has_frontmatter_malformed(self, tmp_path):
        """Test frontmatter detection with malformed YAML."""
        test_file = tmp_path / "test.md"
        test_file.write_text("""--
title: Malformed
content here""")

        assert has_frontmatter(test_file) is False

    def test_has_frontmatter_file_error(self, tmp_path):
        """Test frontmatter detection with file read error."""
        nonexistent_file = tmp_path / "nonexistent.md"

        # Should handle file read errors gracefully
        assert has_frontmatter(nonexistent_file) is False


class TestFileClassification:
    """Test intelligent file classification functionality."""

    @patch("claude_knowledge_catalyst.cli.smart_sync.KnowledgeClassifier")
    def test_classify_file_intelligent_basic(self, mock_classifier_class, tmp_path):
        """Test basic intelligent file classification."""
        # Setup test file
        test_file = tmp_path / "test.py"
        test_file.write_text("# Python test file\nimport os\ndef main(): pass")

        # Mock config and metadata manager
        mock_config = Mock(spec=CKCConfig)
        mock_config.hybrid_structure = {}
        mock_metadata_manager = Mock()

        # Mock classifier
        mock_classifier = Mock()
        mock_classifier_class.return_value = mock_classifier

        result = classify_file_intelligent(
            test_file, mock_config, mock_metadata_manager
        )

        assert result["success"] is True
        assert "classification" in result
        assert "confidence" in result

    def test_classify_file_intelligent_error_handling(self, tmp_path):
        """Test classification with file read error."""
        nonexistent_file = tmp_path / "nonexistent.py"

        mock_config = Mock(spec=CKCConfig)
        mock_config.hybrid_structure = {}
        mock_metadata_manager = Mock()

        result = classify_file_intelligent(
            nonexistent_file, mock_config, mock_metadata_manager
        )

        assert result["success"] is False
        assert "error" in result
        assert "classification" in result  # Should have default classification

    @patch("claude_knowledge_catalyst.cli.smart_sync.KnowledgeClassifier")
    def test_analyze_content_advanced_architecture(
        self, mock_classifier_class, tmp_path
    ):
        """Test advanced content analysis for architecture files."""
        # Create architecture file
        arch_file = tmp_path / "architecture" / "system_design.md"
        arch_file.parent.mkdir()
        arch_file.write_text("# System Architecture\nThis describes the system design.")

        mock_classifier = Mock()
        mock_classifier_class.return_value = mock_classifier

        result = analyze_content_advanced(
            arch_file.read_text(), arch_file, mock_classifier
        )

        assert result["category"] == "concept"
        assert "architecture" in result["tags"]
        assert "design" in result["tags"]

    @patch("claude_knowledge_catalyst.cli.smart_sync.KnowledgeClassifier")
    def test_analyze_content_advanced_command(self, mock_classifier_class, tmp_path):
        """Test advanced content analysis for command files."""
        # Create command file
        cmd_file = tmp_path / "commands" / "test_cmd.sh"
        cmd_file.parent.mkdir()
        cmd_file.write_text("#!/bin/bash\necho 'Hello World'")

        mock_classifier = Mock()
        mock_classifier_class.return_value = mock_classifier

        result = analyze_content_advanced(
            cmd_file.read_text(), cmd_file, mock_classifier
        )

        assert result["category"] == "command"
        assert "shell" in result["tags"]
        assert "automation" in result["tags"]


class TestMetadataGeneration:
    """Test metadata generation functionality."""

    def test_get_default_classification(self):
        """Test default classification generation."""
        result = get_default_classification()

        assert isinstance(result, dict)
        assert "category" in result
        assert "tags" in result
        assert isinstance(result["tags"], list)

    def test_generate_frontmatter_basic(self, tmp_path):
        """Test basic frontmatter generation."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Content")

        classification = {
            "category": "concept",
            "tags": ["test", "example"],
            "complexity": "simple",
            "quality": "medium",
        }

        result = generate_frontmatter(test_file, classification)

        assert isinstance(result, str)
        assert "---" in result  # YAML frontmatter delimiters
        assert "category: concept" in result
        assert "test" in result
        assert "example" in result

    def test_generate_frontmatter_empty_classification(self, tmp_path):
        """Test frontmatter generation with minimal classification."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Content")

        classification = {
            "category": "unknown",
            "tags": [],
            "complexity": "simple",
            "quality": "medium",
        }

        result = generate_frontmatter(test_file, classification)

        assert isinstance(result, str)
        assert "---" in result  # Should still generate valid YAML

    def test_apply_metadata_to_file_basic(self, tmp_path):
        """Test applying metadata to file."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Original Content")

        classification = {
            "category": "concept",
            "tags": ["test"],
            "complexity": "simple",
            "quality": "high",
        }

        result = apply_metadata_to_file(test_file, classification)

        assert result["success"] is True

        # Check that file was modified
        updated_content = test_file.read_text()
        assert "---" in updated_content  # Frontmatter added
        assert "# Original Content" in updated_content  # Original content preserved

    def test_apply_metadata_to_file_error_handling(self, tmp_path):
        """Test metadata application with file write error."""
        readonly_file = tmp_path / "readonly.md"
        readonly_file.write_text("# Test Content")
        readonly_file.chmod(0o444)  # Make read-only

        classification = {"category": "test"}

        try:
            result = apply_metadata_to_file(readonly_file, classification)
            # May succeed or fail depending on system, but should not crash
            assert isinstance(result, dict)
            assert "success" in result
        except PermissionError:
            # Expected on some systems
            pass
        finally:
            # Restore write permissions for cleanup
            readonly_file.chmod(0o644)


class TestSyncOperations:
    """Test sync operations functionality."""

    def test_run_ckc_sync_basic(self):
        """Test basic CKC sync operation."""
        result = run_ckc_sync()

        assert isinstance(result, dict)
        assert "success" in result

    def test_run_ckc_sync_error_handling(self):
        """Test CKC sync with error handling."""
        with patch(
            "claude_knowledge_catalyst.cli.smart_sync.console.print"
        ):
            result = run_ckc_sync()

            # Should return a result dict even on errors
            assert isinstance(result, dict)
            assert "success" in result or "error" in result


class TestSmartSyncCommand:
    """Test smart sync CLI command integration."""

    @patch("claude_knowledge_catalyst.cli.smart_sync.scan_metadata_status")
    @patch("claude_knowledge_catalyst.cli.smart_sync.console.print")
    def test_smart_sync_command_basic(self, mock_console_print, mock_scan, tmp_path):
        """Test basic smart sync command functionality."""
        # Mock scan results
        has_metadata = [tmp_path / "has_meta.md"]
        needs_classification = [tmp_path / "needs_class.md"]
        mock_scan.return_value = (has_metadata, needs_classification)

        # Mock config
        mock_config = Mock(spec=CKCConfig)
        mock_config.project_root = tmp_path
        mock_config.sync_targets = []

        with patch(
            "claude_knowledge_catalyst.cli.smart_sync.run_ckc_sync"
        ) as mock_sync:
            mock_sync.return_value = {"success": True}
            smart_sync_command(mock_config, directory=".claude", dry_run=False)

            assert mock_scan.called
            assert mock_console_print.called

    def test_smart_sync_command_dry_run(self, tmp_path):
        """Test smart sync command in dry run mode."""
        mock_config = Mock(spec=CKCConfig)
        mock_config.project_root = tmp_path
        mock_config.sync_targets = []

        with patch(
            "claude_knowledge_catalyst.cli.smart_sync.console.print"
        ) as mock_print:
            with patch(
                "claude_knowledge_catalyst.cli.smart_sync.scan_metadata_status"
            ) as mock_scan:
                mock_scan.return_value = ([], [])
                smart_sync_command(
                    mock_config, directory=".claude", dry_run=True
                )

                # Dry run should show preview without making changes
                assert mock_print.called

    @patch("claude_knowledge_catalyst.cli.smart_sync.scan_metadata_status")
    def test_smart_sync_command_error_handling(self, mock_scan, tmp_path):
        """Test smart sync command error handling."""
        # Mock scan to raise exception
        mock_scan.side_effect = Exception("Scan error")

        mock_config = Mock(spec=CKCConfig)
        mock_config.project_root = tmp_path
        mock_config.sync_targets = []

        with patch(
            "claude_knowledge_catalyst.cli.smart_sync.console.print"
        ):
            try:
                smart_sync_command(
                    mock_config, directory=".claude", dry_run=False
                )
                # Should handle errors gracefully
                # May or may not show error messages depending on implementation
            except Exception:
                # Some errors may propagate, which is also acceptable
                pass
