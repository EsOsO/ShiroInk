"""
Localization system for ShiroInk.

Supports multi-language UI with auto-detection and fallback.
"""

import json
import os
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class Language(Enum):
    """Supported languages."""

    EN = "en"
    IT = "it"


class LocalizationError(Exception):
    """Raised when localization fails."""

    pass


class LocalizationManager:
    """Manages translations and language detection."""

    # Directory where translation files are stored
    LOCALES_DIR = Path(__file__).parent / "locales"

    # Default language
    DEFAULT_LANGUAGE = Language.EN

    def __init__(self):
        """Initialize localization manager."""
        self._language: Language = self._detect_language()
        self._translations: dict[str, Any] = {}
        self._load_translations()

    def _detect_language(self) -> Language:
        """
        Detect language from system settings.

        Priority:
        1. SHIROINK_LANG environment variable
        2. System locale settings
        3. Default to English

        Returns:
            Language enum value
        """
        # Check environment variable first
        env_lang = os.getenv("SHIROINK_LANG")
        if env_lang:
            try:
                return Language(env_lang.lower())
            except ValueError:
                pass  # Fall through to system detection

        # Try system locale detection
        import locale

        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                lang_code = system_locale.split("_")[0].lower()
                # Map common locale codes to our Language enum
                locale_map = {
                    "en": Language.EN,
                    "it": Language.IT,
                }
                if lang_code in locale_map:
                    return locale_map[lang_code]
        except Exception:
            pass  # Fall through to default

        return self.DEFAULT_LANGUAGE

    def _load_translations(self) -> None:
        """Load translation file for current language."""
        if self._language is None:
            self._language = self.DEFAULT_LANGUAGE

        lang_file = self.LOCALES_DIR / f"{self._language.value}.json"

        if not lang_file.exists():
            # Fallback to English if requested language not available
            if self._language != Language.EN:
                lang_file = self.LOCALES_DIR / "en.json"
                if not lang_file.exists():
                    raise LocalizationError(f"Language file not found: {lang_file}")
            else:
                raise LocalizationError(f"Language file not found: {lang_file}")

        try:
            with open(lang_file, "r", encoding="utf-8") as f:
                self._translations = json.load(f)
        except json.JSONDecodeError as e:
            raise LocalizationError(f"Invalid JSON in {lang_file}: {e}")
        except Exception as e:
            raise LocalizationError(f"Failed to load translations: {e}")

    def get(self, key: str, default: str = "") -> str:
        """
        Get translated string.

        Args:
            key: Translation key (e.g., "wizard.welcome")
            default: Default value if key not found

        Returns:
            Translated string or default
        """
        keys = key.split(".")
        value = self._translations

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        if isinstance(value, str):
            return value
        return default

    def get_language(self) -> Language:
        """Get current language."""
        return self._language

    def set_language(self, language: Language) -> None:
        """
        Set language and reload translations.

        Args:
            language: Language to switch to
        """
        self._language = language
        self._load_translations()


# Global instance
_manager = LocalizationManager()


def get_translation(key: str, default: str = "") -> str:
    """
    Get translated string using global manager.

    Args:
        key: Translation key
        default: Default if not found

    Returns:
        Translated string
    """
    return _manager.get(key, default)


def get_language() -> Language:
    """Get current language."""
    return _manager.get_language()


def set_language(language: Language) -> None:
    """Set current language."""
    _manager.set_language(language)
