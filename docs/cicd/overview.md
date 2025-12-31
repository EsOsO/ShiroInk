# CI/CD Overview - ShiroInk

## Current Status

**Last Updated**: 2025-12-31  
**Latest Version**: v2.0.9  
**Status**: ✅ Production Ready

---

## Automation Pipeline

ShiroInk uses a fully automated CI/CD pipeline powered by GitHub Actions with the following components:

### 1. Automated Releases (Release Please)

**Workflow**: `.github/workflows/release-please.yml`

- **Triggers**: Every push to `main` branch
- **Actions**:
  - Analyzes commits using Conventional Commits
  - Creates/updates release PR with version bump and changelog
  - When PR is merged: creates GitHub release with tag
  - Automatically triggers Docker image build

**Version Management**:
- Single source of truth: `pyproject.toml`
- Follows Semantic Versioning (SemVer)
- Auto-updates CHANGELOG.md

**Release Types**:
- `fix:` → Patch release (2.0.X)
- `feat:` → Minor release (2.X.0)
- `feat!:` or `BREAKING CHANGE:` → Major release (X.0.0)

### 2. Docker Image Publishing

**Workflow**: `.github/workflows/build-and-push-image.yml`

- **Triggers**:
  - Automatically after each release (via `workflow_call`)
  - Manually via `workflow_dispatch`
  - On version tags (`v*.*.*`)

- **Build Features**:
  - Multi-platform: `linux/amd64` + `linux/arm64`
  - Multi-stage build (optimized size: ~245MB)
  - GitHub Actions build cache (40% faster builds)
  - Non-root user execution (UID 1000)

- **Security Features**:
  - Trivy vulnerability scanning (CRITICAL + HIGH)
  - SARIF upload to GitHub Security tab
  - Artifact attestation (supply chain security)
  - Digest-pinned base images

- **Image Tags** (7 variants):
  ```
  ghcr.io/esoso/shiroink:2.0.9     # Exact version
  ghcr.io/esoso/shiroink:v2.0.9    # Exact version with v prefix
  ghcr.io/esoso/shiroink:2.0       # Major.minor
  ghcr.io/esoso/shiroink:v2.0      # Major.minor with v prefix
  ghcr.io/esoso/shiroink:2         # Major version
  ghcr.io/esoso/shiroink:v2        # Major version with v prefix
  ghcr.io/esoso/shiroink:latest    # Latest release
  ```

### 3. Pull Request Validation

**Workflow**: `.github/workflows/test.yml`

- **Triggers**: All PRs to `main` + pushes to `main`

- **Test Matrix**: Python 3.11, 3.12, 3.13

- **Quality Checks**:
  - **Flake8**: Syntax errors, undefined names
  - **Black**: Code formatting validation
  - **MyPy**: Type checking (non-blocking)
  - **Pytest**: Unit tests with coverage
  - **Codecov**: Coverage reporting
  - **Hadolint**: Dockerfile linting
  - **Docker Build Test**: Validates all 5 pipeline presets

### 4. Documentation Deployment

**Workflow**: `.github/workflows/docs.yml`

- **Triggers**: 
  - Changes to `docs/**` on `main`
  - Changes to `mkdocs.yml`
  - Manual dispatch

- **Actions**:
  - Builds documentation with MkDocs Material theme
  - Deploys to GitHub Pages
  - Accessible at: https://esoso.github.io/ShiroInk/

### 5. Dependency Management

**Configuration**: `.github/dependabot.yml`

- **Weekly Updates** (Mondays 09:00 UTC):
  - Python packages (pip)
  - Docker base images
  - GitHub Actions versions

- **Automated PRs**:
  - Auto-created with test validation
  - Labeled appropriately
  - Security updates prioritized

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  Developer commits code with conventional commit message    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Release Please Workflow                                    │
│  - Analyzes commits                                         │
│  - Creates/updates release PR                               │
│  - Updates version in pyproject.toml                        │
│  - Updates CHANGELOG.md                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Maintainer merges release PR                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Release Please creates GitHub release (e.g., v2.0.9)       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Docker Build Workflow (automatic)                          │
│  ├─ Checkout code at release tag                            │
│  ├─ Build multi-platform image (amd64 + arm64)              │
│  ├─ Push to ghcr.io with all 7 tag variants                 │
│  ├─ Run Trivy security scan                                 │
│  ├─ Upload results to Security tab                          │
│  └─ Generate artifact attestation                           │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Images available at ghcr.io/esoso/shiroink                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Release Process

### Automatic Release Flow

1. **Developer**: Commit with conventional commit message
   ```bash
   git commit -m "feat: add new processing option"
   git push origin main
   ```

2. **Release Please**: Analyzes and creates release PR
   - Bumps version (feat → 2.X.0)
   - Updates CHANGELOG.md
   - Updates pyproject.toml

3. **Maintainer**: Reviews and merges release PR
   ```bash
   gh pr merge <number> --squash
   ```

4. **Release Please**: Creates GitHub release with tag
   - Tag: `v2.X.0`
   - Release notes from CHANGELOG

5. **Docker Build**: Automatically triggered
   - Builds and pushes images
   - Scans for vulnerabilities
   - Generates attestations

6. **Users**: Pull new version
   ```bash
   docker pull ghcr.io/esoso/shiroink:latest
   docker pull ghcr.io/esoso/shiroink:v2.X.0
   ```

### Manual Release (if needed)

