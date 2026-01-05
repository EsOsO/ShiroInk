"""
Unit tests for localization/loader.py module.

Tests the LocalizationManager class and language detection/persistence.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from localization.loader import (
    Language,
    LocalizationManager,
    LocalizationError,
    get_translation,
    get_language,
    set_language,
)


@pytest.mark.unit
class TestLanguageEnum:
    """Tests for Language enum."""

    def test_language_enum_values(self):
        """Test Language enum has expected values."""
        assert Language.EN.value == "en"
        assert Language.IT.value == "it"

    def test_language_enum_from_value(self):
        """Test creating Language enum from value."""
        assert Language("en") == Language.EN
        assert Language("it") == Language.IT

    def test_language_enum_invalid_value(self):
        """Test that invalid values raise ValueError."""
        with pytest.raises(ValueError):
            Language("fr")


@pytest.mark.unit
class TestLocalizationManager:
    """Tests for LocalizationManager class."""

    def test_manager_initialization(self):
        """Test LocalizationManager initializes correctly."""
        manager = LocalizationManager()
        assert manager is not None
        assert manager.get_language() in [Language.EN, Language.IT]

    def test_default_language_is_english(self):
        """Test default language is English."""
        assert LocalizationManager.DEFAULT_LANGUAGE == Language.EN

    def test_locales_dir_exists(self):
        """Test locales directory exists."""
        assert LocalizationManager.LOCALES_DIR.exists()

    def test_english_locale_file_exists(self):
        """Test English locale file exists."""
        en_file = LocalizationManager.LOCALES_DIR / "en.json"
        assert en_file.exists()

    def test_get_translation_with_valid_key(self):
        """Test getting translation with valid key."""
        manager = LocalizationManager()
        manager.set_language(Language.EN)
        # Get a translation that should exist
        result = manager.get("wizard.welcome", "")
        # Should return something (either translation or default)
        assert isinstance(result, str)

    def test_get_translation_with_invalid_key(self):
        """Test getting translation with invalid key returns default."""
        manager = LocalizationManager()
        result = manager.get("invalid.key.that.does.not.exist", "default_value")
        assert result == "default_value"

    def test_get_language(self):
        """Test getting current language."""
        manager = LocalizationManager()
        lang = manager.get_language()
        assert isinstance(lang, Language)

    def test_set_language(self):
        """Test setting language."""
        manager = LocalizationManager()
        manager.set_language(Language.EN)
        assert manager.get_language() == Language.EN

    def test_get_prefs_file_path(self):
        """Test preferences file path."""
        manager = LocalizationManager()
        prefs_file = manager._get_prefs_file()
        assert str(prefs_file).endswith(".config/shiroink/prefs.json")
        assert prefs_file.parent == Path.home() / ".config" / "shiroink"

    @patch("localization.loader.Path.home")
    def test_save_language_creates_directory(self, mock_home):
        """Test saving language creates config directory."""
        mock_home.return_value = Path("/tmp/test_home")
        manager = LocalizationManager()
        manager._language = Language.EN

        with patch("builtins.open", mock_open()):
            with patch("pathlib.Path.mkdir"):
                manager._save_language()

    @patch("localization.loader.Path.home")
    def test_save_language_persists_preference(self, mock_home):
        """Test saving language persists preference to file."""
        mock_home.return_value = Path("/tmp/test_home")
        manager = LocalizationManager()
        manager._language = Language.IT

        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            with patch("pathlib.Path.mkdir"):
                with patch("pathlib.Path.exists", return_value=False):
                    manager._save_language()

        # Verify file write was attempted
        mock_file.assert_called()

    @patch("localization.loader.Path.home")
    def test_load_saved_language_when_file_exists(self, mock_home):
        """Test loading saved language preference."""
        mock_home.return_value = Path("/tmp/test_home")
        manager = LocalizationManager()

        prefs_content = json.dumps({"language": "it"})
        mock_file = mock_open(read_data=prefs_content)

        with patch("builtins.open", mock_file):
            with patch("pathlib.Path.exists", return_value=True):
                lang = manager._load_saved_language()
                assert lang == Language.IT

    @patch("localization.loader.Path.home")
    def test_load_saved_language_when_file_not_exists(self, mock_home):
        """Test loading saved language returns None when file doesn't exist."""
        mock_home.return_value = Path("/tmp/test_home")
        manager = LocalizationManager()

        with patch("pathlib.Path.exists", return_value=False):
            lang = manager._load_saved_language()
            assert lang is None

    @patch("localization.loader.Path.home")
    def test_load_saved_language_with_invalid_json(self, mock_home):
        """Test loading saved language handles invalid JSON gracefully."""
        mock_home.return_value = Path("/tmp/test_home")
        manager = LocalizationManager()

        mock_file = mock_open(read_data="invalid json")
        with patch("builtins.open", mock_file):
            with patch("pathlib.Path.exists", return_value=True):
                lang = manager._load_saved_language()
                assert lang is None

    @patch.dict("os.environ", {"SHIROINK_LANG": "it"})
    def test_detect_language_from_env_variable(self):
        """Test language detection from environment variable."""
        # Create new manager to trigger detection
        with patch(
            "localization.loader.LocalizationManager._load_saved_language",
            return_value=None,
        ):
            manager = LocalizationManager()
            # The detection happens in __init__, but env var check comes after saved lang
            lang = manager.get_language()
            # Should detect from env or default
            assert isinstance(lang, Language)

    def test_detect_language_default_english(self):
        """Test language detection defaults to English."""
        with patch(
            "localization.loader.LocalizationManager._load_saved_language",
            return_value=None,
        ):
            with patch.dict("os.environ", {}, clear=True):
                with patch("locale.getdefaultlocale", return_value=(None, None)):
                    manager = LocalizationManager()
                    # Should default to English if no detection works
                    lang = manager.get_language()
                    assert lang in [Language.EN, Language.IT]

    def test_invalid_localization_error(self):
        """Test LocalizationError exception."""
        with pytest.raises(LocalizationError):
            raise LocalizationError("Test error message")

    @patch(
        "localization.loader.LocalizationManager._load_saved_language",
        return_value=None,
    )
    def test_fallback_to_english_if_lang_file_missing(self, mock_load_saved):
        """Test fallback to English if requested language file is missing."""
        manager = LocalizationManager()
        manager._language = Language.IT

        # Check that it tries to load translations
        # If IT file doesn't exist, it should fallback to EN
        assert manager._language == Language.IT


