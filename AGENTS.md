# Agent Guidelines for ShiroInk

This guide provides coding agents with essential commands and style guidelines for working in the ShiroInk repository.

## Quick Start

```bash
# Setup environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-cov pytest-mock

# Set PYTHONPATH
export PYTHONPATH=src  # Windows: set PYTHONPATH=src
```

## Communication and Documentation Standards

### Language Conventions

**IMPORTANT**: This project follows strict language conventions for code and communication:

- **User Communication**: Respond in the same language the user writes in (e.g., Italian if user writes in Italian, English if user writes in English)
- **Internal Reasoning**: ALL internal thoughts and reasoning processes MUST be in English
- **Code Documentation**: ALWAYS in English
  - Docstrings: English only
  - Comments: English only
  - Variable/function names: English only
- **Git Commits**: ALWAYS in English
  - Commit messages: English only
  - PR descriptions: English only
  - Issue descriptions: English only

**Example**:
```python
# ✅ CORRECT
def process_image(image: Image.Image) -> Image.Image:
    """
    Process an image through the pipeline.
    
    Args:
        image: Input image to process.
        
    Returns:
        Processed image.
    """
    # Apply rotation correction before cropping
    rotated = self._fix_rotation(image)
    return rotated

# ❌ WRONG - Italian documentation
def elabora_immagine(image: Image.Image) -> Image.Image:
    """
    Elabora un'immagine attraverso la pipeline.
    
    Args:
        image: Immagine da elaborare.
    """
    # Applica correzione rotazione prima del crop
    ruotata = self._correggi_rotazione(image)
    return ruotata
```

**Why English for code?**
- Makes the codebase accessible to the international open-source community
- Ensures consistency across all technical documentation
- Facilitates collaboration with developers worldwide
- Standard practice in professional software development

### Pre-Commit Checklist

**ALWAYS run these commands BEFORE committing** (in order):

```bash
# 1. Format code with black
black src/ tests/

# 2. Verify with flake8
flake8 src/ --max-line-length=88 --extend-ignore=E203,W503

# 3. Run tests
pytest tests/unit/ -v --tb=short

# 4. Stage changes
git add <modified files>

# 5. Commit with descriptive message (in English)
git commit -m "feat: add feature description"
```

**⚠️ CRITICAL**: Never commit without running black first! Code formatting must be part of the development workflow, not an afterthought.

## Build/Lint/Test Commands

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/unit/test_devices.py -v

# Run single test function
python -m pytest tests/unit/test_devices.py::TestDeviceSpecs::test_get_device -v

# Run with markers
python -m pytest -m unit          # Unit tests only
python -m pytest -m integration   # Integration tests only
python -m pytest -m "not slow"    # Skip slow tests

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Quick unit tests (pre-commit hook)
pytest tests/unit/ -v --tb=short
```

### Linting and Formatting

```bash
# Format code with black (line-length: 88)
black src/ tests/

# Check with flake8
flake8 src/ --max-line-length=88 --extend-ignore=E203,W503

# Type checking with mypy (excludes tests)
mypy src/ --ignore-missing-imports --no-strict-optional

# Pre-commit hooks (runs all checks)
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

### Local Development

```bash
# Run CLI locally
export PYTHONPATH=src
python src/main.py input/ output/ --preset kindle

# Test with device preset
python src/main.py input.jpg -d kobo_clara_colour -o output.jpg

# List available devices
python src/main.py list-devices

# Get device info
python src/main.py device-info kindle_colorsoft_se
```

## Code Style Guidelines

### Imports

Follow this import order (groups separated by blank lines):
```python
# 1. Standard library
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# 2. Third-party packages
from PIL import Image
from rich.console import Console

# 3. Local imports
from image_pipeline.devices import DeviceSpec
from exceptions import ShiroInkError
```

### Type Hints

- **Always use type hints** for function signatures
- Use modern syntax: `list[str]`, `dict[str, int]`, `tuple[int, int]`
- Use `Optional[T]` for nullable types: `Optional[Path]`
- Use `| None` for union types: `str | None` (Python 3.10+)

```python
def process(self, image: Image.Image) -> Image.Image:
    """Process an image."""
    pass

def __init__(self, path: Optional[Path] = None) -> None:
    """Initialize with optional path."""
    self.path = path
```

