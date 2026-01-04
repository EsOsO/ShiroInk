# ShiroInk Test Suite

## Overview

The ShiroInk test suite is organized following industry best practices with clear separation between unit and integration tests.

## Directory Structure

```
tests/
├── __init__.py               # Test package marker
├── conftest.py               # Shared pytest fixtures
├── unit/                     # Unit tests (fast, isolated)
│   ├── __init__.py
│   ├── test_devices.py       # Device specification tests
│   ├── test_pipeline.py      # Pipeline and preset tests
│   ├── test_color_profile.py # ColorProfileStep tests
│   └── test_quantize.py      # QuantizeStep tests
├── integration/              # Integration tests (slower, end-to-end)
│   ├── __init__.py
│   └── test_workflows.py     # Complete workflow tests
└── fixtures/                 # Test data and fixtures
    └── __init__.py
```

## Running Tests

### Install Test Dependencies

```bash
pip install -e ".[dev]"
```

This installs:
- `pytest` - Test framework
- `pytest-cov` - Coverage reporting
- `pytest-mock` - Mocking utilities

### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Run specific test file
pytest tests/unit/test_devices.py

# Run specific test class
pytest tests/unit/test_devices.py::TestDeviceSpecFields

# Run specific test
pytest tests/unit/test_devices.py::TestDeviceSpecFields::test_all_devices_have_name
```

### Run with Coverage

```bash
# Generate coverage report
pytest --cov=src --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### Run Tests with Markers

```bash
# Run only fast unit tests
pytest -m unit

# Run only slow integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Test Organization

### Unit Tests

Unit tests are fast, isolated tests that verify individual components:

- **test_devices.py**: Device specifications, ColorGamut enum, DisplayType enum
- **test_pipeline.py**: Pipeline creation, presets, from_device_spec() factory
- **test_color_profile.py**: ColorProfileStep grayscale/color conversion
- **test_quantize.py**: QuantizeStep, dynamic palette generation

### Integration Tests

Integration tests verify complete workflows:

- **test_workflows.py**: End-to-end device preset workflows, file processing

### Shared Fixtures (conftest.py)

Common fixtures available to all tests:

- `test_image`: Simple RGB test image
- `test_grayscale_image`: Grayscale test image
- `test_color_image`: Colorful test image for processing tests
- `silent_reporter`: SilentProgressReporter for testing
- `error_tracker`: ErrorTracker for testing
- `test_config`: ProcessingConfig with temp directories
- `sample_images`: Directory with sample image files

## Writing Tests

### Test Class Organization

Group related tests in classes:

```python
class TestFeatureName:
    """Test feature description."""
    
    def test_specific_behavior(self):
        """Test specific behavior."""
        # Arrange
        # Act
        # Assert
```

### Using Fixtures

```python
def test_with_fixture(test_image):
    """Test using shared fixture."""
    # test_image is automatically provided
    assert test_image.size == (100, 100)
```

### Parametrized Tests

Test multiple scenarios efficiently:

```python
@pytest.mark.parametrize("device_key", [
    "kindle_paperwhite_11",
    "ipad_pro_11",
])
def test_multiple_devices(device_key):
    device = DeviceSpecs.get_device(device_key)
    assert device is not None
```

## Test Coverage Goals

Current coverage targets:

- **Overall**: 80%+
- **Core modules** (devices, pipeline, presets): 90%+
- **Processing steps**: 85%+

## Continuous Integration

Tests run automatically on:
- Every pull request
- Every push to main
- Scheduled daily runs

See `.github/workflows/test.yml` for CI configuration.

## Best Practices

1. **Test Naming**: Use descriptive names starting with `test_`
2. **One Assertion Per Test**: Focus each test on one behavior
3. **AAA Pattern**: Arrange, Act, Assert
4. **Fixtures Over Setup**: Use pytest fixtures instead of setUp/tearDown
5. **Parametrize**: Use `@pytest.mark.parametrize` for similar tests
6. **Mark Slow Tests**: Use `@pytest.mark.slow` for slow integration tests
7. **Docstrings**: Add docstrings explaining what each test verifies

## Troubleshooting

### Import Errors

If you get import errors, ensure you're running from the project root:

```bash
cd /home/esoso/ShiroInk
pytest
```

### Fixture Not Found

Ensure `conftest.py` is in the `tests/` directory and contains your fixtures.

### Test Discovery Issues

Ensure all test files match the pattern `test_*.py` and all test functions start with `test_`.
