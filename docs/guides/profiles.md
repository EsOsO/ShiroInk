# Configuration Profiles Guide

Configuration profiles allow you to save and reuse ShiroInk settings, eliminating the need to specify parameters each time you process files with the same settings.

## What Are Profiles?

A profile is a saved configuration containing:
- Target device and resolution
- Image quality settings
- Processing performance settings
- Page format (LTR/RTL)
- Input and output directories

Profiles are stored as JSON files, making them easy to:
- Share with teammates
- Version control
- Edit manually
- Back up

## Where Profiles Are Stored

Profiles are stored in your user configuration directory:

| Platform | Location |
|----------|----------|
| **Linux** | `~/.config/shiroink/profiles/` |
| **macOS** | `~/.config/shiroink/profiles/` |
| **Windows** | `%APPDATA%\shiroink\profiles\` |

Example files:
```
~/.config/shiroink/profiles/
├── my-kindle.json
├── fast-preview.json
├── publication-quality.json
└── tablet-portrait.json
```

## Creating Profiles

### Method 1: Interactive Wizard (Recommended)

```bash
shiroink --wizard
```

After completing the wizard steps:
1. Review your configuration
2. Choose "Proceed"
3. When asked "Save this configuration as a profile?", answer yes
4. Enter a profile name (e.g., "my-kindle")

The profile is now saved and ready to use.

### Method 2: Command-Line Conversion

Process files with desired settings, then save as profile:

```bash
# Process with specific settings
shiroink input/ output/ --device kindle_paperwhite --quality 8 --workers 4

# When prompted "Save as profile?", answer yes
```

### Method 3: Manual JSON Creation

Create a JSON file directly:

```bash
mkdir -p ~/.config/shiroink/profiles
nano ~/.config/shiroink/profiles/my-custom.json
```

Profile JSON template:

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

**Profile fields:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Profile identifier |
| `device` | string | Target device key (e.g., "kindle_paperwhite") |
| `resolution` | array | [width, height] in pixels |
| `quality` | int | Quality level 1-9 |
| `workers` | int | Thread count for processing |
| `rtl` | bool | Right-to-left page order |
| `created` | string | ISO timestamp of creation |
| `last_used` | string | ISO timestamp of last use |

## Using Profiles

### List Available Profiles

```bash
shiroink --list-profiles
```

Output:
```
Saved Profiles:
============================================================
  my-kindle                 Created: 2024-01-15, Last used: 2024-01-20
  tablet-fast              Created: 2024-01-10, Last used: Never
============================================================

Usage: shiroink input/ output/ --profile PROFILE_NAME
```

### Apply a Profile

```bash
shiroink input/ output/ --profile my-kindle
```

This uses all settings from the profile:
- Resolution
- Quality level
- Worker count
- Format (LTR/RTL)

### Override Profile Settings

Command-line parameters override profile settings:

```bash
# Use profile but increase quality
shiroink input/ output/ --profile my-kindle --quality 9

# Use profile but different device
shiroink input/ output/ --profile standard-config --device kobo_libra_2

# Use profile but change worker count
shiroink input/ output/ --profile my-setup --workers 8
```

Priority order (highest to lowest):
1. Command-line arguments
2. Profile settings
3. Built-in defaults

## Managing Profiles

### View Profile Contents

```bash
# Linux/macOS
cat ~/.config/shiroink/profiles/my-kindle.json

# Windows
type %APPDATA%\shiroink\profiles\my-kindle.json
```

Example output:
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

### Edit a Profile

Edit the JSON file directly:

```bash
# Linux/macOS
nano ~/.config/shiroink/profiles/my-kindle.json

# Windows
notepad %APPDATA%\shiroink\profiles\my-kindle.json
```

Make your changes and save. The profile is updated immediately.

### Duplicate a Profile

Copy an existing profile as a starting point:

```bash
# Linux/macOS
cp ~/.config/shiroink/profiles/my-kindle.json \
   ~/.config/shiroink/profiles/my-kindle-variant.json

# Windows
copy %APPDATA%\shiroink\profiles\my-kindle.json \
     %APPDATA%\shiroink\profiles\my-kindle-variant.json
```

Then edit the new file to customize it.

### Delete a Profile

```bash
# Linux/macOS
rm ~/.config/shiroink/profiles/my-profile.json

