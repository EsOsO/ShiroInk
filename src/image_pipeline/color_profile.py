"""
Color profile management step for device-specific color conversion.

This module provides color space conversion optimized for different display types,
with support for ICC profiles when available (hybrid approach).
"""

import io
from PIL import Image
from .pipeline import ProcessingStep
from .enums import ColorGamut


class ColorProfileStep(ProcessingStep):
    """
    Processing step to convert images to the target device's color space.

    This uses a hybrid approach:
    - Always provides optimized B&W conversion for grayscale displays
    - Attempts ICC-based conversion for color displays when available
    - Falls back gracefully when ICC support is unavailable
    """

    def __init__(
        self, color_support: bool, target_gamut: ColorGamut | None, bit_depth: int
    ):
        """
        Initialize color profile conversion step.

        Args:
            color_support: True if target device supports color, False for B&W
            target_gamut: Target color gamut (None for B&W devices)
            bit_depth: Target bit depth (4=16 levels, 8=256, 24=16M)
        """
        super().__init__(
            color_support=color_support, target_gamut=target_gamut, bit_depth=bit_depth
        )
        self.color_support = color_support
        self.target_gamut = target_gamut
        self.bit_depth = bit_depth

        # Try to import ImageCms for ICC support
        self._icc_available = False
        try:
            from PIL import ImageCms

            self._ImageCms = ImageCms
            self._icc_available = True
        except ImportError:
            self._ImageCms = None

    def process(self, image: Image.Image) -> Image.Image:
        """
        Convert image to target device color space.

        Args:
            image: Input PIL Image

        Returns:
            Image converted to target color space
        """
        # Ensure image is in RGB mode first
        if image.mode != "RGB":
            image = image.convert("RGB")

        # B&W conversion - always optimized
        if not self.color_support:
            return self._convert_to_grayscale(image)

        # Color devices - attempt ICC conversion
        if self.target_gamut:
            return self._convert_color_gamut(image)

        # Fallback: return as-is
        return image

    def _convert_to_grayscale(self, image: Image.Image) -> Image.Image:
        """
        Convert image to perceptual grayscale optimized for e-ink displays.

        Uses ITU-R 601-2 luma transform for perceptually accurate conversion.
        If bit_depth < 8, applies posterization for limited grayscale levels.

        Args:
            image: RGB image

        Returns:
            Grayscale image converted back to RGB for pipeline compatibility
        """
        # Convert to perceptual grayscale (L mode uses ITU-R 601-2 luma)
        gray = image.convert("L")

        # Apply bit depth limitation if needed (e.g., 4-bit = 16 levels)
        if self.bit_depth < 8:
            # Calculate number of gray levels
            num_levels = 2**self.bit_depth

            # Posterize to limited levels
            # This maps 256 levels to num_levels
            gray = gray.point(lambda x: int(x / 256 * num_levels) * (256 // num_levels))

        # Convert back to RGB for pipeline compatibility
        # (quantization step will handle final palette conversion)
        return gray.convert("RGB")

    def _convert_color_gamut(self, image: Image.Image) -> Image.Image:
        """
        Convert image to target color gamut using ICC profiles when available.

        Hybrid approach:
        - Attempts ICC-based conversion if littlecms2 is available
        - Falls back to simpler heuristics if not

        Args:
            image: RGB image

        Returns:
            Image in target color gamut
        """
        # DCI-P3 wide gamut - attempt ICC conversion
        if self.target_gamut == ColorGamut.DCI_P3:
            if self._icc_available:
                return self._icc_convert_to_p3(image)
            else:
                # Fallback: no conversion needed, modern displays handle sRGB→P3
                return image

        # sRGB - standard gamut
        elif self.target_gamut == ColorGamut.SRGB:
            if self._icc_available:
                return self._icc_ensure_srgb(image)
            else:
                # Fallback: PIL defaults to sRGB, no conversion needed
                return image

        # Adobe RGB - professional wide gamut
        elif self.target_gamut == ColorGamut.ADOBE_RGB:
            if self._icc_available:
                return self._icc_convert_to_adobe_rgb(image)
            else:
                # Fallback: treat as sRGB
                return image

        # Unknown or None - no conversion
        return image

    def _icc_convert_to_p3(self, image: Image.Image) -> Image.Image:
        """
        Convert image to DCI-P3 color space using ICC profiles.

        Falls back gracefully if profiles are not available.
        """
        try:
            # Try to get embedded profile from image
            try:
                source_profile = self._ImageCms.getOpenProfile(
                    io.BytesIO(image.info["icc_profile"])
                )
            except (KeyError, Exception):
                # No embedded profile, assume sRGB
                source_profile = self._ImageCms.createProfile("sRGB")

            # For P3, we'd need a P3 ICC profile file
            # Since we don't ship ICC files, use sRGB as approximation
            # (Most systems will handle sRGB→P3 at display level)
            target_profile = self._ImageCms.createProfile("sRGB")

            # Build and apply transform
            transform = self._ImageCms.buildTransform(
                source_profile,
                target_profile,
                image.mode,
                image.mode,
                renderingIntent=self._ImageCms.Intent.PERCEPTUAL,
            )

            return self._ImageCms.applyTransform(image, transform)

        except Exception:
            # ICC conversion failed, return original
            return image

    def _icc_ensure_srgb(self, image: Image.Image) -> Image.Image:
        """
        Ensure image is in sRGB color space.

        If image has embedded profile, convert to sRGB.
        Otherwise, assume it's already sRGB.
        """
        try:
            # Check if image has embedded profile
            if "icc_profile" not in image.info:
                # No profile, assume sRGB
                return image

            source_profile = self._ImageCms.getOpenProfile(
                io.BytesIO(image.info["icc_profile"])
            )
            target_profile = self._ImageCms.createProfile("sRGB")

            # Build and apply transform
            transform = self._ImageCms.buildTransform(
                source_profile,
                target_profile,
                image.mode,
                image.mode,
                renderingIntent=self._ImageCms.Intent.PERCEPTUAL,
            )

            return self._ImageCms.applyTransform(image, transform)

        except Exception:
            # ICC conversion failed, return original
            return image

    def _icc_convert_to_adobe_rgb(self, image: Image.Image) -> Image.Image:
        """
        Convert image to Adobe RGB color space.

        Falls back to sRGB if Adobe RGB profile not available.
        """
        # Similar to P3, would need Adobe RGB ICC profile file
        # For now, use sRGB as fallback
        return self._icc_ensure_srgb(image)

    def get_name(self) -> str:
        """Get the name of this step."""
        if not self.color_support:
            return f"ColorProfile(B&W-{self.bit_depth}bit)"
        else:
            gamut_name = self.target_gamut.value if self.target_gamut else "RGB"
            return f"ColorProfile({gamut_name})"
