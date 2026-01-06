"""
Device specifications for e-readers and tablets.

This module contains resolution and display characteristics for different devices
to optimize manga image processing for each device type.

Devices are organized by brand in the `brands` subdirectory:
- brands/kindle.py - Kindle e-readers
- brands/kobo.py - Kobo e-readers
- brands/tolino.py - Tolino e-readers
- brands/pocketbook.py - PocketBook e-readers
- brands/apple.py - Apple iPads
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from image_pipeline.enums import DisplayType, ColorGamut
from typing import Optional

if TYPE_CHECKING:
    from image_pipeline.pipeline import ImagePipeline

try:
    from image_pipeline.devices.brands.kindle import DEVICES as KINDLE_DEVICES
    from image_pipeline.devices.brands.kobo import DEVICES as KOBO_DEVICES
    from image_pipeline.devices.brands.tolino import DEVICES as TOLINO_DEVICES
    from image_pipeline.devices.brands.pocketbook import DEVICES as POCKETBOOK_DEVICES
    from image_pipeline.devices.brands.apple import DEVICES as APPLE_DEVICES
except ImportError as e:
    raise ImportError(f"Failed to import device brand modules: {e}")


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
        recommended_pipeline: Recommended pipeline preset name
        description: Human-readable description
    """

    name: str
    resolution: tuple[int, int]
    display_type: DisplayType
    ppi: int
    screen_size_inches: float
    color_support: bool
    color_gamut: Optional[ColorGamut]
    bit_depth: int
    max_colors: Optional[int]
    recommended_pipeline: str
    description: str

    def __repr__(self) -> str:
        """String representation of device spec."""
        color_info = "Color" if self.color_support else "B&W"
        return (
            f"{self.name} ({self.resolution[0]}x{self.resolution[1]}, "
            f"{self.display_type.value}, {color_info})"
        )


class DeviceTemplates:
    """Device templates with display characteristics and pipeline parameters."""

    EINK_BW = dict(
        display_type=DisplayType.EINK,
        color_support=False,
        color_gamut=None,
        bit_depth=4,
        max_colors=16,
        pipeline="kindle",
        pipeline_params=dict(
            contrast=1.6,
            sharpen=1.3,
            quantize=True,
            text_sharpen=1.5,
            edge_enhance=0.3,
        ),
    )

    EINK_COLOR = dict(
        display_type=DisplayType.EINK,
        color_support=True,
        color_gamut=ColorGamut.SRGB,
        bit_depth=12,
        max_colors=4096,
        pipeline="kindle_color",
        pipeline_params=dict(
            contrast=1.3,
            sharpen=1.1,
            quantize=False,
            text_sharpen=1.3,
            edge_enhance=0.25,
        ),
    )

    COLOR = dict(
        display_type=DisplayType.RETINA,
        color_support=True,
        color_gamut=ColorGamut.DCI_P3,
        bit_depth=24,
        max_colors=16777216,
        pipeline="ipad",
        pipeline_params=dict(
            contrast=1.2,
            sharpen=1.4,
            quantize=False,
            text_sharpen=1.4,
            edge_enhance=0.25,
        ),
    )

    @classmethod
    def get_template(cls, template_key: str) -> dict:
        """Get a template by key."""
        templates = {
            "eink_bw": cls.EINK_BW,
            "eink_color": cls.EINK_COLOR,
            "color": cls.COLOR,
        }
        if template_key not in templates:
            raise ValueError(
                f"Unknown template: {template_key}. Available: {list(templates.keys())}"
            )
        return templates[template_key].copy()


def _create_device_spec(data: dict) -> DeviceSpec:
    """Create a DeviceSpec from a device data dictionary."""
    template = DeviceTemplates.get_template(data["template"])
    return DeviceSpec(
        name=data["name"],
        resolution=data["resolution"],
        ppi=data["ppi"],
        screen_size_inches=data["screen_size"],
        description=data["description"],
        display_type=template["display_type"],
        color_support=template["color_support"],
        color_gamut=template["color_gamut"],
        bit_depth=template["bit_depth"],
        max_colors=template["max_colors"],
        recommended_pipeline=data.get("pipeline") or template["pipeline"],
    )


