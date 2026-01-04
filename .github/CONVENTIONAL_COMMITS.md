# Conventional Commits Configuration for ShiroInk

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification.

## Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types and Version Bumping

### Types that BUMP the version:

- **feat**: A new feature → **MINOR** version bump (0.x.0)
- **fix**: A bug fix → **PATCH** version bump (0.0.x)
- **perf**: A performance improvement → **PATCH** version bump (0.0.x)
- **refactor**: Code refactoring (non-breaking) → **PATCH** version bump (0.0.x)
- **revert**: Reverting a previous commit → **PATCH** version bump (0.0.x)
- **deps**: Dependency updates → **PATCH** version bump (0.0.x)
- **build**: Build system changes (affects production) → **PATCH** version bump (0.0.x)
- **Breaking changes** (any type with `!` or `BREAKING CHANGE:`) → **MAJOR** version bump (x.0.0)

### Types that DO NOT bump the version:

- **docs**: Documentation only changes (README, guides, etc.)
- **test**: Adding or updating tests
- **ci**: CI/CD configuration changes (GitHub Actions, etc.)
- **style**: Code style/formatting changes (whitespace, etc.)
- **chore**: Miscellaneous changes (config files, etc.)

> **Important**: Changes to `docs/**`, `tests/**`, `.github/workflows/**`, `*.md`, `.pre-commit-config.yaml`, `.coveragerc`, and `pytest.ini` are automatically excluded from version bumping, regardless of commit type.

## Examples

### Version-bumping commits:

```bash
# New feature → MINOR bump (2.0.0 → 2.1.0)
feat: add device preset for Kobo readers
feat(devices): add support for PocketBook InkPad Color 3

# Bug fix → PATCH bump (2.0.0 → 2.0.1)
fix: correct image rotation for RTL mode
fix(pipeline): resolve memory leak in quantization step

# Performance improvement → PATCH bump (2.0.0 → 2.0.1)
perf: optimize color profile conversion
perf(resize): use faster interpolation algorithm

# Code refactoring → PATCH bump (2.0.0 → 2.0.1)
refactor: simplify error handling logic
refactor(devices): consolidate device spec validation

# Dependency update → PATCH bump (2.0.0 → 2.0.1)
deps: update Pillow to 11.3.0

# Breaking change → MAJOR bump (2.0.0 → 3.0.0)
feat!: change default pipeline to use ColorProfileStep
fix!: remove deprecated --format option

# With BREAKING CHANGE footer → MAJOR bump (2.0.0 → 3.0.0)
feat: redesign device preset API

BREAKING CHANGE: Device presets now use from_device_spec() factory method.
The old device-specific methods (kobo(), tolino(), etc.) are removed.
```

### Non-version-bumping commits:

```bash
# Documentation changes → NO version bump
docs: update README with device preset examples
docs(guides): add ColorProfileStep explanation
docs: fix typo in installation guide

# Test changes → NO version bump
test: add tests for ColorProfileStep
test(devices): add parametrized device validation tests
test: increase coverage for quantize module

# CI/CD changes → NO version bump
ci: add multi-platform testing matrix
ci(workflows): update test.yml for new test structure
ci: add pre-commit hooks configuration

# Style changes → NO version bump
style: format code with black
style: fix flake8 warnings

# Chore changes → NO version bump
chore: update .gitignore
chore: configure coverage reporting
```

## Scopes (Optional)

Use scopes to indicate which part of the codebase is affected:

- `devices` - Device specifications
- `pipeline` - Image processing pipeline
- `presets` - Pipeline presets
- `cli` - Command-line interface
- `docker` - Docker-related changes
- `config` - Configuration files

Example:
```bash
feat(devices): add iPad Pro 11" device preset
fix(pipeline): correct color space conversion
refactor(cli): simplify argument parsing
```

## Breaking Changes

For breaking changes, use either format:

### Option 1: Add `!` after the type

```bash
git commit -m "feat!: change default resolution to 1920x1080"
```

