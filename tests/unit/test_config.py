"""
Unit tests for ProcessingConfig.
"""

import pytest
from pathlib import Path
from config import ProcessingConfig


@pytest.mark.unit
class TestProcessingConfig:
    """Tests for ProcessingConfig class."""

    def test_config_initialization_with_defaults(self):
        """Test ProcessingConfig initializes with default values."""
        config = ProcessingConfig(
            src_dir=Path("/input"),
            dest_dir=Path("/output"),
        )

        assert config.src_dir == Path("/input")
        assert config.dest_dir == Path("/output")
        assert config.resolution == (1404, 1872)
        assert config.rtl is False
        assert config.quality == 6
        assert config.workers == 4
        assert config.pipeline_preset == "kindle"
        assert config.loaded_profile is None

    def test_config_with_custom_values(self):
        """Test ProcessingConfig with custom values."""
        config = ProcessingConfig(
            src_dir=Path("/input"),
            dest_dir=Path("/output"),
            resolution=(1072, 1448),
            rtl=True,
            quality=8,
            workers=8,
            pipeline_preset="kobo",
            loaded_profile="my-device",
        )

        assert config.resolution == (1072, 1448)
        assert config.rtl is True
        assert config.quality == 8
        assert config.workers == 8
        assert config.pipeline_preset == "kobo"
        assert config.loaded_profile == "my-device"

    def test_config_loaded_profile_tracks_profile_name(self):
        """Test that loaded_profile field tracks which profile was loaded."""
        config1 = ProcessingConfig(
            src_dir=Path("/input"),
            dest_dir=Path("/output"),
            loaded_profile="profile1",
        )
        assert config1.loaded_profile == "profile1"

        config2 = ProcessingConfig(
            src_dir=Path("/input"),
            dest_dir=Path("/output"),
            loaded_profile=None,
        )
        assert config2.loaded_profile is None

    def test_config_quality_validation_too_low(self):
        """Test that quality validation rejects values below 1."""
        with pytest.raises(ValueError, match="Quality must be between 1 and 9"):
            ProcessingConfig(
                src_dir=Path("/input"),
                dest_dir=Path("/output"),
                quality=0,
            )

    def test_config_quality_validation_too_high(self):
        """Test that quality validation rejects values above 9."""
        with pytest.raises(ValueError, match="Quality must be between 1 and 9"):
            ProcessingConfig(
                src_dir=Path("/input"),
                dest_dir=Path("/output"),
                quality=10,
            )

    def test_config_workers_validation_negative(self):
        """Test that workers validation rejects negative values."""
        with pytest.raises(ValueError, match="Workers must be at least 1"):
            ProcessingConfig(
                src_dir=Path("/input"),
                dest_dir=Path("/output"),
                workers=0,
            )

    def test_config_resolution_validation_invalid(self):
        """Test that resolution validation rejects invalid values."""
        with pytest.raises(ValueError, match="Resolution values must be positive"):
            ProcessingConfig(
                src_dir=Path("/input"),
                dest_dir=Path("/output"),
                resolution=(0, 1448),
            )

    def test_config_max_retries_validation(self):
        """Test that max_retries validation rejects negative values."""
        with pytest.raises(ValueError, match="Max retries must be non-negative"):
            ProcessingConfig(
                src_dir=Path("/input"),
                dest_dir=Path("/output"),
                max_retries=-1,
            )

    def test_config_all_valid_quality_values(self):
        """Test that all valid quality values 1-9 are accepted."""
        for quality in range(1, 10):
            config = ProcessingConfig(
                src_dir=Path("/input"),
                dest_dir=Path("/output"),
                quality=quality,
            )
            assert config.quality == quality

    def test_config_loaded_profile_none_when_not_specified(self):
        """Test that loaded_profile defaults to None."""
        config = ProcessingConfig(
            src_dir=Path("/input"),
            dest_dir=Path("/output"),
        )
        assert config.loaded_profile is None

    def test_config_loaded_profile_empty_string(self):
        """Test that loaded_profile can be empty string."""
        config = ProcessingConfig(
            src_dir=Path("/input"),
            dest_dir=Path("/output"),
            loaded_profile="",
        )
        assert config.loaded_profile == ""

    def test_config_loaded_profile_with_special_chars(self):
        """Test that loaded_profile accepts special characters."""
        config = ProcessingConfig(
            src_dir=Path("/input"),
            dest_dir=Path("/output"),
            loaded_profile="my-device-v2.0",
        )
        assert config.loaded_profile == "my-device-v2.0"