class DeviceSpecs:
    """Collection of device specifications for e-readers and tablets."""

    _DEVICES: dict[str, DeviceSpec] = {}

    @classmethod
    def _define(
        cls,
        name: str,
        resolution: tuple[int, int],
        template_key: str,
        ppi: int,
        screen_size: float,
        description: str,
        pipeline: str | None = None,
    ) -> DeviceSpec:
        """Create a DeviceSpec from parameters."""
        template = DeviceTemplates.get_template(template_key)
        return DeviceSpec(
            name=name,
            resolution=resolution,
            ppi=ppi,
            screen_size_inches=screen_size,
            description=description,
            display_type=template["display_type"],
            color_support=template["color_support"],
            color_gamut=template["color_gamut"],
            bit_depth=template["bit_depth"],
            max_colors=template["max_colors"],
            recommended_pipeline=pipeline or template["pipeline"],
        )

    @classmethod
    def _init_devices(cls) -> None:
        """Initialize all device specifications from brand modules."""
        if cls._DEVICES:
            return

        cls._DEVICES = {}

        for device_data in (
            KINDLE_DEVICES
            + KOBO_DEVICES
            + TOLINO_DEVICES
            + POCKETBOOK_DEVICES
            + APPLE_DEVICES
        ):
            cls._DEVICES[device_data["key"]] = _create_device_spec(device_data)

    @classmethod
    def get_all_devices(cls) -> dict[str, DeviceSpec]:
        """Get all device specifications."""
        cls._init_devices()
        return cls._DEVICES.copy()

    @classmethod
    def get_device(cls, key: str) -> DeviceSpec:
        """Get a device specification by key."""
        devices = cls.get_all_devices()
        if key not in devices:
            available = ", ".join(sorted(devices.keys()))
            raise KeyError(f"Unknown device '{key}'. Available: {available}")
        return devices[key]

    @classmethod
    def list_devices(cls) -> list[str]:
        """Get a list of all available device keys."""
        return sorted(cls.get_all_devices().keys())

    @classmethod
    def get_devices_by_brand(cls, brand: str) -> dict[str, DeviceSpec]:
        """Get all devices from a specific brand."""
        all_devices = cls.get_all_devices()
        brand_lower = brand.lower()
        return {
            key: spec
            for key, spec in all_devices.items()
            if key.startswith(brand_lower)
        }

    @classmethod
    def format_devices_for_display(cls) -> str:
        """Format all devices as a formatted string for CLI display."""
        brands = {
            "Kindle": [],
            "Kobo": [],
            "Tolino": [],
            "PocketBook": [],
            "iPad": [],
        }

        for key, spec in sorted(cls.get_all_devices().items()):
            if key.startswith("kindle"):
                brands["Kindle"].append((key, spec))
            elif key.startswith("kobo"):
                brands["Kobo"].append((key, spec))
            elif key.startswith("tolino"):
                brands["Tolino"].append((key, spec))
            elif key.startswith("pocketbook"):
                brands["PocketBook"].append((key, spec))
            elif key.startswith("ipad"):
                brands["iPad"].append((key, spec))

        lines = [
            "\nAvailable device presets:\n",
            "=" * 140,
            f"{'Device':<32} {'Resolution':<12} {'Size':<7} "
            f"{'Display':<8} {'Color':<8} {'Gamut':<10} {'Bits':<5} {'Pipeline':<20}",
            "-" * 140,
        ]

        for brand, device_list in brands.items():
            if device_list:
                for key, spec in device_list:
                    color_str = "Color" if spec.color_support else "B&W"
                    gamut_str = spec.color_gamut.value if spec.color_gamut else "-"
                    lines.append(
                        f"{key:<32} {spec.resolution[0]:4d}x{spec.resolution[1]:<7d} "
                        f'{spec.screen_size_inches:>5.1f}" {spec.display_type.value:<8} '
                        f"{color_str:<8} {gamut_str:<10} {spec.bit_depth:<5} "
                        f"{spec.recommended_pipeline:<20}"
                    )

        lines.extend(
            [
                "\n" + "=" * 140,
                "\nUsage: --device <device_key>",
                "Example: --device kindle_paperwhite_11",
                "\n",
            ]
        )

        return "\n".join(lines)

    @classmethod
    def format_device_info(cls, device_spec: DeviceSpec) -> str:
        """
        Format device information for CLI display.

        Args:
            device_spec: Device specification to format

        Returns:
            Formatted string with device information
        """
        lines = [
            f"\n{'=' * 60}",
            f"Using device preset: {device_spec.name}",
            f"{'=' * 60}",
            f"Resolution:       {device_spec.resolution[0]}x{device_spec.resolution[1]}",
            f'Screen size:      {device_spec.screen_size_inches}"',
            f"Display type:     {device_spec.display_type.value}",
            f"Color support:    {'Color' if device_spec.color_support else 'B&W only'}",
        ]

        if device_spec.color_gamut:
            lines.append(f"Color gamut:      {device_spec.color_gamut.value}")

        lines.append(
            f"Bit depth:        {device_spec.bit_depth}-bit "
            f"({device_spec.max_colors if device_spec.max_colors else 'grayscale'} colors)"
        )
        lines.append(f"Recommended:      {device_spec.recommended_pipeline} pipeline")
        lines.append(f"{'=' * 60}\n")

        return "\n".join(lines)

    @classmethod
    def _get_template_key(cls, device: DeviceSpec) -> str:
        """Get the template key for a device based on its characteristics."""
        if device.display_type == DisplayType.EINK:
            if device.color_support:
                return "eink_color"
            return "eink_bw"
        return "color"

    @classmethod
    def create_pipeline(cls, device: DeviceSpec) -> "ImagePipeline":
        """Create an optimized pipeline for a device based on its template."""
        from image_pipeline.pipeline import ImagePipeline
        from image_pipeline.contrast import ContrastStep
        from image_pipeline.sharpen import SharpenStep
        from image_pipeline.quantize import QuantizeStep, Palette16
        from image_pipeline.color_profile import ColorProfileStep
        from image_pipeline.crop import SmartCropStep
        from image_pipeline.rotation import AutoRotateStep
        from image_pipeline.text_enhance import TextEnhanceStep

        template_key = cls._get_template_key(device)
        template = DeviceTemplates.get_template(template_key)
        params = template["pipeline_params"]

        target_gamut = device.color_gamut
        if target_gamut and isinstance(target_gamut, str):
            gamut_map = {"srgb": ColorGamut.SRGB, "dci_p3": ColorGamut.DCI_P3}
            target_gamut = gamut_map.get(target_gamut.lower(), ColorGamut.NONE)

        pipeline = ImagePipeline()
        pipeline.add_step(AutoRotateStep(max_angle=5.0, threshold=0.5))
        pipeline.add_step(SmartCropStep(threshold=245, min_margin=10))
        pipeline.add_step(
            TextEnhanceStep(
                text_sharpen=params["text_sharpen"],
                edge_enhance=params["edge_enhance"],
            )
        )
        pipeline.add_step(
            ColorProfileStep(
                color_support=device.color_support,
                target_gamut=target_gamut,
                bit_depth=device.bit_depth,
            )
        )
        pipeline.add_step(ContrastStep(factor=params["contrast"]))
        pipeline.add_step(SharpenStep(factor=params["sharpen"]))
        if params["quantize"]:
            pipeline.add_step(QuantizeStep(palette=Palette16))

        return pipeline
