"""
Predefined pipeline configurations for different devices and use cases.
"""

from .pipeline import ImagePipeline
from .contrast import ContrastStep
from .sharpen import SharpenStep
from .quantize import QuantizeStep, Palette16


class PipelinePresets:
    """Factory class for creating predefined image processing pipelines."""

    @staticmethod
    def kindle() -> ImagePipeline:
        """
        Create a pipeline optimized for Kindle e-readers.

        Features:
        - High contrast for e-ink displays
        - Moderate sharpening
        - 16-color quantization for file size reduction

        Returns:
            ImagePipeline configured for Kindle devices.
        """
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep(factor=1.5))
        pipeline.add_step(SharpenStep(factor=1.2))
        pipeline.add_step(QuantizeStep(palette=Palette16))
        return pipeline

    @staticmethod
    def tablet() -> ImagePipeline:
        """
        Create a pipeline optimized for color tablets.

        Features:
        - Moderate contrast
        - Light sharpening
        - No quantization (preserves color)

        Returns:
            ImagePipeline configured for tablet devices.
        """
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep(factor=1.3))
        pipeline.add_step(SharpenStep(factor=1.1))
        return pipeline

    @staticmethod
    def print() -> ImagePipeline:
        """
        Create a pipeline optimized for printing.

        Features:
        - Minimal processing
        - Light sharpening only

        Returns:
            ImagePipeline configured for print output.
        """
        pipeline = ImagePipeline()
        pipeline.add_step(SharpenStep(factor=1.05))
        return pipeline

    @staticmethod
    def high_quality() -> ImagePipeline:
        """
        Create a pipeline for high-quality displays.

        Features:
        - Light contrast adjustment
        - Enhanced sharpening
        - No quantization

        Returns:
            ImagePipeline configured for high-quality displays.
        """
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep(factor=1.2))
        pipeline.add_step(SharpenStep(factor=1.4))
        return pipeline

    @staticmethod
    def minimal() -> ImagePipeline:
        """
        Create a minimal pipeline with no processing steps.

        Returns:
            Empty ImagePipeline.
        """
        return ImagePipeline()

    @staticmethod
    def custom(
        contrast: float | None = None,
        sharpen: float | None = None,
        quantize: bool = False,
    ) -> ImagePipeline:
        """
        Create a custom pipeline with specified parameters.

        Args:
            contrast: Contrast factor (None to skip).
            sharpen: Sharpening factor (None to skip).
            quantize: Whether to apply 16-color quantization.

        Returns:
            ImagePipeline with custom configuration.
        """
        pipeline = ImagePipeline()

        if contrast is not None:
            pipeline.add_step(ContrastStep(factor=contrast))

        if sharpen is not None:
            pipeline.add_step(SharpenStep(factor=sharpen))

        if quantize:
            pipeline.add_step(QuantizeStep(palette=Palette16))

        return pipeline

    @staticmethod
    def get_preset(name: str) -> ImagePipeline:
        """
        Get a preset pipeline by name.

        Args:
            name: Name of the preset (kindle, tablet, print, high_quality, minimal).

        Returns:
            ImagePipeline for the specified preset.

        Raises:
            ValueError: If preset name is not recognized.
        """
        presets = {
            "kindle": PipelinePresets.kindle,
            "tablet": PipelinePresets.tablet,
            "print": PipelinePresets.print,
            "high_quality": PipelinePresets.high_quality,
            "minimal": PipelinePresets.minimal,
        }

        if name.lower() not in presets:
            available = ", ".join(presets.keys())
            raise ValueError(f"Unknown preset '{name}'. Available presets: {available}")

        return presets[name.lower()]()

    @staticmethod
    def list_presets() -> list[str]:
        """
        Get a list of available preset names.

        Returns:
            List of preset names.
        """
        return ["kindle", "tablet", "print", "high_quality", "minimal"]
