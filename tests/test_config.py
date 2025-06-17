"""Tests for configuration management."""

import tempfile
from pathlib import Path

import pytest

from claude_knowledge_catalyst.core.config import CKCConfig, SyncTarget, TagConfig, WatchConfig


class TestCKCConfig:
    """Test cases for CKCConfig class."""
    
    def test_default_config(self):
        """Test default configuration creation."""
        config = CKCConfig()
        
        assert config.version == "1.0"
        assert config.project_name == ""
        assert config.auto_sync is True
        assert config.git_integration is True
        assert config.auto_commit is False
        assert isinstance(config.tags, TagConfig)
        assert isinstance(config.watch, WatchConfig)
    
    def test_sync_target_management(self):
        """Test sync target add/remove functionality."""
        config = CKCConfig()
        
        # Add sync target
        target = SyncTarget(
            name="test_vault",
            type="obsidian",
            path=Path("/tmp/test_vault"),
            enabled=True
        )
        config.add_sync_target(target)
        
        assert len(config.sync_targets) == 1
        assert config.sync_targets[0].name == "test_vault"
        
        # Get enabled targets
        enabled = config.get_enabled_sync_targets()
        assert len(enabled) == 1
        
        # Remove sync target
        removed = config.remove_sync_target("test_vault")
        assert removed is True
        assert len(config.sync_targets) == 0
        
        # Try to remove non-existent target
        removed = config.remove_sync_target("non_existent")
        assert removed is False
    
    def test_config_file_operations(self):
        """Test saving and loading configuration files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test_config.yaml"
            
            # Create and save config
            original_config = CKCConfig(
                project_name="test_project",
                auto_sync=False
            )
            original_config.save_to_file(config_path)
            
            # Load config
            loaded_config = CKCConfig.load_from_file(config_path)
            
            assert loaded_config.project_name == "test_project"
            assert loaded_config.auto_sync is False
    
    def test_path_validation(self):
        """Test path validation in sync targets."""
        # Valid obsidian type
        target = SyncTarget(
            name="test",
            type="obsidian",
            path=Path("/tmp/test")
        )
        assert target.type == "obsidian"
        
        # Invalid type should raise error
        with pytest.raises(ValueError):
            SyncTarget(
                name="test",
                type="invalid_type",
                path=Path("/tmp/test")
            )


class TestTagConfig:
    """Test cases for TagConfig class."""
    
    def test_default_tags(self):
        """Test default tag configuration."""
        config = TagConfig()
        
        assert "prompt" in config.category_tags
        assert "python" in config.tech_tags
        assert "opus" in config.claude_tags
        assert "draft" in config.status_tags
        assert "high" in config.quality_tags


class TestWatchConfig:
    """Test cases for WatchConfig class."""
    
    def test_default_watch_config(self):
        """Test default watch configuration."""
        config = WatchConfig()
        
        assert Path(".claude") in config.watch_paths
        assert "*.md" in config.file_patterns
        assert ".git" in config.ignore_patterns
        assert config.debounce_seconds == 1.0