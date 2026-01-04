"""
Unit tests for manga-specific image processing steps.

This module tests the functionality of SmartCropStep, AutoRotateStep,
and TextEnhanceStep to ensure they work correctly for manga processing.
"""

import pytest
from PIL import Image, ImageDraw
from image_pipeline.crop import SmartCropStep
from image_pipeline.rotation import AutoRotateStep
from image_pipeline.text_enhance import (
    TextEnhanceStep,
    AdaptiveTextEnhanceStep,
)


class TestSmartCropStep:
    """Tests for SmartCropStep margin detection and cropping."""

    def test_init_default_params(self):
        """Test SmartCropStep initialization with default parameters."""
        step = SmartCropStep()
        assert step.threshold == 250
        assert step.min_margin == 10
        assert step.enabled is True
        assert step.get_name() == "SmartCrop"

    def test_init_custom_params(self):
        """Test SmartCropStep initialization with custom parameters."""
        step = SmartCropStep(threshold=240, min_margin=15, enabled=False)
        assert step.threshold == 240
        assert step.min_margin == 15
        assert step.enabled is False
        assert step.get_name() == "SmartCrop(disabled)"

    def test_crop_image_with_white_margins(self):
        """Test that white margins are detected and removed."""
        # Create image with white margins
        img = Image.new("RGB", (200, 200), "white")
        # Add black content in center
        draw = ImageDraw.Draw(img)
        draw.rectangle([50, 50, 150, 150], fill="black")

        step = SmartCropStep(threshold=250, min_margin=10)
        result = step.process(img)

        # Should crop to content + min_margin
        assert result.size[0] < img.size[0]
        assert result.size[1] < img.size[1]
        # Should preserve min_margin around content
        assert result.size[0] >= 100 + 2 * 10  # content + 2*margin
        assert result.size[1] >= 100 + 2 * 10

    def test_no_crop_on_full_content(self):
        """Test that images without margins are not cropped."""
        # Create image with content edge-to-edge
        img = Image.new("RGB", (100, 100), "gray")

        step = SmartCropStep(threshold=250, min_margin=10)
        result = step.process(img)

        # Should not crop (no white margins detected)
        assert result.size == img.size

    def test_disabled_step_returns_original(self):
        """Test that disabled step returns image unchanged."""
        img = Image.new("RGB", (200, 200), "white")
        draw = ImageDraw.Draw(img)
        draw.rectangle([50, 50, 150, 150], fill="black")

        step = SmartCropStep(enabled=False)
        result = step.process(img)

        assert result.size == img.size

    def test_crop_preserves_image_mode(self):
        """Test that cropping preserves image mode (RGB, L, etc.)."""
        for mode in ["RGB", "L", "RGBA"]:
            img = Image.new(mode, (200, 200), "white")
            draw = ImageDraw.Draw(img)
            if mode == "RGBA":
                draw.rectangle([50, 50, 150, 150], fill=(0, 0, 0, 255))
            else:
                draw.rectangle([50, 50, 150, 150], fill="black")

            step = SmartCropStep()
            result = step.process(img)

            assert result.mode == mode


class TestAutoRotateStep:
    """Tests for AutoRotateStep rotation detection and correction."""

    def test_init_default_params(self):
        """Test AutoRotateStep initialization with default parameters."""
        step = AutoRotateStep()
        assert step.max_angle == 5.0
        assert step.threshold == 0.5
        assert step.enabled is True
        assert step.fill_color == "white"

    def test_init_custom_params(self):
        """Test AutoRotateStep initialization with custom parameters."""
        step = AutoRotateStep(
            max_angle=10.0, threshold=1.0, enabled=False, fill_color="black"
        )
        assert step.max_angle == 10.0
        assert step.threshold == 1.0
        assert step.enabled is False
        assert step.fill_color == "black"
        assert step.get_name() == "AutoRotate(disabled)"

    def test_no_rotation_on_straight_image(self):
        """Test that straight images are not rotated."""
        # Create straight image with horizontal lines
        img = Image.new("RGB", (200, 200), "white")
        draw = ImageDraw.Draw(img)
        for y in range(50, 150, 20):
            draw.line([(20, y), (180, y)], fill="black", width=2)

        step = AutoRotateStep()
        result = step.process(img)

        # Image should not be rotated (size unchanged)
        assert result.size == img.size

    def test_disabled_step_returns_original(self):
        """Test that disabled step returns image unchanged."""
        img = Image.new("RGB", (200, 200), "white")

        step = AutoRotateStep(enabled=False)
        result = step.process(img)

        assert result is img or result.size == img.size

    def test_rotation_preserves_image_mode(self):
        """Test that rotation preserves image mode."""
        for mode in ["RGB", "L", "RGBA"]:
            img = Image.new(mode, (200, 200), "white")

            step = AutoRotateStep()
            result = step.process(img)

            assert result.mode == mode

    def test_get_name_shows_detection_method(self):
        """Test that get_name indicates which detection method is available."""
        step = AutoRotateStep()
        name = step.get_name()

        # Should indicate opencv or basic
        assert "opencv" in name or "basic" in name


