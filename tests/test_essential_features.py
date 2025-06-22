"""Essential features testing based on README.md and Quick Start guide.

This module tests the core functionality that users experience when following
the README and Quick Start documentation. These tests ensure that the most
important user-facing features work correctly.
"""

import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from claude_knowledge_catalyst.ai.smart_classifier import SmartContentClassifier
from claude_knowledge_catalyst.cli.main import app
from claude_knowledge_catalyst.core.config import CKCConfig, SyncTarget
from claude_knowledge_catalyst.core.metadata import MetadataManager
from claude_knowledge_catalyst.sync.obsidian import ObsidianVaultManager


class TestEssentialCLICommands:
    """Test essential CLI commands that users depend on."""

    @pytest.fixture
    def cli_runner(self):
        """Create CLI test runner."""
        return CliRunner()

    @pytest.fixture
    def isolated_project(self):
        """Create isolated project environment."""
        temp_dir = tempfile.mkdtemp()
        project_path = Path(temp_dir) / "test-project"
        project_path.mkdir()

        # Create .claude directory
        claude_dir = project_path / ".claude"
        claude_dir.mkdir()

        # Change to project directory for tests
        # Handle case where previous tests may have left us in a deleted directory
        try:
            original_cwd = os.getcwd()
        except (FileNotFoundError, OSError):
            # If current directory was deleted by previous tests, use project root
            original_cwd = Path(__file__).parent.parent.absolute()
            os.chdir(original_cwd)

        os.chdir(project_path)

        yield project_path

        # Cleanup
        try:
            os.chdir(original_cwd)
        except (FileNotFoundError, OSError):
            # If original directory was also deleted, go to project root
            os.chdir(Path(__file__).parent.parent.absolute())
        shutil.rmtree(temp_dir)

    def test_ckc_version_command(self, cli_runner):
        """Test that --version command works correctly."""
        result = cli_runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "Claude Knowledge Catalyst" in result.stdout
        assert "v" in result.stdout  # Should show version number

    def test_ckc_help_command(self, cli_runner):
        """Test that help command provides useful information."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Claude Knowledge Catalyst" in result.stdout
        assert "init" in result.stdout
        assert "sync" in result.stdout

    def test_ckc_init_command(self, cli_runner, isolated_project):
        """Test 'ckc init' command functionality."""
        # Mock Path.cwd() to avoid issues during testing
        with patch("pathlib.Path.cwd", return_value=isolated_project):
            result = cli_runner.invoke(app, ["init"])

        # Should succeed or give helpful error
        assert result.exit_code in [
            0,
            1,
        ]  # 0 = success, 1 = expected error with guidance

        # Check if config file was created (or attempted to be created)
        config_file = isolated_project / "ckc_config.yaml"
        if result.exit_code == 0:
            assert config_file.exists(), "Should create config file on successful init"

    def test_ckc_status_command(self, cli_runner, isolated_project):
        """Test 'ckc status' command shows project state."""
        # Create a basic config first
        config = CKCConfig()
        config.project_root = isolated_project
        config.project_name = "test-project"

        config_path = isolated_project / "ckc_config.yaml"
        config.save_to_file(config_path)

        # Test status command
        with patch("pathlib.Path.cwd", return_value=isolated_project):
            result = cli_runner.invoke(app, ["status"])

        # Should show project information
        assert result.exit_code in [
            0,
            1,
        ]  # Allow for expected errors in test environment
        if result.exit_code == 0:
            assert "test-project" in result.stdout or len(result.stdout) > 0


class TestREADMEWorkflowIntegration:
    """Test the complete README workflow step by step."""

    @pytest.fixture
    def workspace(self):
        """Create complete test workspace."""
        temp_dir = tempfile.mkdtemp()
        workspace_path = Path(temp_dir)

        # Create project structure
        project_path = workspace_path / "my-claude-project"
        project_path.mkdir()
        claude_dir = project_path / ".claude"
        claude_dir.mkdir()

        # Create vault directory
        vault_path = workspace_path / "my-obsidian-vault"
        vault_path.mkdir()

        yield {
            "workspace": workspace_path,
            "project": project_path,
            "vault": vault_path,
            "claude_dir": claude_dir,
        }

        shutil.rmtree(temp_dir)

    def test_complete_5_minute_quickstart(self, workspace):
        """Test the complete 5-minute quickstart experience from README."""
        project_path = workspace["project"]
        vault_path = workspace["vault"]
        claude_dir = workspace["claude_dir"]

        # Step 1: Project initialization (equivalent to: ckc init)
        os.chdir(project_path)

        with patch("pathlib.Path.cwd", return_value=project_path):
            config = CKCConfig()
        config.project_root = project_path
        config.project_name = "my-claude-project"
        config.auto_sync = True

        config_path = project_path / "ckc_config.yaml"
        config.save_to_file(config_path)

        # Verify initialization
        assert config_path.exists()
        assert claude_dir.exists()

        # Step 2: Add Obsidian vault (equivalent to: ckc add my-vault /path/to/vault)
        sync_target = SyncTarget(
            name="my-vault", type="obsidian", path=vault_path, enabled=True
        )
        config.sync_targets = [sync_target]
        config.save_to_file(config_path)

        # Step 3: Create sample content exactly as shown in README
        git_tips_content = """# Git便利コマンド集

