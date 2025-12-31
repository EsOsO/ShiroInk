"""
Progress reporting abstraction for decoupling business logic from UI.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
from pathlib import Path
from rich.console import Console
from rich.table import Column
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TaskID,
)


class ProgressReporter(ABC):
    """Abstract interface for progress reporting and logging."""

    @abstractmethod
    def log(self, message: str, level: str = "info") -> None:
        """
        Log a message.

        Args:
            message: The message to log.
            level: The log level (info, warning, error, debug).
        """
        pass

    @abstractmethod
    def add_task(self, description: str, total: int) -> Any:
        """
        Add a new task to track.

        Args:
            description: Description of the task.
            total: Total number of items to process.

        Returns:
            Task ID or handle for updating progress.
        """
        pass

    @abstractmethod
    def update_task(self, task_id: Any, completed: Optional[int] = None) -> None:
        """
        Update task progress.

        Args:
            task_id: The task ID returned by add_task.
            completed: Number of completed items.
        """
        pass

    @abstractmethod
    def advance_task(self, task_id: Any, advance: int = 1) -> None:
        """
        Advance task progress by a certain amount.

        Args:
            task_id: The task ID returned by add_task.
            advance: Amount to advance by (default 1).
        """
        pass

    @abstractmethod
    def remove_task(self, task_id: Any) -> None:
        """
        Remove a task from tracking.

        Args:
            task_id: The task ID to remove.
        """
        pass

    @abstractmethod
    def __enter__(self) -> "ProgressReporter":
        """Context manager entry."""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> Optional[bool]:
        """Context manager exit."""
        pass


class ConsoleProgressReporter(ProgressReporter):
    """Rich console-based progress reporter."""

    def __init__(self):
        """Initialize the console progress reporter."""
        self.console = Console()
        self.progress = Progress(
            TextColumn(
                "[progress.description]{task.description}", table_column=Column(ratio=2)
            ),
            BarColumn(table_column=Column(ratio=3)),
            TextColumn(
                "[progress.percentage]{task.percentage:>3.0f}%",
                table_column=Column(ratio=1),
            ),
            TextColumn(
                "[progress.completed]{task.completed}/{task.total}",
                table_column=Column(ratio=1),
            ),
            TimeElapsedColumn(table_column=Column(ratio=1)),
            TimeRemainingColumn(table_column=Column(ratio=1)),
            transient=True,
        )
        self._active = False

    def log(self, message: str, level: str = "info") -> None:
        """Log a message to the console."""
        if level == "error":
            self.console.log(f"[bold red]{message}[/bold red]")
        elif level == "warning":
            self.console.log(f"[bold yellow]{message}[/bold yellow]")
        elif level == "debug":
            self.console.log(f"[dim]{message}[/dim]")
        else:
            self.console.log(message)

    def add_task(self, description: str, total: int) -> TaskID:
        """Add a new task to the progress bar."""
        return self.progress.add_task(description, total=total)

    def update_task(self, task_id: TaskID, completed: Optional[int] = None) -> None:
        """Update task progress."""
        self.progress.update(task_id, completed=completed)

    def advance_task(self, task_id: TaskID, advance: int = 1) -> None:
        """Advance task progress."""
        self.progress.advance(task_id, advance=advance)

    def remove_task(self, task_id: TaskID) -> None:
        """Remove a task from the progress bar."""
        self.progress.remove_task(task_id)

    def __enter__(self):
        """Enter the progress context."""
        self._active = True
        self.progress.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the progress context."""
        self._active = False
        return self.progress.__exit__(exc_type, exc_val, exc_tb)


class SilentProgressReporter(ProgressReporter):
    """Silent progress reporter for testing or non-interactive environments."""

    def __init__(self):
        """Initialize the silent progress reporter."""
        self._task_counter = 0
        self._tasks = {}

    def log(self, message: str, level: str = "info") -> None:
        """Silently ignore log messages."""
        pass

    def add_task(self, description: str, total: int) -> int:
        """Add a task (returns a simple integer ID)."""
        task_id = self._task_counter
        self._task_counter += 1
        self._tasks[task_id] = {
            "description": description,
            "total": total,
            "completed": 0,
        }
        return task_id

    def update_task(self, task_id: int, completed: Optional[int] = None) -> None:
        """Update task progress."""
        if task_id in self._tasks and completed is not None:
            self._tasks[task_id]["completed"] = completed

    def advance_task(self, task_id: int, advance: int = 1) -> None:
        """Advance task progress."""
        if task_id in self._tasks:
            self._tasks[task_id]["completed"] += advance

    def remove_task(self, task_id: int) -> None:
        """Remove a task."""
        if task_id in self._tasks:
            del self._tasks[task_id]

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        return False


class FileProgressReporter(ProgressReporter):
    """File-based progress reporter that writes to a log file."""

    def __init__(self, log_file: Path):
        """
        Initialize the file progress reporter.

        Args:
            log_file: Path to the log file.
        """
        self.log_file = log_file
        self._task_counter = 0
        self._tasks = {}
        self._file_handle = None

    def log(self, message: str, level: str = "info") -> None:
        """Write a log message to the file."""
        if self._file_handle:
            self._file_handle.write(f"[{level.upper()}] {message}\n")
            self._file_handle.flush()

    def add_task(self, description: str, total: int) -> int:
        """Add a task and log it."""
        task_id = self._task_counter
        self._task_counter += 1
        self._tasks[task_id] = {
            "description": description,
            "total": total,
            "completed": 0,
        }
        self.log(f"Task started: {description} (total: {total})", "info")
        return task_id

    def update_task(self, task_id: int, completed: Optional[int] = None) -> None:
        """Update task progress."""
        if task_id in self._tasks and completed is not None:
            self._tasks[task_id]["completed"] = completed
            task = self._tasks[task_id]
            self.log(
                f"Task progress: {task['description']} - {completed}/{task['total']}",
                "debug",
            )

    def advance_task(self, task_id: int, advance: int = 1) -> None:
        """Advance task progress."""
        if task_id in self._tasks:
            self._tasks[task_id]["completed"] += advance

    def remove_task(self, task_id: int) -> None:
        """Remove a task and log completion."""
        if task_id in self._tasks:
            task = self._tasks[task_id]
            self.log(f"Task completed: {task['description']}", "info")
            del self._tasks[task_id]

    def __enter__(self):
        """Open the log file."""
        self._file_handle = open(self.log_file, "a", encoding="utf-8")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the log file."""
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None
        return False
