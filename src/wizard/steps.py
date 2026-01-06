"""
Wizard steps implementation for interactive setup using Rich.
"""

from pathlib import Path
from typing import Any, Optional

from .prompts import (
    print_header,
    print_info,
    print_section,
    print_success,
    print_device_card,
    prompt_choice,
    prompt_integer,
    prompt_path,
)


def _(key: str) -> str:
    """Placeholder for translation strings."""
    return key


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

    DEVICES = [
        (1, 'Kindle Paperwhite 11" [DEFAULT]'),
        (2, "Kobo Libra 2"),
        (3, 'iPad Pro 12.9"'),
        (4, "Custom Device..."),
        (5, "List all devices"),
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
            4: None,
            5: None,
        }

        selected_device = device_map.get(choice)

        if choice == 5:
            selected_device = self._show_all_devices()

        if selected_device:
            print_success(f"Selected device: {selected_device}")

        return {"device": selected_device}

    def _show_all_devices(self) -> Optional[str]:
        """Show all available devices and let user choose."""
        from image_pipeline.devices import DeviceSpecs

        print_section("Available Devices")

        all_devices = DeviceSpecs.get_all_devices()

        device_list = sorted(all_devices.items())
        choices = [
            (i + 1, f"{spec.name} ({key})") for i, (key, spec) in enumerate(device_list)
        ]
        choices.append((len(choices) + 1, "Back to quick selection"))

        choice = prompt_choice(
            "Select a device:",
            choices,
            default=1,
        )

        if choice == len(choices):
            return None

        selected_key, _ = device_list[choice - 1]
        from .prompts import print_device_card

        print_device_card(selected_key, all_devices[selected_key])
        return selected_key


class FormatSelectionStep(WizardStep):
    """Format (LTR/RTL) selection step."""

    def execute(self, config: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Execute format selection step."""
        print_section("Format Selection")

        formats = [
            (1, "Right-to-Left (Japanese manga)"),
            (2, "Left-to-Right (Western comics)"),
        ]

        choice = prompt_choice(
            "Choose page orientation:",
            formats,
            default=1,
        )

        return {"rtl": choice == 1}


class PathsSelectionStep(WizardStep):
    """Source and destination path selection step."""

    def execute(self, config: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Execute paths selection step."""
        print_section("Select Directories")

        src_path = prompt_path(
            "Source directory (contains images to process):",
            default=str(Path.home() / "manga"),
            must_exist=True,
        )

        dest_path = prompt_path(
            "Destination directory (where to save processed files):",
            default=str(Path.home() / "manga_processed"),
            must_exist=False,
        )

        return {
            "src_dir": src_path,
            "dest_dir": dest_path,
        }


class QualitySelectionStep(WizardStep):
    """Quality level selection step."""

    def execute(self, config: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Execute quality selection step."""
        print_section("Quality Selection")

        print_info("Quality 1 = Fast (smaller files), 9 = Best (larger files)")

        quality = prompt_integer(
            "Quality level (default: 6):",
            default=6,
            min_val=1,
            max_val=9,
        )

        return {"quality": quality}


class PerformanceSelectionStep(WizardStep):
    """Performance (workers) selection step."""

    def execute(self, config: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Execute performance step."""
        print_section("Performance")

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
        from .prompts import print_config_review

        print_header("Configuration Review")
        print_config_review(config)

        return {}


class ConfirmationStep(WizardStep):
    """Final confirmation step."""

    def execute(self, config: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Execute confirmation step."""
        choices = [
            (1, "Proceed with processing"),
            (2, "Abort"),
            (3, "Modify configuration"),
            (4, "Save as profile"),
        ]

        choice = prompt_choice(
            "Ready to proceed?",
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
