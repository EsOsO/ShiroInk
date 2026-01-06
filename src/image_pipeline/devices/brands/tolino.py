"""
Tolino device specifications.

This file contains all Tolino e-reader configurations.
To add a new device, simply add a new entry to the DEVICES list.
"""

from typing import Final

# Tolino B&W e-ink devices
TOLINO_BW: Final = "eink_bw"

DEVICES = [
    {
        "key": "tolino_vision_6",
        "name": "Tolino Vision 6",
        "resolution": (1264, 1680),
        "ppi": 300,
        "screen_size": 7.0,
        "template": TOLINO_BW,
        "pipeline": "tolino",
        "description": '7" e-ink, 300 ppi',
    },
    {
        "key": "tolino_epos_3",
        "name": "Tolino Epos 3",
        "resolution": (1404, 1872),
        "ppi": 227,
        "screen_size": 8.0,
        "template": TOLINO_BW,
        "pipeline": "tolino",
        "description": '8" e-ink, 227 ppi',
    },
    {
        "key": "tolino_page_2",
        "name": "Tolino Page 2",
        "resolution": (1072, 1448),
        "ppi": 300,
        "screen_size": 6.0,
        "template": TOLINO_BW,
        "pipeline": "tolino",
        "description": '6" e-ink, 300 ppi',
    },
]
