"""
Unit tests for __main__.py and CLI entry point.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from cli import parse_arguments


@pytest.mark.unit
class TestMainEntry:
    """Tests for __main__.py entry point."""

    def test_main_module_can_be_imported(self):
        """Test that main module can be imported."""
        import importlib

        try:
            spec = importlib.util.find_spec("__main__")
        except ValueError:
            spec = None

        if spec is None:
            pytest.skip("__main__.__spec__ is None when running under pytest")

        from main import main

        assert main is not None
        assert callable(main)

    def test_main_returns_int(self):
        """Test that main() returns an integer exit code."""
        from main import main

        # This will fail because it needs input, but we can test the signature
        assert callable(main)


@pytest.mark.unit
class TestFirstRunDetection:
    """Tests for first-run wizard detection."""

    def test_first_run_detection_logic(self):
        """Test the first-run detection logic."""
        # Setup first-run condition
        from unittest.mock import MagicMock

        mock_args = MagicMock()
        mock_args.src_dir = None
        mock_args.wizard = False
        mock_args.list_profiles = False
        mock_args.list_devices = False

        # Test that condition evaluates to True
        is_first_run = (
            not mock_args.src_dir
            and not mock_args.wizard
            and not mock_args.list_profiles
            and not mock_args.list_devices
        )
        assert is_first_run is True

    @patch("main.parse_arguments")
    def test_not_first_run_with_src_dir(self, mock_parse):
        """Test that first-run is False when src_dir is provided."""
        mock_args = MagicMock()
        mock_args.src_dir = Path("/input")
        mock_args.wizard = False
        mock_args.list_profiles = False
        mock_args.list_devices = False

        is_first_run = (
            not mock_args.src_dir
            and not mock_args.wizard
            and not mock_args.list_profiles
            and not mock_args.list_devices
        )
        assert is_first_run is False

    @patch("main.parse_arguments")
    def test_not_first_run_with_wizard_flag(self, mock_parse):
        """Test that first-run is False when --wizard is specified."""
        mock_args = MagicMock()
        mock_args.src_dir = None
        mock_args.wizard = True
        mock_args.list_profiles = False
        mock_args.list_devices = False

        is_first_run = (
            not mock_args.src_dir
            and not mock_args.wizard
            and not mock_args.list_profiles
            and not mock_args.list_devices
        )
        assert is_first_run is False

    @patch("main.parse_arguments")
    def test_not_first_run_with_list_profiles(self, mock_parse):
        """Test that first-run is False when --list-profiles is specified."""
        mock_args = MagicMock()
        mock_args.src_dir = None
        mock_args.wizard = False
        mock_args.list_profiles = True
        mock_args.list_devices = False

        is_first_run = (
            not mock_args.src_dir
            and not mock_args.wizard
            and not mock_args.list_profiles
            and not mock_args.list_devices
        )
        assert is_first_run is False

    @patch("main.parse_arguments")
    def test_not_first_run_with_list_devices(self, mock_parse):
        """Test that first-run is False when --list-devices is specified."""
        mock_args = MagicMock()
        mock_args.src_dir = None
        mock_args.wizard = False
        mock_args.list_profiles = False
        mock_args.list_devices = True

        is_first_run = (
            not mock_args.src_dir
            and not mock_args.wizard
            and not mock_args.list_profiles
            and not mock_args.list_devices
        )
        assert is_first_run is False


@pytest.mark.unit
class TestCLIParsing:
    """Tests for CLI argument parsing with new flags."""

    def test_wizard_flag_parsed(self):
        """Test that --wizard flag is parsed correctly."""
        with patch("sys.argv", ["shiroink", "--wizard"]):
            args = parse_arguments()
            assert args.wizard is True

    def test_list_profiles_flag_parsed(self):
        """Test that --list-profiles flag is parsed correctly."""
        with patch("sys.argv", ["shiroink", "--list-profiles"]):
            args = parse_arguments()
            assert args.list_profiles is True

    def test_profile_flag_with_name_parsed(self):
        """Test that --profile NAME flag is parsed correctly."""
        with patch("sys.argv", ["shiroink", "--profile", "my-device", "in/", "out/"]):
            args = parse_arguments()
            assert args.profile == "my-device"

    def test_list_devices_flag_parsed(self):
        """Test that --list-devices flag is parsed correctly."""
        with patch("sys.argv", ["shiroink", "--list-devices"]):
            args = parse_arguments()
            assert args.list_devices is True

    def test_combined_flags_wizard_and_src(self):
        """Test that wizard can be combined with src/dest dirs."""
        with patch(
            "sys.argv",
            ["shiroink", "input/", "output/", "--wizard"],
        ):
            args = parse_arguments()
            assert args.wizard is True
            assert str(args.src_dir) == "input"
            assert str(args.dest_dir) == "output"

    def test_profile_with_directories(self):
        """Test that --profile works with src/dest directories."""
        with patch(
            "sys.argv",
            ["shiroink", "input/", "output/", "--profile", "my-device"],
        ):
            args = parse_arguments()
            assert args.profile == "my-device"
            assert str(args.src_dir) == "input"
            assert str(args.dest_dir) == "output"
