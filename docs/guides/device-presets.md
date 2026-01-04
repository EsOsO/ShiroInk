# Device Presets Guide

ShiroInk provides optimized presets for popular e-readers and tablets, automatically configuring resolution and processing pipeline for the best reading experience.

## Quick Start

List all available devices:
```sh
python src/main.py --list-devices
```

Use a device preset:
```sh
python src/main.py manga/ output/ --device kindle_paperwhite_11
```

## Supported Devices

### Kindle E-Readers

#### Kindle Paperwhite 11th Gen
- **Device Key**: `kindle_paperwhite_11`
- **Resolution**: 1236x1648 (300 ppi)
- **Display**: 6.8" e-ink
- **Pipeline**: `kindle` (high contrast, moderate sharpening, 16-color quantization)

```sh
python src/main.py manga/ output/ --device kindle_paperwhite_11
```

#### Kindle Paperwhite (older generations)
- **Device Key**: `kindle_paperwhite`
- **Resolution**: 1072x1448 (300 ppi)
- **Display**: 6" e-ink
- **Pipeline**: `kindle`

```sh
python src/main.py manga/ output/ --device kindle_paperwhite
```

#### Kindle Oasis
- **Device Key**: `kindle_oasis`
- **Resolution**: 1264x1680 (300 ppi)
- **Display**: 7" e-ink
- **Pipeline**: `kindle`

```sh
python src/main.py manga/ output/ --device kindle_oasis
```

#### Kindle Scribe
- **Device Key**: `kindle_scribe`
- **Resolution**: 1860x2480 (300 ppi)
- **Display**: 10.2" e-ink
- **Pipeline**: `kindle`

```sh
python src/main.py manga/ output/ --device kindle_scribe
```

### Kobo E-Readers

#### Kobo Clara 2E
- **Device Key**: `kobo_clara_2e`
- **Resolution**: 1072x1448 (300 ppi)
- **Display**: 6" e-ink
- **Pipeline**: `kobo` (high contrast, strong sharpening, 16-color quantization)

```sh
python src/main.py manga/ output/ --device kobo_clara_2e
```

#### Kobo Libra 2
- **Device Key**: `kobo_libra_2`
- **Resolution**: 1264x1680 (300 ppi)
- **Display**: 7" e-ink
- **Pipeline**: `kobo`

```sh
python src/main.py manga/ output/ --device kobo_libra_2
```

#### Kobo Sage
- **Device Key**: `kobo_sage`
- **Resolution**: 1440x1920 (300 ppi)
- **Display**: 8" e-ink
- **Pipeline**: `kobo`

```sh
python src/main.py manga/ output/ --device kobo_sage
```

#### Kobo Elipsa 2E
- **Device Key**: `kobo_elipsa_2e`
- **Resolution**: 1404x1872 (227 ppi)
- **Display**: 10.3" e-ink
- **Pipeline**: `kobo`

```sh
python src/main.py manga/ output/ --device kobo_elipsa_2e
```

### Tolino E-Readers

#### Tolino Page 2
- **Device Key**: `tolino_page_2`
- **Resolution**: 1072x1448 (300 ppi)
- **Display**: 6" e-ink
- **Pipeline**: `tolino` (high contrast, moderate sharpening, 16-color quantization)

```sh
python src/main.py manga/ output/ --device tolino_page_2
```

#### Tolino Vision 6
- **Device Key**: `tolino_vision_6`
- **Resolution**: 1264x1680 (300 ppi)
- **Display**: 7" e-ink
- **Pipeline**: `tolino`

```sh
python src/main.py manga/ output/ --device tolino_vision_6
```

#### Tolino Epos 3
- **Device Key**: `tolino_epos_3`
- **Resolution**: 1404x1872 (227 ppi)
- **Display**: 8" e-ink
- **Pipeline**: `tolino`

```sh
python src/main.py manga/ output/ --device tolino_epos_3
```

### PocketBook E-Readers

#### PocketBook Era
- **Device Key**: `pocketbook_era`
- **Resolution**: 1072x1448 (300 ppi)
- **Display**: 7" e-ink
- **Pipeline**: `pocketbook` (high contrast, moderate sharpening, 16-color quantization)

```sh
python src/main.py manga/ output/ --device pocketbook_era
```

#### PocketBook InkPad 4
- **Device Key**: `pocketbook_inkpad_4`
- **Resolution**: 1072x1448 (300 ppi)
- **Display**: 7.8" e-ink
- **Pipeline**: `pocketbook`

```sh
python src/main.py manga/ output/ --device pocketbook_inkpad_4
```

#### PocketBook InkPad Color 3
- **Device Key**: `pocketbook_inkpad_color_3`
- **Resolution**: 1236x1648 (300 ppi)
- **Display**: 7.8" color e-ink
- **Pipeline**: `pocketbook_color` (moderate contrast, light sharpening, full color)

```sh
python src/main.py manga/ output/ --device pocketbook_inkpad_color_3
```

### iPad and Tablets

