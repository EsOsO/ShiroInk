# Security Scanning Guide

This document explains how GitHub Security scanning works in ShiroInk and how to address alerts.

## Overview

ShiroInk uses **Trivy** (open-source vulnerability scanner) to scan Docker images for security vulnerabilities. Scans run automatically on every Docker image build and publish results to GitHub Security tab.

## Current Configuration

**Workflow**: `.github/workflows/build-and-push-image.yml`

```yaml
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/esoso/shiroink@${{ steps.push.outputs.digest }}
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'  # Only scan for critical/high severity
```

**What gets scanned**:
- Base OS packages (Alpine Linux)
- Python runtime and dependencies
- Application dependencies (Pillow, Rich, etc.)

## Viewing Security Alerts

1. Go to: https://github.com/EsOsO/ShiroInk/security/code-scanning
2. Filter by severity: Critical, High, Medium, Low, Warning, Note
3. Click individual alerts for details

**CLI method**:
```bash
# View all alerts
gh api repos/EsOsO/ShiroInk/code-scanning/alerts

# View only warnings
gh api repos/EsOsO/ShiroInk/code-scanning/alerts --jq '.[] | select(.rule.severity == "warning")'
```

## Addressing Security Alerts

### Option 1: Update Base Image (Recommended)

Most vulnerabilities come from the base Docker image. Update to latest:

```dockerfile
# In Dockerfile
FROM python:3.13-alpine  # Change to: python:3.13-alpine3.21 (latest)
```

Then rebuild:
```bash
docker build -t shiroink:test .
```

### Option 2: Suppress False Positives

Use `.trivyignore` file to suppress alerts that don't affect ShiroInk:

**Already configured** in `.trivyignore`:
- Old CVEs from base OS (2005-2011 era) - not exploitable in containers
- util-linux vulnerabilities - ShiroInk doesn't manage users
- OpenSSL SM2/KEK vulnerabilities - ShiroInk doesn't use these crypto operations

**To add more suppressions**:
```bash
# Edit .trivyignore
echo "CVE-2025-XXXXX" >> .trivyignore
```

### Option 3: Accept Risk & Document

For vulnerabilities that are:
- Not exploitable in containerized environment
- In dependencies not used by ShiroInk
- Awaiting upstream patches

**Document in this file** why they're acceptable:
```markdown
## Accepted Risks

### CVE-2025-XXXXX (Severity: HIGH)
- **Component**: util-linux
- **Why Accepted**: ShiroInk doesn't use user management features
- **Mitigated By**: Container runs as non-root, no shell access
- **Review Date**: 2026-01-05
```

### Option 4: Update Dependencies

For Python package vulnerabilities:

```bash
# Check outdated packages
pip list --outdated

# Update specific package
pip install --upgrade pillow

# Update requirements.txt
pip freeze > requirements.txt
```

Then rebuild Docker image.

## Common Vulnerabilities & Solutions

### 1. pip CVE-2025-8869 (Symbolic Link Extraction)

**Status**: WARNING
**Impact**: Low (pip only used during build, not runtime)
**Solution**:
```dockerfile
# Update pip during build
RUN pip install --upgrade pip>=25.2.1
```

### 2. util-linux CVE-2025-14104 (Heap Buffer Overread)

**Status**: WARNING
**Impact**: None (ShiroInk doesn't use setpwnam())
**Solution**: Suppressed in `.trivyignore` (false positive for our use case)

### 3. OpenSSL CVEs (2025-9230, 2025-9231)

**Status**: WARNING  
**Impact**: None (ShiroInk doesn't use SM2 or KEK operations)
**Solution**: Suppressed in `.trivyignore` (not applicable)

## Best Practices

### 1. Regular Updates

Update base image monthly:
```bash
# Check for updates
docker pull python:3.13-alpine

# Rebuild with latest
docker build --no-cache -t shiroink:latest .
```

### 2. Minimize Attack Surface

Current Dockerfile already follows best practices:
- ✅ Uses Alpine Linux (minimal base)
- ✅ Multi-stage build (smaller final image)
- ✅ Runs as non-root user
- ✅ Only installs required dependencies

### 3. Pin Dependency Versions

In `requirements.txt`:
```txt
pillow>=11.3.0,<12.0.0  # Pin major version
rich>=14.1.0,<15.0.0
```

### 4. Review Alerts Regularly

**Schedule**: Review security alerts monthly
```bash
# Check current status
gh api repos/EsOsO/ShiroInk/code-scanning/alerts --jq '.[] | select(.state == "open") | .rule.severity' | sort | uniq -c
```

## Trivy Configuration Options

### Adjust Severity Threshold

In `.github/workflows/build-and-push-image.yml`:

```yaml
# Currently scans: CRITICAL,HIGH
severity: 'CRITICAL,HIGH,MEDIUM'  # Add MEDIUM severity

# Scan everything (not recommended - too noisy)
severity: 'CRITICAL,HIGH,MEDIUM,LOW,UNKNOWN'
```

### Scan Specific Vulnerability Types

```yaml
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/esoso/shiroink@${{ steps.push.outputs.digest }}
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'
    vuln-type: 'os,library'  # Scan both OS packages and libraries
    ignore-unfixed: true     # Ignore vulnerabilities without fixes
```

### Use Trivy Config File

Create `.trivy.yaml`:
```yaml
severity:
  - CRITICAL
  - HIGH

ignore-unfixed: true

# Ignore specific paths
skip-dirs:
  - tests/
  - docs/
```

## Dismissing Alerts in GitHub

**Via GitHub UI**:
1. Go to Security → Code scanning
2. Click alert
3. Click "Dismiss alert" → Select reason:
   - Won't fix (accepted risk)
   - False positive
   - Used in tests (not production)

**Via API**:
```bash
# Dismiss specific alert
gh api -X PATCH repos/EsOsO/ShiroInk/code-scanning/alerts/71 \
  -f state=dismissed \
  -f dismissed_reason="won't fix" \
  -f dismissed_comment="Not exploitable in containerized environment"
```

## Testing Locally

Run Trivy scan locally before pushing:

```bash
# Build image
docker build -t shiroink:test .

# Scan with Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest image \
  --severity CRITICAL,HIGH \
  --ignore-unfixed \
  shiroink:test

# Use .trivyignore
docker run --rm \
  -v $(pwd)/.trivyignore:/.trivyignore \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest image \
  --severity CRITICAL,HIGH \
  --ignorefile /.trivyignore \
  shiroink:test
```

## Resources

- **Trivy Documentation**: https://aquasecurity.github.io/trivy/
- **GitHub Code Scanning**: https://docs.github.com/en/code-security/code-scanning
- **CVE Database**: https://cve.mitre.org/
- **NVD (National Vulnerability Database)**: https://nvd.nist.gov/

## Current Status

Last reviewed: 2026-01-04
- Total alerts: 71
- Critical: 0
- High: 0  
- Warning: 9
- Note: 62

**Action Required**: Review pip CVE-2025-8869 and update if necessary.
