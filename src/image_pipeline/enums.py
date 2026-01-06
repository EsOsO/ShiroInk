"""
Common enums for image pipeline.

DisplayType and ColorGamut enums used across multiple modules.
"""

from enum import Enum


class DisplayType(Enum):
    """Type of display technology."""

    EINK = "e-ink"
    LCD = "lcd"
    OLED = "oled"
    RETINA = "retina"


class ColorGamut(Enum):
    """Color gamut standards for displays."""

    NONE = None
    SRGB = "sRGB"
    DCI_P3 = "DCI-P3"
    ADOBE_RGB = "Adobe RGB"
