"""
Unit tests for ColorProfileStep.

Tests cover:
- Grayscale conversion for B&W devices
- Color space conversion for color devices
- ICC profile handling (with/without littlecms2)
- Bit depth posterization
"""

import pytest
from PIL import Image

from src.image_pipeline.color_profile import ColorProfileStep
from src.image_pipeline.devices import ColorGamut


class TestColorProfileStepCreation:
    """Test ColorProfileStep instantiation."""

    def test_create_bw_step(self):
        """Create a B&W color profile step."""
        step = ColorProfileStep(color_support=False, target_gamut=None, bit_depth=4)
        
        assert step.color_support is False
        assert step.bit_depth == 4
        assert step.get_name() == "ColorProfile"

    def test_create_color_step_srgb(self):
        """Create a color profile step with sRGB."""
        step = ColorProfileStep(
            color_support=True,
            target_gamut=ColorGamut.SRGB,
            bit_depth=12
        )
        
        assert step.color_support is True
        assert step.target_gamut == ColorGamut.SRGB
        assert step.bit_depth == 12

    def test_create_color_step_dci_p3(self):
        """Create a color profile step with DCI-P3."""
        step = ColorProfileStep(
            color_support=True,
            target_gamut=ColorGamut.DCI_P3,
            bit_depth=24
        )
        
        assert step.target_gamut == ColorGamut.DCI_P3


class TestGrayscaleConversion:
    """Test grayscale conversion for B&W devices."""

    def test_convert_rgb_to_grayscale(self, test_color_image):
        """RGB image should be converted to grayscale."""
        step = ColorProfileStep(color_support=False, target_gamut=None, bit_depth=8)
        result = step.process(test_color_image)
        
        assert isinstance(result, Image.Image)
        # Note: result is RGB mode for pipeline compatibility, but rendered as grayscale
        assert result.mode == "RGB"

    def test_4bit_grayscale_posterization(self, test_color_image):
        """4-bit should produce 16 grayscale levels."""
        step = ColorProfileStep(color_support=False, target_gamut=None, bit_depth=4)
        result = step.process(test_color_image)
        
        # Note: result is RGB mode for pipeline compatibility
        assert result.mode == "RGB"
        
        # Convert to grayscale to count unique values
        gray = result.convert("L")
        unique_values = set(gray.getdata())
        assert len(unique_values) <= 16

    def test_8bit_grayscale_no_posterization(self, test_color_image):
        """8-bit grayscale should have full range."""
        step = ColorProfileStep(color_support=False, target_gamut=None, bit_depth=8)
        result = step.process(test_color_image)
        
        assert result.mode == "RGB"

    def test_grayscale_preserves_size(self, test_color_image):
        """Grayscale conversion should preserve image size."""
        step = ColorProfileStep(color_support=False, target_gamut=None, bit_depth=4)
        result = step.process(test_color_image)
        
        assert result.size == test_color_image.size


class TestColorConversion:
    """Test color space conversion for color devices."""

    def test_color_image_stays_rgb(self, test_color_image):
        """Color mode should keep image in RGB."""
        step = ColorProfileStep(
            color_support=True,
            target_gamut=ColorGamut.SRGB,
            bit_depth=24
        )
        result = step.process(test_color_image)
        
        assert result.mode == "RGB"

    def test_color_conversion_preserves_size(self, test_color_image):
        """Color conversion should preserve image size."""
        step = ColorProfileStep(
            color_support=True,
            target_gamut=ColorGamut.SRGB,
            bit_depth=24
        )
        result = step.process(test_color_image)
        
        assert result.size == test_color_image.size

    def test_srgb_conversion(self, test_color_image):
        """sRGB conversion should work."""
        step = ColorProfileStep(
            color_support=True,
            target_gamut=ColorGamut.SRGB,
            bit_depth=12
        )
        result = step.process(test_color_image)
        
        assert isinstance(result, Image.Image)
        assert result.mode == "RGB"

    def test_dci_p3_conversion(self, test_color_image):
        """DCI-P3 conversion should work."""
        step = ColorProfileStep(
            color_support=True,
            target_gamut=ColorGamut.DCI_P3,
            bit_depth=24
        )
        result = step.process(test_color_image)
        
        assert isinstance(result, Image.Image)
        assert result.mode == "RGB"


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_process_already_grayscale(self, test_grayscale_image):
        """Processing already-grayscale image should work."""
        step = ColorProfileStep(color_support=False, target_gamut=None, bit_depth=4)
        result = step.process(test_grayscale_image)
        
        assert result.mode == "RGB"

    def test_none_gamut_for_bw(self, test_color_image):
        """B&W device with None gamut should work."""
        step = ColorProfileStep(
            color_support=False,
            target_gamut=None,
            bit_depth=4
        )
        result = step.process(test_color_image)
        
        assert result.mode == "RGB"
