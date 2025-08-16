import shutil
import zipfile

from image_pipeline import process
from pathlib import Path
from rich.progress import Progress
from concurrent.futures import ThreadPoolExecutor, as_completed

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp"]


def __create_cbz_archive(
    directory: Path,
    dest_dir: Path,
    progress: Progress,
    debug: bool = False,
    dry_run: bool = False,
) -> None:
    """
    Create a CBZ archive from the processed images in the destination directory.

    Args:
        directory (Path): Path to the directory containing processed images.
        dest_dir (Path): Path to the destination directory.
        debug (bool): Flag to enable debug output.
    """

    cbz_path = dest_dir / f"{directory.name}.cbz"

    try:
        if debug or dry_run:
            progress.console.log(
                f"[bold green]Creating CBZ archive:[/bold green] {cbz_path}"
            )

        if not dry_run:
            with progress:
                with zipfile.ZipFile(cbz_path, "w") as cbz:
                    files = [i for i in directory.rglob("*") if i.is_file()]
                    task_id = progress.add_task(
                        f"Creating CBZ archive [cyan]{cbz_path.name}[/]...",
                        total=len(files),
                    )
                    for file_path in files:
                        cbz.write(file_path, file_path.relative_to(directory))
                        progress.advance(task_id)
                    progress.remove_task(task_id)
            # Remove the directory after creating the CBZ archive
            shutil.rmtree(directory)
            if debug:
                progress.console.log(
                    f"[bold green]Removed directory:[/bold green] {directory}"
                )
    except Exception as e:
        progress.console.log(
            f"[bold red]Error creating CBZ archive {cbz_path}: {e}[/bold red]"
        )


def extract_and_process_cbz(
    cbz_path: Path,
    src_dir: Path,
    dest_dir: Path,
    resolution: tuple[int, int],
    progress: Progress,
    rtl: bool = False,
    quality: int = 6,
    debug: bool = False,
    dry_run: bool = False,
    workers: int = 4,
) -> None:
    """
    Extract a .cbz archive and process all contained images.

    Args:
        cbz_path (Path): Path to the .cbz file.
        src_dir (Path): Path to the source directory.
        dest_dir (Path): Path to the destination directory.
        resolution (str): Resolution to resize the images.
        progress (Progress): Rich progress object to update progress.
        task_id (int): Task ID for the progress bar.
        rtl (bool): Flag to switch the order of two-page images.
        quality (int): The quality level for optimization (1-9).
        debug (bool): Flag to enable debug output.
        dry_run (bool): Flag to only print what would be done.
        workers (int): Number of worker threads to use.
    """
    try:
        if debug or dry_run:
            progress.console.log(
                f"[bold {'yellow' if dry_run else 'green'}]{'Would extract' if dry_run else 'Extracting'} CBZ file:[/bold {'yellow' if dry_run else 'green'}] {cbz_path}"
            )
        if not dry_run:
            with progress:
                with zipfile.ZipFile(cbz_path, "r") as zip_ref:
                    extract_path = cbz_path.with_suffix("")
                    files = zip_ref.namelist()
                    task_id = progress.add_task(
                        f"Extracting and processing [cyan]{cbz_path.name}[/]...",
                        total=len(files),
                    )
                    zip_ref.extractall(extract_path)
                    progress.update(task_id=task_id, completed=len(files))
                    progress.remove_task(task_id)
                    process_images_in_directory(
                        extract_path,
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
                    shutil.rmtree(extract_path)

    except Exception as e:
        progress.console.log(
            f"[bold red]Error extracting CBZ file {cbz_path}: {e}[/bold red]"
        )


def __process_file(
    progress: Progress,
    file_path: Path,
    src_dir: Path,
    dest_dir: Path,
    resolution: tuple[int, int],
    rtl: bool = False,
    quality: int = 6,
    debug: bool = False,
    dry_run: bool = False,
) -> None:
    """
    Process the image file using the manga_image_pipeline and copy to destination directory.

    Args:
        file_path (Path): Path to the file to be processed.
        src_dir (Path): Path to the source directory.
        dest_dir (Path): Path to the destination directory.
        resolution (str): Resolution to resize the image.
        rtl (bool): Flag to switch the order of two-page images.
        quality (int): The quality level for optimization (1-9).
        debug (bool): Flag to enable debug output.
        dry_run (bool): Flag to only print what would be done.
    """
    try:
        relative_path = file_path.relative_to(src_dir)
        dest_path = dest_dir / relative_path.with_suffix(".png")
        if debug or dry_run:
            progress.console.log(
                f"[bold {'yellow' if dry_run else 'green'}]{'Would process' if dry_run else 'Processing'} file:[/bold {'yellow' if dry_run else 'green'}] {file_path} -> {dest_path}"
            )
        if not dry_run:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            process(
                file_path,
                dest_path,
                resolution,
                rtl,
                quality,
            )
    except Exception as e:
        progress.console.log(
            f"[bold red]Error processing file {file_path}: {e}[/bold red]"
        )


def process_images_in_directory(
    directory: Path,
    src_dir: Path,
    dest_dir: Path,
    resolution: tuple[int, int],
    progress: Progress,
    rtl: bool = False,
    quality: int = 6,
    debug: bool = False,
    dry_run: bool = False,
    workers: int = 4,
) -> None:
    """
    Process all image files recursively in the given directory and copy to destination directory.

    Args:
        directory (Path): Path to the directory containing images.
        src_dir (Path): Path to the source directory.
        dest_dir (Path): Path to the destination directory.
        resolution (str): Resolution to resize the images.
        progress (Progress): Rich progress object to update progress.
        rtl (bool): Flag to switch the order of two-page images.
        quality (int): The quality level for optimization (1-9).
        debug (bool): Flag to enable debug output.
        dry_run (bool): Flag to only print what would be done.
        workers (int): Number of worker threads to use.
    """
    try:
        if debug or dry_run:
            progress.console.log(
                f"[bold {'yellow' if dry_run else 'green'}]{'Would process' if dry_run else 'Processing'} directory:[/bold {'yellow' if dry_run else 'green'}] {directory}"
            )

        files = [
            file_path
            for file_path in directory.rglob("*")
            if file_path.suffix.lower() in IMAGE_EXTENSIONS
        ]

        with progress:
            file_task_id = progress.add_task(
                f"Processing images inside [cyan]{directory.name}[/]...",
                total=len(files),
            )

            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = [
                    executor.submit(
                        __process_file,
                        progress,
                        file_path,
                        src_dir,
                        dest_dir,
                        resolution,
                        rtl,
                        quality,
                        debug,
                        dry_run,
                    )
                    for file_path in files
                ]

                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        progress.console.log(
                            f"[bold red]Error processing file: {e}[/bold red]"
                        )
                    finally:
                        progress.advance(file_task_id)

            progress.remove_task(file_task_id)
            directory_to_compress = dest_dir / directory.relative_to(src_dir)
            __create_cbz_archive(
                directory_to_compress, dest_dir, progress, debug, dry_run
            )
    except Exception as e:
        progress.console.log(
            f"[bold red]Error processing directory {directory}: {e}[/bold red]"
        )
