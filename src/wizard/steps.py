"""
Wizard steps implementation for interactive setup.
"""

from pathlib import Path
from typing import Any, Optional

from .prompts import (
    print_header,
    print_info,
    print_section,
    print_success,
    print_warning,
    prompt_choice,
    prompt_input,
    prompt_integer,
)


def _(key: str) -> str:
    """Placeholder for translation strings."""
    # For now, return the key itself
    # Will be replaced with proper localization
    return key


# English translations (Phase 2: will integrate with localization system)
TEXTS = {
    "device_selection_header": "Device Selection",
    "device_selection_prompt": "Choose your target device:",
    "format_selection_header": "Format Selection",
    "format_selection_prompt": "Choose page orientation:",
}


class WizardStep:
    """Base class for wizard steps."""

    def execute(self, config: dict[str, Any]) -> Optional[dict[str, Any]]:
        """
        Execute the wizard step.

        Args:
            config: Current accumulated configuration.

        Returns:
            Dictionary with step results, or None if cancelled.
        """
        raise NotImplementedError


class DeviceSelectionStep(WizardStep):
    """Device selection step."""

    # Device database (will be enhanced in future)
    DEVICES = [
        (1, 'Kindle Paperwhite 11" [DEFAULT]'),
        (2, "Kobo Libra 2"),
        (3, 'iPad Pro 12.9"'),
        (4, "Custom Device..."),
        (5, "Don't know / List all devices"),
    ]

    def execute(self, config: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Execute device selection step."""
        print_section("Device Selection")

        choice = prompt_choice(
            "Choose your target device:",
            self.DEVICES,
            default=1,
        )

        device_map = {
            1: "kindle_paperwhite_11",
            2: "kobo_libra_2",
            3: "ipad_pro_129",
            4: None,  # Custom
            5: None,  # List
        }

        selected_device = device_map.get(choice)

        # If user chose "List all devices", show complete list
        if choice == 5:
            selected_device = self._show_all_devices()

        return {"device": selected_device}

    def _show_all_devices(self) -> Optional[str]:
        """Show all available devices and let user choose."""
        from image_pipeline.devices import DeviceSpecs

        print()
        print_section("Available Devices")

        all_devices = DeviceSpecs.get_all_devices()

        # Group devices by manufacturer
        groups = {
            "Kindle": [],
            "Kobo": [],
            "Tolino": [],
            "PocketBook": [],
            "iPad": [],
        }

        for key, spec in sorted(all_devices.items()):
            if key.startswith("kindle"):
                groups["Kindle"].append((key, spec.name))
            elif key.startswith("kobo"):
                groups["Kobo"].append((key, spec.name))
            elif key.startswith("tolino"):
                groups["Tolino"].append((key, spec.name))
            elif key.startswith("pocketbook"):
                groups["PocketBook"].append((key, spec.name))
            elif key.startswith("ipad"):
                groups["iPad"].append((key, spec.name))

        # Display grouped devices
        device_list = []
        idx = 1
        for group_name, devices in groups.items():
            if devices:
                print(f"\n{group_name}:")
                for device_key, device_name in devices:
                    print(f"  {idx}) {device_name} ({device_key})")
                    device_list.append(device_key)
                    idx += 1

        print(f"\n  {idx}) Back to quick selection")
        device_list.append(None)

        print()
        choice = prompt_integer(
            "Select device number:",
            default=1,
            min_val=1,
            max_val=len(device_list),
        )

        selected_key = device_list[choice - 1]
        if selected_key:
            print_success(f"Selected: {all_devices[selected_key].name}")
        else:
            print_info("Returning to quick selection...")

        return selected_key


class FormatSelectionStep(WizardStep):
    """Format (LTR/RTL) selection step."""

    def execute(self, config: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Execute format selection step."""
        print_section("Format Selection")

        formats = [
            (1, "Left-to-Right (Western comics)"),
            (2, "Right-to-Left (Japanese manga)"),
        ]

        choice = prompt_choice(
            "Choose page orientation:",
            formats,
            default=1,
        )

        return {"rtl": choice == 2}


class PathsSelectionStep(WizardStep):
    """Source and destination path selection step."""

    def execute(self, config: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Execute paths selection step."""
        print_section("Select directories")

        # Source path
        while True:
            src = prompt_input(
                "Source directory (contains images to process):",
                default=str(Path.home() / "manga"),
            )

            src_path = Path(src).expanduser()
            if src_path.exists() and src_path.is_dir():
                print_success(f"Source: {src_path}")
                break
            else:
                print_warning(f"Directory not found: {src_path}")

        # Destination path
        while True:
            dest = prompt_input(
                "Destination directory (where to save processed files):",
                default=str(Path.home() / "manga_processed"),
            )

            dest_path = Path(dest).expanduser()
            # Dest doesn't need to exist, but parent should
            if dest_path.parent.exists():
                print_success(f"Destination: {dest_path}")
                break
            else:
                print_warning(f"Parent directory not found: {dest_path.parent}")

        return {
            "src_dir": src_path,
            "dest_dir": dest_path,
        }


class QualitySelectionStep(WizardStep):
    """Quality level selection step."""

    def execute(self, config: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Execute quality selection step."""
        print_section("Quality Selection")

        quality = prompt_integer(
            "Quality level (1=fast, 9=best, default: 6):",
            default=6,
            min_val=1,
            max_val=9,
        )

        return {"quality": quality}


class PerformanceSelectionStep(WizardStep):
    """Performance (workers) selection step."""

    def execute(self, config: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Execute performance selection step."""
        print_section("Performance Configuration")

        import os

        cores = os.cpu_count() or 4
        print_info(f"System detected: {cores} CPU cores")

        workers = prompt_integer(
            "Number of parallel threads (default: 4):",
            default=4,
            min_val=1,
            max_val=cores * 2,
        )

        return {"workers": workers}


class ReviewStep(WizardStep):
    """Configuration review step."""

    def execute(self, config: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Execute review step."""
        print_header("Configuration Review")

        print_section("Configuration Review")
        print(f"  {'Device:':<20} {config.get('device', 'Default')}")
        print(f"  {'Format:':<20} {'RTL' if config.get('rtl') else 'LTR'}")
        print(f"  {'Source:':<20} {config.get('src_dir')}")
        print(f"  {'Destination:':<20} {config.get('dest_dir')}")
        print(f"  {'Quality:':<20} {config.get('quality')} / 9")
        print(f"  {'Workers:':<20} {config.get('workers')}")

        return {}


class ConfirmationStep(WizardStep):
    """Final confirmation step."""

    def execute(self, config: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Execute confirmation step."""
        print()

        choices = [
            (1, "[y] Yes, start processing"),
            (2, "[n] No, abort"),
            (3, "[m] Modify configuration"),
            (4, "[s] Save as profile before proceeding"),
        ]

        choice = prompt_choice(
            "Proceed with processing?",
            choices,
            default=1,
        )

        return {
            "action": {
                1: "proceed",
                2: "abort",
                3: "modify",
                4: "save",
            }.get(choice, "abort")
        }
