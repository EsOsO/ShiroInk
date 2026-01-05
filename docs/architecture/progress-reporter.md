# Progress Reporting Architecture

## Overview

ShiroInk uses an abstract `ProgressReporter` interface to decouple progress tracking from specific UI frameworks. This enables flexible reporting without coupling business logic to console output or other UI dependencies.

## Architecture

### The Problem

Without abstraction:
- Business logic tightly coupled to Rich library
- Testing requires complex UI mocking
- Difficult to add new reporting methods
- UI concerns mixed with processing logic

### The Solution

Abstract `ProgressReporter` interface enables:
- Multiple reporting implementations
- Easy testing without UI
- Flexible output channels
- Clear separation of concerns

## ProgressReporter Interface

```python
class ProgressReporter(ABC):
    """Abstract interface for progress reporting."""
    
    @abstractmethod
    def log(self, message: str, level: str = "info") -> None:
        """Log a message."""
        pass
    
    @abstractmethod
    def add_task(self, description: str, total: int) -> Any:
        """Create a progress task."""
        pass
    
    @abstractmethod
    def advance_task(self, task_id: Any, advance: int = 1) -> None:
        """Update task progress."""
        pass
```

## Implementations

### ConsoleProgressReporter

Rich-formatted console output with colors and progress bars.

**Features:**
- Colored output by log level
- Progress bars for file processing
- Real-time status updates
- Professional formatting

**Use case:** Interactive command-line use

```python
from progress_reporter import ConsoleProgressReporter

reporter = ConsoleProgressReporter()
reporter.log("Processing started", level="info")
task_id = reporter.add_task("Processing files", total=100)
reporter.advance_task(task_id, 10)
```

### SilentProgressReporter

No output at all.

**Features:**
- Zero I/O overhead
- No console pollution
- Completely silent

**Use cases:**
- Unit testing
- CI/CD pipelines
- Headless environments
- Background processing

```python
from progress_reporter import SilentProgressReporter

reporter = SilentProgressReporter()
main(config, reporter)  # Runs silently
```

### FileProgressReporter

Logs to a file instead of console.

**Features:**
- Persistent log file
- Time-stamped entries
- Structured logging
- No console output

**Use cases:**
- Batch processing
- Server environments
- Audit trails
- Debugging complex issues

```python
from progress_reporter import FileProgressReporter
from pathlib import Path

reporter = FileProgressReporter(Path("processing.log"))
main(config, reporter)
# Creates: processing.log with all messages
```

## Dependency Injection

### Pattern

```python
def main(config: ProcessingConfig, reporter: ProgressReporter):
    """Main processing function with injected reporter."""
    reporter.log("Starting processing", level="info")
    
    # Business logic doesn't know or care about reporter type
    pipeline = config.get_pipeline()
    process_files(config, pipeline, reporter)
    
    reporter.log("Completed", level="info")
```

### Benefits

1. **Testability**: Use SilentProgressReporter in tests
2. **Flexibility**: Swap implementations without changing code
3. **Separation**: Business logic independent of UI
4. **Extensibility**: Easy to add new reporter types

## Creating Custom Reporters

```python
from progress_reporter import ProgressReporter
from pathlib import Path

class CustomReporter(ProgressReporter):
    """Custom reporter implementation."""
    
    def __init__(self, config: dict):
        self.config = config
    
    def log(self, message: str, level: str = "info") -> None:
        # Your logging logic
        print(f"[{level.upper()}] {message}")
    
    def add_task(self, description: str, total: int) -> str:
        task_id = str(uuid.uuid4())
        print(f"Task: {description}")
        return task_id
    
    def advance_task(self, task_id: str, advance: int = 1) -> None:
        # Update progress tracking
        pass

# Use it
reporter = CustomReporter({})
main(config, reporter)
```

## Usage Examples

### Standard Processing (Console)

```bash
python src/main.py input/ output/ --pipeline kindle
```