class TestTextEnhanceStep:
    """Tests for TextEnhanceStep text enhancement."""

    def test_init_default_params(self):
        """Test TextEnhanceStep initialization with default parameters."""
        step = TextEnhanceStep()
        assert step.text_sharpen == 1.5
        assert step.edge_enhance == 0.3
        assert step.enabled is True
        assert step.get_name() == "TextEnhance(s=1.5)"

    def test_init_custom_params(self):
        """Test TextEnhanceStep initialization with custom parameters."""
        step = TextEnhanceStep(text_sharpen=2.0, edge_enhance=0.5, enabled=False)
        assert step.text_sharpen == 2.0
        assert step.edge_enhance == 0.5
        assert step.enabled is False
        assert step.get_name() == "TextEnhance(disabled)"

    def test_edge_enhance_clamped_to_range(self):
        """Test that edge_enhance is clamped to 0-1 range."""
        step1 = TextEnhanceStep(edge_enhance=-0.5)
        assert step1.edge_enhance == 0.0

        step2 = TextEnhanceStep(edge_enhance=1.5)
        assert step2.edge_enhance == 1.0

    def test_text_enhancement_applied(self):
        """Test that text enhancement is applied to image."""
        # Create image with text-like content
        img = Image.new("RGB", (200, 200), "white")
        draw = ImageDraw.Draw(img)
        # Simulate text with thin lines
        for x in range(50, 150, 10):
            draw.line([(x, 50), (x, 150)], fill="black", width=1)

        step = TextEnhanceStep(text_sharpen=1.5, edge_enhance=0.3)
        result = step.process(img)

        # Should return processed image with same dimensions
        assert result.size == img.size
        assert isinstance(result, Image.Image)

    def test_disabled_step_returns_original(self):
        """Test that disabled step returns image unchanged."""
        img = Image.new("RGB", (200, 200), "white")

        step = TextEnhanceStep(enabled=False)
        result = step.process(img)

        # Should be identical or very similar
        assert result.size == img.size

    def test_no_enhancement_when_factors_are_default(self):
        """Test that no enhancement occurs when factors are at default values."""
        img = Image.new("RGB", (200, 200), "gray")

        # text_sharpen=1.0, edge_enhance=0.0 should do nothing
        step = TextEnhanceStep(text_sharpen=1.0, edge_enhance=0.0)
        result = step.process(img)

        assert result.size == img.size

    def test_enhancement_preserves_image_mode(self):
        """Test that enhancement preserves image mode."""
        for mode in ["RGB", "L", "RGBA"]:
            img = Image.new(mode, (200, 200), "gray")

            step = TextEnhanceStep()
            result = step.process(img)

            assert result.mode == mode


