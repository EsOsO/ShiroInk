"""
Unit tests for image processing pipeline and presets.

Tests cover:
- Pipeline creation and step management
- Preset pipeline configurations
- from_device_spec() factory method
- Device-aware pipeline generation
"""

import pytest
from PIL import Image

from src.image_pipeline.pipeline import ImagePipeline
from src.image_pipeline.presets import PipelinePresets
from src.image_pipeline.contrast import ContrastStep
from src.image_pipeline.sharpen import SharpenStep
from src.image_pipeline.quantize import QuantizeStep
from src.image_pipeline.color_profile import ColorProfileStep
from src.image_pipeline.devices import DeviceSpecs, ColorGamut


class TestImagePipeline:
    """Test basic pipeline functionality."""

    def test_empty_pipeline_creation(self):
        """Empty pipeline should have zero steps."""
        pipeline = ImagePipeline()
        
        assert len(pipeline) == 0
        assert pipeline.get_steps() == []

    def test_add_single_step(self):
        """Adding a single step should work."""
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep(factor=1.5))
        
        assert len(pipeline) == 1
        assert pipeline.get_steps() == ["Contrast"]

    def test_add_multiple_steps(self):
        """Adding multiple steps should maintain order."""
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep(factor=1.5))
        pipeline.add_step(SharpenStep(factor=1.2))
        pipeline.add_step(QuantizeStep())
        
        assert len(pipeline) == 3
        assert pipeline.get_steps() == ["Contrast", "Sharpen", "Quantize(16)"]

    def test_method_chaining(self):
        """Pipeline should support method chaining."""
        pipeline = (ImagePipeline()
                   .add_step(ContrastStep())
                   .add_step(SharpenStep()))
        
        assert len(pipeline) == 2

    def test_remove_step(self):
        """Removing a step should work correctly."""
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep())
        pipeline.add_step(SharpenStep())
        pipeline.add_step(QuantizeStep())
        
        pipeline.remove_step("Sharpen")
        
        assert len(pipeline) == 2
        assert pipeline.get_steps() == ["Contrast", "Quantize(16)"]

    def test_clear_pipeline(self):
        """Clearing pipeline should remove all steps."""
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep())
        pipeline.add_step(SharpenStep())
        
        pipeline.clear()
        
        assert len(pipeline) == 0

    def test_process_empty_pipeline(self, test_image):
        """Empty pipeline should return image unchanged."""
        pipeline = ImagePipeline()
        result = pipeline.process(test_image)
        
        assert isinstance(result, Image.Image)
        assert result.size == test_image.size

    def test_process_with_steps(self, test_image):
        """Pipeline with steps should process image."""
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep(factor=1.5))
        pipeline.add_step(SharpenStep(factor=1.2))
        
        result = pipeline.process(test_image)
        
        assert isinstance(result, Image.Image)
        assert result.size == test_image.size


class TestPipelinePresets:
    """Test predefined pipeline presets."""

    def test_kindle_preset(self):
        """Kindle preset should have contrast, sharpen, and quantize."""
        pipeline = PipelinePresets.kindle()
        steps = pipeline.get_steps()
        
        assert len(pipeline) == 3
        assert "Contrast" in steps
        assert "Sharpen" in steps
        assert "Quantize" in steps

    def test_tablet_preset(self):
        """Tablet preset should have contrast and sharpen, no quantize."""
        pipeline = PipelinePresets.tablet()
        steps = pipeline.get_steps()
        
        assert len(pipeline) == 2
        assert "Contrast" in steps
        assert "Sharpen" in steps
        assert "Quantize" not in steps

    def test_print_preset(self):
        """Print preset should only sharpen."""
        pipeline = PipelinePresets.print()
        steps = pipeline.get_steps()
        
        assert len(pipeline) == 1
        assert "Sharpen" in steps

    def test_minimal_preset(self):
        """Minimal preset should have no steps."""
        pipeline = PipelinePresets.minimal()
        
        assert len(pipeline) == 0

    def test_high_quality_preset(self):
        """High quality preset should have contrast and sharpen."""
        pipeline = PipelinePresets.high_quality()
        steps = pipeline.get_steps()
        
        assert len(pipeline) == 2
        assert "Contrast" in steps
        assert "Sharpen" in steps

    def test_custom_preset_full(self):
        """Custom preset with all parameters."""
        pipeline = PipelinePresets.custom(
            contrast=1.8,
            sharpen=1.5,
            quantize=True
        )
        
        assert len(pipeline) == 3
        assert pipeline.get_steps() == ["Contrast", "Sharpen", "Quantize(16)"]

    def test_custom_preset_partial(self):
        """Custom preset with partial parameters."""
        pipeline = PipelinePresets.custom(contrast=1.5)
        
        assert len(pipeline) == 1
        assert pipeline.get_steps() == ["Contrast"]

    def test_get_preset_by_name(self):
        """Get preset by name string."""
        pipeline = PipelinePresets.get_preset("kindle")
        
        assert len(pipeline) == 3

    def test_get_preset_invalid_name(self):
        """Invalid preset name should raise ValueError."""
        with pytest.raises(ValueError):
            PipelinePresets.get_preset("invalid_preset")

    def test_list_presets(self):
        """List presets should return all available presets."""
        presets = PipelinePresets.list_presets()
        
        # Generic presets
        assert "kindle" in presets
        assert "tablet" in presets
        assert "print" in presets
        assert "minimal" in presets
        
        # Device-specific presets
        assert "kobo" in presets
        assert "tolino" in presets
        assert "pocketbook" in presets
        assert "pocketbook_color" in presets
        assert "ipad" in presets


