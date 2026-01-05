# Error Handling System

## Overview

ShiroInk implements a robust error handling system that differentiates between recoverable and critical errors, provides automatic retry logic, and tracks all failures for comprehensive reporting.

## Error Classification

### WARNING
Minor issues that don't affect processing

**Examples:**
- File already exists
- Missing metadata
- Non-critical format issues

**Action:** Log and continue

### ERROR
Recoverable failures affecting individual files

**Examples:**
- Corrupted file
- Unsupported format
- Processing step failure

**Action:** Log, skip file, continue processing

### CRITICAL
Severe errors that may compromise results

**Examples:**
- Directory inaccessible
- Insufficient disk space
- Permission denied
- Batch failure threshold exceeded

**Action:** Log and potentially halt batch processing

## Exception Hierarchy

```
ShiroInkError (base)
├── ImageProcessingError
├── FileReadError
├── FileWriteError
├── CBZExtractionError
├── CBZCreationError
└── RetryableError
```

## Error Tracking

The `ErrorTracker` class centralizes error collection and statistics:

### Key Features

- Tracks all errors with full context
- Categorizes by severity level
- Provides aggregated statistics
- Generates summary reports

### Usage

```python
from error_handler import ErrorTracker, ErrorSeverity

tracker = ErrorTracker()

# Record an error
tracker.add_error(
    error=ImageProcessingError("Failed to process"),
    path=Path("image.jpg"),
    severity=ErrorSeverity.ERROR,
    step="contrast"
)

# Get statistics
summary = tracker.get_summary()
# {
#   'total_errors': 1,
#   'warnings': 0,
#   'errors': 1,
#   'critical': 0,
#   'files_with_errors': 1,
#   'errors_by_step': {'contrast': 1}
# }
```

## Retry Logic

Automatic retry with exponential backoff for transient failures:

```python
@retry_on_error(max_retries=3, delay=1.0, backoff=2.0)
def process_file(path: Path) -> None:
    # Processing logic
    pass
```

**Strategy:**
- Initial delay: 1 second
- Backoff multiplier: 2x
- Total attempts: 4 (initial + 3 retries)
- Timeline: 0s, 1s, 3s, 7s

## Configuration

### ProcessingConfig

```python
@dataclass
class ProcessingConfig:
    continue_on_error: bool = True  # Continue despite errors
    max_retries: int = 3            # Retry attempts for I/O
    debug: bool = False             # Verbose error details
```

### Behavior

**continue_on_error = True (Default)**
- Process all files despite errors
- Track and report failures
- Exit code: 0 (success), 1 (errors), 2 (critical)

**continue_on_error = False**
- Stop on first error
- Useful for strict validation
- Exit code: 0 (success), 1+ (failure)

## Exit Codes

- `0`: Success - no errors
- `1`: Processing completed with non-critical errors
- `2`: Critical errors occurred

## Error Summary Report

```
ERROR SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total errors: 5
  Warnings: 1
  Errors: 3
  Critical: 1
  
Files affected: 4
Most problematic: /path/to/file.jpg (2 errors)

Errors by step:
  image_processing: 3
  cbz_creation: 1
  cbz_extraction: 1

First 5 errors:
  [ERROR] ImageProcessingError: Failed at step contrast
  [ERROR] FileReadError: Permission denied
  [CRITICAL] CBZCreationError: Invalid archive
  ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Usage Examples

### Standard Processing

```bash
# Continue despite errors (default)
python src/main.py input/ output/ --pipeline kindle
```

Output shows total errors and summary.

### Strict Mode

```python
config = ProcessingConfig(
    src_dir=Path("input"),
    dest_dir=Path("output"),
    continue_on_error=False  # Stop on first error
)
```

### Custom Retry Configuration

```python
config = ProcessingConfig(
    src_dir=Path("input"),
    dest_dir=Path("output"),
    max_retries=5  # More aggressive retry
)
```

### Debug Mode

```bash
python src/main.py input/ output/ --debug
```

Shows:
- All retry attempts
- Detailed error messages
- Processing statistics

## Integration with Pipeline

Errors during pipeline execution are caught and tracked:

```python
def process(image_path: Path, output_path: Path) -> None:
    try:
        pipeline = config.get_pipeline()
        image = Image.open(image_path)
        processed = pipeline.process(image)
        processed.save(output_path)
    except Exception as e:
        error_tracker.add_error(
            error=e,
            path=image_path,
            severity=ErrorSeverity.ERROR,
            step="pipeline"
        )
        
        if not config.continue_on_error:
            raise
```

## Testing

### Unit Tests

```bash
# Test error tracking
python -m pytest tests/unit/test_error_handler.py -v

# Test retry logic
python -m pytest tests/unit/test_retry.py -v
```

### Error Simulation

```python
# Test error tracking
tracker = ErrorTracker()
tracker.add_error(
    error=Exception("Test error"),
    path=Path("test.jpg"),
    severity=ErrorSeverity.ERROR
)

assert tracker.has_errors()
assert tracker.get_summary()["total_errors"] == 1
```

## Best Practices

### Development Mode

```python
ProcessingConfig(
    continue_on_error=False,  # Fail fast
    max_retries=1,            # Quick feedback
    debug=True                # Full logging
)
```

### Production Mode

```python
ProcessingConfig(
    continue_on_error=True,   # Process everything
    max_retries=3,            # Reasonable retry
    debug=False               # Summary only
)
```

### Batch Processing

```python
ProcessingConfig(
    continue_on_error=True,   # Never stop
    max_retries=5,            # Aggressive retry
    debug=True                # Full analysis log
)
```

## Error Prevention

### Before Processing

1. Validate directory access
2. Check disk space
3. Verify file permissions
4. Validate file formats

### During Processing

1. Use try-catch blocks
2. Implement retry logic
3. Track all failures
4. Log contextual information

### After Processing

1. Generate summary report
2. Identify patterns
3. Suggest corrective actions
4. Archive logs for analysis

## Monitoring and Logging

Error tracking data can be used for:

- **Monitoring**: Alert on critical errors
- **Analytics**: Identify problematic files or steps
- **Improvement**: Fix recurring issues
- **Audit**: Track all processing failures

## Related Documentation

- [Pipeline System](pipeline-system.md) - Processing steps
- [Progress Reporting](progress-reporter.md) - User feedback
- [Configuration](../guides/quickstart.md) - Setup instructions
