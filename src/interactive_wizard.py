"""
Interactive wizard coordinator for ShiroInk.

This module orchestrates the multi-step configuration wizard,
guiding users through device selection, format preferences, paths,
and quality settings to create a complete processing configuration.
"""

from typing import Any, Optional
from pathlib import Path

from wizard.prompts import print_header, print_section
from wizard.steps import (
    DeviceSelectionStep,
    FormatSelectionStep,
    PathsSelectionStep,
    QualitySelectionStep,
    PerformanceSelectionStep,
    ReviewStep,
    ConfirmationStep,
)
from profiles.manager import ProfileManager


class InteractiveWizard:
    """
    Orchestrates the interactive configuration wizard.

    This class manages the multi-step wizard process, allowing users to
    configure ShiroInk settings interactively. It supports modifying
    individual steps and saving configurations as profiles.

    Attributes:
        profile_manager: ProfileManager instance for saving profiles.
        _config: Accumulated configuration dictionary.
        _steps: List of wizard steps in order.
    """

    def __init__(self) -> None:
        """Initialize the wizard with profile manager."""
        self.profile_manager = ProfileManager()
        self._config: dict[str, Any] = {}
        self._steps = [
            DeviceSelectionStep(),
            FormatSelectionStep(),
            PathsSelectionStep(),
            QualitySelectionStep(),
            PerformanceSelectionStep(),
            ReviewStep(),
            ConfirmationStep(),
        ]

    def run(self) -> Optional[dict[str, Any]]:
        """
        Run the interactive wizard.

        Guides the user through all wizard steps, allowing modification
        of individual steps and saving of the final configuration.

        Returns:
            Configuration dictionary if user confirms, None if aborted.
        """
        print_header("ShiroInk Configuration Wizard")
        print()
        print_section("Let's configure ShiroInk for your manga processing needs.")
        print()

        while True:
            # Run through all steps
            step_index = 0
            while step_index < len(self._steps):
                step = self._steps[step_index]
                result = step.execute(self._config)

                if result is None:
                    # User cancelled
                    return None

                self._config.update(result)
                step_index += 1

            # Ask user to confirm or modify
            confirmation_step = ConfirmationStep()
            confirmation_result = confirmation_step.execute(self._config)

            if confirmation_result is None:
                # User cancelled
                return None

            action = confirmation_result.get("action")

            if action == "proceed":
                # User confirmed - save optional profile
                self._prompt_save_profile()
                return self._config

            elif action == "modify":
                # User wants to modify - show menu
                step_to_modify = self._prompt_which_step_to_modify()
                if step_to_modify is None:
                    continue

                # Re-run that step and update config
                modified_result = self._steps[step_to_modify].execute(self._config)
                if modified_result is not None:
                    self._config.update(modified_result)

            elif action == "abort":
                # User aborted
                return None

    def _prompt_which_step_to_modify(self) -> Optional[int]:
        """
        Prompt user which step to modify.

        Returns:
            Index of step to modify, or None if user cancels.
        """
        from wizard.prompts import prompt_choice

        print()
        print_section("Which setting would you like to modify?")
        print()

        step_names = [
            "Device Selection",
            "Format (LTR/RTL)",
            "Paths (Input/Output)",
            "Quality Level",
            "Performance (Threads)",
            "Cancel",
        ]

        choice = prompt_choice(step_names, "Choose an option")
        if choice == len(step_names) - 1:  # Cancel option
            return None

        return choice

    def _prompt_save_profile(self) -> None:
        """
        Prompt user if they want to save this configuration as a profile.
        """
        from wizard.prompts import prompt_yes_no, print_success

        print()
        if not prompt_yes_no("Save this configuration as a profile?"):
            return

        from wizard.prompts import prompt_input

        profile_name = prompt_input(
            "Profile name (e.g., 'my-kindle'):", validate_not_empty=True
        )

        try:
            # Convert paths to strings for storage
            config_to_save = self._config.copy()
            if "src_dir" in config_to_save:
                config_to_save["src_dir"] = str(config_to_save["src_dir"])
            if "dest_dir" in config_to_save:
                config_to_save["dest_dir"] = str(config_to_save["dest_dir"])

            self.profile_manager.save(profile_name, config_to_save)
            print_success(f"Profile '{profile_name}' saved successfully!")
        except Exception as e:
            from wizard.prompts import print_warning

            print_warning(f"Failed to save profile: {e}")

    def get_config_for_processing(self) -> Optional[dict[str, Any]]:
        """
        Get configuration suitable for processing.

        Converts wizard output to format expected by processing pipeline.

        Returns:
            Configuration dict or None if wizard was cancelled.
        """
        config = self.run()
        if config is None:
            return None

        # Convert to processing format
        return {
            "src_dir": Path(config["src_dir"]),
            "dest_dir": Path(config["dest_dir"]),
            "device": config.get("device"),
            "resolution": config.get("resolution"),
            "rtl": config.get("rtl", False),
            "quality": config.get("quality", 6),
            "workers": config.get("workers", 4),
        }
