"""
Unit tests for the interactive wizard.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from interactive_wizard import InteractiveWizard
from wizard.steps import (
    DeviceSelectionStep,
    FormatSelectionStep,
    PathsSelectionStep,
    QualitySelectionStep,
    PerformanceSelectionStep,
)


@pytest.mark.unit
class TestInteractiveWizard:
    """Tests for InteractiveWizard class."""

    def test_wizard_initialization(self):
        """Test wizard initializes with profile manager."""
        wizard = InteractiveWizard()
        assert wizard.profile_manager is not None
        assert wizard._config == {}
        assert len(wizard._steps) == 7

    @patch("interactive_wizard.InteractiveWizard._prompt_save_profile")
    @patch("interactive_wizard.ConfirmationStep.execute")
    @patch("interactive_wizard.ReviewStep.execute")
    @patch("interactive_wizard.PerformanceSelectionStep.execute")
    @patch("interactive_wizard.QualitySelectionStep.execute")
    @patch("interactive_wizard.PathsSelectionStep.execute")
    @patch("interactive_wizard.FormatSelectionStep.execute")
    @patch("interactive_wizard.DeviceSelectionStep.execute")
    def test_wizard_run_success(
        self,
        mock_device,
        mock_format,
        mock_paths,
        mock_quality,
        mock_performance,
        mock_review,
        mock_confirmation,
        mock_save_profile,
    ):
        """Test successful wizard execution."""
        # Setup mock returns
        mock_device.return_value = {"device": "kindle_paperwhite"}
        mock_format.return_value = {"rtl": False}
        mock_paths.return_value = {
            "src_dir": "/input",
            "dest_dir": "/output",
        }
        mock_quality.return_value = {"quality": 6}
        mock_performance.return_value = {"workers": 4}
        mock_review.return_value = {}
        mock_confirmation.return_value = {"action": "proceed"}

        wizard = InteractiveWizard()
        result = wizard.run()

        assert result is not None
        assert result["device"] == "kindle_paperwhite"
        assert result["quality"] == 6
        mock_save_profile.assert_called_once()

    @patch("interactive_wizard.ConfirmationStep.execute")
    @patch("interactive_wizard.ReviewStep.execute")
    @patch("interactive_wizard.PerformanceSelectionStep.execute")
    @patch("interactive_wizard.QualitySelectionStep.execute")
    @patch("interactive_wizard.PathsSelectionStep.execute")
    @patch("interactive_wizard.FormatSelectionStep.execute")
    @patch("interactive_wizard.DeviceSelectionStep.execute")
    def test_wizard_run_cancelled(
        self,
        mock_device,
        mock_format,
        mock_paths,
        mock_quality,
        mock_performance,
        mock_review,
        mock_confirmation,
    ):
        """Test wizard cancellation."""
        mock_device.return_value = None

        wizard = InteractiveWizard()
        result = wizard.run()

        assert result is None

    def test_wizard_get_config_for_processing(self):
        """Test conversion to processing config format."""
        wizard = InteractiveWizard()
        wizard._config = {
            "src_dir": "/input",
            "dest_dir": "/output",
            "device": "kindle_paperwhite",
            "resolution": (1072, 1448),
            "quality": 6,
            "workers": 4,
            "rtl": False,
        }

        with patch.object(wizard, "run", return_value=wizard._config):
            config = wizard.get_config_for_processing()

        assert config is not None
        assert isinstance(config["src_dir"], Path)
        assert isinstance(config["dest_dir"], Path)
        assert config["device"] == "kindle_paperwhite"
        assert config["quality"] == 6

    def test_wizard_get_config_for_processing_cancelled(self):
        """Test processing config when wizard is cancelled."""
        wizard = InteractiveWizard()

        with patch.object(wizard, "run", return_value=None):
            config = wizard.get_config_for_processing()

        assert config is None

    @patch("wizard.prompts.prompt_choice")
    def test_prompt_which_step_to_modify(self, mock_choice):
        """Test prompting for step modification."""
        mock_choice.return_value = 2  # Paths step

        wizard = InteractiveWizard()
        result = wizard._prompt_which_step_to_modify()

        assert result == 2

    @patch("wizard.prompts.prompt_choice")
    def test_prompt_which_step_to_modify_cancel(self, mock_choice):
        """Test cancellation in step modification."""
        mock_choice.return_value = 5  # Cancel option

        wizard = InteractiveWizard()
        result = wizard._prompt_which_step_to_modify()

        assert result is None

    @patch("interactive_wizard.InteractiveWizard._prompt_save_profile")
    @patch("wizard.prompts.prompt_choice")
    @patch("interactive_wizard.ConfirmationStep.execute")
    @patch("interactive_wizard.ReviewStep.execute")
    @patch("interactive_wizard.PerformanceSelectionStep.execute")
    @patch("interactive_wizard.QualitySelectionStep.execute")
    @patch("interactive_wizard.PathsSelectionStep.execute")
    @patch("interactive_wizard.FormatSelectionStep.execute")
    @patch("interactive_wizard.DeviceSelectionStep.execute")
    def test_wizard_modify_step(
        self,
        mock_device,
        mock_format,
        mock_paths,
        mock_quality,
        mock_performance,
        mock_review,
        mock_confirmation,
        mock_choice,
        mock_save_profile,
    ):
        """Test modifying a step during wizard."""
        # First run
        mock_device.return_value = {"device": "kindle_basic"}
        mock_format.return_value = {"rtl": False}
        mock_paths.return_value = {"src_dir": "/input", "dest_dir": "/output"}
        mock_quality.return_value = {"quality": 6}
        mock_performance.return_value = {"workers": 4}
        mock_review.return_value = {}

        # First confirmation - ask to modify
        # Then modify device step
        # Then confirmation - proceed
        mock_confirmation.side_effect = [
            {"action": "modify"},
            {"action": "proceed"},
        ]
        mock_choice.return_value = 0  # Modify device step

        # Mock the modified device return
        with patch.object(
            DeviceSelectionStep,
            "execute",
            return_value={"device": "kindle_paperwhite"},
        ):
            wizard = InteractiveWizard()
            result = wizard.run()

        assert result is not None

    @patch("wizard.prompts.prompt_yes_no")
    @patch("wizard.prompts.prompt_input")
    def test_prompt_save_profile_yes(self, mock_input, mock_yes_no):
        """Test saving profile when user confirms."""
        mock_yes_no.return_value = True
        mock_input.return_value = "test-profile"

        wizard = InteractiveWizard()
        wizard._config = {
            "src_dir": "/input",
            "dest_dir": "/output",
            "quality": 6,
        }

        with patch.object(wizard.profile_manager, "save") as mock_save:
            wizard._prompt_save_profile()
            mock_save.assert_called_once()

    @patch("wizard.prompts.prompt_yes_no")
    def test_prompt_save_profile_no(self, mock_yes_no):
        """Test not saving profile."""
        mock_yes_no.return_value = False

        wizard = InteractiveWizard()

        with patch.object(wizard.profile_manager, "save") as mock_save:
            wizard._prompt_save_profile()
            mock_save.assert_not_called()
