# Image Processing Pipeline System

## Overview

The image processing pipeline is a modular, configurable system for transforming images through a sequence of processing steps. Each step implements the `ProcessingStep` interface, allowing flexible composition and customization.

## Architecture

### Core Concepts

**ProcessingStep (Interface)**
- Abstract base class for all processing operations
- Must implement `process()` and `get_name()` methods
- Encapsulates both configuration and execution

**ImagePipeline (Container)**
- Manages a sequence of ProcessingStep instances
- Executes steps in order (Chain of Responsibility pattern)
- Supports dynamic add/remove operations
- Provides fluent interface for construction

**Pipeline Presets (Factory)**
- Pre-configured pipelines for common use cases
- Optimized for specific device types and quality requirements
- Easy to extend or customize

## Available Steps

### ResizeStep
Resizes images to exact device screen dimensions.

**Configuration:**
```python
ResizeStep(width: int, height: int, fit_mode: str = "contain")
```

**Use case:** Ensure output matches exact device resolution

### ContrastStep
Adjusts image contrast for better readability on e-ink displays.

**Configuration:**
```python
ContrastStep(factor: float = 1.5)
```

**Use case:** Enhance visibility on low-contrast displays

### SharpenStep
Enhances edge sharpness and detail clarity.

**Configuration:**
```python
SharpenStep(factor: float = 1.2)
```

**Use case:** Improve text and line clarity

### QuantizeStep
Reduces color palette to decrease file size.

**Configuration:**
```python
QuantizeStep(palette: bytes = Palette16)
```

**Use case:** Optimize for e-ink displays or reduce file size

## Preset Pipelines

### kindle (Default)
Optimized for Amazon Kindle e-ink readers.

**Steps:**
- ResizeStep (to device resolution)
- ContrastStep (factor: 1.5)
- SharpenStep (factor: 1.2)
- QuantizeStep (16 colors)

**Best for:** E-ink readers, file size optimization

### tablet
Optimized for LCD/tablet displays.

**Steps:**
- ResizeStep (to device resolution)
- ContrastStep (factor: 1.3)
- SharpenStep (factor: 1.1)

**Best for:** Color LCD devices, web viewing

### high_quality
Maximum quality for archival storage.

**Steps:**
- ResizeStep (to device resolution)
- ContrastStep (factor: 1.2)
- SharpenStep (factor: 1.4)

**Best for:** Archive storage, future-proofing

### minimal
No processing (pass-through).

**Steps:** None

**Best for:** Quick conversions, preserving original quality

### custom
Build a custom pipeline programmatically.

```python
pipeline = ImagePipeline()
pipeline.add_step(ContrastStep(factor=1.8))
pipeline.add_step(SharpenStep(factor=1.5))
```

## Usage Examples

### Using Presets via CLI

```bash
# Default (kindle preset)
python src/main.py input/ output/

# Tablet optimization
python src/main.py input/ output/ --pipeline tablet

# High quality archive
python src/main.py input/ output/ --pipeline high_quality

# No processing
python src/main.py input/ output/ --pipeline minimal
```

### Programmatic Usage

```python
from image_pipeline.presets import PipelinePresets
from image_pipeline import process

# Using a preset
pipeline = PipelinePresets.kindle()
process(input_path, output_path, resolution=(1072, 1448), pipeline=pipeline)

# Using custom pipeline
pipeline = ImagePipeline()
pipeline.add_step(ContrastStep(factor=1.8))
pipeline.add_step(SharpenStep(factor=1.5))

process(input_path, output_path, resolution=(1072, 1448), pipeline=pipeline)

# Method chaining
pipeline = (ImagePipeline()
    .add_step(ContrastStep(1.5))
    .add_step(SharpenStep(1.2)))
```

### Dynamic Modification

```python
# Start with preset
pipeline = PipelinePresets.kindle()

# Modify it
pipeline.remove_step("Quantize")  # Preserve colors
pipeline.add_step(CustomStep())   # Add custom processing

process(input_path, output_path, resolution=res, pipeline=pipeline)
```

## Creating Custom Steps

To add a new processing step:

```python
from image_pipeline.pipeline import ProcessingStep
from PIL import Image, ImageFilter

class BlurStep(ProcessingStep):
    """Apply Gaussian blur to image."""
    
    def __init__(self, radius: float = 2.0):
        super().__init__(radius=radius)
        self.radius = radius
    
    def process(self, image: Image.Image) -> Image.Image:
        return image.filter(ImageFilter.GaussianBlur(self.radius))
    
    def get_name(self) -> str:
        return "Blur"

# Use it
pipeline = ImagePipeline()
pipeline.add_step(BlurStep(radius=3.0))
```

## Creating Custom Presets

```python
from image_pipeline.presets import PipelinePresets
from image_pipeline.pipeline import ImagePipeline

# Add to PipelinePresets class
@staticmethod
def manga_optimized() -> ImagePipeline:
    """Pipeline optimized for manga."""
    pipeline = ImagePipeline()
    pipeline.add_step(ContrastStep(factor=1.8))
    pipeline.add_step(SharpenStep(factor=1.5))
    pipeline.add_step(QuantizeStep())
    return pipeline

# Use it
pipeline = PipelinePresets.manga_optimized()
```

## Design Patterns

### Strategy Pattern
Each ProcessingStep is a strategy that can be swapped or replaced.

### Chain of Responsibility
Pipeline executes steps sequentially, each transforming the image for the next.

### Factory Pattern
PipelinePresets creates pre-configured pipelines.

### Builder Pattern
Fluent interface (`add_step()`, `remove_step()`) for constructing pipelines.

## Testing

### Unit Tests

```bash
# Run pipeline tests
python -m pytest tests/unit/test_pipeline.py -v

# Run device preset tests
python -m pytest tests/unit/test_devices.py -v
```

### Functional Tests

```bash
# Test different presets
python src/main.py test_images/ output/ --pipeline kindle
python src/main.py test_images/ output/ --pipeline tablet
python src/main.py test_images/ output/ --pipeline high_quality
```

## Configuration

Pipeline preset can be specified via CLI or configuration:

```python
from config import ProcessingConfig

config = ProcessingConfig(
    src_dir=Path("input"),
    dest_dir=Path("output"),
    pipeline_preset="tablet"  # or custom instance
)
```

## Benefits

1. **Modularity**: Each step is independent and testable
2. **Flexibility**: Easy to add, remove, or reorder steps
3. **Extensibility**: Create custom steps without modifying core code
4. **Performance**: Disable expensive steps when not needed
5. **Reusability**: Share pipelines across projects

## Migration Guide

### Before (Hardcoded Pipeline)
```python
img = contrast(img)
img = sharpen(img)
img = quantize(img)
```

### After (Flexible Pipeline)
```python
pipeline = PipelinePresets.kindle()
img = pipeline.process(img)
```
