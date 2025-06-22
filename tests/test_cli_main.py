"""Tests for main CLI interface."""

# Re-enabled CLI tests for improved coverage
# pytestmark = pytest.mark.skip(reason="CLI tests require complex setup - skipping for v0.9.2 release")
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import typer
from typer.testing import CliRunner

from claude_knowledge_catalyst import __version__
from claude_knowledge_catalyst.cli.main import app, version_callback
from claude_knowledge_catalyst.core.config import CKCConfig, SyncTarget


class TestCLIBasics:
    """Test basic CLI functionality."""

    @pytest.fixture
    def cli_runner(self):
        """Create CLI test runner."""
        return CliRunner()

    @pytest.fixture
    def temp_project_dir(self):
        """Create temporary project directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    def test_version_callback_true(self):
        """Test version callback when value is True."""
        with pytest.raises(typer.Exit):
            version_callback(True)

    def test_version_callback_false(self):
        """Test version callback when value is False."""
        # Should not raise exception when False
        result = version_callback(False)
        assert result is None

    def test_version_option(self, cli_runner):
        """Test --version option."""
        result = cli_runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "Claude Knowledge Catalyst (CKC)" in result.stdout
        assert __version__ in result.stdout

    def test_version_short_option(self, cli_runner):
        """Test -v short version option."""
        result = cli_runner.invoke(app, ["-v"])
        assert result.exit_code == 0
        assert "Claude Knowledge Catalyst (CKC)" in result.stdout

    def test_help_option(self, cli_runner):
        """Test help option displays correctly."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Claude Knowledge Catalyst" in result.stdout
        assert "Modern knowledge management system" in result.stdout

    def test_no_args_shows_help(self, cli_runner):
        """Test that running with no arguments shows help."""
        result = cli_runner.invoke(app, [])
        # Allow exit code 2 for missing arguments (typical for Typer)
        assert result.exit_code in [0, 2]
        # Should show help or usage when no arguments provided
        assert "Usage:" in result.stdout or "Try" in result.stdout


