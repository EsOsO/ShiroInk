import argparse
from pathlib import Path
from __version__ import __version__
from rich.console import Console


def _create_rich_help() -> str:
    """Create a Rich-formatted help message."""
    help_text = """
[bold]ShiroInk[/bold] - Manga and Comic Book Image Optimization

[bold yellow]USAGE:[/bold yellow]
  shiroink [OPTIONS] SRC_DIR DEST_DIR    Process images in batch mode
  shiroink --wizard                       Interactive configuration wizard
  shiroink --list-devices                 Show available devices
  shiroink --help                         Show this help message

[bold yellow]EXAMPLES:[/bold yellow]
  shiroink input/ output/ --device kindle_paperwhite
  shiroink input/ output/ --resolution 1072x1448 --quality 8
  shiroink --wizard                       Start interactive setup

[bold yellow]OPTIONS:[/bold yellow]
  -d, --device PRESET        Use device preset (e.g., kindle_paperwhite)
  -r, --resolution WxH       Manual resolution (e.g., 800x600)
  -q, --quality LEVEL        Quality 1-9 (default: 6)
  -w, --workers NUM          Thread count (default: auto-detect)
  --rtl                      Right-to-left page order
  --dry-run                  Preview without processing
  -p, --pipeline PRESET      Pipeline preset (default: kindle)
  --list-devices             Show all available devices
  --profile NAME             Load configuration from profile
  --list-profiles            Show all saved profiles
  --wizard                   Interactive configuration wizard
  --debug                    Enable debug output
  -v, --version              Show version
  -h, --help                 Show this help

[bold yellow]PROFILES:[/bold yellow]
  Save configurations as profiles for reuse:
    shiroink input/ output/ --profile my-kindle    [green](uses profile)[/green]
    shiroink --wizard --profile save-as-new        [green](save new profile)[/green]

[bold yellow]MORE HELP:[/bold yellow]
  Run 'shiroink --wizard' for interactive setup (recommended for first-time users)
  Use 'shiroink --list-devices' to see all compatible devices
    """
    return help_text


def _print_rich_help() -> None:
    """Print Rich-formatted help message."""
    console = Console()
    console.print(_create_rich_help())


def parse_arguments():
    def parse_resolution(value: str) -> tuple[int, int]:
        """Accept forms like '800x600', '800X600', '800 600', '800,600'.

        Or '800' -> (800,800).
        """
        if not isinstance(value, str):
            raise argparse.ArgumentTypeError("Resolution must be a string")
        s = value.strip().replace("X", "x").replace("x", " ").replace(",", " ")
        parts = s.split()
        if not parts:
            raise argparse.ArgumentTypeError(
                "Resolution must be like '800x600', '800 600', '800,600' or '800'"
            )
        try:
            nums = [int(p) for p in parts]
        except ValueError:
            raise argparse.ArgumentTypeError("Resolution values must be integers")
        if len(nums) == 1:
            w = h = nums[0]
        else:
            w, h = nums[0], nums[1]
        if w <= 0 or h <= 0:
            raise argparse.ArgumentTypeError("Resolution values must be positive")
        return (w, h)

    parser = argparse.ArgumentParser(
        description="Resize and optimize images in a directory or CBZ files.",
        prog="ShiroInk",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "src_dir",
        type=Path,
        nargs="?",
        help="Source directory containing files to process",
    )
    parser.add_argument(
        "dest_dir",
        type=Path,
        nargs="?",
        help="Destination directory to place processed files",
    )
    parser.add_argument(
        "-r",
        "--resolution",
        type=parse_resolution,
        default=None,
        help="Resolution to resize the images (e.g., 800x600, '800 600', '800,600' or '800'). "
        "Defaults to 1404x1872 if neither --device nor --resolution is specified.",
    )
    parser.add_argument(
        "--rtl", action="store_true", help="Switch the order of two-page images"
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=6,
        help="Quality level for optimization (1-9)",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug output"
    )
    parser.add_argument(
        "-w", "--workers", type=int, default=4, help="Number of threads to use"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually doing it",
    )
    parser.add_argument(
        "-p",
        "--pipeline",
        type=str,
        default="kindle",
        choices=[
            "kindle",
            "kobo",
            "tolino",
            "pocketbook",
            "pocketbook_color",
            "ipad",
            "eink",
            "tablet",
            "print",
            "high_quality",
            "minimal",
        ],
        help="Processing pipeline preset to use (default: kindle)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="Specific device preset (e.g., kindle_paperwhite, kobo_libra_2, ipad_pro_11). "
        "Automatically sets resolution and pipeline. Use --list-devices to see available devices.",
    )
    parser.add_argument(
        "--list-devices",
        action="store_true",
        help="List all available device presets and exit",
    )
    parser.add_argument(
        "--wizard",
        action="store_true",
        help="Start interactive configuration wizard",
    )
    parser.add_argument(
        "--profile",
        type=str,
        default=None,
        help="Load configuration from saved profile or save new profile",
    )
    parser.add_argument(
        "--list-profiles",
        action="store_true",
        help="List all saved profiles and exit",
    )
    return parser.parse_args()
