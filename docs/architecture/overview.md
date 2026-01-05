# ShiroInk Architecture Overview

ShiroInk is a modular image processing system designed for e-book and manga optimization. This document outlines the core architectural components.

## Core Components

### 1. Image Pipeline System
The pipeline is a configurable, modular processing system that transforms images through a series of steps:

- **ResizeStep**: Resizes images to exact device dimensions
- **ContrastStep**: Adjusts image contrast for e-ink displays
- **SharpenStep**: Enhances image sharpness
- **QuantizeStep**: Reduces color palette for file size optimization

Each step implements the `ProcessingStep` interface, allowing easy composition and customization.

**Available presets:**
- `kindle`: Optimized for e-ink displays (default)
- `tablet`: Preserves colors for LCD/tablet devices
- `high_quality`: Enhanced processing for archive storage
- `minimal`: No processing (pass-through)

### 2. Configuration System
The `ProcessingConfig` dataclass centralizes all configuration parameters:

```python
@dataclass
class ProcessingConfig:
    src_dir: Path
    dest_dir: Path
    resolution: tuple[int, int]
    pipeline_preset: str = "kindle"
    continue_on_error: bool = True
    max_retries: int = 3
    # ... other options
```

This eliminates scattered function parameters and provides validated, type-safe configuration.

### 3. Progress Reporting
An abstract `ProgressReporter` interface decouples progress tracking from the UI framework:

- **ConsoleProgressReporter**: Rich-formatted console output
- **SilentProgressReporter**: No output (testing)
- **FileProgressReporter**: File-based logging

This allows flexible reporting without coupling business logic to UI frameworks.

### 4. Error Handling
A robust error handling system with:

- **Exception hierarchy**: Custom exceptions for different error types
- **Error tracking**: Centralized error collection and statistics
- **Retry logic**: Automatic retries with exponential backoff
- **Configurable behavior**: Continue-on-error or fail-fast modes

Exit codes indicate result status:
- `0`: Success
- `1`: Errors occurred
- `2`: Critical errors occurred

## Design Patterns

- **Strategy Pattern**: Pluggable processing steps and reporters
- **Factory Pattern**: Pipeline preset creation
- **Dependency Injection**: Configuration and reporter injection
- **Chain of Responsibility**: Sequential pipeline execution

## Code Organization

```
src/
├── image_pipeline/        # Image processing modules
│   ├── pipeline.py        # Pipeline abstraction
│   ├── presets.py         # Pipeline presets
│   ├── resize_step.py     # Exact dimension resizing
│   ├── contrast.py        # Contrast adjustment
│   ├── sharpen.py         # Sharpening
│   └── ...                # Other processing steps
├── config.py              # Configuration management
├── progress_reporter.py   # Progress abstraction
├── error_handler.py       # Error tracking
└── main.py                # Entry point
```

## Key Design Principles

1. **Single Responsibility**: Each component has one clear purpose
2. **Open/Closed**: Easy to extend (new steps/reporters) without modification
3. **Dependency Inversion**: Components depend on abstractions, not implementations
4. **Backward Compatibility**: Default behavior unchanged; new features are opt-in

## Extension Points

To add a new processing step:

```python
from image_pipeline.pipeline import ProcessingStep

class CustomStep(ProcessingStep):
    def process(self, image: Image.Image) -> Image.Image:
        # Your processing logic
        return image
    
    def get_name(self) -> str:
        return "CustomStep"
```

To add a new reporter:

```python
from progress_reporter import ProgressReporter

class CustomReporter(ProgressReporter):
    def log(self, message: str, level: str = "info") -> None:
        # Your logging logic
        pass
```
