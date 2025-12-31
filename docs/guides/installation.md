# Installation

ShiroInk can be installed and run in multiple ways depending on your preference.

## Docker (Recommended)

The easiest way to use ShiroInk is via Docker:

```bash
# Pull the latest image
docker pull ghcr.io/esoso/shiroink:latest

# Verify installation
docker run --rm ghcr.io/esoso/shiroink:latest --version
```

### Multi-Platform Support

ShiroInk Docker images support:

- **linux/amd64** - Intel/AMD processors
- **linux/arm64** - ARM processors (M1/M2 Macs, ARM servers)

Docker will automatically pull the correct image for your architecture.

## Python Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/EsOsO/ShiroInk.git
cd ShiroInk

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation

```bash
python src/main.py --version
```

## Docker Compose

For local development, use Docker Compose:

```bash
# Clone the repository
git clone https://github.com/EsOsO/ShiroInk.git
cd ShiroInk

# Build the image
docker-compose build

# Run with default settings
docker-compose run --rm shiroink
```

## System Requirements

### Minimum

- **CPU**: 2 cores
- **RAM**: 512MB
- **Storage**: 100MB for application, space for processed images

### Recommended

- **CPU**: 4+ cores (for parallel processing)
- **RAM**: 2GB
- **Storage**: SSD for faster processing

## Next Steps

- [Quick Start Guide](quickstart.md) - Get started in 5 minutes
- [Usage Guide](usage.md) - Detailed usage instructions
- [Docker Guide](docker.md) - Advanced Docker usage
