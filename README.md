# ShiroInk

ShiroInk is a powerful tool for processing manga images optimized for various e-readers and devices. It supports resizing, customizable image processing pipelines, and CBZ format creation.

## Features

- **Flexible Image Processing**: 5 predefined pipelines + custom configurations
- **Device Optimization**: Presets for Kindle, tablets, print, and more
- **Batch Processing**: Multi-threaded processing of directories and CBZ files
- **Right-to-Left Support**: Full RTL manga support
- **Configurable**: Extensive CLI options for fine-tuning
- **Testable**: 20+ unit tests ensuring reliability

## What's New (v2.0)

### Major Improvements
1. **Simplified Configuration**: Single config object instead of 10+ parameters
2. **Dependency Injection**: Pluggable progress reporters (console, file, silent)
3. **Configurable Pipeline**: Choose from 5 presets or create custom processing pipelines

See [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) for detailed information.

## Requirements

- Python 3.11+
- [Rich](https://github.com/Textualize/rich)
- [Pillow](https://python-pillow.org/)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/esoso/shiroink.git
    cd shiroink
    ```

2. Create a virtual environment:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Basic Usage

```sh
python src/main.py <src_dir> <dest_dir> [options]
```

### Arguments

- `src_dir`: Source directory containing files to process
- `dest_dir`: Destination directory to place processed files

### Options

- `-r, --resolution`: Resolution to resize the images (default: `1404x1872`)
  - Examples: `800x600`, `1080x1920`, `800` (square)
- `--rtl`: Switch the order of two-page images (for RTL manga)
- `-q, --quality`: Compression quality level (1-9, default: `6`)
- `-d, --debug`: Enable debug output
- `-w, --workers`: Number of threads to use (default: `4`)
- `--dry-run`: Preview what would be done without processing
- `-p, --pipeline`: Processing pipeline preset (default: `kindle`)
  - Choices: `kindle`, `kobo`, `tolino`, `pocketbook`, `pocketbook_color`, `ipad`, `eink`, `tablet`, `print`, `high_quality`, `minimal`
- `--device`: Specific device preset (auto-sets resolution and pipeline)
  - Examples: `kindle_paperwhite_11`, `kobo_libra_2`, `ipad_pro_11`
  - Use `--list-devices` to see all available devices
- `--list-devices`: List all available device presets and exit

### Pipeline Presets

ShiroInk includes optimized presets for different e-reader brands and display types:

#### E-ink Devices

##### Kindle (default)
Optimized for Kindle e-readers with e-ink displays:
```sh
python src/main.py manga/ output/ --pipeline kindle
# Or use specific device preset:
python src/main.py manga/ output/ --device kindle_paperwhite_11
```
- High contrast for e-ink
- Moderate sharpening
- 16-color quantization (reduces file size)
- Supported devices: Kindle Paperwhite, Kindle Oasis, Kindle Scribe

##### Kobo
Optimized for Kobo e-readers:
```sh
python src/main.py manga/ output/ --pipeline kobo
# Or use specific device preset:
python src/main.py manga/ output/ --device kobo_libra_2
```
- High contrast for e-ink
- Strong sharpening (Kobo benefits from sharper images)
- 16-color quantization
- Supported devices: Kobo Libra 2, Kobo Sage, Kobo Elipsa 2E, Kobo Clara 2E

##### Tolino
Optimized for Tolino e-readers:
```sh
python src/main.py manga/ output/ --pipeline tolino
# Or use specific device preset:
python src/main.py manga/ output/ --device tolino_vision_6
```
- High contrast for e-ink
- Moderate sharpening
- 16-color quantization
- Supported devices: Tolino Vision 6, Tolino Epos 3, Tolino Page 2

##### PocketBook
Optimized for PocketBook e-readers:
```sh
# For standard e-ink models:
python src/main.py manga/ output/ --pipeline pocketbook
# Or use specific device preset:
python src/main.py manga/ output/ --device pocketbook_era

# For color e-ink models:
python src/main.py manga/ output/ --pipeline pocketbook_color
# Or use specific device preset:
python src/main.py manga/ output/ --device pocketbook_inkpad_color_3
```
- Standard: High contrast, moderate sharpening, 16-color quantization
- Color: Moderate contrast, light sharpening, full color preservation
- Supported devices: PocketBook InkPad 4, PocketBook Era, PocketBook InkPad Color 3

#### Tablets and High-Resolution Displays

##### iPad
Optimized for iPad and Retina displays:
```sh
python src/main.py webcomic/ output/ --pipeline ipad
# Or use specific device preset:
python src/main.py webcomic/ output/ --device ipad_pro_11
```
- Light contrast for LCD/OLED
- Enhanced sharpening for high-res displays
- Full color preservation
- Supported devices: iPad Pro 11", iPad Pro 12.9", iPad Air, iPad Mini, iPad 10th Gen

#### Tablet
Optimized for color tablets:
```sh
python src/main.py webcomic/ output/ --pipeline tablet -r 1080x1920
```
- Moderate contrast
- Light sharpening
- Preserves full color

#### Generic E-ink
Generic preset for any e-ink device:
```sh
python src/main.py manga/ output/ --pipeline eink
```
- High contrast for e-ink clarity
- Moderate sharpening
- 16-color quantization

#### Print
Minimal processing for print output:
```sh
python src/main.py manga/ print_output/ --pipeline print
```
- Light sharpening only
- No color reduction

#### High Quality
For high-resolution displays:
```sh
python src/main.py manga/ hq_output/ --pipeline high_quality -r 2048x2732
```
- Enhanced sharpening
- Light contrast
- Full color preservation

#### Minimal
No processing (resize only):
```sh
python src/main.py manga/ output/ --pipeline minimal
```
- Fast processing
- No image enhancements

### Device Presets

For convenience, you can use the `--device` flag to automatically configure resolution and pipeline for specific devices:

```sh
# List all available devices
python src/main.py --list-devices

# Use a specific device preset
python src/main.py manga/ output/ --device kindle_paperwhite_11
python src/main.py manga/ output/ --device kobo_sage
python src/main.py manga/ output/ --device ipad_pro_129
```

Available device families:
- **Kindle**: `kindle_paperwhite`, `kindle_paperwhite_11`, `kindle_oasis`, `kindle_scribe`
- **Kobo**: `kobo_clara_2e`, `kobo_libra_2`, `kobo_sage`, `kobo_elipsa_2e`
- **Tolino**: `tolino_page_2`, `tolino_vision_6`, `tolino_epos_3`
- **PocketBook**: `pocketbook_era`, `pocketbook_inkpad_4`, `pocketbook_inkpad_color_3`
- **iPad**: `ipad_10`, `ipad_mini`, `ipad_air`, `ipad_pro_11`, `ipad_pro_129`

### Examples

#### Device-Specific Processing
```sh
# Use device preset (auto-configures resolution and pipeline)
python src/main.py /path/to/manga /path/to/output --device kindle_paperwhite_11

# Kobo with RTL manga
python src/main.py /manga/source /manga/output --device kobo_libra_2 --rtl

# iPad Pro with high quality
python src/main.py /source /dest --device ipad_pro_129 -q 9
```

#### Standard Kindle Processing
```sh
python src/main.py /path/to/manga /path/to/output
```

#### RTL Manga for Tablet
```sh
python src/main.py /manga/source /manga/output --rtl --pipeline tablet -r 1200x1600
```

#### PocketBook Color E-ink
```sh
python src/main.py /manga/source /manga/output --device pocketbook_inkpad_color_3
```

#### High Quality with Custom Resolution
```sh
python src/main.py /source /dest --pipeline high_quality -r 2048x2732 -q 9
```

#### Dry Run (Preview)
```sh
python src/main.py /source /dest --dry-run --debug
```

#### Fast Processing (8 threads, minimal pipeline)
```sh
python src/main.py /source /dest --pipeline minimal -w 8
```

## Advanced Usage

### Programmatic API

```python
from pathlib import Path
from src.config import ProcessingConfig
from src.progress_reporter import ConsoleProgressReporter
from src.main import main

# Create configuration
config = ProcessingConfig(
    src_dir=Path("manga_source"),
    dest_dir=Path("manga_output"),
    resolution=(1404, 1872),
    pipeline_preset="kindle",
    workers=4
)

# Run processing
reporter = ConsoleProgressReporter()
main(config, reporter)
```

### Custom Pipeline

```python
from src.image_pipeline.presets import PipelinePresets

# Create custom pipeline
pipeline = PipelinePresets.custom(
    contrast=2.0,    # High contrast
    sharpen=1.5,     # Strong sharpening
    quantize=False   # Preserve colors
)
```

### Silent Processing (for scripts)

```python
from src.progress_reporter import SilentProgressReporter

reporter = SilentProgressReporter()
main(config, reporter)  # No console output
```

## Docker

Run ShiroInk using Docker:

```sh
# Using device preset
docker run --rm -it \
    -v /path/to/source:/manga/src \
    -v /path/to/destination:/manga/dest \
    ghcr.io/esoso/shiroink \
    --device kobo_libra_2 \
    /manga/src/MangaName /manga/dest/MangaName

# Using pipeline preset
docker run --rm -it \
    -v /path/to/source:/manga/src \
    -v /path/to/destination:/manga/dest \
    ghcr.io/esoso/shiroink \
    --pipeline kindle \
    /manga/src/MangaName /manga/dest/MangaName

# List available devices
docker run --rm ghcr.io/esoso/shiroink --list-devices
```

## Development

### Running Tests

```sh
# All tests
PYTHONPATH=src python -m unittest discover -s . -p 'test_*.py' -v

# Specific test file
PYTHONPATH=src python -m unittest test_pipeline.py -v
```

### Project Structure

```
ShiroInk/
├── src/
│   ├── cli.py                      # CLI argument parsing
│   ├── config.py                   # ProcessingConfig dataclass
│   ├── main.py                     # Main entry point
│   ├── file_processor.py           # File and directory processing
│   ├── progress_reporter.py        # Progress reporting abstraction
│   └── image_pipeline/
│       ├── __init__.py             # Public API
│       ├── pipeline.py             # Pipeline infrastructure
│       ├── presets.py              # Preset configurations
│       ├── contrast.py             # Contrast adjustment
│       ├── sharpen.py              # Image sharpening
│       ├── quantize.py             # Color quantization
│       ├── resize.py               # Image resizing
│       └── save.py                 # Image saving
├── test_example.py                 # Reporter tests
├── test_pipeline.py                # Pipeline tests
└── requirements.txt
```

## Documentation

For complete documentation, see the [docs](docs) directory:

- **[Architecture](docs/architecture/)** - System design and patterns
  - [Overview](docs/architecture/overview.md) - Core components
  - [Pipeline System](docs/architecture/pipeline-system.md) - Processing pipeline
  - [Error Handling](docs/architecture/error-handling.md) - Error management
  - [Progress Reporting](docs/architecture/progress-reporter.md) - Progress tracking

- **[User Guides](docs/guides/)** - How to use ShiroInk
  - [Quick Start](docs/guides/quickstart.md) - Get started in 5 minutes
  - [Installation](docs/guides/installation.md) - Setup instructions
  - [Usage](docs/guides/usage.md) - Usage examples
  - [Device Presets](docs/guides/device-presets.md) - Device specifications
  - [Docker](docs/guides/docker.md) - Docker deployment

- **[Contributing](docs/contributing/)** - Development guidelines
  - [Development](docs/contributing/development.md) - Setup for developers
  - [Testing Guide](docs/contributing/testing-guide.md) - Running tests
  - [Conventional Commits](docs/contributing/conventional-commits.md) - Commit standards

## License

This project is licensed under the ISC License. See the [LICENSE.txt](LICENSE.txt) file for details.

## Acknowledgements

- [Rich](https://github.com/Textualize/rich) for beautiful console output
- [Pillow](https://python-pillow.org/) for image processing capabilities
