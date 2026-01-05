# Interactive Wizard Guide

The ShiroInk interactive wizard is an optional, guided configuration system designed for new users and those who prefer step-by-step setup.

## Quick Start

To start the wizard:

```bash
shiroink --wizard
```

## How the Wizard Works

The wizard walks you through 6 configuration steps:

### 1. Device Selection
Choose your target device or display type:
- **Kindle** - Amazon Kindle e-readers (Paperwhite, Oasis, Colorsoft, etc.)
- **Kobo** - Kobo e-readers (Clara, Libra, Elipsa, etc.)
- **iPad** - Apple iPad tablets (Mini, Pro, etc.)
- **Tolino** - Tolino e-readers (Vision, Shine, etc.)
- **PocketBook** - PocketBook e-readers
- **Custom** - Manual resolution and settings

The device selection automatically configures:
- Optimal resolution
- Color profile (grayscale vs. color)
- Display characteristics
- Recommended pipeline

### 2. Format Selection
Choose page orientation handling:
- **LTR (Left-to-Right)** - Standard Western book format
- **RTL (Right-to-Left)** - Arabic, Hebrew, manga format (flip page order)

### 3. Paths Selection
Specify your input and output directories:
- **Source Directory** - Contains your images or CBZ files to process
- **Destination Directory** - Where processed files will be saved

Both directories must exist and be readable/writable.

### 4. Quality Level
Choose image quality (1-9):
- **1-3: Fast** - Lower quality, faster processing (good for previews)
- **4-6: Balanced** - Good quality and speed (recommended)
- **7-9: Best** - Best quality, slower processing (for final output)

Quality affects:
- Color depth reduction
- Compression levels
- Processing time
- Final file size

### 5. Performance Settings
Configure parallel processing:
- **Auto (Default)** - Uses number of CPU cores - 1
- **Manual** - Specify custom worker thread count

More workers = faster processing but higher CPU usage.

### 6. Review & Confirm
Review your configuration:
- Confirm and proceed with processing
- Modify individual settings
- Cancel and exit

## Saving Configurations as Profiles

After configuration, you can save your settings as a **profile** for future reuse.

```bash
# Wizard will ask if you want to save:
# "Save this configuration as a profile for future use? [y/N]"
```

Profiles are saved in:
- **Linux/macOS**: `~/.config/shiroink/profiles/`
- **Windows**: `%APPDATA%\shiroink\profiles\`

## Using Saved Profiles

### List Available Profiles
```bash
shiroink --list-profiles
```

Output:
```
Saved Profiles:
============================================================
  my-kindle                 Created: 2024-01-15, Last used: 2024-01-20
  tablet-fast              Created: 2024-01-10, Last used: 2024-01-18
  publication-best         Created: 2024-01-05, Last used: Never
============================================================

Usage: shiroink input/ output/ --profile PROFILE_NAME
```

### Apply a Profile
```bash
shiroink input/ output/ --profile my-kindle
```

This loads all settings from the profile (resolution, quality, workers, etc.).

### Override Profile Settings
Command-line arguments override profile settings:

```bash
# Use profile but override quality
shiroink input/ output/ --profile my-kindle --quality 9

# Use profile but override device
shiroink input/ output/ --profile my-config --device kobo_libra_2
```

## Example Workflows

### First-Time User: Interactive Setup
```bash
# Start wizard for guided configuration
shiroink --wizard

# Answer each step
# -> Choose device: Kindle Paperwhite
# -> Format: LTR
# -> Paths: /home/user/manga /home/user/manga-optimized
# -> Quality: 6 (balanced)
# -> Workers: Auto
# -> Review and save as "my-kindle-setup"

# Now you can use it repeatedly:
shiroink /home/user/manga /home/user/manga-optimized --profile my-kindle-setup
```

### Power User: Direct Arguments
```bash
# Skip wizard, use specific settings
shiroink input/ output/ --device kindle_paperwhite --quality 8 --workers 8
```

### Mixed Approach: Profile + Overrides
```bash
# Load fast profile but use higher quality for this job
shiroink input/ output/ --profile fast-preview --quality 8
```

## Troubleshooting

### I made a mistake during wizard setup
During the wizard, you can:
- **Modify** individual steps at the review screen
- **Abort** and start over with `--wizard` again

### I want to edit a saved profile
Profiles are JSON files. You can edit them directly:

**Linux/macOS:**
```bash
nano ~/.config/shiroink/profiles/my-profile.json
```

**Windows:**
```powershell
notepad %APPDATA%\shiroink\profiles\my-profile.json
```

Profile format:
```json
{
  "name": "my-kindle",
  "device": "kindle_paperwhite",
  "resolution": [1072, 1448],
  "quality": 6,
  "workers": 4,
  "rtl": false,
  "created": "2024-01-15T10:30:00",
  "last_used": "2024-01-20T14:22:15"
}
```

### I want to delete a profile
Delete the profile's JSON file:

```bash
# Linux/macOS
rm ~/.config/shiroink/profiles/my-profile.json

# Windows
del %APPDATA%\shiroink\profiles\my-profile.json
```

Or use the CLI (when available):
```bash
shiroink --delete-profile my-profile
```

## Keyboard Controls

During wizard navigation:

| Key | Action |
|-----|--------|
| `↑/↓` | Select option |
| `Enter` | Confirm selection |
| `Ctrl+C` | Cancel wizard |

## Tips & Best Practices

1. **Create device-specific profiles** - Save one for each target device
2. **Test quality levels** - Try 6 (balanced) first, adjust up/down as needed
3. **Use appropriate worker counts** - Don't exceed CPU cores
4. **Save after setup** - Profiles make repeated processing fast and consistent
5. **Share profiles** - Profiles are JSON, easily shareable with others
6. **Version your profiles** - Add dates or version numbers to profile names

## See Also

- [Profiles Management Guide](profiles.md)
- [Device Presets](device-presets.md)
- [CLI Reference](../usage.md)
