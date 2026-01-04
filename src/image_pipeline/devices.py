"""
Device specifications for popular e-readers and tablets.

This module contains resolution and display characteristics for different devices
to optimize manga image processing for each device type.
"""

from dataclasses import dataclass
from enum import Enum


class DisplayType(Enum):
    """Type of display technology."""

    EINK = "e-ink"
    LCD = "lcd"
    OLED = "oled"
    RETINA = "retina"


class ColorGamut(Enum):
    """Color gamut standards for displays."""

    NONE = None  # For B&W displays
    SRGB = "sRGB"  # Standard RGB (most LCD displays)
    DCI_P3 = "DCI-P3"  # Wide gamut (iPad Pro, high-end displays)
    ADOBE_RGB = "Adobe RGB"  # Wide gamut (professional displays)


@dataclass
class DeviceSpec:
    """
    Complete specification for a device.

    Attributes:
        name: Display name of the device
        resolution: Screen resolution as (width, height) tuple
        display_type: Type of display technology
        ppi: Pixels per inch
        screen_size_inches: Physical screen size in inches
        color_support: True if device supports color, False for B&W
        color_gamut: Color gamut standard (None for B&W devices)
        bit_depth: Color bit depth (4=16 colors, 8=256, 24=16M colors)
        max_colors: Maximum number of colors device can display
        recommended_pipeline: Name of the recommended pipeline preset
        description: Human-readable description
    """

    name: str
    resolution: tuple[int, int]
    display_type: DisplayType
    ppi: int
    screen_size_inches: float
    color_support: bool
    color_gamut: ColorGamut | None
    bit_depth: int
    max_colors: int | None
    recommended_pipeline: str
    description: str

    def __repr__(self) -> str:
        """String representation of device spec."""
        color_info = "Color" if self.color_support else "B&W"
        return f"{self.name} ({self.resolution[0]}x{self.resolution[1]}, {self.display_type.value}, {color_info})"