class TestAdaptiveTextEnhanceStep:
    """Tests for AdaptiveTextEnhanceStep advanced text enhancement."""

    def test_init_default_params(self):
        """Test AdaptiveTextEnhanceStep initialization with default parameters."""
        step = AdaptiveTextEnhanceStep()
        assert step.text_sharpen == 1.6
        assert step.detail_enhance == 1.3
        assert step.enabled is True

    def test_init_custom_params(self):
        """Test AdaptiveTextEnhanceStep initialization with custom parameters."""
        step = AdaptiveTextEnhanceStep(
            text_sharpen=2.0, detail_enhance=1.5, enabled=False
        )
        assert step.text_sharpen == 2.0
        assert step.detail_enhance == 1.5
        assert step.enabled is False

    def test_adaptive_enhancement_applied(self):
        """Test that adaptive enhancement is applied to image."""
        img = Image.new("RGB", (200, 200), "white")
        draw = ImageDraw.Draw(img)
        draw.text((50, 50), "Manga Text", fill="black")

        step = AdaptiveTextEnhanceStep(text_sharpen=1.6, detail_enhance=1.3)
        result = step.process(img)

        assert result.size == img.size
        assert isinstance(result, Image.Image)

    def test_disabled_step_returns_original(self):
        """Test that disabled step returns image unchanged."""
        img = Image.new("RGB", (200, 200), "white")

        step = AdaptiveTextEnhanceStep(enabled=False)
        result = step.process(img)

        assert result.size == img.size

    def test_get_name(self):
        """Test get_name returns correct format."""
        step = AdaptiveTextEnhanceStep(text_sharpen=1.8)
        assert step.get_name() == "AdaptiveTextEnhance(s=1.8)"

        step_disabled = AdaptiveTextEnhanceStep(enabled=False)
        assert step_disabled.get_name() == "AdaptiveTextEnhance(disabled)"


class TestMangaStepsIntegration:
    """Integration tests for manga-specific steps working together."""

    def test_steps_can_be_chained(self):
        """Test that manga steps can be chained in a pipeline."""
        from image_pipeline.pipeline import ImagePipeline

        # Create test image
        img = Image.new("RGB", (300, 300), "white")
        draw = ImageDraw.Draw(img)
        # Add content in center with margins
        draw.rectangle([80, 80, 220, 220], fill="black")

        # Create pipeline with all manga steps
        pipeline = ImagePipeline()
        pipeline.add_step(SmartCropStep(threshold=245, min_margin=10))
        pipeline.add_step(AutoRotateStep(max_angle=5.0))
        pipeline.add_step(TextEnhanceStep(text_sharpen=1.5))

        result = pipeline.process(img)

        # Should successfully process through all steps
        assert isinstance(result, Image.Image)
        # Should be cropped (smaller than original)
        assert result.size[0] <= img.size[0]
        assert result.size[1] <= img.size[1]

    def test_scanned_manga_preset(self):
        """Test the scanned_manga preset pipeline."""
        from image_pipeline.presets import PipelinePresets

        pipeline = PipelinePresets.scanned_manga()

        # Should have all expected steps
        step_names = pipeline.get_steps()
        assert "AutoRotate" in str(step_names)
        assert "SmartCrop" in str(step_names)
        assert "TextEnhance" in str(step_names)
        assert "Contrast" in str(step_names)
        assert "Sharpen" in str(step_names)
        assert "Quantize" in str(step_names)

        # Should have 6 steps total
        assert len(pipeline) == 6

    def test_scanned_manga_advanced_preset(self):
        """Test the scanned_manga_advanced preset pipeline."""
        from image_pipeline.presets import PipelinePresets

        pipeline = PipelinePresets.scanned_manga_advanced()

        # Should have all expected steps
        step_names = pipeline.get_steps()
        assert "AutoRotate" in str(step_names)
        assert "SmartCrop" in str(step_names)
        assert "AdaptiveTextEnhance" in str(step_names)
        assert "Contrast" in str(step_names)
        assert "Sharpen" in str(step_names)
        assert "Quantize" in str(step_names)

        # Should have 6 steps total
        assert len(pipeline) == 6

    def test_manga_presets_available(self):
        """Test that manga presets are available in list."""
        from image_pipeline.presets import PipelinePresets

        presets = PipelinePresets.list_presets()

        assert "scanned_manga" in presets
        assert "scanned_manga_advanced" in presets

    def test_get_manga_preset_by_name(self):
        """Test getting manga presets by name."""
        from image_pipeline.presets import PipelinePresets
        from image_pipeline.pipeline import ImagePipeline

        pipeline1 = PipelinePresets.get_preset("scanned_manga")
        assert isinstance(pipeline1, ImagePipeline)
        assert len(pipeline1) == 6

        pipeline2 = PipelinePresets.get_preset("scanned_manga_advanced")
        assert isinstance(pipeline2, ImagePipeline)
        assert len(pipeline2) == 6
