# Conventional Commits Configuration for ShiroInk

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification.

## Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to our CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit
- **deps**: Dependency updates (usually automated by Dependabot)

## Examples

```
feat: add support for WebP image format
fix: resolve memory leak in image processing pipeline
docs: update README with new pipeline presets
refactor: simplify error handling logic
perf: optimize image resizing algorithm
ci: add multi-platform Docker builds
```

## Breaking Changes

For breaking changes, add `!` after the type or add `BREAKING CHANGE:` in the footer:

```
feat!: change default resolution to 1920x1080

BREAKING CHANGE: The default resolution has changed from 1404x1872 to 1920x1080.
Users relying on the old default should explicitly set --resolution 1404x1872.
```

## Semantic Versioning

Based on commit types, Release Please will automatically:

- **MAJOR** (x.0.0): Breaking changes (commits with `!` or `BREAKING CHANGE`)
- **MINOR** (0.x.0): New features (`feat:`)
- **PATCH** (0.0.x): Bug fixes (`fix:`, `perf:`)

## Release Process

1. Push commits to `main` branch using conventional commit format
2. Release Please creates/updates a PR with changelog and version bump
3. Review and merge the Release Please PR
4. Release Please creates a GitHub release and tag
5. Docker build workflow automatically builds and publishes the container
