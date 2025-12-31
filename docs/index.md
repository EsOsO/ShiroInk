# ShiroInk Documentation

Welcome to the **ShiroInk** documentation! ShiroInk is a powerful manga and comic book image optimization tool designed to prepare images for e-readers, tablets, and printing.

## What is ShiroInk?

ShiroInk processes manga and comic book images with configurable pipelines to:

- **Resize** images to optimal resolutions for different devices
- **Optimize** image quality and file size
- **Enhance** contrast and sharpness
- **Quantize** colors for better e-reader display
- **Process** CBZ archives automatically

## Features

### 🎨 Configurable Processing Pipelines

Choose from 5 built-in presets or create your own:

- **Kindle**: Optimized for e-readers (default)
- **Tablet**: Perfect for iPad and Android tablets
- **Print**: High-quality for printing
- **High Quality**: Maximum quality preservation
- **Minimal**: Light processing

### 🚀 Performance

- Multi-threaded processing
- Batch processing support
- CBZ archive support
- Dry-run mode for testing

### 🔧 Flexible Configuration

- Custom resolutions
- Quality levels (1-9)
- RTL (right-to-left) support for manga
- Debug mode
- Continue-on-error option

### 🐳 Docker Support

- Multi-platform images (amd64, arm64)
- Pre-built containers on GitHub Container Registry
- Docker Compose configurations

## Quick Start

### Using Docker

```bash
docker pull ghcr.io/esoso/shiroink:latest

docker run --rm \
  -v ./input:/input:ro \
  -v ./output:/output \
  ghcr.io/esoso/shiroink:latest \
  /input /output --pipeline kindle
```

### Using Python

```bash
pip install -r requirements.txt
python src/main.py input/ output/ --pipeline tablet
```

## Architecture Highlights

ShiroInk v2.0.0 features a completely redesigned architecture:

- **ProcessingConfig Dataclass**: Simplified configuration management
- **ProgressReporter Abstraction**: Testable progress tracking
- **Configurable Pipelines**: Strategy pattern for extensibility
- **Comprehensive Error Handling**: Retry logic and error tracking

See the [Architecture Overview](architecture/overview.md) for details.

## CI/CD & DevOps

ShiroInk includes enterprise-grade CI/CD:

- Automated testing on every PR
- Multi-platform Docker builds
- Vulnerability scanning with Trivy
- Automatic semantic versioning with Release Please
- Comprehensive test coverage

Learn more in the [CI/CD section](cicd/implementation.md).

## Version

Current version: **2.0.0**

See the [releases page](https://github.com/EsOsO/ShiroInk/releases) for changelog.

## License

ShiroInk is licensed under the ISC License.

## Getting Help

- 📖 Read the [Usage Guide](guides/usage.md)
- 🐳 Check the [Docker Guide](guides/docker.md)
- 🐛 Report issues on [GitHub](https://github.com/EsOsO/ShiroInk/issues)
- 💡 See [Contributing Guidelines](contributing/conventional-commits.md)

## Navigation

Use the navigation menu on the left to explore:

- **Getting Started**: Installation and usage guides
- **Architecture**: Deep dive into system design
- **CI/CD**: DevOps and automation details
- **Contributing**: How to contribute to ShiroInk
- **API Reference**: Code-level documentation
