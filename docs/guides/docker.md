# Docker Guide

Advanced Docker usage for ShiroInk.

## Using Docker Compose

Create a `docker-compose.yml`:

```yaml
version: '3.8'
services:
  shiroink:
    image: ghcr.io/esoso/shiroink:latest
    volumes:
      - ./input:/input:ro
      - ./output:/output
    command: /input /output --pipeline kindle
```

Run:
```bash
docker-compose run --rm shiroink
```

## Multi-Platform Support

ShiroInk supports both amd64 and arm64 architectures.

## Building Locally

```bash
docker build -t shiroink:local .
docker run --rm shiroink:local --version
```

See the [Installation Guide](installation.md) for more details.
