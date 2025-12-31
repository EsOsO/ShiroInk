from pathlib import Path
from file_processor import process_images_in_directory, extract_and_process_cbz
from cli import parse_arguments
from config import ProcessingConfig
from progress_reporter import ProgressReporter, ConsoleProgressReporter
from error_handler import ErrorTracker, ErrorSeverity


def main(config: ProcessingConfig, reporter: ProgressReporter) -> int:
    """
    Main processing function that handles directories and CBZ files.

    Args:
        config: ProcessingConfig object containing all processing parameters.
        reporter: ProgressReporter for logging and progress tracking.

    Returns:
        Exit code (0 for success, 1 for errors, 2 for critical errors).
    """
    error_tracker = ErrorTracker()

    if not config.src_dir.is_dir():
        reporter.log(
            f"Error: {config.src_dir} is not a valid directory.", level="error"
        )
        return 2

    items = [
        Path(item)
        for item in config.src_dir.iterdir()
        if item.is_dir() or item.suffix in (".cbz")
    ]

    with reporter:
        task_id = reporter.add_task("Processing chapter/volumes...", total=len(items))

        for item in items:
            if item.is_dir():
                process_images_in_directory(
                    item,
                    config,
                    reporter,
                    error_tracker,
                )
            elif item.suffix == ".cbz":
                extract_and_process_cbz(
                    item,
                    config,
                    reporter,
                    error_tracker,
                )

            reporter.advance_task(task_id)

    # Print error summary
    if error_tracker.has_errors():
        reporter.log("\n" + "=" * 60, level="warning")
        reporter.log("ERROR SUMMARY", level="warning")
        reporter.log("=" * 60, level="warning")

        summary = error_tracker.get_summary()
        reporter.log(f"Total errors: {summary['total_errors']}", level="warning")
        reporter.log(f"  Warnings: {summary['warnings']}", level="warning")
        reporter.log(f"  Errors: {summary['errors']}", level="error")
        reporter.log(f"  Critical: {summary['critical']}", level="error")
        reporter.log(
            f"Files with errors: {summary['files_with_errors']}", level="warning"
        )

        if summary["most_problematic_file"]:
            file_path, count = summary["most_problematic_file"]
            reporter.log(
                f"Most problematic file: {file_path} ({count} errors)", level="warning"
            )

        if summary["errors_by_step"]:
            reporter.log("\nErrors by step:", level="warning")
            for step, count in summary["errors_by_step"].items():
                reporter.log(f"  {step}: {count}", level="warning")

        # Show first few errors in detail
        if config.debug:
            reporter.log("\nFirst 5 errors in detail:", level="warning")
            for error in error_tracker.get_errors()[:5]:
                reporter.log(f"  {error}", level="error")

        reporter.log("=" * 60, level="warning")

        # Determine exit code
        if error_tracker.has_critical_errors():
            return 2
        else:
            return 1
    else:
        reporter.log(
            "\nProcessing completed successfully with no errors!", level="info"
        )
        return 0


if __name__ == "__main__":
    args = parse_arguments()
    config = ProcessingConfig(
        src_dir=args.src_dir,
        dest_dir=args.dest_dir,
        resolution=args.resolution,
        rtl=args.rtl,
        quality=args.quality,
        debug=args.debug,
        dry_run=args.dry_run,
        workers=args.workers,
        pipeline_preset=args.pipeline,
    )

    # Create the appropriate reporter
    reporter = ConsoleProgressReporter()

    exit_code = main(config, reporter)
    exit(exit_code)
