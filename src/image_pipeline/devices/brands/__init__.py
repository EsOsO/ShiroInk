"""
Device brand modules.

Import all device lists from brand modules.
"""

from .kindle import DEVICES as KINDLE_DEVICES
from .kobo import DEVICES as KOBO_DEVICES
from .tolino import DEVICES as TOLINO_DEVICES
from .pocketbook import DEVICES as POCKETBOOK_DEVICES
from .apple import DEVICES as APPLE_DEVICES

__all__ = [
    "KINDLE_DEVICES",
    "KOBO_DEVICES",
    "TOLINO_DEVICES",
    "POCKETBOOK_DEVICES",
    "APPLE_DEVICES",
]
