"""
Error handling utilities including retry logic and error tracking.
"""

import time
from typing import Callable, TypeVar, Optional, List
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum

from exceptions import ShiroInkError, RetryableError


T = TypeVar("T")


class ErrorSeverity(Enum):
    """Error severity levels."""

    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ErrorRecord:
    """Record of an error that occurred during processing."""

    path: Optional[Path]
    error: Exception
    severity: ErrorSeverity
    step: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    retry_count: int = 0

    def __str__(self) -> str:
        """String representation of the error."""
        msg = f"[{self.severity.value.upper()}] {type(self.error).__name__}: {str(self.error)}"
        if self.step:
            msg = f"{msg} (step: {self.step})"
        if self.path:
            msg = f"{msg} - {self.path}"
        if self.retry_count > 0:
            msg = f"{msg} (retries: {self.retry_count})"
        return msg


class ErrorTracker:
    """Track errors that occur during processing."""

    def __init__(self):
        """Initialize the error tracker."""
        self.errors: List[ErrorRecord] = []
        self._file_errors: dict[Path, int] = {}
        self._step_errors: dict[str, int] = {}

    def add_error(
        self,
        error: Exception,
        path: Optional[Path] = None,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        step: Optional[str] = None,
        retry_count: int = 0,
    ) -> None:
        """
        Add an error to the tracker.

        Args:
            error: The exception that occurred.
            path: Path related to the error.
            severity: Severity level of the error.
            step: Processing step where error occurred.
            retry_count: Number of retries attempted.
        """
        record = ErrorRecord(
            path=path,
            error=error,
            severity=severity,
            step=step,
            retry_count=retry_count,
        )
        self.errors.append(record)

        # Track statistics
        if path:
            self._file_errors[path] = self._file_errors.get(path, 0) + 1
        if step:
            self._step_errors[step] = self._step_errors.get(step, 0) + 1

    def get_errors(
        self, severity: Optional[ErrorSeverity] = None
    ) -> List[ErrorRecord]:
        """
        Get all errors, optionally filtered by severity.

        Args:
            severity: Filter by this severity level.

        Returns:
            List of error records.
        """
        if severity is None:
            return self.errors.copy()
        return [e for e in self.errors if e.severity == severity]

    def has_errors(self) -> bool:
        """Check if any errors were recorded."""
        return len(self.errors) > 0

    def has_critical_errors(self) -> bool:
        """Check if any critical errors were recorded."""
        return any(e.severity == ErrorSeverity.CRITICAL for e in self.errors)

    def get_summary(self) -> dict:
        """
        Get a summary of all errors.

        Returns:
            Dictionary with error statistics.
        """
        return {
            "total_errors": len(self.errors),
            "warnings": len(self.get_errors(ErrorSeverity.WARNING)),
            "errors": len(self.get_errors(ErrorSeverity.ERROR)),
            "critical": len(self.get_errors(ErrorSeverity.CRITICAL)),
            "files_with_errors": len(self._file_errors),
            "most_problematic_file": (
                max(self._file_errors.items(), key=lambda x: x[1])
                if self._file_errors
                else None
            ),
            "errors_by_step": dict(self._step_errors),
        }

    def clear(self) -> None:
        """Clear all error records."""
        self.errors.clear()
        self._file_errors.clear()
        self._step_errors.clear()


def retry_on_error(
    func: Callable[..., T],
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
) -> Callable[..., T]:
    """
    Decorator to retry a function on error.

    Args:
        func: Function to retry.
        max_retries: Maximum number of retries.
        delay: Initial delay between retries in seconds.
        backoff: Multiplier for delay after each retry.
        exceptions: Tuple of exceptions to catch and retry on.

    Returns:
        Wrapped function with retry logic.
    """

    def wrapper(*args, **kwargs) -> T:
        current_delay = delay
        last_exception = None

        for attempt in range(max_retries + 1):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                last_exception = e
                if attempt < max_retries:
                    time.sleep(current_delay)
                    current_delay *= backoff
                else:
                    raise RetryableError(
                        f"Failed after {max_retries} retries",
                        retry_count=attempt,
                        max_retries=max_retries,
                    ) from last_exception

        # This should never be reached, but makes type checker happy
        raise last_exception  # type: ignore

    return wrapper


def safe_execute(
    func: Callable[..., T],
    error_tracker: Optional[ErrorTracker] = None,
    path: Optional[Path] = None,
    step: Optional[str] = None,
    severity: ErrorSeverity = ErrorSeverity.ERROR,
    default: Optional[T] = None,
    reraise: bool = False,
) -> Optional[T]:
    """
    Execute a function and track any errors.

    Args:
        func: Function to execute.
        error_tracker: Error tracker to record errors.
        path: Path related to the operation.
        step: Processing step name.
        severity: Error severity level.
        default: Default value to return on error.
        reraise: Whether to re-raise the exception after tracking.

    Returns:
        Function result or default value on error.

    Raises:
        Exception if reraise is True.
    """
    try:
        return func()
    except Exception as e:
        if error_tracker:
            error_tracker.add_error(
                error=e, path=path, severity=severity, step=step
            )
        if reraise:
            raise
        return default
