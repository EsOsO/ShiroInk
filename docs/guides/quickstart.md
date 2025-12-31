# Quick Start

Get up and running with ShiroInk in 5 minutes!

## Docker Quick Start

```bash
# Pull the image
docker pull ghcr.io/esoso/shiroink:latest

# Process your manga
docker run --rm \
  -v ./my-manga:/input:ro \
  -v ./optimized:/output \
  ghcr.io/esoso/shiroink:latest \
  /input /output --pipeline kindle
```

## What Just Happened?

ShiroInk processed all images in `./my-manga` and saved optimized versions to `./optimized` using the Kindle preset.

## Try Different Presets

```bash
# For tablets
docker run --rm -v ./input:/input:ro -v ./output:/output \
  ghcr.io/esoso/shiroink:latest /input /output --pipeline tablet

# For printing
docker run --rm -v ./input:/input:ro -v ./output:/output \
  ghcr.io/esoso/shiroink:latest /input /output --pipeline print
```

## Next Steps

- [Full Usage Guide](usage.md) - All options and features
- [Docker Guide](docker.md) - Advanced Docker usage
- [Architecture](../architecture/overview.md) - How it works
