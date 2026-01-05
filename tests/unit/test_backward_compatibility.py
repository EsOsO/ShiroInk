"""
Unit tests for backward compatibility with legacy CLI flags.

Ensures that existing CLI arguments continue to work with the new
interactive wizard and profile system.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from cli import parse_arguments


@pytest.mark.unit
class TestBackwardCompatibilityLegacyFlags:
    """Tests for backward compatibility with legacy CLI flags."""

    def test_legacy_resolution_flag(self):
        """Test that legacy --resolution flag still works."""
        with patch(
            "sys.argv", ["shiroink", "input/", "output/", "--resolution", "1920x1080"]
        ):
            args = parse_arguments()
            assert args.resolution == (1920, 1080)

    def test_legacy_device_flag(self):
        """Test that legacy --device flag still works."""
        with patch(
            "sys.argv",
            ["shiroink", "input/", "output/", "--device", "kindle_paperwhite"],
        ):
            args = parse_arguments()
            assert args.device == "kindle_paperwhite"

    def test_legacy_quality_flag_short(self):
        """Test that legacy -q short quality flag still works."""
        with patch("sys.argv", ["shiroink", "input/", "output/", "-q", "8"]):
            args = parse_arguments()
            assert args.quality == 8

    def test_legacy_quality_flag_long(self):
        """Test that legacy --quality long flag still works."""
        with patch("sys.argv", ["shiroink", "input/", "output/", "--quality", "7"]):
            args = parse_arguments()
            assert args.quality == 7

    def test_legacy_workers_flag_short(self):
        """Test that legacy -w short workers flag still works."""
        with patch("sys.argv", ["shiroink", "input/", "output/", "-w", "8"]):
            args = parse_arguments()
            assert args.workers == 8

    def test_legacy_workers_flag_long(self):
        """Test that legacy --workers long flag still works."""
        with patch("sys.argv", ["shiroink", "input/", "output/", "--workers", "4"]):
            args = parse_arguments()
            assert args.workers == 4

    def test_legacy_pipeline_flag(self):
        """Test that legacy --pipeline flag still works."""
        with patch("sys.argv", ["shiroink", "input/", "output/", "--pipeline", "eink"]):
            args = parse_arguments()
            assert args.pipeline == "eink"

    def test_legacy_rtl_flag(self):
        """Test that legacy --rtl flag still works."""
        with patch("sys.argv", ["shiroink", "input/", "output/", "--rtl"]):
            args = parse_arguments()
            assert args.rtl is True

    def test_legacy_rtl_flag_false_by_default(self):
        """Test that --rtl is False by default."""
        with patch("sys.argv", ["shiroink", "input/", "output/"]):
            args = parse_arguments()
            assert args.rtl is False

    def test_legacy_debug_flag(self):
        """Test that legacy --debug flag still works."""
        with patch("sys.argv", ["shiroink", "input/", "output/", "--debug"]):
            args = parse_arguments()
            assert args.debug is True

    def test_legacy_debug_flag_false_by_default(self):
        """Test that --debug is False by default."""
        with patch("sys.argv", ["shiroink", "input/", "output/"]):
            args = parse_arguments()
            assert args.debug is False

    def test_legacy_dry_run_flag(self):
        """Test that legacy --dry-run flag still works."""
        with patch("sys.argv", ["shiroink", "input/", "output/", "--dry-run"]):
            args = parse_arguments()
            assert args.dry_run is True

    def test_legacy_dry_run_flag_false_by_default(self):
        """Test that --dry-run is False by default."""
        with patch("sys.argv", ["shiroink", "input/", "output/"]):
            args = parse_arguments()
            assert args.dry_run is False

    def test_multiple_legacy_flags_combined(self):
        """Test combining multiple legacy flags."""
        with patch(
            "sys.argv",
            [
                "shiroink",
                "input/",
                "output/",
                "--resolution",
                "1440x1920",
                "--quality",
                "8",
                "--workers",
                "6",
                "--rtl",
                "--debug",
            ],
        ):
            args = parse_arguments()
            assert args.resolution == (1440, 1920)
            assert args.quality == 8
            assert args.workers == 6
            assert args.rtl is True
            assert args.debug is True

    def test_resolution_parsing_various_formats(self):
        """Test resolution parsing with various formats."""
        test_cases = [
            ("1920x1080", (1920, 1080)),
            ("1404x1872", (1404, 1872)),
            ("768x1024", (768, 1024)),
            ("600x800", (600, 800)),
        ]
        for resolution_str, expected_tuple in test_cases:
            with patch(
                "sys.argv",
                ["shiroink", "input/", "output/", "--resolution", resolution_str],
            ):
                args = parse_arguments()
                assert args.resolution == expected_tuple

    def test_quality_range_values(self):
        """Test quality accepts values from 1 to 9."""
        for quality in range(1, 10):
            with patch(
                "sys.argv",
                ["shiroink", "input/", "output/", "--quality", str(quality)],
            ):
                args = parse_arguments()
                assert args.quality == quality

    def test_workers_positive_values(self):
        """Test workers accepts positive integer values."""
        for workers in [1, 2, 4, 8, 16, 32]:
            with patch(
                "sys.argv",
                ["shiroink", "input/", "output/", "--workers", str(workers)],
            ):
                args = parse_arguments()
                assert args.workers == workers

    def test_pipeline_preset_values(self):
        """Test pipeline flag accepts various preset values."""
        presets = ["kindle", "kobo", "eink", "tablet", "print"]
        for preset in presets:
            with patch(
                "sys.argv",
                ["shiroink", "input/", "output/", "--pipeline", preset],
            ):
                args = parse_arguments()
                assert args.pipeline == preset


@pytest.mark.unit
class TestBackwardCompatibilityMixedWithNewFeatures:
    """Tests for using legacy flags with new features."""

    def test_legacy_flags_with_wizard(self):
        """Test that legacy flags don't interfere with wizard."""
        with patch(
            "sys.argv",
            ["shiroink", "--wizard", "--quality", "8"],
        ):
            args = parse_arguments()
            assert args.wizard is True
            assert args.quality == 8

    def test_legacy_flags_with_profile(self):
        """Test that legacy flags don't interfere with profile."""
        with patch(
            "sys.argv",
            [
                "shiroink",
                "input/",
                "output/",
                "--profile",
                "my-device",
                "--quality",
                "7",
            ],
        ):
            args = parse_arguments()
            assert args.profile == "my-device"
            assert args.quality == 7
            assert str(args.src_dir) == "input"
            assert str(args.dest_dir) == "output"

    def test_legacy_device_with_profile(self):
        """Test that --device works with --profile."""
        with patch(
            "sys.argv",
            [
                "shiroink",
                "input/",
                "output/",
                "--profile",
                "my-profile",
                "--device",
                "kindle_paperwhite",
            ],
        ):
            args = parse_arguments()
            assert args.profile == "my-profile"
            assert args.device == "kindle_paperwhite"

    def test_list_devices_legacy_compatibility(self):
        """Test that --list-devices is backward compatible."""
        with patch("sys.argv", ["shiroink", "--list-devices"]):
            args = parse_arguments()
            assert args.list_devices is True
            assert args.src_dir is None  # No directory needed