# Windows
del %APPDATA%\shiroink\profiles\my-profile.json
```

Or use CLI (when available):
```bash
shiroink --delete-profile my-profile
```

### Rename a Profile

Edit the `"name"` field in the JSON file, or rename the file:

```bash
# Linux/macOS
mv ~/.config/shiroink/profiles/old-name.json \
   ~/.config/shiroink/profiles/new-name.json

# Windows
ren %APPDATA%\shiroink\profiles\old-name.json new-name.json
```

## Profile Examples

### Fast Preview for Testing

```json
{
  "name": "fast-preview",
  "device": "kindle_paperwhite",
  "resolution": [1072, 1448],
  "quality": 3,
  "workers": 8,
  "rtl": false,
  "created": "2024-01-15T10:30:00",
  "last_used": "2024-01-15T14:22:15"
}
```

### Publication Quality

```json
{
  "name": "publication-quality",
  "device": "kobo_libra_h2o",
  "resolution": [1440, 1920],
  "quality": 9,
  "workers": 4,
  "rtl": false,
  "created": "2024-01-15T10:30:00",
  "last_used": "2024-01-15T14:22:15"
}
```

### Manga (Right-to-Left)

```json
{
  "name": "manga-rtl-kindle",
  "device": "kindle_paperwhite_11",
  "resolution": [1264, 1680],
  "quality": 6,
  "workers": 4,
  "rtl": true,
  "created": "2024-01-15T10:30:00",
  "last_used": "2024-01-15T14:22:15"
}
```

### iPad Tablet Processing

```json
{
  "name": "ipad-pro-11-color",
  "device": "ipad_pro_11",
  "resolution": [1668, 2388],
  "quality": 8,
  "workers": 6,
  "rtl": false,
  "created": "2024-01-15T10:30:00",
  "last_used": "2024-01-15T14:22:15"
}
```

## Sharing Profiles

Profiles are JSON files that can be shared with others:

### Share a Profile File

```bash
# Copy profile to share
cp ~/.config/shiroink/profiles/my-kindle.json ~/Downloads/

# Share via email, file hosting, etc.
```

### Import a Received Profile

```bash
# Copy received profile to profiles directory
cp ~/Downloads/shared-profile.json ~/.config/shiroink/profiles/

# Use it immediately
shiroink input/ output/ --profile shared-profile
```

## Tips & Best Practices

### Naming Conventions

Use descriptive names for easy identification:

```
Good profile names:
- kindle_paperwhite_best_quality
- tablet_ipad_fast
- manga_rtl_cobo_clara
- publication_print_ready

Avoid:
- profile1, profile2
- test, temp
- unnamed
```

### Creating a Library

Build a profile library for different scenarios:

```
~/.config/shiroink/profiles/
├── device_kindle_paperwhite.json
├── device_kobo_libra.json
├── device_ipad_pro.json
├── quality_fast.json
├── quality_balanced.json
├── quality_best.json
├── format_ltr.json
├── format_rtl_manga.json
└── README.md
```

### Documentation

Create a README in your profiles directory:

```markdown
# ShiroInk Profiles

## Device Presets
- kindle_paperwhite: Optimized for Amazon Kindle Paperwhite
- kobo_libra: Optimized for Kobo Libra e-reader
- ipad_pro: Optimized for Apple iPad Pro 11"

## Quality Presets
- fast: Speed priority, lower quality (quality level 3)
- balanced: Good balance (quality level 6)
- best: Quality priority (quality level 9)

## Format Presets
- ltr: Left-to-right (books, publications)
- rtl: Right-to-left (manga, Arabic, Hebrew)
```

### Version Control

If using Git, you can version control your profiles:

```bash
cd ~/.config/shiroink/profiles
git init
git add *.json
git commit -m "Add ShiroInk profiles"
```

## Troubleshooting

### Profile Not Found

```
Error: Profile 'my-profile' not found.
Use --list-profiles to see available profiles.
```

**Solution:** Check the profile name spelling, or list profiles with `shiroink --list-profiles`.

### Invalid Profile Format

If a profile file is corrupted or has invalid JSON, you'll see an error. Fix it by:

1. Opening the file in a text editor
2. Checking JSON syntax (use a [JSON validator](https://jsonlint.com/))
3. Ensuring all required fields are present

### Profiles Not Found on Startup

On Windows, ensure the path exists:

```powershell
# Create profiles directory if needed
mkdir "$env:APPDATA\shiroink\profiles"
```

## See Also

- [Interactive Wizard Guide](wizard.md)
- [CLI Reference](../usage.md)
- [Device Presets](device-presets.md)
