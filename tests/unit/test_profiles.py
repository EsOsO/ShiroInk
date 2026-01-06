"""
Unit tests for ProfileManager.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

from profiles.manager import ProfileManager
from profiles.schema import ProfileSchema


@pytest.fixture
def temp_profiles_dir():
    """Create a temporary directory for profiles."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def profile_manager(temp_profiles_dir):
    """Create a ProfileManager with a temp directory."""
    manager = ProfileManager()
    manager.profiles_dir = temp_profiles_dir
    return manager


@pytest.mark.unit
class TestProfileManagerBasic:
    """Test basic profile management operations."""

    def test_save_and_load_profile(self, profile_manager):
        """Test saving and loading a profile."""
        profile_manager.save(
            name="test-profile",
            device="kindle_paperwhite_11",
            resolution=(1236, 1648),
            quality=8,
        )

        loaded = profile_manager.load("test-profile")

        assert loaded.name == "test-profile"
        assert loaded.device == "kindle_paperwhite_11"
        assert loaded.resolution == (1236, 1648)
        assert loaded.quality == 8

    def test_list_profiles(self, profile_manager):
        """Test listing profiles."""
        profile_manager.save(name="profile1", device="kindle")
        profile_manager.save(name="profile2", device="kobo")

        profiles = profile_manager.list_profiles()

        assert len(profiles) == 2
        names = [p["name"] for p in profiles]
        assert "profile1" in names
        assert "profile2" in names

    def test_delete_profile(self, profile_manager):
        """Test deleting a profile."""
        profile_manager.save(name="to-delete", device="kindle")

        assert profile_manager.exists("to-delete")

        profile_manager.delete("to-delete")

        assert not profile_manager.exists("to-delete")

    def test_exists_returns_false_for_nonexistent(self, profile_manager):
        """Test exists returns False for non-existent profile."""
        assert profile_manager.exists("nonexistent") is False


@pytest.mark.unit
class TestProfileManagerDisplay:
    """Test profile display formatting."""

    def test_format_profiles_for_display_empty(self, profile_manager):
        """Test formatting empty profile list."""
        output = profile_manager.format_profiles_for_display()

        assert "No saved profiles found" in output

    def test_format_profiles_for_display_with_profiles(self, profile_manager):
        """Test formatting profile list with profiles."""
        profile_manager.save(
            name="test-profile",
            device="kindle_paperwhite_11",
        )

        output = profile_manager.format_profiles_for_display()

        assert "Saved Profiles" in output
        assert "test-profile" in output
        assert "--profile" in output

    def test_format_profiles_shows_metadata(self, profile_manager):
        """Test that formatted output shows creation date."""
        profile_manager.save(name="test-profile", device="kindle")

        output = profile_manager.format_profiles_for_display()

        assert "Created:" in output
        assert "Last used:" in output


@pytest.mark.unit
class TestProfileManagerApplyToArgs:
    """Test apply_to_args method."""

    def test_apply_to_args_device(self, profile_manager):
        """Test applying device from profile."""
        profile_manager.save(name="test-profile", device="kindle_paperwhite_11")

        class Args:
            device = None
            resolution = None
            quality = 6
            workers = 4
            rtl = False

        args = Args()
        profile_manager.apply_to_args(args, "test-profile")

        assert args.device == "kindle_paperwhite_11"

    def test_apply_to_args_resolution(self, profile_manager):
        """Test applying resolution from profile."""
        profile_manager.save(
            name="test-profile",
            resolution=(1236, 1648),
        )

        class Args:
            device = None
            resolution = None
            quality = 6
            workers = 4
            rtl = False

        args = Args()
        profile_manager.apply_to_args(args, "test-profile")

        assert args.resolution == (1236, 1648)

    def test_apply_to_args_does_not_override_existing_device(self, profile_manager):
        """Test that apply_to_args doesn't override existing device."""
        profile_manager.save(name="test-profile", device="kobo")

        class Args:
            device = "kindle"
            resolution = None
            quality = 6
            workers = 4
            rtl = False

        args = Args()
        profile_manager.apply_to_args(args, "test-profile")

        assert args.device == "kindle"

    def test_apply_to_args_quality(self, profile_manager):
        """Test applying quality from profile."""
        profile_manager.save(name="test-profile", quality=9)

        class Args:
            device = None
            resolution = None
            quality = 6
            workers = 4
            rtl = False

        args = Args()
        profile_manager.apply_to_args(args, "test-profile")

        assert args.quality == 9

    def test_apply_to_args_workers(self, profile_manager):
        """Test applying workers from profile."""
        profile_manager.save(name="test-profile", workers=8)

        class Args:
            device = None
            resolution = None
            quality = 6
            workers = 4
            rtl = False

        args = Args()
        profile_manager.apply_to_args(args, "test-profile")

        assert args.workers == 8

    def test_apply_to_args_rtl(self, profile_manager):
        """Test applying rtl from profile."""
        profile_manager.save(name="test-profile", rtl=True)

        class Args:
            device = None
            resolution = None
            quality = 6
            workers = 4
            rtl = False

        args = Args()
        profile_manager.apply_to_args(args, "test-profile")

        assert args.rtl is True
