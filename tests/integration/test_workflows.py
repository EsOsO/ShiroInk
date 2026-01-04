"""
Integration tests for end-to-end workflows.

Tests cover:
- Device preset selection and pipeline generation
- Image processing with device-specific pipelines
- Error handling and recovery
"""

import pytest
from pathlib import Path
from PIL import Image

from src.config import ProcessingConfig
from src.progress_reporter import SilentProgressReporter
from src.error_handler import ErrorTracker
from src.file_processor import process_images_in_directory
from src.image_pipeline.devices import DeviceSpecs
from src.image_pipeline.presets import PipelinePresets


class TestDevicePresetWorkflow:
    """Test complete workflow using device presets."""

    @pytest.mark.parametrize("device_key", [
        "kindle_paperwhite_11",
        "pocketbook_inkpad_color_3",
        "ipad_pro_11",
    ])
    def test_device_pipeline_end_to_end(self, device_key, test_color_image):
        """Test complete pipeline for different device types."""
        device = DeviceSpecs.get_device(device_key)
        pipeline = PipelinePresets.from_device_spec(device)
        
        result = pipeline.process(test_color_image)
        
        assert isinstance(result, Image.Image)
        assert result.size == test_color_image.size

    def test_bw_device_produces_grayscale(self, test_color_image):
        """B&W device pipeline should produce grayscale output."""
        device = DeviceSpecs.get_device("kindle_paperwhite_11")
        pipeline = PipelinePresets.from_device_spec(device)
        
        result = pipeline.process(test_color_image)
        
        # Should be grayscale after ColorProfileStep
        assert result.mode in ("L", "P")  # L for grayscale, P for palette

    def test_color_device_preserves_color(self, test_color_image):
        """Color device pipeline should preserve RGB mode."""
        device = DeviceSpecs.get_device("ipad_pro_11")
        pipeline = PipelinePresets.from_device_spec(device)
        
        result = pipeline.process(test_color_image)
        
        assert result.mode in ("RGB", "P")


class TestFileProcessing:
    """Test file processing with device presets."""

    def test_process_directory_with_silent_reporter(self, sample_images, tmp_path):
        """Test processing directory with silent reporter."""
        dest_dir = tmp_path / "output"
        dest_dir.mkdir()
        
        config = ProcessingConfig(
            src_dir=sample_images,
            dest_dir=dest_dir,
            dry_run=True,
        )
        reporter = SilentProgressReporter()
        error_tracker = ErrorTracker()
        
        # Should not raise exceptions
        process_images_in_directory(
            sample_images,
            config,
            reporter,
            error_tracker
        )

    def test_error_tracking(self, tmp_path):
        """Test error tracking during processing."""
        from src.error_handler import ErrorSeverity
        
        error_tracker = ErrorTracker()
        
        # Simulate adding errors
        test_error = ValueError("Test error")
        error_tracker.add_error(
            error=test_error,
            path=Path("test.jpg"),
            step="TestStep",
            severity=ErrorSeverity.ERROR
        )
        
        assert error_tracker.has_errors()
        summary = error_tracker.get_summary()
        assert summary["total_errors"] == 1


class TestConfigurationValidation:
    """Test configuration validation."""

    def test_valid_config_creation(self, tmp_path):
        """Valid configuration should be created successfully."""
        src = tmp_path / "src"
        dest = tmp_path / "dest"
        src.mkdir()
        dest.mkdir()
        
        config = ProcessingConfig(
            src_dir=src,
            dest_dir=dest,
            resolution=(1000, 1000),
        )
        
        assert config.src_dir == src
        assert config.dest_dir == dest
        assert config.resolution == (1000, 1000)

    def test_invalid_quality_raises_error(self, tmp_path):
        """Invalid quality should raise ValueError."""
        src = tmp_path / "src"
        dest = tmp_path / "dest"
        src.mkdir()
        dest.mkdir()
        
        with pytest.raises(ValueError):
            ProcessingConfig(
                src_dir=src,
                dest_dir=dest,
                quality=10,  # Invalid: must be 1-9
            )

    def test_custom_pipeline_usage(self, tmp_path):
        """Test using custom pipeline in config."""
        src = tmp_path / "src"
        dest = tmp_path / "dest"
        src.mkdir()
        dest.mkdir()
        
        device = DeviceSpecs.get_device("kindle_paperwhite_11")
        custom_pipeline = PipelinePresets.from_device_spec(device)
        
        config = ProcessingConfig(
            src_dir=src,
            dest_dir=dest,
            custom_pipeline=custom_pipeline,
        )
        
        pipeline = config.get_pipeline()
        assert pipeline == custom_pipeline
