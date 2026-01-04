"""
Predefined pipeline configurations for different devices and use cases.
"""

from .pipeline import ImagePipeline
from .contrast import ContrastStep
from .sharpen import SharpenStep
from .quantize import QuantizeStep, Palette16
from .color_profile import ColorProfileStep
from .devices import DeviceSpecs, DeviceSpec, DisplayType, ColorGamut


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
            name: Name of the preset (kindle, kobo, tolino, pocketbook, pocketbook_color,
                  ipad, eink, tablet, print, high_quality, minimal).

        Returns:
            ImagePipeline for the specified preset.

        Raises:
            ValueError: If preset name is not recognized.
        """
        presets = {
            # Generic presets
            "kindle": PipelinePresets.kindle,
            "tablet": PipelinePresets.tablet,
            "print": PipelinePresets.print,
            "high_quality": PipelinePresets.high_quality,
            "minimal": PipelinePresets.minimal,
            # Device-specific presets
            "kobo": PipelinePresets.kobo,
            "tolino": PipelinePresets.tolino,
            "pocketbook": PipelinePresets.pocketbook,
            "pocketbook_color": PipelinePresets.pocketbook_color,
            "ipad": PipelinePresets.ipad,
            "eink": PipelinePresets.eink,
        }

        if name.lower() not in presets:
            available = ", ".join(sorted(presets.keys()))
            raise ValueError(f"Unknown preset '{name}'. Available presets: {available}")

        return presets[name.lower()]()

    @staticmethod
    def list_presets() -> list[str]:
        """
        Get a list of available preset names.

        Returns:
            List of preset names.
        """
        return [
            # Generic presets
            "kindle",
            "tablet",
            "print",
            "high_quality",
            "minimal",
            # Device-specific presets
            "kobo",
            "tolino",
            "pocketbook",
            "pocketbook_color",
            "ipad",
            "eink",
        ]

    # Device-specific presets with optimized pipelines for e-ink and LCD displays

    @staticmethod
    def kobo() -> ImagePipeline:
        """
        Create a pipeline optimized for Kobo e-readers.

        Features:
        - High contrast for e-ink displays
        - Strong sharpening (Kobo benefits from sharper images)
        - 16-color quantization for file size reduction

        Returns:
            ImagePipeline configured for Kobo devices.
        """
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep(factor=1.6))
        pipeline.add_step(SharpenStep(factor=1.3))
        pipeline.add_step(QuantizeStep(palette=Palette16))
        return pipeline

    @staticmethod
    def tolino() -> ImagePipeline:
        """
        Create a pipeline optimized for Tolino e-readers.

        Features:
        - High contrast for e-ink displays
        - Moderate sharpening
        - 16-color quantization for file size reduction

        Returns:
            ImagePipeline configured for Tolino devices.
        """
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep(factor=1.5))
        pipeline.add_step(SharpenStep(factor=1.2))
        pipeline.add_step(QuantizeStep(palette=Palette16))
        return pipeline

    @staticmethod
    def pocketbook() -> ImagePipeline:
        """
        Create a pipeline optimized for PocketBook e-readers.

        Features:
        - High contrast for e-ink displays
        - Moderate sharpening
        - 16-color quantization for file size reduction
        - Works well with both regular and color e-ink displays

        Returns:
            ImagePipeline configured for PocketBook devices.
        """
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep(factor=1.5))
        pipeline.add_step(SharpenStep(factor=1.2))
        pipeline.add_step(QuantizeStep(palette=Palette16))
        return pipeline

    @staticmethod
    def from_device_spec(device_spec: DeviceSpec) -> ImagePipeline:
        """
        Create an optimized pipeline based on complete device specifications.

        This factory method uses the device's full specifications including:
        - Color support (B&W vs Color)
        - Color gamut (sRGB, DCI-P3, etc.)
        - Bit depth (4-bit, 8-bit, 24-bit)
        - Display type (e-ink, LCD, OLED, Retina)

        Args:
            device_spec: Complete device specification

        Returns:
            Optimized ImagePipeline for the device
        """
        pipeline = ImagePipeline()

        # Step 1: Color Profile Conversion
        # Always add this first to handle color space conversion and B&W optimization
        pipeline.add_step(
            ColorProfileStep(
                color_support=device_spec.color_support,
                target_gamut=device_spec.color_gamut,
                bit_depth=device_spec.bit_depth,
            )
        )

        # Step 2: Contrast Adjustment
        # E-ink displays need more contrast than LCD/OLED
        if device_spec.display_type == DisplayType.EINK:
            if device_spec.color_support:
                # Color e-ink needs gentler contrast
                contrast_factor = 1.3
            else:
                # B&W e-ink benefits from high contrast
                contrast_factor = 1.6
        else:
            # LCD/OLED have good native contrast
            contrast_factor = 1.2

        pipeline.add_step(ContrastStep(factor=contrast_factor))

        # Step 3: Sharpening
        # E-ink and high-PPI displays benefit from different sharpening
        if device_spec.display_type == DisplayType.EINK:
            # E-ink benefits from stronger sharpening
            if device_spec.ppi >= 300:
                sharpen_factor = 1.3
            else:
                sharpen_factor = 1.2
        else:
            # High-res LCD/OLED displays
            if device_spec.ppi >= 300:
                sharpen_factor = 1.4
            else:
                sharpen_factor = 1.3

        pipeline.add_step(SharpenStep(factor=sharpen_factor))

        # Step 4: Quantization (only for limited color devices)
        # Full color devices (24-bit) don't need quantization
        if device_spec.bit_depth < 16:
            if device_spec.color_support:
                # Color e-ink with limited palette
                pipeline.add_step(
                    QuantizeStep(colors=device_spec.max_colors, color_mode=True)
                )
            else:
                # B&W devices - use bit depth specific palette
                pipeline.add_step(
                    QuantizeStep(
                        use_bit_depth=True,
                        bit_depth=device_spec.bit_depth,
                        color_mode=False,
                    )
                )

        return pipeline

    @staticmethod
    def pocketbook_color() -> ImagePipeline:
        """
        Create a pipeline optimized for PocketBook color e-ink devices.

        Features:
        - Moderate contrast (color e-ink is more delicate)
        - Light sharpening
        - No quantization (preserves color)

        Returns:
            ImagePipeline configured for PocketBook color devices.
        """
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep(factor=1.3))
        pipeline.add_step(SharpenStep(factor=1.1))
        return pipeline

    @staticmethod
    def ipad() -> ImagePipeline:
        """
        Create a pipeline optimized for iPad and Retina displays.

        Features:
        - Light contrast for LCD/OLED displays
        - Enhanced sharpening for high-resolution displays
        - No quantization (preserves full color)

        Returns:
            ImagePipeline configured for iPad devices.
        """
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep(factor=1.2))
        pipeline.add_step(SharpenStep(factor=1.4))
        return pipeline

    @staticmethod
    def eink() -> ImagePipeline:
        """
        Create a generic pipeline optimized for e-ink displays.

        Features:
        - High contrast for e-ink clarity
        - Moderate sharpening
        - 16-color quantization for file size reduction

        Returns:
            ImagePipeline configured for generic e-ink devices.
        """
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep(factor=1.5))
        pipeline.add_step(SharpenStep(factor=1.2))
        pipeline.add_step(QuantizeStep(palette=Palette16))
        return pipeline