### Option 2: Add `BREAKING CHANGE:` in the footer

```bash
git commit -m "feat: change default resolution

BREAKING CHANGE: The default resolution has changed from 1404x1872 to 1920x1080.
Users relying on the old default should explicitly set --resolution 1404x1872."
```

## Semantic Versioning Summary

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` | MINOR (0.x.0) | 2.0.0 → 2.1.0 |
| `fix:` | PATCH (0.0.x) | 2.0.0 → 2.0.1 |
| `perf:` | PATCH (0.0.x) | 2.0.0 → 2.0.1 |
| `refactor:` | PATCH (0.0.x) | 2.0.0 → 2.0.1 |
| `deps:` | PATCH (0.0.x) | 2.0.0 → 2.0.1 |
| `build:` | PATCH (0.0.x) | 2.0.0 → 2.0.1 |
| `feat!:` or `BREAKING CHANGE:` | MAJOR (x.0.0) | 2.0.0 → 3.0.0 |
| `docs:`, `test:`, `ci:`, `style:`, `chore:` | **NO BUMP** | 2.0.0 → 2.0.0 |

## Release Process

1. **Commit code changes** using conventional commit format
   ```bash
   git commit -m "feat: add new device preset"
   git push origin main
   ```

2. **Release Please monitors commits** and creates/updates a release PR
   - Aggregates all commits since last release
   - Generates CHANGELOG.md
   - Bumps version in `pyproject.toml` and `src/__version__.py`
   - Only includes commits that affect `src/` (excludes docs, tests, CI)

3. **Review the Release PR**
   - Check version bump is correct
   - Review changelog entries
   - Ensure only code changes trigger version bump

4. **Merge the Release PR**
   - Release Please creates GitHub release with tag
   - Changelog is published
   - New version is tagged

5. **Automated Docker Build**
   - Docker workflow triggered by new release
   - Multi-platform image built
   - Published to GitHub Container Registry

## Best Practices

### ✅ DO:
- Use `feat:` for new features
- Use `fix:` for bug fixes
- Use `docs:` for documentation-only changes
- Use `test:` for test-only changes
- Use `ci:` for CI/CD-only changes
- Keep commit messages concise and clear
- Use scopes to indicate affected module
- Add `BREAKING CHANGE:` footer for breaking changes

### ❌ DON'T:
- Don't use `feat:` or `fix:` for non-code changes
- Don't mix code changes with docs/test/CI changes in one commit
- Don't forget to add `!` or `BREAKING CHANGE:` for breaking changes
- Don't use unclear commit messages like "update stuff"

## Examples of Proper Commit Separation

### ❌ BAD (Mixed changes):
```bash
# This would bump version even though it's mostly docs/tests
git commit -m "feat: add device preset and update docs and tests"
```

### ✅ GOOD (Separated commits):
```bash
# Version bump (code change)
git commit -m "feat: add device preset for Kobo Libra 2"

# No version bump (docs)
git commit -m "docs: add Kobo Libra 2 to device preset guide"

# No version bump (tests)
git commit -m "test: add unit tests for Kobo device preset"
```

## Verification

Before committing, ask yourself:

1. **Does this change affect production code?**
   - YES → Use `feat:`, `fix:`, `perf:`, `refactor:`, etc.
   - NO → Use `docs:`, `test:`, `ci:`, `style:`, `chore:`

2. **Where are the file changes?**
   - `src/**` → Version bump
   - `docs/**`, `tests/**`, `.github/**`, `*.md` → No version bump

3. **Is this a breaking change?**
   - YES → Add `!` or `BREAKING CHANGE:`
   - NO → Regular commit

## Tools

### Commitizen
For interactive commit message creation:
```bash
pip install commitizen
cz commit
```

### Commitlint (Pre-commit)
Pre-commit hooks validate commit messages automatically. See `.pre-commit-config.yaml`.

## Questions?

See the [Conventional Commits specification](https://www.conventionalcommits.org/) for more details.
