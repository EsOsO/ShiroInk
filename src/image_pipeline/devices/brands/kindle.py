"""
Kindle device specifications.

This file contains all Kindle e-reader configurations.
To add a new device, simply add a new entry to the DEVICES list.
"""

from typing import Final

# Kindle B&W e-ink devices
KINDLE_BW: Final = "eink_bw"

# Kindle color e-ink devices
KINDLE_COLOR: Final = "eink_color"

DEVICES = [
    {
        "key": "kindle_paperwhite_11",
        "name": "Kindle Paperwhite 11th Gen",
        "resolution": (1236, 1648),
        "ppi": 300,
        "screen_size": 6.8,
        "template": KINDLE_BW,
        "description": '6.8" e-ink, 300 ppi',
    },
    {
        "key": "kindle_paperwhite_11_se",
        "name": "Kindle Paperwhite SE 11th Gen",
        "resolution": (1236, 1648),
        "ppi": 300,
        "screen_size": 6.8,
        "template": KINDLE_BW,
        "description": '6.8" e-ink, 300 ppi, Qi',
    },
    {
        "key": "kindle_paperwhite",
        "name": "Kindle Paperwhite (older)",
        "resolution": (1072, 1448),
        "ppi": 300,
        "screen_size": 6.0,
        "template": KINDLE_BW,
        "description": '6" e-ink, 300 ppi',
    },
    {
        "key": "kindle_scribe",
        "name": "Kindle Scribe",
        "resolution": (1860, 2480),
        "ppi": 300,
        "screen_size": 10.2,
        "template": KINDLE_BW,
        "description": '10.2" e-ink, 300 ppi',
    },
    {
        "key": "kindle_scribe_2024",
        "name": "Kindle Scribe 2024",
        "resolution": (1860, 2480),
        "ppi": 300,
        "screen_size": 10.2,
        "template": KINDLE_BW,
        "description": '10.2" e-ink, 300 ppi, stylus',
    },
    {
        "key": "kindle_oasis",
        "name": "Kindle Oasis",
        "resolution": (1264, 1680),
        "ppi": 300,
        "screen_size": 7.0,
        "template": KINDLE_BW,
        "description": '7" e-ink, 300 ppi',
    },
    {
        "key": "kindle_11_2022",
        "name": "Kindle 11th Gen 2022",
        "resolution": (1072, 1448),
        "ppi": 300,
        "screen_size": 6.0,
        "template": KINDLE_BW,
        "description": '6" e-ink, 300 ppi, USB-C',
    },
    {
        "key": "kindle_11_2024",
        "name": "Kindle 11th Gen 2024",
        "resolution": (1072, 1448),
        "ppi": 300,
        "screen_size": 6.0,
        "template": KINDLE_BW,
        "description": '6" e-ink, 300 ppi, USB-C',
    },
    {
        "key": "kindle_paperwhite_12",
        "name": "Kindle Paperwhite 12th Gen",
        "resolution": (1264, 1680),
        "ppi": 300,
        "screen_size": 7.0,
        "template": KINDLE_BW,
        "description": '7" e-ink, 300 ppi, IPX8',
    },
    {
        "key": "kindle_paperwhite_12_se",
        "name": "Kindle Paperwhite SE 12th Gen",
        "resolution": (1264, 1680),
        "ppi": 300,
        "screen_size": 7.0,
        "template": KINDLE_BW,
        "description": '7" e-ink, 300 ppi, Qi, IPX8',
    },
    {
        "key": "kindle_colorsoft_se",
        "name": "Kindle Colorsoft SE",
        "resolution": (1264, 1680),
        "ppi": 300,
        "screen_size": 7.0,
        "template": KINDLE_COLOR,
        "description": '7" color e-ink, 300/150 ppi',
    },
]
