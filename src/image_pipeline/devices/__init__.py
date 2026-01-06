"""
Device specifications module.

Devices are organized by brand in the `brands` subdirectory:
- brands/kindle.py - Kindle e-readers
- brands/kobo.py - Kobo e-readers
- brands/tolino.py - Tolino e-readers
- brands/pocketbook.py - PocketBook e-readers
- brands/apple.py - Apple iPads
"""

from ._specs import DeviceSpec, DeviceSpecs, DeviceTemplates
from image_pipeline.enums import DisplayType, ColorGamut

__all__ = [
    "DeviceSpec",
    "DeviceSpecs",
    "DeviceTemplates",
    "DisplayType",
    "ColorGamut",
]
