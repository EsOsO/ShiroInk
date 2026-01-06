# Quick Start

Get up and running with ShiroInk in 5 minutes!

## Interactive Setup (Recommended for New Users)

If you're new to ShiroInk, use the interactive wizard to get started:

```bash
shiroink --wizard
```

The wizard will guide you through:
- Selecting your device
- Choosing input/output directories
- Setting quality preferences
- Saving your configuration as a reusable profile

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

## Save Your Configuration

After running successfully, ShiroInk will ask if you want to save your configuration as a profile:

```bash
shiroink input/ output/ --device kindle_paperwhite_11
# After processing: "Save this configuration as a profile for future use? [Y/n]"
```

Next time, just use:

```bash
shiroink input/ output/ --profile kindle_paperwhite_11
```

## Next Steps

- [Interactive Wizard Guide](wizard.md) - Learn about the setup wizard
- [Profile Management](profiles.md) - Learn about saving and using profiles
- [Full Usage Guide](usage.md) - All options and features
- [Docker Guide](docker.md) - Advanced Docker usage
