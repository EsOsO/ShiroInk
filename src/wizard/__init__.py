"""Wizard module for ShiroInk interactive setup."""

from .steps import (
    ConfirmationStep,
    DeviceSelectionStep,
    FormatSelectionStep,
    PerformanceSelectionStep,
    PathsSelectionStep,
    QualitySelectionStep,
    ReviewStep,
    WizardStep,
)

__all__ = [
    "WizardStep",
    "DeviceSelectionStep",
    "FormatSelectionStep",
    "PathsSelectionStep",
    "QualitySelectionStep",
    "PerformanceSelectionStep",
    "ReviewStep",
    "ConfirmationStep",
]
