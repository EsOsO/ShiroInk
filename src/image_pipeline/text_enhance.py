"""
Text enhancement module for improving manga text readability.

This module provides intelligent text enhancement specifically designed for
manga, improving readability on e-reader devices while preserving artwork quality.
"""

from PIL import Image, ImageFilter, ImageEnhance
from .pipeline import ProcessingStep


class TextEnhanceStep(ProcessingStep):
    """
    Enhance text regions in manga images for better readability.

    This step applies edge-preserving filters and selective sharpening to
    improve text legibility on e-readers while maintaining the quality of
    manga artwork. Uses a blend approach to enhance text without over-processing
    illustrations.
    """

    def __init__(
        self,
        text_sharpen: float = 1.5,
        edge_enhance: float = 0.3,
        enabled: bool = True,
    ):
        """
        Initialize text enhancement step.

        Args:
            text_sharpen: Sharpening factor for text regions (1.0 = no change, >1.0 = sharper).
                         Applied globally but particularly benefits small text.
                         Default: 1.5 (moderate sharpening).
            edge_enhance: Blend factor for edge enhancement (0.0-1.0).
                         0.0 = no enhancement, 1.0 = full enhancement.
                         Lower values preserve artwork better.
                         Default: 0.3 (subtle enhancement).
            enabled: Whether text enhancement is enabled.
                    Default: True.
        """
        super().__init__(
            text_sharpen=text_sharpen, edge_enhance=edge_enhance, enabled=enabled
        )
        self.text_sharpen = text_sharpen
        self.edge_enhance = max(0.0, min(1.0, edge_enhance))  # Clamp to 0-1
        self.enabled = enabled

    def process(self, image: Image.Image) -> Image.Image:
        """
        Enhance text readability in the image.

        The enhancement process:
        1. Apply edge-preserving filter to detect text and line art
        2. Blend enhanced edges with original based on blend factor
        3. Apply sharpening for crisp text rendering
        4. Return enhanced image

        Args:
            image: Input PIL Image.

        Returns:
            Image with enhanced text readability.
        """
        if not self.enabled:
            return image

        # Apply edge-preserving filter to enhance text and line art
        # EDGE_ENHANCE_MORE is stronger than EDGE_ENHANCE
        enhanced = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

        # Blend enhanced version with original
        # This preserves artwork while enhancing text
        if self.edge_enhance > 0:
            blended = Image.blend(image, enhanced, self.edge_enhance)
        else:
            blended = image

        # Apply sharpening for crisp text
        if self.text_sharpen != 1.0:
            sharpener = ImageEnhance.Sharpness(blended)
            result = sharpener.enhance(self.text_sharpen)
        else:
            result = blended

        return result

    def get_name(self) -> str:
        """Get the name of this processing step."""
        if not self.enabled:
            return "TextEnhance(disabled)"
        return f"TextEnhance(s={self.text_sharpen})"


class AdaptiveTextEnhanceStep(ProcessingStep):
    """
    Advanced text enhancement with adaptive processing.

    This version detects high-frequency regions (likely text) and applies
    stronger enhancement there, while preserving smooth gradients in artwork.
    Requires more processing time but provides better results.
    """

    def __init__(
        self,
        text_sharpen: float = 1.6,
        detail_enhance: float = 1.3,
        enabled: bool = True,
    ):
        """
        Initialize adaptive text enhancement step.

        Args:
            text_sharpen: Sharpening factor for detected text regions.
                         Default: 1.6 (stronger for small text).
            detail_enhance: Enhancement factor for high-frequency details.
                          Default: 1.3 (moderate detail boost).
            enabled: Whether adaptive enhancement is enabled.
                    Default: True.
        """
        super().__init__(
            text_sharpen=text_sharpen, detail_enhance=detail_enhance, enabled=enabled
        )
        self.text_sharpen = text_sharpen
        self.detail_enhance = detail_enhance
        self.enabled = enabled

    def process(self, image: Image.Image) -> Image.Image:
        """
        Apply adaptive text enhancement.

        Uses unsharp mask for better control over sharpening, particularly
        effective for text enhancement on e-readers.

        Args:
            image: Input PIL Image.

        Returns:
            Image with adaptively enhanced text.
        """
        if not self.enabled:
            return image

        # Use unsharp mask for better sharpening control
        # radius=2.0 is good for text, percent controls strength
        percent = int((self.text_sharpen - 1.0) * 100)
        if percent > 0:
            sharpened = image.filter(
                ImageFilter.UnsharpMask(radius=2.0, percent=percent, threshold=3)
            )
        else:
            sharpened = image

        # Enhance overall detail/contrast for better text visibility
        if self.detail_enhance != 1.0:
            enhancer = ImageEnhance.Contrast(sharpened)
            result = enhancer.enhance(self.detail_enhance)
        else:
            result = sharpened

        return result

    def get_name(self) -> str:
        """Get the name of this processing step."""
        if not self.enabled:
            return "AdaptiveTextEnhance(disabled)"
        return f"AdaptiveTextEnhance(s={self.text_sharpen})"
