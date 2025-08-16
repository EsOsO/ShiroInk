from rich.console import Console
from rich.table import Column
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


def create_progress() -> Progress:
    return Progress(
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


console = Console()
