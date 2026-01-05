"""
Resize step for image processing pipeline.

This module provides a ResizeStep that can be integrated into the pipeline
to ensure images are resized to exact device dimensions. This step should
typically be placed AFTER cropping and rotation to ensure the final output
matches the target device resolution exactly.
"""

from PIL import Image, ImageOps
from .pipeline import ProcessingStep


class ResizeStep(ProcessingStep):
    """
    Resize image to exact target resolution with aspect-ratio preserving padding.

    This step ensures the output image matches the device screen resolution exactly
    by resizing while maintaining aspect ratio and adding white padding as needed.

    This is critical for ensuring images fit perfectly on e-reader screens.
    """

    def __init__(self, resolution: tuple[int, int], enabled: bool = True):
        """
        Initialize resize step.

        Args:
            resolution: Target resolution as (width, height) tuple.
            enabled: Whether resizing is enabled. If False, returns image unchanged.
                    Default: True.
        """
        super().__init__(resolution=resolution, enabled=enabled)
        self.resolution = resolution
        self.enabled = enabled

    def process(self, image: Image.Image) -> Image.Image:
        """
        Resize image to target resolution, preserving aspect ratio with padding.

        The algorithm:
        1. Calculate scaling to fit image within target resolution
        2. Resize image maintaining aspect ratio
        3. Add white padding to achieve exact target dimensions

        Args:
            image: Input PIL Image.

        Returns:
            Resized image with exact target resolution.
        """
        if not self.enabled:
            return image

        # Use ImageOps.pad to resize with aspect ratio preservation
        # This adds white padding to achieve exact dimensions
        resized = ImageOps.pad(
            image, self.resolution, method=Image.Resampling.LANCZOS, color="white"
        )

        return resized

    def get_name(self) -> str:
        """Get the name of this processing step."""
        if not self.enabled:
            return "Resize(disabled)"
        return f"Resize({self.resolution[0]}x{self.resolution[1]})"
