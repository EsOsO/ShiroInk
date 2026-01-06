"""
Predefined pipeline configurations for different devices and use cases.

Pipeline Step Ordering:
=====================
PRE-RESIZE: AutoRotate, SmartCrop, TextEnhance
RESIZE: (auto-inserted)
POST-RESIZE: ColorProfile, Contrast, Sharpen, Quantize
"""

from .pipeline import ImagePipeline
from .contrast import ContrastStep
from .sharpen import SharpenStep
from .quantize import QuantizeStep, Palette16
from .color_profile import ColorProfileStep
from .crop import SmartCropStep
from .rotation import AutoRotateStep
from .text_enhance import TextEnhanceStep, AdaptiveTextEnhanceStep
from .enums import DisplayType
from .devices import DeviceSpec


def _build_pipeline(
    rotate: bool = True,
    crop: bool = True,
    text_sharpen: float | None = None,
    color_profile: bool = False,
    contrast: float | None = None,
    sharpen: float | None = None,
    quantize: bool = False,
) -> ImagePipeline:
    """Build a pipeline with the specified steps."""
    pipeline = ImagePipeline()
    if rotate:
        pipeline.add_step(AutoRotateStep(max_angle=5.0, threshold=0.5))
    if crop:
        pipeline.add_step(SmartCropStep(threshold=245, min_margin=10))
    if text_sharpen:
        pipeline.add_step(
            TextEnhanceStep(text_sharpen=text_sharpen, edge_enhance=text_sharpen * 0.2)
        )
    if color_profile:
        pipeline.add_step(
            ColorProfileStep(color_support=True, target_gamut=None, bit_depth=24)
        )
    if contrast:
        pipeline.add_step(ContrastStep(factor=contrast))
    if sharpen:
        pipeline.add_step(SharpenStep(factor=sharpen))
    if quantize:
        pipeline.add_step(QuantizeStep(palette=Palette16))
    return pipeline