class TestDeviceSpecificPresets:
    """Test device-specific preset configurations."""

    def test_kobo_preset(self):
        """Kobo preset should be optimized for Kobo e-readers."""
        pipeline = PipelinePresets.kobo()
        steps = pipeline.get_steps()
        
        assert len(pipeline) == 3
        assert "Contrast" in steps
        assert "Sharpen" in steps
        assert "Quantize" in steps

    def test_tolino_preset(self):
        """Tolino preset should be optimized for Tolino e-readers."""
        pipeline = PipelinePresets.tolino()
        steps = pipeline.get_steps()
        
        assert len(pipeline) == 3
        assert "Contrast" in steps
        assert "Sharpen" in steps
        assert "Quantize" in steps

    def test_pocketbook_preset(self):
        """PocketBook preset should be optimized for B&W PocketBook."""
        pipeline = PipelinePresets.pocketbook()
        steps = pipeline.get_steps()
        
        assert len(pipeline) == 3
        assert "Contrast" in steps
        assert "Sharpen" in steps
        assert "Quantize" in steps

    def test_pocketbook_color_preset(self):
        """PocketBook color preset should preserve colors."""
        pipeline = PipelinePresets.pocketbook_color()
        steps = pipeline.get_steps()
        
        assert len(pipeline) == 2
        assert "Contrast" in steps
        assert "Sharpen" in steps
        assert "Quantize" not in steps

    def test_ipad_preset(self):
        """iPad preset should be optimized for high-quality displays."""
        pipeline = PipelinePresets.ipad()
        steps = pipeline.get_steps()
        
        assert len(pipeline) == 2
        assert "Contrast" in steps
        assert "Sharpen" in steps
        assert "Quantize" not in steps

    def test_eink_preset(self):
        """Generic e-ink preset for any e-reader."""
        pipeline = PipelinePresets.eink()
        steps = pipeline.get_steps()
        
        assert len(pipeline) == 3
        assert "Contrast" in steps
        assert "Sharpen" in steps
        assert "Quantize" in steps


class TestFromDeviceSpec:
    """Test from_device_spec() factory method for device-aware pipelines."""

    def test_bw_eink_device_pipeline(self):
        """B&W e-ink devices should get ColorProfile, Contrast, Sharpen, Quantize."""
        device = DeviceSpecs.get_device("kindle_paperwhite_11")
        pipeline = PipelinePresets.from_device_spec(device)
        steps = pipeline.get_steps()
        
        assert len(pipeline) == 4
        assert "ColorProfile" in steps
        assert "Contrast" in steps
        assert "Sharpen" in steps
        assert "Quantize" in steps

    def test_color_eink_device_pipeline(self):
        """Color e-ink devices should get ColorProfile, Contrast, Sharpen, Quantize."""
        device = DeviceSpecs.get_device("pocketbook_inkpad_color_3")
        pipeline = PipelinePresets.from_device_spec(device)
        steps = pipeline.get_steps()
        
        assert len(pipeline) == 4
        assert "ColorProfile" in steps
        assert "Contrast" in steps
        assert "Sharpen" in steps
        assert "Quantize" in steps  # 12-bit needs quantization

    def test_ipad_device_pipeline(self):
        """iPad devices should get ColorProfile, Contrast, Sharpen (no quantize)."""
        device = DeviceSpecs.get_device("ipad_pro_11")
        pipeline = PipelinePresets.from_device_spec(device)
        steps = pipeline.get_steps()
        
        assert len(pipeline) == 3
        assert "ColorProfile" in steps
        assert "Contrast" in steps
        assert "Sharpen" in steps
        assert "Quantize" not in steps  # 24-bit doesn't need quantization

    def test_all_devices_have_color_profile_step(self):
        """All devices should have ColorProfileStep as first step."""
        for device_key in DeviceSpecs.list_devices():
            device = DeviceSpecs.get_device(device_key)
            pipeline = PipelinePresets.from_device_spec(device)
            
            assert len(pipeline) > 0
            assert pipeline.get_steps()[0] == "ColorProfile"

    def test_quantization_based_on_bit_depth(self):
        """Quantization should be added for devices with bit_depth < 16."""
        for device_key in DeviceSpecs.list_devices():
            device = DeviceSpecs.get_device(device_key)
            pipeline = PipelinePresets.from_device_spec(device)
            steps = pipeline.get_steps()
            
            if device.bit_depth < 16:
                assert "Quantize" in steps
            else:
                assert "Quantize" not in steps


class TestPipelineProcessing:
    """Test that pipelines can process images."""

    def test_preset_can_process_image(self, test_image):
        """All presets should be able to process an image."""
        presets_to_test = [
            "kindle", "kobo", "tolino", "pocketbook",
            "pocketbook_color", "ipad", "tablet", "eink"
        ]
        
        for preset_name in presets_to_test:
            pipeline = PipelinePresets.get_preset(preset_name)
            result = pipeline.process(test_image)
            
            assert isinstance(result, Image.Image)
            assert result.size == test_image.size

    def test_device_specific_pipeline_can_process(self, test_image):
        """Device-specific pipelines should process images."""
        devices_to_test = [
            "kindle_paperwhite_11",
            "pocketbook_inkpad_color_3",
            "ipad_pro_11"
        ]
        
        for device_key in devices_to_test:
            device = DeviceSpecs.get_device(device_key)
            pipeline = PipelinePresets.from_device_spec(device)
            result = pipeline.process(test_image)
            
            assert isinstance(result, Image.Image)
            assert result.size == test_image.size
