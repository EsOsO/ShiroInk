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

    # Handle --list-devices flag
    if args.list_devices:
        from image_pipeline.devices import DeviceSpecs

        print("\nAvailable device presets:\n")
        print("=" * 140)

        devices = DeviceSpecs.get_all_devices()

        # Group by brand
        brands = {
            "Kindle": [],
            "Kobo": [],
            "Tolino": [],
            "PocketBook": [],
            "iPad": [],
        }

        for key, spec in sorted(devices.items()):
            if key.startswith("kindle"):
                brands["Kindle"].append((key, spec))
            elif key.startswith("kobo"):
                brands["Kobo"].append((key, spec))
            elif key.startswith("tolino"):
                brands["Tolino"].append((key, spec))
            elif key.startswith("pocketbook"):
                brands["PocketBook"].append((key, spec))
            elif key.startswith("ipad"):
                brands["iPad"].append((key, spec))

        # Print header
        print(
            f"{'Device':<32} {'Resolution':<12} {'Size':<7} {'Display':<8} {'Color':<8} {'Gamut':<10} {'Bits':<5} {'Pipeline':<20}"
        )
        print("-" * 140)

        for brand, device_list in brands.items():
            if device_list:
                for key, spec in device_list:
                    color_str = "Color" if spec.color_support else "B&W"
                    gamut_str = spec.color_gamut.value if spec.color_gamut else "-"
                    print(
                        f"{key:<32} {spec.resolution[0]:4d}x{spec.resolution[1]:<7d} "
                        f'{spec.screen_size_inches:>5.1f}" {spec.display_type.value:<8} '
                        f"{color_str:<8} {gamut_str:<10} {spec.bit_depth:<5} {spec.recommended_pipeline:<20}"
                    )

        print("\n" + "=" * 140)
        print("\nUsage: --device <device_key>")
        print("Example: --device kindle_paperwhite_11")
        print("\n")
        exit(0)

    # Validate required arguments
    if not args.src_dir or not args.dest_dir:
        print("Error: src_dir and dest_dir are required (unless using --list-devices)")
        print("Run with -h for help")
        exit(1)

    # Validate that --device and --resolution are not used together
    if args.device and args.resolution is not None:
        print("Error: Cannot use --device and --resolution together")
        print(
            "The --device preset automatically sets the optimal resolution for that device"
        )
        print("Use either --device <preset> OR --resolution <width>x<height>, not both")
        exit(1)

    # Determine resolution and pipeline based on device or manual settings
    resolution = args.resolution
    pipeline_preset = args.pipeline
    custom_pipeline = None

    if args.device:
        from image_pipeline.devices import DeviceSpecs
        from image_pipeline.presets import PipelinePresets

        try:
            device_spec = DeviceSpecs.get_device(args.device)
            resolution = device_spec.resolution

            # Use the device-aware pipeline factory
            custom_pipeline = PipelinePresets.from_device_spec(device_spec)

            # Display comprehensive device information
            print(f"\n{'='*60}")
            print(f"Using device preset: {device_spec.name}")
            print(f"{'='*60}")
            print(f"Resolution:       {resolution[0]}x{resolution[1]}")
            print(f'Screen size:      {device_spec.screen_size_inches}"')
            print(f"Display type:     {device_spec.display_type.value}")
            print(
                f"Color support:    {'Color' if device_spec.color_support else 'B&W only'}"
            )
            if device_spec.color_gamut:
                print(f"Color gamut:      {device_spec.color_gamut.value}")
            print(
                f"Bit depth:        {device_spec.bit_depth}-bit ({device_spec.max_colors if device_spec.max_colors else 'grayscale'} colors)"
            )
            print(f"Recommended:      {device_spec.recommended_pipeline} pipeline")
            print(f"{'='*60}\n")

        except KeyError as e:
            print(f"Error: {e}")
            print("Use --list-devices to see available device presets")
            exit(1)
    elif args.resolution is None:
        # No --device and no --resolution specified, use default
        resolution = (1404, 1872)
        print(f"Using default resolution: {resolution[0]}x{resolution[1]}")
        print("(Specify --resolution or --device to override)\n")

    config = ProcessingConfig(
        src_dir=args.src_dir,
        dest_dir=args.dest_dir,
        resolution=resolution,
        rtl=args.rtl,
        quality=args.quality,
        debug=args.debug,
        dry_run=args.dry_run,
        workers=args.workers,
        pipeline_preset=pipeline_preset,
        custom_pipeline=custom_pipeline,
    )

    # Create the appropriate reporter
    reporter = ConsoleProgressReporter()

    exit_code = main(config, reporter)
    exit(exit_code)
