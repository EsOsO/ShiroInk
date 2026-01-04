# Conventional Commits - Quick Reference

## Version Bumping Rules

### ✅ BUMPS VERSION (Code Changes)

```bash
feat:      # New feature        → MINOR (0.x.0)
fix:       # Bug fix            → PATCH (0.0.x)
perf:      # Performance        → PATCH (0.0.x)
refactor:  # Code refactoring   → PATCH (0.0.x)
deps:      # Dependencies       → PATCH (0.0.x)
build:     # Build system       → PATCH (0.0.x)
revert:    # Revert commit      → PATCH (0.0.x)

feat!:     # Breaking change    → MAJOR (x.0.0)
fix!:      # Breaking fix       → MAJOR (x.0.0)
```

### ❌ NO VERSION BUMP (Non-Code Changes)

```bash
docs:      # Documentation
test:      # Tests
ci:        # CI/CD pipelines
style:     # Formatting
chore:     # Config files
```

## Quick Examples

```bash
# Add new feature (MINOR bump: 2.0.0 → 2.1.0)
git commit -m "feat: add device preset for Kobo"

# Fix bug (PATCH bump: 2.0.0 → 2.0.1)
git commit -m "fix: resolve image rotation issue"

# Update docs (NO bump)
git commit -m "docs: update README"

# Add tests (NO bump)
git commit -m "test: add device preset tests"

# Update CI (NO bump)
git commit -m "ci: add coverage reporting"

# Breaking change (MAJOR bump: 2.0.0 → 3.0.0)
git commit -m "feat!: change default pipeline"
```

## Excluded Paths (Never Bump Version)

- `docs/**`
- `tests/**`
- `.github/workflows/**`
- `*.md`
- `.pre-commit-config.yaml`
- `.coveragerc`
- `pytest.ini`

## Cheat Sheet

| What Changed? | Commit Type | Version Bump |
|---------------|-------------|--------------|
| New feature in `src/` | `feat:` | MINOR |
| Bug fix in `src/` | `fix:` | PATCH |
| Performance improvement | `perf:` | PATCH |
| Code refactoring | `refactor:` | PATCH |
| README update | `docs:` | **NONE** |
| Test update | `test:` | **NONE** |
| CI workflow update | `ci:` | **NONE** |
| Breaking API change | `feat!:` | MAJOR |

## Full Specification

See [CONVENTIONAL_COMMITS.md](.github/CONVENTIONAL_COMMITS.md)
