"""Localization module for ShiroInk."""

from .loader import (
    Language,
    LocalizationManager,
    get_language,
    get_translation,
    set_language,
)

__all__ = [
    "Language",
    "LocalizationManager",
    "get_translation",
    "get_language",
    "set_language",
]
