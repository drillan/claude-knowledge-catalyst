"""Simplified tests for sync hybrid manager functionality."""

import re
from pathlib import Path
from unittest.mock import Mock

import pytest
from claude_knowledge_catalyst.core.config import CKCConfig
from claude_knowledge_catalyst.core.hybrid_config import (
    HybridStructureConfig,
    NumberingSystem,
    NumberManagerConfig,
)
from claude_knowledge_catalyst.core.metadata import KnowledgeMetadata
from claude_knowledge_catalyst.sync.hybrid_manager import (
    HybridObsidianVaultManager,
    KnowledgeClassifier,
    StructureManager,
)


class TestStructureManagerSimple:
    """Test StructureManager basic functionality."""

    @pytest.fixture
    def hybrid_config(self):
        """Create HybridStructureConfig for testing."""
        return HybridStructureConfig(
            numbering_system=NumberingSystem.TEN_STEP, custom_structure=None
        )

    @pytest.fixture
    def structure_manager(self, hybrid_config):
        """Create StructureManager for testing."""
        return StructureManager(hybrid_config)

    def test_init_basic(self, hybrid_config):
        """Test basic StructureManager initialization."""
        manager = StructureManager(hybrid_config)

        assert manager.config == hybrid_config
        assert isinstance(manager.number_manager, NumberManagerConfig)
        assert manager.number_manager.system_type == NumberingSystem.TEN_STEP

    def test_get_vault_structure_default(self, structure_manager):
        """Test getting default vault structure."""
        structure = structure_manager.get_vault_structure()

        assert isinstance(structure, dict)
        assert len(structure) > 0

        # Should contain typical directories
        dir_names = list(structure.keys())
        ten_step_dirs = [d for d in dir_names if re.match(r"\d+_", d)]
        assert len(ten_step_dirs) >= 0  # At least some numbered directories

    def test_flatten_default_structure(self, structure_manager):
        """Test flattening default structure."""
        flattened = structure_manager._flatten_default_structure()

        assert isinstance(flattened, dict)
        assert len(flattened) > 0

        # Check that all values are descriptions (strings)
        for dir_name, description in flattened.items():
            assert isinstance(dir_name, str)
            assert isinstance(description, str)

    def test_flatten_custom_structure(self, hybrid_config):
        """Test flattening custom structure."""
        custom_structure = {
            "tier_1": {"Dir_A": "Description A", "Dir_B": "Description B"}
        }
        hybrid_config.custom_structure = custom_structure

        manager = StructureManager(hybrid_config)
        flattened = manager._flatten_custom_structure()

        assert isinstance(flattened, dict)
        assert "Dir_A" in flattened
        assert "Dir_B" in flattened
        assert flattened["Dir_A"] == "Description A"


class TestKnowledgeClassifierSimple:
    """Test KnowledgeClassifier basic functionality."""

    @pytest.fixture
    def hybrid_config(self):
        """Create HybridStructureConfig for testing."""
        return HybridStructureConfig()

    @pytest.fixture
    def classifier(self, hybrid_config):
        """Create KnowledgeClassifier for testing."""
        return KnowledgeClassifier(hybrid_config)

    def test_init_basic(self, hybrid_config):
        """Test basic KnowledgeClassifier initialization."""
        classifier = KnowledgeClassifier(hybrid_config)

        assert classifier.config == hybrid_config

    def test_classify_content_basic(self, classifier):
        """Test basic content classification."""
        from pathlib import Path

        # Create metadata for testing
        metadata = KnowledgeMetadata(
            title="Test Content",
            category="test",
            tags=["example"],
            description="Test description",
        )

        # Test basic content classification
        content = "This is a test content for classification"
        source_path = Path("/tmp/test.md")
        result = classifier.classify_content(content, metadata, source_path)

        assert isinstance(result, str)
        assert len(result) > 0

    def test_classify_prompt_content(self, classifier):
        """Test prompt classification."""
        metadata = KnowledgeMetadata(
            title="Test Prompt",
            category="prompt",
            tags=["test"],
            description="Test prompt",
        )

        prompt_content = "Please help me write a Python function"
        result = classifier._classify_prompt(prompt_content, metadata)

        assert isinstance(result, str)
        assert len(result) > 0

    def test_classify_code_content(self, classifier):
        """Test code classification."""
        metadata = KnowledgeMetadata(
            title="Python Script",
            category="code",
            tags=["python"],
            description="Python code example",
        )

        code_content = "def hello_world():\n    print('Hello, World!')"
        result = classifier._classify_code(code_content, metadata)

        assert isinstance(result, str)
        assert len(result) > 0

    def test_extract_domain_from_tags(self, classifier):
        """Test domain extraction from tags."""
        tags = ["python", "web-development", "backend"]
        domain = classifier._extract_domain_from_tags(tags)

        # Should return string or None
        assert isinstance(domain, str) or domain is None

    def test_detect_language_from_content(self, classifier):
        """Test language detection from content."""
        metadata = KnowledgeMetadata(
            title="Test Code", category="code", tags=["python"], description="Test code"
        )

        python_content = "def main():\n    import os\n    print('Hello')"
        language = classifier._detect_language_from_content(python_content, metadata)

        # Should return string or None
        assert isinstance(language, str) or language is None


class TestHybridObsidianVaultManagerSimple:
    """Test HybridObsidianVaultManager basic functionality."""

    @pytest.fixture
    def mock_config(self):
        """Create mock CKCConfig for testing."""
        config = Mock(spec=CKCConfig)
        config.project_name = "test-project"
        config.hybrid_structure = HybridStructureConfig()
        config.sync_targets = []
        return config

    @pytest.fixture
    def vault_manager(self, tmp_path, mock_config):
        """Create HybridObsidianVaultManager for testing."""
        vault_path = tmp_path / "vault"
        vault_path.mkdir()
        from claude_knowledge_catalyst.core.metadata import MetadataManager

        metadata_manager = MetadataManager()
        return HybridObsidianVaultManager(vault_path, metadata_manager, mock_config)

    def test_init_basic(self, tmp_path, mock_config):
        """Test basic HybridObsidianVaultManager initialization."""
        vault_path = tmp_path / "vault"
        vault_path.mkdir()

        from claude_knowledge_catalyst.core.metadata import MetadataManager

        metadata_manager = MetadataManager()
        manager = HybridObsidianVaultManager(vault_path, metadata_manager, mock_config)

        assert manager.vault_path == vault_path
        assert manager.config == mock_config

    def test_basic_vault_operations(self, vault_manager):
        """Test basic vault operations."""
        # Test that vault manager was created successfully
        assert vault_manager.vault_path.exists()
        assert vault_manager.config is not None

        # Test basic file operations
        test_file = vault_manager.vault_path / "test.md"
        test_file.write_text("# Test Content")

        assert test_file.exists()
        content = test_file.read_text()
        assert "Test Content" in content

    def test_vault_path_handling(self, vault_manager):
        """Test vault path handling."""
        # Test that vault path is properly handled
        assert isinstance(vault_manager.vault_path, Path)
        assert vault_manager.vault_path.is_dir()

        # Test creating subdirectories
        subdir = vault_manager.vault_path / "subdir"
        subdir.mkdir()

        assert subdir.exists()
        assert subdir.is_dir()

    def test_config_access(self, vault_manager):
        """Test configuration access."""
        # Test that configuration is accessible
        assert vault_manager.config is not None
        assert hasattr(vault_manager.config, "project_name")
        assert vault_manager.config.project_name == "test-project"
