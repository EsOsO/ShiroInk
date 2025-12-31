# Usage Guide

Complete guide to using ShiroInk.

## Basic Usage

```bash
shiroink <input_directory> <output_directory> [options]
```

## Options

### Pipeline Selection

```bash
-p, --pipeline {kindle,tablet,print,high_quality,minimal}
```

Choose a processing preset:

- **kindle**: Optimized for e-readers (default)
- **tablet**: For iPad/Android tablets
- **print**: High quality for printing
- **high_quality**: Maximum quality
- **minimal**: Light processing

### Resolution

```bash
-r, --resolution RESOLUTION
```

Set custom resolution (e.g., `800x600`, `1920x1080`, or just `800` for square)

### Quality

```bash
-q, --quality QUALITY
```

Quality level from 1-9 (higher = better quality but larger files)

### Other Options

```bash
--rtl               # Right-to-left mode for manga
--dry-run           # Test without processing
-d, --debug         # Enable debug output
-w, --workers NUM   # Number of parallel workers (default: 4)
```

## Examples

See [Quick Start](quickstart.md) and [Docker Guide](docker.md) for more examples.
