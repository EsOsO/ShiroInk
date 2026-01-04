"""
Smart cropping module for automatic margin detection and removal.

This module provides intelligent cropping functionality to automatically
detect and remove white margins from manga pages, maximizing screen space
utilization on e-reader devices.
"""

from PIL import Image, ImageChops
from .pipeline import ProcessingStep


class SmartCropStep(ProcessingStep):
    """
    Automatically detect and remove white margins from manga pages.

    This step analyzes the image to identify content boundaries and removes
    unnecessary white space while preserving a minimal margin for aesthetics.
    Particularly useful for scanned manga which often have large white borders.
    """

    def __init__(
        self, threshold: int = 250, min_margin: int = 10, enabled: bool = True
    ):
        """
        Initialize smart crop step.

        Args:
            threshold: Pixel brightness threshold for "white" detection (0-255).
                      Pixels brighter than this are considered margin candidates.
                      Default: 250 (near-white).
            min_margin: Minimum margin to preserve around content (pixels).
                       Prevents cropping too tightly to the content.
                       Default: 10 pixels.
            enabled: Whether cropping is enabled. If False, returns image unchanged.
                    Default: True.
        """
        super().__init__(threshold=threshold, min_margin=min_margin, enabled=enabled)
        self.threshold = threshold
        self.min_margin = min_margin
        self.enabled = enabled

    def process(self, image: Image.Image) -> Image.Image:
        """
        Detect and crop white margins from the image.

        The algorithm:
        1. Converts image to grayscale for analysis
        2. Creates a binary mask of "white" pixels above threshold
        3. Finds bounding box of non-white content
        4. Adds back minimum margin for aesthetics
        5. Crops to the calculated bounds

        Args:
            image: Input PIL Image.

        Returns:
            Cropped image with margins removed, or original if no cropping needed.
        """
        if not self.enabled:
            return image

        # Convert to grayscale for analysis
        gray = image.convert("L")

        # Create background reference at threshold brightness
        bg = Image.new("L", gray.size, self.threshold)

        # Calculate difference from white background
        diff = ImageChops.difference(gray, bg)

        # Enhance the difference to make content detection more reliable
        # This step increases contrast between content and margins
        diff = ImageChops.add(diff, diff, 2.0, -100)

        # Get bounding box of non-white content
        bbox = diff.getbbox()

        if bbox:
            width, height = image.size

            # Add back minimum margin, ensuring we stay within image bounds
            left = max(0, bbox[0] - self.min_margin)
            top = max(0, bbox[1] - self.min_margin)
            right = min(width, bbox[2] + self.min_margin)
            bottom = min(height, bbox[3] + self.min_margin)

            # Only crop if we're actually removing a significant margin
            # (avoid cropping if it would only remove a few pixels)
            crop_amount = (
                (bbox[0] - left) + (bbox[1] - top) + (width - right) + (height - bottom)
            )
            if crop_amount > self.min_margin * 2:  # Meaningful crop
                return image.crop((left, top, right, bottom))

        # No cropping needed or beneficial
        return image

    def get_name(self) -> str:
        """Get the name of this processing step."""
        if not self.enabled:
            return "SmartCrop(disabled)"
        return "SmartCrop"
