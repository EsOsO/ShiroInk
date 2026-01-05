"""
Pytest configuration and shared fixtures.
"""

import pytest
from pathlib import Path
from PIL import Image

from src.config import ProcessingConfig
from src.progress_reporter import SilentProgressReporter
from src.error_handler import ErrorTracker


@pytest.fixture
def test_image():
    """Create a simple test image."""
    return Image.new("RGB", (100, 100), color="white")


@pytest.fixture
def test_grayscale_image():
    """Create a grayscale test image."""
    return Image.new("L", (100, 100), color=128)


@pytest.fixture
def test_color_image():
    """Create a colorful test image for color processing tests."""
    img = Image.new("RGB", (100, 100))
    pixels = img.load()
    for x in range(100):
        for y in range(100):
            pixels[x, y] = (x * 2, y * 2, (x + y) % 256)
    return img


@pytest.fixture
def silent_reporter():
    """Create a silent progress reporter for testing."""
    return SilentProgressReporter()


@pytest.fixture
def error_tracker():
    """Create an error tracker for testing."""
    return ErrorTracker()


@pytest.fixture
def test_config(tmp_path):
    """Create a test configuration."""
    src_dir = tmp_path / "src"
    dest_dir = tmp_path / "dest"
    src_dir.mkdir()
    dest_dir.mkdir()

    return ProcessingConfig(
        src_dir=src_dir,
        dest_dir=dest_dir,
        resolution=(1000, 1000),
        dry_run=True,
        debug=False,
    )


@pytest.fixture
def sample_images(tmp_path):
    """Create sample image files for integration tests."""
    src_dir = tmp_path / "images"
    src_dir.mkdir()

    # Create a few test images
    for i in range(3):
        img = Image.new("RGB", (200, 300), color=(i * 80, i * 80, i * 80))
        img.save(src_dir / f"test_image_{i}.png")

    return src_dir
