"""
Unit tests for parameter validator.
"""

import pytest
from pathlib import Path
from parameter_validator import ParameterValidator


@pytest.mark.unit
class TestParameterValidator:
    """Tests for ParameterValidator class."""

    def test_validate_resolution_valid(self):
        """Test validation of valid resolutions."""
        is_valid, error = ParameterValidator.validate_resolution((1072, 1448))
        assert is_valid is True
        assert error is None

    def test_validate_resolution_too_small(self):
        """Test validation fails for too small resolution."""
        is_valid, error = ParameterValidator.validate_resolution((100, 100))
        assert is_valid is False
        assert "at least 200x200" in error

    def test_validate_resolution_too_large(self):
        """Test validation fails for too large resolution."""
        is_valid, error = ParameterValidator.validate_resolution((50000, 50000))
        assert is_valid is False
        assert "exceeds maximum" in error

    def test_validate_resolution_invalid_format(self):
        """Test validation fails for invalid format."""
        is_valid, error = ParameterValidator.validate_resolution("800x600")
        assert is_valid is False

    def test_validate_quality_valid(self):
        """Test validation of valid quality levels."""
        for quality in range(1, 10):
            is_valid, error = ParameterValidator.validate_quality(quality)
            assert is_valid is True
            assert error is None

    def test_validate_quality_too_low(self):
        """Test validation fails for quality too low."""
        is_valid, error = ParameterValidator.validate_quality(0)
        assert is_valid is False
        assert "between 1 and 9" in error

    def test_validate_quality_too_high(self):
        """Test validation fails for quality too high."""
        is_valid, error = ParameterValidator.validate_quality(10)
        assert is_valid is False
        assert "between 1 and 9" in error

    def test_validate_workers_valid(self):
        """Test validation of valid worker counts."""
        for workers in [1, 4, 8, 16]:
            is_valid, error = ParameterValidator.validate_workers(workers)
            assert is_valid is True
            assert error is None

    def test_validate_workers_zero(self):
        """Test validation fails for zero workers."""
        is_valid, error = ParameterValidator.validate_workers(0)
        assert is_valid is False
        assert "at least 1" in error

    def test_validate_workers_too_many(self):
        """Test validation fails for too many workers."""
        is_valid, error = ParameterValidator.validate_workers(300)
        assert is_valid is False
        assert "cannot exceed 256" in error

    def test_validate_device_valid(self):
        """Test validation of valid device keys."""
        is_valid, error = ParameterValidator.validate_device("kindle_paperwhite")
        assert is_valid is True
        assert error is None

    def test_validate_device_unknown(self):
        """Test validation fails for unknown device."""
        is_valid, error = ParameterValidator.validate_device("unknown_device")
        assert is_valid is False
        assert "Unknown device" in error

    def test_find_similar_device(self):
        """Test finding similar device."""
        all_devices = ParameterValidator._get_all_devices()
        similar = ParameterValidator._find_similar_device("kindle_paper", all_devices)
        assert similar is not None
        assert "kindle" in similar

    def test_suggest_quality_level_fast(self):
        """Test quality level suggestions."""
        quality, description = ParameterValidator.suggest_quality_level("fast")
        assert quality == 3
        assert "fast" in description.lower()

    def test_suggest_quality_level_balanced(self):
        """Test balanced quality suggestion."""
        quality, description = ParameterValidator.suggest_quality_level("balanced")
        assert quality == 6

    def test_suggest_quality_level_best(self):
        """Test best quality suggestion."""
        quality, description = ParameterValidator.suggest_quality_level("best")
        assert quality == 9

    def test_suggest_workers(self):
        """Test worker suggestion."""
        workers = ParameterValidator.suggest_workers()
        assert isinstance(workers, int)
        assert workers >= 1
        assert workers <= 256

    def test_validate_configuration_valid(self):
        """Test validation of valid configuration."""
        config = {
            "src_dir": "/input",
            "dest_dir": "/output",
            "quality": 6,
            "workers": 4,
        }
        is_valid, errors = ParameterValidator.validate_configuration(config)
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_configuration_missing_required(self):
        """Test validation fails for missing required fields."""
        config = {"src_dir": "/input"}
        is_valid, errors = ParameterValidator.validate_configuration(config)
        assert is_valid is False
        assert any("dest_dir" in error for error in errors)

    def test_validate_configuration_invalid_quality(self):
        """Test validation fails for invalid quality."""
        config = {
            "src_dir": "/input",
            "dest_dir": "/output",
            "quality": 15,
        }
        is_valid, errors = ParameterValidator.validate_configuration(config)
        assert is_valid is False
        assert any("quality" in error for error in errors)

    def test_validate_configuration_invalid_workers(self):
        """Test validation fails for invalid workers."""
        config = {
            "src_dir": "/input",
            "dest_dir": "/output",
            "workers": -1,
        }
        is_valid, errors = ParameterValidator.validate_configuration(config)
        assert is_valid is False
        assert any("workers" in error for error in errors)