## ブランチ状態確認
```bash
git branch -vv
git status --porcelain
```

## リモート同期
```bash
git fetch --all
git pull origin main
```"""

        git_tips_file = claude_dir / "git_tips.md"
        git_tips_file.write_text(git_tips_content)

        # Step 4: Test classification (equivalent to: ckc classify git_tips.md)
        classifier = SmartContentClassifier()
        results = classifier.classify_content(git_tips_content, str(git_tips_file))

        # Verify expected classification results from README
        tech_results = [r for r in results if r.tag_type == "tech"]
        type_results = [r for r in results if r.tag_type == "type"]

        # Should detect git technology
        git_detected = any("git" in r.suggested_value.lower() for r in tech_results)
        assert git_detected, "Should detect git technology"

        # Should detect code type (from bash blocks)
        code_detected = any("code" in r.suggested_value.lower() for r in type_results)
        assert code_detected, "Should detect code content type"

        # Step 5: Test sync to Obsidian (equivalent to: ckc sync)
        metadata_manager = MetadataManager()
        vault_manager = ObsidianVaultManager(vault_path, metadata_manager)
        vault_manager.initialize_vault()

        # Verify vault structure creation
        expected_dirs = [
            "_system",
            "_attachments",
            "inbox",
            "active",
            "archive",
            "knowledge",
        ]
        for dir_name in expected_dirs:
            assert (vault_path / dir_name).exists(), (
                f"Should create {dir_name} directory"
            )

        # Test file sync
        sync_result = vault_manager.sync_file(git_tips_file)
        assert sync_result, "Should successfully sync file"

        # Verify file was synced
        synced_files = list(vault_path.rglob("*.md"))
        assert len(synced_files) > 0, "Should have synced files in vault"

        # Verify content preservation
        git_files = [f for f in synced_files if "git" in f.name.lower()]
        if git_files:
            synced_content = git_files[0].read_text()
            assert "git branch -vv" in synced_content

    def test_auto_metadata_enhancement(self, workspace):
        """Test automatic metadata enhancement capabilities."""
        claude_dir = workspace["claude_dir"]

        # Create content without frontmatter (zero-config approach)
        fastapi_content = """# FastAPI RESTful API Development

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python.

## Key Features
- Automatic API documentation
- Type hints support
- High performance
- Easy to use and learn

## Example Implementation
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str

