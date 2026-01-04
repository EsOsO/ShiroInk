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
        return (
            f"{self.name} ({self.resolution[0]}x{self.resolution[1]}, "
            f"{self.display_type.value}, {color_info})"
        )


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

    KINDLE_PAPERWHITE_11TH_SE = DeviceSpec(
        name="Kindle Paperwhite Signature Edition (11th Gen)",
        resolution=(1236, 1648),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=6.8,
        color_support=False,
        color_gamut=None,
        bit_depth=4,  # 16 grayscale levels
        max_colors=16,
        recommended_pipeline="kindle",
        description='6.8" e-ink display, 300 ppi, Qi charging, IPX8',
    )

    KINDLE_11_2022 = DeviceSpec(
        name="Kindle (11th Gen, 2022)",
        resolution=(1072, 1448),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=6.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kindle",
        description='6" e-ink display, 300 ppi, USB-C',
    )

    KINDLE_SCRIBE_2024 = DeviceSpec(
        name="Kindle Scribe (2024)",
        resolution=(1860, 2480),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=10.2,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kindle",
        description='10.2" e-ink display, 300 ppi, Wacom stylus',
    )

    KINDLE_11_2024 = DeviceSpec(
        name="Kindle (11th Gen, 2024)",
        resolution=(1072, 1448),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=6.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kindle",
        description='6" e-ink display, 300 ppi, USB-C',
    )

    KINDLE_PAPERWHITE_12TH = DeviceSpec(
        name="Kindle Paperwhite (12th Gen)",
        resolution=(1264, 1680),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=7.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kindle",
        description='7" e-ink display, 300 ppi, IPX8',
    )

    KINDLE_PAPERWHITE_12TH_SE = DeviceSpec(
        name="Kindle Paperwhite Signature Edition (12th Gen)",
        resolution=(1264, 1680),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=7.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kindle",
        description='7" e-ink display, 300 ppi, Qi charging, IPX8',
    )

    KINDLE_COLORSOFT_SE = DeviceSpec(
        name="Kindle Colorsoft Signature Edition",
        resolution=(1264, 1680),
        display_type=DisplayType.EINK,
        ppi=300,  # 300 ppi B&W, 150 ppi color layer
        screen_size_inches=7.0,
        color_support=True,
        color_gamut=ColorGamut.SRGB,  # E Ink Kaleido technology
        bit_depth=12,  # ~4096 colors (E Ink Kaleido)
        max_colors=4096,
        recommended_pipeline="kindle_color",
        description='7" color e-ink (Kaleido), 300/150 ppi, IPX8',
    )

    # Kobo devices
    # Kobo devices (2020-2025)

    # 2020 releases
    KOBO_NIA = DeviceSpec(
        name="Kobo Nia",
        resolution=(1024, 758),
        display_type=DisplayType.EINK,
        ppi=212,
        screen_size_inches=6.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kobo",
        description='6" E Ink Carta, 212 ppi, entry-level',
    )

    # 2021 releases
    KOBO_ELIPSA = DeviceSpec(
        name="Kobo Elipsa",
        resolution=(1404, 1872),
        display_type=DisplayType.EINK,
        ppi=227,
        screen_size_inches=10.3,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kobo",
        description='10.3" E Ink Carta 1200, 227 ppi, stylus',
    )

    KOBO_LIBRA_2 = DeviceSpec(
        name="Kobo Libra 2",
        resolution=(1680, 1264),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=7.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kobo",
        description='7" E Ink Carta 1200, 300 ppi, IPX8',
    )

    KOBO_SAGE = DeviceSpec(
        name="Kobo Sage",
        resolution=(1920, 1440),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=8.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kobo",
        description='8" E Ink Carta 1200, 300 ppi, IPX8, stylus',
    )

    # 2022 releases
    KOBO_CLARA_2E = DeviceSpec(
        name="Kobo Clara 2E",
        resolution=(1448, 1072),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=6.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kobo",
        description='6" E Ink Carta 1200, 300 ppi, IPX8, 85% recycled',
    )

    # 2023 releases
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
        description='10.3" E Ink Carta 1200, 227 ppi, stylus v2',
    )

    # 2024 releases
    KOBO_CLARA_BW = DeviceSpec(
        name="Kobo Clara BW",
        resolution=(1448, 1072),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=6.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="kobo",
        description='6" E Ink Carta 1300, 300 ppi, IPX8, repairable',
    )

    KOBO_CLARA_COLOUR = DeviceSpec(
        name="Kobo Clara Colour",
        resolution=(1448, 1072),
        display_type=DisplayType.EINK,
        ppi=300,  # 300 ppi B&W, 150 ppi color
        screen_size_inches=6.0,
        color_support=True,
        color_gamut=ColorGamut.SRGB,  # E Ink Kaleido 3
        bit_depth=12,  # 4096 colors
        max_colors=4096,
        recommended_pipeline="kobo_color",
        description='6" E Ink Kaleido 3, 300/150 ppi, IPX8, repairable',
    )

    KOBO_LIBRA_COLOUR = DeviceSpec(
        name="Kobo Libra Colour",
        resolution=(1680, 1264),
        display_type=DisplayType.EINK,
        ppi=300,  # 300 ppi B&W, 150 ppi color
        screen_size_inches=7.0,
        color_support=True,
        color_gamut=ColorGamut.SRGB,  # E Ink Kaleido 3
        bit_depth=12,  # 4096 colors
        max_colors=4096,
        recommended_pipeline="kobo_color",
        description='7" E Ink Kaleido 3, 300/150 ppi, IPX8, stylus',
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

    # PocketBook devices (2020-2025)

    # 2020 releases
    POCKETBOOK_TOUCH_LUX_5 = DeviceSpec(
        name="PocketBook Touch Lux 5",
        resolution=(758, 1024),
        display_type=DisplayType.EINK,
        ppi=212,
        screen_size_inches=6.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="pocketbook",
        description='6" e-ink Carta, 212 ppi, SMARTlight',
    )

    POCKETBOOK_COLOR_633 = DeviceSpec(
        name="PocketBook Color (633)",
        resolution=(1072, 1448),
        display_type=DisplayType.EINK,
        ppi=212,
        screen_size_inches=6.0,
        color_support=True,
        color_gamut=ColorGamut.SRGB,  # E Ink Kaleido
        bit_depth=12,  # E Ink Kaleido = 4096 colors
        max_colors=4096,
        recommended_pipeline="pocketbook_color",
        description='6" E Ink Kaleido (first gen), 212 ppi',
    )

    POCKETBOOK_BASIC_4 = DeviceSpec(
        name="PocketBook Basic 4",
        resolution=(1024, 758),
        display_type=DisplayType.EINK,
        ppi=212,
        screen_size_inches=6.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="pocketbook",
        description='6" e-ink Carta, 212 ppi, entry-level',
    )

    # 2021 releases
    POCKETBOOK_INKPAD_COLOR = DeviceSpec(
        name="PocketBook InkPad Color",
        resolution=(1404, 1872),
        display_type=DisplayType.EINK,
        ppi=300,  # 300 ppi B&W, 100 ppi color
        screen_size_inches=7.8,
        color_support=True,
        color_gamut=ColorGamut.SRGB,  # E Ink Kaleido Plus
        bit_depth=12,  # 4096 colors
        max_colors=4096,
        recommended_pipeline="pocketbook_color",
        description='7.8" E Ink Kaleido Plus, 300/100 ppi',
    )

    POCKETBOOK_INKPAD_LITE = DeviceSpec(
        name="PocketBook InkPad Lite",
        resolution=(825, 1200),
        display_type=DisplayType.EINK,
        ppi=150,
        screen_size_inches=9.7,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="pocketbook",
        description='9.7" e-ink Carta, 150 ppi, large screen',
    )

    # 2022 releases
    POCKETBOOK_ERA = DeviceSpec(
        name="PocketBook Era (700)",
        resolution=(1264, 1680),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=7.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="pocketbook",
        description='7" E Ink Carta 1200, 300 ppi, IPX8',
    )

    # 2023 releases
    POCKETBOOK_INKPAD_4 = DeviceSpec(
        name="PocketBook InkPad 4",
        resolution=(1404, 1872),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=7.8,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="pocketbook",
        description='7.8" E Ink Carta 1200, 300 ppi, IPX8',
    )

    POCKETBOOK_INKPAD_COLOR_2 = DeviceSpec(
        name="PocketBook InkPad Color 2",
        resolution=(1404, 1872),
        display_type=DisplayType.EINK,
        ppi=300,  # 300 ppi B&W, 100 ppi color
        screen_size_inches=7.8,
        color_support=True,
        color_gamut=ColorGamut.SRGB,  # E Ink Kaleido Plus
        bit_depth=12,  # 4096 colors
        max_colors=4096,
        recommended_pipeline="pocketbook_color",
        description='7.8" E Ink Kaleido Plus, 300/100 ppi, IPX8',
    )

    POCKETBOOK_INKPAD_COLOR_3 = DeviceSpec(
        name="PocketBook InkPad Color 3",
        resolution=(1404, 1872),
        display_type=DisplayType.EINK,
        ppi=300,  # 300 ppi B&W, 150 ppi color
        screen_size_inches=7.8,
        color_support=True,
        color_gamut=ColorGamut.SRGB,  # E Ink Kaleido 3
        bit_depth=12,  # 4096 colors
        max_colors=4096,
        recommended_pipeline="pocketbook_color",
        description='7.8" E Ink Kaleido 3 Color, 300/150 ppi, IPX8',
    )

    POCKETBOOK_INKPAD_X_PRO = DeviceSpec(
        name="PocketBook InkPad X Pro",
        resolution=(1404, 1872),
        display_type=DisplayType.EINK,
        ppi=227,
        screen_size_inches=10.3,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="pocketbook",
        description='10.3" E Ink Carta Mobius, 227 ppi, Wacom',
    )

    POCKETBOOK_VERSE = DeviceSpec(
        name="PocketBook Verse",
        resolution=(758, 1024),
        display_type=DisplayType.EINK,
        ppi=212,
        screen_size_inches=6.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="pocketbook",
        description='6" e-ink Carta, 212 ppi, SMARTlight',
    )

    POCKETBOOK_VERSE_PRO = DeviceSpec(
        name="PocketBook Verse Pro",
        resolution=(1072, 1448),
        display_type=DisplayType.EINK,
        ppi=300,
        screen_size_inches=6.0,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        recommended_pipeline="pocketbook",
        description='6" E Ink Carta 1200, 300 ppi, IPX8',
    )

    # 2024 releases
    POCKETBOOK_ERA_COLOR = DeviceSpec(
        name="PocketBook Era Color",
        resolution=(1264, 1680),
        display_type=DisplayType.EINK,
        ppi=300,  # 300 ppi B&W, 150 ppi color
        screen_size_inches=7.0,
        color_support=True,
        color_gamut=ColorGamut.SRGB,  # E Ink Kaleido 3
        bit_depth=12,  # 4096 colors
        max_colors=4096,
        recommended_pipeline="pocketbook_color",
        description='7" E Ink Kaleido 3, 300/150 ppi, IPX8',
    )

    POCKETBOOK_VERSE_PRO_COLOR = DeviceSpec(
        name="PocketBook Verse Pro Color",
        resolution=(1072, 1448),
        display_type=DisplayType.EINK,
        ppi=300,  # 300 ppi B&W, 150 ppi color
        screen_size_inches=6.0,
        color_support=True,
        color_gamut=ColorGamut.SRGB,  # E Ink Kaleido 3
        bit_depth=12,  # 4096 colors
        max_colors=4096,
        recommended_pipeline="pocketbook_color",
        description='6" E Ink Kaleido 3, 300/150 ppi, IPX8',
    )

    POCKETBOOK_INKPAD_EO = DeviceSpec(
        name="PocketBook InkPad Eo",
        resolution=(1860, 2480),
        display_type=DisplayType.EINK,
        ppi=300,  # 300 ppi B&W, 150 ppi color
        screen_size_inches=10.3,
        color_support=True,
        color_gamut=ColorGamut.SRGB,  # E Ink Kaleido 3
        bit_depth=12,  # 4096 colors
        max_colors=4096,
        recommended_pipeline="pocketbook_color",
        description='10.3" E Ink Kaleido 3, 300/150 ppi, Android',
    )

    POCKETBOOK_COLOR_NOTE = DeviceSpec(
        name="PocketBook Color Note",
        resolution=(1404, 1872),
        display_type=DisplayType.EINK,
        ppi=227,  # 227 ppi B&W, 76 ppi color
        screen_size_inches=10.3,
        color_support=True,
        color_gamut=ColorGamut.SRGB,  # E Ink Kaleido 3
        bit_depth=12,  # 4096 colors
        max_colors=4096,
        recommended_pipeline="pocketbook_color",
        description='10.3" E Ink Kaleido 3, 227/76 ppi',
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
            "kindle_paperwhite_11_se": cls.KINDLE_PAPERWHITE_11TH_SE,
            "kindle_paperwhite": cls.KINDLE_PAPERWHITE,
            "kindle_scribe": cls.KINDLE_SCRIBE,
            "kindle_scribe_2024": cls.KINDLE_SCRIBE_2024,
            "kindle_oasis": cls.KINDLE_OASIS,
            "kindle_11_2022": cls.KINDLE_11_2022,
            "kindle_11_2024": cls.KINDLE_11_2024,
            "kindle_paperwhite_12": cls.KINDLE_PAPERWHITE_12TH,
            "kindle_paperwhite_12_se": cls.KINDLE_PAPERWHITE_12TH_SE,
            "kindle_colorsoft_se": cls.KINDLE_COLORSOFT_SE,
            # Kobo
            "kobo_nia": cls.KOBO_NIA,
            "kobo_elipsa": cls.KOBO_ELIPSA,
            "kobo_libra_2": cls.KOBO_LIBRA_2,
            "kobo_sage": cls.KOBO_SAGE,
            "kobo_clara_2e": cls.KOBO_CLARA_2E,
            "kobo_elipsa_2e": cls.KOBO_ELIPSA_2E,
            "kobo_clara_bw": cls.KOBO_CLARA_BW,
            "kobo_clara_colour": cls.KOBO_CLARA_COLOUR,
            "kobo_libra_colour": cls.KOBO_LIBRA_COLOUR,
            # Tolino
            "tolino_vision_6": cls.TOLINO_VISION_6,
            "tolino_epos_3": cls.TOLINO_EPOS_3,
            "tolino_page_2": cls.TOLINO_PAGE_2,
            # PocketBook
            "pocketbook_touch_lux_5": cls.POCKETBOOK_TOUCH_LUX_5,
            "pocketbook_color_633": cls.POCKETBOOK_COLOR_633,
            "pocketbook_basic_4": cls.POCKETBOOK_BASIC_4,
            "pocketbook_inkpad_color": cls.POCKETBOOK_INKPAD_COLOR,
            "pocketbook_inkpad_lite": cls.POCKETBOOK_INKPAD_LITE,
            "pocketbook_era": cls.POCKETBOOK_ERA,
            "pocketbook_inkpad_4": cls.POCKETBOOK_INKPAD_4,
            "pocketbook_inkpad_color_2": cls.POCKETBOOK_INKPAD_COLOR_2,
            "pocketbook_inkpad_color_3": cls.POCKETBOOK_INKPAD_COLOR_3,
            "pocketbook_inkpad_x_pro": cls.POCKETBOOK_INKPAD_X_PRO,
            "pocketbook_verse": cls.POCKETBOOK_VERSE,
            "pocketbook_verse_pro": cls.POCKETBOOK_VERSE_PRO,
            "pocketbook_era_color": cls.POCKETBOOK_ERA_COLOR,
            "pocketbook_verse_pro_color": cls.POCKETBOOK_VERSE_PRO_COLOR,
            "pocketbook_inkpad_eo": cls.POCKETBOOK_INKPAD_EO,
            "pocketbook_color_note": cls.POCKETBOOK_COLOR_NOTE,
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
