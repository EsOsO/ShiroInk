from pathlib import Path
from file_processor import process_images_in_directory, extract_and_process_cbz
from cli import parse_arguments
from config import create_progress, console


def main(
    src_dir: Path,
    dest_dir: Path,
    resolution: str,
    rtl: bool = False,
    quality: int = 6,
    debug: bool = False,
    dry_run: bool = False,
    workers: int = 4,
) -> None:
    progress = create_progress()
    if not src_dir.is_dir():
        console.print(
            f"[bold red]Error:[/bold red] {src_dir} is not a valid directory."
        )
        return

    items = [
        Path(item)
        for item in src_dir.iterdir()
        if item.is_dir() or item.suffix in (".cbz")
    ]

    with progress:
        task_id = progress.add_task("Processing chapter/volumes...", total=len(items))

        for item in items:
            if item.is_dir():
                process_images_in_directory(
                    item,
                    src_dir,
                    dest_dir,
                    resolution,
                    progress,
                    rtl,
                    quality,
                    debug,
                    dry_run,
                    workers,
                )
            elif item.suffix == ".cbz":
                extract_and_process_cbz(
                    item,
                    src_dir,
                    dest_dir,
                    resolution,
                    progress,
                    rtl,
                    quality,
                    debug,
                    dry_run,
                    workers,
                )

            progress.advance(task_id)


if __name__ == "__main__":
    args = parse_arguments()

    # Validate resolution format
    try:
        width, height = map(int, args.resolution.split("x"))
    except ValueError:
        console.print(
            "[bold red]Error:[/bold red] Invalid resolution format. Use WIDTHxHEIGHT."
        )
        exit(1)

    main(
        args.src_dir,
        args.dest_dir,
        args.resolution,
        args.rtl,
        args.quality,
        args.debug,
        args.dry_run,
        args.workers,
    )