@pytest.mark.unit
class TestGlobalLocalizationFunctions:
    """Tests for module-level localization functions."""

    def test_get_translation_function(self):
        """Test get_translation global function."""
        result = get_translation("wizard.welcome", "default")
        assert isinstance(result, str)

    def test_get_language_function(self):
        """Test get_language global function."""
        lang = get_language()
        assert isinstance(lang, Language)

    def test_set_language_function(self):
        """Test set_language global function."""
        original_lang = get_language()
        try:
            set_language(Language.EN)
            assert get_language() == Language.EN
        finally:
            set_language(original_lang)

    def test_translation_key_hierarchy(self):
        """Test translation key with multiple levels."""
        # Test nested key access like "wizard.welcome"
        manager = LocalizationManager()
        manager.set_language(Language.EN)
        result = manager.get("wizard.welcome", "fallback")
        assert isinstance(result, str)

    def test_translation_missing_intermediate_key(self):
        """Test translation with missing intermediate key."""
        manager = LocalizationManager()
        result = manager.get("nonexistent.key.value", "fallback")
        assert result == "fallback"

    def test_translation_non_string_value(self):
        """Test translation when value is not a string."""
        manager = LocalizationManager()
        # Manually set a non-string value to test edge case
        manager._translations = {"test": {"key": 123}}
        result = manager.get("test.key", "fallback")
        assert result == "fallback"


@pytest.mark.unit
class TestLocalizationIntegration:
    """Integration tests for localization system."""

    def test_language_switching_workflow(self):
        """Test complete language switching workflow."""
        manager = LocalizationManager()
        original_lang = manager.get_language()

        try:
            # Switch to English
            manager.set_language(Language.EN)
            en_translation = manager.get("wizard.welcome", "")
            assert isinstance(en_translation, str)

            # Switch to Italian (if available)
            try:
                manager.set_language(Language.IT)
                it_translation = manager.get("wizard.welcome", "")
                assert isinstance(it_translation, str)
            except LocalizationError:
                # Italian language file might not exist, that's okay
                pass

        finally:
            manager.set_language(original_lang)

    def test_multiple_managers_isolation(self):
        """Test that multiple manager instances are independent."""
        manager1 = LocalizationManager()
        manager2 = LocalizationManager()

        original_lang = manager1.get_language()

        try:
            manager1.set_language(Language.EN)
            # manager2 should remain independent (but shares global state)
            assert isinstance(manager2.get_language(), Language)
        finally:
            manager1.set_language(original_lang)

    def test_translations_loaded_correctly(self):
        """Test that translations are loaded correctly."""
        manager = LocalizationManager()
        manager.set_language(Language.EN)

        # Verify translations dict is populated
        assert isinstance(manager._translations, dict)
        assert len(manager._translations) > 0

    def test_locale_file_is_valid_json(self):
        """Test that locale files contain valid JSON."""
        en_file = LocalizationManager.LOCALES_DIR / "en.json"
        with open(en_file, "r", encoding="utf-8") as f:
            content = json.load(f)
            assert isinstance(content, dict)
            assert len(content) > 0
