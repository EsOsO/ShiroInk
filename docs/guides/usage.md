# Usage Guide

ShiroInk processes images through a configurable pipeline optimized for e-readers, tablets, and other devices.

## Basic Command

```bash
shiroink <input_directory> <output_directory> [options]
```

## Interactive Wizard

For first-time users or when you need help configuring:

```bash
shiroink --wizard
```

The wizard will guide you through:
- Device selection (with recommendations)
- Directory configuration
- Quality and performance settings
- Saving as a profile for future use

## Profiles

Save and reuse your configurations:

### Save a Profile

```bash
# After running successfully, save your configuration
shiroink input/ output/ --device kindle_paperwhite_11
# "Save this configuration as a profile for future use? [Y/n]"

# Or save explicitly during processing
shiroink input/ output/ --device kindle_paperwhite_11 --save-profile my-kindle
```

### Use a Profile

```bash
shiroink input/ output/ --profile my-kindle
```

### Manage Profiles

```bash
# List all saved profiles
shiroink --list-profiles

# Delete a profile
shiroink --delete-profile old-profile
```

## Pipeline Presets

Choose an optimization profile based on your target device:

### kindle (Default)
Optimized for Amazon Kindle e-ink readers.

```bash
shiroink input/ output/ --pipeline kindle
```

**Best for:**
- E-Ink readers (Kindle, Kobo, PocketBook)
- File size optimization
- High contrast environments

### tablet
Optimized for color LCD displays (iPad, Android tablets).

```bash
shiroink input/ output/ --pipeline tablet
```

**Best for:**
- iPad and Android tablets
- Color preservation
- Modern LCD screens

### high_quality
Maximum quality for archival storage.

```bash
shiroink input/ output/ --pipeline high_quality
```

**Best for:**
- Future-proofing content
- Archive storage
- Printing
- Premium viewing

### minimal
No processing (fast pass-through).

```bash
shiroink input/ output/ --pipeline minimal
```

**Best for:**
- Quick format conversion
- Preserving original quality
- Testing

## Device Presets

ShiroInk includes optimized presets for specific devices:

```bash
# List all available devices
shiroink --list-devices

# Use a specific device (auto-configures resolution and pipeline)
shiroink input/ output/ --device kindle_paperwhite_11
shiroink input/ output/ --device kobo_libra_2
shiroink input/ output/ --device ipad_pro_11
```

## Resolution Settings

Set output dimensions for your target device.

### Default Resolution
Uses device-specific dimensions (automatic).

```bash
shiroink input/ output/
```

### Custom Resolution
Specify exact width and height:

```bash
# Portrait: 1072x1448 (Kindle Paperwhite)
shiroink input/ output/ -r 1072x1448

# Landscape: 1448x1072
shiroink input/ output/ -r 1448x1072

# Square: 1024x1024
shiroink input/ output/ -r 1024x1024

# Shorthand (square): -r 1024
shiroink input/ output/ -r 1024
```

## Quality Settings

Control file size vs. image quality (1-9).

```bash
# Lower quality, smaller files (good for e-ink)
shiroink input/ output/ -q 3

# Default quality (balanced)
shiroink input/ output/ -q 6

# High quality (larger files)
shiroink input/ output/ -q 9
```

## Processing Options

### Right-to-Left Mode
For manga and RTL content:

```bash
shiroink input/ output/ --rtl
```

### Debug Output
Enable detailed logging:

```bash
shiroink input/ output/ --debug
```

Shows:
- Processing steps
- File-by-file progress
- Error details
- Processing time

### Dry Run
Test without saving files:

```bash
shiroink input/ output/ --dry-run
```

Useful for:
- Testing pipeline configuration
- Estimating processing time
- Debugging issues

### Parallel Workers
Control processing speed:

```bash
# Use 2 parallel workers (slower, less memory)
shiroink input/ output/ -w 2

# Use 8 parallel workers (faster, more memory)
shiroink input/ output/ -w 8

# Default: 4 workers
shiroink input/ output/
```

## Practical Examples

### Kindle E-Book Processing

```bash
shiroink ebook_scans/ kindle_output/ \
  --pipeline kindle \
  -r 1072x1448 \
  -q 6
```

### Tablet Viewing

```bash
shiroink comics/ tablet_output/ \
  --pipeline tablet \
  -r 1920x1440 \
  --workers 8
```

### Archive Storage

```bash
shiroink originals/ archive/ \
  --pipeline high_quality \
  -q 9
```

### Manga Processing

```bash
shiroink manga/ output/ \
  --rtl \
  --pipeline kindle \
  -r 1072x1448
```

### Using a Saved Profile

```bash
shiroink manga/ output/ --profile my-kindle-reader
```

### Quick Format Conversion

```bash
# Fast, no processing
shiroink images/ output/ --pipeline minimal
```

### Batch Processing with Logging

```bash
shiroink input/ output/ \
  --pipeline kindle \
  --debug \
  --workers 8 > processing.log 2>&1
```

## Supported Formats

**Input:**
- JPEG, PNG, WebP, GIF, BMP, TIFF

**Output:**
- JPEG (default)
- PNG (preserves quality)

## Error Handling

By default, ShiroInk continues processing even if some files fail:

```bash
# Continue on errors (default)
shiroink input/ output/
# Exit code: 0 (success), 1 (errors), 2 (critical)

# Stop on first error
shiroink input/ output/ --continue-on-error false
```

## Performance Tips

1. **Use Reasonable Worker Count**: 4-8 workers for most systems
2. **Match Resolution to Device**: Exact device dimensions prevent unnecessary scaling
3. **Use Minimal Pipeline**: For simple format conversion
4. **Dry Run First**: Test configuration before full batch
5. **Save Profiles**: Reuse your best settings across sessions

## Troubleshooting

### Out of Memory
Reduce worker count:
```bash
shiroink input/ output/ -w 2
```

### Slow Processing
Increase worker count or use minimal pipeline:
```bash
shiroink input/ output/ --pipeline minimal -w 8
```

### Quality Issues
Increase quality setting:
```bash
shiroink input/ output/ -q 9
```

## More Information

- [Quick Start](quickstart.md) - 5-minute setup
- [Interactive Wizard Guide](wizard.md) - Learn about the setup wizard
- [Profile Management](profiles.md) - Learn about saving and using profiles
- [Device Presets](device-presets.md) - Device specifications
- [Architecture](../architecture/) - How ShiroInk works