class DeviceSpecs:
    """Collection of device specifications for popular e-readers and tablets."""

    # Kindle devices
    KINDLE_PAPERWHITE_11TH = DeviceSpec(
        name="Kindle Paperwhite 11th Gen",
        resolution=(1236, 1648),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=6.8,
        color_support=False,
        color_gamut=None,
        bit_depth=4,  # 16 grayscale levels
        max_colors=16,
        recommended_pipeline="kindle",
        description='6.8" e-ink display, 300 ppi',
    )

    KINDLE_PAPERWHITE = DeviceSpec(
        name="Kindle Paperwhite (older)",
        resolution=(1072, 1448),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=6.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kindle",
        description='6" e-ink display, 300 ppi',
    )

    KINDLE_SCRIBE = DeviceSpec(
        name="Kindle Scribe",
        resolution=(1860, 2480),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=10.2,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kindle",
        description='10.2" e-ink display, 300 ppi',
    )

    KINDLE_OASIS = DeviceSpec(
        name="Kindle Oasis",
        resolution=(1264, 1680),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=7.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kindle",
        description='7" e-ink display, 300 ppi',
    )

    # Kobo devices
    KOBO_LIBRA_2 = DeviceSpec(
        name="Kobo Libra 2",
        resolution=(1264, 1680),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=7.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kobo",
        description='7" e-ink display, 300 ppi',
    )

    KOBO_SAGE = DeviceSpec(
        name="Kobo Sage",
        resolution=(1440, 1920),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=8.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kobo",
        description='8" e-ink display, 300 ppi',
    )

    KOBO_ELIPSA_2E = DeviceSpec(
        name="Kobo Elipsa 2E",
        resolution=(1404, 1872),
        display_type=DisplayType.EINK,
        ppi=227,
        screen_size_inches=10.3,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kobo",
        description='10.3" e-ink display, 227 ppi',
    )

    KOBO_CLARA_2E = DeviceSpec(
        name="Kobo Clara 2E",
        resolution=(1072, 1448),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=6.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kobo",
        description='6" e-ink display, 300 ppi',
    )

    # Tolino devices
    TOLINO_VISION_6 = DeviceSpec(
        name="Tolino Vision 6",
        resolution=(1264, 1680),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=7.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="tolino",
        description='7" e-ink display, 300 ppi',
    )

    TOLINO_EPOS_3 = DeviceSpec(
        name="Tolino Epos 3",
        resolution=(1404, 1872),
        display_type=DisplayType.EINK,
        ppi=227,
        screen_size_inches=8.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="tolino",
        description='8" e-ink display, 227 ppi',
    )

    TOLINO_PAGE_2 = DeviceSpec(
        name="Tolino Page 2",
        resolution=(1072, 1448),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=6.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="tolino",
        description='6" e-ink display, 300 ppi',
    )

    # PocketBook devices
    POCKETBOOK_INKPAD_4 = DeviceSpec(
        name="PocketBook InkPad 4",
        resolution=(1072, 1448),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=7.8,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="pocketbook",
        description='7.8" e-ink display, 300 ppi',
    )

    POCKETBOOK_INKPAD_COLOR_3 = DeviceSpec(
        name="PocketBook InkPad Color 3",
        resolution=(1236, 1648),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=7.8,
        color_support=True,
        color_gamut=ColorGamut.SRGB,  # E-ink color limited gamut
        bit_depth=12,  # ~4096 colors typical for e-ink color
        max_colors=4096,
        recommended_pipeline="pocketbook_color",
        description='7.8" color e-ink display, 300 ppi',
    )

    POCKETBOOK_ERA = DeviceSpec(
        name="PocketBook Era",
        resolution=(1072, 1448),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=7.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="pocketbook",
        description='7" e-ink display, 300 ppi',
    )

    # iPad devices
    IPAD_PRO_11 = DeviceSpec(
        name='iPad Pro 11"',
        resolution=(1668, 2388),
        display_type=DisplayType.RETINA,
        ppi=264,
        screen_size_inches=11.0,
        color_support=True,
        color_gamut=ColorGamut.DCI_P3,  # Wide gamut
        bit_depth=24,  # 16M colors
        max_colors=16777216,
        recommended_pipeline="ipad",
        description='11" Liquid Retina display, 264 ppi',
    )

    IPAD_PRO_129 = DeviceSpec(
        name='iPad Pro 12.9"',
        resolution=(2048, 2732),
        display_type=DisplayType.RETINA,
        ppi=264,
        screen_size_inches=12.9,
        color_support=True,
        color_gamut=ColorGamut.DCI_P3,
        bit_depth=24,
        max_colors=16777216,
        recommended_pipeline="ipad",
        description='12.9" Liquid Retina XDR display, 264 ppi',
    )

    IPAD_AIR = DeviceSpec(
        name="iPad Air",
        resolution=(1640, 2360),
        display_type=DisplayType.RETINA,
        ppi=264,
        screen_size_inches=10.9,
        color_support=True,
        color_gamut=ColorGamut.DCI_P3,
        bit_depth=24,
        max_colors=16777216,
        recommended_pipeline="ipad",
        description='10.9" Liquid Retina display, 264 ppi',
    )

    IPAD_MINI = DeviceSpec(
        name="iPad Mini",
        resolution=(1488, 2266),
        display_type=DisplayType.RETINA,
        ppi=326,
        screen_size_inches=8.3,
        color_support=True,
        color_gamut=ColorGamut.DCI_P3,
        bit_depth=24,
        max_colors=16777216,
        recommended_pipeline="ipad",
        description='8.3" Liquid Retina display, 326 ppi',
    )

    IPAD_10 = DeviceSpec(
        name="iPad 10th Gen",
        resolution=(1620, 2360),
        display_type=DisplayType.RETINA,
        ppi=264,
        screen_size_inches=10.9,
        color_support=True,
        color_gamut=ColorGamut.SRGB,  # Standard gamut (not P3)
        bit_depth=24,
        max_colors=16777216,
        recommended_pipeline="ipad",
        description='10.9" Liquid Retina display, 264 ppi',
    )

    @classmethod
    def get_all_devices(cls) -> dict[str, DeviceSpec]:
        """
        Get all device specifications.

        Returns:
            Dictionary mapping device keys to DeviceSpec objects.
        """
        return {
            # Kindle
            "kindle_paperwhite_11": cls.KINDLE_PAPERWHITE_11TH,
            "kindle_paperwhite": cls.KINDLE_PAPERWHITE,
            "kindle_scribe": cls.KINDLE_SCRIBE,
            "kindle_oasis": cls.KINDLE_OASIS,
            # Kobo
            "kobo_libra_2": cls.KOBO_LIBRA_2,
            "kobo_sage": cls.KOBO_SAGE,
            "kobo_elipsa_2e": cls.KOBO_ELIPSA_2E,
            "kobo_clara_2e": cls.KOBO_CLARA_2E,
            # Tolino
            "tolino_vision_6": cls.TOLINO_VISION_6,
            "tolino_epos_3": cls.TOLINO_EPOS_3,
            "tolino_page_2": cls.TOLINO_PAGE_2,
            # PocketBook
            "pocketbook_inkpad_4": cls.POCKETBOOK_INKPAD_4,
            "pocketbook_inkpad_color_3": cls.POCKETBOOK_INKPAD_COLOR_3,
            "pocketbook_era": cls.POCKETBOOK_ERA,
            # iPad
            "ipad_pro_11": cls.IPAD_PRO_11,
            "ipad_pro_129": cls.IPAD_PRO_129,
            "ipad_air": cls.IPAD_AIR,
            "ipad_mini": cls.IPAD_MINI,
            "ipad_10": cls.IPAD_10,
        }

    @classmethod
    def get_device(cls, key: str) -> DeviceSpec:
        """
        Get a device specification by key.

        Args:
            key: Device key (e.g., 'kindle_paperwhite', 'ipad_pro_11').

        Returns:
            DeviceSpec for the requested device.

        Raises:
            KeyError: If device key is not found.
        """
        devices = cls.get_all_devices()
        if key not in devices:
            available = ", ".join(sorted(devices.keys()))
            raise KeyError(f"Unknown device '{key}'. Available devices: {available}")
        return devices[key]

    @classmethod
    def list_devices(cls) -> list[str]:
        """
        Get a list of all available device keys.

        Returns:
            List of device keys.
        """
        return sorted(cls.get_all_devices().keys())

    @classmethod
    def get_devices_by_brand(cls, brand: str) -> dict[str, DeviceSpec]:
        """
        Get all devices from a specific brand.

        Args:
            brand: Brand name (kindle, kobo, tolino, pocketbook, ipad).

        Returns:
            Dictionary of devices from the specified brand.
        """
        all_devices = cls.get_all_devices()
        brand_lower = brand.lower()
        return {
            key: spec
            for key, spec in all_devices.items()
            if key.startswith(brand_lower)
        }