@pytest.mark.unit
class TestInputValidation:
    """Tests for input validation with legacy flags."""

    def test_required_directories(self):
        """Test that src_dir and dest_dir are required (unless special flags)."""
        with patch("sys.argv", ["shiroink"]):
            args = parse_arguments()
            # Both should be None when not provided
            assert args.src_dir is None
            assert args.dest_dir is None

    def test_directories_parsed_as_paths(self):
        """Test that directories are parsed as Path objects."""
        with patch("sys.argv", ["shiroink", "input_dir/", "output_dir/"]):
            args = parse_arguments()
            assert isinstance(args.src_dir, Path)
            assert isinstance(args.dest_dir, Path)

    def test_directory_names_without_trailing_slash(self):
        """Test directories work without trailing slash."""
        with patch("sys.argv", ["shiroink", "input", "output"]):
            args = parse_arguments()
            assert str(args.src_dir) == "input"
            assert str(args.dest_dir) == "output"

    def test_directory_names_with_trailing_slash(self):
        """Test directories work with trailing slash."""
        with patch("sys.argv", ["shiroink", "input/", "output/"]):
            args = parse_arguments()
            assert str(args.src_dir) == "input"
            assert str(args.dest_dir) == "output"

    def test_complex_directory_paths(self):
        """Test complex directory paths."""
        with patch(
            "sys.argv",
            ["shiroink", "/home/user/manga/input", "/home/user/manga/output"],
        ):
            args = parse_arguments()
            assert str(args.src_dir).endswith("input")
            assert str(args.dest_dir).endswith("output")

    def test_relative_directory_paths(self):
        """Test relative directory paths."""
        with patch("sys.argv", ["shiroink", "./input", "../output"]):
            args = parse_arguments()
            assert "input" in str(args.src_dir)
            assert "output" in str(args.dest_dir)


@pytest.mark.unit
class TestDefaultValues:
    """Tests for default values of CLI arguments."""

    def test_default_quality(self):
        """Test default quality value."""
        with patch("sys.argv", ["shiroink", "input/", "output/"]):
            args = parse_arguments()
            assert args.quality == 6

    def test_default_workers(self):
        """Test default workers value."""
        with patch("sys.argv", ["shiroink", "input/", "output/"]):
            args = parse_arguments()
            assert args.workers == 4

    def test_default_resolution_none(self):
        """Test default resolution is None."""
        with patch("sys.argv", ["shiroink", "input/", "output/"]):
            args = parse_arguments()
            assert args.resolution is None

    def test_default_device_none(self):
        """Test default device is None."""
        with patch("sys.argv", ["shiroink", "input/", "output/"]):
            args = parse_arguments()
            assert args.device is None

    def test_default_pipeline_none(self):
        """Test default pipeline is 'kindle'."""
        with patch("sys.argv", ["shiroink", "input/", "output/"]):
            args = parse_arguments()
            assert args.pipeline == "kindle"

    def test_default_wizard_false(self):
        """Test default wizard flag is False."""
        with patch("sys.argv", ["shiroink", "input/", "output/"]):
            args = parse_arguments()
            assert args.wizard is False

    def test_default_profile_none(self):
        """Test default profile is None."""
        with patch("sys.argv", ["shiroink", "input/", "output/"]):
            args = parse_arguments()
            assert args.profile is None

    def test_default_list_profiles_false(self):
        """Test default list_profiles flag is False."""
        with patch("sys.argv", ["shiroink", "input/", "output/"]):
            args = parse_arguments()
            assert args.list_profiles is False

    def test_default_list_devices_false(self):
        """Test default list_devices flag is False."""
        with patch("sys.argv", ["shiroink", "input/", "output/"]):
            args = parse_arguments()
            assert args.list_devices is False