```bash
# Create tag manually
git tag v2.X.Y
git push origin v2.X.Y

# This triggers Docker build workflow directly
```

---

## Version Detection

ShiroInk automatically detects its version using a hierarchical approach:

1. **If installed as package**: Reads from `importlib.metadata`
2. **Fallback**: Reads from `pyproject.toml` directly
3. **Used by**: `--version` CLI flag and Docker image metadata

**Example**:
```bash
# Local installation
$ python src/main.py --version
ShiroInk 2.0.9

# Docker container
$ docker run --rm ghcr.io/esoso/shiroink:latest --version
ShiroInk 2.0.9
```

---

## Security Features

### 1. Vulnerability Scanning
- **Tool**: Trivy (Aqua Security)
- **Scan Targets**: Container images
- **Severity Levels**: CRITICAL, HIGH
- **Results**: Uploaded to GitHub Security tab

### 2. Supply Chain Security
- **Artifact Attestations**: SLSA provenance
- **SHA-pinned Actions**: Prevents supply chain attacks
- **Digest-pinned Images**: Immutable base images
- **Dependabot**: Automated security updates

### 3. Access Control
- **Non-root Execution**: UID 1000 in containers
- **Minimal Permissions**: Least privilege in workflows
- **No Hardcoded Secrets**: Uses GitHub tokens only

---

## Performance Metrics

### Build Times
- **Without cache**: ~60 seconds
- **With cache**: ~36 seconds
- **Multi-platform**: ~90 seconds total

### Test Times
- **Per Python version**: ~2-3 minutes
- **Total (3 versions)**: ~6-9 minutes (parallel)
- **Docker build test**: ~30 seconds

### Image Metrics
- **Size**: 245MB (optimized)
- **Layers**: 14 (multi-stage build)
- **Platforms**: 2 (amd64, arm64)

---

## Monitoring & Observability

### GitHub Actions
- **Workflow runs**: https://github.com/EsOsO/ShiroInk/actions
- **Release history**: https://github.com/EsOsO/ShiroInk/releases
- **Security alerts**: https://github.com/EsOsO/ShiroInk/security

### Container Registry
- **Package page**: https://github.com/EsOsO/ShiroInk/pkgs/container/shiroink
- **All tags**: Available on package page
- **Pull stats**: Visible on package page

### Coverage Reports
- **Codecov**: Integrated with PR checks
- **Coverage trend**: Tracked over time
- **Target**: >80% coverage

---

## Troubleshooting

### Release Please Not Creating PR

**Possible causes**:
- No conventional commits since last release
- Commits don't trigger version bump (e.g., `docs:`, `chore:`)

**Solution**:
```bash
# Check recent commits
git log --oneline -10

# Add a feat or fix commit to trigger release
git commit -m "fix: minor improvement" --allow-empty
git push origin main
```

### Docker Build Failing

**Check**:
1. Workflow logs: https://github.com/EsOsO/ShiroInk/actions
2. Trivy scan results in Security tab
3. Build cache issues (clear with workflow_dispatch)

**Common fixes**:
- Clear GitHub Actions cache
- Rebuild base image
- Check Dockerfile syntax

### Version Not Updating in Container

**Verify**:
```bash
# Check pyproject.toml was copied
docker run --rm ghcr.io/esoso/shiroink:latest python -c "import toml; print(toml.load('/app/pyproject.toml')['project']['version'])"

# Check __version__.py
docker run --rm ghcr.io/esoso/shiroink:latest python -c "import sys; sys.path.insert(0, '/app/src'); from __version__ import __version__; print(__version__)"
```

---

## Best Practices

### For Developers

1. **Always use conventional commits**:
   ```bash
   git commit -m "feat: add feature"
   git commit -m "fix: resolve bug"
   git commit -m "docs: update readme"
   ```

2. **Test locally before pushing**:
   ```bash
   docker build -t shiroink:test .
   docker run --rm shiroink:test --version
   ```

3. **Run tests locally**:
   ```bash
   pytest test_*.py -v
   black --check src/
   flake8 src/
   ```

### For Maintainers

1. **Review release PRs carefully**:
   - Check version bump is correct
   - Review CHANGELOG.md changes
   - Verify all tests pass

2. **Monitor security alerts**:
   - Check Security tab regularly
   - Review Trivy scan results
   - Address vulnerabilities promptly

3. **Manage dependencies**:
   - Review Dependabot PRs weekly
   - Test updates before merging
   - Keep actions up to date

---

## Future Enhancements

### Planned
- [ ] Automated changelog formatting improvements
- [ ] Performance benchmarking in CI
- [ ] Integration tests for full workflow
- [ ] SBOM (Software Bill of Materials) generation

### Under Consideration
- [ ] Signed releases with Sigstore/cosign
- [ ] Performance regression detection
- [ ] Automated rollback on failures
- [ ] Multi-region container registry mirrors

---

## References

- **Release Please**: https://github.com/googleapis/release-please
- **Conventional Commits**: https://www.conventionalcommits.org/
- **Semantic Versioning**: https://semver.org/
- **Trivy Scanner**: https://github.com/aquasecurity/trivy
- **GitHub Actions**: https://docs.github.com/en/actions
- **Docker Multi-platform**: https://docs.docker.com/build/building/multi-platform/

---

**Document Version**: 2.0  
**Last Updated**: 2025-12-31  
**Status**: Current and Accurate ✅
