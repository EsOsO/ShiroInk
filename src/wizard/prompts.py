"""
Helper functions for wizard user input and prompts.
"""

from typing import Any, Callable, Optional


def prompt_choice(
    prompt: str,
    choices: list[tuple[int, str]],
    default: Optional[int] = None,
) -> int:
    """
    Prompt user to choose from a list of options.

    Args:
        prompt: Prompt message
        choices: List of (number, description) tuples
        default: Default choice (if any)

    Returns:
        Selected choice number
    """
    print(f"\n{prompt}")
    print()

    for num, desc in choices:
        print(f"  {num}) {desc}")

    print()

    while True:
        if default is not None:
            user_input = input(f"→ Choice [{default}]: ").strip()
            if not user_input:
                return default
        else:
            user_input = input("→ Choice: ").strip()

        try:
            choice = int(user_input)
            if any(num == choice for num, _ in choices):
                return choice
            else:
                print(f"Invalid choice. Please select from the available options.")
        except ValueError:
            print(f"Please enter a valid number.")


def prompt_input(
    prompt: str,
    default: Optional[str] = None,
    validate: Optional[Callable[[str], Optional[str]]] = None,
) -> str:
    """
    Prompt user for text input.

    Args:
        prompt: Prompt message
        default: Default value (if any)
        validate: Optional validation function (returns error message or None)

    Returns:
        User input
    """
    print()

    while True:
        if default is not None:
            user_input = input(f"{prompt}\n→ [{default}]: ").strip()
            if not user_input:
                user_input = default
        else:
            user_input = input(f"{prompt}\n→ ").strip()

        if validate:
            error = validate(user_input)
            if error:
                print(f"❌ {error}")
                continue

        return user_input


def prompt_yes_no(
    prompt: str,
    default: bool = True,
) -> bool:
    """
    Prompt user for yes/no input.

    Args:
        prompt: Prompt message
        default: Default value (True for yes, False for no)

    Returns:
        Boolean user response
    """
    print()
    default_str = "y/N" if not default else "Y/n"
    user_input = input(f"{prompt} ({default_str}): ").strip().lower()

    if not user_input:
        return default

    return user_input[0] == "y"


def prompt_integer(
    prompt: str,
    default: Optional[int] = None,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None,
) -> int:
    """
    Prompt user for integer input.

    Args:
        prompt: Prompt message
        default: Default value (if any)
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        Integer user input
    """
    print()

    while True:
        if default is not None:
            user_input = input(f"{prompt}\n→ [{default}]: ").strip()
            if not user_input:
                return default
        else:
            user_input = input(f"{prompt}\n→ ").strip()

        try:
            value = int(user_input)

            if min_val is not None and value < min_val:
                print(f"❌ Value must be at least {min_val}")
                continue

            if max_val is not None and value > max_val:
                print(f"❌ Value must be at most {max_val}")
                continue

            return value
        except ValueError:
            print(f"❌ Please enter a valid integer")


def print_header(title: str) -> None:
    """Print a formatted header."""
    print(f"\n{'═' * 70}")
    print(f"  {title}")
    print(f"{'═' * 70}")


def print_section(title: str) -> None:
    """Print a formatted section title."""
    print(f"\n{title}")
    print(f"{'-' * len(title)}")


def print_success(message: str) -> None:
    """Print success message."""
    print(f"✓ {message}")


def print_warning(message: str) -> None:
    """Print warning message."""
    print(f"⚠️  {message}")


def print_error(message: str) -> None:
    """Print error message."""
    print(f"❌ {message}")


def print_info(message: str) -> None:
    """Print info message."""
    print(f"ℹ️  {message}")


def print_tip(message: str) -> None:
    """Print tip message."""
    print(f"💡 {message}")
