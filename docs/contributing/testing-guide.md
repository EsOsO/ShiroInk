# Testing Quick Reference

## Quick Start

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## Common Test Commands

### Run Specific Test Categories

```bash
# Unit tests only (fast)
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_devices.py

# Specific test class
pytest tests/unit/test_devices.py::TestDeviceSpecFields

# Specific test function
pytest tests/unit/test_devices.py::TestDeviceSpecFields::test_all_devices_have_name

# Tests matching pattern
pytest -k "device"
```

### Test Output Control

```bash
# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Run last failed tests
pytest --lf

# Run only failed tests from last run
pytest --ff
```

### Coverage Commands

```bash
# Basic coverage
pytest --cov=src

# Coverage with missing lines
pytest --cov=src --cov-report=term-missing

# HTML coverage report
pytest --cov=src --cov-report=html

# XML coverage for CI
pytest --cov=src --cov-report=xml

# Check coverage threshold
pytest --cov=src --cov-fail-under=70
```

### Test Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Pre-commit Hooks

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run all hooks manually
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
pre-commit run flake8 --all-files
pre-commit run pytest-check --all-files

# Skip hooks for a commit (not recommended)
git commit --no-verify
```

## Code Quality Checks

### Formatting

```bash
# Check formatting (don't modify)
black --check src/

# Auto-format code
black src/

# Format specific file
black src/main.py
```

### Linting

```bash
# Lint all code
flake8 src/

# Lint with statistics
flake8 src/ --statistics

# Lint specific file
flake8 src/main.py
```

### Type Checking

```bash
# Type check all code
mypy src/ --ignore-missing-imports

# Type check specific file
mypy src/main.py --ignore-missing-imports
```

## Writing Tests

### Test Structure

```python
class TestFeatureName:
    """Test suite for feature."""
    
    def test_specific_behavior(self):
        """Test one specific behavior."""
        # Arrange - Set up test data
        input_value = 10
        
        # Act - Execute the code
        result = my_function(input_value)
        
        # Assert - Verify results
        assert result == expected_value
```

### Using Fixtures

```python
def test_with_fixture(test_image):
    """Use shared fixture from conftest.py."""
    assert test_image.size == (100, 100)


def test_with_temp_dir(tmp_path):
    """Use pytest's built-in tmp_path fixture."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")
    assert test_file.read_text() == "content"
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_multiply_by_two(input, expected):
    """Test with multiple input/output pairs."""
    assert input * 2 == expected
```

### Testing Exceptions

```python
def test_raises_error():
    """Test that function raises expected error."""
    with pytest.raises(ValueError):
        my_function(invalid_input)
```

## Available Fixtures

From `tests/conftest.py`:

- `test_image` - Simple RGB test image (100x100)
- `test_grayscale_image` - Grayscale test image (100x100)
- `test_color_image` - Colorful test image with gradients
- `silent_reporter` - SilentProgressReporter for testing
- `error_tracker` - ErrorTracker for testing
- `test_config` - ProcessingConfig with temp directories
- `sample_images` - Directory with sample PNG files

Pytest built-in fixtures:

- `tmp_path` - Temporary directory (Path object)
- `tmpdir` - Temporary directory (py.path.local object)
- `capsys` - Capture stdout/stderr
- `monkeypatch` - Modify objects/dicts/environment variables

## Debugging Tests

### Print Debugging

```bash
# Show print statements
pytest -s tests/unit/test_devices.py

# Use in test
def test_debug():
    print(f"Debug: {variable}")
    assert True
```

### PDB Debugging

```bash
# Drop into debugger on failure
pytest --pdb

# Use in test
def test_debug():
    import pdb; pdb.set_trace()
    assert True
```

### Verbose Output

```bash
# Show all test names and results
pytest -v

# Show local variables on failure
pytest -l

# Show full diff on assertion failures
pytest -vv
```

## CI/CD Integration

### Local CI Simulation

```bash
# Run exactly what CI runs
pip install -r requirements.txt
pip install -e ".[dev]"
pip install flake8 mypy black

# Linting
flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 src/ --count --exit-zero --max-line-length=88 --statistics

# Formatting
black --check src/

# Type checking
mypy src/ --ignore-missing-imports --no-strict-optional

# Unit tests
pytest tests/unit/ -v --cov=src --cov-report=term-missing

# Integration tests
pytest tests/integration/ -v

# Coverage threshold
coverage report --fail-under=70
```

### Viewing CI Results

- **GitHub Actions:** https://github.com/EsOsO/ShiroInk/actions
- **Coverage:** https://codecov.io/gh/EsOsO/ShiroInk
- **Artifacts:** Click on workflow run → Artifacts → coverage-report

## Tips

### Speed Up Tests

```bash
# Run in parallel (requires pytest-xdist)
pip install pytest-xdist
pytest -n auto

# Run only modified tests
pytest --testmon

# Use markers to skip slow tests
pytest -m "not slow"
```

### Clean Test Environment

```bash
# Remove cache
pytest --cache-clear

# Remove coverage data
rm -rf .coverage htmlcov/

# Remove all __pycache__
find . -type d -name __pycache__ -exec rm -rf {} +
```

### Test Coverage Goals

- Overall: 70%+ (CI enforced)
- Core modules (devices, pipeline, presets): 90%+
- Processing steps: 85%+
- New code: 80%+

## Common Issues

### Import Errors

```bash
# Ensure you're in project root
cd /path/to/ShiroInk

# Install in editable mode
pip install -e .

# Set PYTHONPATH if needed
export PYTHONPATH=$PWD/src
```

### Fixture Not Found

Ensure `conftest.py` exists in `tests/` directory and contains your fixtures.

### Tests Pass Locally But Fail in CI

Check Python version matches CI:
```bash
python --version  # Should be 3.11, 3.12, or 3.13
```

### Coverage Below Threshold

```bash
# See which lines are uncovered
pytest --cov=src --cov-report=term-missing

# Focus on uncovered code
pytest --cov=src --cov-report=html
open htmlcov/index.html
```
