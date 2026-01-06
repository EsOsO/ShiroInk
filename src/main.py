from pathlib import Path
from file_processor import process_images_in_directory, extract_and_process_cbz
from cli import parse_arguments
from config import ProcessingConfig
from progress_reporter import ProgressReporter, ConsoleProgressReporter
from error_handler import ErrorTracker, ErrorSeverity


def process_images(config: ProcessingConfig, reporter: ProgressReporter) -> int:
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

        # Suggest saving as profile (unless one was already loaded or saved by wizard)
        if not config.loaded_profile and not config.wizard_saved_profile:
            from profiles.manager import ProfileManager

            try:
                from wizard.prompts import prompt_yes_no, prompt_input

                print()
                if prompt_yes_no(
                    "Save this configuration as a profile for future use?"
                ):

                    def validate_profile_name(name: str) -> str | None:
                        """Validate profile name is not empty."""
                        if not name.strip():
                            return "Profile name cannot be empty"
                        return None

                    profile_name = prompt_input(
                        "Profile name (e.g., 'my-device'):",
                        validate=validate_profile_name,
                    )
                    profile_manager = ProfileManager()
                    profile_manager.save(
                        name=profile_name,
                        device=(
                            config.device_key if hasattr(config, "device_key") else None
                        ),
                        pipeline=None,
                        resolution=config.resolution,
                        rtl=config.rtl,
                        quality=config.quality,
                        workers=config.workers,
                        description="",
                    )
                    print(f"Profile '{profile_name}' saved!")
            except Exception:
                # Silently ignore profile save errors
                pass

        return 0


def main() -> int:
    """Entry point for the shiroink CLI command."""
    import sys

    args = parse_arguments()

    wizard_saved_profile = False

    # Handle --help with Rich formatting
    if "-h" in sys.argv or "--help" in sys.argv:
        from cli import _print_rich_help

        _print_rich_help()
        return 0

    # Detect first-run: no src_dir and no special flags
    is_first_run = (
        not args.src_dir
        and not args.wizard
        and not args.list_profiles
        and not args.list_devices
    )

    if is_first_run:
        # Offer wizard to first-time users
        from wizard.prompts import prompt_yes_no

        print()
        if prompt_yes_no(
            "Welcome to ShiroInk! Would you like to run the interactive setup wizard?"
        ):
            args.wizard = True
        else:
            print("\nYou can always run the wizard later with: shiroink --wizard")
            print("For help, run: shiroink --help")
            return 0

    # Handle --wizard flag
    if args.wizard:
        from interactive_wizard import InteractiveWizard

        wizard = InteractiveWizard()
        wizard_config = wizard.get_config_for_processing()

        if wizard_config is None:
            print("Configuration cancelled.")
            return 0

        # Use wizard configuration
        args.src_dir = wizard_config["src_dir"]
        args.dest_dir = wizard_config["dest_dir"]
        args.resolution = wizard_config.get("resolution")
        args.device = wizard_config.get("device")
        args.quality = wizard_config.get("quality", 6)
        args.workers = wizard_config.get("workers", 4)
        args.rtl = wizard_config.get("rtl", False)
        wizard_saved_profile = wizard_config.get("saved_profile", False)

    # Handle --list-profiles flag
    if args.list_profiles:
        from profiles.manager import ProfileManager

        profile_manager = ProfileManager()
        print(profile_manager.format_profiles_for_display())
        return 0

    # Handle --profile flag (load existing profile)
    if args.profile and not args.wizard:
        from profiles.manager import ProfileManager

        profile_manager = ProfileManager()

        try:
            profile_manager.apply_to_args(args, args.profile)
            print(f"Loaded profile: {args.profile}")
        except FileNotFoundError:
            print(f"Error: Profile '{args.profile}' not found.")
            print("Use --list-profiles to see available profiles.")
            return 1
        except Exception as e:
            print(f"Error loading profile: {e}")
            return 1

    # Handle --list-devices flag
    if args.list_devices:
        from image_pipeline.devices import DeviceSpecs

        print(DeviceSpecs.format_devices_for_display())
        return 0

    # Validate required arguments
    if not args.src_dir or not args.dest_dir:
        print(
            "Error: src_dir and dest_dir are required (unless using --list-devices or --wizard)"
        )
        print("Run with -h for help")
        return 1

    # Validate that --device and --resolution are not used together
    if args.device and args.resolution is not None:
        print("Error: Cannot use --device and --resolution together")
        print(
            "The --device preset automatically sets the optimal resolution for that device"
        )
        print("Use either --device <preset> OR --resolution <width>x<height>, not both")
        return 1

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
            print(DeviceSpecs.format_device_info(device_spec))

        except KeyError as e:
            print(f"Error: {e}")
            print("Use --list-devices to see available device presets")
            return 1
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
        loaded_profile=args.profile if hasattr(args, "profile") else None,
        wizard_saved_profile=wizard_saved_profile,
    )

    # Create the appropriate reporter
    reporter = ConsoleProgressReporter()

    return process_images(config, reporter)


if __name__ == "__main__":
    exit(main())