class PipelinePresets:
    """Factory class for creating predefined image processing pipelines."""

    @staticmethod
    def kindle() -> ImagePipeline:
        """Pipeline optimized for Kindle e-readers (B&W e-ink)."""
        return _build_pipeline(
            text_sharpen=1.5,
            contrast=1.5,
            sharpen=1.2,
            quantize=True,
        )

    @staticmethod
    def tablet() -> ImagePipeline:
        """Pipeline optimized for color tablets (LCD displays)."""
        return _build_pipeline(
            text_sharpen=1.3,
            contrast=1.3,
            sharpen=1.1,
        )

    @staticmethod
    def print_() -> ImagePipeline:
        """Pipeline optimized for printing (minimal processing)."""
        pipeline = ImagePipeline()
        pipeline.add_step(SharpenStep(factor=1.05))
        return pipeline

    @staticmethod
    def print() -> ImagePipeline:
        """Pipeline optimized for printing (minimal processing)."""
        return PipelinePresets.print_()

    @staticmethod
    def high_quality() -> ImagePipeline:
        """Pipeline for high-quality displays."""
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep(factor=1.2))
        pipeline.add_step(SharpenStep(factor=1.4))
        return pipeline

    @staticmethod
    def minimal() -> ImagePipeline:
        """Minimal pipeline with no processing steps."""
        return ImagePipeline()

    @staticmethod
    def custom(
        contrast: float | None = None,
        sharpen: float | None = None,
        quantize: bool = False,
    ) -> ImagePipeline:
        """Create a custom pipeline with specified parameters."""
        pipeline = ImagePipeline()
        if contrast:
            pipeline.add_step(ContrastStep(factor=contrast))
        if sharpen:
            pipeline.add_step(SharpenStep(factor=sharpen))
        if quantize:
            pipeline.add_step(QuantizeStep(palette=Palette16))
        return pipeline

    @staticmethod
    def eink() -> ImagePipeline:
        """Generic pipeline for e-ink displays (B&W)."""
        return PipelinePresets.kindle()

    @staticmethod
    def ipad() -> ImagePipeline:
        """Pipeline optimized for iPad and Retina displays."""
        return _build_pipeline(
            text_sharpen=1.4,
            contrast=1.2,
            sharpen=1.4,
        )

    @staticmethod
    def kobo() -> ImagePipeline:
        """Pipeline optimized for Kobo e-readers (B&W e-ink)."""
        return PipelinePresets.kindle()

    @staticmethod
    def tolino() -> ImagePipeline:
        """Pipeline optimized for Tolino e-readers (B&W e-ink)."""
        return PipelinePresets.kindle()

    @staticmethod
    def pocketbook() -> ImagePipeline:
        """Pipeline optimized for PocketBook e-readers (B&W e-ink)."""
        return PipelinePresets.kindle()

    @staticmethod
    def pocketbook_color() -> ImagePipeline:
        """Pipeline optimized for PocketBook color e-readers."""
        return PipelinePresets.tablet()

    @staticmethod
    def scanned_manga() -> ImagePipeline:
        """Pipeline optimized for scanned manga (B&W e-ink)."""
        return PipelinePresets.kindle()

    @staticmethod
    def scanned_manga_advanced() -> ImagePipeline:
        """Advanced pipeline for high-quality scanned manga."""
        pipeline = ImagePipeline()
        pipeline.add_step(AutoRotateStep(max_angle=5.0, threshold=0.5))
        pipeline.add_step(SmartCropStep(threshold=240, min_margin=8))
        pipeline.add_step(AdaptiveTextEnhanceStep(text_sharpen=1.6, detail_enhance=1.3))
        pipeline.add_step(ContrastStep(factor=1.6))
        pipeline.add_step(SharpenStep(factor=1.3))
        pipeline.add_step(QuantizeStep(palette=Palette16))
        return pipeline

    @classmethod
    def from_device_spec(cls, device: DeviceSpec) -> ImagePipeline:
        """
        Create a pipeline based on device specifications.

        Args:
            device: Device specification object containing display characteristics.

        Returns:
            ImagePipeline configured for the device.
        """
        if device.display_type == DisplayType.EINK:
            if device.color_support:
                return _build_pipeline(
                    text_sharpen=1.3,
                    color_profile=True,
                    contrast=1.3,
                    sharpen=1.1,
                    quantize=device.bit_depth < 16,
                )
            else:
                return _build_pipeline(
                    text_sharpen=1.5,
                    color_profile=True,
                    contrast=1.6,
                    sharpen=1.3,
                    quantize=device.bit_depth < 16,
                )
        else:
            return _build_pipeline(
                text_sharpen=1.4,
                color_profile=True,
                contrast=1.2,
                sharpen=1.4,
            )

    @classmethod
    def get_preset(cls, name: str) -> ImagePipeline:
        """
        Get a preset pipeline by name.

        Args:
            name: Name of the preset (kindle, kobo, tolino, pocketbook,
                  pocketbook_color, ipad, eink, tablet, print, high_quality,
                  minimal, scanned_manga, scanned_manga_advanced).

        Returns:
            ImagePipeline for the specified preset.

        Raises:
            ValueError: If preset name is not recognized.
        """
        preset_map = {
            "kindle": cls.kindle,
            "tablet": cls.tablet,
            "print": cls.print_,
            "high_quality": cls.high_quality,
            "minimal": cls.minimal,
            "eink": cls.eink,
            "ipad": cls.ipad,
            "scanned_manga": cls.scanned_manga,
            "scanned_manga_advanced": cls.scanned_manga_advanced,
            "kobo": cls.kobo,
            "tolino": cls.tolino,
            "pocketbook": cls.pocketbook,
            "pocketbook_color": cls.pocketbook_color,
        }

        name_lower = name.lower()
        if name_lower not in preset_map:
            available = ", ".join(sorted(preset_map.keys()))
            raise ValueError(f"Unknown preset '{name}'. Available: {available}")

        return preset_map[name_lower]()

    @classmethod
    def list_presets(cls) -> list[str]:
        """Get a list of available preset names."""
        return [
            "kindle",
            "tablet",
            "print",
            "high_quality",
            "minimal",
            "eink",
            "ipad",
            "scanned_manga",
            "scanned_manga_advanced",
            "kobo",
            "tolino",
            "pocketbook",
            "pocketbook_color",
        ]
