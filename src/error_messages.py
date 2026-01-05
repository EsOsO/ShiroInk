"""
Enhanced error message formatting for ShiroInk.

This module provides utilities for displaying user-friendly error messages
with optional detailed information for debugging.
"""

from typing import Optional, Dict, Any


class ErrorFormatter:
    """
    Formats error messages for display to users.

    Provides concise error messages by default with option for verbose output.
    """

    # Error message templates
    MESSAGES = {
        "invalid_device": "Unknown device: {device}",
        "invalid_resolution": "Invalid resolution: {resolution}",
        "invalid_quality": "Quality must be between 1 and 9",
        "invalid_workers": "Workers must be a positive integer",
        "path_not_found": "Path not found: {path}",
        "path_not_readable": "Cannot read from path: {path}",
        "path_not_writable": "Cannot write to path: {path}",
        "invalid_profile": "Profile not found: {profile}",
        "no_input_files": "No compatible files found in: {path}",
        "processing_failed": "Processing failed: {reason}",
        "device_not_supported": "Device not supported: {device}",
    }

    def __init__(self, verbose: bool = False) -> None:
        """
        Initialize error formatter.

        Args:
            verbose: If True, show detailed error information.
        """
        self.verbose = verbose

    def format_error(
        self,
        error_type: str,
        **kwargs: Any,
    ) -> str:
        """
        Format an error message.

        Args:
            error_type: Type of error (key from MESSAGES).
            **kwargs: Values to interpolate into message template.

        Returns:
            Formatted error message.
        """
        if error_type not in self.MESSAGES:
            return f"Error: {error_type}"

        template = self.MESSAGES[error_type]
        try:
            return template.format(**kwargs)
        except KeyError:
            return template

    def format_validation_error(
        self,
        field: str,
        value: Any,
        reason: str,
        suggestion: Optional[str] = None,
    ) -> str:
        """
        Format a validation error message.

        Args:
            field: Field name that failed validation.
            value: Invalid value.
            reason: Reason validation failed.
            suggestion: Optional suggestion for fixing the error.

        Returns:
            Formatted validation error message.
        """
        message = f"Invalid {field}: {reason}"

        if suggestion:
            message += f"\nTip: {suggestion}"

        if self.verbose:
            message += f"\nReceived value: {value}"

        return message

    def format_file_error(
        self,
        filename: str,
        error_type: str,
        details: Optional[str] = None,
    ) -> str:
        """
        Format a file operation error message.

        Args:
            filename: Name of file that caused error.
            error_type: Type of file error ('read', 'write', 'not_found').
            details: Optional detailed error information.

        Returns:
            Formatted file error message.
        """
        messages = {
            "read": f"Cannot read file: {filename}",
            "write": f"Cannot write file: {filename}",
            "not_found": f"File not found: {filename}",
            "corrupt": f"File appears corrupted: {filename}",
        }

        message = messages.get(error_type, f"File error: {filename}")

        if details:
            message += f" ({details})"

        return message

    def format_processing_error(
        self,
        filename: str,
        step: str,
        error: str,
    ) -> str:
        """
        Format a processing pipeline error message.

        Args:
            filename: Name of file being processed.
            step: Pipeline step that failed.
            error: Error message from step.

        Returns:
            Formatted processing error message.
        """
        message = f"Error processing '{filename}' at {step} step: {error}"

        if self.verbose:
            message += "\nEnable --debug flag for more detailed information"

        return message

    def format_config_error(
        self,
        issue: str,
        suggestion: Optional[str] = None,
    ) -> str:
        """
        Format a configuration error message.

        Args:
            issue: Description of configuration issue.
            suggestion: Optional suggestion for fixing.

        Returns:
            Formatted configuration error message.
        """
        message = f"Configuration error: {issue}"

        if suggestion:
            message += f"\nSuggestion: {suggestion}"

        return message

    def format_device_error(
        self,
        device_key: str,
        reason: str,
        similar: Optional[str] = None,
    ) -> str:
        """
        Format a device-related error message.

        Args:
            device_key: Device key that caused error.
            reason: Reason the device caused error.
            similar: Optional similar device suggestion.

        Returns:
            Formatted device error message.
        """
        message = f"Device error for '{device_key}': {reason}"

        if similar:
            message += f"\nDid you mean: {similar}?"

        if self.verbose:
            message += "\nUse --list-devices to see available devices"

        return message


class ErrorSuggester:
    """
    Provides helpful suggestions for common errors.
    """

    SUGGESTIONS = {
        "path_not_found": "Check that the path exists and is accessible",
        "invalid_device": "Use --list-devices to see available device presets",
        "invalid_quality": "Choose a quality level between 1 (fast) and 9 (best)",
        "invalid_workers": "Use a positive integer (e.g., 4, 8)",
        "no_input_files": "Ensure the directory contains JPG, PNG, or WEBP files",
        "insufficient_space": "Free up disk space and try again",
        "permission_denied": "Check file permissions and try again",
    }

    @classmethod
    def get_suggestion(cls, error_type: str) -> Optional[str]:
        """
        Get suggestion for an error type.

        Args:
            error_type: Type of error.

        Returns:
            Suggestion string or None if no suggestion available.
        """
        return cls.SUGGESTIONS.get(error_type)

    @classmethod
    def suggest_for_device_error(cls, device_key: str) -> Optional[str]:
        """
        Suggest similar device for invalid device key.

        Args:
            device_key: Invalid device key.

        Returns:
            Similar device suggestion or None.
        """
        # This would integrate with ParameterValidator.suggest_similar_device
        # For now, return generic suggestion
        return "Use --list-devices to see available device presets"


def print_error(message: str, verbose: bool = False) -> None:
    """
    Print error message to console.

    Args:
        message: Error message to print.
        verbose: If True, include additional details.
    """
    from rich.console import Console

    console = Console()
    console.print(f"[red]Error:[/red] {message}")


def print_warning(message: str) -> None:
    """
    Print warning message to console.

    Args:
        message: Warning message to print.
    """
    from rich.console import Console

    console = Console()
    console.print(f"[yellow]Warning:[/yellow] {message}")


def print_success(message: str) -> None:
    """
    Print success message to console.

    Args:
        message: Success message to print.
    """
    from rich.console import Console

    console = Console()
    console.print(f"[green]✓[/green] {message}")