Output:
```
Processing images... ━━━━━━━━━━━━━━━━━━━ 50%
Processing: image1.jpg... ✓
Processing: image2.jpg... ✓
```

### Silent Processing (Testing)

```python
from progress_reporter import SilentProgressReporter

def test_processing():
    config = ProcessingConfig(
        src_dir=Path("test_input"),
        dest_dir=Path("test_output")
    )
    reporter = SilentProgressReporter()
    
    # No console output during test
    main(config, reporter)
    
    # Verify results
    assert Path("test_output/image.jpg").exists()
```

### File Logging

```python
from progress_reporter import FileProgressReporter

config = ProcessingConfig(
    src_dir=Path("input"),
    dest_dir=Path("output")
)
reporter = FileProgressReporter(Path("processing.log"))

main(config, reporter)

# Review log
with open("processing.log") as f:
    print(f.read())
```

### Batch Processing

```bash
# Run silently with file logging
python src/main.py input/ output/ > batch.log 2>&1

# Check results
tail batch.log
```

## Integration with Error Handling

The reporter is used throughout error handling:

```python
def main(config: ProcessingConfig, reporter: ProgressReporter) -> int:
    error_tracker = ErrorTracker()
    
    try:
        process_files(config, reporter, error_tracker)
    except Exception as e:
        reporter.log(f"Error: {e}", level="error")
        error_tracker.add_error(e, None, ErrorSeverity.CRITICAL)
    
    # Report summary
    if error_tracker.has_errors():
        summary = error_tracker.get_summary()
        reporter.log(
            f"Completed with {summary['total_errors']} errors",
            level="error"
        )
        return 1
    
    reporter.log("Completed successfully", level="info")
    return 0
```

## Log Levels

### INFO
General informational messages.

```python
reporter.log("Starting processing", level="info")
```

### WARNING
Issues that don't stop processing.

```python
reporter.log("File already exists, skipping", level="warning")
```

### ERROR
Recoverable errors.

```python
reporter.log("Failed to process file, skipping", level="error")
```

### DEBUG
Detailed technical information (if debug mode enabled).

```python
if config.debug:
    reporter.log("Opening image pipeline", level="debug")
```

## Performance Considerations

- **ConsoleProgressReporter**: Slight I/O overhead for formatting
- **SilentProgressReporter**: Zero overhead (ideal for testing)
- **FileProgressReporter**: Disk I/O but buffered for efficiency

## Testing Strategy

### Unit Tests with SilentReporter

```python
def test_file_processing():
    config = ProcessingConfig(...)
    reporter = SilentProgressReporter()
    
    # No output, fast execution
    result = process_files(config, reporter)
    
    assert result is True
```

### Integration Tests with FileReporter

```python
def test_batch_processing():
    log_file = Path("test.log")
    reporter = FileProgressReporter(log_file)
    
    main(config, reporter)
    
    # Verify log contents
    log_contents = log_file.read_text()
    assert "completed" in log_contents.lower()
```

## Extension Points

### Adding a New Reporter Type

1. Inherit from `ProgressReporter`
2. Implement required methods
3. Use like any other reporter

```python
class MetricsReporter(ProgressReporter):
    def __init__(self, metrics_endpoint: str):
        self.endpoint = metrics_endpoint
    
    def log(self, message: str, level: str = "info") -> None:
        # Send to metrics service
        requests.post(self.endpoint, json={"message": message, "level": level})
```

### Adding a New Log Level

Extend log levels by modifying reporter implementations:

```python
def log(self, message: str, level: str = "info") -> None:
    if level == "trace":
        # Ultra-detailed logging
        self._trace(message)
    elif level == "debug":
        # Debug information
        self._debug(message)
```

## Related Documentation

- [Pipeline System](pipeline-system.md) - Processing pipeline
- [Error Handling](error-handling.md) - Error tracking
- [Configuration](../guides/quickstart.md) - Setup instructions