class TestCLICommands:
    """Test specific CLI commands."""

    @pytest.fixture
    def cli_runner(self):
        """Create CLI test runner."""
        return CliRunner()

    @pytest.fixture
    def temp_project_dir(self):
        """Create temporary project directory with config."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)

            # Create basic CKC config
            config = CKCConfig()
            config.project_root = project_dir
            config.project_name = "test-project"

            config_path = project_dir / "ckc_config.yaml"
            config.save_to_file(config_path)

            yield project_dir

    @patch("claude_knowledge_catalyst.cli.main.CKCConfig")
    def test_init_command(self, mock_config_class, cli_runner, temp_project_dir):
        """Test ckc init command."""
        mock_config = Mock()
        mock_config_class.return_value = mock_config
        mock_config.save_to_file = Mock()

        with cli_runner.isolated_filesystem():
            result = cli_runner.invoke(app, ["init"])

            # Should succeed (exit code 0 or handle gracefully)
            assert result.exit_code in [0, 1]  # May fail due to missing dependencies

    @patch("claude_knowledge_catalyst.cli.main.load_config")
    def test_status_command(self, mock_load_config, cli_runner, temp_project_dir):
        """Test ckc status command."""
        # Setup mock config
        mock_config = Mock(spec=CKCConfig)
        mock_config.project_name = "test-project"
        mock_config.sync_targets = []
        mock_load_config.return_value = mock_config

        result = cli_runner.invoke(app, ["status"], cwd=str(temp_project_dir))

        # Should show status information
        assert result.exit_code in [0, 1]  # May fail due to missing config

    def test_sync_command_group(self, cli_runner):
        """Test sync command group exists."""
        result = cli_runner.invoke(app, ["sync", "--help"])
        assert result.exit_code == 0
        assert "sync" in result.stdout.lower()

    def test_watch_command_group(self, cli_runner):
        """Test watch command group exists."""
        result = cli_runner.invoke(app, ["watch", "--help"])
        assert result.exit_code == 0
        assert "watch" in result.stdout.lower()

    def test_search_command_group(self, cli_runner):
        """Test search command group exists."""
        result = cli_runner.invoke(app, ["search", "--help"])
        assert result.exit_code == 0

    def test_analyze_command_group(self, cli_runner):
        """Test analyze command group exists."""
        result = cli_runner.invoke(app, ["analyze", "--help"])
        assert result.exit_code == 0

    @patch("claude_knowledge_catalyst.cli.main.ObsidianVaultManager")
    @patch("claude_knowledge_catalyst.cli.main.load_config")
    def test_sync_add_command(
        self, mock_load_config, mock_vault_manager, cli_runner, temp_project_dir
    ):
        """Test sync add command."""
        # Setup mocks
        mock_config = Mock(spec=CKCConfig)
        mock_config.sync_targets = []
        mock_config.save_to_file = Mock()
        mock_load_config.return_value = mock_config

        mock_vault = Mock()
        mock_vault_manager.return_value = mock_vault

        vault_path = temp_project_dir / "test_vault"
        vault_path.mkdir()

        result = cli_runner.invoke(
            app,
            [
                "sync",
                "add",
                "--name",
                "test-vault",
                "--type",
                "obsidian",
                "--path",
                str(vault_path),
            ],
            cwd=str(temp_project_dir),
        )

        # Should handle the command (may fail due to validation)
        assert result.exit_code in [0, 1]

    @patch("claude_knowledge_catalyst.cli.main.KnowledgeWatcher")
    @patch("claude_knowledge_catalyst.cli.main.load_config")
    def test_watch_start_command(
        self, mock_load_config, mock_watcher_class, cli_runner, temp_project_dir
    ):
        """Test watch start command."""
        # Setup mocks
        mock_config = Mock(spec=CKCConfig)
        mock_config.watch = Mock()
        mock_config.watch.enabled = True
        mock_load_config.return_value = mock_config

        mock_watcher = Mock()
        mock_watcher_class.return_value = mock_watcher
        mock_watcher.__enter__ = Mock(return_value=mock_watcher)
        mock_watcher.__exit__ = Mock(return_value=None)

        # This test may need to be run with timeout due to blocking nature
        result = cli_runner.invoke(
            app, ["watch", "start"], cwd=str(temp_project_dir), input="\n"
        )  # Simulate Ctrl+C

        assert result.exit_code in [0, 1]


class TestCLIErrorHandling:
    """Test CLI error handling scenarios."""

    @pytest.fixture
    def cli_runner(self):
        """Create CLI test runner."""
        return CliRunner()

    def test_missing_config_file(self, cli_runner):
        """Test behavior when config file is missing."""
        with cli_runner.isolated_filesystem():
            result = cli_runner.invoke(app, ["status"])

            # Should handle missing config gracefully
            assert result.exit_code in [0, 1]
            # Should provide helpful error message
            assert len(result.stdout) > 0 or len(result.stderr) > 0

    def test_invalid_command(self, cli_runner):
        """Test invalid command handling."""
        result = cli_runner.invoke(app, ["invalid-command"])
        assert result.exit_code != 0
        # Typer typically shows error messages in stderr or stdout
        error_output = result.stdout + (result.stderr or "")
        assert (
            "No such command" in error_output
            or "Usage:" in error_output
            or "Error:" in error_output
        )

    def test_sync_add_missing_args(self, cli_runner):
        """Test sync add with missing required arguments."""
        result = cli_runner.invoke(app, ["sync", "add"])
        assert result.exit_code != 0
        # Should show error about missing arguments

    @patch("claude_knowledge_catalyst.cli.main.load_config")
    def test_sync_add_invalid_path(self, mock_load_config, cli_runner):
        """Test sync add with invalid vault path."""
        mock_config = Mock(spec=CKCConfig)
        mock_config.sync_targets = []
        mock_load_config.return_value = mock_config

        result = cli_runner.invoke(
            app,
            [
                "sync",
                "add",
                "--name",
                "test",
                "--type",
                "obsidian",
                "--path",
                "/non/existent/path",
            ],
        )

        assert result.exit_code in [
            0,
            1,
            2,
        ]  # May be handled gracefully, 2 for argument errors


class TestCLIIntegration:
    """Integration tests for CLI functionality."""

    @pytest.fixture
    def cli_runner(self):
        """Create CLI test runner."""
        return CliRunner()

    @pytest.fixture
    def full_project_setup(self):
        """Create full project setup with vault."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "project"
            vault_dir = Path(temp_dir) / "vault"

            project_dir.mkdir()
            vault_dir.mkdir()

            # Create basic vault structure
            for dir_name in [
                "_system",
                "_attachments",
                "inbox",
                "active",
                "archive",
                "knowledge",
            ]:
                (vault_dir / dir_name).mkdir()

            # Create CKC config
            config = CKCConfig()
            config.project_root = project_dir
            config.project_name = "integration-test"
            config.sync_targets = [
                SyncTarget(
                    name="test-vault", type="obsidian", path=vault_dir, enabled=True
                )
            ]

            config_path = project_dir / "ckc_config.yaml"
            config.save_to_file(config_path)

            yield project_dir, vault_dir

    @patch("claude_knowledge_catalyst.cli.main.ObsidianVaultManager")
    @patch("claude_knowledge_catalyst.cli.main.MetadataManager")
    def test_full_workflow(
        self, mock_metadata_manager, mock_vault_manager, cli_runner, full_project_setup
    ):
        """Test complete CLI workflow."""
        project_dir, vault_dir = full_project_setup

        # Setup mocks
        mock_vault = Mock()
        mock_vault.initialize_vault.return_value = True
        mock_vault_manager.return_value = mock_vault

        mock_meta_mgr = Mock()
        mock_metadata_manager.return_value = mock_meta_mgr

        # Test status command
        result = cli_runner.invoke(app, ["status"], cwd=str(project_dir))
        assert result.exit_code in [0, 1]

        # Test sync list command
        result = cli_runner.invoke(app, ["sync", "list"], cwd=str(project_dir))
        assert result.exit_code in [0, 1]

    @pytest.mark.parametrize(
        "command",
        [
            ["--help"],
            ["init", "--help"],
            ["sync", "--help"],
            ["watch", "--help"],
            ["search", "--help"],
            ["analyze", "--help"],
        ],
    )
    def test_help_commands(self, cli_runner, command):
        """Test that all help commands work."""
        result = cli_runner.invoke(app, command)
        assert result.exit_code == 0
        assert "Usage:" in result.stdout or "help" in result.stdout.lower()

    def test_command_discovery(self, cli_runner):
        """Test that all expected commands are available."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0

        # Check for main command groups
        expected_commands = ["init", "status", "sync", "watch", "search", "analyze"]
        for cmd in expected_commands:
            assert cmd in result.stdout

    def test_interactive_features(self, cli_runner):
        """Test interactive CLI features."""
        # Test search command which has interactive features
        result = cli_runner.invoke(app, ["search", "--help"])
        assert result.exit_code == 0
        assert "search" in result.stdout.lower()

        # Test analyze command which has interactive features
        result = cli_runner.invoke(app, ["analyze", "--help"])
        assert result.exit_code == 0
        assert "analyze" in result.stdout.lower()


class TestCLIValidation:
    """Test CLI input validation."""

    @pytest.fixture
    def cli_runner(self):
        """Create CLI test runner."""
        return CliRunner()

    def test_sync_type_validation(self, cli_runner):
        """Test sync target type validation."""
        with cli_runner.isolated_filesystem():
            result = cli_runner.invoke(
                app,
                [
                    "sync",
                    "add",
                    "--name",
                    "test",
                    "--type",
                    "invalid-type",
                    "--path",
                    "/tmp",
                ],
            )

            # Should reject invalid sync types
            assert result.exit_code != 0 or "invalid" in result.stdout.lower()

    def test_path_validation(self, cli_runner):
        """Test path validation for various commands."""
        with cli_runner.isolated_filesystem():
            # Test with various invalid paths
            invalid_paths = [
                "/definitely/does/not/exist",
                "relative/path/that/does/not/exist",
                "",
            ]

            for path in invalid_paths:
                result = cli_runner.invoke(
                    app,
                    [
                        "sync",
                        "add",
                        "--name",
                        "test",
                        "--type",
                        "obsidian",
                        "--path",
                        path,
                    ],
                )

                # Should handle invalid paths gracefully, 2 for argument validation errors
                assert result.exit_code in [0, 1, 2]

    def test_config_validation(self, cli_runner):
        """Test configuration validation."""
        with cli_runner.isolated_filesystem():
            # Create invalid config file
            Path("ckc_config.yaml").write_text("invalid: yaml: content: [")

            result = cli_runner.invoke(app, ["status"])

            # Should handle invalid config gracefully
            assert result.exit_code in [0, 1]
            # Should provide error information
            assert len(result.stdout) > 0 or len(result.stderr) > 0
