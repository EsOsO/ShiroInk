import argparse
from pathlib import Path


def parse_arguments():
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
        type=str,
        default="1404x1872",
        help="Resolution to resize the images (e.g., 800x600)",
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
    return parser.parse_args()
