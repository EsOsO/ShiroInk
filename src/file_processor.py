import shutil
import zipfile

from image_pipeline import process
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import ProcessingConfig
from progress_reporter import ProgressReporter
from error_handler import ErrorTracker, ErrorSeverity
from exceptions import (
    CBZExtractionError,
    CBZCreationError,
    ImageProcessingError,
)

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp"]


def __create_cbz_archive(
    directory: Path,
    config: ProcessingConfig,
    reporter: ProgressReporter,
    error_tracker: ErrorTracker,
) -> None:
    """
    Create a CBZ archive from the processed images in the destination directory.

    Args:
        directory: Path to the directory containing processed images.
        config: ProcessingConfig object containing processing parameters.
        reporter: ProgressReporter for logging and progress tracking.
        error_tracker: ErrorTracker for tracking errors.
    """

    cbz_path = config.dest_dir / f"{directory.name}.cbz"

    def _create_archive():
        if config.debug or config.dry_run:
            reporter.log(f"Creating CBZ archive: {cbz_path}")

        if not config.dry_run:
            with reporter:
                with zipfile.ZipFile(cbz_path, "w") as cbz:
                    files = [i for i in directory.rglob("*") if i.is_file()]
                    task_id = reporter.add_task(
                        f"Creating CBZ archive [cyan]{cbz_path.name}[/]...",
                        total=len(files),
                    )
                    for file_path in files:
                        cbz.write(file_path, file_path.relative_to(directory))
                        reporter.advance_task(task_id)
                    reporter.remove_task(task_id)
            shutil.rmtree(directory)
            if config.debug:
                reporter.log(f"Removed directory: {directory}")

    try:
        _create_archive()
    except Exception as exc:
        error = CBZCreationError("Failed to create CBZ archive", path=cbz_path)
        error_tracker.add_error(
            error=error,
            path=cbz_path,
            severity=ErrorSeverity.ERROR,
            step="cbz_creation",
        )
        reporter.log(f"Error creating CBZ archive {cbz_path}: {exc}", level="error")
        if not config.continue_on_error:
            raise error from exc


def extract_and_process_cbz(
    cbz_path: Path,
    config: ProcessingConfig,
    reporter: ProgressReporter,
    error_tracker: ErrorTracker,
) -> None:
    """
    Extract a .cbz archive and process all contained images.

    Args:
        cbz_path: Path to the .cbz file.
        config: ProcessingConfig object containing processing parameters.
        reporter: ProgressReporter for logging and progress tracking.
        error_tracker: ErrorTracker for tracking errors.
    """
    try:
        if config.debug or config.dry_run:
            status = "Would extract" if config.dry_run else "Extracting"
            reporter.log(f"{status} CBZ file: {cbz_path}")

        if not config.dry_run:
            with reporter:
                with zipfile.ZipFile(cbz_path, "r") as zip_ref:
                    extract_path = cbz_path.with_suffix("")
                    files = zip_ref.namelist()
                    task_id = reporter.add_task(
                        f"Extracting and processing [cyan]{cbz_path.name}[/]...",
                        total=len(files),
                    )
                    zip_ref.extractall(extract_path)
                    reporter.update_task(task_id=task_id, completed=len(files))
                    reporter.remove_task(task_id)
                    process_images_in_directory(
                        extract_path,
                        config,
                        reporter,
                        error_tracker,
                    )
                    shutil.rmtree(extract_path)

    except Exception as exc:
        error = CBZExtractionError("Failed to extract CBZ file", path=cbz_path)
        error_tracker.add_error(
            error=error,
            path=cbz_path,
            severity=ErrorSeverity.ERROR,
            step="cbz_extraction",
        )
        reporter.log(f"Error extracting CBZ file {cbz_path}: {exc}", level="error")
        if not config.continue_on_error:
            raise error from exc


def __process_file(
    reporter: ProgressReporter,
    file_path: Path,
    config: ProcessingConfig,
    error_tracker: ErrorTracker,
) -> None:
    """
    Process the image file using the manga_image_pipeline
    and copy to destination directory.

    Args:
        reporter: ProgressReporter for logging and progress tracking.
        file_path: Path to the file to be processed.
        config: ProcessingConfig object containing processing parameters.
        error_tracker: ErrorTracker for tracking errors.
    """
    try:
        relative_path = file_path.relative_to(config.src_dir)
        dest_path = config.dest_dir / relative_path.with_suffix(".png")
        if config.debug or config.dry_run:
            status = "Would process" if config.dry_run else "Processing"
            reporter.log(f"{status} file: {file_path} -> {dest_path}")

        if not config.dry_run:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            pipeline = config.get_pipeline()

            for attempt in range(config.max_retries + 1):
                try:
                    process(
                        file_path,
                        dest_path,
                        config.resolution,
                        config.rtl,
                        config.quality,
                        pipeline,
                    )
                    break
                except Exception:
                    if attempt < config.max_retries:
                        if config.debug:
                            reporter.log(
                                f"Retry {attempt + 1}/{config.max_retries} "
                                f"for {file_path}",
                                level="warning",
                            )
                        continue
                    else:
                        raise

    except Exception as exc:
        error = ImageProcessingError(
            "Failed to process image",
            path=file_path,
            step="image_processing",
            original_error=exc,
        )
        error_tracker.add_error(
            error=error,
            path=file_path,
            severity=ErrorSeverity.ERROR,
            step="image_processing",
        )
        reporter.log(f"Error processing file {file_path}: {exc}", level="error")
        if not config.continue_on_error:
            raise error from exc


def process_images_in_directory(
    directory: Path,
    config: ProcessingConfig,
    reporter: ProgressReporter,
    error_tracker: ErrorTracker,
) -> None:
    """
    Process all image files recursively in the given directory
    and copy to destination directory.

    Args:
        directory: Path to the directory containing images.
        config: ProcessingConfig object containing processing parameters.
        reporter: ProgressReporter for logging and progress tracking.
        error_tracker: ErrorTracker for tracking errors.
    """
    try:
        if config.debug or config.dry_run:
            status = "Would process" if config.dry_run else "Processing"
            reporter.log(f"{status} directory: {directory}")

        files = [
            file_path
            for file_path in directory.rglob("*")
            if file_path.suffix.lower() in IMAGE_EXTENSIONS
        ]

        with reporter:
            file_task_id = reporter.add_task(
                f"Processing images inside [cyan]{directory.name}[/]...",
                total=len(files),
            )

            with ThreadPoolExecutor(max_workers=config.workers) as executor:
                futures = [
                    executor.submit(
                        __process_file,
                        reporter,
                        file_path,
                        config,
                        error_tracker,
                    )
                    for file_path in files
                ]

                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        if not config.continue_on_error:
                            reporter.log(f"Error processing file: {e}", level="error")
                    finally:
                        reporter.advance_task(file_task_id)

            reporter.remove_task(file_task_id)
            directory_to_compress = config.dest_dir / directory.relative_to(
                config.src_dir
            )
            __create_cbz_archive(directory_to_compress, config, reporter, error_tracker)
    except Exception as e:
        reporter.log(f"Error processing directory {directory}: {e}", level="error")
        error_tracker.add_error(
            error=e,
            path=directory,
            severity=ErrorSeverity.CRITICAL,
            step="directory_processing",
        )
        if not config.continue_on_error:
            raise
