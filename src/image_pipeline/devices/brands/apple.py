"""
Apple device specifications (iPad).

This file contains all Apple iPad configurations.
To add a new device, simply add a new entry to the DEVICES list.
"""

from typing import Final

# iPad Retina/LCD displays
APPLE_COLOR: Final = "color"

DEVICES = [
    {
        "key": "ipad_pro_11",
        "name": 'iPad Pro 11"',
        "resolution": (1668, 2388),
        "ppi": 264,
        "screen_size": 11.0,
        "template": APPLE_COLOR,
        "description": '11" Liquid Retina, 264 ppi',
    },
    {
        "key": "ipad_pro_129",
        "name": 'iPad Pro 12.9"',
        "resolution": (2048, 2732),
        "ppi": 264,
        "screen_size": 12.9,
        "template": APPLE_COLOR,
        "description": '12.9" Liquid Retina XDR, 264 ppi',
    },
    {
        "key": "ipad_air",
        "name": "iPad Air",
        "resolution": (1640, 2360),
        "ppi": 264,
        "screen_size": 10.9,
        "template": APPLE_COLOR,
        "description": '10.9" Liquid Retina, 264 ppi',
    },
    {
        "key": "ipad_mini",
        "name": "iPad Mini",
        "resolution": (1488, 2266),
        "ppi": 326,
        "screen_size": 8.3,
        "template": APPLE_COLOR,
        "description": '8.3" Liquid Retina, 326 ppi',
    },
    {
        "key": "ipad_10",
        "name": "iPad 10th Gen",
        "resolution": (1620, 2360),
        "ppi": 264,
        "screen_size": 10.9,
        "template": APPLE_COLOR,
        "description": '10.9" Liquid Retina, 264 ppi',
    },
]
