from pathlib import Path
from queue import Queue
from file_processor import worker
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
        item for item in src_dir.iterdir() if item.is_dir() or item.suffix == ".cbz"
    ]
    queue = Queue()
    for item in items:
        queue.put(item)

    with progress:
        task_id = progress.add_task("Processing chapter/volumes...", total=len(items))
        for _ in range(workers):
            worker(
                queue,
                src_dir,
                dest_dir,
                resolution,
                progress,
                task_id,
                rtl,
                quality,
                debug,
                dry_run,
            )


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
