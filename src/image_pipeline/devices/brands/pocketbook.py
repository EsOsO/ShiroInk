"""
PocketBook device specifications.

This file contains all PocketBook e-reader configurations.
To add a new device, simply add a new entry to the DEVICES list.
"""

from typing import Final

# PocketBook B&W e-ink devices
POCKETBOOK_BW: Final = "eink_bw"

# PocketBook color e-ink devices
POCKETBOOK_COLOR: Final = "eink_color"

DEVICES = [
    # B&W devices
    {
        "key": "pocketbook_touch_lux_5",
        "name": "PocketBook Touch Lux 5",
        "resolution": (758, 1024),
        "ppi": 212,
        "screen_size": 6.0,
        "template": POCKETBOOK_BW,
        "pipeline": "pocketbook",
        "description": '6" e-ink Carta, 212 ppi',
    },
    {
        "key": "pocketbook_basic_4",
        "name": "PocketBook Basic 4",
        "resolution": (1024, 758),
        "ppi": 212,
        "screen_size": 6.0,
        "template": POCKETBOOK_BW,
        "pipeline": "pocketbook",
        "description": '6" e-ink Carta, 212 ppi',
    },
    {
        "key": "pocketbook_inkpad_lite",
        "name": "PocketBook InkPad Lite",
        "resolution": (825, 1200),
        "ppi": 150,
        "screen_size": 9.7,
        "template": POCKETBOOK_BW,
        "pipeline": "pocketbook",
        "description": '9.7" e-ink Carta, 150 ppi',
    },
    {
        "key": "pocketbook_era",
        "name": "PocketBook Era",
        "resolution": (1264, 1680),
        "ppi": 300,
        "screen_size": 7.0,
        "template": POCKETBOOK_BW,
        "pipeline": "pocketbook",
        "description": '7" E Ink Carta, 300 ppi',
    },
    {
        "key": "pocketbook_inkpad_4",
        "name": "PocketBook InkPad 4",
        "resolution": (1404, 1872),
        "ppi": 300,
        "screen_size": 7.8,
        "template": POCKETBOOK_BW,
        "pipeline": "pocketbook",
        "description": '7.8" E Ink Carta, 300 ppi',
    },
    {
        "key": "pocketbook_inkpad_x_pro",
        "name": "PocketBook InkPad X Pro",
        "resolution": (1404, 1872),
        "ppi": 227,
        "screen_size": 10.3,
        "template": POCKETBOOK_BW,
        "pipeline": "pocketbook",
        "description": '10.3" E Ink Carta, 227 ppi',
    },
    {
        "key": "pocketbook_verse",
        "name": "PocketBook Verse",
        "resolution": (758, 1024),
        "ppi": 212,
        "screen_size": 6.0,
        "template": POCKETBOOK_BW,
        "pipeline": "pocketbook",
        "description": '6" e-ink Carta, 212 ppi',
    },
    {
        "key": "pocketbook_verse_pro",
        "name": "PocketBook Verse Pro",
        "resolution": (1072, 1448),
        "ppi": 300,
        "screen_size": 6.0,
        "template": POCKETBOOK_BW,
        "pipeline": "pocketbook",
        "description": '6" E Ink Carta, 300 ppi',
    },
    # Color devices
    {
        "key": "pocketbook_color_633",
        "name": "PocketBook Color 633",
        "resolution": (1072, 1448),
        "ppi": 212,
        "screen_size": 6.0,
        "template": POCKETBOOK_COLOR,
        "pipeline": "pocketbook_color",
        "description": '6" E Ink Kaleido, 212 ppi',
    },
    {
        "key": "pocketbook_inkpad_color",
        "name": "PocketBook InkPad Color",
        "resolution": (1404, 1872),
        "ppi": 300,
        "screen_size": 7.8,
        "template": POCKETBOOK_COLOR,
        "pipeline": "pocketbook_color",
        "description": '7.8" E Ink Kaleido, 300/100 ppi',
    },
    {
        "key": "pocketbook_inkpad_color_2",
        "name": "PocketBook InkPad Color 2",
        "resolution": (1404, 1872),
        "ppi": 300,
        "screen_size": 7.8,
        "template": POCKETBOOK_COLOR,
        "pipeline": "pocketbook_color",
        "description": '7.8" E Ink Kaleido Plus, 300/100 ppi',
    },
    {
        "key": "pocketbook_inkpad_color_3",
        "name": "PocketBook InkPad Color 3",
        "resolution": (1404, 1872),
        "ppi": 300,
        "screen_size": 7.8,
        "template": POCKETBOOK_COLOR,
        "pipeline": "pocketbook_color",
        "description": '7.8" E Ink Kaleido 3, 300/150 ppi',
    },
    {
        "key": "pocketbook_era_color",
        "name": "PocketBook Era Color",
        "resolution": (1264, 1680),
        "ppi": 300,
        "screen_size": 7.0,
        "template": POCKETBOOK_COLOR,
        "pipeline": "pocketbook_color",
        "description": '7" E Ink Kaleido 3, 300/150 ppi',
    },
    {
        "key": "pocketbook_verse_pro_color",
        "name": "PocketBook Verse Pro Color",
        "resolution": (1072, 1448),
        "ppi": 300,
        "screen_size": 6.0,
        "template": POCKETBOOK_COLOR,
        "pipeline": "pocketbook_color",
        "description": '6" E Ink Kaleido 3, 300/150 ppi',
    },
    {
        "key": "pocketbook_inkpad_eo",
        "name": "PocketBook InkPad Eo",
        "resolution": (1860, 2480),
        "ppi": 300,
        "screen_size": 10.3,
        "template": POCKETBOOK_COLOR,
        "pipeline": "pocketbook_color",
        "description": '10.3" E Ink Kaleido 3, 300/150 ppi',
    },
    {
        "key": "pocketbook_color_note",
        "name": "PocketBook Color Note",
        "resolution": (1404, 1872),
        "ppi": 227,
        "screen_size": 10.3,
        "template": POCKETBOOK_COLOR,
        "pipeline": "pocketbook_color",
        "description": '10.3" E Ink Kaleido 3, 227/76 ppi',
    },
]