### Docstrings

Use **Google-style docstrings** with full type information:

```python
def create_pipeline(device: str, options: dict[str, Any]) -> ImagePipeline:
    """
    Create an optimized pipeline for a device.

    Args:
        device: Device key (e.g., 'kindle_paperwhite', 'kobo_clara_colour').
        options: Pipeline configuration options.

    Returns:
        Configured ImagePipeline instance.

    Raises:
        KeyError: If device key is not found.
        InvalidConfigurationError: If options are invalid.
    """
    pass
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `ImagePipeline`, `DeviceSpec`)
- **Functions/methods**: `snake_case` (e.g., `get_device`, `process_image`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `KINDLE_PAPERWHITE`, `MAX_RETRIES`)
- **Private members**: Prefix with `_` (e.g., `_format_message`, `_validate_config`)
- **Enums**: Class in PascalCase, members in UPPER_SNAKE_CASE

```python
class DisplayType(Enum):
    EINK = "e-ink"
    LCD = "lcd"
    RETINA = "retina"
```

### Error Handling

Use **custom exceptions** from `src/exceptions.py`:

```python
from exceptions import ImageProcessingError, FileReadError, ShiroInkError

# Raise with context
raise ImageProcessingError(
    "Failed to process image",
    path=image_path,
    step="quantize",
    original_error=e
)

# Catch and re-raise with context
try:
    image = Image.open(path)
except Exception as e:
    raise FileReadError(path, original_error=e)
```

**Exception hierarchy**:
- `ShiroInkError` (base)
  - `ImageProcessingError`
  - `CBZExtractionError` / `CBZCreationError`
  - `InvalidConfigurationError`
  - `FileReadError` / `FileWriteError`
  - `RetryableError`

### Dataclasses and Enums

Prefer **dataclasses** for data structures:

```python
from dataclasses import dataclass

@dataclass
class DeviceSpec:
    """Device specification."""
    name: str
    resolution: tuple[int, int]
    ppi: int
    color_support: bool
```

Use **Enums** for fixed sets of values:

```python
from enum import Enum

class ColorGamut(Enum):
    SRGB = "sRGB"
    DCI_P3 = "DCI-P3"
```

## Git Commit Conventions

**Follow Conventional Commits** (see `COMMIT_GUIDE.md`):

```bash
# Feature (MINOR bump: 2.0.0 → 2.1.0)
git commit -m "feat: add Kobo color device support"

# Bug fix (PATCH bump: 2.0.0 → 2.0.1)
git commit -m "fix: correct resolution for Kindle Colorsoft"

# Documentation (NO bump)
git commit -m "docs: update device preset guide"

# Tests (NO bump)
git commit -m "test: add device spec validation tests"

# CI/CD (NO bump)
git commit -m "ci: add coverage reporting to workflow"

# Breaking change (MAJOR bump: 2.0.0 → 3.0.0)
git commit -m "feat!: change pipeline API signature"
```

**Excluded paths** (never bump version):
- `docs/**`, `tests/**`, `.github/workflows/**`, `*.md`

## Testing Best Practices

- Place tests in `tests/unit/` or `tests/integration/`
- Name test files `test_*.py` (e.g., `test_devices.py`)
- Name test classes `Test*` (e.g., `TestDeviceSpecs`)
- Name test functions `test_*` (e.g., `test_get_device`)
- Use fixtures from `tests/conftest.py`
- Use markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.slow`

```python
import pytest

@pytest.mark.unit
def test_device_resolution(sample_device):
    """Test device resolution validation."""
    assert sample_device.resolution == (1072, 1448)
```

## Project Structure

```
src/
  image_pipeline/       # Core processing modules
    __init__.py
    pipeline.py         # Pipeline abstraction
    devices.py          # Device specifications
    color_profile.py    # Color management
    quantize.py         # Color quantization
    presets.py          # Pipeline presets
  cli.py               # CLI interface
  main.py              # Entry point
  exceptions.py        # Custom exceptions
tests/
  unit/                # Unit tests
  integration/         # Integration tests
  conftest.py          # Shared fixtures
```

---

**Remember**: Run `pytest tests/unit/ -v` before committing. Use `pre-commit run --all-files` to verify code quality.
