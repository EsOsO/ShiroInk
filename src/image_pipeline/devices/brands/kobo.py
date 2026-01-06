"""
Kobo device specifications.

This file contains all Kobo e-reader configurations.
To add a new device, simply add a new entry to the DEVICES list.
"""

from typing import Final

# Kobo B&W e-ink devices
KOBO_BW: Final = "eink_bw"

# Kobo color e-ink devices
KOBO_COLOR: Final = "eink_color"

DEVICES = [
    {
        "key": "kobo_nia",
        "name": "Kobo Nia",
        "resolution": (1024, 758),
        "ppi": 212,
        "screen_size": 6.0,
        "template": KOBO_BW,
        "pipeline": "kobo",
        "description": '6" E Ink Carta, 212 ppi',
    },
    {
        "key": "kobo_elipsa",
        "name": "Kobo Elipsa",
        "resolution": (1404, 1872),
        "ppi": 227,
        "screen_size": 10.3,
        "template": KOBO_BW,
        "pipeline": "kobo",
        "description": '10.3" E Ink Carta, 227 ppi',
    },
    {
        "key": "kobo_libra_2",
        "name": "Kobo Libra 2",
        "resolution": (1680, 1264),
        "ppi": 300,
        "screen_size": 7.0,
        "template": KOBO_BW,
        "pipeline": "kobo",
        "description": '7" E Ink Carta, 300 ppi',
    },
    {
        "key": "kobo_sage",
        "name": "Kobo Sage",
        "resolution": (1920, 1440),
        "ppi": 300,
        "screen_size": 8.0,
        "template": KOBO_BW,
        "pipeline": "kobo",
        "description": '8" E Ink Carta, 300 ppi',
    },
    {
        "key": "kobo_clara_2e",
        "name": "Kobo Clara 2E",
        "resolution": (1448, 1072),
        "ppi": 300,
        "screen_size": 6.0,
        "template": KOBO_BW,
        "pipeline": "kobo",
        "description": '6" E Ink Carta, 300 ppi',
    },
    {
        "key": "kobo_elipsa_2e",
        "name": "Kobo Elipsa 2E",
        "resolution": (1404, 1872),
        "ppi": 227,
        "screen_size": 10.3,
        "template": KOBO_BW,
        "pipeline": "kobo",
        "description": '10.3" E Ink Carta, 227 ppi',
    },
    {
        "key": "kobo_clara_bw",
        "name": "Kobo Clara BW",
        "resolution": (1448, 1072),
        "ppi": 300,
        "screen_size": 6.0,
        "template": KOBO_BW,
        "pipeline": "kobo",
        "description": '6" E Ink Carta 1300, 300 ppi',
    },
    # Color devices
    {
        "key": "kobo_clara_colour",
        "name": "Kobo Clara Colour",
        "resolution": (1448, 1072),
        "ppi": 300,
        "screen_size": 6.0,
        "template": KOBO_COLOR,
        "pipeline": "kobo_color",
        "description": '6" E Ink Kaleido 3, 300/150 ppi',
    },
    {
        "key": "kobo_libra_colour",
        "name": "Kobo Libra Colour",
        "resolution": (1680, 1264),
        "ppi": 300,
        "screen_size": 7.0,
        "template": KOBO_COLOR,
        "pipeline": "kobo_color",
        "description": '7" E Ink Kaleido 3, 300/150 ppi',
    },
]
