"""Tests for sync hybrid manager functionality."""

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
from claude_knowledge_catalyst.core.metadata import KnowledgeMetadata, MetadataManager
from claude_knowledge_catalyst.sync.hybrid_manager import (
    HybridObsidianVaultManager,
    KnowledgeClassifier,
    StructureManager,
)


class TestStructureManager:
    """Test StructureManager functionality."""

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
        assert len(ten_step_dirs) > 0

    def test_get_vault_structure_custom(self, hybrid_config):
        """Test getting custom vault structure."""
        # Set custom structure
        custom_structure = {
            "tier_1": {
                "Custom_Dir_1": "Custom directory 1",
                "Custom_Dir_2": "Custom directory 2",
            }
        }
        hybrid_config.custom_structure = custom_structure

        manager = StructureManager(hybrid_config)
        structure = manager.get_vault_structure()

        assert isinstance(structure, dict)
        assert "Custom_Dir_1" in structure
        assert "Custom_Dir_2" in structure

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
            "tier_1": {"Dir_A": "Description A", "Dir_B": "Description B"},
            "tier_2": {"Dir_C": "Description C"},
        }
        hybrid_config.custom_structure = custom_structure

        manager = StructureManager(hybrid_config)
        flattened = manager._flatten_custom_structure()

        assert isinstance(flattened, dict)
        assert "Dir_A" in flattened
        assert "Dir_B" in flattened
        assert "Dir_C" in flattened
        assert flattened["Dir_A"] == "Description A"

    def test_add_subdirectories_method(self, structure_manager):
        """Test the _add_subdirectories method."""
        flattened = {}
        subdirs = {"subdir1": "Description 1", "subdir2": "Description 2"}

        structure_manager._add_subdirectories(flattened, subdirs, "parent")

        assert "parent/subdir1" in flattened
        assert "parent/subdir2" in flattened
        assert flattened["parent/subdir1"] == "Description 1"


class TestKnowledgeClassifier:
    """Test KnowledgeClassifier functionality."""

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

        # Test project-related content
        project_content = "This is a new project for developing a web application"
        source_path = Path("/tmp/test.md")
        result = classifier.classify_content(project_content, metadata, source_path)

        assert isinstance(result, str)

        # Test knowledge-based content
        knowledge_content = "This explains the concept of machine learning algorithms"
        result = classifier.classify_content(knowledge_content, metadata, source_path)

        assert isinstance(result, str)

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

    def test_classify_concept_content(self, classifier):
        """Test concept classification."""
        metadata = KnowledgeMetadata(
            title="Machine Learning",
            category="concept",
            tags=["ml", "ai"],
            description="ML concepts",
        )

        concept_content = "Machine learning is a subset of artificial intelligence"
        result = classifier._classify_concept(concept_content, metadata)

        assert isinstance(result, str)

    def test_extract_domain_from_tags(self, classifier):
        """Test domain extraction from tags."""
        tags = ["python", "web-development", "backend"]
        domain = classifier._extract_domain_from_tags(tags)

        assert isinstance(domain, str) or domain is None

    def test_detect_language_from_content(self, classifier):
        """Test language detection from content."""
        metadata = KnowledgeMetadata(
            title="Test Code", category="code", tags=["python"], description="Test code"
        )

        python_content = "def main():\n    import os\n    print('Hello')"
        language = classifier._detect_language_from_content(python_content, metadata)

        assert isinstance(language, str) or language is None

        js_content = "function hello() {\n    console.log('Hello');\n}"
        language = classifier._detect_language_from_content(js_content, metadata)

        assert isinstance(language, str) or language is None


class TestHybridObsidianVaultManager:
    """Test HybridObsidianVaultManager functionality."""

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

        metadata_manager = MetadataManager()
        return HybridObsidianVaultManager(vault_path, metadata_manager, mock_config)

    def test_init_basic(self, tmp_path, mock_config):
        """Test basic HybridObsidianVaultManager initialization."""
        vault_path = tmp_path / "vault"
        vault_path.mkdir()


        metadata_manager = MetadataManager()
        manager = HybridObsidianVaultManager(vault_path, metadata_manager, mock_config)

        assert manager.vault_path == vault_path
        assert manager.config == mock_config

    def test_setup_vault_structure(self, vault_manager):
        """Test vault structure setup."""
        # Test initialization without throwing errors
        assert vault_manager.vault_path.exists()
        assert vault_manager.config is not None

    def test_add_note_with_classification(self, vault_manager):
        """Test file sync with classification."""
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            content = "# Project Planning\nThis is a new project documentation"
            f.write(content)
            f.flush()

            source_path = Path(f.name)

            # Test sync operation
            result = vault_manager.sync_file(source_path, "test_project")

            assert isinstance(result, bool)

            # Clean up
            source_path.unlink()

    def test_vault_initialization(self, vault_manager):
        """Test vault initialization."""
        result = vault_manager.initialize_vault()
        assert isinstance(result, bool)

    def test_sync_directory(self, vault_manager, tmp_path):
        """Test directory sync operation."""
        # Create test directory with markdown files
        test_dir = tmp_path / "test_content"
        test_dir.mkdir()

        test_file = test_dir / "test_note.md"
        test_file.write_text("# Test Note\nThis is test content")

        # Test directory sync
        result = vault_manager.sync_directory(test_dir, "test_project")

        assert isinstance(result, dict)

    def test_sync_nonexistent_file(self, vault_manager):
        """Test sync error handling for non-existent file."""
        fake_path = vault_manager.vault_path / "nonexistent.md"

        result = vault_manager.sync_file(fake_path, "test_project")

        assert result is False

    def test_get_vault_stats(self, vault_manager):
        """Test vault statistics."""
        result = vault_manager.get_vault_stats()

        assert isinstance(result, dict)

    def test_get_structure_info(self, vault_manager):
        """Test structure information retrieval."""
        info = vault_manager.get_structure_info()

        assert isinstance(info, dict)
        assert "hybrid_enabled" in info
        assert "numbering_system" in info

    def test_cleanup_empty_directories(self, vault_manager):
        """Test empty directory cleanup."""
        # Create an empty directory
        empty_dir = vault_manager.vault_path / "empty_test"
        empty_dir.mkdir(parents=True, exist_ok=True)

        result = vault_manager.cleanup_empty_directories()

        assert isinstance(result, int)

    def test_vault_path_property(self, vault_manager):
        """Test vault path property."""
        assert isinstance(vault_manager.vault_path, Path)
        assert vault_manager.vault_path.exists()

    def test_vault_structure_property(self, vault_manager):
        """Test vault structure property."""
        structure = vault_manager.vault_structure

        assert isinstance(structure, dict)
        assert len(structure) > 0

    def test_config_access(self, vault_manager):
        """Test configuration access."""
        assert hasattr(vault_manager, "config")
        assert vault_manager.config is not None

    def test_hybrid_config_access(self, vault_manager):
        """Test hybrid configuration access."""
        assert hasattr(vault_manager, "hybrid_config")
        assert vault_manager.hybrid_config is not None
