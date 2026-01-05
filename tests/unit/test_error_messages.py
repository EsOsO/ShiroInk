"""
Unit tests for error_messages.py module.

Tests the ErrorFormatter and ErrorSuggester classes,
as well as utility functions for error printing.
"""

import pytest
from io import StringIO
from unittest.mock import patch
from error_messages import (
    ErrorFormatter,
    ErrorSuggester,
    print_error,
    print_warning,
    print_success,
)


@pytest.mark.unit
class TestErrorFormatter:
    """Tests for ErrorFormatter class."""

    def test_init_default_verbose_false(self):
        """Test ErrorFormatter initializes with verbose=False by default."""
        formatter = ErrorFormatter()
        assert formatter.verbose is False

    def test_init_with_verbose_true(self):
        """Test ErrorFormatter can be initialized with verbose=True."""
        formatter = ErrorFormatter(verbose=True)
        assert formatter.verbose is True

    def test_format_error_basic(self):
        """Test basic error formatting with known error type."""
        formatter = ErrorFormatter()
        message = formatter.format_error("invalid_device", device="kindle_unknown")
        assert message == "Unknown device: kindle_unknown"

    def test_format_error_with_multiple_placeholders(self):
        """Test error formatting with multiple template placeholders."""
        formatter = ErrorFormatter()
        message = formatter.format_error("path_not_found", path="/tmp/missing")
        assert message == "Path not found: /tmp/missing"

    def test_format_error_unknown_type(self):
        """Test error formatting with unknown error type."""
        formatter = ErrorFormatter()
        message = formatter.format_error("unknown_error_type")
        assert message == "Error: unknown_error_type"

    def test_format_error_missing_kwargs(self):
        """Test error formatting when required kwargs are missing."""
        formatter = ErrorFormatter()
        message = formatter.format_error("invalid_device")
        # Should return template without replacement
        assert "Unknown device:" in message or "{device}" in message

    def test_format_validation_error_basic(self):
        """Test validation error formatting with basic info."""
        formatter = ErrorFormatter()
        message = formatter.format_validation_error(
            field="resolution",
            value="1920",
            reason="must be in WIDTHxHEIGHT format",
        )
        assert "Invalid resolution:" in message
        assert "must be in WIDTHxHEIGHT format" in message

    def test_format_validation_error_with_suggestion(self):
        """Test validation error formatting with suggestion."""
        formatter = ErrorFormatter()
        message = formatter.format_validation_error(
            field="quality",
            value="15",
            reason="out of range",
            suggestion="use a value between 1 and 9",
        )
        assert "Invalid quality:" in message
        assert "Tip: use a value between 1 and 9" in message

    def test_format_validation_error_verbose_includes_value(self):
        """Test that verbose mode includes the received value."""
        formatter = ErrorFormatter(verbose=True)
        message = formatter.format_validation_error(
            field="quality",
            value="15",
            reason="out of range",
        )
        assert "Received value: 15" in message

    def test_format_validation_error_non_verbose_no_value(self):
        """Test that non-verbose mode excludes the received value."""
        formatter = ErrorFormatter(verbose=False)
        message = formatter.format_validation_error(
            field="quality",
            value="15",
            reason="out of range",
        )
        assert "Received value: 15" not in message

    def test_format_file_error_read(self):
        """Test file error formatting for read errors."""
        formatter = ErrorFormatter()
        message = formatter.format_file_error(
            filename="image.jpg",
            error_type="read",
        )
        assert message == "Cannot read file: image.jpg"

    def test_format_file_error_write(self):
        """Test file error formatting for write errors."""
        formatter = ErrorFormatter()
        message = formatter.format_file_error(
            filename="output.jpg",
            error_type="write",
        )
        assert message == "Cannot write file: output.jpg"

    def test_format_file_error_not_found(self):
        """Test file error formatting for not found errors."""
        formatter = ErrorFormatter()
        message = formatter.format_file_error(
            filename="missing.jpg",
            error_type="not_found",
        )
        assert message == "File not found: missing.jpg"

    def test_format_file_error_corrupt(self):
        """Test file error formatting for corrupt file errors."""
        formatter = ErrorFormatter()
        message = formatter.format_file_error(
            filename="corrupt.jpg",
            error_type="corrupt",
        )
        assert message == "File appears corrupted: corrupt.jpg"

    def test_format_file_error_with_details(self):
        """Test file error formatting with additional details."""
        formatter = ErrorFormatter()
        message = formatter.format_file_error(
            filename="image.jpg",
            error_type="read",
            details="Permission denied",
        )
        assert message == "Cannot read file: image.jpg (Permission denied)"

    def test_format_file_error_unknown_type(self):
        """Test file error formatting with unknown error type."""
        formatter = ErrorFormatter()
        message = formatter.format_file_error(
            filename="image.jpg",
            error_type="unknown_type",
        )
        assert "File error: image.jpg" in message

    def test_format_processing_error_basic(self):
        """Test processing error formatting."""
        formatter = ErrorFormatter()
        message = formatter.format_processing_error(
            filename="image.jpg",
            step="quantize",
            error="invalid color space",
        )
        assert "Error processing 'image.jpg' at quantize step:" in message
        assert "invalid color space" in message

    def test_format_processing_error_verbose(self):
        """Test processing error includes debug suggestion in verbose mode."""
        formatter = ErrorFormatter(verbose=True)
        message = formatter.format_processing_error(
            filename="image.jpg",
            step="quantize",
            error="invalid color space",
        )
        assert "--debug flag" in message

    def test_format_processing_error_non_verbose(self):
        """Test processing error excludes debug suggestion in non-verbose mode."""
        formatter = ErrorFormatter(verbose=False)
        message = formatter.format_processing_error(
            filename="image.jpg",
            step="quantize",
            error="invalid color space",
        )
        assert "--debug flag" not in message

    def test_format_config_error_basic(self):
        """Test configuration error formatting."""
        formatter = ErrorFormatter()
        message = formatter.format_config_error(
            issue="conflicting options",
        )
        assert "Configuration error: conflicting options" in message

    def test_format_config_error_with_suggestion(self):
        """Test configuration error with suggestion."""
        formatter = ErrorFormatter()
        message = formatter.format_config_error(
            issue="--device and --resolution cannot be used together",
            suggestion="choose one option: either --device or --resolution",
        )
        assert "Configuration error:" in message
        assert "Suggestion:" in message
        assert "choose one option" in message

    def test_format_device_error_basic(self):
        """Test device error formatting."""
        formatter = ErrorFormatter()
        message = formatter.format_device_error(
            device_key="kindle_invalid",
            reason="not found",
        )
        assert "Device error for 'kindle_invalid': not found" in message

    def test_format_device_error_with_similar(self):
        """Test device error with similar device suggestion."""
        formatter = ErrorFormatter()
        message = formatter.format_device_error(
            device_key="kindle_paperwhte",
            reason="not found",
            similar="kindle_paperwhite",
        )
        assert "Device error for 'kindle_paperwhte'" in message
        assert "Did you mean: kindle_paperwhite?" in message

    def test_format_device_error_verbose(self):
        """Test device error includes list-devices suggestion in verbose mode."""
        formatter = ErrorFormatter(verbose=True)
        message = formatter.format_device_error(
            device_key="kindle_invalid",
            reason="not found",
        )
        assert "--list-devices" in message

    def test_format_device_error_non_verbose(self):
        """Test device error excludes list-devices suggestion in non-verbose mode."""
        formatter = ErrorFormatter(verbose=False)
        message = formatter.format_device_error(
            device_key="kindle_invalid",
            reason="not found",
        )
        assert "--list-devices" not in message

    def test_messages_dictionary_has_expected_keys(self):
        """Test that MESSAGES dictionary has expected error keys."""
        expected_keys = [
            "invalid_device",
            "invalid_resolution",
            "invalid_quality",
            "invalid_workers",
            "path_not_found",
            "path_not_readable",
            "path_not_writable",
            "invalid_profile",
            "no_input_files",
            "processing_failed",
            "device_not_supported",
        ]
        for key in expected_keys:
            assert key in ErrorFormatter.MESSAGES


