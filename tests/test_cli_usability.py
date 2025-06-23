"""Tests for CLI usability enhancements - wizard and diagnostics."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock

import pytest
from typer.testing import CliRunner

from claude_knowledge_catalyst.cli.main import app
from claude_knowledge_catalyst.core.config import CKCConfig, SyncTarget


class TestCLIWizard:
    """Test CLI wizard functionality."""

    @pytest.fixture
    def cli_runner(self):
        """Create CLI test runner."""
        return CliRunner()

    @pytest.fixture
    def isolated_environment(self):
        """Create isolated test environment."""
        temp_dir = tempfile.mkdtemp()
        project_path = Path(temp_dir) / "test-project"
        project_path.mkdir()
        
        # Change to project directory for tests
        original_cwd = os.getcwd()
        os.chdir(project_path)
        
        yield project_path
        
        # Restore original directory
        os.chdir(original_cwd)

    def test_wizard_help_command(self, cli_runner):
        """Test wizard help information."""
        result = cli_runner.invoke(app, ["wizard", "--help"])
        assert result.exit_code == 0
        assert "Interactive setup wizard" in result.stdout

    @patch("claude_knowledge_catalyst.cli.main.Confirm.ask")
    @patch("claude_knowledge_catalyst.cli.main.Prompt.ask")
    def test_wizard_skip_reconfigure(self, mock_prompt, mock_confirm, cli_runner, isolated_environment):
        """Test wizard when existing config exists and user skips reconfigure."""
        # Create existing config
        config_file = isolated_environment / "ckc_config.yaml"
        config_file.write_text("project_name: existing-project\n")
        
        # Mock user declining reconfiguration
        mock_confirm.return_value = False
        
        result = cli_runner.invoke(app, ["wizard"])
        
        # Should exit gracefully without reconfiguring
        assert result.exit_code == 0
        assert "Setup cancelled" in result.stdout

    @patch("claude_knowledge_catalyst.cli.main.Confirm.ask")
    @patch("claude_knowledge_catalyst.cli.main.Prompt.ask")
    def test_wizard_basic_setup_no_vault(self, mock_prompt, mock_confirm, cli_runner, isolated_environment):
        """Test wizard basic setup without vault."""
        # Mock user inputs
        mock_prompt.return_value = "test-project"
        mock_confirm.side_effect = [False, False]  # No vault, no sample files
        
        with patch("claude_knowledge_catalyst.cli.main.get_config") as mock_get_config:
            mock_config = Mock(spec=CKCConfig)
            mock_config.project_root = isolated_environment
            mock_config.project_name = "test-project"
            mock_config.auto_sync = True
            mock_config.sync_targets = []
            mock_config.save_to_file = Mock()
            mock_get_config.return_value = mock_config
            
            result = cli_runner.invoke(app, ["wizard"])
        
        # Should complete successfully
        assert result.exit_code == 0
        assert "Setup Complete" in result.stdout

    @patch("claude_knowledge_catalyst.cli.main.Confirm.ask")
    @patch("claude_knowledge_catalyst.cli.main.Prompt.ask")
    @patch("claude_knowledge_catalyst.cli.main.ObsidianVaultManager")
    @patch("claude_knowledge_catalyst.cli.main.get_metadata_manager")
    def test_wizard_with_vault_setup(self, mock_metadata_manager, mock_vault_manager, 
                                   mock_prompt, mock_confirm, cli_runner, isolated_environment):
        """Test wizard with vault setup."""
        # Create mock vault directory
        vault_dir = isolated_environment / "test-vault"
        vault_dir.mkdir()
        
        # Mock user inputs
        mock_prompt.side_effect = ["test-project", str(vault_dir), "my-vault"]
        mock_confirm.side_effect = [True, True, False]  # Setup vault, create samples, no sync
        
        # Mock vault manager
        mock_vault = Mock()
        mock_vault.initialize_vault.return_value = True
        mock_vault_manager.return_value = mock_vault
        
        with patch("claude_knowledge_catalyst.cli.main.get_config") as mock_get_config:
            mock_config = Mock(spec=CKCConfig)
            mock_config.project_root = isolated_environment
            mock_config.project_name = "test-project"
            mock_config.auto_sync = True
            mock_config.sync_targets = []
            mock_config.add_sync_target = Mock()
            mock_config.save_to_file = Mock()
            mock_config.get_enabled_sync_targets.return_value = []
            mock_get_config.return_value = mock_config
            
            result = cli_runner.invoke(app, ["wizard"])
        
        # Should complete successfully with vault setup
        assert result.exit_code == 0
        assert "Vault 'my-vault' configured" in result.stdout

    @patch("claude_knowledge_catalyst.cli.main.Confirm.ask")
    @patch("claude_knowledge_catalyst.cli.main.Prompt.ask")
    def test_wizard_sample_content_creation(self, mock_prompt, mock_confirm, cli_runner, isolated_environment):
        """Test wizard sample content creation."""
        # Mock user inputs
        mock_prompt.return_value = "test-project"
        mock_confirm.side_effect = [False, True]  # No vault, yes sample files
        
        with patch("claude_knowledge_catalyst.cli.main.get_config") as mock_get_config:
            mock_config = Mock(spec=CKCConfig)
            mock_config.project_root = isolated_environment
            mock_config.sync_targets = []
            mock_config.save_to_file = Mock()
            mock_get_config.return_value = mock_config
            
            result = cli_runner.invoke(app, ["wizard"])
        
        # Should create sample files
        assert result.exit_code == 0
        assert "python_tips.md" in result.stdout
        assert "git_workflow.md" in result.stdout
        
        # Check files were actually created
        claude_dir = isolated_environment / ".claude"
        assert (claude_dir / "python_tips.md").exists()
        assert (claude_dir / "git_workflow.md").exists()


class TestCLIDiagnostics:
    """Test CLI diagnostics functionality."""

    @pytest.fixture
    def cli_runner(self):
        """Create CLI test runner."""
        return CliRunner()

    @pytest.fixture
    def mock_environment(self):
        """Create mock test environment."""
        temp_dir = tempfile.mkdtemp()
        project_path = Path(temp_dir) / "test-project"
        project_path.mkdir()
        
        original_cwd = os.getcwd()
        os.chdir(project_path)
        
        yield project_path
        
        os.chdir(original_cwd)

    def test_diagnose_help_command(self, cli_runner):
        """Test diagnose help information."""
        result = cli_runner.invoke(app, ["diagnose", "--help"])
        assert result.exit_code == 0
        assert "comprehensive system diagnostics" in result.stdout

    @patch("claude_knowledge_catalyst.cli.main.load_config")
    def test_diagnose_no_config(self, mock_load_config, cli_runner, mock_environment):
        """Test diagnostics when no configuration exists."""
        mock_load_config.side_effect = Exception("No config found")
        
        result = cli_runner.invoke(app, ["diagnose"])
        
        assert result.exit_code == 0
        assert "Configuration error" in result.stdout
        assert "Critical Issues" in result.stdout

    @patch("claude_knowledge_catalyst.cli.main.load_config")
    def test_diagnose_healthy_system(self, mock_load_config, cli_runner, mock_environment):
        """Test diagnostics with healthy system."""
        # Create mock healthy config
        mock_config = Mock(spec=CKCConfig)
        mock_config.project_name = "test-project"
        mock_config.project_root = mock_environment
        mock_config.sync_targets = [
            SyncTarget(name="test-vault", type="obsidian", path=mock_environment / "vault", enabled=True)
        ]
        mock_load_config.return_value = mock_config
        
        # Create .claude directory and sample file
        claude_dir = mock_environment / ".claude"
        claude_dir.mkdir()
        sample_file = claude_dir / "test.md"
        sample_file.write_text("# Test Content\nSample content for testing.")
        
        # Create vault directory with proper structure
        vault_dir = mock_environment / "vault"
        vault_dir.mkdir()
        for subdir in ["_system", "_attachments", "inbox", "active", "archive", "knowledge"]:
            (vault_dir / subdir).mkdir()
        
        with (
            patch("claude_knowledge_catalyst.cli.main.get_metadata_manager") as mock_metadata_manager,
            patch("claude_knowledge_catalyst.cli.main.SmartContentClassifier") as mock_classifier
        ):
            # Mock metadata manager
            mock_manager = Mock()
            mock_manager.extract_metadata_from_file.return_value = Mock()
            mock_metadata_manager.return_value = mock_manager
            
            # Mock classifier
            mock_clf = Mock()
            mock_clf.classify_content.return_value = [Mock(), Mock()]  # Some results
            mock_classifier.return_value = mock_clf
            
            result = cli_runner.invoke(app, ["diagnose"])
        
        assert result.exit_code == 0
        assert "All systems healthy" in result.stdout or "Configuration loaded" in result.stdout

    @patch("claude_knowledge_catalyst.cli.main.load_config")
    def test_diagnose_missing_claude_directory(self, mock_load_config, cli_runner, mock_environment):
        """Test diagnostics when .claude directory is missing."""
        # Mock config
        mock_config = Mock(spec=CKCConfig)
        mock_config.project_name = "test-project"
        mock_config.project_root = mock_environment
        mock_config.sync_targets = []
        mock_load_config.return_value = mock_config
        
        result = cli_runner.invoke(app, ["diagnose"])
        
        assert result.exit_code == 0
        assert ".claude directory does not exist" in result.stdout
        assert "Critical Issues" in result.stdout

    @patch("claude_knowledge_catalyst.cli.main.load_config") 
    def test_diagnose_performance_check(self, mock_load_config, cli_runner, mock_environment):
        """Test diagnostics performance checking."""
        # Create mock config
        mock_config = Mock(spec=CKCConfig)
        mock_config.project_name = "test-project"
        mock_config.project_root = mock_environment
        mock_config.sync_targets = []
        mock_load_config.return_value = mock_config
        
        # Create .claude directory and sample file
        claude_dir = mock_environment / ".claude"
        claude_dir.mkdir()
        sample_file = claude_dir / "test.md"
        sample_file.write_text("# Test File\nContent for performance testing.")
        
        with patch("claude_knowledge_catalyst.cli.main.get_metadata_manager") as mock_metadata_manager:
            mock_manager = Mock()
            mock_manager.extract_metadata_from_file.return_value = Mock()
            mock_metadata_manager.return_value = mock_manager
            
            result = cli_runner.invoke(app, ["diagnose"])
        
        assert result.exit_code == 0
        assert "Performance Check" in result.stdout
        assert "Metadata extraction:" in result.stdout

    @patch("claude_knowledge_catalyst.cli.main.load_config")
    def test_diagnose_yake_availability(self, mock_load_config, cli_runner, mock_environment):
        """Test diagnostics YAKE dependency checking."""
        mock_config = Mock(spec=CKCConfig)
        mock_config.project_name = "test-project"
        mock_config.project_root = mock_environment
        mock_config.sync_targets = []
        mock_load_config.return_value = mock_config
        
        result = cli_runner.invoke(app, ["diagnose"])
        
        assert result.exit_code == 0
        assert "Dependency Check" in result.stdout
        # Should show YAKE status (available or not)
        assert ("YAKE keyword extraction available" in result.stdout or 
                "YAKE dependencies not available" in result.stdout)

    @patch("claude_knowledge_catalyst.cli.main.load_config")
    def test_diagnose_recommendations(self, mock_load_config, cli_runner, mock_environment):
        """Test diagnostics recommendations."""
        mock_config = Mock(spec=CKCConfig)
        mock_config.project_name = "test-project"
        mock_config.project_root = mock_environment
        mock_config.sync_targets = []  # No sync targets to trigger recommendations
        mock_load_config.return_value = mock_config
        
        result = cli_runner.invoke(app, ["diagnose"])
        
        assert result.exit_code == 0
        assert "Recommendations" in result.stdout
        assert "ckc wizard" in result.stdout or "ckc add" in result.stdout


class TestCLIUsabilityIntegration:
    """Integration tests for CLI usability features."""

    @pytest.fixture
    def cli_runner(self):
        """Create CLI test runner."""
        return CliRunner()

    def test_wizard_and_diagnose_workflow(self, cli_runner):
        """Test wizard setup followed by diagnostics."""
        # This is a basic integration test to ensure commands don't conflict
        
        # Test that both commands are available
        help_result = cli_runner.invoke(app, ["--help"])
        assert help_result.exit_code == 0
        assert "wizard" in help_result.stdout
        assert "diagnose" in help_result.stdout

    def test_cli_command_availability(self, cli_runner):
        """Test that new commands are properly registered."""
        result = cli_runner.invoke(app, ["--help"])
        
        assert result.exit_code == 0
        output = result.stdout
        
        # Check new commands are listed
        assert "wizard" in output
        assert "diagnose" in output
        assert "Interactive setup wizard" in output
        assert "comprehensive system diagnostics" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])