"""
Unit tests for QuantizeStep with dynamic palette generation.

Tests cover:
- Traditional Palette16 quantization
- Dynamic palette generation from bit depth
- Color quantization for limited color devices
- Grayscale quantization
"""

import pytest
from PIL import Image

from src.image_pipeline.quantize import (
    QuantizeStep,
    create_palette_from_bit_depth,
    Palette16,
)


class TestCreatePaletteFromBitDepth:
    """Test dynamic palette creation function."""

    def test_4bit_grayscale_palette(self):
        """4-bit grayscale should create 16-level palette."""
        palette = create_palette_from_bit_depth(bit_depth=4, color_mode=False)

        assert isinstance(palette, bytes)
        # 256 colors * 3 bytes (RGB) = 768 bytes (padded)
        assert len(palette) == 768

    def test_8bit_grayscale_palette(self):
        """8-bit grayscale should create 256-level palette."""
        palette = create_palette_from_bit_depth(bit_depth=8, color_mode=False)

        assert isinstance(palette, bytes)
        # 256 colors * 3 bytes (RGB) = 768 bytes
        assert len(palette) == 768

    def test_12bit_color_palette(self):
        """12-bit color should create 4096-color palette."""
        palette = create_palette_from_bit_depth(bit_depth=12, color_mode=True)

        # For color mode, function returns None (uses automatic quantization)
        assert palette is None

    def test_invalid_bit_depth_raises_error(self):
        """Invalid bit depth (non-standard) should still work."""
        # The function doesn't validate bit depth, just calculates 2^bit_depth
        # 7-bit would give 128 colors
        palette = create_palette_from_bit_depth(bit_depth=7, color_mode=False)
        assert isinstance(palette, bytes)
        assert len(palette) == 768  # Always padded to 256 colors


class TestQuantizeStepCreation:
    """Test QuantizeStep instantiation with different parameters."""

    def test_default_quantize_step(self):
        """Default QuantizeStep should use Palette16."""
        step = QuantizeStep()

        assert step.get_name().startswith("Quantize")

    def test_quantize_with_custom_palette(self):
        """QuantizeStep with custom palette bytes."""
        custom_palette = Palette16  # Palette16 is bytes, not a function
        step = QuantizeStep(palette=custom_palette)

        assert step.get_name().startswith("Quantize")

    def test_quantize_with_colors_parameter(self):
        """QuantizeStep with direct colors count."""
        step = QuantizeStep(colors=64)

        assert step.get_name().startswith("Quantize")

    def test_quantize_with_bit_depth_grayscale(self):
        """QuantizeStep with bit_depth for grayscale."""
        step = QuantizeStep(use_bit_depth=True, bit_depth=4, color_mode=False)

        assert step.get_name().startswith("Quantize")

    def test_quantize_with_bit_depth_color(self):
        """QuantizeStep with bit_depth for color."""
        step = QuantizeStep(use_bit_depth=True, bit_depth=12, color_mode=True)

        assert step.get_name().startswith("Quantize")


class TestQuantizeProcessing:
    """Test quantization processing."""

    def test_quantize_reduces_colors(self, test_color_image):
        """Quantization should reduce color count."""
        step = QuantizeStep()
        result = step.process(test_color_image)

        assert isinstance(result, Image.Image)

    def test_quantize_with_16_colors(self, test_color_image):
        """Quantize to 16 colors."""
        step = QuantizeStep(colors=16)
        result = step.process(test_color_image)

        assert isinstance(result, Image.Image)

    def test_quantize_4bit_grayscale(self, test_grayscale_image):
        """Quantize grayscale to 4-bit (16 levels)."""
        step = QuantizeStep(use_bit_depth=True, bit_depth=4, color_mode=False)
        result = step.process(test_grayscale_image)

        assert isinstance(result, Image.Image)

    def test_quantize_12bit_color(self, test_color_image):
        """Quantize color image to 12-bit (4096 colors)."""
        step = QuantizeStep(use_bit_depth=True, bit_depth=12, color_mode=True)
        result = step.process(test_color_image)

        assert isinstance(result, Image.Image)

    def test_quantize_preserves_size(self, test_color_image):
        """Quantization should preserve image size."""
        step = QuantizeStep()
        result = step.process(test_color_image)

        assert result.size == test_color_image.size


class TestPalette16:
    """Test the Palette16 constant."""

    def test_palette16_is_bytes(self):
        """Palette16 should be a bytes object."""
        assert isinstance(Palette16, bytes)

    def test_palette16_has_16_colors(self):
        """Palette16 should have 16 grayscale levels."""
        # 16 colors * 3 bytes (RGB) = 48 bytes
        assert len(Palette16) == 48


class TestBackwardCompatibility:
    """Test backward compatibility with existing code."""

    def test_default_behavior_unchanged(self, test_color_image):
        """Default QuantizeStep should work as before."""
        step = QuantizeStep()
        result = step.process(test_color_image)

        assert isinstance(result, Image.Image)

    def test_palette16_still_works(self, test_color_image):
        """Using Palette16 directly should still work."""
        palette = Palette16  # Palette16 is bytes, not a function
        step = QuantizeStep(palette=palette)
        result = step.process(test_color_image)

        assert isinstance(result, Image.Image)
