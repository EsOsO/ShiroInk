"""
Automatic rotation detection and correction module.

This module provides functionality to detect and correct slight rotations
in scanned manga pages, improving readability and visual alignment.
"""

from PIL import Image
import math
from .pipeline import ProcessingStep


class AutoRotateStep(ProcessingStep):
    """
    Automatically detect and correct image rotation.

    Particularly useful for scanned manga pages that may have slight rotation
    due to scanning imperfections. Uses edge detection to identify text lines
    and calculate the optimal rotation correction.

    Note: For best results with advanced rotation detection, install opencv-python.
    Falls back to basic rotation detection if OpenCV is not available.
    """

    def __init__(
        self,
        max_angle: float = 5.0,
        threshold: float = 0.5,
        enabled: bool = True,
        fill_color: str = "white",
    ):
        """
        Initialize auto-rotation step.

        Args:
            max_angle: Maximum rotation to correct in degrees.
                      Rotations larger than this are ignored (likely intentional).
                      Default: 5.0 degrees.
            threshold: Minimum rotation angle to trigger correction (degrees).
                      Rotations smaller than this are considered insignificant.
                      Default: 0.5 degrees.
            enabled: Whether rotation correction is enabled.
                    Default: True.
            fill_color: Color to fill exposed areas after rotation.
                       Default: "white".
        """
        super().__init__(
            max_angle=max_angle,
            threshold=threshold,
            enabled=enabled,
            fill_color=fill_color,
        )
        self.max_angle = max_angle
        self.threshold = threshold
        self.enabled = enabled
        self.fill_color = fill_color

        # Try to import OpenCV for advanced detection
        self._cv2_available = False
        try:
            import cv2
            import numpy as np

            self._cv2 = cv2
            self._np = np
            self._cv2_available = True
        except ImportError:
            pass

    def process(self, image: Image.Image) -> Image.Image:
        """
        Detect and correct rotation in the image.

        Args:
            image: Input PIL Image.

        Returns:
            Rotated image if rotation detected, otherwise original image.
        """
        if not self.enabled:
            return image

        # Detect rotation angle
        if self._cv2_available:
            angle = self._detect_rotation_opencv(image)
        else:
            angle = self._detect_rotation_basic(image)

        # Check if rotation is significant enough to correct
        if abs(angle) < self.threshold:
            return image  # No significant rotation

        # Check if rotation is within acceptable range
        if abs(angle) > self.max_angle:
            # Too much rotation, might be intentional or misdetected
            return image

        # Apply rotation correction
        # Negative angle because we want to counter-rotate
        return image.rotate(
            -angle,
            resample=Image.Resampling.BICUBIC,
            expand=False,
            fillcolor=self.fill_color,
        )

    def _detect_rotation_opencv(self, image: Image.Image) -> float:
        """
        Detect rotation using OpenCV's Hough line transform.

        This method is more accurate and detects rotation based on
        dominant line orientations (typically panel borders and text baselines).

        Args:
            image: PIL Image to analyze.

        Returns:
            Rotation angle in degrees (positive = clockwise).
        """
        # Convert PIL image to OpenCV format
        img_array = self._np.array(image)
        gray = self._cv2.cvtColor(img_array, self._cv2.COLOR_RGB2GRAY)

        # Edge detection
        edges = self._cv2.Canny(gray, 50, 150, apertureSize=3)

        # Detect lines using Hough transform
        lines = self._cv2.HoughLines(edges, 1, self._np.pi / 180, 200)

        if lines is None or len(lines) == 0:
            return 0.0  # No lines detected

        # Collect angles of all detected lines
        angles = []
        for line in lines:
            rho, theta = line[0]
            # Convert to degrees
            angle = math.degrees(theta) - 90

            # Normalize to -90 to 90 range
            if angle < -90:
                angle += 180
            elif angle > 90:
                angle -= 180

            # Focus on near-horizontal and near-vertical lines
            # (typical for manga panels and text)
            if abs(angle) < 45:  # Near horizontal
                angles.append(angle)
            elif abs(angle - 90) < 45 or abs(angle + 90) < 45:  # Near vertical
                # Normalize vertical lines to horizontal equivalent
                angles.append(angle - 90 if angle > 0 else angle + 90)

        if not angles:
            return 0.0

        # Calculate median angle (more robust than mean)
        angles.sort()
        median_angle = angles[len(angles) // 2]

        return median_angle

    def _detect_rotation_basic(self, image: Image.Image) -> float:
        """
        Basic rotation detection using image moments.

        This is a fallback method when OpenCV is not available.
        Less accurate but still useful for obvious rotations.

        Args:
            image: PIL Image to analyze.

        Returns:
            Rotation angle in degrees (positive = clockwise).
        """
        # Convert to grayscale
        gray = image.convert("L")

        # Simple edge detection using PIL
        from PIL import ImageFilter

        edges = gray.filter(ImageFilter.FIND_EDGES)

        # Get bounding box of content
        bbox = edges.getbbox()

        if not bbox:
            return 0.0  # No content detected

        # Calculate aspect ratio deviation as a proxy for rotation
        # This is a very basic heuristic
        left, top, right, bottom = bbox
        width = right - left
        height = bottom - top

        # For manga pages, we expect roughly portrait orientation
        # If severely skewed, might indicate rotation
        expected_ratio = image.height / image.width
        actual_ratio = height / width if width > 0 else 1.0

        ratio_diff = abs(expected_ratio - actual_ratio)

        # Very basic heuristic: if ratio is off, assume small rotation
        # This is not accurate but better than nothing
        if ratio_diff > 0.1:
            # Guess a small correction angle
            return 1.0 if actual_ratio > expected_ratio else -1.0

        return 0.0  # No significant rotation detected

    def get_name(self) -> str:
        """Get the name of this processing step."""
        if not self.enabled:
            return "AutoRotate(disabled)"
        method = "opencv" if self._cv2_available else "basic"
        return f"AutoRotate({method})"