@pytest.mark.unit
class TestErrorSuggester:
    """Tests for ErrorSuggester class."""

    def test_get_suggestion_valid_error_type(self):
        """Test getting suggestion for known error type."""
        suggestion = ErrorSuggester.get_suggestion("invalid_device")
        assert suggestion == "Use --list-devices to see available device presets"

    def test_get_suggestion_invalid_quality(self):
        """Test getting suggestion for invalid quality error."""
        suggestion = ErrorSuggester.get_suggestion("invalid_quality")
        assert "1 (fast)" in suggestion
        assert "9 (best)" in suggestion

    def test_get_suggestion_invalid_workers(self):
        """Test getting suggestion for invalid workers error."""
        suggestion = ErrorSuggester.get_suggestion("invalid_workers")
        assert "positive integer" in suggestion

    def test_get_suggestion_path_not_found(self):
        """Test getting suggestion for path not found error."""
        suggestion = ErrorSuggester.get_suggestion("path_not_found")
        assert "path exists" in suggestion

    def test_get_suggestion_no_input_files(self):
        """Test getting suggestion for no input files error."""
        suggestion = ErrorSuggester.get_suggestion("no_input_files")
        assert "JPG" in suggestion or "PNG" in suggestion

    def test_get_suggestion_insufficient_space(self):
        """Test getting suggestion for insufficient space error."""
        suggestion = ErrorSuggester.get_suggestion("insufficient_space")
        assert "disk space" in suggestion

    def test_get_suggestion_permission_denied(self):
        """Test getting suggestion for permission denied error."""
        suggestion = ErrorSuggester.get_suggestion("permission_denied")
        assert "permissions" in suggestion

    def test_get_suggestion_unknown_error(self):
        """Test getting suggestion for unknown error type returns None."""
        suggestion = ErrorSuggester.get_suggestion("unknown_error_type")
        assert suggestion is None

    def test_suggestions_dictionary_has_expected_keys(self):
        """Test that SUGGESTIONS dictionary has expected keys."""
        expected_keys = [
            "path_not_found",
            "invalid_device",
            "invalid_quality",
            "invalid_workers",
            "no_input_files",
            "insufficient_space",
            "permission_denied",
        ]
        for key in expected_keys:
            assert key in ErrorSuggester.SUGGESTIONS

    def test_suggest_for_device_error(self):
        """Test device error suggestion."""
        suggestion = ErrorSuggester.suggest_for_device_error("kindle_unknown")
        assert "list-devices" in suggestion or "--list-devices" in suggestion


