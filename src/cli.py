import argparse
from pathlib import Path


def parse_arguments():
    def parse_resolution(value: str) -> tuple[int, int]:
        """Accept forms like '800x600', '800X600', '800 600', '800,600' or '800' -> (800,800)."""
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
        description="Resize and optimize images in a directory or CBZ files."
    )
    parser.add_argument(
        "src_dir", type=Path, help="Source directory containing files to process"
    )
    parser.add_argument(
        "dest_dir", type=Path, help="Destination directory to place processed files"
    )
    parser.add_argument(
        "-r",
        "--resolution",
        type=parse_resolution,
        default=parse_resolution("1404x1872"),
        help="Resolution to resize the images (e.g., 800x600, '800 600', '800,600' or '800')",
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
        choices=["kindle", "tablet", "print", "high_quality", "minimal"],
        help="Processing pipeline preset to use (default: kindle)",
    )
    return parser.parse_args()
