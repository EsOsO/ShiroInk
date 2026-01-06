"""
Helper functions for wizard user input and prompts using Rich.
"""

from pathlib import Path
from typing import Callable, Optional

from rich.console import Console
from rich.prompt import Prompt, InvalidResponse
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box


console = Console()


def prompt_choice(
    prompt: str,
    choices: list[tuple[int, str]],
    default: Optional[int] = None,
) -> int:
    """
    Prompt user to choose from a list of options using Rich.
    """
    table = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
    table.add_column("Num", width=4, justify="right")
    table.add_column("Description")

    for num, desc in choices:
        if num == default:
            table.add_row(
                Text(str(num), style="bold green"),
                Text(desc, style="bold green"),
            )
        else:
            table.add_row(str(num), desc)

    console.print(
        Panel(
            table,
            title=prompt,
            subtitle="[dim]Press Enter for default[/]",
        )
    )

    while True:
        try:
            default_str = str(default) if default is not None else ""
            user_input = Prompt.ask("[bold]?[/]", default=default_str)

            if not user_input and default is not None:
                return default

            choice = int(user_input)
            valid_choices = [num for num, _ in choices]
            if choice in valid_choices:
                return choice
            else:
                console.print(
                    "[red]Invalid choice. Please select from the "
                    "available options.[/]"
                )
        except (ValueError, InvalidResponse):
            console.print("[red]Please enter a valid number.[/]")


def prompt_input(
    prompt: str,
    default: Optional[str] = None,
    validate: Optional[Callable[[str], Optional[str]]] = None,
) -> str:
    """
    Prompt user for text input using Rich.
    """
    while True:
        default_str = f"[dim]({default})[/]" if default else ""
        user_input = Prompt.ask(f"[bold]{prompt}[/] {default_str}").strip()

        if not user_input and default:
            user_input = default

        if validate:
            error = validate(user_input)
            if error:
                console.print(f"[red]✗ {error}[/]")
                continue

        return user_input


def prompt_yes_no(
    prompt: str,
    default: bool = True,
) -> bool:
    """
    Prompt user for yes/no input using Rich.
    """
    default_str = "[Y/n]" if default else "[y/N]"
    while True:
        user_input = Prompt.ask(
            f"[bold]{prompt}[/] {default_str}", default="y" if default else "n"
        )
        user_input = user_input.strip().lower()

        if not user_input:
            return default

        if user_input[0] == "y":
            return True
        elif user_input[0] == "n":
            return False

        console.print("[red]Please enter 'y' or 'n'.[/]")


def prompt_integer(
    prompt: str,
    default: Optional[int] = None,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None,
) -> int:
    """
    Prompt user for integer input using Rich.
    """
    while True:
        default_str = str(default) if default is not None else ""
        user_input = Prompt.ask(f"[bold]{prompt}[/]", default=default_str)

        try:
            value = int(user_input)

            if min_val is not None and value < min_val:
                console.print(f"[red]✗ Value must be at least {min_val}[/]")
                continue

            if max_val is not None and value > max_val:
                console.print(f"[red]✗ Value must be at most {max_val}[/]")
                continue

            return value
        except ValueError:
            console.print("[red]Please enter a valid integer[/]")


def prompt_path(
    prompt: str,
    default: Optional[str] = None,
    must_exist: bool = True,
) -> Path:
    """
    Prompt user for a directory path using Rich.
    """
    while True:
        default_str = str(default) if default else ""
        user_input = Prompt.ask(f"[bold]{prompt}[/]", default=default_str)

        if not user_input and default:
            user_input = str(default)

        path = Path(user_input).expanduser()

        if not path.exists():
            console.print(f"[red]✗ Path does not exist: {path}[/]")
            continue

        if must_exist and not path.is_dir():
            console.print(f"[red]✗ Not a directory: {path}[/]")
            continue

        console.print(f"[green]✓ {path}[/]")
        return path


def print_header(title: str) -> None:
    """Print a formatted header using Rich."""
    console.print(
        Panel(
            Text(title, justify="center", style="bold white on blue"),
            box=box.HEAVY,
            style="blue",
        )
    )


def print_section(title: str) -> None:
    """Print a formatted section title using Rich."""
    console.print(f"\n[bold cyan]{title}[/]")
    console.print(f"[cyan]{'─' * len(title)}[/]")


def print_success(message: str) -> None:
    """Print success message."""
    console.print(f"[green]✓ {message}[/]")


def print_warning(message: str) -> None:
    """Print warning message."""
    console.print(f"[yellow]⚠️  {message}[/]")


def print_error(message: str) -> None:
    """Print error message."""
    console.print(f"[red]✗ {message}[/]")


def print_info(message: str) -> None:
    """Print info message."""
    console.print(f"[blue]ℹ️  {message}[/]")


def print_tip(message: str) -> None:
    """Print tip message."""
    console.print(f"[magenta]💡 {message}[/]")


def print_config_review(config: dict[str, any]) -> None:
    """Print a nice configuration review table."""
    table = Table(box=box.ROUNDED, show_header=False)
    table.add_column("Setting", style="bold cyan", width=15)
    table.add_column("Value", style="white")

    def fmt_value(key: str) -> str:
        val = config.get(key)
        if val is None:
            return "[dim]Not set[/]"
        if isinstance(val, Path):
            return str(val)
        if isinstance(val, tuple):
            return f"{val[0]}×{val[1]}"
        return str(val)

    table.add_row("Device", fmt_value("device") or "[dim]Default[/]")
    table.add_row("Format", "RTL" if config.get("rtl") else "LTR")
    table.add_row("Source", fmt_value("src_dir"))
    table.add_row("Destination", fmt_value("dest_dir"))
    table.add_row("Quality", f"{config.get('quality', 6)} / 9")
    table.add_row("Workers", str(config.get("workers", 4)))

    console.print(Panel(table, title="[bold]Configuration Review[/]", style="blue"))


def print_device_card(device_key: str, spec) -> None:
    """Print a device information card."""
    table = Table(box=box.SIMPLE, show_header=False)
    table.add_column("Property", style="bold")
    table.add_column("Value")

    table.add_row("Name", spec.name)
    table.add_row("Resolution", f"{spec.resolution[0]}×{spec.resolution[1]}")
    table.add_row("Screen Size", f'{spec.screen_size_inches}"')
    table.add_row("Display", spec.display_type.value)
    table.add_row("Color", "Yes" if spec.color_support else "No")
    table.add_row("Pipeline", spec.recommended_pipeline)

    console.print(Panel(table, title=f"[bold]{device_key}[/]"))