#### iPad 10th Gen
- **Device Key**: `ipad_10`
- **Resolution**: 1620x2360 (264 ppi)
- **Display**: 10.9" Liquid Retina
- **Pipeline**: `ipad` (light contrast, enhanced sharpening, full color)

```sh
python src/main.py manga/ output/ --device ipad_10
```

#### iPad Mini
- **Device Key**: `ipad_mini`
- **Resolution**: 1488x2266 (326 ppi)
- **Display**: 8.3" Liquid Retina
- **Pipeline**: `ipad`

```sh
python src/main.py manga/ output/ --device ipad_mini
```

#### iPad Air
- **Device Key**: `ipad_air`
- **Resolution**: 1640x2360 (264 ppi)
- **Display**: 10.9" Liquid Retina
- **Pipeline**: `ipad`

```sh
python src/main.py manga/ output/ --device ipad_air
```

#### iPad Pro 11"
- **Device Key**: `ipad_pro_11`
- **Resolution**: 1668x2388 (264 ppi)
- **Display**: 11" Liquid Retina
- **Pipeline**: `ipad`

```sh
python src/main.py manga/ output/ --device ipad_pro_11
```

#### iPad Pro 12.9"
- **Device Key**: `ipad_pro_129`
- **Resolution**: 2048x2732 (264 ppi)
- **Display**: 12.9" Liquid Retina XDR
- **Pipeline**: `ipad`

```sh
python src/main.py manga/ output/ --device ipad_pro_129
```

## Pipeline Characteristics

### E-ink Pipelines (Kindle, Kobo, Tolino, PocketBook)

E-ink displays benefit from:
- **High Contrast** (1.5-1.6x): Improves readability on lower-contrast e-ink screens
- **Moderate to Strong Sharpening** (1.2-1.3x): Compensates for e-ink refresh characteristics
- **16-color Quantization**: Reduces file size significantly (manga is mostly grayscale)

Differences between brands:
- **Kobo**: Slightly stronger sharpening (1.3x) as Kobo devices benefit from crisper images
- **Kindle/Tolino/PocketBook**: Standard settings (1.2-1.25x sharpening)

### Color E-ink Pipeline (PocketBook Color)

Color e-ink requires gentler processing:
- **Moderate Contrast** (1.3x): Preserves color vibrancy
- **Light Sharpening** (1.1x): Avoids artifacts on color e-ink
- **No Quantization**: Full color preservation

### LCD/OLED Pipelines (iPad, Tablet)

High-resolution displays benefit from:
- **Light Contrast** (1.2x): LCD/OLED has better native contrast
- **Enhanced Sharpening** (1.4x): Takes advantage of high pixel density
- **Full Color**: No quantization for vibrant colors

## Advanced Usage

### Override Pipeline

You can use a device preset for resolution but override the pipeline:

```sh
# Use Kobo Libra 2 resolution but with tablet pipeline
python src/main.py manga/ output/ --device kobo_libra_2 --pipeline tablet
```

Note: When you specify `--device`, the pipeline is auto-selected, but you can override it with `--pipeline`.

### Custom Resolution with Device Pipeline

```sh
# Use Kindle pipeline with custom resolution
python src/main.py manga/ output/ --pipeline kindle -r 1600x2400
```

### RTL Manga

All device presets support RTL (right-to-left) manga:

```sh
python src/main.py manga/ output/ --device kobo_sage --rtl
```

## Programmatic API

```python
from pathlib import Path
from src.config import ProcessingConfig
from src.progress_reporter import ConsoleProgressReporter
from src.main import main
from src.image_pipeline.devices import DeviceSpecs

# Get device specification
device = DeviceSpecs.get_device("kindle_paperwhite_11")

# Create configuration
config = ProcessingConfig(
    src_dir=Path("manga_source"),
    dest_dir=Path("manga_output"),
    resolution=device.resolution,
    pipeline_preset="kindle",
    workers=4
)

# Run processing
reporter = ConsoleProgressReporter()
main(config, reporter)
```

## Adding Custom Devices

To add a custom device, edit `src/image_pipeline/devices.py` and add a new `DeviceSpec`:

```python
CUSTOM_DEVICE = DeviceSpec(
    name="My Custom Device",
    resolution=(1200, 1600),
    display_type=DisplayType.EINK,
    ppi=300,
    description="Custom e-reader"
)
```

Then add it to the `get_all_devices()` method.

## Troubleshooting

### Images Too Dark/Light

Adjust the quality setting:
```sh
python src/main.py manga/ output/ --device kobo_libra_2 -q 8  # Higher quality
```

### Images Not Sharp Enough

Use a different pipeline with stronger sharpening:
```sh
python src/main.py manga/ output/ --device kindle_paperwhite --pipeline kobo
```

### File Size Too Large

Ensure quantization is enabled (automatic for e-ink devices) or lower quality:
```sh
python src/main.py manga/ output/ --device ipad_pro_11 -q 4
```

### Wrong Resolution

Verify device preset:
```sh
python src/main.py --list-devices | grep kobo
```