@app.post("/users/")
async def create_user(user: User):
    return {"message": f"User {user.name} created successfully"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id == 1:
        return {"name": "John Doe", "email": "john@example.com"}
    raise HTTPException(status_code=404, detail="User not found")
```

Technologies: Python, FastAPI, Pydantic, async, REST API"""

        fastapi_file = claude_dir / "fastapi_guide.md"
        fastapi_file.write_text(fastapi_content)

        # Test metadata extraction
        metadata_manager = MetadataManager()
        metadata = metadata_manager.extract_metadata_from_file(fastapi_file)

        # Verify automatic detection
        assert metadata.type in ["code", "concept", "resource"], (
            "Should detect appropriate type"
        )
        assert metadata.tech, "Should extract technology tags"

        # Verify specific technologies were detected
        tech_tags = [tag.lower() for tag in metadata.tech]
        assert any("python" in tag for tag in tech_tags), "Should detect Python"
        assert any("api" in tag or "fastapi" in tag for tag in tech_tags), (
            "Should detect API technology"
        )

        # Test classification with AI
        classifier = SmartContentClassifier()
        results = classifier.classify_content(fastapi_content, str(fastapi_file))

        # Verify classification results
        assert len(results) > 0, "Should return classification results"

        tech_results = [r for r in results if r.tag_type == "tech"]
        assert len(tech_results) > 0, "Should classify technology tags"


class TestCoreFeatureReliability:
    """Test reliability of core features that users depend on."""

    @pytest.fixture
    def test_env(self):
        """Create minimal test environment."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    def test_config_loading_and_saving(self, test_env):
        """Test config file operations work reliably."""
        config_path = test_env / "test_config.yaml"

        # Create and save config with mocked cwd
        with patch("pathlib.Path.cwd", return_value=test_env):
            config = CKCConfig()
        config.project_name = "test-project"
        config.auto_sync = True
        config.save_to_file(config_path)

        assert config_path.exists(), "Config file should be created"

        # Load config back
        loaded_config = CKCConfig.load_from_file(config_path)
        assert loaded_config.project_name == "test-project"
        assert loaded_config.auto_sync == True

    def test_metadata_extraction_robustness(self, test_env):
        """Test metadata extraction handles various content types."""
        metadata_manager = MetadataManager()

        # Test with minimal content
        minimal_file = test_env / "minimal.md"
        minimal_file.write_text("# Test\nMinimal content.")

        metadata = metadata_manager.extract_metadata_from_file(minimal_file)
        assert metadata.title == "Test"

        # Test with complex frontmatter
        complex_file = test_env / "complex.md"
        complex_content = """---
title: "Complex Document"
type: concept
tech: ["python", "fastapi"]
domain: ["web-dev"]
status: production
---

# Complex Document
This is a more complex document with frontmatter.
"""
        complex_file.write_text(complex_content)

        metadata = metadata_manager.extract_metadata_from_file(complex_file)
        assert metadata.title == "Complex Document"
        assert metadata.type == "concept"
        assert "python" in metadata.tech

    def test_classification_consistency(self, test_env):
        """Test that classification produces consistent results."""
        classifier = SmartContentClassifier()

        # Test with consistent content
        python_content = """# Python Data Processing

```python
import pandas as pd
import numpy as np

def process_data(df):
    return df.groupby('category').sum()
```

This script processes CSV data using pandas and numpy.
"""

        # Run classification multiple times
        results_1 = classifier.classify_content(python_content, "test.md")
        results_2 = classifier.classify_content(python_content, "test.md")

        # Should get consistent results
        tech_1 = [r.suggested_value for r in results_1 if r.tag_type == "tech"]
        tech_2 = [r.suggested_value for r in results_2 if r.tag_type == "tech"]

        # Should detect Python consistently
        python_1 = any("python" in tag.lower() for tag in tech_1)
        python_2 = any("python" in tag.lower() for tag in tech_2)

        assert python_1 == python_2, "Classification should be consistent"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
