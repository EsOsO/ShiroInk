# CI/CD Pipeline Documentation

## Overview

ShiroInk uses GitHub Actions for continuous integration and continuous deployment. The CI/CD pipeline ensures code quality, runs comprehensive tests, and validates Docker builds.

## Workflows

### 1. Test and Lint (`test.yml`)

**Triggers:**
- Pull requests to `main`
- Pushes to `main`
- Daily scheduled runs at 6 AM UTC

**Jobs:**

#### `test`
Runs comprehensive test suite across multiple Python versions and operating systems.

**Matrix:**
- Python versions: 3.11, 3.12, 3.13
- Operating systems: Ubuntu (all versions), macOS (3.13 only), Windows (3.13 only)

**Steps:**
1. **Checkout code**
2. **Setup Python** with pip caching
3. **Install dependencies** from requirements.txt and dev dependencies
4. **Lint with flake8** - Syntax errors and style warnings
5. **Check formatting** with black
6. **Type check** with mypy (non-blocking)
7. **Run unit tests** with coverage
8. **Run integration tests** with coverage
9. **Upload coverage** to Codecov (Python 3.13 on Ubuntu only)
10. **Upload HTML coverage report** as artifact
11. **Check coverage threshold** (70% minimum)

#### `test-device-presets`
Tests all device preset functionality.

**Steps:**
1. Test `--list-devices` command
2. Test device preset selection (Kindle, PocketBook Color, iPad)
3. Test device/resolution conflict validation
4. Run device-specific unit tests

#### `lint-dockerfile`
Lints the Dockerfile using hadolint.

#### `docker-build-test`
Tests Docker image build and functionality.

**Steps:**
1. Build Docker image with BuildKit caching
2. Test basic functionality (`--help`)
3. Test all 11 pipeline presets
4. Test device preset listing

#### `test-summary`
Aggregates test results from all jobs and reports overall status.

## Coverage Reporting

### Configuration

Coverage is configured in `.coveragerc`:
- **Source:** `src/` directory
- **Omit:** Tests, `__init__.py`, virtual environments
- **Branch coverage:** Enabled
- **Threshold:** 70% minimum
- **Formats:** Terminal, XML (Codecov), HTML (artifact)

### Viewing Coverage

#### Locally
```bash
# Run tests with coverage
pytest --cov=src --cov-report=html

# Open HTML report
open htmlcov/index.html
```

#### CI/CD
- **Codecov:** Coverage reports uploaded to Codecov for tracking over time
- **Artifacts:** HTML coverage reports stored as GitHub Actions artifacts (30-day retention)

## Pre-commit Hooks

Pre-commit hooks ensure code quality before commits.

### Installation

```bash
pip install pre-commit
pre-commit install
```

### Hooks

1. **trailing-whitespace** - Remove trailing whitespace
2. **end-of-file-fixer** - Ensure files end with newline
3. **check-yaml** - Validate YAML syntax
4. **check-added-large-files** - Prevent large file commits (>1MB)
5. **check-merge-conflict** - Detect merge conflict markers
6. **check-toml** - Validate TOML syntax
7. **debug-statements** - Detect debug statements
8. **mixed-line-ending** - Ensure consistent line endings
9. **black** - Auto-format Python code
10. **flake8** - Lint Python code
11. **mypy** - Type check Python code
12. **pytest** - Run unit tests

### Running Manually

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
```

## Test Organization

### Test Types

1. **Unit Tests** (`tests/unit/`)
   - Fast, isolated component tests
   - Run on every commit
   - Target: 90%+ coverage for core modules

2. **Integration Tests** (`tests/integration/`)
   - End-to-end workflow tests
   - Run on every commit
   - Validate complete feature functionality

3. **Device Preset Tests**
   - Dedicated job for device preset validation
   - Tests all 19 device configurations
   - Validates CLI behavior

4. **Docker Tests**
   - Validates Docker build process
   - Tests Docker image functionality
   - Validates all pipeline and device presets

### Test Execution Order

```
1. Lint & Format Checks (fast fail)
   ↓
