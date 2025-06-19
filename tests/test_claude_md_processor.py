"""Test CLAUDE.md processor functionality."""

import tempfile
from pathlib import Path

import pytest

from src.claude_knowledge_catalyst.core.claude_md_processor import ClaudeMdProcessor


class TestClaudeMdProcessor:
    """Test CLAUDE.md processor."""

    def test_init_without_exclusions(self):
        """Test processor initialization without exclusions."""
        processor = ClaudeMdProcessor()
        assert processor.sections_exclude == []
        assert processor.exclude_patterns == []

    def test_init_with_exclusions(self):
        """Test processor initialization with exclusions."""
        sections = ["# secrets", "# private"]
        processor = ClaudeMdProcessor(sections_exclude=sections)
        assert processor.sections_exclude == sections
        assert len(processor.exclude_patterns) == 2

    def test_process_claude_md_no_exclusions(self):
        """Test processing CLAUDE.md without exclusions."""
        content = """# Project Overview
This is a test project.

# Commands
Run tests with pytest.

# Secrets
API_KEY=secret123
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            
            processor = ClaudeMdProcessor()
            result = processor.process_claude_md(Path(f.name))
            
            assert result == content
            
        Path(f.name).unlink()

    def test_process_claude_md_with_exclusions(self):
        """Test processing CLAUDE.md with exclusions."""
        content = """# Project Overview
This is a test project.

# Commands
Run tests with pytest.

# Secrets
API_KEY=secret123

# Private
Internal notes here.
"""
        
        expected = """# Project Overview
This is a test project.

# Commands
Run tests with pytest."""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            
            processor = ClaudeMdProcessor(sections_exclude=["# Secrets", "# Private"])
            result = processor.process_claude_md(Path(f.name))
            
            assert result == expected
            
        Path(f.name).unlink()

    def test_get_metadata_for_claude_md(self):
        """Test metadata generation for CLAUDE.md."""
        content = """# Project Overview
This is a test project with architecture info.

# Commands
Run tests with pytest.

# Best Practices
Follow these guidelines.
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            
            processor = ClaudeMdProcessor()
            metadata = processor.get_metadata_for_claude_md(Path(f.name))
            
            assert metadata["file_type"] == "claude_config"
            assert metadata["is_claude_md"] is True
            assert metadata["sections_filtered"] is False
            assert metadata["has_project_overview"] is True
            assert metadata["has_architecture_info"] is True
            assert metadata["has_commands"] is True
            assert metadata["has_guidelines"] is True
            assert metadata["section_count"] == 3
            
        Path(f.name).unlink()

    def test_should_sync_claude_md_valid_file(self):
        """Test sync decision for valid CLAUDE.md file."""
        content = """# Project Overview
This is a test project.
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            
            # Rename to CLAUDE.md
            claude_path = Path(f.name).parent / "CLAUDE.md"
            Path(f.name).rename(claude_path)
            
            processor = ClaudeMdProcessor()
            assert processor.should_sync_claude_md(claude_path) is True
            
        claude_path.unlink()

    def test_should_sync_claude_md_empty_file(self):
        """Test sync decision for empty CLAUDE.md file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("")
            f.flush()
            
            # Rename to CLAUDE.md
            claude_path = Path(f.name).parent / "CLAUDE.md"
            Path(f.name).rename(claude_path)
            
            processor = ClaudeMdProcessor()
            assert processor.should_sync_claude_md(claude_path) is False
            
        claude_path.unlink()

    def test_should_sync_claude_md_wrong_name(self):
        """Test sync decision for wrong filename."""
        content = """# Project Overview
This is a test project.
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            
            processor = ClaudeMdProcessor()
            assert processor.should_sync_claude_md(Path(f.name)) is False
            
        Path(f.name).unlink()

    def test_section_filtering_case_insensitive(self):
        """Test case-insensitive section filtering."""
        content = """# Project Overview
This is a test project.

# secrets
API_KEY=secret123

# PRIVATE
Internal notes here.
"""
        
        expected = """# Project Overview
This is a test project."""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            
            processor = ClaudeMdProcessor(sections_exclude=["# Secrets", "# Private"])
            result = processor.process_claude_md(Path(f.name))
            
            assert result == expected
            
        Path(f.name).unlink()