@pytest.mark.unit
class TestPrintFunctions:
    """Tests for print_error, print_warning, and print_success functions."""

    @patch("rich.console.Console")
    def test_print_error(self, mock_console_class):
        """Test print_error function."""
        mock_console = mock_console_class.return_value
        print_error("Test error message")
        mock_console.print.assert_called_once()
        call_args = mock_console.print.call_args[0][0]
        assert "[red]Error:[/red]" in call_args
        assert "Test error message" in call_args

    @patch("rich.console.Console")
    def test_print_warning(self, mock_console_class):
        """Test print_warning function."""
        mock_console = mock_console_class.return_value
        print_warning("Test warning message")
        mock_console.print.assert_called_once()
        call_args = mock_console.print.call_args[0][0]
        assert "[yellow]Warning:[/yellow]" in call_args
        assert "Test warning message" in call_args

    @patch("rich.console.Console")
    def test_print_success(self, mock_console_class):
        """Test print_success function."""
        mock_console = mock_console_class.return_value
        print_success("Test success message")
        mock_console.print.assert_called_once()
        call_args = mock_console.print.call_args[0][0]
        assert "[green]✓[/green]" in call_args
        assert "Test success message" in call_args

    @patch("rich.console.Console")
    def test_print_error_with_special_characters(self, mock_console_class):
        """Test print_error with special characters."""
        mock_console = mock_console_class.return_value
        print_error("Error: /path/to/file.jpg (Permission denied)")
        mock_console.print.assert_called_once()

    @patch("rich.console.Console")
    def test_print_error_with_long_message(self, mock_console_class):
        """Test print_error with very long message."""
        mock_console = mock_console_class.return_value
        long_message = "A" * 200
        print_error(long_message)
        mock_console.print.assert_called_once()

    @patch("rich.console.Console")
    def test_print_error_verbose_parameter_ignored(self, mock_console_class):
        """Test that verbose parameter doesn't affect print_error."""
        mock_console = mock_console_class.return_value
        print_error("Test message", verbose=True)
        print_error("Test message", verbose=False)
        # Both should call print once
        assert mock_console.print.call_count == 2


@pytest.mark.unit
class TestErrorFormatterIntegration:
    """Integration tests combining multiple error formatting features."""

    def test_combined_error_handling_workflow(self):
        """Test a typical error handling workflow."""
        formatter = ErrorFormatter(verbose=True)
        suggester = ErrorSuggester()

        # Simulate device error workflow
        device_error = formatter.format_device_error(
            device_key="kindle_paperwhte",
            reason="Device not found in available presets",
            similar="kindle_paperwhite",
        )

        suggestion = suggester.get_suggestion("invalid_device")

        assert "Device error for 'kindle_paperwhte'" in device_error
        assert "kindle_paperwhite" in device_error
        assert suggestion is not None
        assert "--list-devices" in suggestion or "list-devices" in suggestion

    def test_validation_error_with_suggestion(self):
        """Test validation error with suggestion from suggester."""
        formatter = ErrorFormatter()
        suggester = ErrorSuggester()

        # Quality validation error
        validation_error = formatter.format_validation_error(
            field="quality",
            value="99",
            reason="must be between 1 and 9",
            suggestion=suggester.get_suggestion("invalid_quality"),
        )

        assert "Invalid quality:" in validation_error
        assert "Tip:" in validation_error

    def test_file_error_with_context(self):
        """Test file error with contextual information."""
        formatter = ErrorFormatter(verbose=False)

        # Read error with details
        error = formatter.format_file_error(
            filename="chapter_001.jpg",
            error_type="read",
            details="File size: 0 bytes (corrupted)",
        )

        assert "Cannot read file: chapter_001.jpg" in error
        assert "corrupted" in error

    def test_processing_error_full_context(self):
        """Test processing error with full context."""
        formatter = ErrorFormatter(verbose=True)

        error = formatter.format_processing_error(
            filename="page_042.jpg",
            step="quantize",
            error="Insufficient color space conversion depth",
        )

        assert "page_042.jpg" in error
        assert "quantize" in error
        assert "Insufficient color space conversion depth" in error
        assert "--debug" in error