2. Type Checking (non-blocking)
   ↓
3. Unit Tests (parallel across Python versions)
   ↓
4. Integration Tests (parallel across Python versions)
   ↓
5. Device Preset Tests
   ↓
6. Docker Build & Tests
   ↓
7. Test Summary & Status Report
```

## Continuous Deployment

### Release Process

Releases are managed by Release Please (see `.github/workflows/release-please.yml`):

1. **Commit Convention:** Follow Conventional Commits
2. **PR Creation:** Release Please creates PR with changelog
3. **Merge:** Merging the PR triggers release
4. **GitHub Release:** Automatically created with notes
5. **Docker Build:** Triggered by release (see `build-and-push-image.yml`)

### Docker Image Publishing

**Trigger:** New GitHub release

**Steps:**
1. Build multi-platform image (linux/amd64, linux/arm64)
2. Tag with version and `latest`
3. Push to GitHub Container Registry (ghcr.io)

## Status Badges

Add to README.md:

```markdown
![Tests](https://github.com/EsOsO/ShiroInk/actions/workflows/test.yml/badge.svg)
![Coverage](https://codecov.io/gh/EsOsO/ShiroInk/branch/main/graph/badge.svg)
![Docker](https://github.com/EsOsO/ShiroInk/actions/workflows/build-and-push-image.yml/badge.svg)
```

## Troubleshooting CI/CD

### Tests Failing Locally But Passing in CI

**Cause:** Different Python version or dependencies

**Solution:**
```bash
# Use same Python version as CI
pyenv install 3.13
pyenv local 3.13

# Install exact dependencies
pip install -r requirements.txt
pip install -e ".[dev]"
```

### Coverage Threshold Not Met

**Cause:** New code not covered by tests

**Solution:**
```bash
# Check which lines are missing coverage
pytest --cov=src --cov-report=term-missing

# Add tests for uncovered code
```

### Docker Build Failing

**Cause:** Missing files or incorrect Dockerfile

**Solution:**
```bash
# Test Docker build locally
docker build -t shiroink:test .
docker run --rm shiroink:test --help

# Check .dockerignore
cat .dockerignore
```

### Pre-commit Hooks Failing

**Cause:** Code doesn't meet style guidelines

**Solution:**
```bash
# Auto-fix formatting
black src/

# Check lint errors
flake8 src/

# Run all hooks
pre-commit run --all-files
```

## Performance Optimization

### CI/CD Speed Improvements

1. **Pip Caching:** GitHub Actions caches pip packages
2. **Docker BuildKit:** Layer caching for faster Docker builds
3. **Parallel Jobs:** Tests run in parallel across Python versions
4. **Fail Fast:** Disabled to see all test results
5. **Selective Coverage Upload:** Only Python 3.13 on Ubuntu uploads to Codecov

### Test Speed Improvements

1. **Test Markers:** Use `pytest -m unit` to run only fast tests during development
2. **Fixtures:** Shared fixtures reduce setup time
3. **Parametrization:** Efficient multi-scenario testing

## Monitoring

### GitHub Actions

- **Dashboard:** https://github.com/EsOsO/ShiroInk/actions
- **Workflow runs:** View all test runs and results
- **Artifacts:** Download coverage reports

### Codecov

- **Dashboard:** https://codecov.io/gh/EsOsO/ShiroInk
- **Trends:** Track coverage over time
- **Pull Request Comments:** Automatic coverage reports on PRs

## Security

### Secrets

Required GitHub secrets:
- `CODECOV_TOKEN` - Codecov upload token (optional but recommended)

### Dependency Scanning

Dependabot is configured to:
- Check for security vulnerabilities
- Update dependencies automatically
- Create PRs for updates

See `.github/dependabot.yml` for configuration.
