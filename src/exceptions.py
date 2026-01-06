"""
Custom exceptions for ShiroInk application.
"""

from pathlib import Path
from typing import Optional


class ShiroInkError(Exception):
    """Base exception for all ShiroInk errors."""

    def __init__(self, message: str, path: Optional[Path] = None):
        """
        Initialize the exception.

        Args:
            message: Error message.
            path: Optional path related to the error.
        """
        self.message = message
        self.path = path
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Format the error message."""
        if self.path:
            return f"{self.message}: {self.path}"
        return self.message


class ImageProcessingError(ShiroInkError):
    """Exception raised when image processing fails."""

    def __init__(
        self,
        message: str,
        path: Optional[Path] = None,
        step: Optional[str] = None,
        original_error: Optional[Exception] = None,
    ):
        """
        Initialize the exception.

        Args:
            message: Error message.
            path: Path to the image that failed.
            step: Processing step that failed.
            original_error: Original exception that caused this error.
        """
        self.step = step
        self.original_error = original_error
        super().__init__(message, path)

    def _format_message(self) -> str:
        """Format the error message."""
        msg = self.message
        if self.step:
            msg = f"{msg} (step: {self.step})"
        if self.path:
            msg = f"{msg}: {self.path}"
        if self.original_error:
            msg = (
                f"{msg} - {type(self.original_error).__name__}: "
                f"{str(self.original_error)}"
            )
        return msg


class CBZExtractionError(ShiroInkError):
    """Exception raised when CBZ extraction fails."""

    pass


class CBZCreationError(ShiroInkError):
    """Exception raised when CBZ creation fails."""

    pass


class InvalidConfigurationError(ShiroInkError):
    """Exception raised when configuration is invalid."""

    pass


class FileReadError(ShiroInkError):
    """Exception raised when reading a file fails."""

    def __init__(
        self,
        path: Path,
        original_error: Optional[Exception] = None,
    ):
        """
        Initialize the exception.

        Args:
            path: Path to the file that couldn't be read.
            original_error: Original exception that caused this error.
        """
        self.original_error = original_error
        message = "Failed to read file"
        super().__init__(message, path)

    def _format_message(self) -> str:
        """Format the error message."""
        msg = f"{self.message}: {self.path}"
        if self.original_error:
            msg = (
                f"{msg} - {type(self.original_error).__name__}: "
                f"{str(self.original_error)}"
            )
        return msg


class FileWriteError(ShiroInkError):
    """Exception raised when writing a file fails."""

    def __init__(
        self,
        path: Path,
        original_error: Optional[Exception] = None,
    ):
        """
        Initialize the exception.

        Args:
            path: Path to the file that couldn't be written.
            original_error: Original exception that caused this error.
        """
        self.original_error = original_error
        message = "Failed to write file"
        super().__init__(message, path)

    def _format_message(self) -> str:
        """Format the error message."""
        msg = f"{self.message}: {self.path}"
        if self.original_error:
            msg = (
                f"{msg} - {type(self.original_error).__name__}: "
                f"{str(self.original_error)}"
            )
        return msg


class RetryableError(ShiroInkError):
    """Exception for errors that can be retried."""

    def __init__(
        self,
        message: str,
        path: Optional[Path] = None,
        retry_count: int = 0,
        max_retries: int = 3,
    ):
        """
        Initialize the exception.

        Args:
            message: Error message.
            path: Path related to the error.
            retry_count: Current retry attempt.
            max_retries: Maximum number of retries.
        """
        self.retry_count = retry_count
        self.max_retries = max_retries
        super().__init__(message, path)

    def can_retry(self) -> bool:
        """Check if the operation can be retried."""
        return self.retry_count < self.max_retries
