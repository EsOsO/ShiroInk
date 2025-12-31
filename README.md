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
  - Choices: `kindle`, `tablet`, `print`, `high_quality`, `minimal`

### Pipeline Presets

#### Kindle (default)
Optimized for Kindle e-readers with e-ink displays:
```sh
python src/main.py manga/ output/ --pipeline kindle
```
- High contrast for e-ink
- Moderate sharpening
- 16-color quantization (reduces file size)

#### Tablet
Optimized for color tablets:
```sh
python src/main.py webcomic/ output/ --pipeline tablet -r 1080x1920
```
- Moderate contrast
- Light sharpening
- Preserves full color

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

### Examples

#### Standard Kindle Processing
```sh
python src/main.py /path/to/manga /path/to/output
```

#### RTL Manga for Tablet
```sh
python src/main.py /manga/source /manga/output --rtl --pipeline tablet -r 1200x1600
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
docker run --rm -it \
    -v /path/to/source:/manga/src \
    -v /path/to/destination:/manga/dest \
    ghcr.io/esoso/shiroink \
    --pipeline kindle \
    /manga/src/MangaName /manga/dest/MangaName
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

- [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) - Complete overview of improvements
- [REFACTORING_PUNTO1.md](REFACTORING_PUNTO1.md) - ProcessingConfig details (Italian)
- [REFACTORING_PUNTO2.md](REFACTORING_PUNTO2.md) - ProgressReporter details (Italian)
- [REFACTORING_PUNTO3.md](REFACTORING_PUNTO3.md) - Pipeline details (Italian)

## License

This project is licensed under the ISC License. See the [LICENSE.txt](LICENSE.txt) file for details.

## Acknowledgements

- [Rich](https://github.com/Textualize/rich) for beautiful console output
- [Pillow](https://python-pillow.org/) for image processing capabilities
